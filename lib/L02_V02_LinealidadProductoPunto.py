from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("La linealidad del producto punto", "Linearity of the dot product")

Q_EJ = [3, 2, 1]      # la cesta del sábado: kilos de patatas, docenas de huevos, litros de aceite (la de L02-V01)
R_EJ = [2, 0, 1]      # la del domingo
P_EJ = [1, 3, 6]      # los precios, en euros
QR_EJ = [q + r for q, r in zip(Q_EJ, R_EJ)]   # (5, 2, 2): la compra de una vez
DOS_Q = [2*q for q in Q_EJ]                   # (6, 4, 2): el doble
A3_EJ, B3_EJ, C3_EJ = [1, 0], [2, 3], [0, 1]  # tres vectores: a·b = 2, b·c = 3
COLOR_LAMBDA = COLOR_ESCALAR


def vector_col(valores, color=WHITE, escala=0.8):
    """Un vector numérico en vertical, entre paréntesis, con sus componentes accesibles."""
    v = IntegerMatrix([[x] for x in valores], v_buff=0.62, left_bracket="(", right_bracket=")")
    v.get_entries().set_color(color)
    return v.scale(escala)


def con_nombre(tex, mob, font_size=48):
    return VGroup(MathTex(tex, tex_template=myTemplate, font_size=font_size), mob).arrange(RIGHT, buff=0.2)


def leyenda(rotulos, v, x_der, font_size=30):
    """Rótulos alineados a la derecha en x_der, cada uno a la altura de su componente de v (como en V08)."""
    filas = VGroup(*[Tex(r, font_size=font_size) for r in rotulos])
    for f, e in zip(filas, v.get_entries()):
        f.move_to([x_der - f.width/2, e.get_y(), 0])
    return filas


def marco(mob, color=COLOR_ESCALAR):
    return SurroundingRectangle(mob, color=color, buff=0.1, corner_radius=0.08, stroke_width=3)


def resalta(escena, mobs, color=COLOR_ESCALAR, factor=1.3, run_time=0.3):
    """Resaltado inmediato y sostenido (color y tamaño), sin la subida lenta de Indicate."""
    escena.play(*[x.animate.set_color(color).scale(factor) for x in mobs], run_time=run_time)


def apaga(escena, mobs, color=WHITE, factor=1.3, run_time=0.3):
    escena.play(*[x.animate.set_color(color).scale(1/factor) for x in mobs], run_time=run_time)


CAMPANITA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos", "campanita.wav")   # suena al subir un contador

# trozos de las cadenas
def X(i): return rf"\eleVRpE{{x}}{{{i}}}"                                   # (x|i): 5 glifos
def Y(i): return rf"\eleVRpE{{y}}{{{i}}}"
def Z(i): return rf"\eleVRpE{{z}}{{{i}}}"
def yb(i): return rf"\eleVR{{y}}{{{i}}}"                                    # y|i: 3 glifos
def zb(i): return rf"\eleVR{{z}}{{{i}}}"
def PL(i): return rf"\parentesis{{\elemRp{{\lambda\Vect{{x}}}}{{{i}}}}}"     # ((λx)|i): 8 glifos
def PS(i): return rf"\parentesis{{\elemRp{{\Vect{{y}}+\Vect{{z}}}}{{{i}}}}}" # ((y+z)|i): 9 glifos
LAM, VX, VY, VZ, PUNTO, CD = r"\lambda", r"\Vect{x}", r"\Vect{y}", r"\Vect{z}", r"\cdot", r"\cdots"

# color de cada glifo de cada trozo: x azul, y naranja, z verde, el escalar amarillo
COLORES = {VX: {0: COLOR_A}, VY: {0: COLOR_B}, VZ: {0: COLOR_C}, LAM: {0: COLOR_LAMBDA}}
for i in ("1", "n"):
    COLORES.update({X(i): {1: COLOR_A}, Y(i): {1: COLOR_B}, Z(i): {1: COLOR_C}, yb(i): {0: COLOR_B}, zb(i): {0: COLOR_C},
                    PL(i): {2: COLOR_LAMBDA, 3: COLOR_A}, PS(i): {2: COLOR_B, 4: COLOR_C}})


class Linea:
    """Una línea de cadena: una sola MathTex partida en trozos por su número de glifos."""
    _n = {}

    def __init__(self, trozos, font_size=34):
        self.trozos = list(trozos)
        self.tex = MathTex("".join(self.trozos), tex_template=myTemplate, font_size=font_size)
        self.g = self.tex[0]
        self.ini, k = [], 0
        for t in self.trozos:
            if t not in Linea._n:
                Linea._n[t] = len(MathTex(t, tex_template=myTemplate)[0])
            self.ini.append(k); k += Linea._n[t]
        assert k == len(self.g), (self.trozos, k, len(self.g))
        for t, trozo in enumerate(self.trozos):
            for j, c in COLORES.get(trozo, {}).items():
                self.g[self(t, j)].set_color(c)

    def __call__(self, t, k=None):
        if k is None:
            return list(range(self.ini[t], self.ini[t] + Linea._n[self.trozos[t]]))
        assert 0 <= k < Linea._n[self.trozos[t]], (t, k)
        return self.ini[t] + k

    def trozo(self, t):
        return VGroup(*[self.g[i] for i in self(t)])


def igual_trozo(lo, to, ld, td):
    """Un trozo que pasa entero, glifo a glifo (los dos trozos tienen los mismos glifos)."""
    return list(zip(lo(to), ld(td)))


def nace_l(escena, lo, ld, fijos=(), moviles=(), aparecen=(), tramo=None, marca=None, extra=(), t_fijos=0.8, t_moviles=0.9):
    """Una línea (o un tramo de una fila) nace de la anterior (V13). Índices de glifos de lo y ld."""
    t0, t1 = tramo or (0, len(ld.trozos) - 1)
    destino = [i for t in range(t0, t1 + 1) for i in ld(t)]
    igual = ld(t0)   # el tramo empieza por su igual
    cubiertos = sorted({j for _, j in fijos} | {j for _, j in moviles} | set(aparecen) | set(igual))
    assert cubiertos == destino, (sorted(set(destino) - set(cubiertos)), sorted(set(cubiertos) - set(destino)))
    escena.play(*extra, *[FadeIn(ld.g[j]) for j in igual],
                *[TransformFromCopy(lo.g[i], ld.g[j]) for i, j in fijos], run_time=t_fijos)
    if marca is not None:
        escena.wait_until_bookmark(marca)
    if moviles or aparecen:
        # si dos glifos de origen se reúnen en uno de destino, el segundo viaja como copia y se retira
        vistos, anims, sobran = {j for _, j in fijos}, [], []
        for i, j in moviles:
            if j in vistos:
                viajero = lo.g[i].copy()
                sobran.append(viajero)
                anims.append(Transform(viajero, ld.g[j].copy()))
            else:
                vistos.add(j)
                anims.append(TransformFromCopy(lo.g[i], ld.g[j]))
        escena.play(*anims, *[FadeIn(ld.g[j]) for j in aparecen], run_time=t_moviles)
        escena.remove(*sobran)


def entera(escena, linea):
    """Tras nacer glifo a glifo, la línea vuelve a estar en la escena como un solo objeto."""
    escena.remove(*linea.g); escena.add(linea.tex)


def coloca_cadena(lineas, y_sup=0.15, salto=0.56, sangria=0.6, ancho_max=12.6):
    """La primera línea arriba y las siguientes (que empiezan por '=') sangradas; todas a la misma escala y el
    conjunto centrado. Si la línea más ancha no cabe, todas se reducen igual."""
    ancho = max(l.tex.width for l in lineas[1:]) + sangria
    ancho = max(ancho, lineas[0].tex.width)
    if ancho > ancho_max:
        for l in lineas:
            l.tex.scale(ancho_max/ancho)
        sangria *= ancho_max/ancho; ancho = ancho_max
    x_izq = -ancho/2
    for k, l in enumerate(lineas):
        l.tex.move_to([0, y_sup - k*salto, 0]).align_to([x_izq + (sangria if k else 0), 0, 0], LEFT)


DEFINICIONES = {"punto":    r"\Vect{a}\cdot\Vect{b}=\eleVRpE{a}{1}\eleVRpE{b}{1}+\cdots+\eleVRpE{a}{n}\eleVRpE{b}{n}",
                "producto": r"\elemRp{\lambda\Vect{a}}{i}=\lambda\eleVRpE{a}{i}",
                "suma":     r"\elemRp{\Vect{a}+\Vect{b}}{i}=\eleVR{a}{i}+\eleVR{b}{i}"}
REALES = {1: r"a+b=b+a", 2: r"a+(b+c)=(a+b)+c", 6: r"a(b+c)=ab+ac", 7: r"a(bc)=(ab)c"}   # numeración de V05 y V07


class Panel:
    """Panel de herramientas (V06, V07, L02-V01): las definiciones que pide la demostración a la izquierda y las
    propiedades de los números reales a la derecha, en pequeño. Cada uso se cuenta con una insignia y la campanita."""
    def __init__(self, escena, definiciones, reales, y_sup=2.95, font_size=28):
        self.escena, self.piezas, self.usos, self.contadores, self.cajas = escena, {}, {}, {}, {}
        izq = VGroup(*[MathTex(DEFINICIONES[c], tex_template=myTemplate, font_size=font_size) for c in definiciones])
        izq.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for c, m in zip(definiciones, izq):
            self.piezas[c] = m
        der = VGroup(*[MathTex(f"{k}.\\;", REALES[k], tex_template=myTemplate, font_size=font_size) for k in reales])
        der.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for k, m in zip(reales, der):
            self.piezas[k] = m
        cab_izq = Tex(tr("Definiciones", "Definitions"), font_size=24).set_color(GRAY_B)
        cab_der = Tex(tr("Números reales", "Real numbers"), font_size=24).set_color(GRAY_B)
        self.izq = VGroup(cab_izq, izq).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=0.35)
        self.der = VGroup(cab_der, der).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=1.0)
        for g in (self.izq, self.der):
            g.align_to([0, y_sup, 0], UP)
        self.todo = VGroup(self.izq, self.der)

    def enciende(self, clave, run_time=0.4):
        """Al nombrarla al presentar el panel: la pieza crece un instante."""
        return Indicate(self.piezas[clave], color=COLOR_ESCALAR, scale_factor=1.12, run_time=run_time)

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


def paso(escena, panel, claves, lo, ld, fijos=(), moviles=(), aparecen=(), marca=None, t_moviles=0.9):
    """Un paso de una demostración con panel (orden de V06): la pieza parpadea mientras se copia lo que no cambia,
    en la marca viaja lo que el paso mueve y, con la línea completa, suben los contadores con la campanita."""
    nace_l(escena, lo, ld, fijos, moviles, aparecen, marca=marca, extra=[panel.senala(c) for c in claves],
           t_moviles=t_moviles)
    entera(escena, ld)
    for c in claves:
        panel.cuenta(c)


def enunciado(trozos, y=1.0, font_size=42):
    return Linea(trozos, font_size).tex.move_to([0, y, 0])


