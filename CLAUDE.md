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
  `NotacionNacal.org`: V05 reales con regla y compás, V06 vectores
  especiales y propiedades de la suma, V07 propiedades del producto por
  escalares, ..., V12), programación literaria
  y **fuente única bilingüe**. Plantilla: `LXX-VYY-NombreVideo.org`.
  Cada escena es un chunk con nombre que reutilizan la clase del vídeo
  completo y las clases `LXX_VYY_Enn_*` (chunk "Clases de las escenas").
- El código común (carga de librerías, `LANG`, `tr`, voces, colores,
  `myTemplate`, `MiEscenaConVoz`, tarjeta de pausa, créditos,
  VectorR2/R3) vive en `Comunes.org`, que tangle `lib/vm2comun.py` en
  los dos repositorios (solo difieren en `LANG`). Cada vídeo hace
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
  normaliza la voz (loudnorm), pone música solo en la portada (fundido al
  empezar la escena 1) y desde la escena `cierre` hasta el fundido a negro,
  y fusiona los `.srt` de las escenas en un único `video.srt` para YouTube.
- Web: cada vídeo publicado lleva su entrada en `README.org` (python, html
  del org, enlaces a YouTube es/en) y su org exportado a html. El org del
  vídeo se exporta en batch con htmlize cargado (`emacs --batch -l
  exporta.el --visit=FICHERO.org -f org-html-export-to-html`, con
  `exporta.el` añadiendo `~/.emacs.d/elpa/htmlize-*` al load-path); sale
  igual que el de V05. El `index.html`, en cambio, **no** se reexporta en
  batch: el tema de la web (estilo UCM, `worg.css` incrustado) solo sale
  con `C-c C-e h h` desde el Emacs abierto de Marcos (su configuración
  `~/.emacs.d`, no scimax); cargar ese `init.el` en batch no lo reproduce
  (probado 2026-10-17: algo de la sesión interactiva lo pone).
  Se le añade la entrada a mano copiando la anterior, o lo exporta Marcos.
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
  primera coincidencia). Hecho en las conclusiones de V06 (2026-10-14).
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
- Varias sesiones pueden escribir a la vez en el mismo `cache.json`: no
  renderizar dos vídeos con Azure en paralelo en el mismo repo.

## Estilo de los vídeos (acordado 2026-10-11)

