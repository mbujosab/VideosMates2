from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("El producto punto", "The dot product")

A_EJ = [1, 2, 3]      # el ejemplo del libro (Sección 2.1)
B_EJ = [1, -1, 2]
COLOR_COLUMNA = GREEN

# Glifos de las cuentas (contados con una imagen numerada; véase cada escena)
EJ_AB = [r"\Vect{a}\cdot\Vect{b}", "=", r"1\cdot 1", "+", r"2\cdot(-1)", "+", r"3\cdot 2", "=", "1", "-2", "+6", "=", "5"]
EJ_BA = [r"\Vect{b}\cdot\Vect{a}", "=", r"1\cdot 1", "+", r"(-1)\cdot 2", "+", r"2\cdot 3", "=", "1", "-2", "+6", "=", "5"]
EJ_BB = [r"\Vect{b}\cdot\Vect{b}", "=", r"1\cdot 1", "+", r"(-1)\cdot(-1)", "+", r"2\cdot 2", "=", "1", "+1", "+4", "=", "6"]
EJ_ID = [r"\Vect{a}\cdot\VectCpE{I}{2}", "=", r"1\cdot 0", "+", r"2\cdot 1", "+", r"3\cdot 0", "=", "2"]
DEF = [r"\Vect{a}\cdot\Vect{b}", "=", r"\eleVRpE{a}{1}\eleVRpE{b}{1}", "+", r"\eleVRpE{a}{2}\eleVRpE{b}{2}", "+",
       r"\cdots", "+", r"\eleVRpE{a}{n}\eleVRpE{b}{n}"]
# la cadena de la simetría: L0 = a·b = (a|1)(b|1) + ⋯ + (a|n)(b|n) (29 glifos: a · b = 0-3; (a|1) 4-8; (b|1) 9-13;
# + 14; ⋯ 15-17; + 18; (a|n) 19-23; (b|n) 24-28); L1 = = (b|1)(a|1) + ⋯ + (b|n)(a|n) (26: = 0; (b|1) 1-5;
# (a|1) 6-10; + 11; ⋯ 12-14; + 15; (b|n) 16-20; (a|n) 21-25); L2 = = b · a (4)
CADENA = [r"\Vect{a}\cdot\Vect{b}=\eleVRpE{a}{1}\eleVRpE{b}{1}+\cdots+\eleVRpE{a}{n}\eleVRpE{b}{n}",
          r"=\eleVRpE{b}{1}\eleVRpE{a}{1}+\cdots+\eleVRpE{b}{n}\eleVRpE{a}{n}",
          r"=\Vect{b}\cdot\Vect{a}"]


def vector_col(valores, color=WHITE, escala=0.8):
    """Un vector numérico en vertical, entre paréntesis, con sus componentes accesibles."""
    v = IntegerMatrix([[x] for x in valores], v_buff=0.62, left_bracket="(", right_bracket=")")
    v.get_entries().set_color(color)
    return v.scale(escala)


def matriz(filas, color=WHITE, escala=0.8, h_buff=1.0):
    m = IntegerMatrix(filas, v_buff=0.62, h_buff=h_buff)
    m.get_entries().set_color(color)
    return m.scale(escala)


def con_nombre(tex, mob, font_size=48):
    return VGroup(MathTex(tex, tex_template=myTemplate, font_size=font_size), mob).arrange(RIGHT, buff=0.2)


def franja_columna(m, j, color=COLOR_COLUMNA):
    """Franja translúcida sobre la columna j (desde 0) de la matriz m (como en V10 y V12)."""
    col = m.get_columns()[j]
    return Rectangle(width=col.width + 0.35, height=m.get_brackets()[0].height, stroke_width=0, fill_color=color,
                     fill_opacity=0.22).move_to([col.get_x(), m.get_y(), 0])


def marco(mob, color=COLOR_ESCALAR):
    return SurroundingRectangle(mob, color=color, buff=0.1, corner_radius=0.08, stroke_width=3)


def resalta(escena, mobs, color=COLOR_ESCALAR, factor=1.3, run_time=0.3):
    """Resaltado inmediato y sostenido (color y tamaño), sin la subida lenta de Indicate."""
    escena.play(*[x.animate.set_color(color).scale(factor) for x in mobs], run_time=run_time)


def apaga(escena, mobs, color=WHITE, factor=1.3, run_time=0.3):
    escena.play(*[x.animate.set_color(color).scale(1/factor) for x in mobs], run_time=run_time)


CAMPANITA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos", "campanita.wav")   # suena al subir un contador


class Panel:
    """Panel de herramientas (como en V06 y V13): la definición a la izquierda y la propiedad de los números
    reales a la derecha, en pequeño. Cada uso se cuenta con una insignia y la campanita."""
    def __init__(self, escena, y_sup=2.85, font_size=30):
        self.escena, self.usos, self.contadores, self.cajas = escena, {}, {}, {}
        self.piezas = {"def": MathTex(CADENA[0], tex_template=myTemplate, font_size=font_size),
                       "conm": MathTex(r"\alpha\beta=\beta\alpha", tex_template=myTemplate, font_size=font_size)}
        cab_izq = Tex(tr("Definición", "Definition"), font_size=24).set_color(GRAY_B)
        cab_der = Tex(tr("Números reales", "Real numbers"), font_size=24).set_color(GRAY_B)
        self.izq = VGroup(cab_izq, self.piezas["def"]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=0.4)
        self.der = VGroup(cab_der, self.piezas["conm"]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=1.0)
        for g in (self.izq, self.der):
            g.align_to([0, y_sup, 0], UP)
        self.todo = VGroup(self.izq, self.der)

    def senala(self, clave):
        return Indicate(self.piezas[clave], color=COLOR_RESULTADO, scale_factor=1.12)

    def pista(self, *claves):
        """Las piezas que hacen falta pasan a amarillo y se recuadran (el amarillo solo no se ve en baja resolución)."""
        for c in claves:
            self.cajas[c] = marco(self.piezas[c])
        self.escena.play(*[self.piezas[c].animate.set_color(COLOR_ESCALAR) for c in claves],
                         *[Create(self.cajas[c]) for c in claves], run_time=0.8)

    def quita_pista(self):
        self.escena.play(*[self.piezas[c].animate.set_color(WHITE) for c in self.cajas],
                         *[FadeOut(b) for b in self.cajas.values()], run_time=0.5)
        self.cajas = {}

    def cuenta(self, clave, run_time=0.5):
        """Después del paso: sube el contador de usos de la pieza, con la campanita (insignia de V06)."""
        pieza = self.piezas[clave]
        self.usos[clave] = self.usos.get(clave, 0) + 1
        disco = Circle(radius=0.17, fill_color=COLOR_TITULO, fill_opacity=1, stroke_width=0)
        numero = Tex(f"\\textbf{{{self.usos[clave]}}}", font_size=24).set_color(WHITE).move_to(disco)
        nuevo = VGroup(disco, numero).move_to([pieza.get_right()[0] + 0.3 + 0.17, pieza.get_y() + 0.1, 0])
        self.escena.add_sound(CAMPANITA)
        if clave in self.contadores:
            self.escena.play(ReplacementTransform(self.contadores[clave], nuevo), run_time=run_time)
        else:
            self.escena.play(FadeIn(nuevo, scale=0.5), run_time=run_time)
        self.contadores[clave] = nuevo

    def parpadea(self, clave):
        """En la conclusión, cada contador parpadea cuando la voz nombra su pieza (Marcos, V11)."""
        return [Indicate(self.contadores[clave], color=COLOR_ESCALAR, scale_factor=1.5),
                Indicate(self.piezas[clave], color=COLOR_ESCALAR, scale_factor=1.1)]


def nace(escena, origen, destino, fijos, moviles=(), aparecen=(), con_igual=True, extra=(), marca=None,
         t_fijos=0.8, t_moviles=0.9):
    """Una expresión nace de la anterior (V13): primero se copia lo que no cambia (fijos) y aparece el igual;
    después (en la marca, si se da) viaja lo que el paso mueve (moviles) y surge lo nuevo (aparecen). Si dos
    glifos de origen se reúnen en uno de destino, el segundo viaja como copia y se retira."""
    cubiertos = sorted({j for _, j in fijos} | {j for _, j in moviles} | set(aparecen) | ({0} if con_igual else set()))
    assert cubiertos == list(range(len(destino))), (cubiertos, len(destino))
    escena.play(*extra, *([FadeIn(destino[0])] if con_igual else []),
                *[TransformFromCopy(origen[i], destino[j]) for i, j in fijos], run_time=t_fijos)
    if marca is not None:
        escena.wait_until_bookmark(marca)
    if moviles or aparecen:
        vistos, anims, sobran = set(), [], []
        for i, j in moviles:
            if j in vistos:
                viajero = origen[i].copy()
                sobran.append(viajero)
                anims.append(Transform(viajero, destino[j].copy()))
            else:
                vistos.add(j)
                anims.append(TransformFromCopy(origen[i], destino[j]))
        escena.play(*anims, *[FadeIn(destino[j]) for j in aparecen], run_time=t_moviles)
        escena.remove(*sobran)


def entera(escena, linea):
    """Tras nacer glifo a glifo, la línea vuelve a estar en la escena como un solo objeto."""
    escena.remove(*linea[0]); escena.add(linea)

