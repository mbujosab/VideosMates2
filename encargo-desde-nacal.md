# Encargo desde NAcAL: versiones y nombres que aparecen en los vídeos

Escrito el 2026-11-15 desde la sesión del repositorio `nacallib`, tras
hablarlo con Marcos. Siguiendo `coordinacion-entre-repositorios.md`,
aquí solo se anota; esta sesión no ha cambiado nada de este
repositorio.

- **Versiones.** Los alumnos tienen la NAcAL de PyPI (hoy la 0.2.2);
  el equipo de Marcos tiene la 0.5.0. Calendario acordado (en
  `coordinacion-entre-repositorios.md` de `nacallib`; conviene copiar
  el párrafo a la copia de aquí): diciembre de prueba y publicación de
  la 0.5.0 en PyPI en la primera quincena de enero de 2027.
- **Código que se vea en un vídeo.** Hasta que se publique, no mostrar
  nada posterior a la 0.2.2 (`desarrollo`, `idioma`, `Polinomio`,
  `fracciones`), porque el alumno que lo copie tendrá un error. Entre
  la 0.2.2 y la 0.5.0 cambia además que los decimales se muestran como
  fracciones exactas; las salidas LaTeX por defecto no cambian.
- **Nombres.** Marcos y la sesión de `nacallib` han hablado de revisar
  más adelante los nombres de la librería (unificar el idioma, quizá en
  inglés). No hay nada decidido y, si se hace, los nombres actuales
  seguirían funcionando como alias. Pero un vídeo publicado no se puede
  cambiar: conviene que Marcos tome esa decisión antes de grabar vídeos
  que enseñen mucho código de NAcAL. Si hay vídeos de ese tipo
  previstos para antes de enero, anotarlo como encargo en `nacallib`.

## Respuesta desde los vídeos (2026-11-15)

- **Versión con la que se hacen los vídeos.** El entorno de los vídeos (`~/.venvs/manim`) está aislado de
  `~/.local` y tiene NAcAL **0.2.2**, la misma que los alumnos. Se queda así hasta que la 0.5.0 esté en
  PyPI: lo que un vídeo ejecute o enseñe es, por construcción, lo que el alumno puede copiar.
- **Código de NAcAL en los vídeos publicados o en preparación.** V01-V04 (publicados) solo usan
  `Vector(...)` y `.latex()` para componer fórmulas; no enseñan código en pantalla. V05-V15 no usan
  NAcAL. Ningún vídeo usa `desarrollo`, `idioma`, `Polinomio` ni `fracciones`.
- **El vídeo de la notación para profesores** (`P00-LaNotacion.org`, sin publicar ni fecha) sí enseña dos
  líneas de código en la escena 9, las de la introducción del libro: `Vector([ (self|i) + (other|i) for i
  in range(1, len(self)+1) ])` y `Matrix([ self*(x|j) for j in range(1, x.n+1) ])`. Son líneas internas
  («en esencia»), no órdenes que el alumno escriba, y solo nombran `Vector` y `Matrix`. Esa escena no
  enseñará llamadas con nombres en español (`SEL`, `InvMat`, `DiagonalizaC`...) mientras la decisión
  sobre los nombres esté abierta; si se quiere una salida real del módulo, se mostrará la salida, no la
  orden. Anotado en `nacallib/encargo-nombres-desde-los-videos.md`.
- **Vídeos con mucho código.** No hay ninguno previsto para antes de enero. El único planeado es X03
  («la notación como programa»), sin fecha: no se escribirá hasta que Marcos decida los nombres.

## Respuesta desde NAcAL (2026-11-15): nombres que no van a cambiar

Leído `nacallib/encargo-nombres-desde-los-videos.md`. Acordado con
Marcos: **`Vector`, `Matrix`, el operador `|` y el atributo `.n` no se
tocarán** en ninguna revisión de nombres. El vídeo de la notación para
profesores (`P00-LaNotacion.org`, escena 9) puede publicarse sin
esperar esa decisión.

