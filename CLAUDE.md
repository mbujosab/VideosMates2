# VideosMates2 — vídeos con Manim para Matemáticas II (GECO, UCM)

Vídeos que siguen el libro *Curso de Álgebra Lineal* (fuentes en
`../CursoDeAlgebraLineal-SRC/partes/`). **Toda la fuente está aquí**: los org bilingües
(desde V05) y, en `en/`, los org en inglés de V01-V04 (anteriores a la fuente bilingüe) y el
prompt de traducción. `../videoMath2` es solo la **carpeta de salida del inglés** (py del tangle,
caché de Azure de Ollie, mp4 y srt); su git está congelado desde el 2026-10-30 (no hacer commits
allí; `LEEME.txt`).

## Antes de escribir cualquier escena

Leer `NotacionNacal.org`: convenios del libro, macros de `nacal.sty`,
cuenta de glifos de `MathTex`, API del módulo `nacal` y terminología
inglesa ya fijada. Las fórmulas y narraciones deben respetar esa
notación (vectores entre paréntesis, matrices entre corchetes, operador
selector, "componente a componente", etc.).

## Flujo de trabajo

- Un fichero org por vídeo (`L01-V05-Nombre.org`; plan de la lección 1 en
  `NotacionNacal.org`: V05 reales con regla y compás, V06 vectores
  especiales y propiedades de la suma, V07 propiedades del producto por
  escalares, ..., V12), programación literaria
  y **fuente única bilingüe**. Plantilla: `LXX-VYY-NombreVideo.org`.
  Cada escena es un chunk con nombre que reutilizan la clase del vídeo
  completo y las clases `LXX_VYY_Enn_*` (chunk "Clases de las escenas").
- El código común (carga de librerías, `LANG`, `tr`, voces, colores,
  `myTemplate`, `MiEscenaConVoz`, tarjeta de pausa, créditos,
  VectorR2/R3) vive en `Comunes.org`, que tangle `lib/vm2comun.py` en
  `lib/` y en `../videoMath2/lib/` (solo difieren en `LANG`). Cada vídeo hace
  `from vm2comun import *` y declara `class ZCreditosFinales(CreditosFinales): pass`
  (manim solo renderiza clases definidas en el fichero del vídeo). Si se
  cambia algo común: tangle `Comunes.org` y todos los vídeos lo heredan.
- Bilingüe: toda narración y texto en pantalla se escribe
  `tr("español", "English")`; las fórmulas nacal son comunes. El tangle
  genera dos py: `./lib/<Nombre>.py` (LANG="es") y
  `../videoMath2/lib/<EnglishName>.py` (LANG="en"). La voz la fija
  `MiEscenaConVoz.setup()` (llama a `self.voz()`), así que las clases de
  escena solo contienen `<<N escena>>`; `VOZ=gtts` en el entorno usa
  Google en vez de Azure. `myTemplate` (TexTemplate con nacal) se define
  una vez a nivel de módulo.
- Para revisar la narración sin leer código: bloque `guion` del org
  (`#+call: guion(fichero=..., idioma="es"|"en")`), que extrae los
  `tr()` escena por escena (narración en prosa, textos de pantalla entre
  corchetes). Útil también para la descripción o subtítulos del vídeo.
- Los chunks que contienen referencias noweb anidadas deben llevar
  `:noweb no-export` (con `:noweb tangle` la recursión no expande).
- Tangle en batch:
  `emacs --batch -l org --eval '(org-babel-tangle-file "FICHERO.org")'`.
- Renderizar desde `lib/` (o `../videoMath2/lib/`) con el entorno virtual:
  `VOZ=gtts ~/.venvs/manim/bin/manim -ql FICHERO.py NombreDeClase --disable_caching`
  (`-qh` para 1080p60). Salida en `lib/media/videos/<fichero>/<calidad>/`.
- La portada es la escena 0 (clase `LXX_VYY_E00_Portada`, sin voz). El
  vídeo final se monta con el bloque `montaje` del org a partir de los mp4
  de las escenas (nunca con `-c copy`: manim genera el audio unas décimas
  más largo que la imagen y la concatenación sin recodificar deja un parón
  en cada unión). `montaje` iguala cada segmento, concatena recodificando,
  lleva la voz a -16 LUFS con una ganancia fija medida sobre toda la voz más un limitador (desde V08, 2026-10-26: `loudnorm` en una pasada sube la ganancia poco a poco y la primera frase quedaba 5 dB más baja; V05-V07 publicados lo tienen; aplicado también a V09, que se volvió a montar, a V10 y a la plantilla), pone música solo en la portada (fundido al
  empezar la escena 1) y desde la escena `cierre` hasta el fundido a negro,
  y fusiona los `.srt` de las escenas en un único `video.srt` para YouTube.
- Web: cada vídeo publicado lleva su entrada en `README.org` (python, html
  del org, enlaces a YouTube es/en) y su org exportado a html. El org del
  vídeo se exporta en batch con htmlize cargado (`emacs --batch -l
  lib/exporta.el --visit=FICHERO.org -f org-html-export-to-html`, desde la raíz;
  `lib/exporta.el` añade `~/.emacs.d/elpa/htmlize-*` al load-path y no evalúa
  bloques); sale igual que el de V05. El `index.html`, en cambio, **no** se reexporta en
  batch: el tema de la web (estilo UCM, `worg.css` incrustado) solo sale
  con `C-c C-e h h` desde el Emacs abierto de Marcos (su configuración
  `~/.emacs.d`, no scimax); cargar ese `init.el` en batch no lo reproduce
  (probado 2026-10-17: algo de la sesión interactiva lo pone).
  Se le añade la entrada a mano copiando la anterior, o lo exporta Marcos.
- Comprobar visualmente: extraer fotogramas con ffmpeg (bloque
  `fotogramas`, en especial alrededor de cada unión) y mirarlos.
- **Antes de enseñar un vídeo a Marcos, y tras cada retoque de la narración, repasar
  `Comprobaciones.org`** (seis pasadas: contenido, lenguaje, ritmo, imagen, audio y entrega, y publicación en
  abierto, esta última añadida el 2026-11-02: licencia CC BY-SA 4.0 y música en créditos y descripción, fuentes
  de datos, línea fija sobre la notación, enlaces de navegación, título «Tema | Álgebra lineal 1.9», miniatura,
  pantalla final, prueba de radio y de mudo, un alumno real, ver el vídeo subido, erratas con comentario fijado;
  la de lenguaje empieza con `python3 lib/revisa_guion.py lib/FICHERO.py --anterior lib/ANTERIOR.py`).
  Nació el 2026-10-29 de una frase rota en V09 que llegó hasta el HD aprobado.

## Entorno

- `~/.venvs/manim`: manim 0.21.0, manim-voiceover 0.4.0 (azure, gtts,
  translate), nacal, sympy, ipython, opencv. El manim 0.19 del usuario
  sigue en `~/.local` por si hay que regenerar vídeos antiguos.
- `lib/.env` (ignorado por git) contiene las claves de Azure y DeepL.
  Nunca copiar claves a ficheros versionados ni a la salida.
- Voces: Azure `es-ES-Tristan:DragonHDLatestNeural` (ES) y
  `en-GB-Ollie:DragonHDLatestNeural` (EN), elegidas el 2026-10-12 entre
  ocho voces de cada idioma (V01-V04 llevan Álvaro y Ryan). Ollie por su
  ritmo pausado: el grupo en inglés no es angloparlante. Para pruebas
  usar `GTTSService` (gratis): Azure cobra por carácter y la caché
  `lib/media/voiceovers/cache.json` evita resintetizar. Las voces HD ya
  pausan solas en los dos puntos (`BREAK_DOS_PUNTOS` vacío) y devuelven
  límites de palabra, que es lo que hace funcionar las marcas; Marta
  (MAI) no los devuelve. Mayúsculas descartadas para las letras: en las
  lecciones siguientes la mayúscula es una matriz.

## Letras sueltas en la narración (a, b, c): casuística medida 2026-10-12

Las voces HD deciden por contexto y **no son deterministas**: la misma
frase sintetizada seis veces dio la 'a' en 10, 30, 10, 340, 340 y 40 ms.
No hay reglas fijas por frase; hay posiciones seguras, posiciones malas
y un procedimiento. Medir siempre sobre el audio (duración de la letra
con las marcas de palabra de Azure y la envolvente del mp3):
`tmp/analiza_letras.py` (una escena, tres formas por letra) y
`tmp/optimiza_letras_en.py` (todas las frases, combinaciones de
comillas, usa la caché real para que el audio elegido sea el del vídeo).

- **Posiciones seguras** (la letra sale entera casi siempre): delante
  de coma o punto ("el opuesto de a,", "the number 'a'."), tras "de"/"of"
  o "the number", y "la suma, 'a' más b" / "the sum, 'a' plus 'b'".
- **Posiciones malas**: letra pegada a un verbo o a una preposición
  débil ("sumar a", "add a", "move segment b", "at a plus b"), 'a'
  delante de "hay" u otra vocal (Tristan la enlaza: "a hay" suena "ar"),
  "a a" (preposición + letra: se funden), "ab" escrito junto (se lee
  como sílaba: decir "a por b" o, a final de frase, entrecomillar),
  "cero. a" (Tristan lee "punto": entrecomillar la letra), y dos letras
  entrecomilladas seguidas ("'a' y 'b'": añade pausas).