class L02_V01_ProductoPunto(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        a, b = vector_col(A_EJ, COLOR_A), vector_col(B_EJ, COLOR_B)
        na, nb = con_nombre(r"\Vect{a}=", a), con_nombre(r"\Vect{b}=", b)
        na[0].set_color(COLOR_A); nb[0].set_color(COLOR_B)
        VGroup(na, nb).arrange(RIGHT, buff=2.2).move_to([0, 0.9, 0])
        cuenta = MathTex(*EJ_AB, tex_template=myTemplate, font_size=46).move_to([0, -1.7, 0])
        cuenta[0][0].set_color(COLOR_A); cuenta[0][2].set_color(COLOR_B)
        # cada producto: (glifos del factor de a, glifos del factor de b)
        prods = [(cuenta[2][0:1], cuenta[2][2:3]), (cuenta[4][0:1], cuenta[4][3:5]), (cuenta[6][0:1], cuenta[6][2:3])]
        resto = [[cuenta[2][1]], [cuenta[4][1], cuenta[4][2], cuenta[4][5]], [cuenta[6][1]]]   # puntos y paréntesis
        for fa, fb in prods:
            fa.set_color(COLOR_A); fb.set_color(COLOR_B)
        ea, eb = a.get_entries(), b.get_entries()
        marcos_par = [VGroup(marco(ea[k]), marco(eb[k])) for k in range(3)]
        marcos_fin = [VGroup(marco(ea[k]), marco(eb[k])) for k in range(3)]   # los de arriba se deforman al encadenarlos
        intro = MathTex(r"\Vect{a}\cdot\Vect{b}", tex_template=myTemplate, font_size=72).move_to([0, 0.3, 0])
        intro[0][0].set_color(COLOR_A); intro[0][2].set_color(COLOR_B)
        tres = [Tex(tr("3 componentes", "3 components"), font_size=30).set_color(COLOR_ESCALAR).next_to(v, DOWN, buff=0.3) for v in (a, b)]
        
        with self.voiceover(text=tr("""En este vídeo veremos una operación entre dos vectores cuyo resultado es un número: <bookmark mark='pp'/> el producto punto.""",
                                    """In this video we will look at an operation between two vectors whose result is a number: <bookmark mark='pp'/> the dot product.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
            self.wait_until_bookmark("pp")
            self.play(FadeIn(intro, scale=0.9), run_time=0.6)
        self.wait(0.8)   # respiro tras el arranque
        self.play(FadeOut(intro), run_time=0.4)
        
        with self.voiceover(text=tr("""Tomemos estos dos vectores. Para calcular <bookmark mark='pp'/> su producto punto, multiplicamos <bookmark mark='p1'/> las primeras componentes, <bookmark mark='p2'/> las segundas <bookmark mark='p3'/> y las terceras.""",
                                    """Take these two vectors. To compute <bookmark mark='pp'/> their dot product, we multiply <bookmark mark='p1'/> the first components, <bookmark mark='p2'/> the second ones <bookmark mark='p3'/> and the third ones.""")) as tracker:
            self.play(FadeIn(na), FadeIn(nb), run_time=1)
            self.wait_until_bookmark("pp")
            self.play(FadeIn(cuenta[0]), FadeIn(cuenta[1]), run_time=0.6)
            actual = None
            for k, marca in enumerate(["p1", "p2", "p3"]):
                self.wait_until_bookmark(marca)
                fa, fb = prods[k]
                self.play(FadeIn(marcos_par[k]) if actual is None else ReplacementTransform(actual, marcos_par[k]),
                          *([FadeIn(cuenta[2*k + 1])] if k else []), run_time=0.3)
                actual = marcos_par[k]
                self.play(TransformFromCopy(ea[k], fa), TransformFromCopy(eb[k], fb), *[FadeIn(g) for g in resto[k]], run_time=0.6)
            self.play(FadeOut(actual), run_time=0.3)
        
        with self.voiceover(text=tr("""Después sumamos los tres productos, <bookmark mark='s'/> y el resultado es <bookmark mark='r'/> cinco.""",
                                    """Then we add the three products, <bookmark mark='s'/> and the result is <bookmark mark='r'/> five.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(*[FadeIn(cuenta[k]) for k in range(7, 11)], run_time=0.6)
            self.wait_until_bookmark("r")
            self.play(FadeIn(cuenta[11]), FadeIn(cuenta[12]), run_time=0.5)
            resalta(self, [cuenta[12]], factor=1.3)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Cada componente de un vector se multiplica por la que ocupa la misma posición en el otro. <bookmark mark='m'/> Por eso los dos vectores han de tener el mismo número de componentes.""",
                                    """Each component of one vector is multiplied by the one in the same position in the other. <bookmark mark='m'/> That is why the two vectors must have the same number of components.""")) as tracker:
            apaga(self, [cuenta[12]], factor=1.3)
            self.play(*[Create(m) for m in marcos_fin], run_time=0.8)
            self.wait_until_bookmark("m")
            self.play(*[FadeIn(t, shift=0.1*UP) for t in tres], run_time=0.5)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in marcos_fin], *[FadeOut(t) for t in tres], run_time=0.4)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Definición", "Definition"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        deff = MathTex(*DEF, tex_template=myTemplate, font_size=44).move_to([0, 0.6, 0])
        deff[0][0].set_color(COLOR_A); deff[0][2].set_color(COLOR_B)
        for k in (2, 4, 8):
            deff[k][0:5].set_color(COLOR_A); deff[k][5:10].set_color(COLOR_B)
        ejemplo = MathTex(*EJ_AB, tex_template=myTemplate, font_size=40).set_color(GRAY_A).move_to([0, -1.6, 0])
        espacio = MathTex(r"\Vect{a},\,\Vect{b}\in\R[n]", tex_template=myTemplate, font_size=40).move_to([0, 1.75, 0])
        espacio[0][0].set_color(COLOR_A); espacio[0][2].set_color(COLOR_B)
        nota = Tex(tr(r"$\eleVRpE{a}{1}$: la primera componente de $\Vect{a}$", r"$\eleVRpE{a}{1}$: the first component of $\Vect{a}$"),
                   tex_template=myTemplate, font_size=30).set_color(COLOR_ESCALAR)
        
        with self.voiceover(text=tr("""En general, tomemos dos vectores <bookmark mark='v'/> con el mismo número de componentes. <bookmark mark='d'/> Su producto punto es la suma de los productos de las componentes que ocupan la misma posición.""",
                                    """In general, take two vectors <bookmark mark='v'/> with the same number of components. <bookmark mark='d'/> Their dot product is the sum of the products of the components in the same position.""")) as tracker:
            self.play(Write(cabecera), FadeIn(ejemplo), run_time=1)
            self.wait_until_bookmark("v")
            self.play(FadeIn(espacio), run_time=0.6)
            self.wait_until_bookmark("d")
            self.play(Write(deff), run_time=1.5)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Cada sumando multiplica dos de ellas: <bookmark mark='p1'/> las primeras, <bookmark mark='p2'/> las segundas, <bookmark mark='pn'/> y así hasta las últimas.""",
                                    """Each term multiplies two of them: <bookmark mark='p1'/> the first ones, <bookmark mark='p2'/> the second ones, <bookmark mark='pn'/> and so on up to the last ones.""")) as tracker:
            actual = None
            for k, marca in zip((2, 4, 8), ["p1", "p2", "pn"]):
                self.wait_until_bookmark(marca)
                nuevo = marco(deff[k])
                self.play(Create(nuevo) if actual is None else ReplacementTransform(actual, nuevo),
                          *([FadeIn(nota.next_to(deff[2], DOWN, buff=0.35))] if k == 2 else []), run_time=0.35)
                actual = nuevo
            self.wait(0.6)
            self.play(FadeOut(actual), FadeOut(nota), run_time=0.3)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""El resultado <bookmark mark='r'/> es un número, no un vector. <bookmark mark='p'/> Se escribe con un punto entre los dos vectores, y de ahí su nombre.""",
                                    """The result <bookmark mark='r'/> is a number, not a vector. <bookmark mark='p'/> It is written with a dot between the two vectors, hence its name.""")) as tracker:
            self.wait_until_bookmark("r")
            self.play(Create(marco(deff[0])), Indicate(ejemplo[12], color=COLOR_ESCALAR, scale_factor=1.5), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(*[FadeOut(m) for m in self.mobjects if isinstance(m, SurroundingRectangle)], run_time=0.2)
            resalta(self, [deff[0][1]], factor=1.8)
        self.wait(0.8)
        apaga(self, [deff[0][1]], factor=1.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Simetría", "Symmetry"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        ab = MathTex(*EJ_AB, tex_template=myTemplate, font_size=40).move_to([0, 1.3, 0])
        ba = MathTex(*EJ_BA, tex_template=myTemplate, font_size=40)
        ba.shift(ab[1].get_center() - ba[1].get_center() + 1.1*DOWN)   # los iguales, uno debajo del otro
        for c, (ca, cb) in ((ab, (COLOR_A, COLOR_B)), (ba, (COLOR_B, COLOR_A))):
            c[0][0].set_color(ca); c[0][2].set_color(cb)
        # colores por vector: en ab el primer factor es de a; en ba, el segundo
        for g in (ab[2][0], ab[4][0], ab[6][0], ba[2][2], ba[4][5], ba[6][2]):
            g.set_color(COLOR_A)
        for g in (ab[2][2], *ab[4][3:5], ab[6][2], ba[2][0], *ba[4][1:3], ba[6][0]):
            g.set_color(COLOR_B)
        # cada glifo de ab y su sitio en ba: los factores cambian de lado
        viajes = [(ab[0][0], ba[0][2]), (ab[0][1], ba[0][1]), (ab[0][2], ba[0][0]), (ab[1], ba[1]),
                  (ab[2][0], ba[2][2]), (ab[2][1], ba[2][1]), (ab[2][2], ba[2][0]), (ab[3], ba[3]),
                  (ab[4][0], ba[4][5]), (ab[4][1], ba[4][4]), (ab[4][2:6], ba[4][0:4]), (ab[5], ba[5]),
                  (ab[6][0], ba[6][2]), (ab[6][1], ba[6][1]), (ab[6][2], ba[6][0]),
                  *[(ab[k], ba[k]) for k in range(7, 13)]]
        panel = Panel(self)
        # el enunciado, en el hueco entre los dos lados del panel; la cadena debajo (como en V06 y V13)
        x_hueco = (panel.izq.get_right()[0] + panel.der.get_left()[0]) / 2
        enunciado = MathTex(r"\Vect{a}\cdot\Vect{b}=\Vect{b}\cdot\Vect{a}", tex_template=myTemplate, font_size=44).move_to([0, 1.75, 0])   # centrado, como la cadena (auditoría)
        for g, c in ((0, COLOR_A), (2, COLOR_B), (4, COLOR_B), (6, COLOR_A)):
            enunciado[0][g].set_color(c)
        cadena = [MathTex(c, tex_template=myTemplate, font_size=40) for c in CADENA]
        cadena[0].move_to([0, 0.45, 0])
        for k in (1, 2):
            cadena[k].next_to(cadena[k-1], DOWN, buff=0.5).align_to(cadena[0][0][3], LEFT)   # los iguales alineados
        # a en azul y b en naranja en las tres líneas (es lo que deja ver el cruce); el igual del paso con números
        # reales, en COLOR_REGLA
        for k, c in ((0, COLOR_A), (2, COLOR_B)):
            cadena[0][0][k].set_color(c)
        for ini, c in ((4, COLOR_A), (9, COLOR_B), (19, COLOR_A), (24, COLOR_B)):
            cadena[0][0][ini:ini+5].set_color(c)
        for ini, c in ((1, COLOR_B), (6, COLOR_A), (16, COLOR_B), (21, COLOR_A)):
            cadena[1][0][ini:ini+5].set_color(c)
        cadena[1][0][0].set_color(COLOR_REGLA)
        cadena[2][0][1].set_color(COLOR_B); cadena[2][0][3].set_color(COLOR_A)
        sumandos = [cadena[0][0][4:14], cadena[0][0][19:29]]
        
        with self.voiceover(text=tr("""Volvamos al ejemplo. <bookmark mark='c'/> Si intercambiamos los dos vectores, en cada producto los factores cambian de sitio, <bookmark mark='r'/> pero el resultado es el mismo.""",
                                    """Let us go back to the example. <bookmark mark='c'/> If we swap the two vectors, in each product the factors swap places, <bookmark mark='r'/> but the result is the same.""")) as tracker:
            self.play(Write(cabecera), FadeIn(ab), run_time=1)
            self.wait_until_bookmark("c")
            self.play(*[TransformFromCopy(x, y) for x, y in viajes], run_time=1.6)
            self.wait_until_bookmark("r")
            resalta(self, [ab[12], ba[12]], factor=1.4)
        self.wait(1.2)
        apaga(self, [ab[12], ba[12]], factor=1.4)
        
        with self.voiceover(text=tr("""Este ejemplo solo lo ilustra. <bookmark mark='e'/> Vamos a demostrar que ocurre con dos vectores cualesquiera.""",
                                    """This example only illustrates it. <bookmark mark='e'/> We are going to prove that it happens with any two vectors.""")) as tracker:
            self.wait_until_bookmark("e")
            self.play(FadeOut(ab), FadeOut(ba), FadeIn(enunciado), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Cuando el resultado no depende de cuál de los dos va primero, <bookmark mark='s'/> decimos que el producto es simétrico. <bookmark mark='p'/> Para demostrarlo contamos con la definición y con las propiedades de los números reales.""",
                                    """When the result does not depend on which of the two comes first, <bookmark mark='s'/> we say that the product is symmetric. <bookmark mark='p'/> To prove it we can use the definition and the properties of real numbers.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(Indicate(enunciado, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.0)
            self.wait_until_bookmark("p")
            self.play(FadeIn(panel.todo), run_time=1)
        self.wait(0.8)
        
        self.pausa_para_pensar(invitacion=tr(r"Demuestre que $\Vect{a}\cdot\Vect{b}=\Vect{b}\cdot\Vect{a}$.",
                                             r"Prove that $\Vect{a}\cdot\Vect{b}=\Vect{b}\cdot\Vect{a}$."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que el producto punto es simétrico.",
                                                 "Pause the video and try to prove that the dot product is symmetric."),
                               pista=tr("la definición y la propiedad conmutativa del producto de números.",
                                        "the definition and the commutative property of multiplication."),
                               pista_voz=tr("use la definición y la propiedad conmutativa del producto de números.",
                                            "use the definition and the commutative property of multiplication."),
                               al_dar_la_pista=lambda: panel.pista("def", "conm"))
        panel.quita_pista()
        
        with self.voiceover(text=tr("""Por la definición <bookmark mark='l0'/> podemos escribir el producto punto como una suma de productos de números.""",
                                    """By the definition <bookmark mark='l0'/> we can write the dot product as a sum of products of numbers.""")) as tracker:
            # la primera línea baja del panel: es la definición misma
            self.play(panel.senala("def"), run_time=0.8)
            self.wait_until_bookmark("l0")
            self.play(TransformFromCopy(panel.piezas["def"], cadena[0]), run_time=1.2)
            panel.cuenta("def")
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Cada sumando <bookmark mark='s'/> es un producto de dos números, así que <bookmark mark='k'/> por la conmutativa <bookmark mark='l1'/> podemos intercambiar sus factores.""",
                                    """Each term <bookmark mark='s'/> is a product of two numbers, so <bookmark mark='k'/> by the commutative property <bookmark mark='l1'/> we can swap its factors.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(*[Indicate(g, color=COLOR_REGLA, scale_factor=1.15) for g in sumandos], run_time=0.9)
            self.wait_until_bookmark("k")   # la pieza parpadea y la línea empieza cuando la voz nombra la regla
            # glifos: L0 = a · b = 0-3; (a|1) 4-8; (b|1) 9-13; + 14; ⋯ 15-17; + 18; (a|n) 19-23; (b|n) 24-28
            #         L1 = 0; (b|1) 1-5; (a|1) 6-10; + 11; ⋯ 12-14; + 15; (b|n) 16-20; (a|n) 21-25
            # mientras la voz nombra la regla se copia lo que no cambia; en «cambiar el orden» los factores se cruzan
            nace(self, cadena[0][0], cadena[1][0], [(14, 11), (15, 12), (16, 13), (17, 14), (18, 15)],
                 [*[(4 + t, 6 + t) for t in range(5)], *[(9 + t, 1 + t) for t in range(5)],
                  *[(19 + t, 21 + t) for t in range(5)], *[(24 + t, 16 + t) for t in range(5)]],
                 marca="l1", extra=[panel.senala("conm")], t_moviles=1.2)
            entera(self, cadena[1])
            panel.cuenta("conm")
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Y por la definición <bookmark mark='l2'/> podemos escribir esta suma como el producto punto de b por a.""",
                                    """And by the definition <bookmark mark='l2'/> we can write this sum as the dot product of b and 'a'.""")) as tracker:
            # en sentido contrario al primer paso: las componentes de b se reúnen en b y las de a en a; lo demás
            # (paréntesis, selectores, sumas) no aparece. L2 = «= b · a» (0-3)
            nace(self, cadena[1][0], cadena[2][0], [], [(2, 1), (17, 1), (7, 3), (22, 3)], aparecen=[2],
                 marca="l2", extra=[panel.senala("def")], t_moviles=1.2)
            entera(self, cadena[2])
            panel.cuenta("def")
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Hemos usado <bookmark mark='d'/> dos veces la definición <bookmark mark='c'/> y una vez la propiedad conmutativa del producto de números. <bookmark mark='s'/> Así pues, el producto punto es simétrico.""",
                                    """We have used <bookmark mark='d'/> the definition twice <bookmark mark='c'/> and the commutative property of multiplication once. <bookmark mark='s'/> So the dot product is symmetric.""")) as tracker:
            self.wait_until_bookmark("d")
            self.play(*panel.parpadea("def"), run_time=0.9)
            self.wait_until_bookmark("c")
            self.play(*panel.parpadea("conm"), run_time=0.9)
            self.wait_until_bookmark("s")
            self.play(Indicate(cadena[0][0][0:3], color=COLOR_ESCALAR), Indicate(cadena[2][0][1:4], color=COLOR_ESCALAR),
                      Indicate(enunciado, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.4)
        self.wait(1.0)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Un vector por sí mismo", "A vector times itself"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        b = vector_col(B_EJ, COLOR_B)
        nb = con_nombre(r"\Vect{b}=", b); nb[0].set_color(COLOR_B)
        nb.move_to([0, 1.45, 0])
        cuenta = MathTex(*EJ_BB, tex_template=myTemplate, font_size=44).move_to([0, -0.3, 0])
        cuenta[0][0].set_color(COLOR_B); cuenta[0][2].set_color(COLOR_B)
        for p_, (f1, f2) in zip((2, 4, 6), ((slice(0, 1), slice(2, 3)), (slice(0, 4), slice(5, 9)), (slice(0, 1), slice(2, 3)))):
            cuenta[p_][f1].set_color(COLOR_B); cuenta[p_][f2].set_color(COLOR_B)
        cuadrados = [cuenta[8], cuenta[9][1], cuenta[10][1]]
        eb = b.get_entries()
        # la suma general de cuadrados: x·x = (x|1)(x|1) + ⋯ + (x|n)(x|n) ≥ 0 (glifos: x · x = 0-3; (x|1)(x|1) 4-13; + 14;
        # ⋯ 15-17; + 18; (x|n)(x|n) 19-28; ≥ 29; 0 30)
        general = MathTex(r"\Vect{x}\cdot\Vect{x}=\eleVRpE{x}{1}\eleVRpE{x}{1}+\cdots+\eleVRpE{x}{n}\eleVRpE{x}{n}\geq 0",
                          tex_template=myTemplate, font_size=44).move_to([0, -1.55, 0])
        sumandos_x = [general[0][4:14], general[0][19:29]]
        componentes_x = [general[0][4:9], general[0][9:14], general[0][19:24], general[0][24:29]]
        cero = MathTex(r"\Vect{x}\cdot\Vect{x}=0\ \Leftrightarrow\ \Vect{x}=\Vect{0}", tex_template=myTemplate, font_size=44).move_to([0, -2.75, 0])
        
        with self.voiceover(text=tr("""Multipliquemos ahora este vector por sí mismo. <bookmark mark='c'/> Cada sumando es el cuadrado de una componente, <bookmark mark='r'/> y el resultado es seis.""",
                                    """Now let us multiply this vector by itself. <bookmark mark='c'/> Each term is the square of a component, <bookmark mark='r'/> and the result is six.""")) as tracker:
            self.play(Write(cabecera), FadeIn(nb), run_time=1)
            self.play(FadeIn(cuenta[0]), FadeIn(cuenta[1]), run_time=0.5)
            self.wait_until_bookmark("c")
            for k, (p_, f1, f2, pt) in enumerate(((2, slice(0, 1), slice(2, 3), [1]), (4, slice(0, 4), slice(5, 9), [4]),
                                                  (6, slice(0, 1), slice(2, 3), [1]))):
                self.play(TransformFromCopy(eb[k], cuenta[p_][f1]), TransformFromCopy(eb[k], cuenta[p_][f2]),
                          *[FadeIn(cuenta[p_][q]) for q in pt], *([FadeIn(cuenta[p_ - 1])] if k else []), run_time=0.45)
            self.play(*[FadeIn(cuenta[k]) for k in range(7, 11)], run_time=0.5)
            self.wait_until_bookmark("r")
            self.play(FadeIn(cuenta[11]), FadeIn(cuenta[12]), run_time=0.5)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Los cuadrados <bookmark mark='q'/> nunca son negativos, <bookmark mark='n'/> aunque el número lo sea.""",
                                    """Squares <bookmark mark='q'/> are never negative, <bookmark mark='n'/> even when the number is.""")) as tracker:
            self.wait_until_bookmark("q")
            resalta(self, cuadrados, factor=1.3)
            self.wait_until_bookmark("n")
            resalta(self, [cuenta[4][0:4], cuenta[4][5:9], eb[1]], factor=1.15)
        self.wait(0.8)
        apaga(self, [cuenta[4][0:4], cuenta[4][5:9]], color=COLOR_B, factor=1.15)
        self.play(eb[1].animate.set_color(COLOR_B).scale(1/1.15), *[x.animate.set_color(WHITE).scale(1/1.3) for x in cuadrados], run_time=0.3)
        
        with self.voiceover(text=tr("""Por tanto, <bookmark mark='g'/> el producto punto de cualquier vector por sí mismo tampoco es negativo.""",
                                    """Therefore, <bookmark mark='g'/> the dot product of any vector with itself is not negative either.""")) as tracker:
            self.wait_until_bookmark("g")
            self.play(Write(general), run_time=1.5)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Además, una suma de números que no son negativos <bookmark mark='s'/> solo es cero si todos ellos son cero, <bookmark mark='u'/> y un cuadrado solo es cero si lo es el número. <bookmark mark='z'/> Por eso, el producto punto de un vector por sí mismo solo es cero cuando el vector es nulo.""",
                                    """Moreover, a sum of numbers that are not negative <bookmark mark='s'/> is zero only if all of them are zero, <bookmark mark='u'/> and a square is zero only if the number is. <bookmark mark='z'/> That is why the dot product of a vector with itself is zero only when the vector is the zero vector.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(*[Indicate(g, color=COLOR_ESCALAR, scale_factor=1.12) for g in sumandos_x], run_time=1.0)
            self.wait_until_bookmark("u")
            self.play(*[Indicate(g, color=COLOR_ESCALAR, scale_factor=1.15) for g in componentes_x], run_time=1.0)
            self.wait_until_bookmark("z")
            self.play(FadeIn(cero), run_time=0.8)
        self.wait(1.0)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Las columnas de la identidad", "The columns of the identity"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        I3 = matriz([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        nI = con_nombre(r"\Mat{I}=", I3)
        col = vector_col([0, 1, 0], COLOR_COLUMNA)
        ncol = con_nombre(r"\VectC{I}{2}=", col)
        a = vector_col(A_EJ, COLOR_A)
        na = con_nombre(r"\Vect{a}=", a); na[0].set_color(COLOR_A)
        VGroup(na, nI, ncol).arrange(RIGHT, buff=1.0).move_to([0, 1.0, 0])   # en el orden de la cuenta: a, después I y su columna
        franja = franja_columna(I3, 1)
        cuenta = MathTex(*EJ_ID, tex_template=myTemplate, font_size=44).move_to([0, -1.2, 0])
        cuenta[0][0].set_color(COLOR_A); cuenta[0][2:7].set_color(COLOR_COLUMNA)
        for k in (2, 4, 6):
            cuenta[k][0].set_color(COLOR_A); cuenta[k][2].set_color(COLOR_COLUMNA)
        ea, ec = a.get_entries(), col.get_entries()
        # a·(I|i) = a|i = (I|i)·a (glifos: a 0; · 1; (I|i) 2-6; = 7; a|i 8-10; = 11; (I|i) 12-16; · 17; a 18). Primero se ve
        # la parte 0-10 en su sitio; al decir «a la izquierda» nace el resto con los factores cruzándose (como en la escena 3)
        ambos = MathTex(r"\Vect{a}\cdot\VectCpE{I}{i}=\eleVR{a}{i}=\VectCpE{I}{i}\cdot\Vect{a}", tex_template=myTemplate,
                        font_size=48).move_to([0, -2.6, 0])
        for g in (0, 8, 18):
            ambos[0][g].set_color(COLOR_A)
        ambos[0][2:7].set_color(COLOR_COLUMNA); ambos[0][12:17].set_color(COLOR_COLUMNA)
        general = ambos[0][0:11]
        
        with self.voiceover(text=tr("""Este vector tiene tres componentes. <bookmark mark='i'/> Tomemos la matriz identidad de orden tres. <bookmark mark='c'/> Su segunda columna <bookmark mark='v'/> tiene un uno en la segunda posición y ceros en las demás.""",
                                    """This vector has three components. <bookmark mark='i'/> Take the identity matrix of order three. <bookmark mark='c'/> Its second column <bookmark mark='v'/> has a one in the second position and zeros elsewhere.""")) as tracker:
            self.play(Write(cabecera), FadeIn(na), run_time=1)
            self.wait_until_bookmark("i")
            self.play(FadeIn(nI), run_time=0.6)
            self.wait_until_bookmark("c")
            self.play(FadeIn(franja), run_time=0.4)
            self.wait_until_bookmark("v")
            self.play(FadeIn(ncol[0]), FadeIn(col.get_brackets()),
                      *[TransformFromCopy(I3.get_columns()[1][k], ec[k]) for k in range(3)], run_time=0.9)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Multipliquemos este vector por esa columna. <bookmark mark='z'/> Los ceros anulan la primera y la tercera componente, <bookmark mark='u'/> y el uno deja pasar la segunda. <bookmark mark='r'/> El resultado es la segunda componente del vector.""",
                                    """Let us multiply this vector by that column. <bookmark mark='z'/> The zeros cancel out the first and the third component, <bookmark mark='u'/> and the one lets the second one through. <bookmark mark='r'/> The result is the second component of the vector.""")) as tracker:
            self.play(FadeOut(franja), FadeIn(cuenta[0]), FadeIn(cuenta[1]), run_time=0.4)
            for k, p in zip(range(3), (2, 4, 6)):
                self.play(TransformFromCopy(ea[k], cuenta[p][0]), TransformFromCopy(ec[k], cuenta[p][2]), FadeIn(cuenta[p][1]),
                          *([FadeIn(cuenta[p - 1])] if k else []), run_time=0.4)
            self.wait_until_bookmark("z")
            self.play(cuenta[2].animate.set_opacity(0.3), cuenta[6].animate.set_opacity(0.3),
                      ea[0].animate.set_opacity(0.3), ea[2].animate.set_opacity(0.3), run_time=0.4)
            self.wait_until_bookmark("u")
            resalta(self, [cuenta[4]], factor=1.12)
            self.wait_until_bookmark("r")
            self.play(FadeIn(cuenta[7]), TransformFromCopy(ea[1], cuenta[8]), run_time=0.7)
            resalta(self, [ea[1], cuenta[8]], factor=1.3)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""El mismo argumento vale para cualquier columna y cualquier vector: la columna i-ésima de la identidad tiene un uno en la posición i-ésima y ceros en las demás. <bookmark mark='g'/> Así que el producto punto por ella selecciona la componente i-ésima.""",
                                    """The same argument works for any column and any vector: the i-th column of the identity has a one in the i-th position and zeros elsewhere. <bookmark mark='g'/> So the dot product with it selects the i-th component.""")) as tracker:
            self.play(ea[0].animate.set_opacity(1), ea[2].animate.set_opacity(1), run_time=0.5)
            self.wait_until_bookmark("g")
            self.play(FadeIn(general), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Como el producto punto es simétrico, da igual que la columna esté <bookmark mark='d'/> a la derecha <bookmark mark='i'/> o a la izquierda.""",
                                    """Since the dot product is symmetric, it does not matter whether the column is <bookmark mark='d'/> on the right <bookmark mark='i'/> or on the left.""")) as tracker:
            self.wait_until_bookmark("d")
            self.play(Indicate(ambos[0][2:7], color=COLOR_ESCALAR, scale_factor=1.2), run_time=0.8)
            self.wait_until_bookmark("i")
            self.play(FadeIn(ambos[0][11]), TransformFromCopy(ambos[0][2:7], ambos[0][12:17]),
                      TransformFromCopy(ambos[0][1], ambos[0][17]), TransformFromCopy(ambos[0][0], ambos[0][18]), run_time=1.2)
            self.remove(*ambos[0]); self.add(ambos)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Así pues, seleccionar una componente de un vector es lo mismo que multiplicarlo por una columna de la identidad.""",
                                    """So selecting a component of a vector is the same as multiplying it by a column of the identity.""")) as tracker:
            self.play(Indicate(ambos, color=COLOR_ESCALAR, scale_factor=1.08), run_time=1.5)
        self.wait(1.0)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [DEF, [r"\Vect{a}\cdot\Vect{b}=\Vect{b}\cdot\Vect{a}"],
                    [r"\Vect{x}\cdot\Vect{x}\geq 0,\qquad \Vect{x}\cdot\Vect{x}=0\ \Leftrightarrow\ \Vect{x}=\Vect{0}"],
                    [r"\Vect{a}\cdot\VectCpE{I}{i}=\eleVR{a}{i}"]]
        rotulos = [tr("suma de productos, posición a posición (un número)", "sum of products, position by position (a number)"),
                   tr("simétrico", "symmetric"),
                   tr("nunca negativo; cero solo para el vector nulo", "never negative; zero only for the zero vector"),
                   tr("la columna i-ésima de I selecciona la componente i-ésima", "the i-th column of I selects the i-th component")]
        filas = VGroup(*[VGroup(MathTex(*f, tex_template=myTemplate, font_size=42), Tex(r, tex_template=myTemplate, font_size=32, color=GRAY_A)).arrange(DOWN, buff=0.15)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.3).next_to(cabecera, DOWN, buff=0.35)
        
        with self.voiceover(text=tr("""Resumamos. El producto punto de dos vectores multiplica las componentes que ocupan la misma posición y suma los productos. Da un número. <bookmark mark='s'/> Además, es simétrico: da igual cuál de los dos vectores va primero.""",
                                    """Let us sum up. The dot product of two vectors multiplies the components in the same position and adds the products. It gives a number. <bookmark mark='s'/> Moreover, it is symmetric: it does not matter which of the two vectors comes first.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(filas[1]), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""El producto punto de un vector por sí mismo nunca es negativo, y solo es cero para el vector nulo. <bookmark mark='i'/> Y multiplicar por una columna de la identidad selecciona una componente.""",
                                    """The dot product of a vector with itself is never negative, and it is zero only for the zero vector. <bookmark mark='i'/> And multiplying by a column of the identity selects a component.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.8)
            self.wait_until_bookmark("i")
            self.play(FadeIn(filas[3]), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos las propiedades del producto punto con la suma de vectores y con el producto por un escalar.""",
                                    """In the next video we will see the properties of the dot product with vector addition and with scalar multiplication.""")) as tracker:
            pass
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos_finales()


class L02_V01_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

class L02_V01_E01_Ejemplo(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        a, b = vector_col(A_EJ, COLOR_A), vector_col(B_EJ, COLOR_B)
        na, nb = con_nombre(r"\Vect{a}=", a), con_nombre(r"\Vect{b}=", b)
        na[0].set_color(COLOR_A); nb[0].set_color(COLOR_B)
        VGroup(na, nb).arrange(RIGHT, buff=2.2).move_to([0, 0.9, 0])
        cuenta = MathTex(*EJ_AB, tex_template=myTemplate, font_size=46).move_to([0, -1.7, 0])
        cuenta[0][0].set_color(COLOR_A); cuenta[0][2].set_color(COLOR_B)
        # cada producto: (glifos del factor de a, glifos del factor de b)
        prods = [(cuenta[2][0:1], cuenta[2][2:3]), (cuenta[4][0:1], cuenta[4][3:5]), (cuenta[6][0:1], cuenta[6][2:3])]
        resto = [[cuenta[2][1]], [cuenta[4][1], cuenta[4][2], cuenta[4][5]], [cuenta[6][1]]]   # puntos y paréntesis
        for fa, fb in prods:
            fa.set_color(COLOR_A); fb.set_color(COLOR_B)
        ea, eb = a.get_entries(), b.get_entries()
        marcos_par = [VGroup(marco(ea[k]), marco(eb[k])) for k in range(3)]
        marcos_fin = [VGroup(marco(ea[k]), marco(eb[k])) for k in range(3)]   # los de arriba se deforman al encadenarlos
        intro = MathTex(r"\Vect{a}\cdot\Vect{b}", tex_template=myTemplate, font_size=72).move_to([0, 0.3, 0])
        intro[0][0].set_color(COLOR_A); intro[0][2].set_color(COLOR_B)
        tres = [Tex(tr("3 componentes", "3 components"), font_size=30).set_color(COLOR_ESCALAR).next_to(v, DOWN, buff=0.3) for v in (a, b)]
        
        with self.voiceover(text=tr("""En este vídeo veremos una operación entre dos vectores cuyo resultado es un número: <bookmark mark='pp'/> el producto punto.""",
                                    """In this video we will look at an operation between two vectors whose result is a number: <bookmark mark='pp'/> the dot product.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
            self.wait_until_bookmark("pp")
            self.play(FadeIn(intro, scale=0.9), run_time=0.6)
        self.wait(0.8)   # respiro tras el arranque
        self.play(FadeOut(intro), run_time=0.4)
        
        with self.voiceover(text=tr("""Tomemos estos dos vectores. Para calcular <bookmark mark='pp'/> su producto punto, multiplicamos <bookmark mark='p1'/> las primeras componentes, <bookmark mark='p2'/> las segundas <bookmark mark='p3'/> y las terceras.""",
                                    """Take these two vectors. To compute <bookmark mark='pp'/> their dot product, we multiply <bookmark mark='p1'/> the first components, <bookmark mark='p2'/> the second ones <bookmark mark='p3'/> and the third ones.""")) as tracker:
            self.play(FadeIn(na), FadeIn(nb), run_time=1)
            self.wait_until_bookmark("pp")
            self.play(FadeIn(cuenta[0]), FadeIn(cuenta[1]), run_time=0.6)
            actual = None
            for k, marca in enumerate(["p1", "p2", "p3"]):
                self.wait_until_bookmark(marca)
                fa, fb = prods[k]
                self.play(FadeIn(marcos_par[k]) if actual is None else ReplacementTransform(actual, marcos_par[k]),
                          *([FadeIn(cuenta[2*k + 1])] if k else []), run_time=0.3)
                actual = marcos_par[k]
                self.play(TransformFromCopy(ea[k], fa), TransformFromCopy(eb[k], fb), *[FadeIn(g) for g in resto[k]], run_time=0.6)
            self.play(FadeOut(actual), run_time=0.3)
        
        with self.voiceover(text=tr("""Después sumamos los tres productos, <bookmark mark='s'/> y el resultado es <bookmark mark='r'/> cinco.""",
                                    """Then we add the three products, <bookmark mark='s'/> and the result is <bookmark mark='r'/> five.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(*[FadeIn(cuenta[k]) for k in range(7, 11)], run_time=0.6)
            self.wait_until_bookmark("r")
            self.play(FadeIn(cuenta[11]), FadeIn(cuenta[12]), run_time=0.5)
            resalta(self, [cuenta[12]], factor=1.3)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Cada componente de un vector se multiplica por la que ocupa la misma posición en el otro. <bookmark mark='m'/> Por eso los dos vectores han de tener el mismo número de componentes.""",
                                    """Each component of one vector is multiplied by the one in the same position in the other. <bookmark mark='m'/> That is why the two vectors must have the same number of components.""")) as tracker:
            apaga(self, [cuenta[12]], factor=1.3)
            self.play(*[Create(m) for m in marcos_fin], run_time=0.8)
            self.wait_until_bookmark("m")
            self.play(*[FadeIn(t, shift=0.1*UP) for t in tres], run_time=0.5)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in marcos_fin], *[FadeOut(t) for t in tres], run_time=0.4)
        
        self.pausa_media()

class L02_V01_E02_Definicion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Definición", "Definition"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        deff = MathTex(*DEF, tex_template=myTemplate, font_size=44).move_to([0, 0.6, 0])
        deff[0][0].set_color(COLOR_A); deff[0][2].set_color(COLOR_B)
        for k in (2, 4, 8):
            deff[k][0:5].set_color(COLOR_A); deff[k][5:10].set_color(COLOR_B)
        ejemplo = MathTex(*EJ_AB, tex_template=myTemplate, font_size=40).set_color(GRAY_A).move_to([0, -1.6, 0])
        espacio = MathTex(r"\Vect{a},\,\Vect{b}\in\R[n]", tex_template=myTemplate, font_size=40).move_to([0, 1.75, 0])
        espacio[0][0].set_color(COLOR_A); espacio[0][2].set_color(COLOR_B)
        nota = Tex(tr(r"$\eleVRpE{a}{1}$: la primera componente de $\Vect{a}$", r"$\eleVRpE{a}{1}$: the first component of $\Vect{a}$"),
                   tex_template=myTemplate, font_size=30).set_color(COLOR_ESCALAR)
        
        with self.voiceover(text=tr("""En general, tomemos dos vectores <bookmark mark='v'/> con el mismo número de componentes. <bookmark mark='d'/> Su producto punto es la suma de los productos de las componentes que ocupan la misma posición.""",
                                    """In general, take two vectors <bookmark mark='v'/> with the same number of components. <bookmark mark='d'/> Their dot product is the sum of the products of the components in the same position.""")) as tracker:
            self.play(Write(cabecera), FadeIn(ejemplo), run_time=1)
            self.wait_until_bookmark("v")
            self.play(FadeIn(espacio), run_time=0.6)
            self.wait_until_bookmark("d")
            self.play(Write(deff), run_time=1.5)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Cada sumando multiplica dos de ellas: <bookmark mark='p1'/> las primeras, <bookmark mark='p2'/> las segundas, <bookmark mark='pn'/> y así hasta las últimas.""",
                                    """Each term multiplies two of them: <bookmark mark='p1'/> the first ones, <bookmark mark='p2'/> the second ones, <bookmark mark='pn'/> and so on up to the last ones.""")) as tracker:
            actual = None
            for k, marca in zip((2, 4, 8), ["p1", "p2", "pn"]):
                self.wait_until_bookmark(marca)
                nuevo = marco(deff[k])
                self.play(Create(nuevo) if actual is None else ReplacementTransform(actual, nuevo),
                          *([FadeIn(nota.next_to(deff[2], DOWN, buff=0.35))] if k == 2 else []), run_time=0.35)
                actual = nuevo
            self.wait(0.6)
            self.play(FadeOut(actual), FadeOut(nota), run_time=0.3)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""El resultado <bookmark mark='r'/> es un número, no un vector. <bookmark mark='p'/> Se escribe con un punto entre los dos vectores, y de ahí su nombre.""",
                                    """The result <bookmark mark='r'/> is a number, not a vector. <bookmark mark='p'/> It is written with a dot between the two vectors, hence its name.""")) as tracker:
            self.wait_until_bookmark("r")
            self.play(Create(marco(deff[0])), Indicate(ejemplo[12], color=COLOR_ESCALAR, scale_factor=1.5), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(*[FadeOut(m) for m in self.mobjects if isinstance(m, SurroundingRectangle)], run_time=0.2)
            resalta(self, [deff[0][1]], factor=1.8)
        self.wait(0.8)
        apaga(self, [deff[0][1]], factor=1.8)
        
        self.pausa_media()

class L02_V01_E03_Simetria(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Simetría", "Symmetry"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        ab = MathTex(*EJ_AB, tex_template=myTemplate, font_size=40).move_to([0, 1.3, 0])
        ba = MathTex(*EJ_BA, tex_template=myTemplate, font_size=40)
        ba.shift(ab[1].get_center() - ba[1].get_center() + 1.1*DOWN)   # los iguales, uno debajo del otro
        for c, (ca, cb) in ((ab, (COLOR_A, COLOR_B)), (ba, (COLOR_B, COLOR_A))):
            c[0][0].set_color(ca); c[0][2].set_color(cb)
        # colores por vector: en ab el primer factor es de a; en ba, el segundo
        for g in (ab[2][0], ab[4][0], ab[6][0], ba[2][2], ba[4][5], ba[6][2]):
            g.set_color(COLOR_A)
        for g in (ab[2][2], *ab[4][3:5], ab[6][2], ba[2][0], *ba[4][1:3], ba[6][0]):
            g.set_color(COLOR_B)
        # cada glifo de ab y su sitio en ba: los factores cambian de lado
        viajes = [(ab[0][0], ba[0][2]), (ab[0][1], ba[0][1]), (ab[0][2], ba[0][0]), (ab[1], ba[1]),
                  (ab[2][0], ba[2][2]), (ab[2][1], ba[2][1]), (ab[2][2], ba[2][0]), (ab[3], ba[3]),
                  (ab[4][0], ba[4][5]), (ab[4][1], ba[4][4]), (ab[4][2:6], ba[4][0:4]), (ab[5], ba[5]),
                  (ab[6][0], ba[6][2]), (ab[6][1], ba[6][1]), (ab[6][2], ba[6][0]),
                  *[(ab[k], ba[k]) for k in range(7, 13)]]
        panel = Panel(self)
        # el enunciado, en el hueco entre los dos lados del panel; la cadena debajo (como en V06 y V13)
        x_hueco = (panel.izq.get_right()[0] + panel.der.get_left()[0]) / 2
        enunciado = MathTex(r"\Vect{a}\cdot\Vect{b}=\Vect{b}\cdot\Vect{a}", tex_template=myTemplate, font_size=44).move_to([0, 1.75, 0])   # centrado, como la cadena (auditoría)
        for g, c in ((0, COLOR_A), (2, COLOR_B), (4, COLOR_B), (6, COLOR_A)):
            enunciado[0][g].set_color(c)
        cadena = [MathTex(c, tex_template=myTemplate, font_size=40) for c in CADENA]
        cadena[0].move_to([0, 0.45, 0])
        for k in (1, 2):
            cadena[k].next_to(cadena[k-1], DOWN, buff=0.5).align_to(cadena[0][0][3], LEFT)   # los iguales alineados
        # a en azul y b en naranja en las tres líneas (es lo que deja ver el cruce); el igual del paso con números
        # reales, en COLOR_REGLA
        for k, c in ((0, COLOR_A), (2, COLOR_B)):
            cadena[0][0][k].set_color(c)
        for ini, c in ((4, COLOR_A), (9, COLOR_B), (19, COLOR_A), (24, COLOR_B)):
            cadena[0][0][ini:ini+5].set_color(c)
        for ini, c in ((1, COLOR_B), (6, COLOR_A), (16, COLOR_B), (21, COLOR_A)):
            cadena[1][0][ini:ini+5].set_color(c)
        cadena[1][0][0].set_color(COLOR_REGLA)
        cadena[2][0][1].set_color(COLOR_B); cadena[2][0][3].set_color(COLOR_A)
        sumandos = [cadena[0][0][4:14], cadena[0][0][19:29]]
        
        with self.voiceover(text=tr("""Volvamos al ejemplo. <bookmark mark='c'/> Si intercambiamos los dos vectores, en cada producto los factores cambian de sitio, <bookmark mark='r'/> pero el resultado es el mismo.""",
                                    """Let us go back to the example. <bookmark mark='c'/> If we swap the two vectors, in each product the factors swap places, <bookmark mark='r'/> but the result is the same.""")) as tracker:
            self.play(Write(cabecera), FadeIn(ab), run_time=1)
            self.wait_until_bookmark("c")
            self.play(*[TransformFromCopy(x, y) for x, y in viajes], run_time=1.6)
            self.wait_until_bookmark("r")
            resalta(self, [ab[12], ba[12]], factor=1.4)
        self.wait(1.2)
        apaga(self, [ab[12], ba[12]], factor=1.4)
        
        with self.voiceover(text=tr("""Este ejemplo solo lo ilustra. <bookmark mark='e'/> Vamos a demostrar que ocurre con dos vectores cualesquiera.""",
                                    """This example only illustrates it. <bookmark mark='e'/> We are going to prove that it happens with any two vectors.""")) as tracker:
            self.wait_until_bookmark("e")
            self.play(FadeOut(ab), FadeOut(ba), FadeIn(enunciado), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Cuando el resultado no depende de cuál de los dos va primero, <bookmark mark='s'/> decimos que el producto es simétrico. <bookmark mark='p'/> Para demostrarlo contamos con la definición y con las propiedades de los números reales.""",
                                    """When the result does not depend on which of the two comes first, <bookmark mark='s'/> we say that the product is symmetric. <bookmark mark='p'/> To prove it we can use the definition and the properties of real numbers.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(Indicate(enunciado, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.0)
            self.wait_until_bookmark("p")
            self.play(FadeIn(panel.todo), run_time=1)
        self.wait(0.8)
        
        self.pausa_para_pensar(invitacion=tr(r"Demuestre que $\Vect{a}\cdot\Vect{b}=\Vect{b}\cdot\Vect{a}$.",
                                             r"Prove that $\Vect{a}\cdot\Vect{b}=\Vect{b}\cdot\Vect{a}$."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que el producto punto es simétrico.",
                                                 "Pause the video and try to prove that the dot product is symmetric."),
                               pista=tr("la definición y la propiedad conmutativa del producto de números.",
                                        "the definition and the commutative property of multiplication."),
                               pista_voz=tr("use la definición y la propiedad conmutativa del producto de números.",
                                            "use the definition and the commutative property of multiplication."),
                               al_dar_la_pista=lambda: panel.pista("def", "conm"))
        panel.quita_pista()
        
        with self.voiceover(text=tr("""Por la definición <bookmark mark='l0'/> podemos escribir el producto punto como una suma de productos de números.""",
                                    """By the definition <bookmark mark='l0'/> we can write the dot product as a sum of products of numbers.""")) as tracker:
            # la primera línea baja del panel: es la definición misma
            self.play(panel.senala("def"), run_time=0.8)
            self.wait_until_bookmark("l0")
            self.play(TransformFromCopy(panel.piezas["def"], cadena[0]), run_time=1.2)
            panel.cuenta("def")
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Cada sumando <bookmark mark='s'/> es un producto de dos números, así que <bookmark mark='k'/> por la conmutativa <bookmark mark='l1'/> podemos intercambiar sus factores.""",
                                    """Each term <bookmark mark='s'/> is a product of two numbers, so <bookmark mark='k'/> by the commutative property <bookmark mark='l1'/> we can swap its factors.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(*[Indicate(g, color=COLOR_REGLA, scale_factor=1.15) for g in sumandos], run_time=0.9)
            self.wait_until_bookmark("k")   # la pieza parpadea y la línea empieza cuando la voz nombra la regla
            # glifos: L0 = a · b = 0-3; (a|1) 4-8; (b|1) 9-13; + 14; ⋯ 15-17; + 18; (a|n) 19-23; (b|n) 24-28
            #         L1 = 0; (b|1) 1-5; (a|1) 6-10; + 11; ⋯ 12-14; + 15; (b|n) 16-20; (a|n) 21-25
            # mientras la voz nombra la regla se copia lo que no cambia; en «cambiar el orden» los factores se cruzan
            nace(self, cadena[0][0], cadena[1][0], [(14, 11), (15, 12), (16, 13), (17, 14), (18, 15)],
                 [*[(4 + t, 6 + t) for t in range(5)], *[(9 + t, 1 + t) for t in range(5)],
                  *[(19 + t, 21 + t) for t in range(5)], *[(24 + t, 16 + t) for t in range(5)]],
                 marca="l1", extra=[panel.senala("conm")], t_moviles=1.2)
            entera(self, cadena[1])
            panel.cuenta("conm")
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Y por la definición <bookmark mark='l2'/> podemos escribir esta suma como el producto punto de b por a.""",
                                    """And by the definition <bookmark mark='l2'/> we can write this sum as the dot product of b and 'a'.""")) as tracker:
            # en sentido contrario al primer paso: las componentes de b se reúnen en b y las de a en a; lo demás
            # (paréntesis, selectores, sumas) no aparece. L2 = «= b · a» (0-3)
            nace(self, cadena[1][0], cadena[2][0], [], [(2, 1), (17, 1), (7, 3), (22, 3)], aparecen=[2],
                 marca="l2", extra=[panel.senala("def")], t_moviles=1.2)
            entera(self, cadena[2])
            panel.cuenta("def")
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Hemos usado <bookmark mark='d'/> dos veces la definición <bookmark mark='c'/> y una vez la propiedad conmutativa del producto de números. <bookmark mark='s'/> Así pues, el producto punto es simétrico.""",
                                    """We have used <bookmark mark='d'/> the definition twice <bookmark mark='c'/> and the commutative property of multiplication once. <bookmark mark='s'/> So the dot product is symmetric.""")) as tracker:
            self.wait_until_bookmark("d")
            self.play(*panel.parpadea("def"), run_time=0.9)
            self.wait_until_bookmark("c")
            self.play(*panel.parpadea("conm"), run_time=0.9)
            self.wait_until_bookmark("s")
            self.play(Indicate(cadena[0][0][0:3], color=COLOR_ESCALAR), Indicate(cadena[2][0][1:4], color=COLOR_ESCALAR),
                      Indicate(enunciado, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.4)
        self.wait(1.0)
        
        self.pausa_media()

class L02_V01_E04_PorSiMismo(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Un vector por sí mismo", "A vector times itself"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        b = vector_col(B_EJ, COLOR_B)
        nb = con_nombre(r"\Vect{b}=", b); nb[0].set_color(COLOR_B)
        nb.move_to([0, 1.45, 0])
        cuenta = MathTex(*EJ_BB, tex_template=myTemplate, font_size=44).move_to([0, -0.3, 0])
        cuenta[0][0].set_color(COLOR_B); cuenta[0][2].set_color(COLOR_B)
        for p_, (f1, f2) in zip((2, 4, 6), ((slice(0, 1), slice(2, 3)), (slice(0, 4), slice(5, 9)), (slice(0, 1), slice(2, 3)))):
            cuenta[p_][f1].set_color(COLOR_B); cuenta[p_][f2].set_color(COLOR_B)
        cuadrados = [cuenta[8], cuenta[9][1], cuenta[10][1]]
        eb = b.get_entries()
        # la suma general de cuadrados: x·x = (x|1)(x|1) + ⋯ + (x|n)(x|n) ≥ 0 (glifos: x · x = 0-3; (x|1)(x|1) 4-13; + 14;
        # ⋯ 15-17; + 18; (x|n)(x|n) 19-28; ≥ 29; 0 30)
        general = MathTex(r"\Vect{x}\cdot\Vect{x}=\eleVRpE{x}{1}\eleVRpE{x}{1}+\cdots+\eleVRpE{x}{n}\eleVRpE{x}{n}\geq 0",
                          tex_template=myTemplate, font_size=44).move_to([0, -1.55, 0])
        sumandos_x = [general[0][4:14], general[0][19:29]]
        componentes_x = [general[0][4:9], general[0][9:14], general[0][19:24], general[0][24:29]]
        cero = MathTex(r"\Vect{x}\cdot\Vect{x}=0\ \Leftrightarrow\ \Vect{x}=\Vect{0}", tex_template=myTemplate, font_size=44).move_to([0, -2.75, 0])
        
        with self.voiceover(text=tr("""Multipliquemos ahora este vector por sí mismo. <bookmark mark='c'/> Cada sumando es el cuadrado de una componente, <bookmark mark='r'/> y el resultado es seis.""",
                                    """Now let us multiply this vector by itself. <bookmark mark='c'/> Each term is the square of a component, <bookmark mark='r'/> and the result is six.""")) as tracker:
            self.play(Write(cabecera), FadeIn(nb), run_time=1)
            self.play(FadeIn(cuenta[0]), FadeIn(cuenta[1]), run_time=0.5)
            self.wait_until_bookmark("c")
            for k, (p_, f1, f2, pt) in enumerate(((2, slice(0, 1), slice(2, 3), [1]), (4, slice(0, 4), slice(5, 9), [4]),
                                                  (6, slice(0, 1), slice(2, 3), [1]))):
                self.play(TransformFromCopy(eb[k], cuenta[p_][f1]), TransformFromCopy(eb[k], cuenta[p_][f2]),
                          *[FadeIn(cuenta[p_][q]) for q in pt], *([FadeIn(cuenta[p_ - 1])] if k else []), run_time=0.45)
            self.play(*[FadeIn(cuenta[k]) for k in range(7, 11)], run_time=0.5)
            self.wait_until_bookmark("r")
            self.play(FadeIn(cuenta[11]), FadeIn(cuenta[12]), run_time=0.5)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Los cuadrados <bookmark mark='q'/> nunca son negativos, <bookmark mark='n'/> aunque el número lo sea.""",
                                    """Squares <bookmark mark='q'/> are never negative, <bookmark mark='n'/> even when the number is.""")) as tracker:
            self.wait_until_bookmark("q")
            resalta(self, cuadrados, factor=1.3)
            self.wait_until_bookmark("n")
            resalta(self, [cuenta[4][0:4], cuenta[4][5:9], eb[1]], factor=1.15)
        self.wait(0.8)
        apaga(self, [cuenta[4][0:4], cuenta[4][5:9]], color=COLOR_B, factor=1.15)
        self.play(eb[1].animate.set_color(COLOR_B).scale(1/1.15), *[x.animate.set_color(WHITE).scale(1/1.3) for x in cuadrados], run_time=0.3)
        
        with self.voiceover(text=tr("""Por tanto, <bookmark mark='g'/> el producto punto de cualquier vector por sí mismo tampoco es negativo.""",
                                    """Therefore, <bookmark mark='g'/> the dot product of any vector with itself is not negative either.""")) as tracker:
            self.wait_until_bookmark("g")
            self.play(Write(general), run_time=1.5)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Además, una suma de números que no son negativos <bookmark mark='s'/> solo es cero si todos ellos son cero, <bookmark mark='u'/> y un cuadrado solo es cero si lo es el número. <bookmark mark='z'/> Por eso, el producto punto de un vector por sí mismo solo es cero cuando el vector es nulo.""",
                                    """Moreover, a sum of numbers that are not negative <bookmark mark='s'/> is zero only if all of them are zero, <bookmark mark='u'/> and a square is zero only if the number is. <bookmark mark='z'/> That is why the dot product of a vector with itself is zero only when the vector is the zero vector.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(*[Indicate(g, color=COLOR_ESCALAR, scale_factor=1.12) for g in sumandos_x], run_time=1.0)
            self.wait_until_bookmark("u")
            self.play(*[Indicate(g, color=COLOR_ESCALAR, scale_factor=1.15) for g in componentes_x], run_time=1.0)
            self.wait_until_bookmark("z")
            self.play(FadeIn(cero), run_time=0.8)
        self.wait(1.0)
        
        self.pausa_media()

