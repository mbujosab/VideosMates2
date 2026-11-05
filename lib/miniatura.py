"""Miniaturas de YouTube de la serie (1280x720, png), plantilla elegida por Marcos el 2026-11-03.

Composición (variante F de los prototipos; `Comprobaciones.org`, pasada 6, punto 7):
  - disco con el número «1.N» arriba a la izquierda;
  - título corto (dos a cuatro palabras, una o dos líneas) a su derecha, con tamaño de letra fijo;
  - «Álgebra lineal (Esp)» / «Linear algebra (Eng)» en pequeño bajo el título (nunca abajo a la derecha:
    ahí pone YouTube la duración);
  - el dibujo del vídeo centrado debajo, con los colores de la serie;
  - franja al pie.
El idioma se distingue de un vistazo (Marcos, 2026-11-05): en español, disco claro (azul de la serie un 50 %
hacia el blanco) con el número oscuro y franja del azul de la serie; en inglés, disco y franja BLUE_E con el
número blanco. El título va siempre en el azul de la serie.
El disco, el título y el rótulo están siempre en el mismo sitio; solo cambian el número, el texto y el dibujo.

Generar (desde lib/, con el entorno virtual de manim):
    ~/.venvs/manim/bin/python miniatura.py L01_V09 L01_V10      # es y en de cada vídeo
    ~/.venvs/manim/bin/python miniatura.py todas                # todas las de MOTIVOS
Cada una se renderiza con `manim -s` y se copia a ../miniaturas/<clave>_<idioma>.png (van a git).
Para un solo fotograma a mano:
    MINI_CLAVE=L01_V10 MINI_IDIOMA=es ~/.venvs/manim/bin/manim -s -r 1280,720 miniatura.py Miniatura

Para un vídeo nuevo:
  1. Añadir su dibujo a MOTIVOS (función que recibe el idioma y devuelve un VMobject).
  2. Poner en cada sección de idioma de su ficha `titulo_miniatura = "..."` ("\\n" parte la línea; si
     falta, se usa TITULOS de aquí o el título de la ficha hasta " | ") y
     `miniatura = "miniaturas/<clave>_<idioma>.png"`.
  3. Generarla; `subir_youtube.py subir|actualizar` la envía porque la ficha la tiene, y
     `subir_youtube.py miniatura ID FICHERO.png` pone solo la miniatura (vídeos sin ficha, V01-V04).
El número sale de la clave (L01_V10 -> 1.10).
"""
import os
import re
import shutil
import subprocess
import sys
import tomllib

from manim import *
from vm2comun import COLOR_TITULO, COLOR_ESCALAR, COLOR_A, COLOR_B, COLOR_C, COLOR_RESULTADO, myTemplate

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

# Títulos cortos de los vídeos sin ficha (es, en).
TITULOS = {
    "L01_V01": ("Vectores", "Vectors"),
    "L01_V02": ("Suma\nde vectores", "Vector addition"),
    "L01_V03": ("La suma,\ngeométricamente", "Adding,\ngeometrically"),
    "L01_V04": ("Multiplicar\npor un escalar", "Scaling vectors"),
}
FUENTE = "Latin Modern Sans"
TAM_TITULO = 80          # tamaño fijo del título (todas iguales)
ANCHO_TITULO = 10.2      # si un título no cabe, se reduce solo ese (aviso en la salida)
COLOR_FILA, COLOR_COLUMNA = COLOR_ESCALAR, GREEN   # código de V10
# Colores por idioma: (disco, número, franja)
COLORES_IDIOMA = {"es": (interpolate_color(ManimColor(COLOR_TITULO), WHITE, 0.5), "#0B2530", COLOR_TITULO),
                  "en": (BLUE_E, WHITE, BLUE_E)}
ETIQUETA_IDIOMA = {"es": "(Esp)", "en": "(Eng)"}


# ---------- piezas de dibujo ----------

def _matriz(filas, colores_col=None):
    m = IntegerMatrix(filas, h_buff=1.0, v_buff=0.9, element_to_mobject_config={"font_size": 64})
    for col, c in zip(m.get_columns(), colores_col or []):
        col.set_color(c)
    return m


def _vector_col(valores, color, fs=56):
    m = IntegerMatrix([[v] for v in valores], left_bracket="(", right_bracket=")", v_buff=0.75,
                      element_to_mobject_config={"font_size": fs, "group_with_commas": False})
    m.get_entries().set_color(color)
    return m


def _flecha(origen, fin, color, grosor=10):
    return Arrow(origen, fin, buff=0, color=color, stroke_width=grosor, max_tip_length_to_length_ratio=0.18,
                 max_stroke_width_to_length_ratio=10)


