# Encargo desde los Notebooks: lo visto en los vídeos al auditar la Lección 1

Escrito el 2026-11-16 desde la sesión del repositorio
`NAcAL-Jupyter-Notebooks-SRC`, tras hablarlo con Marcos. Siguiendo
`coordinacion-entre-repositorios.md`, aquí solo se anota: esa sesión no
ha cambiado nada de este repositorio.

Origen: una auditoría independiente de los Notebooks de la Lección 1
como guía de estudio
(`../NAcAL-Jupyter-Notebooks-SRC/informe-auditoria-leccion1.md`,
apartado 6).

## 1. Qué enlazan ahora los Notebooks

Cada Notebook enlaza los vídeos de su idioma, con los identificadores de
`fichas/L01_V*.toml`:

| Notebook | Vídeos |
|---|---|
| 1.1 | V01 |
| 1.2 | V02, V03, V04, V05, V06, V07 y V08 |
| 1.4 | V09, V10 y V11 |
| 1.5 | ninguno todavía |

V08 se enlaza desde el 2026-11-16, en un apartado final del Notebook
1.2 que propone la cuenta de la cena con las tres recetas del vídeo.

## 2. Avisar al publicar V12 a V15

Cuando se publique un vídeo hay que enlazarlo en su Notebook, en los
dos idiomas. V12 va al principio del apartado «Tipos de matrices» del
Notebook 1.4. V13, V14 y V15 van en el Notebook 1.5. Basta avisar a
Marcos o dejar aquí la fecha y los identificadores.

## 3. Las descripciones enlazan al repositorio y no al Notebook

Las descripciones de los vídeos enlazan al repositorio de los
Notebooks. Podrían enlazar al Notebook de su sección. Los enlaces son de
esta forma, y los nombres no van a cambiar:

    https://mybinder.org/v2/gh/mbujosab/nacal-jupyter-notebooks/master?urlpath=lab/tree/Esp/Lecc01-Secc1.2.ipynb
    https://mybinder.org/v2/gh/mbujosab/nacal-jupyter-notebooks/master?urlpath=lab/tree/Eng/Lecc01-Secc1.2-Eng.ipynb

## 4. La tabla de `NotacionNacal.org` y V10

La tabla asigna a V10 las secciones 1.4.3 a 1.4.4. Su guion trata filas,
columnas y componentes, que son las secciones 1.4.1 a 1.4.3. La 1.4.4
queda para V15.

## 5. V05 enuncia nueve propiedades de los reales

El libro lista ocho en el recordatorio de la Sección 1.2.1. V05 enuncia
nueve, con el inverso. El plan de los vídeos ya lo recoge. Se anota
también para el libro.

## Respuesta desde los vídeos (2026-11-16)

- **Punto 2 (avisar al publicar).** Incorporado a la rutina de publicación de `CLAUDE.md`: tras cada
  subida se anotarán aquí la fecha y los identificadores de los dos idiomas. Próximas fechas previstas:
  V12 en español el jueves 19 de noviembre y en inglés el sábado 21 (pendientes del último repaso de
  Marcos). V13, V14 y V15 están en borrador, sin fecha.
- **Punto 3 (enlace al Notebook de la sección).** Pendiente de que Marcos lo decida. Propuesta: usar el
  enlace de Binder al Notebook de la sección en las fichas nuevas, empezando por V12, y pasar las de
  V01-V11 (publicadas) con `actualizar --solo-metadatos` cuando él lo apruebe. Duda: Binder tarda en
  arrancar; quizá convenga dejar los dos enlaces, el del Notebook y el del repositorio.
- **Punto 4 (V10).** Corregido: la tabla de `NotacionNacal.org` y la cabecera de
  `L01-V10-Seleccion.org` dicen ahora Secciones 1.4.1 a 1.4.3. La descripción publicada de V10 enlaza
  la 1.4.3 (el resumen de la notación de selección) y se queda así.
- **Punto 5 (V05, nueve propiedades).** Ya recogido en el plan de los vídeos; nada que cambiar aquí.

## Añadido desde los vídeos (2026-11-16, después): punto 3 aplicado y vídeos insertables de nuevo

- **Punto 3.** Marcos lo aprueba. Las descripciones de V01 a V11, en los dos idiomas, enlazan ya al
  Notebook de su sección con Binder y, en la línea siguiente, al repositorio: V01 al 1.1, V02 a V08 al
  1.2, V09 a V11 al 1.4. La ficha de V12 (sin publicar) lleva el del 1.4; V13 a V15 llevarán el del 1.5.
- **Carátulas de los vídeos en los Notebooks.** Marcos vio en Binder «El propietario del vídeo ha
  inhabilitado su reproducción en otros sitios web». La causa estaba aquí: el script de subida, al
  actualizar los metadatos, dejaba sin querer desactivada la inserción en otras webs. Corregido el script
  y los 22 vídeos publicados (V01 a V11, es y en): vuelven a poder insertarse. Los Notebooks no tienen
  que cambiar nada.

## Publicado V12 en español (2026-11-17)

- **V12 «Tipos de matrices | Álgebra lineal 1.12»**, español: https://youtu.be/zKef0mF4YHQ (id `zKef0mF4YHQ`),
  publicado el martes 17 de noviembre, adelantado por Marcos del jueves 19. Va en «Tipos de matrices» del
  Notebook 1.4. Se puede insertar en otras webs. La versión inglesa sigue prevista para el sábado 21; su id
  se anotará aquí al publicarla.