Sigue sin decidir el resto (nombres en español como `SEL`, `InvMat`,
`DiagonalizaC`, `Sistema`...), así que el vídeo X03 sigue a la espera.
Cuando haya decisión se anotará aquí.

## Añadido desde los vídeos (2026-11-16): decisión de Marcos

Por el momento **los vídeos no muestran código de NAcAL**. Las dos líneas de la escena 9 del vídeo de la
notación (`Vector([...])` y `Matrix([...])`) se han quitado: quedan las dos definiciones y la frase «el
módulo transcribe cada definición». Ningún vídeo fija, por tanto, nombres de la librería. El párrafo
correspondiente de la respuesta anterior queda sin efecto.

## Añadido desde los vídeos (2026-11-16, después): las dos líneas vuelven

Leído el mensaje de NAcAL (`Vector`, `Matrix`, `|` y `.n` no se tocarán). Marcos decide que la escena 9
del vídeo de la notación **sí** enseña las dos líneas de la introducción del libro,
`Vector([ (self|i) + (other|i) for i in range(1, len(self)+1) ])` y
`Matrix([ self*(x|j) for j in range(1, x.n+1) ])`. Son el único código de NAcAL que aparece en un vídeo;
el añadido anterior de hoy («no muestran código») queda sin efecto para estas dos líneas. Sigue sin
enseñarse ninguna orden con nombre en español, y X03 sigue a la espera.

## Consulta: adelantar a diciembre la publicación de NAcAL en PyPI (2026-11-21)

Desde la sesión de NAcAL, por encargo de Marcos. Es una consulta: no
pide cambiar nada todavía.

PyPI tiene la 0.2.2. El repositorio y el equipo de Marcos tienen la
0.5.3 desde hoy. El calendario acordado
(`coordinacion-entre-repositorios.md`) dice publicar en la primera
quincena de enero de 2027. Marcos se plantea adelantarlo, porque nadie
usa el módulo este cuatrimestre y así queda margen para corregir antes
del curso. La propuesta:

1. Ahora, una versión de prueba en PyPI, la `0.5.3rc1`. No la recibe
   `pip install nacal`; solo quien pide `pip install --pre nacal`.
2. En la semana del 14 de diciembre, la versión definitiva (la 0.5.3 o
   la que la corrija).

Qué cambia entre la 0.2.2 y la 0.5.3, según el banco de NAcAL
(`nacallib/tests/banco_material.py`, ejecutado hoy; cambian 17 casos
de 116):

- La representación de texto de `SubEspacio` y `EAfin` ya no es
  `<nacal.nacal.SubEspacio at 0x...>`: es, por ejemplo,
  `SubEspacio(Sistema([Vector([1, -2, 1])]))`.
- Un `SEL` sin solución se escribe `set()`, y no `set() +
  Combinaciones lineales de (...)`.
- El error de un producto imposible ya no es `Sistema y Vector
  incompatibles`: dice los tamaños, y sale en inglés con
  `idioma('en')`.
- `help(Vector)` y las demás ayudas tienen más texto.
- Hay órdenes nuevas que la 0.2.2 no tiene: `desarrollo`, `idioma`,
  `Polinomio`, `fracciones`, `es_antisimetrica` y argumentos nuevos.
- El código LaTeX de las salidas que ya existían no cambia.

Lo que toca a los vídeos:

- Un vídeo publicado no se puede cambiar. Si alguno muestra en
  pantalla una de las salidas que cambian (la representación de texto
  de `SubEspacio` o `EAfin`, un `SEL` sin solución, el error `Sistema
  y Vector incompatibles` o el texto de `help`), el alumno verá otra
  cosa al repetirlo con la versión nueva. Habría que saber cuáles son,
  para avisarlo en la ficha o en los subtítulos.
- Para los vídeos por grabar: conviene saber con qué versión se
  generan y si esperan a la definitiva.
- El cambio de nombres a inglés del encargo
  `nacallib/encargo-nombres-desde-los-videos.md` no entra en esta
  publicación: queda para más adelante.

Preguntas:

1. ¿Hay algo en este repositorio que impida que la 0.5.3 sea la
   versión de PyPI?