def _ejes(x0, x1, y0, y1):
    return VGroup(Line([x0, 0, 0], [x1, 0, 0], color=GREY_B, stroke_width=3),
                  Line([0, y0, 0], [0, y1, 0], color=GREY_B, stroke_width=3))


def _letra(tex, color, junto, direccion, buff=0.15, fs=64):
    return MathTex(tex, tex_template=myTemplate, font_size=fs, color=color).next_to(junto, direccion, buff=buff)


# ---------- un motivo por vídeo ----------

def motivo_v01(idioma):          # un vector: flecha y su lista de números
    ejes = _ejes(-0.5, 4.2, -0.5, 2.8)
    a = _flecha(ORIGIN, [3, 2, 0], COLOR_A)
    lista = MathTex(r"\Vect{a}=(3,\,2,)", tex_template=myTemplate, font_size=96, color=COLOR_A)
    lista.next_to(ejes, RIGHT, buff=0.8)
    return VGroup(ejes, a, lista)


def motivo_v02(idioma):          # dos vectores y su suma, uno tras otro
    a = _flecha(ORIGIN, [3, 1, 0], COLOR_A)
    b = _flecha([3, 1, 0], [4, 3, 0], COLOR_B)
    s = _flecha(ORIGIN, [4, 3, 0], COLOR_RESULTADO)
    la = _letra(r"\Vect{a}", COLOR_A, a, DOWN)
    lb = _letra(r"\Vect{b}", COLOR_B, b, RIGHT)
    ls = _letra(r"\Vect{a}+\Vect{b}", COLOR_RESULTADO, s.get_center(), UL, buff=0.25)
    return VGroup(a, b, s, la, lb, ls)


def motivo_v03(idioma):          # la regla del paralelogramo
    p, q = np.array([3, 0.6, 0]), np.array([1, 2.2, 0])
    lados = VGroup(DashedLine(p, p + q, color=GREY_B, stroke_width=4), DashedLine(q, p + q, color=GREY_B, stroke_width=4))
    a, b, s = _flecha(ORIGIN, p, COLOR_A), _flecha(ORIGIN, q, COLOR_B), _flecha(ORIGIN, p + q, COLOR_RESULTADO)
    return VGroup(lados, a, b, s, _letra(r"\Vect{a}", COLOR_A, a, DOWN), _letra(r"\Vect{b}", COLOR_B, b, LEFT),
                  _letra(r"\Vect{a}+\Vect{b}", COLOR_RESULTADO, p + q, UR, buff=0.1))


def motivo_v04(idioma):          # un vector y su múltiplo
    a = _flecha(ORIGIN, [1.6, 0.8, 0], COLOR_A, grosor=12).shift(0.9*UP + 0.45*LEFT)
    d = _flecha(ORIGIN, [4.8, 2.4, 0], COLOR_ESCALAR).shift(0.9*DOWN + 0.45*RIGHT)
    return VGroup(a, d, _letra(r"\Vect{a}", COLOR_A, a.get_end(), UP),
                  _letra(r"3\Vect{a}", COLOR_ESCALAR, d.get_end(), RIGHT))


def motivo_v05(idioma):          # una recta, a y b, y el compás llevando b detrás de a
    recta = Line([-0.6, 0, 0], [6.4, 0, 0], color=GREY_B, stroke_width=4)
    x = {"0": 0, "a": 2.2, "a+b": 3.8}
    marcas = VGroup(*[Line([v, -0.18, 0], [v, 0.18, 0], color=WHITE, stroke_width=4) for v in x.values()])
    etiquetas = VGroup(MathTex("0", font_size=60).next_to([0, 0, 0], DOWN, buff=0.3),
                       MathTex("a", font_size=60, color=COLOR_A).next_to([x["a"], 0, 0], DOWN, buff=0.3),
                       MathTex("a+b", font_size=60).next_to([x["a+b"], 0, 0], DOWN, buff=0.3))
    suelto = Line([-0.4, 1.6, 0], [1.2, 1.6, 0], color=COLOR_B, stroke_width=10)    # el segmento b, aparte
    etiquetas.add(suelto, MathTex("b", font_size=60, color=COLOR_B).next_to(suelto, UP, buff=0.2))
    seg_a = Line([0, 0, 0], [x["a"], 0, 0], color=COLOR_A, stroke_width=10)
    seg_b = Line([x["a"], 0, 0], [x["a+b"], 0, 0], color=COLOR_B, stroke_width=10)
    arco = Arc(radius=x["a+b"] - x["a"], start_angle=0, angle=PI*0.55, arc_center=[x["a"], 0, 0], color=COLOR_B, stroke_width=5)
    vertice = np.array([x["a"] + 0.8, 2.3, 0])          # el compás: dos patas
    compas = VGroup(Line([x["a"], 0, 0], vertice, color=GREY_A, stroke_width=7),
                    Line(vertice, [x["a+b"], 0, 0], color=GREY_A, stroke_width=7),
                    Dot(vertice, radius=0.12, color=GREY_A))
    return VGroup(recta, seg_a, seg_b, arco, compas, marcas, etiquetas)


