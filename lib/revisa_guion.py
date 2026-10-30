#!/usr/bin/env python3
"""Revisión automática del guion de un vídeo (pasada 2 de Comprobaciones.org).

Extrae la narración (los tr() dentro de self.voiceover) escena a escena, como el bloque
`guion` de los org, y señala lo que conviene mirar a mano. No corrige nada: cada aviso
es una pregunta para la revisión, no un error seguro.

Uso (desde la raíz del repositorio):
  python3 lib/revisa_guion.py lib/L01_V10_SeleccionYTransposicion.py
  python3 lib/revisa_guion.py lib/L01_V10_SeleccionYTransposicion.py --anterior lib/L01_V09_MatricesFilasYColumnas.py
  python3 lib/revisa_guion.py FICHERO.py --idioma en --ambiguas order,rank --max-palabras 22
"""
import argparse, ast, difflib, re, sys

# --- Extracción (misma lógica que el bloque `guion` de los org) -------------------------

def es_tr(n):
    return (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id == "tr" and len(n.args) >= 2)

def texto(n):
    try:
        return ast.literal_eval(n)
    except Exception:
        return ast.unparse(n)

def narracion(fichero, idx):
    """Lista de (escena, texto) de la narración del vídeo completo."""
    arbol = ast.parse(open(fichero, encoding="utf-8").read())
    construct = next(f for c in arbol.body if isinstance(c, ast.ClassDef)
                     for f in c.body if isinstance(f, ast.FunctionDef) and f.name == "construct")
    escena, salida = 0, []
    for stmt in construct.body:
        if ast.unparse(stmt).startswith("self.play(*[FadeOut(mob) for mob in self.mobjects])"):
            escena += 1
            continue
        for n in ast.walk(stmt):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "voiceover":
                for s in sorted((s for s in ast.walk(n) if es_tr(s)), key=lambda s: (s.lineno, s.col_offset)):
                    t = texto(s.args[idx])
                    if isinstance(t, str):
                        salida.append((escena, t))
    return salida

def limpia(t):
    """Quita marcas y SSML, y las comillas de las letras."""
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"'([a-zA-Z])'", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()

def frases(t):
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+", t) if f.strip()]

def palabras(f):
    return re.findall(r"[\wáéíóúüñÁÉÍÓÚÜÑ]+", f)

# --- Listas por idioma ----------------------------------------------------------------

CONECTORES = {
    "es": ["por eso", "así que", "por tanto", "es decir", "pero", "sin embargo", "además", "así,",
           "entonces", "pues", "en cambio", "aun así", "del mismo modo", "efectivamente", "y como"],
    "en": ["so ", "that is why", "therefore", "that is,", "but", "however", "moreover", "thus",
           "then", "instead", "even so", "likewise", "indeed", "and since"],
}
REFERENCIAS = {
    "es": ["la otra", "el otro", "los otros", "las otras", "esto", "eso", "esa", "ese", "esas", "esos",
           "esta", "este", "estas", "estos", "aquí", "ahí", "lo anterior"],
    "en": ["the other", "this", "that", "these", "those", "here", "there"],
}
NO_REFERENCIA = {   # giros fijos que contienen una de esas palabras sin ser una referencia
    "es": ["por eso", "de aquí sale", "por esto"],
    "en": ["that is", "so that", "that is why"],
}
VOZ = {   # riesgos de entonación medidos con Tristan y Ollie (CLAUDE.md)
    "es": [(r"[¿?]", "pregunta en la voz"), (r"^(Mire|Fíjese)\b", "«Mire»/«Fíjese» al empezar"),
           (r"\b(qué|cómo|cuál)\b", "interrogativo indirecto: ¿termina en el verbo?"),
           (r"\b[a-z]\s+más\s+[a-z]\b", "«X más Y»: ¿mejor «sumar X y Y»?")],
    "en": [(r"\?", "question in the voice"), (r"\bby property\b", "«by property N» pauses")],
}
AMBIGUAS = {"es": ["orden"], "en": ["order"]}

# --- Informe --------------------------------------------------------------------------