class L02_V02_LinealidadProductoPunto(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        VQ, VR, VP = r"\Vect{q}", r"\Vect{r}", r"\Vect{p}"
        q, r, qr, p = vector_col(Q_EJ, COLOR_A), vector_col(R_EJ, COLOR_C), vector_col(QR_EJ), vector_col(P_EJ, COLOR_B)
        nq, nr, nqr, np_ = con_nombre(VQ + "=", q), con_nombre(VR + "=", r), con_nombre(VQ + "+" + VR + "=", qr), con_nombre(VP + "=", p)
        nq[0].set_color(COLOR_A); nr[0].set_color(COLOR_C); np_[0].set_color(COLOR_B)
        nqr[0][0][0].set_color(COLOR_A); nqr[0][0][2].set_color(COLOR_C)
        fila = VGroup(nq, nr, nqr, np_).arrange(RIGHT, buff=0.55).move_to([0.9, 1.15, 0])
        ley = leyenda([tr("patatas (kilos)", "potatoes (kilos)"), tr("huevos (docenas)", "eggs (dozens)"), tr("aceite (litros)", "oil (litres)")],
                      q, nq.get_left()[0] - 0.3, font_size=26)
        rot = [Tex(t, font_size=26).set_color(c).next_to(v, UP, buff=0.22) for t, c, v in
               ((tr("sábado", "Saturday"), COLOR_A, q), (tr("domingo", "Sunday"), COLOR_C, r), (tr("precios (euros)", "prices (euros)"), COLOR_B, p))]
        for x in rot[1:]:
            x.align_to(rot[0], DOWN)
        
        
        def cuenta(trozos, y):
            m = MathTex(*trozos, tex_template=myTemplate, font_size=42).move_to([0, y, 0])
            for k, t in enumerate(trozos):
                m[k].set_color({VQ: COLOR_A, VR: COLOR_C, VP: COLOR_B}.get(t, WHITE))
            return m
        
        
        cq = cuenta([VQ, PUNTO, VP, "=", "15"], -1.0)
        cr = cuenta([VR, PUNTO, VP, "=", "8"], -1.75)
        cqr = cuenta(["(", VQ, "+", VR, ")", PUNTO, VP, "=", "23", "=", "15", "+", "8"], -2.6)
        for c_ in (cr, cqr):   # los iguales, en columna
            c_.shift((cq[3].get_x() - c_[3 if c_ is cr else 7].get_x())*RIGHT)
        c2q = cuenta(["(", "2", VQ, ")", PUNTO, VP, "=", "30", "=", "2", PUNTO, "15"], -1.75)
        c2q.shift((cq[3].get_x() - c2q[6].get_x())*RIGHT)
        dosq = vector_col(DOS_Q, COLOR_A)
        ndosq = con_nombre(r"2" + VQ + "=", dosq); ndosq[0][0][1].set_color(COLOR_A)
        ndosq.move_to(nr).align_to(nr, LEFT)
        om = omega("normal", mira=UL).to_corner(DR, buff=0.4)
        
        with self.voiceover(text=tr("""En este vídeo veremos las propiedades del producto punto con la suma de vectores y con el producto por un escalar.""",
                                    """In this video we will see the properties of the dot product with vector addition and with scalar multiplication.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        self.wait(0.8)   # respiro tras el arranque
        
        with self.voiceover(text=tr("""Omega y sus amigos hacen la compra dos días seguidos. <bookmark mark='q'/> El sábado compran esta cesta, <bookmark mark='r'/> y el domingo, esta otra. <bookmark mark='p'/> Los precios no cambian.""",
                                    """Omega and friends do the shopping on two days in a row. <bookmark mark='q'/> On Saturday they buy this basket, <bookmark mark='r'/> and on Sunday, this other one. <bookmark mark='p'/> The prices do not change.""")) as tracker:
            entra(self, om)
            self.wait_until_bookmark("q")
            self.play(FadeIn(ley), FadeIn(nq), FadeIn(rot[0]), run_time=0.8)
            self.wait_until_bookmark("r")
            self.play(FadeIn(nr), FadeIn(rot[1]), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(FadeIn(np_), FadeIn(rot[2]), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""El coste de una compra es el producto punto de la cesta por los precios: cada cantidad se multiplica por su precio, y se suman los resultados. <bookmark mark='c1'/> El sábado gastan quince euros, <bookmark mark='c2'/> y el domingo, ocho.""",
                                    """The cost of a purchase is the dot product of the basket and the prices: each quantity is multiplied by its price, and the results are added. <bookmark mark='c1'/> On Saturday they spend fifteen euros, <bookmark mark='c2'/> and on Sunday, eight.""")) as tracker:
            self.wait_until_bookmark("c1")
            self.play(TransformFromCopy(nq[0][0][0], cq[0]), TransformFromCopy(np_[0][0][0], cq[2]), FadeIn(cq[1]), run_time=0.6)
            self.play(FadeIn(cq[3]), FadeIn(cq[4]), run_time=0.4)
            self.wait_until_bookmark("c2")
            self.play(TransformFromCopy(nr[0][0][0], cr[0]), TransformFromCopy(np_[0][0][0], cr[2]), FadeIn(cr[1]), run_time=0.6)
            self.play(FadeIn(cr[3]), FadeIn(cr[4]), run_time=0.4)
        self.wait(1.0)
        
        # la cesta total nace de las dos (cada componente, de las dos de su fila); su coste, de la suma y los precios
        with self.voiceover(text=tr("""Si hubieran comprado todo de una vez, <bookmark mark='s'/> la cesta sería la suma de las dos, <bookmark mark='t'/> y su coste, veintitrés euros: <bookmark mark='u'/> lo mismo que la suma de los dos costes.""",
                                    """Had they bought everything at once, <bookmark mark='s'/> the basket would be the sum of the two, <bookmark mark='t'/> and its cost, twenty-three euros: <bookmark mark='u'/> the same as the sum of the two costs.""")) as tracker:
            self.wait_until_bookmark("s")
            eq_, er_, eqr = q.get_entries(), r.get_entries(), qr.get_entries()
            self.play(FadeIn(nqr[0]), FadeIn(qr.get_brackets()),
                      *[TransformFromCopy(VGroup(eq_[k], er_[k]), eqr[k]) for k in range(3)], run_time=1.0)
            self.wait_until_bookmark("t")
            self.play(*[FadeIn(cqr[k]) for k in range(7)], run_time=0.6)
            self.play(FadeIn(cqr[7]), FadeIn(cqr[8]), run_time=0.4)
            cambia(self, om, "alegria")
            self.wait_until_bookmark("u")
            self.play(FadeIn(cqr[9]), TransformFromCopy(cq[4], cqr[10]), FadeIn(cqr[11]), TransformFromCopy(cr[4], cqr[12]), run_time=0.8)
            cambia(self, om, "normal", mira=UL)   # la alegría dura un instante
        self.wait(1.0)
        
        # la cantinela de V14: en cada verbo, la operación que nombra
        with self.voiceover(text=tr("""Da igual <bookmark mark='a1'/> sumar primero las cestas y <bookmark mark='a2'/> calcular después el coste, que <bookmark mark='a3'/> calcular primero los costes y <bookmark mark='a4'/> sumarlos después.""",
                                    """It makes no difference whether we <bookmark mark='a1'/> add the baskets first and <bookmark mark='a2'/> work out the cost afterwards, or <bookmark mark='a3'/> work out the costs first and <bookmark mark='a4'/> add them afterwards.""")) as tracker:
            previo = []
            for marca, mobs in (("a1", [cqr[2]]), ("a2", [cqr[5]]), ("a3", [cq[1], cr[1]]), ("a4", [cqr[11]])):
                self.wait_until_bookmark(marca)
                self.play(*[x.animate.set_color(WHITE).scale(1/1.6) for x in previo],
                          *[x.animate.set_color(COLOR_ESCALAR).scale(1.6) for x in mobs], run_time=0.25)
                previo = mobs
            self.wait(0.6)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.6) for x in previo], run_time=0.25)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Ahora, si la cena del sábado fuera para el doble de invitados, <bookmark mark='d'/> comprarían el doble de cada ingrediente, <bookmark mark='e'/> y el coste también sería el doble: treinta euros.""",
                                    """Now, if Saturday's dinner were for twice as many guests, <bookmark mark='d'/> they would buy twice as much of each ingredient, <bookmark mark='e'/> and the cost would be twice as much too: thirty euros.""")) as tracker:
            self.play(*[FadeOut(x) for x in (nr, rot[1], nqr, cr, cqr)], run_time=0.6)
            self.wait_until_bookmark("d")
            edq = dosq.get_entries()
            self.play(FadeIn(ndosq[0]), FadeIn(dosq.get_brackets()),
                      *[TransformFromCopy(q.get_entries()[k], edq[k]) for k in range(3)], run_time=1.0)
            self.wait_until_bookmark("e")
            self.play(*[FadeIn(c2q[k]) for k in range(6)], run_time=0.6)
            self.play(FadeIn(c2q[6]), FadeIn(c2q[7]), run_time=0.4)
            self.play(FadeIn(c2q[8]), FadeIn(c2q[9]), FadeIn(c2q[10]), TransformFromCopy(cq[4], c2q[11]), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Da igual <bookmark mark='b1'/> multiplicar primero la cesta por dos y <bookmark mark='b2'/> calcular después el coste, que <bookmark mark='b3'/> calcular primero el coste y <bookmark mark='b4'/> multiplicarlo después por dos.""",
                                    """It makes no difference whether we <bookmark mark='b1'/> multiply the basket by two first and <bookmark mark='b2'/> work out the cost afterwards, or <bookmark mark='b3'/> work out the cost first and <bookmark mark='b4'/> multiply it by two afterwards.""")) as tracker:
            previo = []
            for marca, mobs in (("b1", [c2q[1]]), ("b2", [c2q[4]]), ("b3", [cq[1]]), ("b4", [c2q[9]])):
                self.wait_until_bookmark(marca)
                self.play(*[x.animate.set_color(WHITE).scale(1/1.6) for x in previo],
                          *[x.animate.set_color(COLOR_ESCALAR).scale(1.6) for x in mobs], run_time=0.25)
                previo = mobs
            self.wait(0.6)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.6) for x in previo], run_time=0.25)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Este ejemplo solo lo ilustra. <bookmark mark='e'/> Vamos a demostrar que estas dos igualdades valen para vectores cualesquiera.""",
                                    """This example only illustrates it. <bookmark mark='e'/> We are going to prove that these two equalities hold for any vectors.""")) as tracker:
            self.wait_until_bookmark("e")
            self.play(Indicate(c2q, color=COLOR_ESCALAR, scale_factor=1.06), Indicate(cq, color=COLOR_ESCALAR, scale_factor=1.06), run_time=1.2)
        self.wait(0.6)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Lineal en un argumento", "Linear in one argument"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        I1S = Linea(["(", VX, "+", VY, ")", PUNTO, VZ, "=", VX, PUNTO, VZ, "+", VY, PUNTO, VZ], 40).tex
        I1E = Linea(["(", LAM, VX, ")", PUNTO, VY, "=", LAM, "(", VX, PUNTO, VY, ")"], 40).tex
        I2S = Linea([VX, PUNTO, "(", VY, "+", VZ, ")", "=", VX, PUNTO, VY, "+", VX, PUNTO, VZ], 40).tex
        I2E = Linea([VX, PUNTO, "(", LAM, VY, ")", "=", LAM, "(", VX, PUNTO, VY, ")"], 40).tex
        col1 = VGroup(I1S, I1E).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([-3.4, -0.2, 0])
        col2 = VGroup(I2S, I2E).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([3.4, -0.2, 0])
        r1 = Tex(tr(r"lineal en el\\ primer argumento", r"linear in the\\ first argument"), font_size=32).set_color(GRAY_A).next_to(col1, UP, buff=0.55)
        r2 = Tex(tr(r"lineal en el\\ segundo argumento", r"linear in the\\ second argument"), font_size=32).set_color(GRAY_A).next_to(col2, UP, buff=0.55)
        r2.align_to(r1, UP)
        fijo1 = Tex(tr(r"$\Vect{z}$ fijo", r"$\Vect{z}$ fixed"), tex_template=myTemplate, font_size=28).set_color(COLOR_C).next_to(col1, DOWN, buff=0.45)
        fijo2 = Tex(tr(r"$\Vect{x}$ fijo", r"$\Vect{x}$ fixed"), tex_template=myTemplate, font_size=28).set_color(COLOR_A).next_to(col2, DOWN, buff=0.45)
        fijo2.align_to(fijo1, UP)
        
        with self.voiceover(text=tr("""En el ejemplo, los precios estaban fijos y cambiaba la cesta. <bookmark mark='s'/> Con el segundo vector fijo, el producto punto se distribuye en las sumas <bookmark mark='p'/> y es asociativo con el producto por un escalar.""",
                                    """In the example, the prices were fixed and the basket changed. <bookmark mark='s'/> With the second vector fixed, the dot product distributes over sums <bookmark mark='p'/> and is associative with scalar multiplication.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.play(FadeIn(fijo1), run_time=0.5)
            self.wait_until_bookmark("s")
            self.play(FadeIn(I1S), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(FadeIn(I1E), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Por eso se dice que es lineal en el primer argumento, <bookmark mark='v'/> es decir, en el primer vector.""",
                                    """That is why we say that it is linear in the first argument, <bookmark mark='v'/> that is, in the first vector.""")) as tracker:
            self.play(FadeIn(r1), run_time=0.6)
            self.wait_until_bookmark("v")
            primeros = [I1S[0][0:5], I1E[0][0:4]]   # (x+y) y (λx): el primer vector de cada igualdad
            resalta(self, primeros, factor=1.15)
        self.wait(0.8)
        apaga(self, primeros, factor=1.15)
        for g in (I1S[0][1], I1E[0][2]):
            g.set_color(COLOR_A)
        I1S[0][3].set_color(COLOR_B); I1E[0][1].set_color(COLOR_LAMBDA)
        
        with self.voiceover(text=tr("""Del mismo modo, <bookmark mark='f'/> con el primer vector fijo, <bookmark mark='l'/> es lineal en el segundo argumento.""",
                                    """In the same way, <bookmark mark='f'/> with the first vector fixed, <bookmark mark='l'/> it is linear in the second argument.""")) as tracker:
            self.wait_until_bookmark("f")
            self.play(FadeIn(fijo2), run_time=0.5)
            self.wait_until_bookmark("l")
            self.play(FadeIn(r2), FadeIn(I2S), FadeIn(I2E), run_time=1.0)
        self.wait(1.2)
        
        with self.voiceover(text=tr("""Vamos a demostrar dos de estas igualdades con las definiciones: <bookmark mark='a'/> la del escalar en el primer vector <bookmark mark='b'/> y la de la suma en el segundo. <bookmark mark='c'/> Las otras dos saldrán de la simetría del producto punto.""",
                                    """We are going to prove two of these equalities from the definitions: <bookmark mark='a'/> the one with the scalar in the first vector <bookmark mark='b'/> and the one with the sum in the second. <bookmark mark='c'/> The other two will follow from the symmetry of the dot product.""")) as tracker:
            self.wait_until_bookmark("a")
            ca = marco(I1E)
            self.play(Create(ca), run_time=0.4)
            self.wait_until_bookmark("b")
            cb = marco(I2S)
            self.play(Create(cb), run_time=0.4)
            self.wait_until_bookmark("c")
            cs = [marco(I1S, COLOR_REGLA), marco(I2E, COLOR_REGLA)]
            self.play(*[Create(x) for x in cs], run_time=0.5)
        self.wait(1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("El escalar en el primer vector", "The scalar in the first vector"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        panel = Panel(self, ["punto", "producto"], [6, 7])
        E = Linea(["(", LAM, VX, ")", PUNTO, VY, "=", LAM, "(", VX, PUNTO, VY, ")"], 42)
        E.tex.move_to([0, 1.0, 0])
        A0 = Linea(["(", LAM, VX, ")", PUNTO, VY])
        A1 = Linea(["=", PL(1), Y(1), "+", CD, "+", PL("n"), Y("n")])
        A2 = Linea(["=", "(", LAM, X(1), ")", Y(1), "+", CD, "+", "(", LAM, X("n"), ")", Y("n")])
        A3 = Linea(["=", LAM, "(", X(1), Y(1), ")", "+", CD, "+", LAM, "(", X("n"), Y("n"), ")"])
        A4 = Linea(["=", LAM, "(", X(1), Y(1), "+", CD, "+", X("n"), Y("n"), ")"])
        A5 = Linea(["=", LAM, "(", VX, PUNTO, VY, ")"])
        cadena = [A0, A1, A2, A3, A4, A5]
        coloca_cadena(cadena)
        for L in (A3, A4):
            L.g[0].set_color(COLOR_REGLA)   # pasos con números reales
        
        # A0 -> A1 (definición del producto punto): (λx) va a cada ((λx)|i) e y a cada (y|i)
        a01 = [A1(p, k) for p in (1, 6) for k in (0, 5, 6, 7)] + [A1(p, k) for p in (2, 7) for k in (0, 2, 3, 4)] + A1(3) + A1(4) + A1(5)
        m01 = [(A0.ini[t], A1(p, t + 1)) for p in (1, 6) for t in range(4)] + [(A0.ini[5], A1(p, 1)) for p in (2, 7)]
        # A1 -> A2 (definición del producto por un escalar: desplazar los paréntesis)
        f12 = sum([igual_trozo(A1, o, A2, d) for o, d in ((2, 5), (3, 6), (4, 7), (5, 8), (7, 13))], [])
        m12 = []
        for p, b in ((1, 1), (6, 9)):
            m12 += [(A1(p, 0), A2(b, 0)), (A1(p, 1), A2(b + 2, 0)), (A1(p, 2), A2(b + 1, 0)), (A1(p, 3), A2(b + 2, 1)),
                    (A1(p, 4), A2(b + 2, 4)), (A1(p, 5), A2(b + 2, 2)), (A1(p, 6), A2(b + 2, 3)), (A1(p, 7), A2(b + 3, 0))]
        # A2 -> A3 (asociativa: desplazar los paréntesis)
        f23 = sum([igual_trozo(A2, o, A3, d) for o, d in ((3, 3), (5, 4), (6, 6), (7, 7), (8, 8), (11, 11), (13, 12))], [])
        m23 = []
        for b2, b3 in ((1, 1), (9, 9)):
            m23 += [(A2(b2, 0), A3(b3 + 1, 0)), (A2(b2 + 1, 0), A3(b3, 0)), (A2(b2 + 3, 0), A3(b3 + 4, 0))]
        # A3 -> A4 (distributiva: el escalar, factor común)
        f34 = sum([igual_trozo(A3, o, A4, d) for o, d in ((3, 3), (4, 4), (6, 5), (7, 6), (8, 7), (11, 8), (12, 9))], [])
        m34 = [(A3(1, 0), A4(1, 0)), (A3(9, 0), A4(1, 0)), (A3(2, 0), A4(2, 0)), (A3(13, 0), A4(10, 0))]
        # A4 -> A5 (definición del producto punto, de derecha a izquierda)
        f45 = [(A4(1, 0), A5(1, 0)), (A4(2, 0), A5(2, 0)), (A4(10, 0), A5(6, 0))]
        m45 = [(A4(3, 1), A5(3, 0)), (A4(8, 1), A5(3, 0)), (A4(4, 1), A5(5, 0)), (A4(9, 1), A5(5, 0))]
        
        with self.voiceover(text=tr("""Empecemos por el escalar en el primer vector. <bookmark mark='e'/> Queremos demostrar que sale del producto punto.""",
                                    """Let us start with the scalar in the first vector. <bookmark mark='e'/> We want to prove that it comes out of the dot product.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("e")
            self.play(FadeIn(E.tex), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Para demostrarlo contamos con las definiciones <bookmark mark='d1'/> del producto punto <bookmark mark='d2'/> y del producto por un escalar, y con dos propiedades de los números reales: <bookmark mark='r6'/> la distributiva <bookmark mark='r7'/> y la asociativa.""",
                                    """To prove it we can use the definitions <bookmark mark='d1'/> of the dot product <bookmark mark='d2'/> and of scalar multiplication, and two properties of real numbers: <bookmark mark='r6'/> the distributive property <bookmark mark='r7'/> and the associative property.""")) as tracker:
            self.play(FadeIn(panel.todo), run_time=0.8)
            for marca, clave in (("d1", "punto"), ("d2", "producto"), ("r6", 6), ("r7", 7)):
                self.wait_until_bookmark(marca)
                self.play(panel.enciende(clave))
        self.wait(0.8)
        
        self.pausa_para_pensar(invitacion=tr(r"Demuestre que $(\lambda\Vect{x})\cdot\Vect{y}=\lambda(\Vect{x}\cdot\Vect{y})$.",
                                             r"Prove that $(\lambda\Vect{x})\cdot\Vect{y}=\lambda(\Vect{x}\cdot\Vect{y})$."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que el escalar sale del producto punto.",
                                                 "Pause the video and try to prove that the scalar comes out of the dot product."),
                               al_invitar=lambda: panel.pista("punto", "producto", 6, 7))
        panel.quita_pista()
        
        with self.voiceover(text=tr("""Partimos del lado izquierdo. <bookmark mark='k'/> Por la definición del producto punto <bookmark mark='l1'/> podemos escribirlo como una suma de productos de componentes.""",
                                    """We start from the left-hand side. <bookmark mark='k'/> By the definition of the dot product <bookmark mark='l1'/> we can write it as a sum of products of components.""")) as tracker:
            self.play(*[TransformFromCopy(E.g[i], A0.g[i]) for i in range(6)], run_time=1.0)
            entera(self, A0)
            self.wait_until_bookmark("k")
            paso(self, panel, ["punto"], A0, A1, [], m01, a01, marca="l1", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Por la definición del producto por un escalar, <bookmark mark='l2'/> en cada sumando podemos desplazar los paréntesis.""",
                                    """By the definition of scalar multiplication, <bookmark mark='l2'/> in each term we can move the parentheses.""")) as tracker:
            paso(self, panel, ["producto"], A1, A2, f12, m12, marca="l2", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Ya todo son números reales. <bookmark mark='k'/> Por la asociativa <bookmark mark='l3'/> podemos desplazar otra vez los paréntesis.""",
                                    """Now everything is a real number. <bookmark mark='k'/> By the associative property <bookmark mark='l3'/> we can move the parentheses again.""")) as tracker:
            self.wait_until_bookmark("k")
            paso(self, panel, [7], A2, A3, f23, m23, marca="l3", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""El escalar multiplica a todos los sumandos, <bookmark mark='k'/> así que por la distributiva <bookmark mark='l4'/> podemos sacarlo como factor común.""",
                                    """The scalar multiplies every term, <bookmark mark='k'/> so by the distributive property <bookmark mark='l4'/> we can take it out as a common factor.""")) as tracker:
            self.play(*[Indicate(A3.g[A3(t, 0)], color=COLOR_ESCALAR, scale_factor=1.6) for t in (1, 9)], run_time=0.9)
            self.wait_until_bookmark("k")
            paso(self, panel, [6], A3, A4, f34, m34, marca="l4", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Y por la definición del producto punto, <bookmark mark='l5'/> la suma entre paréntesis es el producto punto de x por y.""",
                                    """And by the definition of the dot product, <bookmark mark='l5'/> the sum in parentheses is the dot product of x and y.""")) as tracker:
            paso(self, panel, ["punto"], A4, A5, f45, m45, [A5(4, 0)], marca="l5", t_moviles=1.2)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Así pues, el escalar sale del producto punto.""",
                                    """So the scalar comes out of the dot product.""")) as tracker:
            self.play(Indicate(A0.tex, color=COLOR_ESCALAR), Indicate(A5.tex, color=COLOR_ESCALAR),
                      Create(marco(E.tex)), run_time=1.4)
        self.wait(1.0)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("La suma en el segundo vector", "The sum in the second vector"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        panel = Panel(self, ["punto", "suma"], [6, 1, 2])
        E = Linea([VX, PUNTO, "(", VY, "+", VZ, ")", "=", VX, PUNTO, VY, "+", VX, PUNTO, VZ], 42)
        E.tex.move_to([0, 0.95, 0])
        B0 = Linea([VX, PUNTO, "(", VY, "+", VZ, ")"])
        B1 = Linea(["=", X(1), PS(1), "+", CD, "+", X("n"), PS("n")])
        B2 = Linea(["=", X(1), "(", yb(1), "+", zb(1), ")", "+", CD, "+", X("n"), "(", yb("n"), "+", zb("n"), ")"])
        B3 = Linea(["=", "(", X(1), Y(1), "+", X(1), Z(1), ")", "+", CD, "+", "(", X("n"), Y("n"), "+", X("n"), Z("n"), ")"])
        B4 = Linea(["=", "(", X(1), Y(1), "+", CD, "+", X("n"), Y("n"), ")", "+", "(", X(1), Z(1), "+", CD, "+", X("n"), Z("n"), ")"])
        B5 = Linea(["=", VX, PUNTO, VY, "+", VX, PUNTO, VZ])
        cadena = [B0, B1, B2, B3, B4, B5]
        coloca_cadena(cadena, y_sup=0.1)
        for L in (B3, B4):
            L.g[0].set_color(COLOR_REGLA)   # pasos con números reales
        
        # B0 -> B1 (definición del producto punto): x va a cada (x|i) y (y+z) a cada ((y+z)|i)
        m01 = [(B0.ini[0], B1(p, 1)) for p in (1, 6)] + [(B0.ini[2 + k], B1(p, 1 + k)) for p in (2, 7) for k in range(5)]
        a01 = [B1(p, k) for p in (1, 6) for k in (0, 2, 3, 4)] + [B1(p, k) for p in (2, 7) for k in (0, 6, 7, 8)] + B1(3) + B1(4) + B1(5)
        # B1 -> B2 (definición de suma: distribuir el selector; la barra y el índice viajan a los dos sumandos)
        f12 = sum([igual_trozo(B1, o, B2, d) for o, d in ((1, 1), (3, 7), (4, 8), (5, 9), (6, 10))], [])
        m12 = []
        for p, b in ((2, 2), (7, 11)):
            m12 += [(B1(p, 0), B2(b, 0)), (B1(p, 2), B2(b + 1, 0)), (B1(p, 3), B2(b + 2, 0)), (B1(p, 4), B2(b + 3, 0)),
                    (B1(p, 6), B2(b + 1, 1)), (B1(p, 6), B2(b + 3, 1)), (B1(p, 7), B2(b + 1, 2)), (B1(p, 7), B2(b + 3, 2)),
                    (B1(p, 8), B2(b + 4, 0))]
        # B2 -> B3 (distributiva: la componente de x se reparte entre los dos sumandos)
        f23 = sum([igual_trozo(B2, o, B3, d) for o, d in ((7, 8), (8, 9), (9, 10))], [])
        m23, a23 = [], []
        for b2, b3 in ((1, 1), (10, 11)):
            m23 += igual_trozo(B2, b2, B3, b3 + 1) + igual_trozo(B2, b2, B3, b3 + 4)
            m23 += [(B2(b2 + 1, 0), B3(b3, 0)), (B2(b2 + 3, 0), B3(b3 + 3, 0)), (B2(b2 + 5, 0), B3(b3 + 6, 0))]
            m23 += [(B2(b2 + 2, k), B3(b3 + 2, k + 1)) for k in range(3)] + [(B2(b2 + 4, k), B3(b3 + 5, k + 1)) for k in range(3)]
            a23 += [B3(t, k) for t in (b3 + 2, b3 + 5) for k in (0, 4)]
        # B3 -> B4 (asociativa y conmutativa de la suma: los sumandos se reordenan en dos sumas)
        m34 = sum([igual_trozo(B3, o, B4, d) for o, d in ((2, 2), (3, 3), (5, 12), (6, 13), (12, 7), (13, 8), (15, 17), (16, 18),
                                                          (9, 5), (9, 15))], [])
        m34 += [(B3(8, 0), B4(4, 0)), (B3(10, 0), B4(6, 0)), (B3(4, 0), B4(14, 0)), (B3(14, 0), B4(16, 0)),
                (B3(1, 0), B4(1, 0)), (B3(7, 0), B4(9, 0)), (B3(11, 0), B4(11, 0)), (B3(17, 0), B4(19, 0))]
        a34 = [B4(10, 0)]
        # B4 -> B5 (definición del producto punto, de derecha a izquierda)
        m45 = [(B4(2, 1), B5(1, 0)), (B4(7, 1), B5(1, 0)), (B4(3, 1), B5(3, 0)), (B4(8, 1), B5(3, 0)), (B4(10, 0), B5(4, 0)),
               (B4(12, 1), B5(5, 0)), (B4(17, 1), B5(5, 0)), (B4(13, 1), B5(7, 0)), (B4(18, 1), B5(7, 0))]
        a45 = [B5(2, 0), B5(6, 0)]
        
        with self.voiceover(text=tr("""Ahora, la suma en el segundo vector. <bookmark mark='e'/> Queremos demostrar que el producto punto se distribuye en ella.""",
                                    """Now, the sum in the second vector. <bookmark mark='e'/> We want to prove that the dot product distributes over it.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("e")
            self.play(FadeIn(E.tex), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Esta vez contamos con las definiciones <bookmark mark='d1'/> del producto punto <bookmark mark='d2'/> y de la suma, <bookmark mark='r6'/> con la distributiva <bookmark mark='r12'/> y con las propiedades conmutativa y asociativa de la suma de números.""",
                                    """This time we can use the definitions <bookmark mark='d1'/> of the dot product <bookmark mark='d2'/> and of addition, <bookmark mark='r6'/> the distributive property <bookmark mark='r12'/> and the commutative and associative properties of the addition of numbers.""")) as tracker:
            self.play(FadeIn(panel.todo), run_time=0.8)
            for marca, claves in (("d1", ["punto"]), ("d2", ["suma"]), ("r6", [6]), ("r12", [1, 2])):
                self.wait_until_bookmark(marca)
                self.play(*[panel.enciende(c) for c in claves])
        self.wait(0.8)
        
        self.pausa_para_pensar(invitacion=tr(r"Demuestre que $\Vect{x}\cdot(\Vect{y}+\Vect{z})=\Vect{x}\cdot\Vect{y}+\Vect{x}\cdot\Vect{z}$.",
                                             r"Prove that $\Vect{x}\cdot(\Vect{y}+\Vect{z})=\Vect{x}\cdot\Vect{y}+\Vect{x}\cdot\Vect{z}$."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que el producto punto se distribuye en la suma.",
                                                 "Pause the video and try to prove that the dot product distributes over the sum."),
                               al_invitar=lambda: panel.pista("punto", "suma", 6, 1, 2))
        panel.quita_pista()
        
        with self.voiceover(text=tr("""Partimos otra vez del lado izquierdo. <bookmark mark='k'/> Por la definición del producto punto <bookmark mark='l1'/> podemos escribirlo como una suma de productos de componentes.""",
                                    """Again we start from the left-hand side. <bookmark mark='k'/> By the definition of the dot product <bookmark mark='l1'/> we can write it as a sum of products of components.""")) as tracker:
            self.play(*[TransformFromCopy(E.g[i], B0.g[i]) for i in range(7)], run_time=1.0)
            entera(self, B0)
            self.wait_until_bookmark("k")
            paso(self, panel, ["punto"], B0, B1, [], m01, a01, marca="l1", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Por la definición de suma <bookmark mark='l2'/> podemos distribuir el selector.""",
                                    """By the definition of addition <bookmark mark='l2'/> we can distribute the selector.""")) as tracker:
            paso(self, panel, ["suma"], B1, B2, f12, m12, marca="l2", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Ya todo son números reales. <bookmark mark='k'/> Por la distributiva <bookmark mark='l3'/> podemos repartir el primer factor entre los dos sumandos.""",
                                    """Now everything is a real number. <bookmark mark='k'/> By the distributive property <bookmark mark='l3'/> we can share out the first factor between the two terms.""")) as tracker:
            self.wait_until_bookmark("k")
            paso(self, panel, [6], B2, B3, f23, m23, a23, marca="l3", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Por las propiedades conmutativa y asociativa de la suma <bookmark mark='l4'/> podemos reordenar los sumandos y agruparlos en dos sumas.""",
                                    """By the commutative and associative properties of addition <bookmark mark='l4'/> we can reorder the terms and group them into two sums.""")) as tracker:
            paso(self, panel, [1, 2], B3, B4, [], m34, a34, marca="l4", t_moviles=1.6)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Y por la definición del producto punto, <bookmark mark='l5'/> cada una de esas sumas es un producto punto.""",
                                    """And by the definition of the dot product, <bookmark mark='l5'/> each of those sums is a dot product.""")) as tracker:
            paso(self, panel, ["punto"], B4, B5, [], m45, a45, marca="l5", t_moviles=1.2)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Así pues, el producto punto se distribuye en la suma.""",
                                    """So the dot product distributes over the sum.""")) as tracker:
            self.play(Indicate(B0.tex, color=COLOR_ESCALAR), Indicate(B5.tex, color=COLOR_ESCALAR),
                      Create(marco(E.tex)), run_time=1.4)
        self.wait(1.0)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("El otro vector", "The other vector"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        C = Linea([VX, PUNTO, "(", LAM, VY, ")",  "=",  "(", LAM, VY, ")", PUNTO, VX,  "=",  LAM, "(", VY, PUNTO, VX, ")",
                   "=",  LAM, "(", VX, PUNTO, VY, ")"], 42)
        D = Linea(["(", VX, "+", VY, ")", PUNTO, VZ,  "=",  VZ, PUNTO, "(", VX, "+", VY, ")",  "=",  VZ, PUNTO, VX, "+", VZ, PUNTO, VY,
                   "=",  VX, PUNTO, VZ, "+", VY, PUNTO, VZ], 42)
        C.tex.move_to([0, 1.3, 0]); D.tex.move_to([0, -0.4, 0])
        # todos los trozos de C y D son de un glifo: L.ini[t] es el glifo del trozo t. Bajo cada igual, de dónde sale el paso
        def rotulos(L, iguales, centro):
            rs = [Tex(t, font_size=26).set_color(c) for t, c in ((tr("simetría", "symmetry"), COLOR_REGLA), (centro, COLOR_ESCALAR),
                                                                 (tr("simetría", "symmetry"), COLOR_REGLA))]
            for r_, t in zip(rs, iguales):
                r_.next_to(L.g[L.ini[t]], DOWN, buff=0.35)
            return rs
        
        
        rot_c = rotulos(C, (6, 13, 20), tr("el escalar sale", "the scalar comes out"))
        rot_d = rotulos(D, (7, 15, 23), tr("se distribuye", "it distributes"))
        F = Linea([VX, PUNTO, "(", LAM, VY, ")", "=", LAM, "(", VX, PUNTO, VY, ")", "=", "(", LAM, VX, ")", PUNTO, VY], 44)
        F.tex.move_to([0, -2.4, 0])
        
        with self.voiceover(text=tr("""Las otras dos igualdades salen de la simetría: el producto punto no depende del orden de los dos vectores.""",
                                    """The other two equalities follow from symmetry: the dot product does not depend on the order of the two vectors.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Si el escalar está en el segundo vector, <bookmark mark='s1'/> por la simetría podemos cambiar el orden de los vectores. <bookmark mark='s2'/> Ahora el escalar está en el primero, así que sale del producto punto. <bookmark mark='s3'/> Y por la simetría otra vez, volvemos al orden de partida.""",
                                    """If the scalar is in the second vector, <bookmark mark='s1'/> by symmetry we can change the order of the vectors. <bookmark mark='s2'/> Now the scalar is in the first one, so it comes out of the dot product. <bookmark mark='s3'/> And by symmetry again, we go back to the original order.""")) as tracker:
            self.play(*[FadeIn(C.g[i]) for t in range(6) for i in C(t)], run_time=0.8)
            # simetría: (λy) y x cambian de sitio
            nace_l(self, C, C, [], [(C.ini[2 + k], C.ini[7 + k]) for k in range(4)] + [(C.ini[1], C.ini[11]), (C.ini[0], C.ini[12])],
                   tramo=(6, 12), marca="s1", extra=[FadeIn(rot_c[0])], t_moviles=1.1)
            # el escalar sale: el «(» pasa detrás del escalar y el «)» detrás de x
            nace_l(self, C, C, [], [(C.ini[7], C.ini[15]), (C.ini[8], C.ini[14]), (C.ini[9], C.ini[16]), (C.ini[10], C.ini[19]),
                                   (C.ini[11], C.ini[17]), (C.ini[12], C.ini[18])],
                   tramo=(13, 19), marca="s2", extra=[FadeIn(rot_c[1])], t_moviles=1.1)
            # simetría: y y x cambian de sitio dentro de los paréntesis
            nace_l(self, C, C, [(C.ini[14], C.ini[21]), (C.ini[15], C.ini[22]), (C.ini[17], C.ini[24]), (C.ini[19], C.ini[26])],
                   [(C.ini[16], C.ini[25]), (C.ini[18], C.ini[23])], tramo=(20, 26), marca="s3", extra=[FadeIn(rot_c[2])], t_moviles=1.0)
            entera(self, C)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Con la suma en el primer vector se hace lo mismo: <bookmark mark='s1'/> la simetría, <bookmark mark='s2'/> la suma en el segundo vector, que ya hemos demostrado, <bookmark mark='s3'/> y otra vez la simetría.""",
                                    """With the sum in the first vector we do the same: <bookmark mark='s1'/> symmetry, <bookmark mark='s2'/> the sum in the second vector, which we have already proved, <bookmark mark='s3'/> and symmetry again.""")) as tracker:
            self.play(*[FadeIn(D.g[i]) for t in range(7) for i in D(t)], run_time=0.8)
            nace_l(self, D, D, [], [(D.ini[k], D.ini[10 + k]) for k in range(5)] + [(D.ini[5], D.ini[9]), (D.ini[6], D.ini[8])],
                   tramo=(7, 14), marca="s1", extra=[FadeIn(rot_d[0])], t_moviles=1.1)
            nace_l(self, D, D, [], [(D.ini[8], D.ini[16]), (D.ini[8], D.ini[20]), (D.ini[9], D.ini[17]), (D.ini[9], D.ini[21]),
                                   (D.ini[11], D.ini[18]), (D.ini[12], D.ini[19]), (D.ini[13], D.ini[22])],
                   tramo=(15, 22), marca="s2", extra=[FadeIn(rot_d[1])], t_moviles=1.1)
            nace_l(self, D, D, [(D.ini[19], D.ini[27])],
                   [(D.ini[18], D.ini[24]), (D.ini[17], D.ini[25]), (D.ini[16], D.ini[26]),
                    (D.ini[22], D.ini[28]), (D.ini[21], D.ini[29]), (D.ini[20], D.ini[30])],
                   tramo=(23, 30), marca="s3", extra=[FadeIn(rot_d[2])], t_moviles=1.0)
            entera(self, D)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Así pues, el producto punto es lineal en sus dos argumentos. <bookmark mark='e'/> En particular, un escalar puede salir de cualquiera de los dos vectores.""",
                                    """So the dot product is linear in both arguments. <bookmark mark='e'/> In particular, a scalar can come out of either of the two vectors.""")) as tracker:
            self.wait_until_bookmark("e")
            self.play(*[TransformFromCopy(C.g[i], F.g[i]) for i in range(6)], run_time=0.8)
            self.play(FadeIn(F.g[F.ini[6]]), *[TransformFromCopy(C.g[C.ini[20 + k]], F.g[F.ini[6 + k]]) for k in range(1, 7)], run_time=0.8)
            self.play(*[FadeIn(F.g[F.ini[t]]) for t in range(13, 20)], run_time=0.8)
            entera(self, F)
        self.wait(1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Tres vectores", "Three vectors"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        VA, VB, VC = r"\Vect{a}", r"\Vect{b}", r"\Vect{c}"
        a, b, c = vector_col(A3_EJ, COLOR_A), vector_col(B3_EJ, COLOR_B), vector_col(C3_EJ, COLOR_C)
        na, nb, nc = con_nombre(VA + "=", a), con_nombre(VB + "=", b), con_nombre(VC + "=", c)
        for n_, col in ((na, COLOR_A), (nb, COLOR_B), (nc, COLOR_C)):
            n_[0].set_color(col)
        VGroup(na, nb, nc).arrange(RIGHT, buff=1.4).move_to([0, 1.6, 0])
        COL = {VA: COLOR_A, VB: COLOR_B, VC: COLOR_C}
        
        
        def cuenta(trozos, resultado, y):
            m = MathTex(*trozos, tex_template=myTemplate, font_size=44)
            for k, t in enumerate(trozos):
                m[k].set_color(COL.get(t, WHITE))
            v = vector_col(resultado, escala=0.7)
            return VGroup(m, v).arrange(RIGHT, buff=0.2).move_to([0, y, 0])
        
        
        uno = cuenta(["(", VA, PUNTO, VB, ")", VC, "=", "2", VC, "="], [0, 2], -0.3)
        dos = cuenta([VA, "(", VB, PUNTO, VC, ")", "=", VA, "3", "="], [3, 0], -1.75)
        dos.shift((uno[0][6].get_x() - dos[0][6].get_x())*RIGHT)   # los iguales, en columna
        distintos = MathTex(r"(\Vect{a}\cdot\Vect{b})\Vect{c}\neq\Vect{a}(\Vect{b}\cdot\Vect{c})", tex_template=myTemplate, font_size=44)
        nota = Tex(tr("en general", "in general"), font_size=30).set_color(GRAY_A)
        VGroup(distintos, nota).arrange(RIGHT, buff=0.4).move_to([0, -3.05, 0])
        u, d_ = uno[0], dos[0]
        
        with self.voiceover(text=tr("""Un escalar sale del producto punto. Podría parecer que con un tercer vector ocurre lo mismo, pero no es así. <bookmark mark='t'/> Tomemos estos tres vectores.""",
                                    """A scalar comes out of the dot product. It might seem that the same happens with a third vector, but it does not. <bookmark mark='t'/> Take these three vectors.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("t")
            self.play(FadeIn(na), FadeIn(nb), FadeIn(nc), run_time=0.8)
        self.wait(0.6)
        
        with self.voiceover(text=tr("""Si calculamos primero el producto punto del vector a por b, <bookmark mark='ab'/> obtenemos dos, <bookmark mark='c'/> y dos por c es este vector.""",
                                    """If we first compute the dot product of the vector 'a' and b, <bookmark mark='ab'/> we get two, <bookmark mark='c'/> and two times c is this vector.""")) as tracker:
            self.play(*[FadeIn(u[k]) for k in range(5)], run_time=0.6)
            self.wait_until_bookmark("ab")
            self.play(FadeIn(u[5]), FadeIn(u[6]), TransformFromCopy(VGroup(*u[0:5]), u[7]), run_time=0.7)
            self.wait_until_bookmark("c")
            self.play(TransformFromCopy(u[5], u[8]), run_time=0.4)
            self.play(FadeIn(u[9]), FadeIn(uno[1]), run_time=0.6)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Si calculamos primero el de b por c, <bookmark mark='bc'/> obtenemos tres, <bookmark mark='a'/> y el producto del vector a por tres es este otro.""",
                                    """If we first compute the one of b and c, <bookmark mark='bc'/> we get three, <bookmark mark='a'/> and the product of the vector 'a' and three is this other one.""")) as tracker:
            self.play(*[FadeIn(d_[k]) for k in range(1, 6)], run_time=0.6)
            self.wait_until_bookmark("bc")
            self.play(FadeIn(d_[0]), FadeIn(d_[6]), TransformFromCopy(VGroup(*d_[1:6]), d_[8]), run_time=0.7)
            self.wait_until_bookmark("a")
            self.play(TransformFromCopy(d_[0], d_[7]), run_time=0.4)
            self.play(FadeIn(d_[9]), FadeIn(dos[1]), run_time=0.6)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Son vectores distintos: <bookmark mark='u'/> el primero se obtiene multiplicando c por un número, <bookmark mark='d'/> y el segundo, multiplicando el vector a por otro.""",
                                    """They are different vectors: <bookmark mark='u'/> the first is obtained by multiplying c by a number, <bookmark mark='d'/> and the second by multiplying the vector 'a' by another.""")) as tracker:
            self.wait_until_bookmark("u")
            resalta(self, [u[7], u[8]], factor=1.25)
            self.wait_until_bookmark("d")
            apaga(self, [u[7]], factor=1.25); apaga(self, [u[8]], color=COLOR_C, factor=1.25)
            resalta(self, [d_[7], d_[8]], factor=1.25)
        self.wait(0.8)
        apaga(self, [d_[7]], color=COLOR_A, factor=1.25); apaga(self, [d_[8]], factor=1.25)
        
        with self.voiceover(text=tr("""Así que con tres vectores no hay un único producto punto, <bookmark mark='p'/> y los paréntesis no se pueden quitar: indican el producto punto que se calcula primero.""",
                                    """So with three vectors there is no single dot product, <bookmark mark='p'/> and the parentheses cannot be removed: they show which dot product is computed first.""")) as tracker:
            self.play(FadeIn(distintos), FadeIn(nota), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(*[Indicate(distintos[0][k], color=COLOR_ESCALAR, scale_factor=1.6) for k in (0, 4, -5, -1)], run_time=1.2)   # los paréntesis (≠ puede ser de dos glifos)
        self.wait(1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [r"(\Vect{x}+\Vect{y})\cdot\Vect{z}=\Vect{x}\cdot\Vect{z}+\Vect{y}\cdot\Vect{z},\qquad \Vect{x}\cdot(\Vect{y}+\Vect{z})=\Vect{x}\cdot\Vect{y}+\Vect{x}\cdot\Vect{z}",
                    r"(\lambda\Vect{x})\cdot\Vect{y}=\lambda(\Vect{x}\cdot\Vect{y})=\Vect{x}\cdot(\lambda\Vect{y})",
                    r"(\Vect{a}\cdot\Vect{b})\Vect{c}\neq\Vect{a}(\Vect{b}\cdot\Vect{c})"]
        rotulos = [tr("se distribuye en las sumas", "it distributes over sums"),
                   tr("un escalar sale de cualquiera de los dos vectores", "a scalar comes out of either vector"),
                   tr("con tres vectores, los paréntesis no se quitan", "with three vectors, the parentheses stay")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=38), Tex(r, font_size=32, color=GRAY_A)).arrange(DOWN, buff=0.15)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.45)
        # «lineal en sus dos argumentos» encima de las dos primeras filas, en horizontal (vertical no se lee en un móvil)
        lineal = Tex(tr("Lineal en sus dos argumentos", "Linear in both arguments"), font_size=34).set_color(COLOR_ESCALAR)
        VGroup(lineal, filas).arrange(DOWN, buff=0.3).next_to(cabecera, DOWN, buff=0.4)
        llave = Brace(VGroup(filas[0], filas[1]), LEFT, color=COLOR_ESCALAR)
        
        with self.voiceover(text=tr("""Resumamos. El producto punto es lineal en sus dos argumentos: <bookmark mark='s'/> se distribuye en las sumas <bookmark mark='p'/> y un escalar puede salir de cualquiera de los dos vectores.""",
                                    """Let us sum up. The dot product is linear in both arguments: <bookmark mark='s'/> it distributes over sums <bookmark mark='p'/> and a scalar can come out of either of the two vectors.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.play(FadeIn(lineal), run_time=0.6)
            self.wait_until_bookmark("s")
            self.play(FadeIn(filas[0]), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(FadeIn(filas[1]), run_time=0.8)
            self.play(GrowFromCenter(llave), run_time=0.5)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Con tres vectores, en cambio, los paréntesis no se pueden quitar.""",
                                    """With three vectors, on the other hand, the parentheses cannot be removed.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos las combinaciones lineales de vectores.""",
                                    """In the next video we will see linear combinations of vectors.""")) as tracker:
            pass
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos_finales()


class L02_V02_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

class L02_V02_E01_Compra(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        VQ, VR, VP = r"\Vect{q}", r"\Vect{r}", r"\Vect{p}"
        q, r, qr, p = vector_col(Q_EJ, COLOR_A), vector_col(R_EJ, COLOR_C), vector_col(QR_EJ), vector_col(P_EJ, COLOR_B)
        nq, nr, nqr, np_ = con_nombre(VQ + "=", q), con_nombre(VR + "=", r), con_nombre(VQ + "+" + VR + "=", qr), con_nombre(VP + "=", p)
        nq[0].set_color(COLOR_A); nr[0].set_color(COLOR_C); np_[0].set_color(COLOR_B)
        nqr[0][0][0].set_color(COLOR_A); nqr[0][0][2].set_color(COLOR_C)
        fila = VGroup(nq, nr, nqr, np_).arrange(RIGHT, buff=0.55).move_to([0.9, 1.15, 0])
        ley = leyenda([tr("patatas (kilos)", "potatoes (kilos)"), tr("huevos (docenas)", "eggs (dozens)"), tr("aceite (litros)", "oil (litres)")],
                      q, nq.get_left()[0] - 0.3, font_size=26)
        rot = [Tex(t, font_size=26).set_color(c).next_to(v, UP, buff=0.22) for t, c, v in
               ((tr("sábado", "Saturday"), COLOR_A, q), (tr("domingo", "Sunday"), COLOR_C, r), (tr("precios (euros)", "prices (euros)"), COLOR_B, p))]
        for x in rot[1:]:
            x.align_to(rot[0], DOWN)
        
        
        def cuenta(trozos, y):
            m = MathTex(*trozos, tex_template=myTemplate, font_size=42).move_to([0, y, 0])
            for k, t in enumerate(trozos):
                m[k].set_color({VQ: COLOR_A, VR: COLOR_C, VP: COLOR_B}.get(t, WHITE))
            return m
        
        
        cq = cuenta([VQ, PUNTO, VP, "=", "15"], -1.0)
        cr = cuenta([VR, PUNTO, VP, "=", "8"], -1.75)
        cqr = cuenta(["(", VQ, "+", VR, ")", PUNTO, VP, "=", "23", "=", "15", "+", "8"], -2.6)
        for c_ in (cr, cqr):   # los iguales, en columna
            c_.shift((cq[3].get_x() - c_[3 if c_ is cr else 7].get_x())*RIGHT)
        c2q = cuenta(["(", "2", VQ, ")", PUNTO, VP, "=", "30", "=", "2", PUNTO, "15"], -1.75)
        c2q.shift((cq[3].get_x() - c2q[6].get_x())*RIGHT)
        dosq = vector_col(DOS_Q, COLOR_A)
        ndosq = con_nombre(r"2" + VQ + "=", dosq); ndosq[0][0][1].set_color(COLOR_A)
        ndosq.move_to(nr).align_to(nr, LEFT)
        om = omega("normal", mira=UL).to_corner(DR, buff=0.4)
        
        with self.voiceover(text=tr("""En este vídeo veremos las propiedades del producto punto con la suma de vectores y con el producto por un escalar.""",
                                    """In this video we will see the properties of the dot product with vector addition and with scalar multiplication.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        self.wait(0.8)   # respiro tras el arranque
        
        with self.voiceover(text=tr("""Omega y sus amigos hacen la compra dos días seguidos. <bookmark mark='q'/> El sábado compran esta cesta, <bookmark mark='r'/> y el domingo, esta otra. <bookmark mark='p'/> Los precios no cambian.""",
                                    """Omega and friends do the shopping on two days in a row. <bookmark mark='q'/> On Saturday they buy this basket, <bookmark mark='r'/> and on Sunday, this other one. <bookmark mark='p'/> The prices do not change.""")) as tracker:
            entra(self, om)
            self.wait_until_bookmark("q")
            self.play(FadeIn(ley), FadeIn(nq), FadeIn(rot[0]), run_time=0.8)
            self.wait_until_bookmark("r")
            self.play(FadeIn(nr), FadeIn(rot[1]), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(FadeIn(np_), FadeIn(rot[2]), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""El coste de una compra es el producto punto de la cesta por los precios: cada cantidad se multiplica por su precio, y se suman los resultados. <bookmark mark='c1'/> El sábado gastan quince euros, <bookmark mark='c2'/> y el domingo, ocho.""",
                                    """The cost of a purchase is the dot product of the basket and the prices: each quantity is multiplied by its price, and the results are added. <bookmark mark='c1'/> On Saturday they spend fifteen euros, <bookmark mark='c2'/> and on Sunday, eight.""")) as tracker:
            self.wait_until_bookmark("c1")
            self.play(TransformFromCopy(nq[0][0][0], cq[0]), TransformFromCopy(np_[0][0][0], cq[2]), FadeIn(cq[1]), run_time=0.6)
            self.play(FadeIn(cq[3]), FadeIn(cq[4]), run_time=0.4)
            self.wait_until_bookmark("c2")
            self.play(TransformFromCopy(nr[0][0][0], cr[0]), TransformFromCopy(np_[0][0][0], cr[2]), FadeIn(cr[1]), run_time=0.6)
            self.play(FadeIn(cr[3]), FadeIn(cr[4]), run_time=0.4)
        self.wait(1.0)
        
        # la cesta total nace de las dos (cada componente, de las dos de su fila); su coste, de la suma y los precios
        with self.voiceover(text=tr("""Si hubieran comprado todo de una vez, <bookmark mark='s'/> la cesta sería la suma de las dos, <bookmark mark='t'/> y su coste, veintitrés euros: <bookmark mark='u'/> lo mismo que la suma de los dos costes.""",
                                    """Had they bought everything at once, <bookmark mark='s'/> the basket would be the sum of the two, <bookmark mark='t'/> and its cost, twenty-three euros: <bookmark mark='u'/> the same as the sum of the two costs.""")) as tracker:
            self.wait_until_bookmark("s")
            eq_, er_, eqr = q.get_entries(), r.get_entries(), qr.get_entries()
            self.play(FadeIn(nqr[0]), FadeIn(qr.get_brackets()),
                      *[TransformFromCopy(VGroup(eq_[k], er_[k]), eqr[k]) for k in range(3)], run_time=1.0)
            self.wait_until_bookmark("t")
            self.play(*[FadeIn(cqr[k]) for k in range(7)], run_time=0.6)
            self.play(FadeIn(cqr[7]), FadeIn(cqr[8]), run_time=0.4)
            cambia(self, om, "alegria")
            self.wait_until_bookmark("u")
            self.play(FadeIn(cqr[9]), TransformFromCopy(cq[4], cqr[10]), FadeIn(cqr[11]), TransformFromCopy(cr[4], cqr[12]), run_time=0.8)
            cambia(self, om, "normal", mira=UL)   # la alegría dura un instante
        self.wait(1.0)
        
        # la cantinela de V14: en cada verbo, la operación que nombra
        with self.voiceover(text=tr("""Da igual <bookmark mark='a1'/> sumar primero las cestas y <bookmark mark='a2'/> calcular después el coste, que <bookmark mark='a3'/> calcular primero los costes y <bookmark mark='a4'/> sumarlos después.""",
                                    """It makes no difference whether we <bookmark mark='a1'/> add the baskets first and <bookmark mark='a2'/> work out the cost afterwards, or <bookmark mark='a3'/> work out the costs first and <bookmark mark='a4'/> add them afterwards.""")) as tracker:
            previo = []
            for marca, mobs in (("a1", [cqr[2]]), ("a2", [cqr[5]]), ("a3", [cq[1], cr[1]]), ("a4", [cqr[11]])):
                self.wait_until_bookmark(marca)
                self.play(*[x.animate.set_color(WHITE).scale(1/1.6) for x in previo],
                          *[x.animate.set_color(COLOR_ESCALAR).scale(1.6) for x in mobs], run_time=0.25)
                previo = mobs
            self.wait(0.6)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.6) for x in previo], run_time=0.25)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Ahora, si la cena del sábado fuera para el doble de invitados, <bookmark mark='d'/> comprarían el doble de cada ingrediente, <bookmark mark='e'/> y el coste también sería el doble: treinta euros.""",
                                    """Now, if Saturday's dinner were for twice as many guests, <bookmark mark='d'/> they would buy twice as much of each ingredient, <bookmark mark='e'/> and the cost would be twice as much too: thirty euros.""")) as tracker:
            self.play(*[FadeOut(x) for x in (nr, rot[1], nqr, cr, cqr)], run_time=0.6)
            self.wait_until_bookmark("d")
            edq = dosq.get_entries()
            self.play(FadeIn(ndosq[0]), FadeIn(dosq.get_brackets()),
                      *[TransformFromCopy(q.get_entries()[k], edq[k]) for k in range(3)], run_time=1.0)
            self.wait_until_bookmark("e")
            self.play(*[FadeIn(c2q[k]) for k in range(6)], run_time=0.6)
            self.play(FadeIn(c2q[6]), FadeIn(c2q[7]), run_time=0.4)
            self.play(FadeIn(c2q[8]), FadeIn(c2q[9]), FadeIn(c2q[10]), TransformFromCopy(cq[4], c2q[11]), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Da igual <bookmark mark='b1'/> multiplicar primero la cesta por dos y <bookmark mark='b2'/> calcular después el coste, que <bookmark mark='b3'/> calcular primero el coste y <bookmark mark='b4'/> multiplicarlo después por dos.""",
                                    """It makes no difference whether we <bookmark mark='b1'/> multiply the basket by two first and <bookmark mark='b2'/> work out the cost afterwards, or <bookmark mark='b3'/> work out the cost first and <bookmark mark='b4'/> multiply it by two afterwards.""")) as tracker:
            previo = []
            for marca, mobs in (("b1", [c2q[1]]), ("b2", [c2q[4]]), ("b3", [cq[1]]), ("b4", [c2q[9]])):
                self.wait_until_bookmark(marca)
                self.play(*[x.animate.set_color(WHITE).scale(1/1.6) for x in previo],
                          *[x.animate.set_color(COLOR_ESCALAR).scale(1.6) for x in mobs], run_time=0.25)
                previo = mobs
            self.wait(0.6)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.6) for x in previo], run_time=0.25)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Este ejemplo solo lo ilustra. <bookmark mark='e'/> Vamos a demostrar que estas dos igualdades valen para vectores cualesquiera.""",
                                    """This example only illustrates it. <bookmark mark='e'/> We are going to prove that these two equalities hold for any vectors.""")) as tracker:
            self.wait_until_bookmark("e")
            self.play(Indicate(c2q, color=COLOR_ESCALAR, scale_factor=1.06), Indicate(cq, color=COLOR_ESCALAR, scale_factor=1.06), run_time=1.2)
        self.wait(0.6)
        
        self.pausa_media()

class L02_V02_E02_Lineal(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Lineal en un argumento", "Linear in one argument"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        I1S = Linea(["(", VX, "+", VY, ")", PUNTO, VZ, "=", VX, PUNTO, VZ, "+", VY, PUNTO, VZ], 40).tex
        I1E = Linea(["(", LAM, VX, ")", PUNTO, VY, "=", LAM, "(", VX, PUNTO, VY, ")"], 40).tex
        I2S = Linea([VX, PUNTO, "(", VY, "+", VZ, ")", "=", VX, PUNTO, VY, "+", VX, PUNTO, VZ], 40).tex
        I2E = Linea([VX, PUNTO, "(", LAM, VY, ")", "=", LAM, "(", VX, PUNTO, VY, ")"], 40).tex
        col1 = VGroup(I1S, I1E).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([-3.4, -0.2, 0])
        col2 = VGroup(I2S, I2E).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([3.4, -0.2, 0])
        r1 = Tex(tr(r"lineal en el\\ primer argumento", r"linear in the\\ first argument"), font_size=32).set_color(GRAY_A).next_to(col1, UP, buff=0.55)
        r2 = Tex(tr(r"lineal en el\\ segundo argumento", r"linear in the\\ second argument"), font_size=32).set_color(GRAY_A).next_to(col2, UP, buff=0.55)
        r2.align_to(r1, UP)
        fijo1 = Tex(tr(r"$\Vect{z}$ fijo", r"$\Vect{z}$ fixed"), tex_template=myTemplate, font_size=28).set_color(COLOR_C).next_to(col1, DOWN, buff=0.45)
        fijo2 = Tex(tr(r"$\Vect{x}$ fijo", r"$\Vect{x}$ fixed"), tex_template=myTemplate, font_size=28).set_color(COLOR_A).next_to(col2, DOWN, buff=0.45)
        fijo2.align_to(fijo1, UP)
        
        with self.voiceover(text=tr("""En el ejemplo, los precios estaban fijos y cambiaba la cesta. <bookmark mark='s'/> Con el segundo vector fijo, el producto punto se distribuye en las sumas <bookmark mark='p'/> y es asociativo con el producto por un escalar.""",
                                    """In the example, the prices were fixed and the basket changed. <bookmark mark='s'/> With the second vector fixed, the dot product distributes over sums <bookmark mark='p'/> and is associative with scalar multiplication.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.play(FadeIn(fijo1), run_time=0.5)
            self.wait_until_bookmark("s")
            self.play(FadeIn(I1S), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(FadeIn(I1E), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Por eso se dice que es lineal en el primer argumento, <bookmark mark='v'/> es decir, en el primer vector.""",
                                    """That is why we say that it is linear in the first argument, <bookmark mark='v'/> that is, in the first vector.""")) as tracker:
            self.play(FadeIn(r1), run_time=0.6)
            self.wait_until_bookmark("v")
            primeros = [I1S[0][0:5], I1E[0][0:4]]   # (x+y) y (λx): el primer vector de cada igualdad
            resalta(self, primeros, factor=1.15)
        self.wait(0.8)
        apaga(self, primeros, factor=1.15)
        for g in (I1S[0][1], I1E[0][2]):
            g.set_color(COLOR_A)
        I1S[0][3].set_color(COLOR_B); I1E[0][1].set_color(COLOR_LAMBDA)
        
        with self.voiceover(text=tr("""Del mismo modo, <bookmark mark='f'/> con el primer vector fijo, <bookmark mark='l'/> es lineal en el segundo argumento.""",
                                    """In the same way, <bookmark mark='f'/> with the first vector fixed, <bookmark mark='l'/> it is linear in the second argument.""")) as tracker:
            self.wait_until_bookmark("f")
            self.play(FadeIn(fijo2), run_time=0.5)
            self.wait_until_bookmark("l")
            self.play(FadeIn(r2), FadeIn(I2S), FadeIn(I2E), run_time=1.0)
        self.wait(1.2)
        
        with self.voiceover(text=tr("""Vamos a demostrar dos de estas igualdades con las definiciones: <bookmark mark='a'/> la del escalar en el primer vector <bookmark mark='b'/> y la de la suma en el segundo. <bookmark mark='c'/> Las otras dos saldrán de la simetría del producto punto.""",
                                    """We are going to prove two of these equalities from the definitions: <bookmark mark='a'/> the one with the scalar in the first vector <bookmark mark='b'/> and the one with the sum in the second. <bookmark mark='c'/> The other two will follow from the symmetry of the dot product.""")) as tracker:
            self.wait_until_bookmark("a")
            ca = marco(I1E)
            self.play(Create(ca), run_time=0.4)
            self.wait_until_bookmark("b")
            cb = marco(I2S)
            self.play(Create(cb), run_time=0.4)
            self.wait_until_bookmark("c")
            cs = [marco(I1S, COLOR_REGLA), marco(I2E, COLOR_REGLA)]
            self.play(*[Create(x) for x in cs], run_time=0.5)
        self.wait(1.2)
        
        self.pausa_media()

class L02_V02_E03_Escalar(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("El escalar en el primer vector", "The scalar in the first vector"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        panel = Panel(self, ["punto", "producto"], [6, 7])
        E = Linea(["(", LAM, VX, ")", PUNTO, VY, "=", LAM, "(", VX, PUNTO, VY, ")"], 42)
        E.tex.move_to([0, 1.0, 0])
        A0 = Linea(["(", LAM, VX, ")", PUNTO, VY])
        A1 = Linea(["=", PL(1), Y(1), "+", CD, "+", PL("n"), Y("n")])
        A2 = Linea(["=", "(", LAM, X(1), ")", Y(1), "+", CD, "+", "(", LAM, X("n"), ")", Y("n")])
        A3 = Linea(["=", LAM, "(", X(1), Y(1), ")", "+", CD, "+", LAM, "(", X("n"), Y("n"), ")"])
        A4 = Linea(["=", LAM, "(", X(1), Y(1), "+", CD, "+", X("n"), Y("n"), ")"])
        A5 = Linea(["=", LAM, "(", VX, PUNTO, VY, ")"])
        cadena = [A0, A1, A2, A3, A4, A5]
        coloca_cadena(cadena)
        for L in (A3, A4):
            L.g[0].set_color(COLOR_REGLA)   # pasos con números reales
        
        # A0 -> A1 (definición del producto punto): (λx) va a cada ((λx)|i) e y a cada (y|i)
        a01 = [A1(p, k) for p in (1, 6) for k in (0, 5, 6, 7)] + [A1(p, k) for p in (2, 7) for k in (0, 2, 3, 4)] + A1(3) + A1(4) + A1(5)
        m01 = [(A0.ini[t], A1(p, t + 1)) for p in (1, 6) for t in range(4)] + [(A0.ini[5], A1(p, 1)) for p in (2, 7)]
        # A1 -> A2 (definición del producto por un escalar: desplazar los paréntesis)
        f12 = sum([igual_trozo(A1, o, A2, d) for o, d in ((2, 5), (3, 6), (4, 7), (5, 8), (7, 13))], [])
        m12 = []
        for p, b in ((1, 1), (6, 9)):
            m12 += [(A1(p, 0), A2(b, 0)), (A1(p, 1), A2(b + 2, 0)), (A1(p, 2), A2(b + 1, 0)), (A1(p, 3), A2(b + 2, 1)),
                    (A1(p, 4), A2(b + 2, 4)), (A1(p, 5), A2(b + 2, 2)), (A1(p, 6), A2(b + 2, 3)), (A1(p, 7), A2(b + 3, 0))]
        # A2 -> A3 (asociativa: desplazar los paréntesis)
        f23 = sum([igual_trozo(A2, o, A3, d) for o, d in ((3, 3), (5, 4), (6, 6), (7, 7), (8, 8), (11, 11), (13, 12))], [])
        m23 = []
        for b2, b3 in ((1, 1), (9, 9)):
            m23 += [(A2(b2, 0), A3(b3 + 1, 0)), (A2(b2 + 1, 0), A3(b3, 0)), (A2(b2 + 3, 0), A3(b3 + 4, 0))]
        # A3 -> A4 (distributiva: el escalar, factor común)
        f34 = sum([igual_trozo(A3, o, A4, d) for o, d in ((3, 3), (4, 4), (6, 5), (7, 6), (8, 7), (11, 8), (12, 9))], [])
        m34 = [(A3(1, 0), A4(1, 0)), (A3(9, 0), A4(1, 0)), (A3(2, 0), A4(2, 0)), (A3(13, 0), A4(10, 0))]
        # A4 -> A5 (definición del producto punto, de derecha a izquierda)
        f45 = [(A4(1, 0), A5(1, 0)), (A4(2, 0), A5(2, 0)), (A4(10, 0), A5(6, 0))]
        m45 = [(A4(3, 1), A5(3, 0)), (A4(8, 1), A5(3, 0)), (A4(4, 1), A5(5, 0)), (A4(9, 1), A5(5, 0))]
        
        with self.voiceover(text=tr("""Empecemos por el escalar en el primer vector. <bookmark mark='e'/> Queremos demostrar que sale del producto punto.""",
                                    """Let us start with the scalar in the first vector. <bookmark mark='e'/> We want to prove that it comes out of the dot product.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("e")
            self.play(FadeIn(E.tex), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Para demostrarlo contamos con las definiciones <bookmark mark='d1'/> del producto punto <bookmark mark='d2'/> y del producto por un escalar, y con dos propiedades de los números reales: <bookmark mark='r6'/> la distributiva <bookmark mark='r7'/> y la asociativa.""",
                                    """To prove it we can use the definitions <bookmark mark='d1'/> of the dot product <bookmark mark='d2'/> and of scalar multiplication, and two properties of real numbers: <bookmark mark='r6'/> the distributive property <bookmark mark='r7'/> and the associative property.""")) as tracker:
            self.play(FadeIn(panel.todo), run_time=0.8)
            for marca, clave in (("d1", "punto"), ("d2", "producto"), ("r6", 6), ("r7", 7)):
                self.wait_until_bookmark(marca)
                self.play(panel.enciende(clave))
        self.wait(0.8)
        
        self.pausa_para_pensar(invitacion=tr(r"Demuestre que $(\lambda\Vect{x})\cdot\Vect{y}=\lambda(\Vect{x}\cdot\Vect{y})$.",
                                             r"Prove that $(\lambda\Vect{x})\cdot\Vect{y}=\lambda(\Vect{x}\cdot\Vect{y})$."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que el escalar sale del producto punto.",
                                                 "Pause the video and try to prove that the scalar comes out of the dot product."),
                               al_invitar=lambda: panel.pista("punto", "producto", 6, 7))
        panel.quita_pista()
        
        with self.voiceover(text=tr("""Partimos del lado izquierdo. <bookmark mark='k'/> Por la definición del producto punto <bookmark mark='l1'/> podemos escribirlo como una suma de productos de componentes.""",
                                    """We start from the left-hand side. <bookmark mark='k'/> By the definition of the dot product <bookmark mark='l1'/> we can write it as a sum of products of components.""")) as tracker:
            self.play(*[TransformFromCopy(E.g[i], A0.g[i]) for i in range(6)], run_time=1.0)
            entera(self, A0)
            self.wait_until_bookmark("k")
            paso(self, panel, ["punto"], A0, A1, [], m01, a01, marca="l1", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Por la definición del producto por un escalar, <bookmark mark='l2'/> en cada sumando podemos desplazar los paréntesis.""",
                                    """By the definition of scalar multiplication, <bookmark mark='l2'/> in each term we can move the parentheses.""")) as tracker:
            paso(self, panel, ["producto"], A1, A2, f12, m12, marca="l2", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Ya todo son números reales. <bookmark mark='k'/> Por la asociativa <bookmark mark='l3'/> podemos desplazar otra vez los paréntesis.""",
                                    """Now everything is a real number. <bookmark mark='k'/> By the associative property <bookmark mark='l3'/> we can move the parentheses again.""")) as tracker:
            self.wait_until_bookmark("k")
            paso(self, panel, [7], A2, A3, f23, m23, marca="l3", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""El escalar multiplica a todos los sumandos, <bookmark mark='k'/> así que por la distributiva <bookmark mark='l4'/> podemos sacarlo como factor común.""",
                                    """The scalar multiplies every term, <bookmark mark='k'/> so by the distributive property <bookmark mark='l4'/> we can take it out as a common factor.""")) as tracker:
            self.play(*[Indicate(A3.g[A3(t, 0)], color=COLOR_ESCALAR, scale_factor=1.6) for t in (1, 9)], run_time=0.9)
            self.wait_until_bookmark("k")
            paso(self, panel, [6], A3, A4, f34, m34, marca="l4", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Y por la definición del producto punto, <bookmark mark='l5'/> la suma entre paréntesis es el producto punto de x por y.""",
                                    """And by the definition of the dot product, <bookmark mark='l5'/> the sum in parentheses is the dot product of x and y.""")) as tracker:
            paso(self, panel, ["punto"], A4, A5, f45, m45, [A5(4, 0)], marca="l5", t_moviles=1.2)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Así pues, el escalar sale del producto punto.""",
                                    """So the scalar comes out of the dot product.""")) as tracker:
            self.play(Indicate(A0.tex, color=COLOR_ESCALAR), Indicate(A5.tex, color=COLOR_ESCALAR),
                      Create(marco(E.tex)), run_time=1.4)
        self.wait(1.0)
        
        self.pausa_media()

class L02_V02_E04_Suma(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La suma en el segundo vector", "The sum in the second vector"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        panel = Panel(self, ["punto", "suma"], [6, 1, 2])
        E = Linea([VX, PUNTO, "(", VY, "+", VZ, ")", "=", VX, PUNTO, VY, "+", VX, PUNTO, VZ], 42)
        E.tex.move_to([0, 0.95, 0])
        B0 = Linea([VX, PUNTO, "(", VY, "+", VZ, ")"])
        B1 = Linea(["=", X(1), PS(1), "+", CD, "+", X("n"), PS("n")])
        B2 = Linea(["=", X(1), "(", yb(1), "+", zb(1), ")", "+", CD, "+", X("n"), "(", yb("n"), "+", zb("n"), ")"])
        B3 = Linea(["=", "(", X(1), Y(1), "+", X(1), Z(1), ")", "+", CD, "+", "(", X("n"), Y("n"), "+", X("n"), Z("n"), ")"])
        B4 = Linea(["=", "(", X(1), Y(1), "+", CD, "+", X("n"), Y("n"), ")", "+", "(", X(1), Z(1), "+", CD, "+", X("n"), Z("n"), ")"])
        B5 = Linea(["=", VX, PUNTO, VY, "+", VX, PUNTO, VZ])
        cadena = [B0, B1, B2, B3, B4, B5]
        coloca_cadena(cadena, y_sup=0.1)
        for L in (B3, B4):
            L.g[0].set_color(COLOR_REGLA)   # pasos con números reales
        
        # B0 -> B1 (definición del producto punto): x va a cada (x|i) y (y+z) a cada ((y+z)|i)
        m01 = [(B0.ini[0], B1(p, 1)) for p in (1, 6)] + [(B0.ini[2 + k], B1(p, 1 + k)) for p in (2, 7) for k in range(5)]
        a01 = [B1(p, k) for p in (1, 6) for k in (0, 2, 3, 4)] + [B1(p, k) for p in (2, 7) for k in (0, 6, 7, 8)] + B1(3) + B1(4) + B1(5)
        # B1 -> B2 (definición de suma: distribuir el selector; la barra y el índice viajan a los dos sumandos)
        f12 = sum([igual_trozo(B1, o, B2, d) for o, d in ((1, 1), (3, 7), (4, 8), (5, 9), (6, 10))], [])
        m12 = []
        for p, b in ((2, 2), (7, 11)):
            m12 += [(B1(p, 0), B2(b, 0)), (B1(p, 2), B2(b + 1, 0)), (B1(p, 3), B2(b + 2, 0)), (B1(p, 4), B2(b + 3, 0)),
                    (B1(p, 6), B2(b + 1, 1)), (B1(p, 6), B2(b + 3, 1)), (B1(p, 7), B2(b + 1, 2)), (B1(p, 7), B2(b + 3, 2)),
                    (B1(p, 8), B2(b + 4, 0))]
        # B2 -> B3 (distributiva: la componente de x se reparte entre los dos sumandos)
        f23 = sum([igual_trozo(B2, o, B3, d) for o, d in ((7, 8), (8, 9), (9, 10))], [])
        m23, a23 = [], []
        for b2, b3 in ((1, 1), (10, 11)):
            m23 += igual_trozo(B2, b2, B3, b3 + 1) + igual_trozo(B2, b2, B3, b3 + 4)
            m23 += [(B2(b2 + 1, 0), B3(b3, 0)), (B2(b2 + 3, 0), B3(b3 + 3, 0)), (B2(b2 + 5, 0), B3(b3 + 6, 0))]
            m23 += [(B2(b2 + 2, k), B3(b3 + 2, k + 1)) for k in range(3)] + [(B2(b2 + 4, k), B3(b3 + 5, k + 1)) for k in range(3)]
            a23 += [B3(t, k) for t in (b3 + 2, b3 + 5) for k in (0, 4)]
        # B3 -> B4 (asociativa y conmutativa de la suma: los sumandos se reordenan en dos sumas)
        m34 = sum([igual_trozo(B3, o, B4, d) for o, d in ((2, 2), (3, 3), (5, 12), (6, 13), (12, 7), (13, 8), (15, 17), (16, 18),
                                                          (9, 5), (9, 15))], [])
        m34 += [(B3(8, 0), B4(4, 0)), (B3(10, 0), B4(6, 0)), (B3(4, 0), B4(14, 0)), (B3(14, 0), B4(16, 0)),
                (B3(1, 0), B4(1, 0)), (B3(7, 0), B4(9, 0)), (B3(11, 0), B4(11, 0)), (B3(17, 0), B4(19, 0))]
        a34 = [B4(10, 0)]
        # B4 -> B5 (definición del producto punto, de derecha a izquierda)
        m45 = [(B4(2, 1), B5(1, 0)), (B4(7, 1), B5(1, 0)), (B4(3, 1), B5(3, 0)), (B4(8, 1), B5(3, 0)), (B4(10, 0), B5(4, 0)),
               (B4(12, 1), B5(5, 0)), (B4(17, 1), B5(5, 0)), (B4(13, 1), B5(7, 0)), (B4(18, 1), B5(7, 0))]
        a45 = [B5(2, 0), B5(6, 0)]
        
        with self.voiceover(text=tr("""Ahora, la suma en el segundo vector. <bookmark mark='e'/> Queremos demostrar que el producto punto se distribuye en ella.""",
                                    """Now, the sum in the second vector. <bookmark mark='e'/> We want to prove that the dot product distributes over it.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("e")
            self.play(FadeIn(E.tex), run_time=0.8)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Esta vez contamos con las definiciones <bookmark mark='d1'/> del producto punto <bookmark mark='d2'/> y de la suma, <bookmark mark='r6'/> con la distributiva <bookmark mark='r12'/> y con las propiedades conmutativa y asociativa de la suma de números.""",
                                    """This time we can use the definitions <bookmark mark='d1'/> of the dot product <bookmark mark='d2'/> and of addition, <bookmark mark='r6'/> the distributive property <bookmark mark='r12'/> and the commutative and associative properties of the addition of numbers.""")) as tracker:
            self.play(FadeIn(panel.todo), run_time=0.8)
            for marca, claves in (("d1", ["punto"]), ("d2", ["suma"]), ("r6", [6]), ("r12", [1, 2])):
                self.wait_until_bookmark(marca)
                self.play(*[panel.enciende(c) for c in claves])
        self.wait(0.8)
        
        self.pausa_para_pensar(invitacion=tr(r"Demuestre que $\Vect{x}\cdot(\Vect{y}+\Vect{z})=\Vect{x}\cdot\Vect{y}+\Vect{x}\cdot\Vect{z}$.",
                                             r"Prove that $\Vect{x}\cdot(\Vect{y}+\Vect{z})=\Vect{x}\cdot\Vect{y}+\Vect{x}\cdot\Vect{z}$."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que el producto punto se distribuye en la suma.",
                                                 "Pause the video and try to prove that the dot product distributes over the sum."),
                               al_invitar=lambda: panel.pista("punto", "suma", 6, 1, 2))
        panel.quita_pista()
        
        with self.voiceover(text=tr("""Partimos otra vez del lado izquierdo. <bookmark mark='k'/> Por la definición del producto punto <bookmark mark='l1'/> podemos escribirlo como una suma de productos de componentes.""",
                                    """Again we start from the left-hand side. <bookmark mark='k'/> By the definition of the dot product <bookmark mark='l1'/> we can write it as a sum of products of components.""")) as tracker:
            self.play(*[TransformFromCopy(E.g[i], B0.g[i]) for i in range(7)], run_time=1.0)
            entera(self, B0)
            self.wait_until_bookmark("k")
            paso(self, panel, ["punto"], B0, B1, [], m01, a01, marca="l1", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Por la definición de suma <bookmark mark='l2'/> podemos distribuir el selector.""",
                                    """By the definition of addition <bookmark mark='l2'/> we can distribute the selector.""")) as tracker:
            paso(self, panel, ["suma"], B1, B2, f12, m12, marca="l2", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Ya todo son números reales. <bookmark mark='k'/> Por la distributiva <bookmark mark='l3'/> podemos repartir el primer factor entre los dos sumandos.""",
                                    """Now everything is a real number. <bookmark mark='k'/> By the distributive property <bookmark mark='l3'/> we can share out the first factor between the two terms.""")) as tracker:
            self.wait_until_bookmark("k")
            paso(self, panel, [6], B2, B3, f23, m23, a23, marca="l3", t_moviles=1.2)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Por las propiedades conmutativa y asociativa de la suma <bookmark mark='l4'/> podemos reordenar los sumandos y agruparlos en dos sumas.""",
                                    """By the commutative and associative properties of addition <bookmark mark='l4'/> we can reorder the terms and group them into two sums.""")) as tracker:
            paso(self, panel, [1, 2], B3, B4, [], m34, a34, marca="l4", t_moviles=1.6)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Y por la definición del producto punto, <bookmark mark='l5'/> cada una de esas sumas es un producto punto.""",
                                    """And by the definition of the dot product, <bookmark mark='l5'/> each of those sums is a dot product.""")) as tracker:
            paso(self, panel, ["punto"], B4, B5, [], m45, a45, marca="l5", t_moviles=1.2)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Así pues, el producto punto se distribuye en la suma.""",
                                    """So the dot product distributes over the sum.""")) as tracker:
            self.play(Indicate(B0.tex, color=COLOR_ESCALAR), Indicate(B5.tex, color=COLOR_ESCALAR),
                      Create(marco(E.tex)), run_time=1.4)
        self.wait(1.0)
        
        self.pausa_media()

