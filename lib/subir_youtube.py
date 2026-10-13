#!/usr/bin/env python3
"""Subir un vídeo a YouTube, o completar uno ya subido, a partir de una ficha TOML.

Modos:
  subir      FICHA IDIOMA            sube el mp4 y pone título, descripción, etiquetas,
                                     idioma, categoría, privacidad, subtítulos y lista
  actualizar FICHA IDIOMA [--id ID]  lo mismo sobre un vídeo ya subido (p. ej. a mano en
                                     YouTube Studio), sin tocar el mp4; el id sale de la
                                     ficha (campo `youtube`) si no se da
  ver        ID                      muestra título, descripción, subtítulos y listas
  listas                             todas las listas propias (también no listadas), con su id

La pantalla final (vídeo siguiente, suscripción) y las tarjetas no se pueden poner por la API:
se hacen en YouTube Studio (se puede copiar la pantalla final de otro vídeo del canal).

Ejemplos (desde la raíz del repositorio, con el entorno virtual de manim):
  ~/.venvs/manim/bin/python lib/subir_youtube.py subir fichas/L01_V05.toml es
  ~/.venvs/manim/bin/python lib/subir_youtube.py actualizar fichas/L01_V05.toml en --id SHu1-X0MWk0
  ~/.venvs/manim/bin/python lib/subir_youtube.py ver SG4ZwRAIQLY

Credenciales (una sola vez, en Google Cloud Console): proyecto con "YouTube Data API v3"
activada, pantalla de consentimiento OAuth con su cuenta como usuario de prueba, y un
"ID de cliente OAuth" de tipo aplicación de escritorio, descargado como
lib/client_secret_youtube.json (ignorado por git). La primera ejecución abre el navegador
para autorizar el canal y guarda lib/token_youtube.json (ignorado por git).

Aviso: los vídeos subidos por la API desde un proyecto que no ha pasado la auditoría de
cumplimiento de YouTube quedan en privado; mientras tanto, subir el mp4 a mano y usar
`actualizar` para el resto.

La ficha (TOML) tiene una sección por idioma; las rutas son relativas a la raíz del
repositorio. Véase fichas/L01_V05.toml.
"""
import argparse
import os
import sys
import tomllib

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_SECRET = os.path.join(RAIZ, "lib", "client_secret_youtube.json")
TOKEN = os.path.join(RAIZ, "lib", "token_youtube.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.force-ssl"]
NOMBRE_SUBTITULOS = {"es": "Español", "en": "English"}


