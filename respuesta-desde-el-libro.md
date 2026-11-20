# Respuesta desde el libro (2026-11-18)

Viene de la sesión del libro. Las respuestas completas a los
pendientes de L02-V01 están en
`../CursoDeAlgebraLineal-SRC/PendientesDesdeLosVideos.org`
(confirmadas en git allí). En resumen, la Sección 2.1 del libro queda
así:

- El apartado (a) del Ejercicio 11 dice solo «Simetría:». El
  paréntesis «(el producto punto es conmutativo)» está quitado.
- «Lineal en uno de sus argumentos» se explica antes del Ejercicio 11
  y remite a la definición de operador lineal (Definición 1.7).
- La propiedad (c) se llama «No negativo». «Definido» no cambia. El
  cambio está también en las lecciones 11 y 18.
- Tras las dos cadenas de la linealidad en el segundo argumento hay
  una frase con las reglas, y después la cadena
  x·(λy) = λ(x·y) = (λx)·y con la regla de cada paso.
- Tras el caso especial 1: «seleccionar la componente i-ésima de un
  vector es lo mismo que multiplicarlo por la columna i-ésima de la
  matriz identidad».
- La solución del Ejercicio 11(b) escribe todas las componentes con el
  selector (x|i) y ya no usa x_i.

Cambios del mismo día que vienen de los Notebooks y afectan a la
Lección 2:

- Párrafo nuevo en la Sección 2.1, antes de «Propiedades del producto
  punto»: no hay producto punto de tres vectores; (a·b)c y a(b·c) son
  en general vectores distintos.
- La Sección 2.3 enuncia, sin número, b(Aᵀ) = Ab tras la demostración
  de aB = (Bᵀ)a.
- El recuadro final de la 2.2.3 dice de qué proposición sale cada
  propiedad.
- El Ejemplo 2 de la Lección 2 ya no existe: su cuenta es la
  demostración del caso especial 2 (Ia = a). Los ejemplos posteriores
  del libro bajan un número. Las secciones, definiciones,
  proposiciones y ejercicios conservan su número.

Nada de esto está todavía en el PDF publicado.

## Tratado desde los vídeos (2026-11-18)

Leído. L02-V01 («El producto punto», sin publicar) ya usa el mismo vocabulario: «simétrico: da igual el
orden de los vectores», «conmutativa» solo para el producto de números, «nunca es negativo», y la frase de
la identidad casi literal. No cita números de ejemplo, así que no le afecta que bajen. El párrafo de que no
hay producto punto de tres vectores y b(Aᵀ) = Ab quedan anotados para los vídeos siguientes de la Lección 2;
si L02-V01 incorpora el primero, lo decidirá Marcos.

---

# Respuesta del libro (2026-11-20): pendientes de V14-V15

Tratados los tres apartados que los vídeos anotaron el 19 y el 20 de
noviembre en `PendientesDesdeLosVideos.org` del libro. Ninguno cambia
la numeración de las secciones. Commits `b087f6a` y `e8dfdb6` del libro.

- **1.4.4, nota al pie del convenio.** Hecho: la nota dice ahora
  `2\Vect{b}` y `\Vect{b}2`, como el texto y como el rótulo de V15.
- **1.5.4 y 1.6, «Transpuesta de un múltiplo».** El libro queda como
  está, con el visto bueno de Marcos: define «múltiplo» y lo usa en más
  sitios. Los vídeos pueden seguir diciendo «producto por un escalar».
- **1.5.3, «asociativo» con el selector de filas.** Hecho. La
  definición de operador lineal no cambia. Tras el recuadro de 1.5.3 se
  ha añadido: «En la segunda igualdad el escalar y el selector cambian
  de orden, como ocurría con el selector por la izquierda de los
  vectores (Sección 1.4.4). En la Sección 1.6 escribiremos el escalar a
  la derecha de la matriz y entonces bastará con desplazar los
  paréntesis.» Coincide con lo que dice V14.

**Tratada (2026-11-20, sesión de los vídeos).** Leída con Marcos; nada que cambiar en los vídeos: la nota al pie de
1.4.4 coincide con V15, «producto por un escalar» se mantiene en los vídeos (la descripción de V14 puede citar «la
transpuesta de un múltiplo» al enlazar la Sección 1.5.4) y la frase nueva de 1.5.3 coincide con la escena 3 de
V14. A raíz de ella se han apuntado en `PendientesDesdeLosVideos.org` dos pendientes más, de V13-V14: la
«cantinela» de la linealidad y el cierre de las demostraciones con «son iguales porque lo son columna a columna».
