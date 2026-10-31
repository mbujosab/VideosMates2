from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Los vectores como representación de datos", "Vectors as a representation of data")

INGREDIENTES = [tr("patatas (g)", "potatoes (g)"), tr("huevos (unidades)", "eggs (units)"),
                tr("cebolla (g)", "onion (g)"), tr("tomate (g)", "tomato (g)"),
                tr("pepino (g)", "cucumber (g)"), tr("aceite (ml)", "oil (ml)")]

# nombre del plato, nombre del vector, ingredientes por ración, color
RECETAS = [(tr("Tortilla", "Spanish tortilla"), r"\Vect{t}", [150, 1, 30, 0, 0, 40], COLOR_A),
           (tr("Gazpacho", "Gazpacho"), r"\Vect{g}", [0, 0, 15, 250, 50, 20], COLOR_B),
           (tr("Ensalada campera", "Potato salad"), tr(r"\Vect{e}", r"\Vect{s}"), [100, 1, 20, 100, 0, 15], COLOR_C)]
T, G, E = (r[2] for r in RECETAS)
UNA_DE_CADA = [a + b + c for a, b, c in zip(T, G, E)]       # t + g + e
PARA_TRES   = [3*x for x in UNA_DE_CADA]                    # 3(t + g + e)
CON_OMEGA   = [x + 4*y for x, y in zip(PARA_TRES, T)]       # 3(t + g + e) + 4t

PAISES = [tr("España", "Spain"), tr("Francia", "France"), tr("Alemania", "Germany"),
          tr("Reino Unido", "United Kingdom"), tr("EE. UU.", "USA")]
PIB = {2003: [2.9, 0.9, -0.2, 2.5, 1.8], 2004: [3.1, 2.0, 1.1, 3.2, 3.1],
       2005: [3.3, 1.6, 0.7, 1.9, 3.7], 2006: [3.3, 2.0, 0.9, 1.5, 3.5]}   # Sección 1.3 del libro (fuente: ICAE)

OMEGA_COLOR  = PURPLE_B     # fuera del código de colores de la serie


def vector(valores, color=WHITE, decimales=0, escala=0.8):
    if decimales:
        m = DecimalMatrix([[v] for v in valores], left_bracket="(", right_bracket=")", v_buff=0.62,
                          element_to_mobject_config={"num_decimal_places": decimales, "group_with_commas": False})
    else:
        m = IntegerMatrix([[v] for v in valores], left_bracket="(", right_bracket=")", v_buff=0.62,
                          element_to_mobject_config={"group_with_commas": False})   # 1050, no 1,050
    m.get_entries().set_color(color)
    return m.scale(escala)


def leyenda(rotulos, v, buff=0.35, font_size=30):
    """Rótulos alineados a la derecha, cada uno a la altura de su componente de v."""
    filas = VGroup(*[Tex(r, font_size=font_size) for r in rotulos])
    x_der = v.get_left()[0] - buff
    for f, e in zip(filas, v.get_entries()):
        f.move_to([x_der - f.width/2, e.get_y(), 0])
    return filas


def banda(v, k, x0, x1, color=COLOR_ESCALAR):
    y = v.get_entries()[k].get_y()
    return Rectangle(width=x1 - x0, height=0.5, stroke_width=0, fill_color=color,
                     fill_opacity=0.22).move_to([(x0 + x1)/2, y, 0])


