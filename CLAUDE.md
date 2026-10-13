# VideosMates2 — vídeos con Manim para Matemáticas II (GECO, UCM)

Vídeos que siguen el libro *Curso de Álgebra Lineal* (fuentes en
`../CursoDeAlgebraLineal-SRC/partes/`). Versión en español aquí; la
versión en inglés vive en el repo hermano `../videoMath2`.

## Antes de escribir cualquier escena

Leer `NotacionNacal.org`: convenios del libro, macros de `nacal.sty`,
cuenta de glifos de `MathTex`, API del módulo `nacal` y terminología
inglesa ya fijada. Las fórmulas y narraciones deben respetar esa
notación (vectores entre paréntesis, matrices entre corchetes, operador
selector, "componente a componente", etc.).

## Flujo de trabajo

- Un fichero org por vídeo (`L01-V05-Nombre.org`; plan de la lección 1 en
  `NotacionNacal.org`: V05 reales con regla y compás, V06 propiedades de
  las operaciones con vectores, ..., V12), programación literaria
  y **fuente única bilingüe**. Plantilla: `LXX-VYY-NombreVideo.org`.
  Cada escena es un chunk con nombre que reutilizan la clase del vídeo
  completo y las clases `LXX_VYY_Enn_*` (chunk "Clases de las escenas").
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
  normaliza la voz (loudnorm), pone música solo en la portada (fundido al
  empezar la escena 1) y desde la escena `cierre` hasta el fundido a negro,
  y fusiona los `.srt` de las escenas en un único `video.srt` para YouTube.
- Comprobar visualmente: extraer fotogramas con ffmpeg (bloque
  `fotogramas`, en especial alrededor de cada unión) y mirarlos.

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

## Estilo de los vídeos (acordado 2026-10-11)

- Esqueleto fijo: portada, enlace con el vídeo anterior en una o dos
  frases, cuerpo, resumen con el resultado en pantalla, una frase que
  anuncie el siguiente vídeo, créditos. Menos de diez minutos.
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
- Legible en un móvil: fórmulas con `font_size` >= 40 en 1080p, márgenes,
  no más de un bloque de texto y una fórmula grande a la vez.
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
  Formato heredado de los vídeos ya publicados: título "L01 V0N Nombre
  (Español)" / "(English)", resumen de una línea, ordinal del vídeo,
  capítulos, enlace a la sección del libro y a los notebooks; categoría
  Educación; listas «Curso de Álgebra Lineal» (es) y «Linear Algebra
  Course» (en), por título en la ficha; la lista antigua «Álgebra Lineal»
  (confinamiento) se deja como está hasta rehacer los determinantes.

## Reglas

- No hacer commit ni push sin que Marcos lo pida. Los `.mp4`, `media/`,
  `tmp/` y `music/` están ignorados y así deben seguir.
- Los descartes se guardan en `ZZ_Basura_*.org`, no se borran.
- Español primero para la revisión pedagógica; el inglés se genera del
  mismo org (objetivo: una sola fuente bilingüe).

## Pendiente

- Cuando los trozos comunes (carga de librerías, `tr`, `voz`,
  `MiEscenaConVoz`, créditos, `myTemplate`, VectorR2/R3) se estabilicen
  tras dos o tres vídeos bilingües, extraerlos a un `Comunes.org` que
  tangle `lib/vm2comun.py` en ambos repos; cada vídeo haría
  `from vm2comun import *`. Hoy se copian en cada org (~150 líneas).