- Esqueleto fijo: portada, enlace con el vídeo anterior en una o dos
  frases, cuerpo, resumen con el resultado en pantalla, una frase que
  anuncie el siguiente vídeo, créditos. Menos de diez minutos.
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
    definición de suma y uno de la conmutativa"), no "dos definiciones".
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
- **Discurso natural, no lectura de puntos** (Marcos, 2026-10-14): frases
  completas y enlazadas, como hablaría un profesor. Nada de titulares
  sueltos ("Definición de suma.", "La componente i-ésima del lado
  izquierdo.", "Las piezas que necesita: ...", "Tres usos de ..."):
  "Por la definición de suma podemos distribuir el selector", "Empezamos
  por la componente i-ésima del lado izquierdo", "Para demostrarla
  necesitará ...", "Hemos usado tres veces la definición de producto ...".
  Directo no significa telegráfico.
- **No leer en voz alta lo que ya está en pantalla.** La voz describe o
  nombra ("la propiedad conmutativa: el orden de los sumandos no altera
  la suma", "definición de suma", "este vector y su opuesto"), no recita
  la fórmula ("a más b es igual a b más a", "la componente i-ésima de a
  más la componente i-ésima de b"). Leerlo alarga el vídeo y aburre.
  Sin preguntas en la voz (Azure las entona mal): la pregunta va en
  pantalla y la voz la parafrasea en afirmativo. Las observaciones
  generales van en el resumen final, no intercaladas en una demostración.
- Nada aparece en pantalla y luego se recoloca: cada elemento se crea ya
  en su posición final (los `set_x`/`arrange` antes de la primera
  animación que lo muestre).
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

## Calendario de publicación en YouTube (acordado con Marcos el 2026-10-18)

Un vídeo por semana: español el **jueves a las 15:00** (Madrid; antes 18:00, cambiado por Marcos el
2026-10-19) e inglés el **sábado a las 15:00**. Se mantienen dos o tres vídeos de reserva. **No subir nada (ni en privado) hasta que Marcos dé
el último repaso** a cada vídeo, unos días después de aprobarlo.

| Vídeo | Español      | Inglés       | Estado                                  |
|-------+--------------+--------------+-----------------------------------------|
| V07   | jue 22-10-26 | sáb 24-10-26 | aprobado (19-10); falta subir es y en   |
| V08   | jue 29-10-26 | sáb 31-10-26 | HD listo; pendiente del último repaso   |
| V09   | jue 05-11-26 | sáb 07-11-26 | HD listo; pendiente del último repaso   |

**Recordatorio:** al empezar cada sesión, mirar la fecha. Si quedan tres días o menos para la
próxima publicación y ese vídeo no está subido, recordárselo a Marcos antes de nada.
Subida: la API deja en privado los vídeos de un proyecto sin auditar. Por eso el mp4 se sube a mano
en YouTube Studio, con la publicación programada allí (Programar: fecha y hora). Después se ejecuta
`lib/subir_youtube.py actualizar FICHA IDIOMA --id ID` para los metadatos, los subtítulos y la lista,
se apunta el id en la ficha y se añaden la entrada de `README.org`/`index.html` y el html del org.
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
  (6:50 es, 6:53 en) y capítulos de la ficha corregidos; HD anterior en el scratchpad de la sesión. **Publicación: es el jueves 22 y en el sábado 24 de octubre
  de 2026** (calendario más abajo), apuntar los ids en la ficha, entrada en `README.org`/`index.html` y html del org.
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
  "orden"). Inglés con Azure (Ollie) 480p el mismo día: `../videoMath2/L01_V09_MatricesRowsAndColumns_azure480p.mp4` (4:53); "...denotes a matrix." salía cortada por Azure en todas las tiradas: en plural ("Parentheses ... denote", "square brackets ... denote a matrix") sale entera. **Aprobado por Marcos en los dos idiomas y HD el 2026-10-18** (`L01_V09_MatricesFilasYColumnas.mp4`, 4:55, y `../videoMath2/L01_V09_MatricesRowsAndColumns.mp4`, 4:54, con sus srt); ficha `fichas/L01_V09.toml`. 2026-10-19: cabeceras añadidas a las escenas 2, 3 y 6 («Ejemplos», «El orden de una matriz», «Componentes, filas y columnas») y HD rehecho sin sintetizar. Falta su último repaso y la subida (5 y 7 de noviembre).
- V10 (`L01-V10-SeleccionYTransposicion.org`, Secciones 1.4.4-1.4.5; inglés
  `L01_V10_SelectionAndTransposition`): estructura aprobada por Marcos el 2026-10-18 (selector por la
  izquierda de un vector y da igual el orden; transposición, con la B de V09 = Aᵀ; matriz fila; regla
  "transponer = cambiar de lado los índices" demostrada y (Aᵀ)ᵀ = A con tarjeta de pausa). El escalar a la
  derecha y las reglas con escalares van a V11; la notación como programa, a X03. Primer uso del rótulo
  `aviso("idea")`. Prueba gTTS 480p: `L01_V10_SeleccionYTransposicion_prueba480p.mp4`, guion en
  `tmp/guion_V10_es.txt`. 2026-10-19 (Marcos): título en la escena 1, cabecera en la 2 y, en la escena 4,
  la matriz columna y la matriz fila escritas un instante como listas del libro, [(9;2);] y [(9,);(2,);],
  con «un vector de R²» / «dos vectores de R¹» (nacal: `Matrix([Vector([9]), Vector([2])])`; el
  Python, para X03). Nueva prueba: 5:17. Falta: revisión de Marcos, Azure, HD, ficha.
- **Vídeos de ampliación (serie X)**: lo más abstracto va en vídeos cortos aparte (`L01 X01`...),
  marcados como opcionales y más difíciles; plan y convenios en `NotacionNacal.org`. X01 = el apéndice
  de R⁰ que salió de V09. La frase final de V09 que lo anunciaba se quitó (2026-10-18, a `ZZ_Basura_L01_V09.org`); se decide al tener X01.
