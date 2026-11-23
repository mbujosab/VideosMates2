from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("El producto punto", "The dot product")

A_EJ = [1, 2, 3]      # el ejemplo del libro (Sección 2.1)
B_EJ = [1, -1, 2]
COLOR_COLUMNA = GREEN
Q_EJ = [3, 2, 1]      # la cesta de Omega: kilos de patatas, docenas de huevos, litros de aceite
P_EJ = [1, 3, 6]      # sus precios, en euros (por kilo, por docena, por litro)
EJ_QP = [r"\Vect{q}\cdot\Vect{p}", "=", r"3\cdot 1", "+", r"2\cdot 3", "+", r"1\cdot 6", "=", "3", "+6", "+6", "=", "15", tr(r"\text{ euros}", r"\text{ euros}")]

# Glifos de las cuentas (contados con una imagen numerada; véase cada escena)
EJ_AB = [r"\Vect{a}\cdot\Vect{b}", "=", r"1\cdot 1", "+", r"2\cdot(-1)", "+", r"3\cdot 2", "=", "1", "-2", "+6", "=", "5"]
EJ_BA = [r"\Vect{b}\cdot\Vect{a}", "=", r"1\cdot 1", "+", r"(-1)\cdot 2", "+", r"2\cdot 3", "=", "1", "-2", "+6", "=", "5"]
EJ_BB = [r"\Vect{b}\cdot\Vect{b}", "=", r"1\cdot 1", "+", r"(-1)\cdot(-1)", "+", r"2\cdot 2", "=", "1", "+1", "+4", "=", "6"]
# la misma cuenta con los productos escritos como cuadrados: 1² (2 glifos), (−1)² (5: (, −, 1, ), 2), 2² (2)
EJ_BB2 = [r"\Vect{b}\cdot\Vect{b}", "=", r"1^2", "+", r"(-1)^2", "+", r"2^2", "=", "1", "+1", "+4", "=", "6"]
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