def informe(fichero, idioma, anterior, ambiguas, max_palabras):
    idx = 0 if idioma == "es" else 1
    datos = [(e, f) for e, t in narracion(fichero, idx) for f in frases(limpia(t))]
    avisos = []
    def aviso(e, tipo, frase, nota=""):
        avisos.append((e, tipo, frase, nota))

    previa = None
    for e, f in datos:
        n = len(palabras(f))
        baja = f.lower()
        if n > max_palabras:
            aviso(e, "LARGA", f, f"{n} palabras: ¿partirla?")
        for c in CONECTORES[idioma]:
            if baja.startswith(c) or baja.startswith(c.capitalize().lower()):
                aviso(e, "CONECTOR", f, f"«{c.strip(' ,')}»: ¿se sigue de: {previa!r}?" if previa else "")
                break
        sin_giros = baja
        for g in NO_REFERENCIA[idioma]:
            sin_giros = sin_giros.replace(g, " ")
        for r in REFERENCIAS[idioma]:
            if re.search(rf"\b{re.escape(r)}\b", sin_giros):
                aviso(e, "REFERENCIA", f, f"«{r}»: ¿antecedente claro solo con la voz?")
                break
        for w in ambiguas:
            if re.search(rf"\b{re.escape(w)}(es|s)?\b", baja):
                aviso(e, "AMBIGUA", f, f"«{w}»: ¿en qué sentido?")
        for patron, nota in VOZ[idioma]:
            if re.search(patron, f):
                aviso(e, "VOZ", f, nota)
        previa = f

    # Frases casi iguales dentro del vídeo (repetición) y respecto al vídeo anterior.
    # En la escena del resumen (la última con voz) repetir es lo esperado: solo se anota.
    ultima = max(e for e, _ in datos)
    for i, (ei, fi) in enumerate(datos):
        for ej, fj in datos[i+1:]:
            if len(palabras(fi)) > 5 and difflib.SequenceMatcher(None, fi.lower(), fj.lower()).ratio() > 0.75:
                aviso(ej, "REPITE", fj, f"se parece a (escena {ei}): {fi!r}" + ("  [resumen: normal]" if ej == ultima else ""))
    if anterior:
        previas = [f for _, t in narracion(anterior, idx) for f in frases(limpia(t))]
        for e, f in datos:
            for p in previas:
                if len(palabras(f)) > 5 and difflib.SequenceMatcher(None, f.lower(), p.lower()).ratio() > 0.7:
                    aviso(e, "YA CONTADO", f, f"en el vídeo anterior: {p!r}")
                    break

    # Salida: resumen por escena y avisos
    print(f"Guion de {fichero} ({idioma})\n")
    print("Escena  frases  palabras  ~segundos de voz")
    for e in sorted({e for e, _ in datos}):
        fs = [f for x, f in datos if x == e]
        n = sum(len(palabras(f)) for f in fs)
        print(f"{e:6}  {len(fs):6}  {n:8}  {n/2.5:8.0f}")
    total = sum(len(palabras(f)) for _, f in datos)
    print(f" total  {len(datos):6}  {total:8}  {total/2.5:8.0f}  (≈{total/2.5/60:.1f} min sin pausas)\n")
    for e, tipo, f, nota in sorted(avisos, key=lambda a: a[0]):
        print(f"[E{e}] {tipo:10} {f}")
        if nota:
            print(f"{'':16}→ {nota}")
    print(f"\n{len(avisos)} avisos: son preguntas para la revisión, no errores seguros.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichero")
    ap.add_argument("--idioma", choices=["es", "en"], default="es")
    ap.add_argument("--anterior", help="py del vídeo anterior, para detectar lo ya contado")
    ap.add_argument("--ambiguas", help="palabras con doble sentido en este vídeo, separadas por comas")
    ap.add_argument("--max-palabras", type=int, default=22)
    a = ap.parse_args()
    amb = a.ambiguas.split(",") if a.ambiguas else AMBIGUAS[a.idioma]
    informe(a.fichero, a.idioma, a.anterior, amb, a.max_palabras)