class L02_V02_E05_OtroVector(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("El otro vector", "The other vector"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        C = Linea([VX, PUNTO, "(", LAM, VY, ")",  "=",  "(", LAM, VY, ")", PUNTO, VX,  "=",  LAM, "(", VY, PUNTO, VX, ")",
                   "=",  LAM, "(", VX, PUNTO, VY, ")"], 42)
        D = Linea(["(", VX, "+", VY, ")", PUNTO, VZ,  "=",  VZ, PUNTO, "(", VX, "+", VY, ")",  "=",  VZ, PUNTO, VX, "+", VZ, PUNTO, VY,
                   "=",  VX, PUNTO, VZ, "+", VY, PUNTO, VZ], 42)
        C.tex.move_to([0, 1.3, 0]); D.tex.move_to([0, -0.4, 0])
        # todos los trozos de C y D son de un glifo: L.ini[t] es el glifo del trozo t. Bajo cada igual, de dónde sale el paso
        def rotulos(L, iguales, centro):
            rs = [Tex(t, font_size=26).set_color(c) for t, c in ((tr("simetría", "symmetry"), COLOR_REGLA), (centro, COLOR_ESCALAR),
                                                                 (tr("simetría", "symmetry"), COLOR_REGLA))]
            for r_, t in zip(rs, iguales):
                r_.next_to(L.g[L.ini[t]], DOWN, buff=0.35)
            return rs
        
        
        rot_c = rotulos(C, (6, 13, 20), tr("el escalar sale", "the scalar comes out"))
        rot_d = rotulos(D, (7, 15, 23), tr("se distribuye", "it distributes"))
        F = Linea([VX, PUNTO, "(", LAM, VY, ")", "=", LAM, "(", VX, PUNTO, VY, ")", "=", "(", LAM, VX, ")", PUNTO, VY], 44)
        F.tex.move_to([0, -2.4, 0])
        
        with self.voiceover(text=tr("""Las otras dos igualdades salen de la simetría: el producto punto no depende del orden de los dos vectores.""",
                                    """The other two equalities follow from symmetry: the dot product does not depend on the order of the two vectors.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Si el escalar está en el segundo vector, <bookmark mark='s1'/> por la simetría podemos cambiar el orden de los vectores. <bookmark mark='s2'/> Ahora el escalar está en el primero, así que sale del producto punto. <bookmark mark='s3'/> Y por la simetría otra vez, volvemos al orden de partida.""",
                                    """If the scalar is in the second vector, <bookmark mark='s1'/> by symmetry we can change the order of the vectors. <bookmark mark='s2'/> Now the scalar is in the first one, so it comes out of the dot product. <bookmark mark='s3'/> And by symmetry again, we go back to the original order.""")) as tracker:
            self.play(*[FadeIn(C.g[i]) for t in range(6) for i in C(t)], run_time=0.8)
            # simetría: (λy) y x cambian de sitio
            nace_l(self, C, C, [], [(C.ini[2 + k], C.ini[7 + k]) for k in range(4)] + [(C.ini[1], C.ini[11]), (C.ini[0], C.ini[12])],
                   tramo=(6, 12), marca="s1", extra=[FadeIn(rot_c[0])], t_moviles=1.1)
            # el escalar sale: el «(» pasa detrás del escalar y el «)» detrás de x
            nace_l(self, C, C, [], [(C.ini[7], C.ini[15]), (C.ini[8], C.ini[14]), (C.ini[9], C.ini[16]), (C.ini[10], C.ini[19]),
                                   (C.ini[11], C.ini[17]), (C.ini[12], C.ini[18])],
                   tramo=(13, 19), marca="s2", extra=[FadeIn(rot_c[1])], t_moviles=1.1)
            # simetría: y y x cambian de sitio dentro de los paréntesis
            nace_l(self, C, C, [(C.ini[14], C.ini[21]), (C.ini[15], C.ini[22]), (C.ini[17], C.ini[24]), (C.ini[19], C.ini[26])],
                   [(C.ini[16], C.ini[25]), (C.ini[18], C.ini[23])], tramo=(20, 26), marca="s3", extra=[FadeIn(rot_c[2])], t_moviles=1.0)
            entera(self, C)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Con la suma en el primer vector se hace lo mismo: <bookmark mark='s1'/> la simetría, <bookmark mark='s2'/> la suma en el segundo vector, que ya hemos demostrado, <bookmark mark='s3'/> y otra vez la simetría.""",
                                    """With the sum in the first vector we do the same: <bookmark mark='s1'/> symmetry, <bookmark mark='s2'/> the sum in the second vector, which we have already proved, <bookmark mark='s3'/> and symmetry again.""")) as tracker:
            self.play(*[FadeIn(D.g[i]) for t in range(7) for i in D(t)], run_time=0.8)
            nace_l(self, D, D, [], [(D.ini[k], D.ini[10 + k]) for k in range(5)] + [(D.ini[5], D.ini[9]), (D.ini[6], D.ini[8])],
                   tramo=(7, 14), marca="s1", extra=[FadeIn(rot_d[0])], t_moviles=1.1)
            nace_l(self, D, D, [], [(D.ini[8], D.ini[16]), (D.ini[8], D.ini[20]), (D.ini[9], D.ini[17]), (D.ini[9], D.ini[21]),
                                   (D.ini[11], D.ini[18]), (D.ini[12], D.ini[19]), (D.ini[13], D.ini[22])],
                   tramo=(15, 22), marca="s2", extra=[FadeIn(rot_d[1])], t_moviles=1.1)
            nace_l(self, D, D, [(D.ini[19], D.ini[27])],
                   [(D.ini[18], D.ini[24]), (D.ini[17], D.ini[25]), (D.ini[16], D.ini[26]),
                    (D.ini[22], D.ini[28]), (D.ini[21], D.ini[29]), (D.ini[20], D.ini[30])],
                   tramo=(23, 30), marca="s3", extra=[FadeIn(rot_d[2])], t_moviles=1.0)
            entera(self, D)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Así pues, el producto punto es lineal en sus dos argumentos. <bookmark mark='e'/> En particular, un escalar puede salir de cualquiera de los dos vectores.""",
                                    """So the dot product is linear in both arguments. <bookmark mark='e'/> In particular, a scalar can come out of either of the two vectors.""")) as tracker:
            self.wait_until_bookmark("e")
            self.play(*[TransformFromCopy(C.g[i], F.g[i]) for i in range(6)], run_time=0.8)
            self.play(FadeIn(F.g[F.ini[6]]), *[TransformFromCopy(C.g[C.ini[20 + k]], F.g[F.ini[6 + k]]) for k in range(1, 7)], run_time=0.8)
            self.play(*[FadeIn(F.g[F.ini[t]]) for t in range(13, 20)], run_time=0.8)
            entera(self, F)
        self.wait(1.2)
        
        self.pausa_media()