class L02_V01_E05_Identidad(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Las columnas de la identidad", "The columns of the identity"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        I3 = matriz([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        nI = con_nombre(r"\Mat{I}=", I3)
        col = vector_col([0, 1, 0], COLOR_COLUMNA)
        ncol = con_nombre(r"\VectC{I}{2}=", col)
        a = vector_col(A_EJ, COLOR_A)
        na = con_nombre(r"\Vect{a}=", a); na[0].set_color(COLOR_A)
        VGroup(na, nI, ncol).arrange(RIGHT, buff=1.0).move_to([0, 1.0, 0])   # en el orden de la cuenta: a, después I y su columna
        franja = franja_columna(I3, 1)
        cuenta = MathTex(*EJ_ID, tex_template=myTemplate, font_size=44).move_to([0, -1.2, 0])
        cuenta[0][0].set_color(COLOR_A); cuenta[0][2:7].set_color(COLOR_COLUMNA)
        for k in (2, 4, 6):
            cuenta[k][0].set_color(COLOR_A); cuenta[k][2].set_color(COLOR_COLUMNA)
        ea, ec = a.get_entries(), col.get_entries()
        # a·(I|i) = a|i = (I|i)·a (glifos: a 0; · 1; (I|i) 2-6; = 7; a|i 8-10; = 11; (I|i) 12-16; · 17; a 18). Primero se ve
        # la parte 0-10 en su sitio; al decir «a la izquierda» nace el resto con los factores cruzándose (como en la escena 3)
        ambos = MathTex(r"\Vect{a}\cdot\VectCpE{I}{i}=\eleVR{a}{i}=\VectCpE{I}{i}\cdot\Vect{a}", tex_template=myTemplate,
                        font_size=48).move_to([0, -2.6, 0])
        for g in (0, 8, 18):
            ambos[0][g].set_color(COLOR_A)
        ambos[0][2:7].set_color(COLOR_COLUMNA); ambos[0][12:17].set_color(COLOR_COLUMNA)
        general = ambos[0][0:11]
        
        with self.voiceover(text=tr("""Este vector tiene tres componentes. <bookmark mark='i'/> Tomemos la matriz identidad de orden tres. <bookmark mark='c'/> Su segunda columna <bookmark mark='v'/> tiene un uno en la segunda posición y ceros en las demás.""",
                                    """This vector has three components. <bookmark mark='i'/> Take the identity matrix of order three. <bookmark mark='c'/> Its second column <bookmark mark='v'/> has a one in the second position and zeros elsewhere.""")) as tracker:
            self.play(Write(cabecera), FadeIn(na), run_time=1)
            self.wait_until_bookmark("i")
            self.play(FadeIn(nI), run_time=0.6)
            self.wait_until_bookmark("c")
            self.play(FadeIn(franja), run_time=0.4)
            self.wait_until_bookmark("v")
            self.play(FadeIn(ncol[0]), FadeIn(col.get_brackets()),
                      *[TransformFromCopy(I3.get_columns()[1][k], ec[k]) for k in range(3)], run_time=0.9)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Multipliquemos este vector por esa columna. <bookmark mark='z'/> Los ceros anulan la primera y la tercera componente, <bookmark mark='u'/> y el uno deja pasar la segunda. <bookmark mark='r'/> El resultado es la segunda componente del vector.""",
                                    """Let us multiply this vector by that column. <bookmark mark='z'/> The zeros cancel out the first and the third component, <bookmark mark='u'/> and the one lets the second one through. <bookmark mark='r'/> The result is the second component of the vector.""")) as tracker:
            self.play(FadeOut(franja), FadeIn(cuenta[0]), FadeIn(cuenta[1]), run_time=0.4)
            for k, p in zip(range(3), (2, 4, 6)):
                self.play(TransformFromCopy(ea[k], cuenta[p][0]), TransformFromCopy(ec[k], cuenta[p][2]), FadeIn(cuenta[p][1]),
                          *([FadeIn(cuenta[p - 1])] if k else []), run_time=0.4)
            self.wait_until_bookmark("z")
            self.play(cuenta[2].animate.set_opacity(0.3), cuenta[6].animate.set_opacity(0.3),
                      ea[0].animate.set_opacity(0.3), ea[2].animate.set_opacity(0.3), run_time=0.4)
            self.wait_until_bookmark("u")
            resalta(self, [cuenta[4]], factor=1.12)
            self.wait_until_bookmark("r")
            self.play(FadeIn(cuenta[7]), TransformFromCopy(ea[1], cuenta[8]), run_time=0.7)
            resalta(self, [ea[1], cuenta[8]], factor=1.3)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""El mismo argumento vale para cualquier columna y cualquier vector: la columna i-ésima de la identidad tiene un uno en la posición i-ésima y ceros en las demás. <bookmark mark='g'/> Así que el producto punto por ella selecciona la componente i-ésima.""",
                                    """The same argument works for any column and any vector: the i-th column of the identity has a one in the i-th position and zeros elsewhere. <bookmark mark='g'/> So the dot product with it selects the i-th component.""")) as tracker:
            self.play(ea[0].animate.set_opacity(1), ea[2].animate.set_opacity(1), run_time=0.5)
            self.wait_until_bookmark("g")
            self.play(FadeIn(general), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Como el producto punto es simétrico, da igual que la columna esté <bookmark mark='d'/> a la derecha <bookmark mark='i'/> o a la izquierda.""",
                                    """Since the dot product is symmetric, it does not matter whether the column is <bookmark mark='d'/> on the right <bookmark mark='i'/> or on the left.""")) as tracker:
            self.wait_until_bookmark("d")
            self.play(Indicate(ambos[0][2:7], color=COLOR_ESCALAR, scale_factor=1.2), run_time=0.8)
            self.wait_until_bookmark("i")
            self.play(FadeIn(ambos[0][11]), TransformFromCopy(ambos[0][2:7], ambos[0][12:17]),
                      TransformFromCopy(ambos[0][1], ambos[0][17]), TransformFromCopy(ambos[0][0], ambos[0][18]), run_time=1.2)
            self.remove(*ambos[0]); self.add(ambos)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Así pues, seleccionar una componente de un vector es lo mismo que multiplicarlo por una columna de la identidad.""",
                                    """So selecting a component of a vector is the same as multiplying it by a column of the identity.""")) as tracker:
            self.play(Indicate(ambos, color=COLOR_ESCALAR, scale_factor=1.08), run_time=1.5)
        self.wait(1.0)
        
        self.pausa_media()