def motivo_v06(idioma):          # dos vectores sumados componente a componente, y la conmutativa
    f = MathTex(r"(1,\,2,)", "+", r"(3,\,0,)", "=", r"(4,\,2,)", font_size=80)
    f[0].set_color(COLOR_A); f[2].set_color(COLOR_B)
    g = MathTex(r"\Vect{a}", "+", r"\Vect{b}", "=", r"\Vect{b}", "+", r"\Vect{a}", tex_template=myTemplate, font_size=80)
    for i, c in ((0, COLOR_A), (2, COLOR_B), (4, COLOR_B), (6, COLOR_A)):
        g[i].set_color(c)
    return VGroup(f, g).arrange(DOWN, buff=0.6)


def motivo_v07(idioma):          # un vector y su múltiplo, y la distributiva
    f = MathTex("3", r"(1,\,2,)", "=", r"(3,\,6,)", font_size=80)
    f[0].set_color(COLOR_ESCALAR); f[1].set_color(COLOR_A)
    g = MathTex(r"\lambda", r"(\Vect{a}", "+", r"\Vect{b})", "=", r"\lambda", r"\Vect{a}", "+", r"\lambda", r"\Vect{b}",
                tex_template=myTemplate, font_size=80)
    for i, c in ((0, COLOR_ESCALAR), (1, COLOR_A), (3, COLOR_B), (5, COLOR_ESCALAR), (6, COLOR_A), (8, COLOR_ESCALAR), (9, COLOR_B)):
        g[i].set_color(c)
    return VGroup(f, g).arrange(DOWN, buff=0.6)


def motivo_v08(idioma):          # una receta como vector de datos: (150; 1; 30), con sus ingredientes
    v = _vector_col([150, 1, 30], COLOR_A, fs=72)
    nombres = ("patatas (g)", "huevos", "cebolla (g)") if idioma == "es" else ("potatoes (g)", "eggs", "onion (g)")
    filas = v.get_rows()
    etiquetas = VGroup(*[Text(n, font=FUENTE, font_size=44, color=GREY_B).match_y(f) for n, f in zip(nombres, filas)])
    etiquetas.arrange_in_grid(cols=1, col_alignments="r", buff=0)
    for e, f in zip(etiquetas, filas):
        e.match_y(f)
    etiquetas.next_to(v, LEFT, buff=0.4)
    return VGroup(etiquetas, v)


def motivo_v09(idioma):          # una matriz: lista de columnas
    return _matriz([[1, 3, 5], [2, 4, 6]], [COLOR_A, COLOR_B, COLOR_C])


def motivo_v10(idioma):          # una fila y una columna seleccionadas
    m = _matriz([[1, 3, 5], [2, 7, 6]])
    fila, col = m.get_rows()[1], m.get_columns()[1]
    fila.set_color(COLOR_FILA)
    col.set_color(COLOR_COLUMNA)
    col[1].set_color(WHITE)
    return VGroup(m, SurroundingRectangle(fila, color=COLOR_FILA, buff=0.12, stroke_width=5),
                  SurroundingRectangle(col, color=COLOR_COLUMNA, buff=0.12, stroke_width=5))


def motivo_v11(idioma):          # transponer: las columnas pasan a filas
    a = _matriz([[1, 3], [2, 4]], [COLOR_A, COLOR_B])
    t = MathTex(r"\T", tex_template=myTemplate, font_size=72).next_to(a, UR, buff=0.05).shift(0.25*DOWN)
    b = _matriz([[1, 2], [3, 4]])
    for fila, c in zip(b.get_rows(), (COLOR_A, COLOR_B)):
        fila.set_color(c)
    return VGroup(VGroup(a, t), MathTex("=", font_size=72), b).arrange(RIGHT, buff=0.35)


def motivo_v12(idioma):          # una matriz simétrica: diagonal en amarillo, pares iguales a ambos lados
    m = _matriz([[1, 2, 3], [2, 4, 5], [3, 5, 6]])
    e = m.get_entries()
    for k in (0, 4, 8):
        e[k].set_color(COLOR_ESCALAR)
    for (i, j), c in (((1, 3), COLOR_A), ((2, 6), COLOR_B), ((5, 7), COLOR_C)):
        e[i].set_color(c); e[j].set_color(c)
    t = MathTex(r"\Mat{S}", "=", r"\MatT{S}", tex_template=myTemplate, font_size=72)
    return VGroup(m, t).arrange(RIGHT, buff=0.8)


