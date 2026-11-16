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