class L02_V01_E06_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [DEF, [r"\Vect{a}\cdot\Vect{b}=\Vect{b}\cdot\Vect{a}"],
                    [r"\Vect{x}\cdot\Vect{x}\geq 0,\qquad \Vect{x}\cdot\Vect{x}=0\ \Leftrightarrow\ \Vect{x}=\Vect{0}"],
                    [r"\Vect{a}\cdot\VectCpE{I}{i}=\eleVR{a}{i}"]]
        rotulos = [tr("suma de productos, posición a posición (un número)", "sum of products, position by position (a number)"),
                   tr("simétrico", "symmetric"),
                   tr("nunca negativo; cero solo para el vector nulo", "never negative; zero only for the zero vector"),
                   tr("la columna i-ésima de I selecciona la componente i-ésima", "the i-th column of I selects the i-th component")]
        filas = VGroup(*[VGroup(MathTex(*f, tex_template=myTemplate, font_size=42), Tex(r, tex_template=myTemplate, font_size=32, color=GRAY_A)).arrange(DOWN, buff=0.15)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.3).next_to(cabecera, DOWN, buff=0.35)
        
        with self.voiceover(text=tr("""Resumamos. El producto punto de dos vectores multiplica las componentes que ocupan la misma posición y suma los productos. Da un número. <bookmark mark='s'/> Además, es simétrico: da igual cuál de los dos vectores va primero.""",
                                    """Let us sum up. The dot product of two vectors multiplies the components in the same position and adds the products. It gives a number. <bookmark mark='s'/> Moreover, it is symmetric: it does not matter which of the two vectors comes first.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(filas[1]), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""El producto punto de un vector por sí mismo nunca es negativo, y solo es cero para el vector nulo. <bookmark mark='i'/> Y multiplicar por una columna de la identidad selecciona una componente.""",
                                    """The dot product of a vector with itself is never negative, and it is zero only for the zero vector. <bookmark mark='i'/> And multiplying by a column of the identity selects a component.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.8)
            self.wait_until_bookmark("i")
            self.play(FadeIn(filas[3]), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos las propiedades del producto punto con la suma de vectores y con el producto por un escalar.""",
                                    """In the next video we will see the properties of the dot product with vector addition and with scalar multiplication.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