- **Comillas simples**: en español, Tristan lee bien casi todas las 'a'
  sin ellas y solo las necesita delante de "más"; en inglés las comillas
  arreglan la mitad de los sitios y no empeoran; `b` y `c` casi nunca
  las necesitan. Nunca entrecomillar la preposición/artículo. No llegan
  al subtítulo. `say-as characters` lo ignoran las voces HD.
- **Pausas**: Tristan y Ollie pausan solos en los dos puntos (sin
  `<break>`); una coma basta para una pausa breve; evitar "Mire" y
  "Fíjese" al principio de frase (Tristan los entona como interjección
  con 250-500 ms de silencio detrás; "Observe ahora" no).
- **Procedimiento**: escribir la frase con las letras en posiciones
  seguras; medir; si una letra sale corta, probar comillas y
  reformulación; si la frase es buena pero la toma salió mal,
  **repetir la tirada** añadiendo al final una marca invisible
  (`<bookmark mark='v2'/>`: cambia la clave de la caché, no el audio
  pedido) y quedarse con la mejor toma. Umbral práctico: 150 ms.

## Frases que Tristan entona mal (V06, 2026-10-14)

Lo que Marcos oyó mal al escuchar V06 con Azure, y la versión que funcionó.
Escribir las frases nuevas ya en la forma buena.