def leyenda(rotulos, v, x_der, font_size=30):
    """Rótulos alineados a la derecha en x_der, cada uno a la altura de su componente de v (como en V08)."""
    filas = VGroup(*[Tex(r, font_size=font_size) for r in rotulos])
    for f, e in zip(filas, v.get_entries()):
        f.move_to([x_der - f.width/2, e.get_y(), 0])
    return filas


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
        intro = MathTex(r"\Vect{a}\cdot\Vect{b}", tex_template=myTemplate, font_size=72).move_to([0, 0.3, 0])
        intro[0][0].set_color(COLOR_A); intro[0][2].set_color(COLOR_B)
        q, p = vector_col(Q_EJ, COLOR_A), vector_col(P_EJ, COLOR_B)
        nq, np_ = con_nombre(r"\Vect{q}=", q), con_nombre(r"\Vect{p}=", p)
        nq[0].set_color(COLOR_A); np_[0].set_color(COLOR_B)
        VGroup(nq, np_).arrange(RIGHT, buff=1.8).move_to([0.2, 0.75, 0])
        ley = leyenda([tr("patatas (kilos)", "potatoes (kilos)"), tr("huevos (docenas)", "eggs (dozens)"), tr("aceite (litros)", "oil (litres)")],
                      q, nq.get_left()[0] - 0.4)
        rot_q = Tex(tr("cantidades", "quantities"), font_size=30).set_color(COLOR_A).next_to(q, UP, buff=0.25)
        rot_p = Tex(tr("precios (euros)", "prices (euros)"), font_size=30).set_color(COLOR_B).next_to(p, UP, buff=0.25)
        rot_p.align_to(rot_q, DOWN)
        cuenta = MathTex(*EJ_QP, tex_template=myTemplate, font_size=46).move_to([-0.9, -1.75, 0])
        cuenta[0][0].set_color(COLOR_A); cuenta[0][2].set_color(COLOR_B)
        prods = [(cuenta[2*k + 2][0:1], cuenta[2*k + 2][2:3]) for k in range(3)]   # (cantidad, precio) de cada producto
        for fa, fb in prods:
            fa.set_color(COLOR_A); fb.set_color(COLOR_B)
        eq, ep = q.get_entries(), p.get_entries()
        marcos_par = [VGroup(marco(eq[k]), marco(ep[k])) for k in range(3)]
        om = omega("duda", mira=LEFT).to_corner(DR, buff=0.5)
        globo = bocadillo(tr(r"¿Cuánto cuesta\\ la compra?", r"How much does\\ the shopping cost?"), om, ancho=3.2)
        
        with self.voiceover(text=tr("""En este vídeo veremos una operación entre dos vectores cuyo resultado es un número: <bookmark mark='pp'/> el producto punto.""",
                                    """In this video we will look at an operation between two vectors whose result is a number: <bookmark mark='pp'/> the dot product.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
            self.wait_until_bookmark("pp")
            self.play(FadeIn(intro, scale=0.9), run_time=0.6)
        self.wait(0.8)   # respiro tras el arranque
        self.play(FadeOut(intro), run_time=0.4)
        
        with self.voiceover(text=tr("""Omega y sus amigos preparan una cena, <bookmark mark='o'/> y quieren conocer el coste de la compra.""",
                                    """Omega and friends are preparing a dinner, <bookmark mark='o'/> and they want to know the cost of the shopping.""")) as tracker:
            entra(self, om)
            self.wait_until_bookmark("o")
            self.play(FadeIn(globo, scale=0.8), run_time=0.6)
        self.wait(0.6)
        
        with self.voiceover(text=tr("""Un vector <bookmark mark='q'/> tiene la cantidad de cada ingrediente de la cesta. <bookmark mark='p'/> Otro tiene sus precios, en el mismo orden.""",
                                    """One vector <bookmark mark='q'/> holds the quantity of each ingredient in the basket. <bookmark mark='p'/> Another holds their prices, in the same order.""")) as tracker:
            self.play(FadeOut(globo), run_time=0.4)
            cambia(self, om, "normal", mira=UL)   # Omega atiende a la cuenta
            self.wait_until_bookmark("q")
            self.play(FadeIn(ley), FadeIn(nq), FadeIn(rot_q), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(FadeIn(np_), FadeIn(rot_p), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Para calcular el coste, multiplicamos <bookmark mark='p1'/> la cantidad de patatas por su precio, <bookmark mark='p2'/> la de huevos por el suyo <bookmark mark='p3'/> y la de aceite por el suyo.""",
                                    """To work out the cost, we multiply <bookmark mark='p1'/> the quantity of potatoes by its price, <bookmark mark='p2'/> the quantity of eggs by theirs <bookmark mark='p3'/> and the quantity of oil by its own.""")) as tracker:
            actual = None
            for k, marca in enumerate(["p1", "p2", "p3"]):
                self.wait_until_bookmark(marca)
                fa, fb = prods[k]
                self.play(FadeIn(marcos_par[k]) if actual is None else ReplacementTransform(actual, marcos_par[k]),
                          ley[k].animate.set_color(COLOR_ESCALAR), *([ley[k-1].animate.set_color(WHITE), FadeIn(cuenta[2*k + 1])] if k else []), run_time=0.3)
                actual = marcos_par[k]
                self.play(TransformFromCopy(eq[k], fa), TransformFromCopy(ep[k], fb), FadeIn(cuenta[2*k + 2][1]), run_time=0.6)
            self.wait(0.4)
            self.play(FadeOut(actual), ley[2].animate.set_color(WHITE), run_time=0.3)
        
        with self.voiceover(text=tr("""Después sumamos los tres productos: <bookmark mark='s'/> la compra cuesta <bookmark mark='r'/> quince euros.""",
                                    """Then we add the three products: <bookmark mark='s'/> the shopping costs <bookmark mark='r'/> fifteen euros.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(*[FadeIn(cuenta[k]) for k in range(7, 11)], run_time=0.6)
            self.wait_until_bookmark("r")
            self.play(FadeIn(cuenta[11]), FadeIn(cuenta[12]), FadeIn(cuenta[13]), run_time=0.5)
            resalta(self, [cuenta[12]], factor=1.3)
            cambia(self, om, "alegria")
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Hemos multiplicado dos vectores componente a componente y hemos sumado los resultados. <bookmark mark='n'/> Esta operación es el producto punto de los dos vectores.""",
                                    """We have multiplied two vectors component by component and added the results. <bookmark mark='n'/> This operation is the dot product of the two vectors.""")) as tracker:
            apaga(self, [cuenta[12]], factor=1.3)
            cambia(self, om, "normal", mira=UL)   # la alegría dura un instante
            self.wait_until_bookmark("n")
            self.play(FadeIn(cuenta[0]), FadeIn(cuenta[1]), run_time=0.6)
            resalta(self, [cuenta[0][1]], factor=1.8)   # el punto
        self.wait(0.6)
        apaga(self, [cuenta[0][1]], factor=1.8)
        # sin pausa_media: aquí no hay nada que pensar ni comprobar y la escena siguiente continúa la idea (Marcos, 2026-11-23)
        self.wait(0.3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Otro ejemplo", "Another example"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
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
        tres = [Tex(tr("3 componentes", "3 components"), font_size=30).set_color(COLOR_ESCALAR).next_to(v, DOWN, buff=0.3) for v in (a, b)]
        
        # el arranque pasó a la escena del coste (2026-11-21); aquí, la misma operación con dos vectores cualesquiera. Sin
        # «Esta operación...», que repetía el final de la escena anterior (Marcos, 2026-11-23)
        # «cualesquiera» al final: delante de la coma quedaba en suspenso en todas las tiradas (Marcos, 2026-11-23); así cierra (tirada v3)
        with self.voiceover(text=tr("""No solo cantidades y precios: del mismo modo podemos multiplicar <bookmark mark='v'/> dos vectores cualesquiera.<bookmark mark='v3'/>""",
                                    """Not only quantities and prices: in the same way we can multiply <bookmark mark='v'/> any two vectors.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("v")
            self.play(FadeIn(na), FadeIn(nb), run_time=0.8)
        self.wait(0.6)
        
        with self.voiceover(text=tr("""Tomemos estos dos vectores. Para calcular <bookmark mark='pp'/> su producto punto, multiplicamos <bookmark mark='p1'/> las primeras componentes, <bookmark mark='p2'/> las segundas <bookmark mark='p3'/> y las terceras.""",
                                    """Take these two vectors. To compute <bookmark mark='pp'/> their dot product, we multiply <bookmark mark='p1'/> the first components, <bookmark mark='p2'/> the second ones <bookmark mark='p3'/> and the third ones.""")) as tracker:
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
            # las parejas una tras otra: el marco recorre las posiciones (Marcos, 2026-11-23: no todas a la vez)
            actual = None
            for k in range(3):
                self.play(Create(marcos_fin[k]) if actual is None else ReplacementTransform(actual, marcos_fin[k]), run_time=0.4)
                actual = marcos_fin[k]
                self.wait(0.5)
            self.wait_until_bookmark("m")
            self.play(FadeOut(actual), *[FadeIn(t, shift=0.1*UP) for t in tres], run_time=0.5)
        self.wait(1.0)
        self.play(*[FadeOut(t) for t in tres], run_time=0.4)
        
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
            for k, j, marca in zip((2, 4, 8), (2, 4, 6), ["p1", "p2", "pn"]):
                self.wait_until_bookmark(marca)
                nuevo = VGroup(marco(deff[k]), marco(ejemplo[j]))   # el sumando general y su producto en el ejemplo
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
        # vuelve el último ejemplo tal como acabó la escena 2: los dos vectores arriba y su cuenta debajo (Marcos, 2026-11-23)
        a, b = vector_col(A_EJ, COLOR_A), vector_col(B_EJ, COLOR_B)
        na, nb = con_nombre(r"\Vect{a}=", a), con_nombre(r"\Vect{b}=", b)
        na[0].set_color(COLOR_A); nb[0].set_color(COLOR_B)
        VGroup(na, nb).arrange(RIGHT, buff=2.2).move_to([0, 0.9, 0])
        ab = MathTex(*EJ_AB, tex_template=myTemplate, font_size=46).move_to([0, -1.7, 0])
        ba = MathTex(*EJ_BA, tex_template=myTemplate, font_size=46)
        ba.shift(ab[1].get_center() - ba[1].get_center() + 1.15*DOWN)   # los iguales, uno debajo del otro
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
        
        with self.voiceover(text=tr("""Volvamos al último ejemplo.""",
                                    """Let us go back to the last example.""")) as tracker:
            self.play(Write(cabecera), FadeIn(na), FadeIn(nb), FadeIn(ab), run_time=1)
        self.wait(0.6)
        
        # la segunda frase es un trozo de la toma anterior («Volvamos al ejemplo. Si intercambiamos...», tmp/parte_toma.py):
        # al decir «intercambiamos» los vectores cambian de sitio, y después los factores de cada producto
        with self.voiceover(text=tr("""Si intercambiamos los dos vectores, en cada producto los factores cambian de sitio, <bookmark mark='r'/> pero el resultado es el mismo.""",
                                    """If we swap the two vectors, in each product the factors swap places, <bookmark mark='r'/> but the result is the same.""")) as tracker:
            self.play(Swap(na, nb), run_time=0.9)
            self.play(*[TransformFromCopy(x, y) for x, y in viajes], run_time=1.6)
            self.wait_until_bookmark("r")
            resalta(self, [ab[12], ba[12]], factor=1.4)
        self.wait(1.2)
        apaga(self, [ab[12], ba[12]], factor=1.4)
        
        with self.voiceover(text=tr("""Este ejemplo solo lo ilustra. <bookmark mark='e'/> Vamos a demostrar que ocurre con dos vectores cualesquiera.""",
                                    """This example only illustrates it. <bookmark mark='e'/> We are going to prove that it happens with any two vectors.""")) as tracker:
            self.wait_until_bookmark("e")
            self.play(*[FadeOut(x) for x in (na, nb, ab, ba)], FadeIn(enunciado), run_time=0.8)
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
                               al_invitar=lambda: panel.pista("def", "conm"))
        # sin la segunda tarjeta, la de la pista (Marcos, 2026-11-21): las dos piezas ya están en pantalla, en el panel, y la
        # voz acaba de nombrarlas; se recuadran mientras la voz invita a pausar
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
                 marca="l1", extra=[panel.piezas["conm"].animate.set_color(COLOR_ESCALAR).scale(1.15)], t_moviles=1.2)
            entera(self, cadena[1])
            panel.cuenta("conm")
            # la conmutativa sigue resaltada todo el paso (Marcos, 2026-11-23) y se apaga tras la campanita
            self.play(panel.piezas["conm"].animate.set_color(WHITE).scale(1/1.15), run_time=0.3)
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
        
        # sin enumerar los usos: los contadores ya están en pantalla (criterio de V14 en adelante; Marcos, 2026-11-23). La
        # toma es el final de la anterior («Hemos usado... Así pues, ...», tmp/parte_toma.py)
        with self.voiceover(text=tr("""Así pues, el producto punto es simétrico.""",
                                    """So the dot product is symmetric.""")) as tracker:
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
        # dos estados de la cuenta: con productos (cuenta) y con cuadrados (cuad), alineados por el igual; la de cuadrados
        # queda centrada. Los productos nacen de las componentes; en «el cuadrado» cada uno se convierte en un cuadrado (el
        # primer factor pasa a la base y el punto y el segundo factor se funden en el exponente; Marcos, 2026-11-23)
        cuad = MathTex(*EJ_BB2, tex_template=myTemplate, font_size=44).move_to([0, -0.3, 0])
        cuenta = MathTex(*EJ_BB, tex_template=myTemplate, font_size=44)
        cuenta.shift(cuad[1].get_center() - cuenta[1].get_center())
        for c_ in (cuenta, cuad):
            c_[0][0].set_color(COLOR_B); c_[0][2].set_color(COLOR_B)
        for p_, (f1, f2) in zip((2, 4, 6), ((slice(0, 1), slice(2, 3)), (slice(0, 4), slice(5, 9)), (slice(0, 1), slice(2, 3)))):
            cuenta[p_][f1].set_color(COLOR_B); cuenta[p_][f2].set_color(COLOR_B)
        bases = [cuad[2][0:1], cuad[4][0:4], cuad[6][0:1]]
        for g in bases:
            g.set_color(COLOR_B)
        # cada producto (factor, punto y factor) y su cuadrado (base y exponente)
        a_cuadrado = [(cuenta[2][0:1], cuenta[2][1:3], cuad[2][0:1], cuad[2][1]),
                      (cuenta[4][0:4], cuenta[4][4:9], cuad[4][0:4], cuad[4][4]),
                      (cuenta[6][0:1], cuenta[6][1:3], cuad[6][0:1], cuad[6][1])]
        cuadrados = [cuad[8], cuad[9][1], cuad[10][1]]
        eb = b.get_entries()
        # la suma general de cuadrados: primero con productos, x·x = (x|1)(x|1) + ⋯ + (x|n)(x|n) ≥ 0 (glifos: x · x = 0-3;
        # (x|1)(x|1) 4-13; + 14; ⋯ 15-17; + 18; (x|n)(x|n) 19-28; ≥ 29; 0 30), y después con cuadrados,
        # x·x = (x|1)² + ⋯ + (x|n)² ≥ 0 (x · x = 0-3; (x|1) 4-8; ² 9; + 10; ⋯ 11-13; + 14; (x|n) 15-19; ² 20; ≥ 21; 0 22)
        general = MathTex(r"\Vect{x}\cdot\Vect{x}=\eleVRpE{x}{1}\eleVRpE{x}{1}+\cdots+\eleVRpE{x}{n}\eleVRpE{x}{n}\geq 0",
                          tex_template=myTemplate, font_size=44).move_to([0, -1.55, 0])
        general2 = MathTex(r"\Vect{x}\cdot\Vect{x}=\eleVRpE{x}{1}^2+\cdots+\eleVRpE{x}{n}^2\geq 0",
                           tex_template=myTemplate, font_size=44).move_to([0, -1.55, 0])
        g, g2 = general[0], general2[0]
        a_cuadrado_x = [(g[0:4], g2[0:4]), (g[4:9], g2[4:9]), (g[9:14], g2[9]), (g[14], g2[10]), (g[15:18], g2[11:14]),
                        (g[18], g2[14]), (g[19:24], g2[15:20]), (g[24:29], g2[20]), (g[29], g2[21]), (g[30], g2[22])]
        sumandos_x = [g2[4:10], g2[15:21]]
        componentes_x = [g2[4:9], g2[15:20]]
        cero = MathTex(r"\Vect{x}\cdot\Vect{x}=0\ \Leftrightarrow\ \Vect{x}=\Vect{0}", tex_template=myTemplate, font_size=44).move_to([0, -2.75, 0])
        
        # los productos nacen al decir «multipliquemos» (la marca c, injertada en la toma que había, ya no hace esperar) y se
        # convierten en cuadrados en la marca q, añadida delante de «el cuadrado»
        with self.voiceover(text=tr("""Multipliquemos ahora este vector por sí mismo. <bookmark mark='c'/> Cada sumando es <bookmark mark='q'/> el cuadrado de una componente.""",
                                    """Now let us multiply this vector by itself. <bookmark mark='c'/> Each term is <bookmark mark='q'/> the square of a component.""")) as tracker:
            self.play(Write(cabecera), FadeIn(nb), run_time=1)
            self.play(FadeIn(cuenta[0]), FadeIn(cuenta[1]), run_time=0.5)
            for k, (p_, f1, f2, pt) in enumerate(((2, slice(0, 1), slice(2, 3), [1]), (4, slice(0, 4), slice(5, 9), [4]),
                                                  (6, slice(0, 1), slice(2, 3), [1]))):
                self.play(TransformFromCopy(eb[k], cuenta[p_][f1]), TransformFromCopy(eb[k], cuenta[p_][f2]),
                          *[FadeIn(cuenta[p_][q]) for q in pt], *([FadeIn(cuenta[p_ - 1])] if k else []), run_time=0.45)
            self.wait_until_bookmark("q")
            self.play(*[ReplacementTransform(fa, ba_) for fa, _, ba_, _ in a_cuadrado],
                      *[ReplacementTransform(resto, ex) for _, resto, _, ex in a_cuadrado],
                      *[ReplacementTransform(cuenta[k], cuad[k]) for k in (0, 1, 3, 5)], run_time=0.9)
            self.add(*[cuad[k] for k in range(7)])
            # el resultado ya no se dice (Marcos, 2026-11-23: se ve, y que es un número ya se dijo en la escena 2)
            self.play(*[FadeIn(cuad[k]) for k in range(7, 11)], run_time=0.5)
            self.play(FadeIn(cuad[11]), FadeIn(cuad[12]), run_time=0.5)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Los cuadrados <bookmark mark='q'/> nunca son negativos, <bookmark mark='n'/> aunque el número lo sea.""",
                                    """Squares <bookmark mark='q'/> are never negative, <bookmark mark='n'/> even when the number is.""")) as tracker:
            self.wait_until_bookmark("q")
            resalta(self, cuadrados, factor=1.3)
            self.wait_until_bookmark("n")
            resalta(self, [cuad[4][0:4], eb[1]], factor=1.15)
        self.wait(0.8)
        apaga(self, [cuad[4][0:4]], color=COLOR_B, factor=1.15)
        self.play(eb[1].animate.set_color(COLOR_B).scale(1/1.15), *[x.animate.set_color(WHITE).scale(1/1.3) for x in cuadrados], run_time=0.3)
        
        # la suma general nace con productos, como dice la definición, y sus productos se convierten en cuadrados como en el ejemplo
        with self.voiceover(text=tr("""Por tanto, <bookmark mark='g'/> el producto punto de cualquier vector por sí mismo tampoco es negativo.""",
                                    """Therefore, <bookmark mark='g'/> the dot product of any vector with itself is not negative either.""")) as tracker:
            self.wait_until_bookmark("g")
            self.play(Write(general), run_time=1.3)
            self.play(*[ReplacementTransform(x, y) for x, y in a_cuadrado_x], run_time=0.9)
            self.remove(*g); self.add(general2)
        self.wait(1.0)
        
        # cada cosa se marca cuando la voz la nombra (Marcos, 2026-11-23): la suma entera mientras se habla de la suma; los
        # sumandos en «todos ellos» y mientras se habla del cuadrado de un número; las bases en «el número»; x·x en «el producto
        # punto»; y la equivalencia aparece en «solo es cero cuando el vector es nulo». Marcas injertadas en la toma v2.
        suma_x = g2[4:21]
        with self.voiceover(text=tr("""Además, <bookmark mark='a'/> una suma de números que no son negativos solo es cero si <bookmark mark='t'/> todos ellos son cero, <bookmark mark='u'/> y el cuadrado de un número solo es cero cuando <bookmark mark='n'/> el número es cero. Por eso, <bookmark mark='p'/> el producto punto de un vector por sí mismo <bookmark mark='c'/> solo es cero cuando el vector es nulo.<bookmark mark='v2'/>""",
                                    """Moreover, <bookmark mark='a'/> a sum of numbers that are not negative is zero only if <bookmark mark='t'/> all of them are zero, <bookmark mark='u'/> and the square of a number is zero only when <bookmark mark='n'/> the number is zero. That is why <bookmark mark='p'/> the dot product of a vector with itself <bookmark mark='c'/> is zero only when the vector is a zero vector.""")) as tracker:
            self.wait_until_bookmark("a")
            self.play(suma_x.animate.set_color(COLOR_ESCALAR), run_time=0.25)
            self.wait_until_bookmark("t")
            self.play(suma_x.animate.set_color(WHITE), *[x.animate.set_color(COLOR_ESCALAR).scale(1.15) for x in sumandos_x], run_time=0.25)
            self.wait_until_bookmark("n")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.15) for x in sumandos_x], run_time=0.2)
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.15) for x in componentes_x], run_time=0.2)
            self.wait_until_bookmark("p")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.15) for x in componentes_x], g2[0:3].animate.set_color(COLOR_ESCALAR).scale(1.15), run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(FadeIn(cero), run_time=0.8)
        self.play(g2[0:3].animate.set_color(WHITE).scale(1/1.15), run_time=0.3)
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
        
        with self.voiceover(text=tr("""Este vector tiene tres componentes. <bookmark mark='i'/> Tomemos ahora la matriz identidad de orden tres. <bookmark mark='c'/> Su segunda columna <bookmark mark='v'/> tiene un uno en la segunda posición y ceros en las demás.<bookmark mark='v2'/>""",
                                    """This vector has three components. <bookmark mark='i'/> Now take the identity matrix of order three. <bookmark mark='c'/> Its second column <bookmark mark='v'/> has a one in the second position and zeros elsewhere.""")) as tracker:
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
            self.play(cuenta[2].animate.set_opacity(0.55), cuenta[6].animate.set_opacity(0.55),
                      ea[0].animate.set_opacity(0.55), ea[2].animate.set_opacity(0.55), run_time=0.4)   # 0.3 casi no se veía
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
                   tr("nunca negativo; cero solo si el vector es nulo", "never negative; zero only if the vector is a zero vector"),
                   tr("la columna i-ésima de I selecciona la componente i-ésima", "the i-th column of I selects the i-th component")]
        filas = VGroup(*[VGroup(MathTex(*f, tex_template=myTemplate, font_size=42), Tex(r, tex_template=myTemplate, font_size=32, color=GRAY_A)).arrange(DOWN, buff=0.15)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.3).next_to(cabecera, DOWN, buff=0.35)
        
        with self.voiceover(text=tr("""Resumamos. El producto punto de dos vectores multiplica las componentes que ocupan la misma posición y suma los productos. Da un número. <bookmark mark='s'/> Además, es simétrico: da igual cuál de los dos vectores va primero.""",
                                    """Let us sum up. The dot product of two vectors multiplies the components in the same position and adds the products. It gives a number. <bookmark mark='s'/> Moreover, it is symmetric: it does not matter which of the two vectors comes first.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(filas[1]), run_time=0.8)
        self.wait(0.8)
        
        # «cuando el vector es nulo», no «para el vector nulo», que parece único (hay uno en cada Rⁿ; Marcos, 2026-11-23). La
        # segunda frase es el final de la toma anterior (tmp/parte_toma.py)
        with self.voiceover(text=tr("""El producto punto de un vector por sí mismo nunca es negativo, y solo es cero cuando el vector es nulo.""",
                                    """The dot product of a vector with itself is never negative, and it is zero only when the vector is a zero vector.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.8)
        with self.voiceover(text=tr("""Y multiplicar por una columna de la identidad selecciona una componente.""",
                                    """And multiplying by a column of the identity selects a component.""")) as tracker:
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

class L02_V01_E01_Coste(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        intro = MathTex(r"\Vect{a}\cdot\Vect{b}", tex_template=myTemplate, font_size=72).move_to([0, 0.3, 0])
        intro[0][0].set_color(COLOR_A); intro[0][2].set_color(COLOR_B)
        q, p = vector_col(Q_EJ, COLOR_A), vector_col(P_EJ, COLOR_B)
        nq, np_ = con_nombre(r"\Vect{q}=", q), con_nombre(r"\Vect{p}=", p)
        nq[0].set_color(COLOR_A); np_[0].set_color(COLOR_B)
        VGroup(nq, np_).arrange(RIGHT, buff=1.8).move_to([0.2, 0.75, 0])
        ley = leyenda([tr("patatas (kilos)", "potatoes (kilos)"), tr("huevos (docenas)", "eggs (dozens)"), tr("aceite (litros)", "oil (litres)")],
                      q, nq.get_left()[0] - 0.4)
        rot_q = Tex(tr("cantidades", "quantities"), font_size=30).set_color(COLOR_A).next_to(q, UP, buff=0.25)
        rot_p = Tex(tr("precios (euros)", "prices (euros)"), font_size=30).set_color(COLOR_B).next_to(p, UP, buff=0.25)
        rot_p.align_to(rot_q, DOWN)
        cuenta = MathTex(*EJ_QP, tex_template=myTemplate, font_size=46).move_to([-0.9, -1.75, 0])
        cuenta[0][0].set_color(COLOR_A); cuenta[0][2].set_color(COLOR_B)
        prods = [(cuenta[2*k + 2][0:1], cuenta[2*k + 2][2:3]) for k in range(3)]   # (cantidad, precio) de cada producto
        for fa, fb in prods:
            fa.set_color(COLOR_A); fb.set_color(COLOR_B)
        eq, ep = q.get_entries(), p.get_entries()
        marcos_par = [VGroup(marco(eq[k]), marco(ep[k])) for k in range(3)]
        om = omega("duda", mira=LEFT).to_corner(DR, buff=0.5)
        globo = bocadillo(tr(r"¿Cuánto cuesta\\ la compra?", r"How much does\\ the shopping cost?"), om, ancho=3.2)
        
        with self.voiceover(text=tr("""En este vídeo veremos una operación entre dos vectores cuyo resultado es un número: <bookmark mark='pp'/> el producto punto.""",
                                    """In this video we will look at an operation between two vectors whose result is a number: <bookmark mark='pp'/> the dot product.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
            self.wait_until_bookmark("pp")
            self.play(FadeIn(intro, scale=0.9), run_time=0.6)
        self.wait(0.8)   # respiro tras el arranque
        self.play(FadeOut(intro), run_time=0.4)
        
        with self.voiceover(text=tr("""Omega y sus amigos preparan una cena, <bookmark mark='o'/> y quieren conocer el coste de la compra.""",
                                    """Omega and friends are preparing a dinner, <bookmark mark='o'/> and they want to know the cost of the shopping.""")) as tracker:
            entra(self, om)
            self.wait_until_bookmark("o")
            self.play(FadeIn(globo, scale=0.8), run_time=0.6)
        self.wait(0.6)
        
        with self.voiceover(text=tr("""Un vector <bookmark mark='q'/> tiene la cantidad de cada ingrediente de la cesta. <bookmark mark='p'/> Otro tiene sus precios, en el mismo orden.""",
                                    """One vector <bookmark mark='q'/> holds the quantity of each ingredient in the basket. <bookmark mark='p'/> Another holds their prices, in the same order.""")) as tracker:
            self.play(FadeOut(globo), run_time=0.4)
            cambia(self, om, "normal", mira=UL)   # Omega atiende a la cuenta
            self.wait_until_bookmark("q")
            self.play(FadeIn(ley), FadeIn(nq), FadeIn(rot_q), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(FadeIn(np_), FadeIn(rot_p), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Para calcular el coste, multiplicamos <bookmark mark='p1'/> la cantidad de patatas por su precio, <bookmark mark='p2'/> la de huevos por el suyo <bookmark mark='p3'/> y la de aceite por el suyo.""",
                                    """To work out the cost, we multiply <bookmark mark='p1'/> the quantity of potatoes by its price, <bookmark mark='p2'/> the quantity of eggs by theirs <bookmark mark='p3'/> and the quantity of oil by its own.""")) as tracker:
            actual = None
            for k, marca in enumerate(["p1", "p2", "p3"]):
                self.wait_until_bookmark(marca)
                fa, fb = prods[k]
                self.play(FadeIn(marcos_par[k]) if actual is None else ReplacementTransform(actual, marcos_par[k]),
                          ley[k].animate.set_color(COLOR_ESCALAR), *([ley[k-1].animate.set_color(WHITE), FadeIn(cuenta[2*k + 1])] if k else []), run_time=0.3)
                actual = marcos_par[k]
                self.play(TransformFromCopy(eq[k], fa), TransformFromCopy(ep[k], fb), FadeIn(cuenta[2*k + 2][1]), run_time=0.6)
            self.wait(0.4)
            self.play(FadeOut(actual), ley[2].animate.set_color(WHITE), run_time=0.3)
        
        with self.voiceover(text=tr("""Después sumamos los tres productos: <bookmark mark='s'/> la compra cuesta <bookmark mark='r'/> quince euros.""",
                                    """Then we add the three products: <bookmark mark='s'/> the shopping costs <bookmark mark='r'/> fifteen euros.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(*[FadeIn(cuenta[k]) for k in range(7, 11)], run_time=0.6)
            self.wait_until_bookmark("r")
            self.play(FadeIn(cuenta[11]), FadeIn(cuenta[12]), FadeIn(cuenta[13]), run_time=0.5)
            resalta(self, [cuenta[12]], factor=1.3)
            cambia(self, om, "alegria")
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Hemos multiplicado dos vectores componente a componente y hemos sumado los resultados. <bookmark mark='n'/> Esta operación es el producto punto de los dos vectores.""",
                                    """We have multiplied two vectors component by component and added the results. <bookmark mark='n'/> This operation is the dot product of the two vectors.""")) as tracker:
            apaga(self, [cuenta[12]], factor=1.3)
            cambia(self, om, "normal", mira=UL)   # la alegría dura un instante
            self.wait_until_bookmark("n")
            self.play(FadeIn(cuenta[0]), FadeIn(cuenta[1]), run_time=0.6)
            resalta(self, [cuenta[0][1]], factor=1.8)   # el punto
        self.wait(0.6)
        apaga(self, [cuenta[0][1]], factor=1.8)
        # sin pausa_media: aquí no hay nada que pensar ni comprobar y la escena siguiente continúa la idea (Marcos, 2026-11-23)
        self.wait(0.3)

class L02_V01_E02_Ejemplo(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Otro ejemplo", "Another example"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
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
        tres = [Tex(tr("3 componentes", "3 components"), font_size=30).set_color(COLOR_ESCALAR).next_to(v, DOWN, buff=0.3) for v in (a, b)]
        
        # el arranque pasó a la escena del coste (2026-11-21); aquí, la misma operación con dos vectores cualesquiera. Sin
        # «Esta operación...», que repetía el final de la escena anterior (Marcos, 2026-11-23)
        # «cualesquiera» al final: delante de la coma quedaba en suspenso en todas las tiradas (Marcos, 2026-11-23); así cierra (tirada v3)
        with self.voiceover(text=tr("""No solo cantidades y precios: del mismo modo podemos multiplicar <bookmark mark='v'/> dos vectores cualesquiera.<bookmark mark='v3'/>""",
                                    """Not only quantities and prices: in the same way we can multiply <bookmark mark='v'/> any two vectors.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("v")
            self.play(FadeIn(na), FadeIn(nb), run_time=0.8)
        self.wait(0.6)
        
        with self.voiceover(text=tr("""Tomemos estos dos vectores. Para calcular <bookmark mark='pp'/> su producto punto, multiplicamos <bookmark mark='p1'/> las primeras componentes, <bookmark mark='p2'/> las segundas <bookmark mark='p3'/> y las terceras.""",
                                    """Take these two vectors. To compute <bookmark mark='pp'/> their dot product, we multiply <bookmark mark='p1'/> the first components, <bookmark mark='p2'/> the second ones <bookmark mark='p3'/> and the third ones.""")) as tracker:
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
            # las parejas una tras otra: el marco recorre las posiciones (Marcos, 2026-11-23: no todas a la vez)
            actual = None
            for k in range(3):
                self.play(Create(marcos_fin[k]) if actual is None else ReplacementTransform(actual, marcos_fin[k]), run_time=0.4)
                actual = marcos_fin[k]
                self.wait(0.5)
            self.wait_until_bookmark("m")
            self.play(FadeOut(actual), *[FadeIn(t, shift=0.1*UP) for t in tres], run_time=0.5)
        self.wait(1.0)
        self.play(*[FadeOut(t) for t in tres], run_time=0.4)
        
        self.pausa_media()

class L02_V01_E03_Definicion(MiEscenaConVoz):
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
            for k, j, marca in zip((2, 4, 8), (2, 4, 6), ["p1", "p2", "pn"]):
                self.wait_until_bookmark(marca)
                nuevo = VGroup(marco(deff[k]), marco(ejemplo[j]))   # el sumando general y su producto en el ejemplo
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

class L02_V01_E04_Simetria(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Simetría", "Symmetry"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        # vuelve el último ejemplo tal como acabó la escena 2: los dos vectores arriba y su cuenta debajo (Marcos, 2026-11-23)
        a, b = vector_col(A_EJ, COLOR_A), vector_col(B_EJ, COLOR_B)
        na, nb = con_nombre(r"\Vect{a}=", a), con_nombre(r"\Vect{b}=", b)
        na[0].set_color(COLOR_A); nb[0].set_color(COLOR_B)
        VGroup(na, nb).arrange(RIGHT, buff=2.2).move_to([0, 0.9, 0])
        ab = MathTex(*EJ_AB, tex_template=myTemplate, font_size=46).move_to([0, -1.7, 0])
        ba = MathTex(*EJ_BA, tex_template=myTemplate, font_size=46)
        ba.shift(ab[1].get_center() - ba[1].get_center() + 1.15*DOWN)   # los iguales, uno debajo del otro
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
        
        with self.voiceover(text=tr("""Volvamos al último ejemplo.""",
                                    """Let us go back to the last example.""")) as tracker:
            self.play(Write(cabecera), FadeIn(na), FadeIn(nb), FadeIn(ab), run_time=1)
        self.wait(0.6)
        
        # la segunda frase es un trozo de la toma anterior («Volvamos al ejemplo. Si intercambiamos...», tmp/parte_toma.py):
        # al decir «intercambiamos» los vectores cambian de sitio, y después los factores de cada producto
        with self.voiceover(text=tr("""Si intercambiamos los dos vectores, en cada producto los factores cambian de sitio, <bookmark mark='r'/> pero el resultado es el mismo.""",
                                    """If we swap the two vectors, in each product the factors swap places, <bookmark mark='r'/> but the result is the same.""")) as tracker:
            self.play(Swap(na, nb), run_time=0.9)
            self.play(*[TransformFromCopy(x, y) for x, y in viajes], run_time=1.6)
            self.wait_until_bookmark("r")
            resalta(self, [ab[12], ba[12]], factor=1.4)
        self.wait(1.2)
        apaga(self, [ab[12], ba[12]], factor=1.4)
        
        with self.voiceover(text=tr("""Este ejemplo solo lo ilustra. <bookmark mark='e'/> Vamos a demostrar que ocurre con dos vectores cualesquiera.""",
                                    """This example only illustrates it. <bookmark mark='e'/> We are going to prove that it happens with any two vectors.""")) as tracker:
            self.wait_until_bookmark("e")
            self.play(*[FadeOut(x) for x in (na, nb, ab, ba)], FadeIn(enunciado), run_time=0.8)
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
                               al_invitar=lambda: panel.pista("def", "conm"))
        # sin la segunda tarjeta, la de la pista (Marcos, 2026-11-21): las dos piezas ya están en pantalla, en el panel, y la
        # voz acaba de nombrarlas; se recuadran mientras la voz invita a pausar
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
                 marca="l1", extra=[panel.piezas["conm"].animate.set_color(COLOR_ESCALAR).scale(1.15)], t_moviles=1.2)
            entera(self, cadena[1])
            panel.cuenta("conm")
            # la conmutativa sigue resaltada todo el paso (Marcos, 2026-11-23) y se apaga tras la campanita
            self.play(panel.piezas["conm"].animate.set_color(WHITE).scale(1/1.15), run_time=0.3)
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
        
        # sin enumerar los usos: los contadores ya están en pantalla (criterio de V14 en adelante; Marcos, 2026-11-23). La
        # toma es el final de la anterior («Hemos usado... Así pues, ...», tmp/parte_toma.py)
        with self.voiceover(text=tr("""Así pues, el producto punto es simétrico.""",
                                    """So the dot product is symmetric.""")) as tracker:
            self.play(Indicate(cadena[0][0][0:3], color=COLOR_ESCALAR), Indicate(cadena[2][0][1:4], color=COLOR_ESCALAR),
                      Indicate(enunciado, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.4)
        self.wait(1.0)
        
        self.pausa_media()

class L02_V01_E05_PorSiMismo(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Un vector por sí mismo", "A vector times itself"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        b = vector_col(B_EJ, COLOR_B)
        nb = con_nombre(r"\Vect{b}=", b); nb[0].set_color(COLOR_B)
        nb.move_to([0, 1.45, 0])
        # dos estados de la cuenta: con productos (cuenta) y con cuadrados (cuad), alineados por el igual; la de cuadrados
        # queda centrada. Los productos nacen de las componentes; en «el cuadrado» cada uno se convierte en un cuadrado (el
        # primer factor pasa a la base y el punto y el segundo factor se funden en el exponente; Marcos, 2026-11-23)
        cuad = MathTex(*EJ_BB2, tex_template=myTemplate, font_size=44).move_to([0, -0.3, 0])
        cuenta = MathTex(*EJ_BB, tex_template=myTemplate, font_size=44)
        cuenta.shift(cuad[1].get_center() - cuenta[1].get_center())
        for c_ in (cuenta, cuad):
            c_[0][0].set_color(COLOR_B); c_[0][2].set_color(COLOR_B)
        for p_, (f1, f2) in zip((2, 4, 6), ((slice(0, 1), slice(2, 3)), (slice(0, 4), slice(5, 9)), (slice(0, 1), slice(2, 3)))):
            cuenta[p_][f1].set_color(COLOR_B); cuenta[p_][f2].set_color(COLOR_B)
        bases = [cuad[2][0:1], cuad[4][0:4], cuad[6][0:1]]
        for g in bases:
            g.set_color(COLOR_B)
        # cada producto (factor, punto y factor) y su cuadrado (base y exponente)
        a_cuadrado = [(cuenta[2][0:1], cuenta[2][1:3], cuad[2][0:1], cuad[2][1]),
                      (cuenta[4][0:4], cuenta[4][4:9], cuad[4][0:4], cuad[4][4]),
                      (cuenta[6][0:1], cuenta[6][1:3], cuad[6][0:1], cuad[6][1])]
        cuadrados = [cuad[8], cuad[9][1], cuad[10][1]]
        eb = b.get_entries()
        # la suma general de cuadrados: primero con productos, x·x = (x|1)(x|1) + ⋯ + (x|n)(x|n) ≥ 0 (glifos: x · x = 0-3;
        # (x|1)(x|1) 4-13; + 14; ⋯ 15-17; + 18; (x|n)(x|n) 19-28; ≥ 29; 0 30), y después con cuadrados,
        # x·x = (x|1)² + ⋯ + (x|n)² ≥ 0 (x · x = 0-3; (x|1) 4-8; ² 9; + 10; ⋯ 11-13; + 14; (x|n) 15-19; ² 20; ≥ 21; 0 22)
        general = MathTex(r"\Vect{x}\cdot\Vect{x}=\eleVRpE{x}{1}\eleVRpE{x}{1}+\cdots+\eleVRpE{x}{n}\eleVRpE{x}{n}\geq 0",
                          tex_template=myTemplate, font_size=44).move_to([0, -1.55, 0])
        general2 = MathTex(r"\Vect{x}\cdot\Vect{x}=\eleVRpE{x}{1}^2+\cdots+\eleVRpE{x}{n}^2\geq 0",
                           tex_template=myTemplate, font_size=44).move_to([0, -1.55, 0])
        g, g2 = general[0], general2[0]
        a_cuadrado_x = [(g[0:4], g2[0:4]), (g[4:9], g2[4:9]), (g[9:14], g2[9]), (g[14], g2[10]), (g[15:18], g2[11:14]),
                        (g[18], g2[14]), (g[19:24], g2[15:20]), (g[24:29], g2[20]), (g[29], g2[21]), (g[30], g2[22])]
        sumandos_x = [g2[4:10], g2[15:21]]
        componentes_x = [g2[4:9], g2[15:20]]
        cero = MathTex(r"\Vect{x}\cdot\Vect{x}=0\ \Leftrightarrow\ \Vect{x}=\Vect{0}", tex_template=myTemplate, font_size=44).move_to([0, -2.75, 0])
        
        # los productos nacen al decir «multipliquemos» (la marca c, injertada en la toma que había, ya no hace esperar) y se
        # convierten en cuadrados en la marca q, añadida delante de «el cuadrado»
        with self.voiceover(text=tr("""Multipliquemos ahora este vector por sí mismo. <bookmark mark='c'/> Cada sumando es <bookmark mark='q'/> el cuadrado de una componente.""",
                                    """Now let us multiply this vector by itself. <bookmark mark='c'/> Each term is <bookmark mark='q'/> the square of a component.""")) as tracker:
            self.play(Write(cabecera), FadeIn(nb), run_time=1)
            self.play(FadeIn(cuenta[0]), FadeIn(cuenta[1]), run_time=0.5)
            for k, (p_, f1, f2, pt) in enumerate(((2, slice(0, 1), slice(2, 3), [1]), (4, slice(0, 4), slice(5, 9), [4]),
                                                  (6, slice(0, 1), slice(2, 3), [1]))):
                self.play(TransformFromCopy(eb[k], cuenta[p_][f1]), TransformFromCopy(eb[k], cuenta[p_][f2]),
                          *[FadeIn(cuenta[p_][q]) for q in pt], *([FadeIn(cuenta[p_ - 1])] if k else []), run_time=0.45)
            self.wait_until_bookmark("q")
            self.play(*[ReplacementTransform(fa, ba_) for fa, _, ba_, _ in a_cuadrado],
                      *[ReplacementTransform(resto, ex) for _, resto, _, ex in a_cuadrado],
                      *[ReplacementTransform(cuenta[k], cuad[k]) for k in (0, 1, 3, 5)], run_time=0.9)
            self.add(*[cuad[k] for k in range(7)])
            # el resultado ya no se dice (Marcos, 2026-11-23: se ve, y que es un número ya se dijo en la escena 2)
            self.play(*[FadeIn(cuad[k]) for k in range(7, 11)], run_time=0.5)
            self.play(FadeIn(cuad[11]), FadeIn(cuad[12]), run_time=0.5)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Los cuadrados <bookmark mark='q'/> nunca son negativos, <bookmark mark='n'/> aunque el número lo sea.""",
                                    """Squares <bookmark mark='q'/> are never negative, <bookmark mark='n'/> even when the number is.""")) as tracker:
            self.wait_until_bookmark("q")
            resalta(self, cuadrados, factor=1.3)
            self.wait_until_bookmark("n")
            resalta(self, [cuad[4][0:4], eb[1]], factor=1.15)
        self.wait(0.8)
        apaga(self, [cuad[4][0:4]], color=COLOR_B, factor=1.15)
        self.play(eb[1].animate.set_color(COLOR_B).scale(1/1.15), *[x.animate.set_color(WHITE).scale(1/1.3) for x in cuadrados], run_time=0.3)
        
        # la suma general nace con productos, como dice la definición, y sus productos se convierten en cuadrados como en el ejemplo
        with self.voiceover(text=tr("""Por tanto, <bookmark mark='g'/> el producto punto de cualquier vector por sí mismo tampoco es negativo.""",
                                    """Therefore, <bookmark mark='g'/> the dot product of any vector with itself is not negative either.""")) as tracker:
            self.wait_until_bookmark("g")
            self.play(Write(general), run_time=1.3)
            self.play(*[ReplacementTransform(x, y) for x, y in a_cuadrado_x], run_time=0.9)
            self.remove(*g); self.add(general2)
        self.wait(1.0)
        
        # cada cosa se marca cuando la voz la nombra (Marcos, 2026-11-23): la suma entera mientras se habla de la suma; los
        # sumandos en «todos ellos» y mientras se habla del cuadrado de un número; las bases en «el número»; x·x en «el producto
        # punto»; y la equivalencia aparece en «solo es cero cuando el vector es nulo». Marcas injertadas en la toma v2.
        suma_x = g2[4:21]
        with self.voiceover(text=tr("""Además, <bookmark mark='a'/> una suma de números que no son negativos solo es cero si <bookmark mark='t'/> todos ellos son cero, <bookmark mark='u'/> y el cuadrado de un número solo es cero cuando <bookmark mark='n'/> el número es cero. Por eso, <bookmark mark='p'/> el producto punto de un vector por sí mismo <bookmark mark='c'/> solo es cero cuando el vector es nulo.<bookmark mark='v2'/>""",
                                    """Moreover, <bookmark mark='a'/> a sum of numbers that are not negative is zero only if <bookmark mark='t'/> all of them are zero, <bookmark mark='u'/> and the square of a number is zero only when <bookmark mark='n'/> the number is zero. That is why <bookmark mark='p'/> the dot product of a vector with itself <bookmark mark='c'/> is zero only when the vector is a zero vector.""")) as tracker:
            self.wait_until_bookmark("a")
            self.play(suma_x.animate.set_color(COLOR_ESCALAR), run_time=0.25)
            self.wait_until_bookmark("t")
            self.play(suma_x.animate.set_color(WHITE), *[x.animate.set_color(COLOR_ESCALAR).scale(1.15) for x in sumandos_x], run_time=0.25)
            self.wait_until_bookmark("n")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.15) for x in sumandos_x], run_time=0.2)
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.15) for x in componentes_x], run_time=0.2)
            self.wait_until_bookmark("p")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.15) for x in componentes_x], g2[0:3].animate.set_color(COLOR_ESCALAR).scale(1.15), run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(FadeIn(cero), run_time=0.8)
        self.play(g2[0:3].animate.set_color(WHITE).scale(1/1.15), run_time=0.3)
        self.wait(1.0)
        
        self.pausa_media()