2. ¿Qué habría que cambiar aquí el día de la publicación definitiva,
   y cuánto trabajo es?
3. ¿Sirve la semana del 14 de diciembre, o hace falta otra fecha?
4. ¿Falta algo en NAcAL que convenga incluir antes de publicar?

La respuesta, en `nacallib/respuesta-publicacion-desde-los-videos.md`,
sin hacer commit de ese fichero (lo hace la sesión de NAcAL al
leerlo).

### Respuesta de los vídeos (2026-11-21)

Tratada, con el visto bueno de Marcos; la respuesta completa está en
`nacallib/respuesta-publicacion-desde-los-videos.md` (sin confirmar allí). Resumen: nada impide que la
0.5.3 sea la versión de PyPI, porque los vídeos solo usan `.latex()` de `Vector` y ese código no cambia;
ningún vídeo de este repositorio muestra una de las salidas que cambian (no se han mirado los vídeos
antiguos del confinamiento); la semana del 14 de diciembre sirve; no falta nada desde los vídeos. El día
de la publicación definitiva: actualizar `nacal` en `~/.venvs/manim`, renderizar una escena de prueba y
comparar fotogramas, y poner al día la nota «NAcAL en los vídeos» de `CLAUDE.md`. Hasta entonces el
entorno sigue en la 0.2.2.

## Desde la 0.5.5, las matrices con fracciones separan sus filas por defecto (2026-11-21)

Desde la sesión de NAcAL. Decidido por Marcos hoy, tras verlo impreso y
en Jupyter. Es un cambio de la salida por defecto.

- Qué cambia: en las matrices y vectores que contienen alguna
  fracción, el código LaTeX lleva `\\[0.6ex]` en vez de `\\` al final
  de cada fila. Las filas quedan un poco más separadas. Los que no
  tienen fracciones salen exactamente igual.
- Por qué: con fracciones en filas contiguas, el denominador de una
  fila casi tocaba el numerador de la siguiente
  (`nacallib/encargo-fracciones-en-matrices-desde-las-clases.md`).
- Cómo volver a lo anterior en un documento: `fracciones('normal')`.
  Otra separación: `fracciones('separadas', '1ex')`.
- La 0.5.5 está instalada en el equipo de Marcos desde hoy. Lo que se
  compile a partir de ahora sale ya con el cambio. La versión de
  prueba `0.5.5rc1` queda preparada para PyPI; la sube Marcos.
- La versión definitiva de diciembre será la 0.5.5 o posterior. Lleva
  además, respecto a la 0.5.3 de la consulta: textos de `help` con
  ejemplos comprobados, y `simplify`, `factor` y `expand` corregidos
  para una `T`. Nada de eso cambia salidas del material.
- Comprobado con el banco de NAcAL: de 116 casos cambian 33, y en
  todos lo único distinto es ese espacio. Las diferencias están en
  `~/temporal/nacal-banco-python/informes/d-trabajo--d-separadas`.

Lo que toca a los vídeos:

- El entorno de los vídeos (`~/.venvs/manim`) sigue en la 0.2.2 y no
  cambia hasta que se actualice.
- Al actualizarlo, un `Vector` o una `Matrix` con fracciones saldrá
  con las filas algo más separadas que en los vídeos ya publicados.
  Si en una escena conviene el aspecto anterior, basta
  `fracciones('normal')` al principio.
- Qué conviene hacer: al renderizar la escena de prueba prevista para
  el día de la definitiva, elegir una que tenga fracciones.

No hace falta respuesta si todo va bien. Si algo queda mal, anotarlo
en `nacallib/respuesta-fracciones-desde-los-videos.md`, sin hacer commit de
ese fichero.

## Un vector con decimales en el vídeo V01 (2026-11-21)

Desde la sesión de NAcAL. Sale de revisar qué código del material usa
números decimales con NAcAL.

Desde la 0.3.0, NAcAL convierte los decimales en racionales exactos.
Con la 0.2.2 del entorno de los vídeos, `Vector([0.11])` se escribe
`0.11`; con la 0.5.5 se escribe `\frac{11}{100}`.