- **Nada de preguntas en la voz**, ni directas ni encadenadas ("¿Son
  estos...? ¿O son...?"): reformular en afirmativo con "podría(n)":
  "Estos comportamientos podrían ser una característica particular de
  los ejemplos, o propiedades generales." La pregunta va en pantalla.
- **Interrogativa indirecta con complemento detrás del verbo**: "da
  igual qué pareja sumemos primero" pausa 350-580 ms antes de "primero",
  que suena aislado. Terminar la frase en el verbo: "da igual por qué
  pareja empecemos" (0 ms en todas las tiradas). En general, no dejar un
  adverbio o complemento corto colgando detrás de "qué ... + subjuntivo".
- **"Un vector más su opuesto da..."** (el "más" de fórmula entre
  sustantivos) se entona mal; con verbo suena natural: "sumar un vector y
  su opuesto da un vector nulo". Mejor el verbo "sumar" que el "más"
  leído, salvo entre letras. Confirmado con números: "un número más su
  opuesto es cero" pausa 210-380 ms antes de "su" en las tres tiradas;
  "sumar un número y su opuesto da cero", 0 ms.
- **Letra vocal (a, i) junto a otra vocal = sinalefa**, aunque haya coma
  en medio: "Como i es" suena "comoi"; "cualquier i, 'a' más" funde la
  'i' con la 'a'; "Por tanto, 'a'" se traga la 'a' (20-70 ms). Poner
  delante de la letra una palabra acabada en consonante ("cualquier i",
  "Así pues, 'a' más") y detrás un punto ("Esto vale para cualquier i.
  Por tanto, ..."). Fórmula definitiva de las conclusiones (V06 y V07): sin letra
  suelta, "Como esto es cierto para cualquier componente del vector, los
  dos vectores son iguales" / "..., 'a' más el vector nulo es a" ('a' tras
  coma, medida 200-220 ms); en inglés "Since this holds for any component
  of the vector, ...".
  Y la 'i' sola delante de una pausa larga (dos puntos) suena "ie" aunque
  dure 210 ms ("para cualquier i: así..."): mejor nombrar la cosa
  ("para cualquier componente:") y dejar la letra en pantalla.
  La duración de la 'i' se mide mejor con las marcas de palabra de Azure
  (`duration_milliseconds` y hueco hasta la siguiente) que con la
  envolvente, que la mezcla con la pausa del punto.
- **"para cualquier i." al final de frase** suena "cualquiera i" o "cualquier ei" aunque la 'i'
  dure 200 ms (Marcos, V06 y V07, 2026-10-15): repetir la tirada no lo arregla. Funcionan
  "sea cual sea i." (la elegida en V07), "para cualquier 'i'." y "sea cual sea el índice i.".
  No sustituirla por "en todas las posiciones": diría que el vector es constante.
- **Ollie: "And by property three/eight of the reals we can..."** pausa 220-270 ms
  entre "property" y el número en todas las tiradas (Marcos lo oyó en V06 y V07).
  Funciona "And property eight of the reals lets us drop the one." (0 ms; queda
  una pausa natural tras "of the reals"). Ya no queda ningún "by property N" en
  los vídeos en inglés.
- **Órdenes "n por m"** (V10, 2026-11-01): Tristan dijo "m por m" en "es de orden n por m" (la n
  delante de "por" se asimila a m), y la m final sonaba "meme". Funcionó entrecomillar las dos
  letras, "es de orden 'n' por 'm'", eligiendo de oído una de tres tiradas. Escribir así los órdenes
  desde el principio y que Marcos escuche las tomas: la duración de la letra no lo detecta.
  En inglés (V12, 2026-11-04), Ollie funde «'n' columns» en «ncolumns» (n de 120 ms en todas las tiradas, también
  con «and with»): decir «of order 'm' by 'n'» (n 240-280 ms; Marcos: «se entiende»). `tmp/parte_toma.py` parte una
  toma por palabras en dos entradas de caché para resintetizar solo una frase de un voiceover.
- Las letras a final de frase ("las de a.") quedan en 110-150 ms en todas
  las tiradas: es la caída natural del final, no hace falta perseguirla.
- Cuando algo "suena raro", **medirlo**: `tmp/huecos.py` (silencio
  delante de cada palabra), `tmp/mide_cache.py` (duración de letras o
  palabras sobre las tomas reales de la caché), `tmp/tiradas.py` (N
  tiradas de una frase en `tmp/pruebas_azure/v06`; la primera, sin marca,
  tiene la misma clave que el render, así que se puede copiar a
  `lib/media/voiceovers` con su entrada de `cache.json` sin pagar otra
  vez). Probar 3-4 redacciones con tres tiradas cada una: distingue una
  toma mala (otra tirada lo arregla) de una frase mala (falla siempre).
- Tras sintetizar frases nuevas, pasar `tmp/pausas_raras.py CACHE [horas]`:
  lista los silencios >= 300 ms entre palabras sin puntuación. Los de
  enumeración ("..., y") son normales; uno de 500-700 ms antes de la
  última palabra ("sumemos | primero", "factor it | out") es el fallo
  que se oye: repetir la tirada y, si persiste, reformular. Si la toma
  buena es la primera tirada (sin marca), sustituye a la mala en la
  caché real con el mismo nombre y sin tocar el org.
- **Mover una marca sin pagar ni perder la toma aprobada**: la clave de
  la caché es el texto con marcas *y* el SSML, y quitar una marca deja
  sus espacios en el SSML, así que moverla cambia la clave y Azure
  sintetiza una toma nueva (distinta). Para conservar la buena: renderizar
  una vez (crea la entrada nueva), copiar en la entrada de la toma buena
  el `input_text` nuevo y el `ssml` nuevo (en `ssml` y en
  `input_data.ssml`) y dejarla en `cache.json` antes que la nueva (gana la
  primera coincidencia). Hecho en las conclusiones de V06 (2026-10-14). Script: `tmp/injerta_marca.py CACHE
  "inicio del texto" "<bookmark mark='x'/>"` (render, injerto, render). Ojo (2026-11-03): `cache.json` acumula
  una entrada repetida, con el mismo mp3, cada vez que un render reutiliza una toma (unas 7.000 entradas por
  idioma para 1.250 mp3), y tras un injerto queda además la toma sobrante con el mismo texto: la «buena» es la
  **primera en orden** con ese texto, nunca la más reciente. **Deduplicadas el 2026-11-03** con
  `tmp/dedup_cache.py CACHE --escribe` (es 7.015 → 1.268 entradas, 33 → 5,6 MB; en 7.575 → 1.259, 34 → 4,9 MB;
  copias en `tmp/cache_{es,en}_antes_dedup.json`): conserva la primera entrada de cada `input_data` (la que gana
  la búsqueda) y la primera de cada mp3, comprueba que ninguna búsqueda cambia y que todo mp3 sigue con entrada.
  Repetirlo cuando la caché vuelva a crecer (sin renders en marcha); una prueba de render no debe crear mp3.
- **Una marca al principio del texto se dispara al final.** manim-voiceover
  interpola el tiempo de una marca en la posición 0 (antes de la primera
  palabra) y la manda al final del audio (aviso "TimeInterpolator received
  weird input"): `<bookmark mark='cc'/> Como esto es...` destacaba los
  extremos de la cadena cuando la frase ya había acabado. `concluye` de V06
  lo corrige (marca con `tracker.bookmark_distances[m] == 0` = ya, sin
  esperar); copiarla así en V07 y en cualquier función que espere una marca
  inicial. Comprobarlo siempre con una tira de fotogramas.
- **Toma cortada por Azure** (V07 en, 2026-10-17: "...the order of the f"): la última
  palabra llega con `duration_milliseconds` 0 y el mp3 acaba ~0,3 s después de su
  inicio, con la voz aún sonando. Ni el render ni el montaje la cortan; es la síntesis.
  `tmp/tomas_cortadas.py CACHE...` lista las candidatas (en una letra final, 0,2 s es
  normal; en una palabra larga, no). Se arregla repitiendo la tirada: la primera
  (misma clave) sustituye a la mala en la caché con el mismo nombre.
- **Palabras repetidas que no salen en las marcas** (V12, 2026-11-04): una tirada dijo «...de orden m por n. por n.
  Su transpuesta...»; la segunda «por n» no tenía marca de palabra y el recorte para escuchar empezaba en «Su», así que
  pasó. Los recortes para elegir de oído empiezan una frase antes, y antes de injertar una toma se mide la energía de los
  huecos entre marcas (voz donde no hay palabra = repetición). Si la repetición está entre silencios, se corta del mp3 y
  se desplazan las marcas posteriores.
- Varias sesiones pueden escribir a la vez en el mismo `cache.json`: no
  renderizar dos vídeos con Azure en paralelo en el mismo repo.

## Estilo de los vídeos (acordado 2026-10-11)

- Esqueleto fijo: portada, arranque que dice qué se va a ver (en una o dos frases; lo de vídeos
  anteriores se nombra solo donde se usa, no en el arranque: Marcos, 2026-11-02, V11), cuerpo, resumen con el resultado en pantalla, una frase que
  anuncie el siguiente vídeo, créditos. Menos de diez minutos.
- **Cada vídeo se sostiene solo** (Marcos, 2026-11-03, V11): quien llegue suelto desde una búsqueda debe poder
  seguirlo. Ningún objeto heredado de un vídeo anterior («la matriz B») aparece sin construirlo en pantalla y
  nombrarlo como si fuera nuevo («Tomemos una matriz A y formemos otra matriz B...»); lo que sí se puede recordar
  en una frase es una regla ya vista («en el vídeo anterior vimos que da igual el orden...»), porque la pantalla
  la escenifica. La notación del curso se enlaza en la descripción (`Comprobaciones.org`, pasada 6).
- **Título y cabeceras** (Marcos, 2026-10-19): la escena 1 lleva arriba el título del vídeo
  (`Title(TITULO)`, como en V05-V10) y cada escena siguiente una cabecera corta
  (`Tex(..., font_size=44).set_color(COLOR_TITULO).to_edge(UP)`), salvo donde la cabecera corte el
  hilo de una historia continua (V08: cena, cesta, PIB, sin cabeceras). Comprobarlo en cada vídeo nuevo.
- La voz manda y la animación acompaña (`tracker.duration`). Nada aparece
  en pantalla sin que la voz lo mencione; en pantalla van fórmulas y
  rótulos cortos, la explicación va en la narración. Para que algo
  aparezca justo cuando la voz lo nombra: `<bookmark mark='x'/>` en el
  texto y `self.wait_until_bookmark("x")` dentro del `with` (exacto con
  Azure, estimado con gTTS; `MiEscenaConVoz.voiceover` se encarga).
- Los dos puntos en la narración producen una pausa de medio segundo
  (`MiEscenaConVoz.voiceover` inserta un `<break>` SSML para Azure). Para
  una pausa breve en otro sitio, con Tristan HD, vale una coma o un
  `<break time="250ms"/>` (medido 2026-10-12: Tristan no se traga la
  palabra anterior; Álvaro sí la dejaba en 70 ms al 11 %). El subtítulo
  ignora el `<break>` y gTTS lo convierte en coma. Las palabras a final
  de frase suenan más flojas por naturaleza.
  Azure no acentúa los interrogativos indirectos (`qué`, `cómo`: "estudiar
  qué propiedades", "vimos cómo multiplicar"): mejor evitarlos ("estudiar
  las propiedades que...", "vimos una construcción que multiplica...").
  La letra `a` sola la puede leer como preposición ("Ponemos a en el
  eje"); entre comillas simples (`'a'`) se entona como letra. Qué forma
  conviene depende de la voz y se mide sobre el audio con
  `tmp/analiza_letras.py` (se le pasa la clase de la escena; sintetiza
  cada letra sin comillas, con comillas y con coma, y mide duración,
  volumen y silencios). Reglas medidas para Tristan HD (2026-10-12):
  casi siempre lee bien la 'a' sin comillas; comillas solo delante de
  "más" ("la suma, 'a' más b", "en 'a' más b", "Primero 'a' más b");
  nunca en `b` ni `c` ni en la 'a' preposición (las comillas la
  silencian); las comillas no llegan al subtítulo
  (`MiEscenaConVoz.voiceover` las quita en español). Con Álvaro las
  reglas eran otras (comillas delante de "más/y/es/en", 'a' tragada tras
  un `<break>`): no extrapolar entre voces. Pruebas rápidas de entonación: sintetizar frases con
  `AzureService.generate_from_text` en `tmp/` y escucharlas.
- Frases pensadas para la voz sintética: cortas, una idea por frase, sin
  giros locales, sin LaTeX leído ("R n", "alfa"); tratamiento de usted en
  español. La traducción es frase a frase dentro de `tr()`.
- Código de colores de la serie (chunk `Código de colores`): `COLOR_A`
  azul, `COLOR_B` naranja, `COLOR_C` verde, `COLOR_ESCALAR` amarillo
  (escalares, preguntas, tarjeta de pausa), `COLOR_RESULTADO` blanco,
  `COLOR_REGLA` teal (pasos que usan una propiedad de los reales),
  `COLOR_TITULO` azul.
- Las demostraciones cortas se proponen como ejercicio con
  `self.pausa_para_pensar(pista=..., pista_voz=...)`: tarjeta única en
  toda la serie, pausa, pista, pausa, y después la demostración paso a paso.
  La voz de la primera tarjeta dice **qué** hay que intentar
  (`invitacion_voz="Pause el vídeo e intente demostrar la propiedad
  conmutativa."`), no solo "inténtelo".
- **Demostraciones con panel de herramientas** (acordado con Marcos el
  2026-10-13 sobre V06; modelo: clase `Panel` y funciones `linea`,
  `coloca_cadena`, `paso`, `concluye` de `L01-V06-PropiedadesDeLaSumaDeVectores.org`):
  - Panel fijo arriba: definiciones a la izquierda (suma y producto por
    escalar siempre visibles; nulo y opuesto atenuados al 30 % hasta la
    escena en que entran en juego), propiedades de los reales a la
    derecha, en pequeño (28 pt). Enunciado sin numerar (el número va en la
    cabecera "Propiedad N: ...") centrado en el hueco entre los paneles y
    a media altura entre la cabecera y la cadena; la cadena debajo, en
    el centro, con las líneas de pasos con reales en `COLOR_REGLA`.
  - Pista = las piezas necesarias pasan a amarillo **y** se recuadran
    (el amarillo solo no se ve en baja resolución). Orden de cada paso:
    la voz nombra la regla, la pieza parpadea en el panel, se escribe la
    línea y entonces sube el contador (insignia: disco azul con el
    número, separado de la fórmula; nunca "×2" pegado, que parece un
    factor) con la campanita `lib/sonidos/campanita.wav`
    (`self.add_sound`). La conclusión dice la cuenta ("dos usos de la
    definición de suma y uno de la conmutativa"), no "dos definiciones",
    y **cada contador parpadea cuando la voz nombra su pieza**, con una marca
    delante de cada una, no los dos a la vez (Marcos, 2026-11-03, V11; aplicado
    también a V12).
  - Al usar una definición del selector, la voz dice **en qué sentido**
    se reescribe (semilla de V01-V04; Marcos, 2026-10-14): "Por la
    definición de suma podemos distribuir el selector" (de izquierda a
    derecha) / "...podemos sacar el selector como factor común" (de
    derecha a izquierda);
    "Por la definición de producto (o de opuesto) podemos desplazar los
    paréntesis" (en los dos sentidos). Al presentar las definiciones, decir ya qué hace
    cada una: "la suma, que distribuye el selector, el producto por un
    escalar, que desplaza los paréntesis, ... y el opuesto, que también
    desplaza los paréntesis". Giro preferido por Marcos para **todos** los pasos,
    también los de los reales: "por [regla] podemos [acción]" ("Ya todo
    son números reales, así que podemos aplicar la asociativa"), más
    natural que "Regla: acción" o que nombrar la regla a secas. Que el alumno asocie selector distribuido ⇄ factorizable.
  - Pausas: dos en las dos primeras propiedades (intentar, pista,
    intentar), una en las siguientes (pista y pausa).
- **Cada expresión nace de la anterior** (Marcos, 2026-10-30; modelo: escena 2 de V11, entonces escena 5 de V10, y la
  técnica de V02). En las cadenas de igualdades y en las expresiones que se completan, se escribe
  la fórmula entera con `MathTex` y se trabaja con los índices de sus glifos (sacarlos con una
  imagen numerada): nada se mueve de sitio ni desaparece un instante. En cada paso, la parte que
  no cambia se copia (`TransformFromCopy`) mientras la voz nombra la regla, y la que cambia se
  transforma (un glifo en otro, o viajando de lado) en una marca `<bookmark>` cuando la voz
  describe el cambio. Lo que se quita (paréntesis, una transposición) simplemente no aparece. Variante
  (demostración de (Aᵀ)ᵀ = A en V11, entonces V10, funciones `copia_literal` y `transforma_copia`): al nombrar la
  regla se copia la expresión anterior tal cual, y sobre la copia desaparece lo que se quita mientras
  lo demás va a su sitio; útil cuando lo que se quita es justo lo que el paso enseña. Una
  expresión que se completa muestra primero unos glifos y después el resto, en su sitio. La
  sincronización fina se comprueba con Azure: con gTTS las marcas se estiman por caracteres.
- **«Los paréntesis», en plural** (Marcos, 2026-10-19): lo que se desplaza o se quita es la pareja,
  así que «podemos desplazar los paréntesis», «los paréntesis de la derecha», «sobran y podemos
  quitarlos». En singular, «el paréntesis de la derecha» parece el signo «)». V06 (publicado) conserva
  el singular.
- **Narración directa y mínima** (criterio de Marcos, 2026-10-14): cada
  frase dice una cosa y solo se dice lo que el vídeo va a usar. Fuera
  los apuntes laterales ("observe que reescalar por menos uno da el
  opuesto, pero no lo usaremos"), las justificaciones de lo que se
  admite ("estas propiedades no las demostramos: las admitimos"), los
  conectores de relleno ("Pero antes...", "Así que, para...") y las
  frases descolgadas de resumen ("distinga los tres tipos de cosas").
  Si dos frases consecutivas dicen lo mismo con distinto énfasis, una
  sobra. Modelo: "El vector nulo es el que tiene todas sus componentes
  nulas, y lo escribimos con un cero en negrita. Por ejemplo, el vector
  nulo de R2 tiene dos ceros, y el de R3 tiene tres. En las
  demostraciones usaremos que toda componente de un vector nulo es
  cero." Los ejemplos en pantalla se eligen para que se vean de un
  vistazo ((0, 1, 2) y su opuesto) y no se describen.
- **No volver a contar lo del vídeo anterior** (Marcos, 2026-10-30): lo ya contado en la serie
  solo se repite si hace falta recordarlo para entender el vídeo, y como recuerdo breve, no como
  algo nuevo (V10 repetía vector/matriz columna/matriz fila de V09; el selector por la izquierda
  ya estaba en V01). Comprobarlo con el guion del vídeo anterior (`Comprobaciones.org`).
- **«Este», no «un», para lo que está en pantalla** (Andrés, hermano de Marcos, 2026-11-03, V10): «lo hemos
  visto en un ejemplo» hacía buscar un ejemplo anterior; «en este ejemplo» señala el de la pantalla. Lo mismo
  con «esta matriz», «este vector»: el artículo indeterminado solo para lo que no se ve.
- **Discurso natural, no lectura de puntos** (Marcos, 2026-10-14): frases
  completas y enlazadas, como hablaría un profesor. Nada de titulares
  sueltos ("Definición de suma.", "La componente i-ésima del lado
  izquierdo.", "Las piezas que necesita: ...", "Tres usos de ..."):
  "Por la definición de suma podemos distribuir el selector", "Empezamos
  por la componente i-ésima del lado izquierdo", "Para demostrarla
  necesitará ...", "Hemos usado tres veces la definición de producto ...".
  Directo no significa telegráfico.
- **«Comprobar» frente a «demostrar»** (Marcos, 2026-11-02, V11): una regla de reescritura de la notación
  (i|Aᵀ|j = j|A|i) se *comprueba* («Por tanto, transponer intercambia los índices...»): la notación está
  construida para que ocurra. Una propiedad de los objetos ((Aᵀ)ᵀ = A, las ocho de los vectores) se
  *demuestra*, con el formato de ejercicio de la serie. «Hemos demostrado» en lo primero es excesivo.
- **Igualdad «columna a columna» y «componente a componente», nunca «las mismas componentes»** (Marcos, 2026-11-03, V12):
  «dos matrices son iguales cuando tienen las mismas componentes» es falso como está dicho (como conjunto, [1 0] y [0 1]
  tienen las mismas componentes). Decir «son iguales si lo son columna a columna» / «si lo son componente a componente»,
  y con la misma fórmula cada vez que se use la igualdad (criterio, cadena, conclusión de una demostración); en inglés
  «equal column by column» / «component by component». Lo mismo para vectores: «iguales componente a componente».
- **No leer en voz alta lo que ya está en pantalla.** La voz describe o
  nombra ("la propiedad conmutativa: el orden de los sumandos no altera
  la suma", "definición de suma", "este vector y su opuesto"), no recita
  la fórmula ("a más b es igual a b más a", "la componente i-ésima de a
  más la componente i-ésima de b"). Leerlo alarga el vídeo y aburre.
  Sin preguntas en la voz (Azure las entona mal): la pregunta va en
  pantalla y la voz la parafrasea en afirmativo. Las observaciones
  generales van en el resumen final, no intercaladas en una demostración.
- **Nada que ya no toca puede verse ni un instante** (Marcos, 2026-11-02, V11: al volver de 3|A|3 a
  i|A|i asomaba 1|A|1). Causa: `Transform`/`ReplacementTransform(x, y)` deforma los puntos de `x`
  hacia `y`, así que `x` deja de ser lo que era; si después se usa `x` como destino de otro
  `Transform`, se anima hacia su forma deformada. Regla: un objeto que ya fue *origen* de una
  transformación no vuelve a ser *destino*; para volver a una forma anterior, transformar hacia una
  copia hecha al crearla (`a_ii_fin = a_ii.copy()` antes de cualquier animación). Comprobar cada
  transformación encadenada con una tira de fotogramas recortada a la fórmula (2-3 fps).
  Qué animación elegir (comparadas el 2026-11-02 en la diagonal de V11):
  - `ReplacementTransform`: se ven glifos a medio deformar ("2" volviéndose "3") y deja inservible
    el origen. Solo cuando se quiere *ver* un glifo convertirse en otro o viajar a su sitio.
  - `TransformMatchingTex`: deja quietas las partes comunes, pero exige partir la fórmula en
    trozos y eso **cambia el espaciado** de las macros nacal (`i | A | i` en vez de `i|A|i`). No usar
    con fórmulas nacal.
  - **Lo preferido** para cambiar parte de una fórmula: una `MathTex` entera por estado, alineadas
    por un glifo común, y `FadeTransform` solo de los glifos que cambian (índices de la imagen
    numerada); después `self.remove(actual, *actual[0]); self.add(nuevo)`. Conserva la composición
    del libro, lo común no se mueve y no deforma nada (V12, escena 2; entonces V11).
- **La pantalla acompaña cada palabra de la narración** (Marcos, 2026-11-03; modelo: V10 escena 2 y V11
  escena 2, retocadas ese día, cuando eran V09 escena 7 y V10 escena 2). Al escribir cada frase:
  1. Cada cosa que la voz nombra se señala en su palabra: marca justo delante del sintagma («una fila de la
     transpuesta», «los índices de la fila», «el siete») y resaltado sostenido con el color de la serie (fila
     amarillo, columna verde), que dura hasta la siguiente cosa nombrada o 0,8 s. Cambio de color y tamaño
     inmediato (0,25 s), no `Indicate`, que llega tarde.
  2. Cada acción que la voz dice se anima en su verbo («podemos quitar los paréntesis», «desplazar»,
     «seleccionar primero»): la transformación arranca en esa marca, no al empezar la frase. Al empezar la
     frase solo aparece el rótulo de la regla.
  3. Cada regla que se recuerda se escenifica, no solo se nombra: «da igual el orden de selección» = los
     paréntesis de los dos lados viajan a la otra colocación y vuelven (`Transform` con
     `there_and_back_with_pause`, 2 s); «vectores iguales, mismas componentes» = los dos selectores aparecen a
     la vez. Misma animación que cuando se enseñó la regla, para que se reconozca.
  4. La pantalla se ordena como la frase: lo que la fórmula pone a la izquierda está a la izquierda arriba
     (V10: Aᵀ bajo (Aᵀ)|i y A bajo i|A).
  4b. Cuando la voz nombra alternativas («primero la fila o la columna»), la pantalla enseña cada una en su
     palabra: se mueve solo la expresión que no la muestra ya, y la que ya la muestra se queda quieta
     (V10 resumen, 2026-11-03: con las dos expresiones viajando a la vez, la de la izquierda enseñaba «columna
     primero» justo cuando la voz decía «la fila»). Si la voz no nombra alternativas sino la regla («da igual el
     orden de los selectores»), sí pueden viajar los dos lados (V11, escena 2).
  5. Mover una marca o añadirla no obliga a resintetizar: injertar el `input_text` y el `ssml` nuevos en la
     entrada de la toma buena (véase «Mover una marca sin pagar»). Comprobar cada frase con marcas con una
     tira de fotogramas a 3-4 fps recortada a la fórmula.
- Nada aparece en pantalla y luego se recoloca: cada elemento se crea ya
  en su posición final (los `set_x`/`arrange` antes de la primera
  animación que lo muestre).
- Legible en un móvil: fórmulas con `font_size` >= 40 en 1080p, márgenes,
  no más de un bloque de texto y una fórmula grande a la vez.
- **Primero un ejemplo, después lo simbólico** (Marcos, 2026-11-02, V11): el curso es para principiantes
  con poca experiencia matemática y la notación sola no basta. Cada escena que define, enuncia o
  demuestra algo empieza con un ejemplo numérico en pantalla (V11: S = Sᵀ antes de A = Aᵀ ⇒ a_ij = a_ji;
  una D diagonal transpuesta antes del ejercicio).
- Decir explícitamente cuándo una escena ilustra y cuándo demuestra.
- Música solo de entrada y salida (lo hace `montaje`); silencio durante
  el contenido y en las pausas para pensar.
- Subir a YouTube con `lib/subir_youtube.py` y una ficha TOML por vídeo
  en `fichas/` (título, descripción con capítulos, etiquetas, lista,
  mp4 y srt de cada idioma; modelo: `fichas/L01_V05.toml`). Modos:
  `subir` (mp4 + todo) y `actualizar --id` (metadatos, subtítulos y lista
  sobre un vídeo subido a mano). Credenciales OAuth en
  `lib/client_secret_youtube.json` y `lib/token_youtube.json`
  (ignorados). Los capítulos salen de los "empieza en" del `montaje`.
  Título (formato desde el 2026-11-02, `Comprobaciones.org` pasada 6): "Tema del vídeo | Álgebra lineal 1.9" /
  "Topic | Linear algebra 1.9", menos de 60 caracteres; **V05-V08 retitulados el 2026-11-03** con `actualizar`
  (título antiguo comentado en la ficha), con la descripción completa (anterior/siguiente, lista, notación con enlace
  a V01, música, licencia, fuentes) y miniatura; **V01-V04 también, el mismo día**, con fichas nuevas
  (`fichas/L01_V01.toml`...; sin `subtitulos`: los suyos, de 2026-10-13, no se tocan) y `actualizar --solo-metadatos`
  (metadatos anteriores en `tmp/metadatos_V01-V04_antes.txt`; capítulos los de la descripción anterior; «Zeta» suena en
  los cuatro en español y en V03-V04 en inglés, no en V01-V02 en). Las fichas inglesas dicen «(the book is in Spanish)»
  tras el enlace al libro. Al borrar y volver a subir subtítulos, YouTube tarda unos segundos
  en liberar la pista (409 `captionExists`): el script reintenta. Resumen de una línea, ordinal del vídeo,
  capítulos, enlace a la sección del libro y a los notebooks; categoría
  Educación; listas «Curso de Álgebra Lineal» (es) y «Linear Algebra
  Course» (en), por título en la ficha; la lista antigua «Álgebra Lineal»
  (confinamiento) se deja como está hasta rehacer los determinantes.
  Licencia: `actualizar` conserva la que tenga el vídeo (estándar de YouTube; la CC BY-SA 4.0 va en la
  descripción y los créditos, `Comprobaciones.org` 6a).
  `actualizar ... --solo-metadatos` (desde el 2026-11-03) pone título, descripción, etiquetas, idioma y lista sin
  tocar subtítulos ni miniatura: usarlo para añadir cada semana el «Siguiente vídeo» al anterior (el modo completo
  borra y resube la pista de subtítulos y el vídeo puede quedarse un rato sin ella) y siempre en V01-V04.
- **Miniaturas** (plantilla elegida por Marcos el 2026-11-03, variante F): `lib/miniatura.py` (cabecera
  documentada) genera `miniaturas/<clave>_<idioma>.png` (van a git) con el número en un disco, el título
  corto de la ficha (`titulo_miniatura`), «Álgebra lineal» debajo y un dibujo del vídeo (`MOTIVOS`):
  `cd lib && ~/.venvs/manim/bin/python miniatura.py L01_V12`. La ficha la cita con `miniatura = "..."` en
  cada idioma y `subir`/`actualizar` la envían; `subir_youtube.py miniatura ID FICHERO.png` pone solo la
  miniatura (V01-V04, sin ficha). Para un vídeo nuevo: añadir su motivo, generar y mirar a 320 px de ancho.

## Reglas

- **Copias de lo no versionado** (acordado con Marcos el 2026-10-30). `lib/media` de los dos
  idiomas y los mp4/srt finales no van a git; se protegen solo en el Synology. Tras publicar un
  vídeo en los dos idiomas:
  - **Borrar** sus renders, que se regeneran: `lib/media/videos/<fichero>/`, y `Tex` e `images`
    (en total eran 3,6 GB entre los dos idiomas el 2026-10-30).
  - **Conservar** su caché de voz (`lib/media/voiceovers`, las entradas de `cache.json` y sus
    mp3: ~250 MB por idioma para toda la serie) y el mp4 y el srt finales (YouTube solo devuelve
    una versión recomprimida). La caché es lo único que no se regenera igual: Azure no repite la
    misma toma, y algunas se eligieron entre varias tiradas. Sirve para retocar un vídeo publicado
    sin volver a revisar el audio (V07 se retocó tras aprobarse).
  - Copia extra opcional en el OneDrive de la UCM (decisión de Marcos), sobre todo de las cachés de
    voz mientras los vídeos están en producción.

- **Erratas y mejoras del libro** (Marcos, 2026-11-01): todo lo que se detecte en el libro al
  preparar un vídeo (huecos en demostraciones, notación usada antes de justificarla, erratas) se
  apunta como `TODO` en `../CursoDeAlgebraLineal-SRC/PendientesDesdeLosVideos.org`, con el vídeo,
  las líneas del `.tex` y la solución que se usó en el vídeo. No se corrige el libro: Marcos lo hará
  al acabar los vídeos de la lección 1.
- No hacer commit ni push sin que Marcos lo pida. Los `.mp4`, `media/`,
  `tmp/` y `music/` están ignorados y así deben seguir.
- Los descartes se guardan en `ZZ_Basura_*.org`, no se borran.
- Español primero para la revisión pedagógica; el inglés se genera del
  mismo org (objetivo: una sola fuente bilingüe).

## Calendario de publicación en YouTube (acordado con Marcos el 2026-10-18)

Un vídeo por semana: español el **jueves a las 15:00** (Madrid; antes 18:00, cambiado por Marcos el
2026-10-19) e inglés el **sábado a las 15:00**. Se mantienen dos o tres vídeos de reserva. **No subir nada (ni en privado) hasta que Marcos dé
el último repaso** a cada vídeo, unos días después de aprobarlo.

| Vídeo | Español      | Inglés       | Estado                                  |
|-------+--------------+--------------+-----------------------------------------|
| V07   | jue 22-10-26 | sáb 24-10-26 | publicado (es GOqglYkmOiA, en cNfCZMC8QcM) |
| V08   | mié 28-10-26 | sáb 31-10-26 | publicado (es w62nh5CvJtM, en C2QvSW4yX-Y el sábado 31 a las 14:34; en con tres frases distintas del español) |
| V09   | lun 03-11-26 | sáb 07-11-26 | **es publicado el lunes 3 (9w6gEv3XrTc, adelantado por Marcos: tres vídeos de reserva)**; «Siguiente vídeo» puesto en V08 es; **en publicado el martes 3 por la noche (t40aDUbc1oE), también adelantado por Marcos**: el mp4 subió público con título y descripción, pero la cuota diaria de la API (10 000 unidades) se agotó justo después, y el 4 de noviembre a las 09:00 se completó con `actualizar` (etiquetas, subtítulos, miniatura y lista) y se puso el «Next video» en V08 en con `--solo-metadatos`. Falta solo la pantalla final en Studio. **Lección aprendida**: la cuota de la API es de 10 000 unidades al día (se renueva a las 09:00 de Madrid) y una subida con todo gasta ~1 700; no encadenar retitulados masivos y una subida el mismo día. «Matrices» desde la **partición del 2026-11-03** (escenas 1-5 y resumen con la definición y el orden; anuncia la selección): solo el resumen y la portada son nuevos (una toma nueva por idioma, la frase D); HD es `L01_V09_MatricesFilasYColumnas.mp4` (4:04) y en `../videoMath2/L01_V09_MatricesRowsAndColumns.mp4` (3:59), capítulos y título «Matrices \| Álgebra lineal 1.9» en la ficha. Las escenas 1-5 estaban aprobadas por Marcos (2026-11-02/03); falta que escuche el resumen nuevo y su último repaso; **español aprobado por Marcos tras la partición (2026-11-03)**, **inglés aprobado también (2026-11-03)**; resumen: solo viaja la expresión del medio, a «fila primero» en «la fila» y de vuelta en «o la columna» (marcas f, c injertadas; es/en 480p y HD rehechos) |
| V10   | jue 05-11-26 | sáb 07-11-26 | **es publicado el jueves 5 a las 09:45 (gpVJnl4nAdU, adelantado por Marcos del jueves 12)**, enlazado desde V09 es, entrada en README/index y html del org; en el sábado 7 (después: id en la ficha, «Next video» en V09 en con `--solo-metadatos`, enlace inglés en README/index) · «Selección de filas, columnas y componentes» (título en YouTube: «Filas, columnas y componentes | Álgebra lineal 1.10») (`L01-V10-Seleccion.org`, nuevo el 2026-11-03 con las escenas 6-7 de V09, aprobadas): tres frases nuevas por idioma (arranque, primera del resumen, anuncio de la transposición); Azure 480p `L01_V10_Seleccion_azure480p.mp4` (2:45) y `../videoMath2/L01_V10_Selection_azure480p.mp4` (2:45) a la espera de su escucha; HD es `L01_V10_Seleccion.mp4` (2:46) y en `../videoMath2/L01_V10_Selection.mp4` (2:45) hechos, con capítulos; ficha `fichas/L01_V10.toml`; **español aprobado por Marcos tras la partición (2026-11-03)**, **inglés aprobado también (2026-11-03)** |
| V11   | jue 12-11-26 | sáb 14-11-26 | la transposición (`L01-V11-Transposicion.org`, era V10 hasta el 2026-11-03; historia en «Pendiente»): **español aprobado** (Azure y HD); el 2026-11-03 la segunda frase de la escena 1 pasa a «Al presentar las matrices formamos la matriz B...» (antes «En el vídeo anterior...», ya no cierto): Azure 480p `L01_V11_Transposicion_azure480p.mp4` (3:05) y `../videoMath2/L01_V11_Transposition_azure480p.mp4` (3:04, el inglés entero sigue pendiente de su escucha); HD es rehecho (`L01_V11_Transposicion.mp4`, 3:06); falta el HD en inglés; **español aprobado por Marcos tras la partición (2026-11-03)**, **inglés aprobado también (2026-11-03)** |
| V12   | jue 19-11-26 | sáb 21-11-26 | (tras el último repaso de Marcos y su visto bueno a la miniatura)  tipos de matrices (`L01-V12-TiposDeMatrices.org`, era V11): **aprobado por Marcos en los dos idiomas el 2026-11-04 (Azure 480p), HD es/en hechos ese día, ficha `fichas/L01_V12.toml` con capítulos y miniatura (matriz simétrica y S = Sᵀ, a la espera de que Marcos la vea)**; **revisado y rehecho el 2026-11-03** (seis escenas: la 3 partida en «Matrices simétricas» y «Componentes de una matriz simétrica»); prueba gTTS `L01_V12_TiposDeMatrices_prueba480p.mp4` (7:14) y `../videoMath2/L01_V12_TypesOfMatrices_prueba480p.mp4` (6:54), a la espera de la revisión de Marcos |

Desde el 2026-11-03 todos los vídeos publicados (V01-V08) llevan la miniatura de la serie, el título
«Tema | Álgebra lineal 1.N» y la descripción completa; todos tienen ficha. V09 es publicado el 2026-11-03 y enlazado desde V08 es; al subir V09 en, lo mismo en la sección `[en]` de V08
(`actualizar --solo-metadatos`) y su enlace inglés en `README.org`/`index.html`. En cada subida, mismo patrón con el anterior.

**Recordatorio:** al empezar cada sesión, mirar la fecha. Si quedan tres días o menos para la
próxima publicación y ese vídeo no está subido, recordárselo a Marcos antes de nada.
Subida: `lib/subir_youtube.py subir FICHA IDIOMA` (mp4, metadatos, subtítulos y lista de una vez).
Pese al aviso del script, la API publica en **público** (V05 y V07 es, 2026-10-22): no programa, así que
se lanza a la hora de publicar. El token caduca cada semana: si da `invalid_grant`, apartar
`lib/token_youtube.json` y repetir; se abre el navegador para autorizar. La pantalla final, en Studio.
Después se apunta el id en la ficha y se añaden la entrada de `README.org`/`index.html` y el html del org.
Al publicar un vídeo, actualizar esta tabla.

## Pendiente

- Iconos de la serie: **hechos el 2026-10-18** en `Comunes.org` (chunk `Iconos`): `aviso(tipo)` da un
  rótulo con icono al estilo de la tarjeta de pausa y `icono(tipo)` solo el símbolo. Tipos: `pregunta`
  (disco amarillo con ?), `idea` (bombilla), `engorroso` (garabato), `ilustra` ("Ilustra, no demuestra",
  ojo) y `ampliacion` (rombo de curva peligrosa, para la serie X). Muestra en `tmp/iconos_serie.png`.
  Aún no los usa ningún vídeo; los colores y dibujos están a la espera de que Marcos los vea.
- V06 (`L01-V06-PropiedadesDeLaSumaDeVectores.org`): **publicado el 2026-10-17** en los dos idiomas
  (ids en la memoria y en `fichas/L01_V06.toml`), con su entrada en `README.org`/`index.html`.
- V07: propiedades 5-8 (producto por escalares) con las mismas
  utilidades de V06; solo usa las cuatro propiedades del producto de los
  reales (5-8); la 6 necesita tres pasos de reales (conmutativa,
  distributiva, conmutativa). **Encargo completo con las cuatro cadenas,
  el panel, las escenas y la entrega en `tmp/HANDOFF_V07_guion.md`.**
  Guion escrito el 2026-10-14 en `L01-V07-PropiedadesDelProductoPorEscalares.org`;
  revisado por Marcos y con voz de Azure (Tristan) a 480p:
  `L01_V07_PropiedadesDelProductoPorEscalares_azure480p.mp4` (6 min 41 s). Las tomas
  de Azure están en una **caché aparte**, `lib/media_v07/voiceovers` (render con
  `--media_dir media_v07`, montaje con `tmp/montaje_v07.sh fichero "escenas" cierre
  video idioma calidad`), porque la sesión de V06 sintetizaba a la vez: antes del HD,
  fusionar su `cache.json` y sus mp3 con `lib/media/voiceovers` y renderizar sin
  `--media_dir`. **Fusionadas el 2026-10-17** (40 tomas, sin conflictos): ya se renderiza
  con `lib/media` como los demás. Ese día se igualó a V06: criterio de la escena 2 con la
  frase de V06 y la igualdad de componentes resaltada, explicación de los paréntesis que
  aparecen en el paso 3 de la propiedad 5 ("el escalar multiplica a la componente, y no al
  vector"), distributiva del panel señalada en el paso 2 de la propiedad 6 y
  `self.wait(0.3)` antes de "Hemos llegado". **Aprobado por Marcos en los dos idiomas y
  renderizado en HD el 2026-10-17** (`L01_V07_PropiedadesDelProductoPorEscalares.mp4`, 6:48, y
  `../videoMath2/L01_V07_PropertiesOfScalarMultiplication.mp4`, 6:50, con sus srt); ficha
  `fichas/L01_V07.toml` con los capítulos. Último repaso de Marcos (2026-10-19): «Como hicimos en el otro vídeo, ... éstas son», «Como ya
  sabemos, para demostrar...», «las dos definiciones y las propiedades conmutativa y distributiva» (que no
  parezcan nombres de las definiciones) y, en la propiedad 7, qué paréntesis se desplaza («los paréntesis de
  fuera»; «los paréntesis de la derecha para sacar fuera el selector»; en inglés solo estos dos); después «los paréntesis» en plural en todo
  V07 y «los paréntesis de fuera» también en el primer paso de las propiedades 5 y 6. HD rehecho
  (6:50 es, 6:53 en) y capítulos de la ficha corregidos; HD anterior en el scratchpad de la sesión. **Publicado: es el jueves 22 (GOqglYkmOiA) y en el sábado 24 de octubre (cNfCZMC8QcM)
  de 2026**, con ids en la ficha, entrada en `README.org`/`index.html` y html del org y pantalla final en Studio.
- V08 (`L01-V08-VectoresComoDatos.org`, Sección 1.3; cena, cesta, combinación lineal, PIB y la
  criatura Omega): **aprobado por Marcos en los dos idiomas y renderizado en HD el 2026-10-17**
  (`L01_V08_VectoresComoDatos.mp4` y `../videoMath2/L01_V08_VectorsAsData.mp4`, 3:19, con sus
  srt); ficha `fichas/L01_V08.toml` con los capítulos. **Publicación: es el jueves 29 y en el sábado 31 de
  octubre de 2026**, y después ids, README/index y html del org. Las utilidades de Omega (`omega`,
  `cambia`, `parpadea`, `entra`, `bocadillo`) **ya están en `Comunes.org`** (2026-10-17); V08
  conserva su copia idéntica (se define tras el import y manda la suya). Retoque 2026-10-18 (Marcos): la
  alegría de Omega dura un instante (1-2 s) y vuelve a `normal` mirando lo que explica la voz; HD de la
  escena 3 rehecho en los dos idiomas (sin sintetizar), capítulos de la ficha corregidos.
- V09 (`L01-V09-MatricesFilasYColumnas.org`, Secciones 1.4-1.4.3): primera versión (2026-10-17) no
  convenció a Marcos; **segunda versión 2026-10-18 fiel a sus transparencias de clase**
  (`../MatematicasII-SRC/Version0/temas/T01.tex`, transparencias "Matrices" y "Más notación": ejemplo
  a, b, c de R², A ≠ [b;c;a] (todas las columnas cambian de sitio; Marcos), B con las filas de A para el orden, una sola matriz 2×3 para los tres
  selectores con su nombre largo). Las transparencias son fuente de consulta para los vídeos siguientes.
  Tercera versión (2026-10-18), **paralela a V01** (Marcos): definición y letras del superíndice,
  ejemplos (posición; listas distintas = orden; igualdad como consecuencia), notación (corchetes,
  matriz columna como (3)≠(3,), mayúsculas, matriz nula) y componentes (a_ij y el selector; sin `elem`).
  Prueba gTTS 480p: `L01_V09_MatricesFilasYColumnas_prueba480p.mp4`, guion en
  `tmp/guion_V09_es.txt`. La versión 1 y el apéndice de R⁰ están en `ZZ_Basura_L01_V09.org`. En inglés,
  "orden" = *order* (Marcos). **Azure es 480p el 2026-10-18**: `L01_V09_MatricesFilasYColumnas_azure480p.mp4`
  (5:01); dos tomas repetidas con `v2` (una cortada por Azure a media frase, otra con 620 ms antes de
  "orden"). Inglés con Azure (Ollie) 480p el mismo día: `../videoMath2/L01_V09_MatricesRowsAndColumns_azure480p.mp4` (4:53); "...denotes a matrix." salía cortada por Azure en todas las tiradas: en plural ("Parentheses ... denote", "square brackets ... denote a matrix") sale entera. **Aprobado por Marcos en los dos idiomas y HD el 2026-10-18** (`L01_V09_MatricesFilasYColumnas.mp4`, 4:55, y `../videoMath2/L01_V09_MatricesRowsAndColumns.mp4`, 4:54, con sus srt); ficha `fichas/L01_V09.toml`. 2026-10-19: cabeceras añadidas a las escenas 2, 3 y 6 («Ejemplos», «El orden de una matriz», «Componentes, filas y columnas») y HD rehecho sin sintetizar. **Cuarta versión, 2026-11-02** (Marcos vio V09 y V10 seguidos: la escena de
  componentes imponía la notación sin paréntesis y V10 la justificaba un vídeo después): escena 6 «Filas y
  columnas» (selector a la derecha = elemento de la lista, una columna; a la izquierda, una fila), escena 7
  «Componentes» con las escenas 1-2 de V10 casi literales (frases nuevas: «Cada componente de una matriz
  está a la vez...», «El siete, por ejemplo, es componente de dos vectores distintos...», «Por eso podemos
  escribir el selector a ambos lados de la matriz, sin paréntesis») y, al final, lo habitual (a_21) frente al
  selector; escena 8 resumen con la línea «da igual el orden de selección» y anuncio solo de la
  transposición. La escena 6 anterior está en `ZZ_Basura_L01_V09.org`. Las frases movidas sin cambios
  conservan sus tomas de Azure (la caché es común a todos los vídeos). Falta: revisión de Marcos de la prueba
  gTTS, Azure, HD, capítulos de la ficha; la subida del 5 de noviembre depende de ese repaso.
  **Quinta versión, 2026-11-03 (partición)**: V09 queda como «Matrices» (título nuevo, también en la portada):
  escenas 1-5 sin cambios y resumen (escena 6, `L01_V09_E06_Resumen`) con la definición y el orden y el
  anuncio «En el próximo vídeo veremos la selección de filas, columnas y componentes de una matriz.». Las
  escenas 6-7 y la tabla del selector del resumen pasaron a V10 (nota en `ZZ_Basura_L01_V09.org`). HD es/en
  y capítulos hechos; falta que Marcos escuche el resumen nuevo y su último repaso.
- V10 (`L01-V10-Seleccion.org`, Secciones 1.4.3-1.4.4; inglés `L01_V10_Selection`; desde el 2026-11-03):
  «Selección de filas, columnas y componentes». Escena 1 = antigua escena 6 de V09 con el título y el
  arranque «En este vídeo veremos la selección...»; escena 2 = antigua escena 7 («Componentes», con
  `aviso("idea")`); escena 3 = resumen con la tabla del selector, «da igual seleccionar primero la fila o la
  columna» (viaje de los paréntesis) y el anuncio de la transposición. Destino de la línea de notación de
  las descripciones. Azure 480p y HD hechos (ver calendario), ficha `fichas/L01_V10.toml`; falta la escucha
  de Marcos de las tres frases nuevas.
- V11 (`L01-V11-Transposicion.org`, Sección 1.4.5; inglés `L01_V11_Transposition`; hasta la partición del
  2026-11-03 era V10, `L01-V10-Transposicion.org`, y así lo nombra lo que sigue; hasta el 2026-11-02
  `L01-V10-SeleccionYTransposicion.org`, Secciones 1.4.4-1.4.5): estructura aprobada por Marcos el 2026-10-18
  (selector por la izquierda de un vector y da igual el orden; transposición, con la B de V09 = Aᵀ; matriz
  fila; regla "transponer = cambiar de lado los índices" demostrada y (Aᵀ)ᵀ = A con tarjeta de pausa). El
  escalar a la derecha y las reglas con escalares van a V14; la notación como programa, a X03. Primer uso del
  rótulo `aviso("idea")` (ahora en V10, escena 2). HD es/en y ficha el 2026-11-02 (4:25 es, 4:28 en).
  **Reducido a la transposición el 2026-11-02**: las escenas 1-2 (enlace y «primero la fila o primero la
  columna») pasaron a V09 (código guardado en `ZZ_Basura_L01_V11.org`, antes `_V10`); queda arranque + transposición,
  cambio de índices (recuerda de V09 que da igual el orden de selección), (Aᵀ)ᵀ = A y resumen de dos líneas.
  Título «La transposición» / «Transposition». Español aprobado con Azure y HD el 2026-11-02/03. Tras la
  partición (2026-11-03): ficheros, clases y montajes renombrados a `L01_V11_*`, ficha `fichas/L01_V11.toml`
  («Álgebra lineal 1.11»), y la frase E de la escena 1 («Al presentar las matrices formamos la matriz B...»).
  Falta: escucha de Marcos del inglés y HD en inglés.
  2026-11-04: en inglés «swap(ping) the sides of the indices» → «move/moving the indices to the other side» (cabecera,
  rótulo del resumen, tres frases nuevas de Ollie; ficha); Azure 480p en rehecho (3:05); **inglés aprobado por Marcos (2026-11-04)**, HD en rehecho ese día.
- **Partición de V09 (decidida y hecha el 2026-11-03, encargo en `tmp/HANDOFF_V09_particion.md`)**: V09 queda
  como «Matrices» (escenas 1-5 y resumen recortado), la selección de filas, columnas y componentes pasa
  a un V10 propio (`L01-V10-Seleccion.org`, destino de la línea de notación de las descripciones), la
  transposición pasa a V11 y los tipos de matrices a V12 (y los siguientes corren un número). Motivo:
  referencia en abierto; un vídeo que solo cuente la selección es enlazable. Cinco frases nuevas por
  idioma, todo lo demás conserva sus tomas. Calendario: V09 jue 5/sáb 7, V10 jue 12/sáb 14, V11 jue
  19/sáb 21 de noviembre. Hecha: cinco tomas nuevas por idioma (en inglés, «When we introduced matrices...»
  sustituida por la tirada 1, sin la pausa de 380 ms antes del segundo «one»). Ojo: manim-voiceover añade
  a `cache.json` una entrada repetida por cada frase que reutiliza, así que la caché crece más que las
  tomas nuevas; contar los mp3 nuevos o las entradas con `original_audio` no visto antes.
- V11 (transposición), 2026-11-03 tras la partición: la escena 1 ya no remite a V09 («Al presentar las matrices
  formamos la matriz B»); dice «Tomemos una matriz A y formemos otra matriz B con dos vectores...» (Marcos: quien
  llegue suelto al vídeo no conoce B; la escena la construye en pantalla). Toma nueva por idioma, montajes es 480p/HD
  y en 480p rehechos (3:05), capítulos es en la ficha; el HD en espera su escucha del inglés.
- **Encargo de mantenimiento para Opus** (2026-11-03, `tmp/HANDOFF_mantenimiento_y_publicados.md`): deduplicar
  las cachés de voz, retitular y completar las descripciones de V05-V08 publicados (con Marcos para el token),
  prototipos de miniaturas y, opcional, borrador de estructura de X00.
- **Para la corrección y traducción del libro** (sesión y repositorio aparte, más adelante; Marcos, 2026-11-03):
  (1) el glosario inglés de `NotacionNacal.org` es la referencia de términos para la traducción, mantenerlo al
  día; (2) centralizar el pie común de las descripciones de YouTube (lista, notación, nota «the book is in
  Spanish», música, licencia) en un fichero por idioma que lea `subir_youtube.py`, para cambiarlo de una vez
  cuando haya libro inglés o vídeo X00 (encargo pequeño para Opus); (3) si la traducción conserva la
  estructura de secciones, los enlaces `#subsection.1.4.3` del PDF valen cambiando solo el nombre del
  fichero; (4) corregir primero el español (con `PendientesDesdeLosVideos.org`) y traducir después.
- **Vídeos de ampliación (serie X)**: lo más abstracto va en vídeos cortos aparte (`L01 X01`...),
  marcados como opcionales y más difíciles; plan y convenios en `NotacionNacal.org`. X01 = el apéndice
  de R⁰ que salió de V09. La frase final de V09 que lo anunciaba se quitó (2026-10-18, a `ZZ_Basura_L01_V09.org`); se decide al tener X01.
- V12 (`L01-V12-TiposDeMatrices.org`, Sección 1.4.6; inglés `L01_V12_TypesOfMatrices`; era V11 hasta el
  2026-11-03): «Tipos de
  matrices» (no «matrices especiales»: da nombre a las matrices por sus características). Reparto del
  resto de la lección 1 (2026-11-02, numeración del 2026-11-03): V12 tipos, V13 suma y producto por escalar (1.5-1.5.2), V14
  transposición lineal, escalar a la derecha, operaciones por filas y reglas (1.5.3-1.6). Prueba gTTS
  480p 2026-11-02 (6:22 es, 5:58 en) con ejemplos iniciales e igualdad componente a componente en la
  escena 3. **Revisión completa el 2026-11-03** (seis pasadas de fase A; Marcos: «esta primera versión está
  lejos de ser óptima», escrita por Opus antes de la guía actual): fuera el nombre «regla de los índices»
  (V11 no lo dio; ahora siempre «quitar la transposición cambiando de lado los índices», también en el panel,
  «Vídeo anterior: quitar la transposición»); escena 3 partida en «Matrices simétricas» (E03: definición,
  ejemplos, cuadrada) y «Componentes de una matriz simétrica» (E04: la voz dice para qué hace falta el criterio
  de igualdad y lo construye en tres pasos, A = B ⟺ mismas columnas ⟺ mismas componentes, con «si, y solo si»;
  cadena; espejo), ejercicio en E05 y resumen en E06; frases largas partidas; letras fuera de posiciones malas
  («Como la matriz es igual...», «la componente de la fila i, columna j»); pantalla: ejemplos a la vista mientras
  la voz habla de sus diagonales, ceros señalados en su palabra, identidad en «la matriz identidad», panel
  parpadea al nombrar la acción. La segunda demostración de (Aᵀ)ᵀ = A con el criterio **no va en V12**
  (propuesta: arranque de V14; decide Marcos). Segunda tanda el mismo día (Marcos tras ver la prueba): en la escena 2 los ceros fuera de la diagonal van en azul en **todos** los ejemplos (D, F, G y las identidades), las matrices nulas se ven cambiando a cero (amarillo) la diagonal de los tres ejemplos con `Transform` (no `ReplacementTransform`, que desmonta el grupo y luego no se desvanece), y «las matrices nulas» / «las matrices identidad» en plural (no hay una sola); en la escena 3, «usamos la transposición» sin «del vídeo anterior» y «Así pues, toda matriz simétrica es cuadrada» en vez de «En general». Tercera tanda: la voz dice por qué se formaliza lo que el ejemplo ya ilustra («El ejemplo lo ilustra con una matriz concreta. Para asegurarnos de que vale para cualquier matriz simétrica, sea cual sea su orden, lo demostramos para una matriz de orden cualquiera: ...» (redacción elegida por Marcos)), con la conclusión en pantalla; Marcos acepta no meter más tipos (triangulares: apéndice del cap. 3, vídeo propio en la lección 3). Cuarta tanda (Marcos): sin anuncio «usamos la transposición» (evidente al oír la definición); contraejemplo **cuadrado** (la C de la escena 1, con el 2 y el 3 en naranja) antes del rectangular, para que no parezca que simétrica = cuadrada; la pregunta «¿Toda matriz simétrica es cuadrada?» en pantalla (amarillo) y «Los ejemplos sugieren que...» en la voz antes de demostrarlo «para una matriz de orden cualquiera»; en el criterio queda un ⟺ en amarillo; y la regla de V11 se llamó primero «la definición de transpuesta» y después (sexta tanda) **«la propiedad de la transpuesta»**, nunca «la regla del vídeo anterior»: un nombre atado al número de vídeo no sirve en los siguientes. Quinta tanda: fuera «dos matrices de distinto orden no son iguales» (evidente con el ejemplo) y «Para asegurarnos de que es así, lo demostramos para una matriz de orden 'm' por 'n': su transpuesta es de orden 'n' por 'm', y como las dos son iguales, m y n coinciden» (Marcos: sin repetir «orden cualquiera / si es de orden»). Escena 4 abre con «Veamos ahora la disposición de las componentes de una matriz simétrica» (Marcos). Sexta tanda (Marcos): la pieza del panel es **«la propiedad de la transpuesta»** (la demostración usa la regla «quitar la transposición cambia de lado los índices», no la definición); criterio «de igualdad componente a componente»; al final del ejercicio aparece una identidad 3×3 con Iᵀ = I al decir que es simétrica (el espectador quizá no recuerde cómo es); el resumen tiene una sexta línea «Iᵀ = I: las matrices identidad son simétricas» y la voz acaba «...; por tanto, las matrices identidad son simétricas». Pista del ejercicio: «la definición de matriz diagonal y el cambio de lado de los índices al transponer» (Marcos). Séptima tanda: la igualdad se dice siempre «columna a columna» / «componente a componente» (nunca «las mismas componentes»,
  que vale como conjunto), en el criterio, la cadena y la conclusión del ejercicio; regla nueva en `CLAUDE.md` (estilo) y
  `Comprobaciones.org` (pasada 1.4). Octava tanda: en la cadena de la escena 4, «Podemos quitar la transposición cambiando de lado los índices» sin nombrar la propiedad (sin antecedente ahí; en el ejercicio sí, por el panel y la pista), rótulo «cambiar de lado los índices». Novena tanda: en el ejercicio la voz dice dónde se usa «cuadrada» («El criterio de igualdad exige que las dos matrices tengan el mismo orden. Como la matriz es cuadrada, su transpuesta tiene el mismo orden que ella, así que basta comparar sus componentes una a una»), con «D, Dᵀ ∈ ℝ^{n×n}» en pantalla; el criterio de la escena 4 ya lleva «del mismo orden» en la voz y en la nota. Tercera lectura en frío (2026-11-03, sobre el guion definitivo): aplicado «una matriz **simétrica** de orden 'm' por 'n'», «esta matriz diagonal **y cuadrada**» en el ejemplo del ejercicio, «basta comprobar que son iguales componente a componente», «Como las matrices identidad son diagonales y cuadradas, también son simétricas» y dos retoques del inglés; no aplicado (decisiones de Marcos o convenciones): nombrar la regla en la cadena, «si y solo si» con premisas en «si», enunciado de la tarjeta. **Azure 480p el 2026-11-03**: `L01_V12_TiposDeMatrices_azure480p.mp4` (5:40) y `../videoMath2/L01_V12_TypesOfMatrices_azure480p.mp4` (5:47). Tomas: en inglés Ollie se tragaba «m and n coincide» (0-50 ms en seis tiradas, con y sin comillas) y pausaba 550 ms en «the | two | are equal»: la frase inglesa pasa a «for a symmetric matrix with 'm' rows and 'n' columns: its transpose has 'n' rows and 'm' columns, and since they are equal, the two orders coincide» (toma v2 injertada); «the ones below» pausaba 440-620 ms antes de «below» en todas las tiradas → «the components below» (tirada 1 injertada); «Take any symmetric matrix...» con 550 ms → sustituida por la tirada 1 (misma clave); en español «lo | demostramos» 490 ms → sustituida por la tirada 1. Letras: español bien (m/n 200-320 ms; la 'i' de «letra i mayúscula» 80 ms en tres tiradas, es la frase: **que Marcos la escuche**); inglés 'n' antes de «columns» 80-130 ms en todas las tiradas, a escuchar. `tomas_cortadas`: ninguna de V12. **Escucha de Marcos del Azure (2026-11-03), once retoques aplicados**: Omega se sorprende al aclarar el criterio (no al aparecer los ejemplos); «con la letra i, en mayúscula y negrita» (la 'i' pasa de 80 a 210 ms); frases que quedaban con entonación de continuar partidas con punto («...las columnas de la transpuesta. Obtenemos la misma matriz», «...de orden 'm' por 'n'. Su transpuesta...», «Cambiando de lado los índices, podemos quitar la transposición», resumen «...como columnas. Es diagonal si...»); coma tras «por encima»; «al quitar la transposición y cambiar de lado los índices»; «Este resultado se aplica a las matrices identidad: como son diagonales y cuadradas, también son simétricas»; ejemplos de estructura simple (S = [1 2 3; 2 4 5; 3 5 6], contraejemplo cuadrado con filas de unos, doses y treses, `N_EJ`) y pausas de 1 s y 0,8 s tras los dos contraejemplos. Ollie: «When | we transpose it» 670 ms, sustituida por la tirada 1 (misma clave). Azure 480p rehecho: es 5:47, en 5:52. 2026-11-04 (Marcos): escena 1, «podemos abreviar y decir ese número una sola vez» (antes «su orden se indica con un solo número», que sugería que no se puede repetir; fórmula del libro «abreviamos»; toma v3 injertada, las dos primeras pausaban 390-490 ms en «decir | ese número»); «Para indicar su orden hacen falta los dos números, el de filas y el de columnas» (Tristan alarga la última palabra de toda frase, 360-560 ms en diez tomas; Marcos eligió de oído la toma B1 entre siete, en `tmp/escucha_V12/`). Falta: segunda escucha de Marcos, HD, ficha, miniatura; guion en `tmp/guion_V12_{es,en}.txt`. **Siguiente paso: Marcos la escucha y después Azure 480p**. Falta: revisión
  de Marcos, Azure, HD, ficha, motivo de miniatura.