class L02_V01_E06_Identidad(MiEscenaConVoz):
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
        
        with self.voiceover(text=tr("""Este vector tiene tres componentes. <bookmark mark='i'/> Tomemos ahora la matriz identidad de orden tres. <bookmark mark='c'/> Su segunda columna <bookmark mark='v'/> tiene un uno en la segunda posición y ceros en las demás.<bookmark mark='v2'/>""",
                                    """This vector has three components. <bookmark mark='i'/> Now take the identity matrix of order three. <bookmark mark='c'/> Its second column <bookmark mark='v'/> has a one in the second position and zeros elsewhere.""")) as tracker:
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
            self.play(cuenta[2].animate.set_opacity(0.55), cuenta[6].animate.set_opacity(0.55),
                      ea[0].animate.set_opacity(0.55), ea[2].animate.set_opacity(0.55), run_time=0.4)   # 0.3 casi no se veía
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

class L02_V01_E07_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [DEF, [r"\Vect{a}\cdot\Vect{b}=\Vect{b}\cdot\Vect{a}"],
                    [r"\Vect{x}\cdot\Vect{x}\geq 0,\qquad \Vect{x}\cdot\Vect{x}=0\ \Leftrightarrow\ \Vect{x}=\Vect{0}"],
                    [r"\Vect{a}\cdot\VectCpE{I}{i}=\eleVR{a}{i}"]]
        rotulos = [tr("suma de productos, posición a posición (un número)", "sum of products, position by position (a number)"),
                   tr("simétrico", "symmetric"),
                   tr("nunca negativo; cero solo si el vector es nulo", "never negative; zero only if the vector is a zero vector"),
                   tr("la columna i-ésima de I selecciona la componente i-ésima", "the i-th column of I selects the i-th component")]
        filas = VGroup(*[VGroup(MathTex(*f, tex_template=myTemplate, font_size=42), Tex(r, tex_template=myTemplate, font_size=32, color=GRAY_A)).arrange(DOWN, buff=0.15)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.3).next_to(cabecera, DOWN, buff=0.35)
        
        with self.voiceover(text=tr("""Resumamos. El producto punto de dos vectores multiplica las componentes que ocupan la misma posición y suma los productos. Da un número. <bookmark mark='s'/> Además, es simétrico: da igual cuál de los dos vectores va primero.""",
                                    """Let us sum up. The dot product of two vectors multiplies the components in the same position and adds the products. It gives a number. <bookmark mark='s'/> Moreover, it is symmetric: it does not matter which of the two vectors comes first.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(filas[1]), run_time=0.8)
        self.wait(0.8)
        
        # «cuando el vector es nulo», no «para el vector nulo», que parece único (hay uno en cada Rⁿ; Marcos, 2026-11-23). La
        # segunda frase es el final de la toma anterior (tmp/parte_toma.py)
        with self.voiceover(text=tr("""El producto punto de un vector por sí mismo nunca es negativo, y solo es cero cuando el vector es nulo.""",
                                    """The dot product of a vector with itself is never negative, and it is zero only when the vector is a zero vector.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.8)
        with self.voiceover(text=tr("""Y multiplicar por una columna de la identidad selecciona una componente.""",
                                    """And multiplying by a column of the identity selects a component.""")) as tracker:
            self.play(FadeIn(filas[3]), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos las propiedades del producto punto con la suma de vectores y con el producto por un escalar.""",
                                    """In the next video we will see the properties of the dot product with vector addition and with scalar multiplication.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