def _cara(estado, alto, mira=ORIGIN):
    """Ojos, cejas y boca de Omega (se colocan dentro del arco). Estados: normal (sonriente),
    neutral (sin sonrisa), duda, sorpresa, alegria y meditacion."""
    u, blanco, r = alto/2, dict(color=WHITE, stroke_width=3), 0.11*alto/2
    def ojo(rr=r, pupila=0.5, m=mira):
        b = Circle(radius=rr, color=WHITE, fill_opacity=1, stroke_width=1.2).set_stroke(BLACK)
        p = Dot(radius=rr*pupila, color=BLACK).move_to(m*rr*0.4)
        return VGroup(b, p, Dot(radius=rr*0.13, color=WHITE).move_to(p.get_center() + rr*0.18*(UP + LEFT)))
    if estado == "alegria":
        ojos = VGroup(*[Arc(radius=0.8*r, start_angle=0, angle=PI, **blanco) for _ in range(2)])
    elif estado == "meditacion":
        ojos = VGroup(*[Arc(radius=0.8*r, start_angle=PI, angle=PI, **blanco) for _ in range(2)])
    elif estado == "sorpresa":
        ojos = VGroup(ojo(1.25*r, 0.3, ORIGIN), ojo(1.25*r, 0.3, ORIGIN))
    elif estado == "duda":
        ojos = VGroup(ojo(m=UR), ojo(m=UR))
    else:
        ojos = VGroup(ojo(), ojo())
    ojos.arrange(RIGHT, buff=0.9*r)
    i, d, w = ojos[0].get_top(), ojos[1].get_top(), 2.2*r
    ceja = lambda c, ang, dy: Line(c + 0.5*w*LEFT, c + 0.5*w*RIGHT, **blanco).rotate(ang).shift((0.12*u + dy)*UP)
    if estado == "duda":          # una ceja alta, con la punta interior levantada
        cejas = VGroup(ceja(i, 0, -0.02*u), ceja(d, -18*DEGREES, 0.1*u))
    elif estado == "sorpresa":
        cejas = VGroup(*[ArcBetweenPoints(c + 0.5*w*LEFT + 0.2*u*UP, c + 0.5*w*RIGHT + 0.2*u*UP, angle=-PI/3, **blanco) for c in (i, d)])
    elif estado in ("meditacion", "neutral"):
        cejas = VGroup(ceja(i, 0, -0.02*u), ceja(d, 0, -0.02*u))
    else:                         # normal y alegría: cejas relajadas
        cejas = VGroup(ceja(i, 10*DEGREES, 0), ceja(d, -10*DEGREES, 0))
    base = ojos.get_bottom() + 0.16*u*DOWN
    if estado == "alegria":
        boca = Arc(radius=0.17*u, start_angle=PI, angle=PI, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(base + 0.04*u*DOWN)
    elif estado == "sorpresa":
        boca = Ellipse(width=0.12*u, height=0.17*u, color=WHITE, stroke_width=3).move_to(base + 0.04*u*DOWN)
    elif estado == "duda":
        boca = Line(base + 0.12*u*LEFT, base + 0.12*u*RIGHT, **blanco).rotate(-12*DEGREES)
    elif estado in ("meditacion", "neutral"):
        boca = Line(base + (0.06 if estado == "meditacion" else 0.1)*u*LEFT, base + (0.06 if estado == "meditacion" else 0.1)*u*RIGHT, **blanco)
    else:
        boca = Arc(radius=0.14*u, start_angle=-PI*0.8, angle=PI*0.6, **blanco).move_to(base)
    return VGroup(ojos, cejas, boca)


def omega(estado="normal", alto=1.6, mira=ORIGIN, color=None):
    """La criatura de la serie: [0] el cuerpo (una Ω gruesa), [1] la cara (ojos, cejas, boca)
    y [2] el signo del estado (?, !, destellos o la nube de pensamiento)."""
    cuerpo = MathTex(r"\boldsymbol{\Omega}").set_color(color or OMEGA_COLOR).scale_to_fit_height(alto)
    cara = _cara(estado, alto, mira).move_to(cuerpo.get_center() + 0.13*alto*UP)
    figura = VGroup(cuerpo, cara)
    signo = VGroup()
    if estado == "duda":
        figura.rotate(-8*DEGREES)
        signo = MathTex("?", font_size=60, color=COLOR_ESCALAR).next_to(figura, UR, buff=0)
    elif estado == "sorpresa":
        figura.stretch(1.08, 1)
        signo = MathTex("!", font_size=60, color=COLOR_ESCALAR).next_to(figura, UR, buff=0)
    elif estado == "alegria":
        figura.stretch(0.95, 1)
        signo = VGroup(*[Star(n=4, outer_radius=0.12, inner_radius=0.04, color=COLOR_ESCALAR, fill_opacity=1).move_to(figura.get_corner(UR) + v)
                         for v in (0.1*UP, 0.35*DOWN + 0.25*RIGHT, 0.25*UP + 0.45*LEFT)])
    elif estado == "meditacion":
        nube = VGroup(*[Circle(radius=rr, color=WHITE, fill_opacity=1) for rr in (0.06, 0.1, 0.38)])
        nube[0].move_to(figura.get_corner(UR) + 0.05*UP); nube[1].next_to(nube[0], UR, buff=0.05); nube[2].next_to(nube[1], UR, buff=0)
        signo = VGroup(nube, MathTex(r"\dots", color=BLACK, font_size=40).move_to(nube[2]))
    o = VGroup(cuerpo, cara, signo)
    o.estado, o.alto, o.mira = estado, alto, mira
    return o


def cambia(escena, criatura, estado, mira=None, run_time=0.6):
    """Cambia la expresión de la criatura sin moverla (el cuerpo se queda donde estaba)."""
    nueva = omega(estado, criatura.alto, criatura.mira if mira is None else mira)
    nueva.shift(criatura[0].get_bottom() - nueva[0].get_bottom())
    # Un signo que aparece o desaparece (?, !, destellos) lo hace en su sitio: transformado
    # desde o hacia un grupo vacío, volaría desde o hacia el origen.
    if len(nueva[2]) == 0 and len(criatura[2]) > 0:
        nueva.submobjects[2] = criatura[2].copy().set_opacity(0)
    elif len(criatura[2]) == 0 and len(nueva[2]) > 0:
        criatura.submobjects[2] = nueva[2].copy().set_opacity(0)
    escena.play(Transform(criatura, nueva), run_time=run_time)
    criatura.estado, criatura.mira = estado, nueva.mira


def bocadillo(texto, criatura, ancho=4.2, font_size=30):
    t = Tex(texto, font_size=font_size, color=BLACK)
    if t.width > ancho:
        t.scale_to_fit_width(ancho)
    globo = RoundedRectangle(corner_radius=0.25, width=t.width + 0.5, height=t.height + 0.4,
                             fill_color=WHITE, fill_opacity=1, stroke_color=WHITE)
    globo.next_to(criatura[0], UL, buff=0.05).shift(0.4*RIGHT)
    t.move_to(globo)
    pico = Polygon(globo.get_corner(DR) + 0.35*LEFT, globo.get_corner(DR) + 0.8*LEFT,
                   criatura[0].get_corner(UL) + 0.15*RIGHT + 0.05*DOWN, fill_color=WHITE, fill_opacity=1, stroke_width=0)
    return VGroup(pico, globo, t)


def parpadea(escena, criatura, run_time=0.3):
    if criatura.estado in ("alegria", "meditacion"):   # ya tiene los ojos cerrados
        return
    ojos = criatura[1][0]
    escena.play(ojos.animate.stretch(0.1, 1), run_time=run_time/2)
    escena.play(ojos.animate.stretch(10, 1), run_time=run_time/2)


def entra(escena, criatura, desde=RIGHT, run_time=1):
    escena.play(FadeIn(criatura, shift=1.5*(-desde)), run_time=run_time)
    parpadea(escena, criatura)

class L01_V08_VectoresComoDatos(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        
        vs = VGroup(*[vector(v, color=c) for _, _, v, c in RECETAS]).arrange(RIGHT, buff=1.3).move_to([1.4, -0.6, 0])
        cabeceras = VGroup(*[VGroup(Tex(n, font_size=32, color=c), MathTex(l, tex_template=myTemplate, font_size=40, color=c)).arrange(DOWN, buff=0.15).next_to(v, UP, buff=0.3)
                             for (n, l, _, c), v in zip(RECETAS, vs)])
        ley = leyenda(INGREDIENTES, vs[0])
        x0, x1 = ley.get_left()[0] - 0.15, vs[-1].get_right()[0] + 0.15
        
        with self.voiceover(text=tr("""En los dos vídeos anteriores hemos operado con vectores sin preocuparnos de para qué los podemos usar. En este veremos que un vector sirve para guardar datos.""",
                                    """In the two previous videos we operated with vectors without worrying about what we can use them for. In this one we will see that a vector is a way of storing data.""")) as tracker:
            self.play(Write(titulo), run_time=1.5)
        self.wait(0.5)   # una pausa antes de presentar a los cocineros (Marcos, 2026-10-26)
        
        with self.voiceover(text=tr("""Ana, Luis y Marta preparan una cena, y cada uno cocinará un plato: <bookmark mark='t'/> Ana, una tortilla de patatas; <bookmark mark='g'/> Luis, un gazpacho; <bookmark mark='e'/> y Marta, una ensalada campera.""",
                                    """Ana, Luis and Marta are preparing a dinner, and each of them will cook one dish: <bookmark mark='t'/> Ana, a Spanish tortilla; <bookmark mark='g'/> Luis, a gazpacho; <bookmark mark='e'/> and Marta, a potato salad.""")) as tracker:
            for marca, cab in zip("tge", cabeceras):
                self.wait_until_bookmark(marca)
                self.play(FadeIn(cab, shift=0.2*DOWN), run_time=0.7)
        
        with self.voiceover(text=tr("""Cada receta es un vector, <bookmark mark='v'/> con la cantidad de cada ingrediente para una ración. A la izquierda <bookmark mark='l'/> tiene la lista de ingredientes, con sus unidades.""",
                                    """Each recipe is a vector, <bookmark mark='v'/> with the amount of each ingredient for one serving. On the left <bookmark mark='l'/> you have the list of ingredients, with their units.""")) as tracker:
            self.wait_until_bookmark("v")
            self.play(LaggedStart(*[FadeIn(v) for v in vs], lag_ratio=0.3), run_time=1.5)
            self.wait_until_bookmark("l")
            self.play(FadeIn(ley), run_time=1)
        
        f_huevos, f_tomate = banda(vs[0], 1, x0, x1), banda(vs[0], 3, x0, x1)
        with self.voiceover(text=tr("""Lo importante es la posición. <bookmark mark='h'/> La segunda componente de cada receta es siempre el número de huevos, y la cuarta, <bookmark mark='to'/> los gramos de tomate.""",
                                    """What matters is the position. <bookmark mark='h'/> The second component of every recipe is always the number of eggs, and the fourth, <bookmark mark='to'/> the grams of tomato.""")) as tracker:
            self.wait_until_bookmark("h")
            self.play(FadeIn(f_huevos), run_time=0.8)
            self.wait_until_bookmark("to")
            self.play(ReplacementTransform(f_huevos, f_tomate), run_time=0.8)
        
        # el inglés difiere del español publicado (2026-10-28): la frase prometía un motivo que el vídeo no da (Marcos, 2026-10-30)
        with self.voiceover(text=tr("""Veamos el motivo por el que, si cada cocinero ordenara los ingredientes de manera distinta, los vectores no servirían para organizar la lista de la compra.""",
                                    """That is why every cook must list the ingredients in the same order: otherwise the vectors would be useless for organising the shopping list.""")) as tracker:
            self.play(FadeOut(f_tomate), run_time=0.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        vs = VGroup(*[vector(v, color=c) for _, _, v, c in RECETAS])
        cesta = vector(UNA_DE_CADA)
        signos = [MathTex(s, font_size=44) for s in "++="]
        fila = VGroup(vs[0], signos[0], vs[1], signos[1], vs[2], signos[2], cesta).arrange(RIGHT, buff=0.5).move_to([1.3, -0.7, 0])   # hueco para los 3 de la propiedad 5
        ley = leyenda(INGREDIENTES, vs[0], buff=0.5)
        nombres = VGroup(*[MathTex(l, tex_template=myTemplate, font_size=40, color=c).next_to(v, UP, buff=0.25) for (_, l, _, c), v in zip(RECETAS, vs)])
        rot_cesta = Tex(tr("cesta", "basket"), font_size=32).next_to(cesta, UP, buff=0.3)
        l_t, l_g, l_e = (r[1] for r in RECETAS)
        f1 = MathTex(f"{l_t}+{l_g}+{l_e}", tex_template=myTemplate, font_size=44).to_edge(UP, buff=0.5)
        f3 = MathTex("3", "(", f"{l_t}+{l_g}+{l_e}", ")", tex_template=myTemplate, font_size=44).to_edge(UP, buff=0.5)
        f3[0].set_color(COLOR_ESCALAR)
        f5 = MathTex(f"=3{l_t}+3{l_g}+3{l_e}", tex_template=myTemplate, font_size=44).set_color(COLOR_REGLA)
        
        with self.voiceover(text=tr("""Para hacer la compra, primero sumamos los ingredientes de las tres recetas. <bookmark mark='s'/> Se suman patatas con patatas, huevos con huevos, y así con cada ingrediente: es la suma componente a componente.<bookmark mark='v2'/>""",
                                    """To do the shopping, we first add up the ingredients of the three recipes. <bookmark mark='s'/> Potatoes are added to potatoes, eggs to eggs, and so on with each ingredient: it is component-wise addition.""")) as tracker:
            self.play(FadeIn(ley), FadeIn(vs), FadeIn(nombres), FadeIn(f1), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(VGroup(*signos)), FadeIn(cesta.get_brackets()), FadeIn(rot_cesta), run_time=0.6)
            self.play(LaggedStart(*[TransformFromCopy(VGroup(*[v.get_entries()[k] for v in vs]), cesta.get_entries()[k])
                                    for k in range(len(INGREDIENTES))], lag_ratio=0.35), run_time=3.5)
        
        nueva = vector(PARA_TRES).move_to(cesta, aligned_edge=LEFT)
        tres_c = MathTex("3", font_size=44, color=COLOR_ESCALAR).next_to(cesta, LEFT, buff=0.1)
        # antes de multiplicar se quitan los sumandos y el igual: t+g+e no es igual a 3(t+g+e)
        with self.voiceover(text=tr("""Este vector tiene los ingredientes de una ración de cada plato. Como cenan tres personas, <bookmark mark='x'/> lo multiplicamos por tres.""",
                                    """This vector holds the ingredients for one serving of each dish. Since three people are having dinner, <bookmark mark='x'/> we multiply it by three.""")) as tracker:
            self.play(FadeOut(vs), FadeOut(nombres), FadeOut(VGroup(*signos)), Indicate(cesta, color=COLOR_RESULTADO, scale_factor=1.08), run_time=1)
            self.wait_until_bookmark("x")
            # el 3 llega desde la izquierda y se pega a t+g+e mientras aparecen los paréntesis; otro 3 se pone delante de la cesta
            self.play(ReplacementTransform(f1, f3[2]), FadeIn(f3[0], shift=2*RIGHT), FadeIn(f3[1]), FadeIn(f3[3]),
                      FadeIn(tres_c, shift=RIGHT), run_time=2)
            self.play(ReplacementTransform(VGroup(tres_c, cesta), nueva), rot_cesta.animate.next_to(nueva, UP, buff=0.3), run_time=1.5)
        
        # las recetas multiplicadas por tres ocupan el sitio de las de antes (mismo ancho) y el igual se recupera
        vs3 = VGroup(*[vector([3*x for x in v], color=c).move_to(w) for (_, _, v, c), w in zip(RECETAS, vs)])
        nombres3 = VGroup(*[MathTex("3", l, tex_template=myTemplate, font_size=40, color=c).next_to(v, UP, buff=0.25) for (_, l, _, c), v in zip(RECETAS, vs3)])
        for n in nombres3:
            n[0].set_color(COLOR_ESCALAR)
        signos3 = VGroup(*[s.copy() for s in signos])
        tres_r = [MathTex("3", font_size=44, color=COLOR_ESCALAR).next_to(v, LEFT, buff=0.1) for v in vs]
        VGroup(f3.copy(), f5).arrange(RIGHT, buff=0.15).to_edge(UP, buff=0.5)
        with self.voiceover(text=tr("""Daría lo mismo multiplicar cada receta por tres y sumar después: <bookmark mark='p'/> es la propiedad cinco del vídeo anterior.""",
                                    """It would be the same to multiply each recipe by three and add afterwards: <bookmark mark='p'/> it is property five from the previous video.""")) as tracker:
            # las recetas vuelven como estaban y se multiplican por tres a la vista, como la cesta
            self.play(f3.animate.next_to(f5, LEFT, buff=0.15), FadeIn(vs), FadeIn(nombres), FadeIn(signos3[:2]), run_time=0.8)
            self.play(*[FadeIn(t, shift=0.5*RIGHT) for t in tres_r], run_time=0.6)
            self.play(*[ReplacementTransform(VGroup(t, v), w) for t, v, w in zip(tres_r, vs, vs3)],
                      *[ReplacementTransform(n, m[1]) for n, m in zip(nombres, nombres3)],
                      *[FadeIn(m[0], shift=0.3*RIGHT) for m in nombres3], run_time=1.2)
            self.wait_until_bookmark("p")
            self.play(Write(f5), FadeIn(signos3[2]), run_time=1.2)
            self.play(Indicate(signos3[2], color=COLOR_REGLA, scale_factor=1.8), run_time=1)   # el igual vuelve gracias a la propiedad 5
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        l_t, l_g, l_e = (r[1] for r in RECETAS)
        cesta = vector(PARA_TRES)
        mas, cuatro, tt, igual = MathTex("+", font_size=44), MathTex("4", font_size=44, color=COLOR_ESCALAR), vector(T, color=COLOR_A), MathTex("=", font_size=44)
        total = vector(CON_OMEGA)
        fila = VGroup(cesta, mas, VGroup(cuatro, tt).arrange(RIGHT, buff=0.1), igual, total).arrange(RIGHT, buff=0.3).move_to([-0.3, -0.7, 0])
        t4 = vector([4*x for x in T], color=COLOR_A).move_to(fila[2])
        ley = leyenda(INGREDIENTES, cesta)
        f3 = MathTex(f"3({l_t}+{l_g}+{l_e})", tex_template=myTemplate, font_size=44).next_to(cesta, UP, buff=0.3)
        ft = MathTex(f"4{l_t}", tex_template=myTemplate, font_size=44).next_to(fila[2], UP, buff=0.3)
        ft[0][0].set_color(COLOR_ESCALAR); ft[0][1:].set_color(COLOR_A)
        ftot = MathTex(f"3({l_t}+{l_g}+{l_e})+4{l_t}", tex_template=myTemplate, font_size=44).to_edge(UP, buff=0.4).shift(1.5*LEFT)
        nombre_cl = Tex(tr("combinación lineal", "linear combination"), font_size=34, color=COLOR_ESCALAR).next_to(ftot, RIGHT, buff=0.5)
        om = omega("normal", mira=LEFT).to_corner(DR, buff=0.5)
        globo = bocadillo(tr(r"¡Yo me apunto! No cocino,\\ pero me comería\\ cuatro raciones de tortilla.",
                             r"Count me in! I won't cook,\\ but I'd eat four\\ servings of tortilla."), om, ancho=3.6)
        
        with self.voiceover(text=tr("""Con la cesta ya preparada para tres, <bookmark mark='o'/> se apunta también Omega. No cocinará, pero le encanta la tortilla y se comería cuatro raciones.""",
                                    """With the basket ready for three, <bookmark mark='o'/> Omega joins in too. Omega will not cook, but loves the tortilla and would eat four servings.""")) as tracker:
            self.play(FadeIn(ley), FadeIn(cesta), FadeIn(f3), run_time=1)
            self.wait_until_bookmark("o")
            entra(self, om)
            self.play(FadeIn(globo, scale=0.8), run_time=0.6)
        
        with self.voiceover(text=tr("""Así que multiplicamos por cuatro la receta de la tortilla <bookmark mark='t4'/> y la sumamos a la cesta. <bookmark mark='s'/>""",
                                    """So we multiply the tortilla recipe by four <bookmark mark='t4'/> and add it to the basket. <bookmark mark='s'/>""")) as tracker:
            self.play(FadeOut(globo), run_time=0.5)
            self.wait_until_bookmark("t4")
            self.play(FadeIn(mas), FadeIn(cuatro), FadeIn(tt), FadeIn(ft), run_time=0.8)
            self.play(ReplacementTransform(VGroup(cuatro, tt), t4), run_time=1.2)   # el 4 se absorbe: queda 4t ya calculado
            self.wait_until_bookmark("s")
            self.play(FadeIn(igual), FadeIn(total.get_brackets()), run_time=0.5)
            self.play(LaggedStart(*[TransformFromCopy(VGroup(cesta.get_entries()[k], t4.get_entries()[k]), total.get_entries()[k])
                                    for k in range(len(INGREDIENTES))], lag_ratio=0.35), run_time=3)
            cambia(self, om, "alegria")   # sus cuatro raciones ya están en la cesta
        
        with self.voiceover(text=tr("""La cesta es una suma de recetas multiplicadas por números. <bookmark mark='f'/> Esta forma de combinar vectores se llama <bookmark mark='cl'/> combinación lineal, y aparecerá a lo largo de todo el curso.""",
                                    """The basket is a sum of recipes multiplied by numbers. <bookmark mark='f'/> This way of combining vectors is called <bookmark mark='cl'/> a linear combination, and it will appear throughout the course.""")) as tracker:
            self.wait(1)
            cambia(self, om, "normal", mira=UL)   # la alegría dura un instante; ahora atiende a la narración
            self.wait_until_bookmark("f")
            self.play(FadeIn(ftot, shift=0.2*DOWN), run_time=1)
            self.wait_until_bookmark("cl")
            self.play(Indicate(ftot, color=COLOR_ESCALAR, scale_factor=1.1), FadeIn(nombre_cl, shift=0.2*UP), run_time=1.5)
            parpadea(self, om)
        
        cantidades = [f"{x}" for x in CON_OMEGA]
        plantillas = [tr("{} g de patatas", "{} g of potatoes"), tr("{} huevos", "{} eggs"), tr("{} g de cebolla", "{} g of onion"),
                      tr("{} g de tomate", "{} g of tomato"), tr("{} g de pepino", "{} g of cucumber"), tr("{} ml de aceite", "{} ml of oil")]
        lista = VGroup(*[Tex(p.format(c), font_size=36) for p, c in zip(plantillas, cantidades)]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        cab_lista = Tex(tr("Lista de la compra", "Shopping list"), font_size=40, color=COLOR_TITULO)
        hoja = VGroup(cab_lista, lista).arrange(DOWN, buff=0.4).move_to([-1, -0.5, 0])
        with self.voiceover(text=tr("""Y con la lista de ingredientes delante, el vector se convierte en la lista de la compra.""",
                                    """And with the list of ingredients alongside, the vector becomes the shopping list.""")) as tracker:
            self.play(FadeOut(VGroup(cesta, mas, t4, igual, ft, f3)), total.animate.next_to(ley, RIGHT, buff=0.35), run_time=1)
            self.play(FadeTransform(VGroup(ley, total), hoja), run_time=1.5)
            cambia(self, om, "normal", mira=LEFT)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        d = vector(PIB[2003], decimales=1).move_to([-0.5, -0.3, 0])
        nombre = MathTex(r"\Vect[2003]{p}", tex_template=myTemplate, font_size=44).next_to(d, UP, buff=0.3)
        paises = leyenda(PAISES, d, font_size=32)
        x0, x1 = paises.get_left()[0] - 0.15, d.get_right()[0] + 0.15
        om = omega("duda").to_corner(DR, buff=0.5).shift(0.8*UP)   # lleva la pregunta
        globo = bocadillo(tr(r"¿Qué país no creció\\ en 2003?", r"Which country did not\\ grow in 2003?"), om, ancho=3.4)
        
        # el inglés difiere del español publicado: la segunda frase decía dos veces lo mismo (Marcos, 2026-10-30)
        with self.voiceover(text=tr("""De manera similar podemos emplear un vector para mostrar datos económicos. Este vector recoge <bookmark mark='d'/> el crecimiento del PIB de cinco países en 2003: las cifras muestran el crecimiento porcentual de los países ese año.""",
                                    """In a similar way we can use a vector to show economic data. This vector holds <bookmark mark='d'/> the percentage GDP growth of five countries in 2003.""")) as tracker:
            self.wait_until_bookmark("d")
            self.play(FadeIn(d), FadeIn(nombre), FadeIn(paises), run_time=1.2)
        
        f_us = banda(d, 4, x0, x1)
        with self.voiceover(text=tr("""Otra vez es la posición la que dice a qué país corresponde cada dato: <bookmark mark='us'/> el quinto número es el crecimiento de Estados Unidos.<bookmark mark='v4'/>""",
                                    """Once again, it is the position that tells which country each figure belongs to: <bookmark mark='us'/> the fifth number is the growth of the United States.""")) as tracker:
            self.wait_until_bookmark("us")
            self.play(FadeIn(f_us), run_time=0.8)
        
        with self.voiceover(text=tr("""Omega busca el país que no creció en 2003.""",
                                    """Omega is looking for the country that did not grow in 2003.""")) as tracker:
            self.play(FadeOut(f_us), run_time=0.5)
            entra(self, om)
            self.play(FadeIn(globo, scale=0.8), run_time=0.6)
        
        self.wait(1.5)   # un instante para buscarlo (sin tarjeta de pausa: es inmediato)
        self.play(Indicate(d.get_entries()[2], color=COLOR_ESCALAR, scale_factor=1.3), run_time=1.2)
        
        f_al = banda(d, 2, x0, x1)
        # el inglés difiere del español publicado: «Indeed» confirmaba algo que nadie había dicho (Marcos, 2026-10-30)
        with self.voiceover(text=tr("""Efectivamente, es <bookmark mark='al'/> Alemania: su dato es negativo, así que su PIB disminuyó ese año.""",
                                    """The answer is <bookmark mark='al'/> Germany: its figure is negative, so its GDP shrank that year.""")) as tracker:
            self.play(FadeOut(globo), run_time=0.4)
            self.wait_until_bookmark("al")
            self.play(FadeIn(f_al), run_time=0.8)
            cambia(self, om, "neutral", mira=LEFT)   # sin sonrisa: es un mal dato
            parpadea(self, om)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        ds = VGroup(*[vector(PIB[a], decimales=1) for a in PIB]).arrange(RIGHT, buff=0.6).move_to([1, 0.1, 0])
        nombres = VGroup(*[MathTex(rf"\Vect[{a}]{{p}}", tex_template=myTemplate, font_size=40).next_to(v, UP, buff=0.3) for a, v in zip(PIB, ds)])
        paises = leyenda(PAISES, ds[0], font_size=32)
        resumen = Tex(tr("Cada posición corresponde siempre a lo mismo:\\\\ un ingrediente, un país...",
                         "Each position always refers to the same thing:\\\\ an ingredient, a country..."), font_size=34).to_edge(DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""Con datos de cuatro años tenemos cuatro vectores, <bookmark mark='a'/> uno por año, con los países siempre en el mismo orden.""",
                                    """With data for four years we have four vectors, <bookmark mark='a'/> one per year, with the countries always in the same order.""")) as tracker:
            self.play(FadeIn(paises), run_time=0.8)
            self.wait_until_bookmark("a")
            self.play(LaggedStart(*[FadeIn(VGroup(v, n)) for v, n in zip(ds, nombres)], lag_ratio=0.4), run_time=2)
        
        with self.voiceover(text=tr("""Resumamos. Un vector puede guardar datos: <bookmark mark='r'/> cada posición corresponde siempre a lo mismo; por ejemplo un ingrediente o un país. Con las recetas, eso nos permitió sumar componente a componente y multiplicar por un número.""",
                                    """Let us sum up. A vector can store data: <bookmark mark='r'/> each position always refers to the same thing; for example, an ingredient or a country. With the recipes, this let us add component-wise and multiply by a number.""")) as tracker:
            self.wait_until_bookmark("r")
            self.play(FadeIn(resumen), run_time=1)
        
        fila = banda(ds[0], 2, paises.get_left()[0] - 0.15, ds[-1].get_right()[0] + 0.15)   # Alemania
        with self.voiceover(text=tr("""Para guardar juntos los cuatro vectores, basta ponerlos uno al lado del otro, <bookmark mark='f'/> lo que nos permite ver la evolución del crecimiento de cada país en su correspondiente fila.""",
                                    """To store the four vectors together, we just place them side by side, <bookmark mark='f'/> which lets us follow how each country's growth evolves along its own row.""")) as tracker:
            self.play(Indicate(ds, color=COLOR_RESULTADO, scale_factor=1.05), run_time=1.5)
            self.wait_until_bookmark("f")
            self.play(FadeIn(fila), run_time=0.8)
        
        self.wait(0.5)   # una pausa antes de anunciar el próximo vídeo (Marcos, 2026-10-26)
        with self.voiceover(text=tr("""En el próximo vídeo esa tabla de números tendrá nombre: una matriz.""",
                                    """In the next video this table of numbers will get a name: a matrix.""")) as tracker:
            self.play(FadeOut(fila), Create(SurroundingRectangle(ds, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15)), run_time=1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos_finales()


class L01_V08_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class L01_V08_E01_LaCena(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        
        vs = VGroup(*[vector(v, color=c) for _, _, v, c in RECETAS]).arrange(RIGHT, buff=1.3).move_to([1.4, -0.6, 0])
        cabeceras = VGroup(*[VGroup(Tex(n, font_size=32, color=c), MathTex(l, tex_template=myTemplate, font_size=40, color=c)).arrange(DOWN, buff=0.15).next_to(v, UP, buff=0.3)
                             for (n, l, _, c), v in zip(RECETAS, vs)])
        ley = leyenda(INGREDIENTES, vs[0])
        x0, x1 = ley.get_left()[0] - 0.15, vs[-1].get_right()[0] + 0.15
        
        with self.voiceover(text=tr("""En los dos vídeos anteriores hemos operado con vectores sin preocuparnos de para qué los podemos usar. En este veremos que un vector sirve para guardar datos.""",
                                    """In the two previous videos we operated with vectors without worrying about what we can use them for. In this one we will see that a vector is a way of storing data.""")) as tracker:
            self.play(Write(titulo), run_time=1.5)
        self.wait(0.5)   # una pausa antes de presentar a los cocineros (Marcos, 2026-10-26)
        
        with self.voiceover(text=tr("""Ana, Luis y Marta preparan una cena, y cada uno cocinará un plato: <bookmark mark='t'/> Ana, una tortilla de patatas; <bookmark mark='g'/> Luis, un gazpacho; <bookmark mark='e'/> y Marta, una ensalada campera.""",
                                    """Ana, Luis and Marta are preparing a dinner, and each of them will cook one dish: <bookmark mark='t'/> Ana, a Spanish tortilla; <bookmark mark='g'/> Luis, a gazpacho; <bookmark mark='e'/> and Marta, a potato salad.""")) as tracker:
            for marca, cab in zip("tge", cabeceras):
                self.wait_until_bookmark(marca)
                self.play(FadeIn(cab, shift=0.2*DOWN), run_time=0.7)
        
        with self.voiceover(text=tr("""Cada receta es un vector, <bookmark mark='v'/> con la cantidad de cada ingrediente para una ración. A la izquierda <bookmark mark='l'/> tiene la lista de ingredientes, con sus unidades.""",
                                    """Each recipe is a vector, <bookmark mark='v'/> with the amount of each ingredient for one serving. On the left <bookmark mark='l'/> you have the list of ingredients, with their units.""")) as tracker:
            self.wait_until_bookmark("v")
            self.play(LaggedStart(*[FadeIn(v) for v in vs], lag_ratio=0.3), run_time=1.5)
            self.wait_until_bookmark("l")
            self.play(FadeIn(ley), run_time=1)
        
        f_huevos, f_tomate = banda(vs[0], 1, x0, x1), banda(vs[0], 3, x0, x1)
        with self.voiceover(text=tr("""Lo importante es la posición. <bookmark mark='h'/> La segunda componente de cada receta es siempre el número de huevos, y la cuarta, <bookmark mark='to'/> los gramos de tomate.""",
                                    """What matters is the position. <bookmark mark='h'/> The second component of every recipe is always the number of eggs, and the fourth, <bookmark mark='to'/> the grams of tomato.""")) as tracker:
            self.wait_until_bookmark("h")
            self.play(FadeIn(f_huevos), run_time=0.8)
            self.wait_until_bookmark("to")
            self.play(ReplacementTransform(f_huevos, f_tomate), run_time=0.8)
        
        # el inglés difiere del español publicado (2026-10-28): la frase prometía un motivo que el vídeo no da (Marcos, 2026-10-30)
        with self.voiceover(text=tr("""Veamos el motivo por el que, si cada cocinero ordenara los ingredientes de manera distinta, los vectores no servirían para organizar la lista de la compra.""",
                                    """That is why every cook must list the ingredients in the same order: otherwise the vectors would be useless for organising the shopping list.""")) as tracker:
            self.play(FadeOut(f_tomate), run_time=0.8)
        
        self.pausa_media()


class L01_V08_E02_LaCesta(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        vs = VGroup(*[vector(v, color=c) for _, _, v, c in RECETAS])
        cesta = vector(UNA_DE_CADA)
        signos = [MathTex(s, font_size=44) for s in "++="]
        fila = VGroup(vs[0], signos[0], vs[1], signos[1], vs[2], signos[2], cesta).arrange(RIGHT, buff=0.5).move_to([1.3, -0.7, 0])   # hueco para los 3 de la propiedad 5
        ley = leyenda(INGREDIENTES, vs[0], buff=0.5)
        nombres = VGroup(*[MathTex(l, tex_template=myTemplate, font_size=40, color=c).next_to(v, UP, buff=0.25) for (_, l, _, c), v in zip(RECETAS, vs)])
        rot_cesta = Tex(tr("cesta", "basket"), font_size=32).next_to(cesta, UP, buff=0.3)
        l_t, l_g, l_e = (r[1] for r in RECETAS)
        f1 = MathTex(f"{l_t}+{l_g}+{l_e}", tex_template=myTemplate, font_size=44).to_edge(UP, buff=0.5)
        f3 = MathTex("3", "(", f"{l_t}+{l_g}+{l_e}", ")", tex_template=myTemplate, font_size=44).to_edge(UP, buff=0.5)
        f3[0].set_color(COLOR_ESCALAR)
        f5 = MathTex(f"=3{l_t}+3{l_g}+3{l_e}", tex_template=myTemplate, font_size=44).set_color(COLOR_REGLA)
        
        with self.voiceover(text=tr("""Para hacer la compra, primero sumamos los ingredientes de las tres recetas. <bookmark mark='s'/> Se suman patatas con patatas, huevos con huevos, y así con cada ingrediente: es la suma componente a componente.<bookmark mark='v2'/>""",
                                    """To do the shopping, we first add up the ingredients of the three recipes. <bookmark mark='s'/> Potatoes are added to potatoes, eggs to eggs, and so on with each ingredient: it is component-wise addition.""")) as tracker:
            self.play(FadeIn(ley), FadeIn(vs), FadeIn(nombres), FadeIn(f1), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(VGroup(*signos)), FadeIn(cesta.get_brackets()), FadeIn(rot_cesta), run_time=0.6)
            self.play(LaggedStart(*[TransformFromCopy(VGroup(*[v.get_entries()[k] for v in vs]), cesta.get_entries()[k])
                                    for k in range(len(INGREDIENTES))], lag_ratio=0.35), run_time=3.5)
        
        nueva = vector(PARA_TRES).move_to(cesta, aligned_edge=LEFT)
        tres_c = MathTex("3", font_size=44, color=COLOR_ESCALAR).next_to(cesta, LEFT, buff=0.1)
        # antes de multiplicar se quitan los sumandos y el igual: t+g+e no es igual a 3(t+g+e)
        with self.voiceover(text=tr("""Este vector tiene los ingredientes de una ración de cada plato. Como cenan tres personas, <bookmark mark='x'/> lo multiplicamos por tres.""",
                                    """This vector holds the ingredients for one serving of each dish. Since three people are having dinner, <bookmark mark='x'/> we multiply it by three.""")) as tracker:
            self.play(FadeOut(vs), FadeOut(nombres), FadeOut(VGroup(*signos)), Indicate(cesta, color=COLOR_RESULTADO, scale_factor=1.08), run_time=1)
            self.wait_until_bookmark("x")
            # el 3 llega desde la izquierda y se pega a t+g+e mientras aparecen los paréntesis; otro 3 se pone delante de la cesta
            self.play(ReplacementTransform(f1, f3[2]), FadeIn(f3[0], shift=2*RIGHT), FadeIn(f3[1]), FadeIn(f3[3]),
                      FadeIn(tres_c, shift=RIGHT), run_time=2)
            self.play(ReplacementTransform(VGroup(tres_c, cesta), nueva), rot_cesta.animate.next_to(nueva, UP, buff=0.3), run_time=1.5)
        
        # las recetas multiplicadas por tres ocupan el sitio de las de antes (mismo ancho) y el igual se recupera
        vs3 = VGroup(*[vector([3*x for x in v], color=c).move_to(w) for (_, _, v, c), w in zip(RECETAS, vs)])
        nombres3 = VGroup(*[MathTex("3", l, tex_template=myTemplate, font_size=40, color=c).next_to(v, UP, buff=0.25) for (_, l, _, c), v in zip(RECETAS, vs3)])
        for n in nombres3:
            n[0].set_color(COLOR_ESCALAR)
        signos3 = VGroup(*[s.copy() for s in signos])
        tres_r = [MathTex("3", font_size=44, color=COLOR_ESCALAR).next_to(v, LEFT, buff=0.1) for v in vs]
        VGroup(f3.copy(), f5).arrange(RIGHT, buff=0.15).to_edge(UP, buff=0.5)
        with self.voiceover(text=tr("""Daría lo mismo multiplicar cada receta por tres y sumar después: <bookmark mark='p'/> es la propiedad cinco del vídeo anterior.""",
                                    """It would be the same to multiply each recipe by three and add afterwards: <bookmark mark='p'/> it is property five from the previous video.""")) as tracker:
            # las recetas vuelven como estaban y se multiplican por tres a la vista, como la cesta
            self.play(f3.animate.next_to(f5, LEFT, buff=0.15), FadeIn(vs), FadeIn(nombres), FadeIn(signos3[:2]), run_time=0.8)
            self.play(*[FadeIn(t, shift=0.5*RIGHT) for t in tres_r], run_time=0.6)
            self.play(*[ReplacementTransform(VGroup(t, v), w) for t, v, w in zip(tres_r, vs, vs3)],
                      *[ReplacementTransform(n, m[1]) for n, m in zip(nombres, nombres3)],
                      *[FadeIn(m[0], shift=0.3*RIGHT) for m in nombres3], run_time=1.2)
            self.wait_until_bookmark("p")
            self.play(Write(f5), FadeIn(signos3[2]), run_time=1.2)
            self.play(Indicate(signos3[2], color=COLOR_REGLA, scale_factor=1.8), run_time=1)   # el igual vuelve gracias a la propiedad 5
        
        self.pausa_media()


class L01_V08_E03_Omega(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        l_t, l_g, l_e = (r[1] for r in RECETAS)
        cesta = vector(PARA_TRES)
        mas, cuatro, tt, igual = MathTex("+", font_size=44), MathTex("4", font_size=44, color=COLOR_ESCALAR), vector(T, color=COLOR_A), MathTex("=", font_size=44)
        total = vector(CON_OMEGA)
        fila = VGroup(cesta, mas, VGroup(cuatro, tt).arrange(RIGHT, buff=0.1), igual, total).arrange(RIGHT, buff=0.3).move_to([-0.3, -0.7, 0])
        t4 = vector([4*x for x in T], color=COLOR_A).move_to(fila[2])
        ley = leyenda(INGREDIENTES, cesta)
        f3 = MathTex(f"3({l_t}+{l_g}+{l_e})", tex_template=myTemplate, font_size=44).next_to(cesta, UP, buff=0.3)
        ft = MathTex(f"4{l_t}", tex_template=myTemplate, font_size=44).next_to(fila[2], UP, buff=0.3)
        ft[0][0].set_color(COLOR_ESCALAR); ft[0][1:].set_color(COLOR_A)
        ftot = MathTex(f"3({l_t}+{l_g}+{l_e})+4{l_t}", tex_template=myTemplate, font_size=44).to_edge(UP, buff=0.4).shift(1.5*LEFT)
        nombre_cl = Tex(tr("combinación lineal", "linear combination"), font_size=34, color=COLOR_ESCALAR).next_to(ftot, RIGHT, buff=0.5)
        om = omega("normal", mira=LEFT).to_corner(DR, buff=0.5)
        globo = bocadillo(tr(r"¡Yo me apunto! No cocino,\\ pero me comería\\ cuatro raciones de tortilla.",
                             r"Count me in! I won't cook,\\ but I'd eat four\\ servings of tortilla."), om, ancho=3.6)
        
        with self.voiceover(text=tr("""Con la cesta ya preparada para tres, <bookmark mark='o'/> se apunta también Omega. No cocinará, pero le encanta la tortilla y se comería cuatro raciones.""",
                                    """With the basket ready for three, <bookmark mark='o'/> Omega joins in too. Omega will not cook, but loves the tortilla and would eat four servings.""")) as tracker:
            self.play(FadeIn(ley), FadeIn(cesta), FadeIn(f3), run_time=1)
            self.wait_until_bookmark("o")
            entra(self, om)
            self.play(FadeIn(globo, scale=0.8), run_time=0.6)
        
        with self.voiceover(text=tr("""Así que multiplicamos por cuatro la receta de la tortilla <bookmark mark='t4'/> y la sumamos a la cesta. <bookmark mark='s'/>""",
                                    """So we multiply the tortilla recipe by four <bookmark mark='t4'/> and add it to the basket. <bookmark mark='s'/>""")) as tracker:
            self.play(FadeOut(globo), run_time=0.5)
            self.wait_until_bookmark("t4")
            self.play(FadeIn(mas), FadeIn(cuatro), FadeIn(tt), FadeIn(ft), run_time=0.8)
            self.play(ReplacementTransform(VGroup(cuatro, tt), t4), run_time=1.2)   # el 4 se absorbe: queda 4t ya calculado
            self.wait_until_bookmark("s")
            self.play(FadeIn(igual), FadeIn(total.get_brackets()), run_time=0.5)
            self.play(LaggedStart(*[TransformFromCopy(VGroup(cesta.get_entries()[k], t4.get_entries()[k]), total.get_entries()[k])
                                    for k in range(len(INGREDIENTES))], lag_ratio=0.35), run_time=3)
            cambia(self, om, "alegria")   # sus cuatro raciones ya están en la cesta
        
        with self.voiceover(text=tr("""La cesta es una suma de recetas multiplicadas por números. <bookmark mark='f'/> Esta forma de combinar vectores se llama <bookmark mark='cl'/> combinación lineal, y aparecerá a lo largo de todo el curso.""",
                                    """The basket is a sum of recipes multiplied by numbers. <bookmark mark='f'/> This way of combining vectors is called <bookmark mark='cl'/> a linear combination, and it will appear throughout the course.""")) as tracker:
            self.wait(1)
            cambia(self, om, "normal", mira=UL)   # la alegría dura un instante; ahora atiende a la narración
            self.wait_until_bookmark("f")
            self.play(FadeIn(ftot, shift=0.2*DOWN), run_time=1)
            self.wait_until_bookmark("cl")
            self.play(Indicate(ftot, color=COLOR_ESCALAR, scale_factor=1.1), FadeIn(nombre_cl, shift=0.2*UP), run_time=1.5)
            parpadea(self, om)
        
        cantidades = [f"{x}" for x in CON_OMEGA]
        plantillas = [tr("{} g de patatas", "{} g of potatoes"), tr("{} huevos", "{} eggs"), tr("{} g de cebolla", "{} g of onion"),
                      tr("{} g de tomate", "{} g of tomato"), tr("{} g de pepino", "{} g of cucumber"), tr("{} ml de aceite", "{} ml of oil")]
        lista = VGroup(*[Tex(p.format(c), font_size=36) for p, c in zip(plantillas, cantidades)]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        cab_lista = Tex(tr("Lista de la compra", "Shopping list"), font_size=40, color=COLOR_TITULO)
        hoja = VGroup(cab_lista, lista).arrange(DOWN, buff=0.4).move_to([-1, -0.5, 0])
        with self.voiceover(text=tr("""Y con la lista de ingredientes delante, el vector se convierte en la lista de la compra.""",
                                    """And with the list of ingredients alongside, the vector becomes the shopping list.""")) as tracker:
            self.play(FadeOut(VGroup(cesta, mas, t4, igual, ft, f3)), total.animate.next_to(ley, RIGHT, buff=0.35), run_time=1)
            self.play(FadeTransform(VGroup(ley, total), hoja), run_time=1.5)
            cambia(self, om, "normal", mira=LEFT)
        
        self.pausa_media()


class L01_V08_E04_PIB(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        d = vector(PIB[2003], decimales=1).move_to([-0.5, -0.3, 0])
        nombre = MathTex(r"\Vect[2003]{p}", tex_template=myTemplate, font_size=44).next_to(d, UP, buff=0.3)
        paises = leyenda(PAISES, d, font_size=32)
        x0, x1 = paises.get_left()[0] - 0.15, d.get_right()[0] + 0.15
        om = omega("duda").to_corner(DR, buff=0.5).shift(0.8*UP)   # lleva la pregunta
        globo = bocadillo(tr(r"¿Qué país no creció\\ en 2003?", r"Which country did not\\ grow in 2003?"), om, ancho=3.4)
        
        # el inglés difiere del español publicado: la segunda frase decía dos veces lo mismo (Marcos, 2026-10-30)
        with self.voiceover(text=tr("""De manera similar podemos emplear un vector para mostrar datos económicos. Este vector recoge <bookmark mark='d'/> el crecimiento del PIB de cinco países en 2003: las cifras muestran el crecimiento porcentual de los países ese año.""",
                                    """In a similar way we can use a vector to show economic data. This vector holds <bookmark mark='d'/> the percentage GDP growth of five countries in 2003.""")) as tracker:
            self.wait_until_bookmark("d")
            self.play(FadeIn(d), FadeIn(nombre), FadeIn(paises), run_time=1.2)
        
        f_us = banda(d, 4, x0, x1)
        with self.voiceover(text=tr("""Otra vez es la posición la que dice a qué país corresponde cada dato: <bookmark mark='us'/> el quinto número es el crecimiento de Estados Unidos.<bookmark mark='v4'/>""",
                                    """Once again, it is the position that tells which country each figure belongs to: <bookmark mark='us'/> the fifth number is the growth of the United States.""")) as tracker:
            self.wait_until_bookmark("us")
            self.play(FadeIn(f_us), run_time=0.8)
        
        with self.voiceover(text=tr("""Omega busca el país que no creció en 2003.""",
                                    """Omega is looking for the country that did not grow in 2003.""")) as tracker:
            self.play(FadeOut(f_us), run_time=0.5)
            entra(self, om)
            self.play(FadeIn(globo, scale=0.8), run_time=0.6)
        
        self.wait(1.5)   # un instante para buscarlo (sin tarjeta de pausa: es inmediato)
        self.play(Indicate(d.get_entries()[2], color=COLOR_ESCALAR, scale_factor=1.3), run_time=1.2)
        
        f_al = banda(d, 2, x0, x1)
        # el inglés difiere del español publicado: «Indeed» confirmaba algo que nadie había dicho (Marcos, 2026-10-30)
        with self.voiceover(text=tr("""Efectivamente, es <bookmark mark='al'/> Alemania: su dato es negativo, así que su PIB disminuyó ese año.""",
                                    """The answer is <bookmark mark='al'/> Germany: its figure is negative, so its GDP shrank that year.""")) as tracker:
            self.play(FadeOut(globo), run_time=0.4)
            self.wait_until_bookmark("al")
            self.play(FadeIn(f_al), run_time=0.8)
            cambia(self, om, "neutral", mira=LEFT)   # sin sonrisa: es un mal dato
            parpadea(self, om)
        
        self.pausa_media()


class L01_V08_E05_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        ds = VGroup(*[vector(PIB[a], decimales=1) for a in PIB]).arrange(RIGHT, buff=0.6).move_to([1, 0.1, 0])
        nombres = VGroup(*[MathTex(rf"\Vect[{a}]{{p}}", tex_template=myTemplate, font_size=40).next_to(v, UP, buff=0.3) for a, v in zip(PIB, ds)])
        paises = leyenda(PAISES, ds[0], font_size=32)
        resumen = Tex(tr("Cada posición corresponde siempre a lo mismo:\\\\ un ingrediente, un país...",
                         "Each position always refers to the same thing:\\\\ an ingredient, a country..."), font_size=34).to_edge(DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""Con datos de cuatro años tenemos cuatro vectores, <bookmark mark='a'/> uno por año, con los países siempre en el mismo orden.""",
                                    """With data for four years we have four vectors, <bookmark mark='a'/> one per year, with the countries always in the same order.""")) as tracker:
            self.play(FadeIn(paises), run_time=0.8)
            self.wait_until_bookmark("a")
            self.play(LaggedStart(*[FadeIn(VGroup(v, n)) for v, n in zip(ds, nombres)], lag_ratio=0.4), run_time=2)
        
        with self.voiceover(text=tr("""Resumamos. Un vector puede guardar datos: <bookmark mark='r'/> cada posición corresponde siempre a lo mismo; por ejemplo un ingrediente o un país. Con las recetas, eso nos permitió sumar componente a componente y multiplicar por un número.""",
                                    """Let us sum up. A vector can store data: <bookmark mark='r'/> each position always refers to the same thing; for example, an ingredient or a country. With the recipes, this let us add component-wise and multiply by a number.""")) as tracker:
            self.wait_until_bookmark("r")
            self.play(FadeIn(resumen), run_time=1)
        
        fila = banda(ds[0], 2, paises.get_left()[0] - 0.15, ds[-1].get_right()[0] + 0.15)   # Alemania
        with self.voiceover(text=tr("""Para guardar juntos los cuatro vectores, basta ponerlos uno al lado del otro, <bookmark mark='f'/> lo que nos permite ver la evolución del crecimiento de cada país en su correspondiente fila.""",
                                    """To store the four vectors together, we just place them side by side, <bookmark mark='f'/> which lets us follow how each country's growth evolves along its own row.""")) as tracker:
            self.play(Indicate(ds, color=COLOR_RESULTADO, scale_factor=1.05), run_time=1.5)
            self.wait_until_bookmark("f")
            self.play(FadeIn(fila), run_time=0.8)
        
        self.wait(0.5)   # una pausa antes de anunciar el próximo vídeo (Marcos, 2026-10-26)
        with self.voiceover(text=tr("""En el próximo vídeo esa tabla de números tendrá nombre: una matriz.""",
                                    """In the next video this table of numbers will get a name: a matrix.""")) as tracker:
            self.play(FadeOut(fila), Create(SurroundingRectangle(ds, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15)), run_time=1.2)
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