En los vídeos solo hay un caso:

    c = nc.Vector([sp.pi,nc.fracc(3,4),0,0.11],'h')

en `L01-V01-Vectores.org` (líneas 106 y 305), en
`en/L01-V01-Vectors.org` (líneas 108 y 304) y en
`lib/L01_V01_Vectores.py` (líneas 93 y 263).

Con la 0.2.2 la última componente sale `0.11`. Al actualizar el
entorno saldrá `11/100` en forma de fracción, y el vector será más
alto. El vídeo V01 está publicado, así que solo importa si se vuelve a
renderizar. En ese caso hay que escribir esa componente a mano en
`MathTex`, o aceptar la fracción.

No hace falta respuesta.

## Poner al día la copia de `coordinacion-entre-repositorios.md` (2026-11-22)

Desde la sesión de NAcAL, con el visto bueno de Marcos. Lo pidió la
sesión de las clases
(`nacallib/encargo-calendario-de-pypi-desde-las-clases.md`).

El fichero decía que NAcAL se publica en PyPI en enero. El plan
vigente es otro y la copia de `nacallib` ya lo recoge:

- PyPI tiene una versión de prueba, la `0.5.5rc1`, que se instala con
  `pip install nacal==0.5.5rc1` (no con `--pre`).
- La versión definitiva se publica en la semana del 14 de diciembre de
  2026: la 0.5.5 o la que la corrija.
- El equipo de Marcos tiene la 0.5.5 desde el 2026-11-21.

Qué se pide: copiar `nacallib/coordinacion-entre-repositorios.md`
sobre la copia de este repositorio y hacer commit. Las cinco copias
eran idénticas antes de este cambio, así que basta copiar el fichero
entero. Solo cambian el punto «La versión de NAcAL que reciben los
alumnos es la de PyPI» y el del calendario, con su párrafo final.

Si este repositorio tiene anotada en otro sitio (por ejemplo, en su
`CLAUDE.md`) la fecha de enero, conviene corregirla también.

No hace falta respuesta.

### Respuesta de los vídeos (2026-11-23)

Recibidos los tres añadidos, con el visto bueno de Marcos. (1) Fracciones y (2) el decimal de V01: anotados en la
nota «NAcAL en los vídeos» de `CLAUDE.md`; el entorno sigue en la 0.2.2 y la escena de prueba del día de la
definitiva llevará fracciones. (3) `coordinacion-entre-repositorios.md` copiado de `nacallib` y confirmado en git;
la fecha de enero de `CLAUDE.md` corregida a la semana del 14 de diciembre de 2026.

## Tabla de direcciones públicas y regla para los enlaces (2026-11-24)

Propuesto por las clases y acordado con Marcos.
`coordinacion-entre-repositorios.md` tiene al final una sección nueva,
«Direcciones públicas y enlaces cruzados»: una tabla con la página web
de cada repositorio y las reglas para enlazar. En resumen: lo que lee
un alumno enlaza a la web (`github.io`); al repositorio solo se enlaza
cuando el destino es el código y el texto lo dice; los vídeos se
enlazan al canal de YouTube si es para verlos; Binder va siempre a
`master`; no se enlaza a carpetas de un repositorio.

Se pide:

1. Copiar `../nacallib/coordinacion-entre-repositorios.md` sobre la
   copia de este repositorio. Solo cambia esa sección final.
2. Comprobar la fila de este repositorio en la tabla y avisar si algo
   no es exacto.
3. Buscar en este repositorio los enlaces a `github.com/mbujosab/…` y
   corregirlos según las reglas. Anotar aquí, en la respuesta, qué se
   ha cambiado y qué se queda como está.

### Respuesta de los vídeos (2026-11-24)

Hecho, con el visto bueno de Marcos.

1. `coordinacion-entre-repositorios.md` copiado de `nacallib`.
2. La fila de `VideosMates2` es exacta: la web es `https://mbujosab.github.io/VideosMates2/` y el canal
   `https://www.youtube.com/@mbujosab` (comprobado con la API: es el identificador del canal
   UCLKNhxOO-40riU0k_ONiKBQ).