MOTIVOS = {f"L01_V{n:02d}": f for n, f in enumerate(
    [motivo_v01, motivo_v02, motivo_v03, motivo_v04, motivo_v05, motivo_v06, motivo_v07, motivo_v08,
     motivo_v09, motivo_v10, motivo_v11, motivo_v12], start=1)}
ESCALA_EXTRA = {"L01_V11": 0.9}     # V11: la ecuación es lo más ancho; un diez por ciento menor


def titulo_corto(clave, idioma):
    ruta = os.path.join(RAIZ, "fichas", clave + ".toml")
    if os.path.exists(ruta):
        sec = tomllib.load(open(ruta, "rb")).get(idioma, {})
        if sec.get("titulo_miniatura"):
            return sec["titulo_miniatura"]
        if clave not in TITULOS:
            return sec["titulo"].partition(" | ")[0]
    return TITULOS[clave][idioma == "en"]


class Miniatura(Scene):
    def construct(self):
        clave = os.environ.get("MINI_CLAVE", "L01_V10")
        idioma = os.environ.get("MINI_IDIOMA", "es")
        lec, vid = re.match(r"L(\d+)_V(\d+)", clave).groups()
        numero = f"{int(lec)}.{int(vid)}"
        W, H = config.frame_width, config.frame_height
        self.camera.background_color = BLACK

        c_disco, c_numero, c_franja = COLORES_IDIOMA[idioma]
        franja = Rectangle(width=W, height=0.18, stroke_width=0, fill_color=c_franja, fill_opacity=1).to_edge(DOWN, buff=0)
        disco = Circle(radius=1.15, stroke_width=0, fill_color=c_disco, fill_opacity=1)
        num = Text(numero, font=FUENTE, weight=BOLD, font_size=100, color=c_numero)
        num.scale_to_fit_width(min(num.width, 1.85)).move_to(disco)
        sello = VGroup(disco, num).move_to([-W/2 + 0.5 + 1.15, H/2 - 0.5 - 1.15, 0])

        izquierda = sello.get_right()[0] + 0.5
        lineas = titulo_corto(clave, idioma).split("\n")
        titulo = VGroup(*[Text(l, font=FUENTE, weight=BOLD, font_size=TAM_TITULO) for l in lineas])
        titulo.arrange(DOWN, aligned_edge=LEFT, buff=0.2).set_color(COLOR_TITULO)
        if titulo.width > ANCHO_TITULO:
            print(f"AVISO {clave} {idioma}: título reducido para que quepa")
            titulo.scale_to_fit_width(ANCHO_TITULO)
        # dos líneas caben en el alto del disco; una sola se centra con él
        titulo.move_to([izquierda + titulo.width/2, sello.get_y(), 0])
        rotulo = Text(("Álgebra lineal " if idioma == "es" else "Linear algebra ") + ETIQUETA_IDIOMA[idioma],
                      font=FUENTE, font_size=40, color=GREY_B)
        rotulo.move_to([izquierda + rotulo.width/2, sello.get_bottom()[1] - 0.35, 0])

        dibujo = MOTIVOS[clave](idioma)
        dibujo.scale_to_fit_height(3.5)
        if dibujo.width > 0.72*W:
            dibujo.scale_to_fit_width(0.72*W)
        dibujo.scale(ESCALA_EXTRA.get(clave, 1))
        arriba, abajo = rotulo.get_bottom()[1] - 0.3, franja.get_top()[1] + 0.3
        dibujo.move_to([0, (arriba + abajo)/2, 0])
        self.add(franja, sello, titulo, rotulo, dibujo)


def genera(claves):
    destino = os.path.join(RAIZ, "miniaturas")
    os.makedirs(destino, exist_ok=True)
    for clave in claves:
        for idioma in ("es", "en"):
            nombre = f"{clave}_{idioma}"
            env = {**os.environ, "MINI_CLAVE": clave, "MINI_IDIOMA": idioma}
            r = subprocess.run([os.path.join(os.path.dirname(sys.executable), "manim"), "-s", "-r", "1280,720",
                                "--disable_caching", "-v", "WARNING", "miniatura.py", "Miniatura", "-o", nombre],
                               cwd=AQUI, env=env, capture_output=True, text=True)
            for linea in (r.stdout + r.stderr).splitlines():
                if "AVISO" in linea:
                    print(linea)
            if r.returncode:
                sys.exit(f"Falló {nombre}:\n{r.stderr[-2000:]}")
            shutil.copy(os.path.join(AQUI, "media", "images", "miniatura", nombre + ".png"),
                        os.path.join(destino, nombre + ".png"))
            print("hecha", os.path.join("miniaturas", nombre + ".png"))


if __name__ == "__main__":
    args = sys.argv[1:]
    genera(sorted(MOTIVOS) if args in ([], ["todas"]) else args)