def youtube():
    """Cliente autorizado de la API (abre el navegador la primera vez)."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET):
                sys.exit(f"Falta {CLIENT_SECRET} (ID de cliente OAuth de escritorio, Google Cloud Console)")
            creds = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES).run_local_server(port=0)
        with open(TOKEN, "w") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def lee_ficha(ruta, idioma):
    with open(ruta, "rb") as f:
        ficha = tomllib.load(f)
    comun = ficha.get("comun", {})
    if idioma not in ficha:
        sys.exit(f"La ficha {ruta} no tiene sección [{idioma}]")
    d = {**comun, **ficha[idioma]}
    d.setdefault("idioma", idioma)
    d.setdefault("categoria", "27")          # Educación
    d.setdefault("privacidad", "public")
    d.setdefault("etiquetas", [])
    for clave in ("video", "subtitulos", "miniatura"):
        if d.get(clave):
            d[clave] = os.path.join(RAIZ, d[clave])
    return d


def cuerpo(d):
    """snippet y status del vídeo según la ficha."""
    return {
        "snippet": {
            "title": d["titulo"],
            "description": d["descripcion"].strip(),
            "tags": d["etiquetas"],
            "categoryId": str(d["categoria"]),
            "defaultLanguage": d["idioma"],
            "defaultAudioLanguage": d["idioma"],
        },
        "status": {
            "privacyStatus": d["privacidad"],
            "selfDeclaredMadeForKids": False,
            "license": "youtube",
        },
    }


def sube_video(yt, d):
    from googleapiclient.http import MediaFileUpload

    if not os.path.exists(d["video"]):
        sys.exit(f"No existe el vídeo {d['video']}")
    media = MediaFileUpload(d["video"], chunksize=8 * 1024 * 1024, resumable=True)
    peticion = yt.videos().insert(part="snippet,status", body=cuerpo(d), media_body=media)
    print(f"Subiendo {os.path.basename(d['video'])} ({os.path.getsize(d['video']) // 2**20} MB)...")
    respuesta = None
    while respuesta is None:
        estado, respuesta = peticion.next_chunk()
        if estado:
            print(f"  {int(estado.progress() * 100):3d} %", end="\r", flush=True)
    print(f"Vídeo subido: https://youtu.be/{respuesta['id']}")
    return respuesta["id"]


def actualiza_metadatos(yt, d, video_id):
    body = cuerpo(d)
    body["id"] = video_id
    yt.videos().update(part="snippet,status", body=body).execute()
    print(f"Metadatos puestos en https://youtu.be/{video_id}: «{d['titulo']}»")


def pone_subtitulos(yt, d, video_id):
    from googleapiclient.http import MediaFileUpload

    if not d.get("subtitulos"):
        return
    if not os.path.exists(d["subtitulos"]):
        sys.exit(f"No existe el fichero de subtítulos {d['subtitulos']}")
    idioma = d["idioma"]
    # Declarar el formato SubRip y desactivar la sincronización: si no, YouTube toma el .srt
    # como transcripción sin tiempos y lo retemporiza él (comprobado 2026-10-12).
    media = MediaFileUpload(d["subtitulos"], mimetype="application/x-subrip", resumable=False)
    # La API no deja actualizar una pista existente (403): se borra y se vuelve a subir.
    for previa in yt.captions().list(part="snippet", videoId=video_id).execute().get("items", []):
        if previa["snippet"]["language"] == idioma:
            yt.captions().delete(id=previa["id"]).execute()
            print(f"Subtítulos ({idioma}) anteriores borrados")
    yt.captions().insert(part="snippet", media_body=media, sync=False,
                         body={"snippet": {"videoId": video_id, "language": idioma,
                                           "name": NOMBRE_SUBTITULOS.get(idioma, idioma),
                                           "isDraft": False}}).execute()
    print(f"Subtítulos ({idioma}) añadidos")


def id_de_lista(yt, lista):
    """Admite el identificador (PL...) o el título exacto de una lista propia."""
    if lista.startswith("PL") and " " not in lista:
        return lista
    pagina = None
    while True:
        r = yt.playlists().list(part="snippet", mine=True, maxResults=50, pageToken=pagina).execute()
        for pl in r.get("items", []):
            if pl["snippet"]["title"].strip().lower() == lista.strip().lower():
                return pl["id"]
        pagina = r.get("nextPageToken")
        if not pagina:
            sys.exit(f"No encuentro una lista propia titulada «{lista}»")


def pone_en_lista(yt, d, video_id):
    lista = d.get("lista")
    if not lista:
        return
    lista = id_de_lista(yt, lista)
    ya = yt.playlistItems().list(part="id", playlistId=lista, videoId=video_id).execute().get("items", [])
    if ya:
        print("Ya estaba en la lista de reproducción")
        return
    yt.playlistItems().insert(part="snippet", body={"snippet": {
        "playlistId": lista, "resourceId": {"kind": "youtube#video", "videoId": video_id}}}).execute()
    print(f"Añadido a la lista {lista}")


def pone_miniatura(yt, d, video_id):
    from googleapiclient.http import MediaFileUpload

    if d.get("miniatura") and os.path.exists(d["miniatura"]):
        yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(d["miniatura"])).execute()
        print("Miniatura puesta")


def listas(yt):
    """Todas las listas propias (incluidas las no listadas o privadas), con identificador."""
    pagina = None
    while True:
        r = yt.playlists().list(part="snippet,status,contentDetails", mine=True, maxResults=50, pageToken=pagina).execute()
        for pl in r.get("items", []):
            print(f"{pl['id']}  {pl['status']['privacyStatus']:8s} {pl['contentDetails']['itemCount']:3d} vídeos  {pl['snippet']['title']}")
        pagina = r.get("nextPageToken")
        if not pagina:
            return


def ver(yt, video_id):
    v = yt.videos().list(part="snippet,status,contentDetails", id=video_id).execute()["items"]
    if not v:
        sys.exit("No encuentro ese vídeo (¿es suyo y está autorizado el canal?)")
    s, st = v[0]["snippet"], v[0]["status"]
    print(f"Título: {s['title']}\nPrivacidad: {st['privacyStatus']}  idioma: {s.get('defaultAudioLanguage')}  "
          f"categoría: {s.get('categoryId')}  duración: {v[0]['contentDetails']['duration']}")
    print(f"Etiquetas: {s.get('tags')}")
    subs = yt.captions().list(part="snippet", videoId=video_id).execute().get("items", [])
    print("Subtítulos:", [(c["snippet"]["language"], c["snippet"]["name"]) for c in subs] or "ninguno")
    print("--- descripción ---\n" + s["description"])


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="modo", required=True)
    for modo in ("subir", "actualizar"):
        q = sub.add_parser(modo)
        q.add_argument("ficha")
        q.add_argument("idioma", choices=["es", "en"])
        if modo == "actualizar":
            q.add_argument("--id", help="identificador del vídeo ya subido (si falta, el campo `youtube` de la ficha)")
    q = sub.add_parser("ver")
    q.add_argument("id")
    sub.add_parser("listas")
    args = p.parse_args()

    yt = youtube()
    if args.modo == "ver":
        return ver(yt, args.id)
    if args.modo == "listas":
        return listas(yt)
    d = lee_ficha(args.ficha, args.idioma)
    if args.modo == "subir":
        video_id = sube_video(yt, d)
    else:
        video_id = args.id or d.get("youtube")
        if not video_id:
            sys.exit("Falta el identificador del vídeo: --id o el campo `youtube` en la ficha")
        actualiza_metadatos(yt, d, video_id)
    pone_subtitulos(yt, d, video_id)
    pone_en_lista(yt, d, video_id)
    pone_miniatura(yt, d, video_id)
    print("Hecho:", f"https://youtu.be/{video_id}")


if __name__ == "__main__":
    main()