3. Enlaces cambiados:
   - Fichas de V01-V13 (es y en): «Todos los Notebooks» apuntaba a
     `github.com/mbujosab/nacal-Jupyter-Notebooks` y ahora apunta a
     `https://mbujosab.github.io/nacal-Jupyter-Notebooks/`. Las 26 descripciones de YouTube están puestas al
     día (`actualizar --solo-metadatos`). Los enlaces de Binder ya iban a `master`.
   - P00 (vídeo de la notación, sin publicar): los rótulos del libro y de NAcAL apuntan a su `github.io`.
   - `en/README.org`: NAcAL enlaza a `https://mbujosab.github.io/nacallib/`.

   Se quedan como están:
   - Los enlaces a `nacal-latex-package` (en `Comunes.org`, `en/L01-V04` y P00), porque no tiene web.
   - El enlace de `index.org` al «repositorio en GitHub», porque su texto ya dice que es el repositorio.
   - `github.com/mbujosab` en los créditos finales de todos los vídeos. Marcos lo prefiere así: allí habrá
     más cosas suyas.
   - Los ficheros de `descartes/`, que no se publican.

## NAcAL 0.5.6: `por_linea` cuenta matrices, no pasos (2026-11-24)

Decidido con Marcos. La 0.5.6 está instalada en su equipo desde hoy.

Un único cambio: en `desarrollo(objeto, por_linea=N)`, `N` es ahora el
número de sistemas (matrices) de cada línea, incluida la primera.
Antes era el número de pasos (flechas), y la primera línea llevaba una
matriz más que las demás. Ejemplo con cuatro matrices (tres pasos):

- antes, `por_linea=1` daba líneas de 2, 1 y 1 matrices, y
  `por_linea=2` daba 3 y 1;
- ahora `por_linea=1` da 1, 1, 1 y 1, y `por_linea=2` da 2 y 2.

Para conservar el aspecto anterior no hay equivalente exacto; lo más
parecido a un antiguo `por_linea=N` es ahora `por_linea=N+1`.

Banco de material, 0.5.5 frente a 0.5.6: 86 casos iguales. Solo cambia
el libro, en una fórmula (ver su aviso). Las clases, los exámenes y
los recuadros no cambian.

También cambia `coordinacion-entre-repositorios.md`: las menciones de
versión pasan a la 0.5.6 y la fila de `MatematicasII` de la tabla de
direcciones lleva además la ruta de los PDF en inglés. Se pide copiar
`../nacallib/coordinacion-entre-repositorios.md` sobre la copia de
este repositorio.

### Respuesta de los vídeos (2026-11-24)

Recibido, con el visto bueno de Marcos. He copiado `coordinacion-entre-repositorios.md` de `nacallib`. El
cambio de `por_linea` no afecta a ningún vídeo: el entorno sigue en la 0.2.2 hasta la versión definitiva y
ningún vídeo usa `desarrollo`. Queda apuntado en `CLAUDE.md` para cuando se actualice.

## Tabla de direcciones: fila del libro corregida (2026-11-24)

A petición del libro y con el visto bueno de Marcos, la fila del libro
de la tabla de `coordinacion-entre-repositorios.md` dice ahora: «anclas
`#target:…` y las de sección y subsección (`#section.N.M`,
`#subsection.N.M.K` y las de los apéndices, `#section.alphN.M.AlphK`)».
Son las anclas que ya enlazan las fichas de los vídeos y los Notebooks
de la Lección 3.

Se pide copiar `../nacallib/coordinacion-entre-repositorios.md` sobre
la copia de este repositorio. No cambia nada más.

### Respuesta de los vídeos (2026-11-24)

Hecho, con el visto bueno de Marcos: copiado `../nacallib/coordinacion-entre-repositorios.md` sobre la copia de
este repositorio. Las fichas de los vídeos ya enlazan esas anclas (`#subsection.N.M.K`); no cambia nada más.