class L02_V02_E06_TresVectores(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Tres vectores", "Three vectors"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        VA, VB, VC = r"\Vect{a}", r"\Vect{b}", r"\Vect{c}"
        a, b, c = vector_col(A3_EJ, COLOR_A), vector_col(B3_EJ, COLOR_B), vector_col(C3_EJ, COLOR_C)
        na, nb, nc = con_nombre(VA + "=", a), con_nombre(VB + "=", b), con_nombre(VC + "=", c)
        for n_, col in ((na, COLOR_A), (nb, COLOR_B), (nc, COLOR_C)):
            n_[0].set_color(col)
        VGroup(na, nb, nc).arrange(RIGHT, buff=1.4).move_to([0, 1.6, 0])
        COL = {VA: COLOR_A, VB: COLOR_B, VC: COLOR_C}
        
        
        def cuenta(trozos, resultado, y):
            m = MathTex(*trozos, tex_template=myTemplate, font_size=44)
            for k, t in enumerate(trozos):
                m[k].set_color(COL.get(t, WHITE))
            v = vector_col(resultado, escala=0.7)
            return VGroup(m, v).arrange(RIGHT, buff=0.2).move_to([0, y, 0])
        
        
        uno = cuenta(["(", VA, PUNTO, VB, ")", VC, "=", "2", VC, "="], [0, 2], -0.3)
        dos = cuenta([VA, "(", VB, PUNTO, VC, ")", "=", VA, "3", "="], [3, 0], -1.75)
        dos.shift((uno[0][6].get_x() - dos[0][6].get_x())*RIGHT)   # los iguales, en columna
        distintos = MathTex(r"(\Vect{a}\cdot\Vect{b})\Vect{c}\neq\Vect{a}(\Vect{b}\cdot\Vect{c})", tex_template=myTemplate, font_size=44)
        nota = Tex(tr("en general", "in general"), font_size=30).set_color(GRAY_A)
        VGroup(distintos, nota).arrange(RIGHT, buff=0.4).move_to([0, -3.05, 0])
        u, d_ = uno[0], dos[0]
        
        with self.voiceover(text=tr("""Un escalar sale del producto punto. Podría parecer que con un tercer vector ocurre lo mismo, pero no es así. <bookmark mark='t'/> Tomemos estos tres vectores.""",
                                    """A scalar comes out of the dot product. It might seem that the same happens with a third vector, but it does not. <bookmark mark='t'/> Take these three vectors.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("t")
            self.play(FadeIn(na), FadeIn(nb), FadeIn(nc), run_time=0.8)
        self.wait(0.6)
        
        with self.voiceover(text=tr("""Si calculamos primero el producto punto del vector a por b, <bookmark mark='ab'/> obtenemos dos, <bookmark mark='c'/> y dos por c es este vector.""",
                                    """If we first compute the dot product of the vector 'a' and b, <bookmark mark='ab'/> we get two, <bookmark mark='c'/> and two times c is this vector.""")) as tracker:
            self.play(*[FadeIn(u[k]) for k in range(5)], run_time=0.6)
            self.wait_until_bookmark("ab")
            self.play(FadeIn(u[5]), FadeIn(u[6]), TransformFromCopy(VGroup(*u[0:5]), u[7]), run_time=0.7)
            self.wait_until_bookmark("c")
            self.play(TransformFromCopy(u[5], u[8]), run_time=0.4)
            self.play(FadeIn(u[9]), FadeIn(uno[1]), run_time=0.6)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Si calculamos primero el de b por c, <bookmark mark='bc'/> obtenemos tres, <bookmark mark='a'/> y el producto del vector a por tres es este otro.""",
                                    """If we first compute the one of b and c, <bookmark mark='bc'/> we get three, <bookmark mark='a'/> and the product of the vector 'a' and three is this other one.""")) as tracker:
            self.play(*[FadeIn(d_[k]) for k in range(1, 6)], run_time=0.6)
            self.wait_until_bookmark("bc")
            self.play(FadeIn(d_[0]), FadeIn(d_[6]), TransformFromCopy(VGroup(*d_[1:6]), d_[8]), run_time=0.7)
            self.wait_until_bookmark("a")
            self.play(TransformFromCopy(d_[0], d_[7]), run_time=0.4)
            self.play(FadeIn(d_[9]), FadeIn(dos[1]), run_time=0.6)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Son vectores distintos: <bookmark mark='u'/> el primero se obtiene multiplicando c por un número, <bookmark mark='d'/> y el segundo, multiplicando el vector a por otro.""",
                                    """They are different vectors: <bookmark mark='u'/> the first is obtained by multiplying c by a number, <bookmark mark='d'/> and the second by multiplying the vector 'a' by another.""")) as tracker:
            self.wait_until_bookmark("u")
            resalta(self, [u[7], u[8]], factor=1.25)
            self.wait_until_bookmark("d")
            apaga(self, [u[7]], factor=1.25); apaga(self, [u[8]], color=COLOR_C, factor=1.25)
            resalta(self, [d_[7], d_[8]], factor=1.25)
        self.wait(0.8)
        apaga(self, [d_[7]], color=COLOR_A, factor=1.25); apaga(self, [d_[8]], factor=1.25)
        
        with self.voiceover(text=tr("""Así que con tres vectores no hay un único producto punto, <bookmark mark='p'/> y los paréntesis no se pueden quitar: indican el producto punto que se calcula primero.""",
                                    """So with three vectors there is no single dot product, <bookmark mark='p'/> and the parentheses cannot be removed: they show which dot product is computed first.""")) as tracker:
            self.play(FadeIn(distintos), FadeIn(nota), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(*[Indicate(distintos[0][k], color=COLOR_ESCALAR, scale_factor=1.6) for k in (0, 4, -5, -1)], run_time=1.2)   # los paréntesis (≠ puede ser de dos glifos)
        self.wait(1.2)
        
        self.pausa_media()

class L02_V02_E07_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [r"(\Vect{x}+\Vect{y})\cdot\Vect{z}=\Vect{x}\cdot\Vect{z}+\Vect{y}\cdot\Vect{z},\qquad \Vect{x}\cdot(\Vect{y}+\Vect{z})=\Vect{x}\cdot\Vect{y}+\Vect{x}\cdot\Vect{z}",
                    r"(\lambda\Vect{x})\cdot\Vect{y}=\lambda(\Vect{x}\cdot\Vect{y})=\Vect{x}\cdot(\lambda\Vect{y})",
                    r"(\Vect{a}\cdot\Vect{b})\Vect{c}\neq\Vect{a}(\Vect{b}\cdot\Vect{c})"]
        rotulos = [tr("se distribuye en las sumas", "it distributes over sums"),
                   tr("un escalar sale de cualquiera de los dos vectores", "a scalar comes out of either vector"),
                   tr("con tres vectores, los paréntesis no se quitan", "with three vectors, the parentheses stay")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=38), Tex(r, font_size=32, color=GRAY_A)).arrange(DOWN, buff=0.15)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.45)
        # «lineal en sus dos argumentos» encima de las dos primeras filas, en horizontal (vertical no se lee en un móvil)
        lineal = Tex(tr("Lineal en sus dos argumentos", "Linear in both arguments"), font_size=34).set_color(COLOR_ESCALAR)
        VGroup(lineal, filas).arrange(DOWN, buff=0.3).next_to(cabecera, DOWN, buff=0.4)
        llave = Brace(VGroup(filas[0], filas[1]), LEFT, color=COLOR_ESCALAR)
        
        with self.voiceover(text=tr("""Resumamos. El producto punto es lineal en sus dos argumentos: <bookmark mark='s'/> se distribuye en las sumas <bookmark mark='p'/> y un escalar puede salir de cualquiera de los dos vectores.""",
                                    """Let us sum up. The dot product is linear in both arguments: <bookmark mark='s'/> it distributes over sums <bookmark mark='p'/> and a scalar can come out of either of the two vectors.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.play(FadeIn(lineal), run_time=0.6)
            self.wait_until_bookmark("s")
            self.play(FadeIn(filas[0]), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(FadeIn(filas[1]), run_time=0.8)
            self.play(GrowFromCenter(llave), run_time=0.5)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Con tres vectores, en cambio, los paréntesis no se pueden quitar.""",
                                    """With three vectors, on the other hand, the parentheses cannot be removed.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.8)
        self.wait(1.0)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos las combinaciones lineales de vectores.""",
                                    """In the next video we will see linear combinations of vectors.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
