from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Propiedades del producto por escalares en ", "Properties of scalar multiplication in ") + r"\R[n]"

PROPIEDADES_REALES = [r"a+b=b+a", r"a+(b+c)=(a+b)+c", r"a+0=a", r"a+(-a)=0",
                      r"ab=ba", r"a(b+c)=ab+ac", r"a(bc)=(ab)c", r"1a=a"]

PROPIEDADES_SUMA = [r"\Vect{a}+\Vect{b}=\Vect{b}+\Vect{a}",
                    r"\Vect{a}+(\Vect{b}+\Vect{c})=(\Vect{a}+\Vect{b})+\Vect{c}",
                    r"\Vect{a}+\Vect{0}=\Vect{a}",
                    r"\Vect{a}+(-\Vect{a})=\Vect{0}"]

PROPIEDADES_PRODUCTO = [r"\lambda(\Vect{a}+\Vect{b})=\lambda\Vect{a}+\lambda\Vect{b}",
                        r"(\lambda+\varphi)\Vect{a}=\lambda\Vect{a}+\varphi\Vect{a}",
                        r"\lambda(\varphi\Vect{a})=(\lambda\varphi)\Vect{a}",
                        r"1\Vect{a}=\Vect{a}"]

CAMPANITA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos", "campanita.wav")   # suena al subir un contador

DEFINICIONES = [("suma",     r"\elemRp{\Vect{a}+\Vect{b}}{i}=\eleVR{a}{i}+\eleVR{b}{i}"),
                ("producto", r"\elemRp{\lambda\Vect{a}}{i}=\lambda\eleVRpE{a}{i}")]


class Panel:
    """Panel fijo de herramientas: definiciones a la izquierda y propiedades de los reales a la
    derecha. Las piezas se identifican por clave ("suma", "producto", 5, 6, ...)."""
    def __init__(self, escena, reales=range(5, 9), atenuadas=(), y_sup=2.95, font_size=28):
        self.escena, self.piezas, self.usos, self.contadores = escena, {}, {}, {}
        izq = VGroup(*[MathTex(f, tex_template=myTemplate, font_size=font_size) for _, f in DEFINICIONES])
        izq.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for (clave, _), m in zip(DEFINICIONES, izq):
            self.piezas[clave] = m
        der = VGroup(*[MathTex(f"{k}.\\;", PROPIEDADES_REALES[k-1], tex_template=myTemplate, font_size=font_size)
                       for k in reales]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for k, m in zip(reales, der):
            self.piezas[k] = m
        cab_izq = Tex(tr("Definiciones", "Definitions"), font_size=24).set_color(GRAY_B)
        cab_der = Tex(tr("Números reales", "Real numbers"), font_size=24).set_color(GRAY_B)
        self.izq = VGroup(cab_izq, izq).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=0.35)
        self.der = VGroup(cab_der, der).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=1.1)
        for g in (self.izq, self.der):
            g.align_to([0, y_sup, 0], UP)
        self.atenuadas = set(atenuadas)
        for clave in atenuadas:
            self.piezas[clave].set_opacity(0.3)
        self.todo = VGroup(self.izq, self.der)

    def enciende(self, *claves, run_time=0.8):
        """Trae al frente piezas atenuadas (cuando entran en juego)."""
        self.atenuadas -= set(claves)
        self.escena.play(*[self.piezas[c].animate.set_opacity(1) for c in claves], run_time=run_time)

    def pista(self, *claves, run_time=1):
        """La pista: las piezas que hacen falta se iluminan en amarillo y se recuadran."""
        self.atenuadas -= set(claves)
        self.marcos = VGroup(*[SurroundingRectangle(self.piezas[c], color=COLOR_ESCALAR, buff=0.1,
                                                    corner_radius=0.1, stroke_width=2) for c in claves])
        self.escena.play(*[self.piezas[c].animate.set_color(COLOR_ESCALAR).set_opacity(1) for c in claves],
                         Create(self.marcos), run_time=run_time)

    def senala(self, clave, run_time=0.8):
        """Antes de dar un paso: la pieza que se va a usar parpadea."""
        self.escena.play(Indicate(self.piezas[clave], color=COLOR_RESULTADO, scale_factor=1.12), run_time=run_time)

    def cuenta(self, clave, run_time=0.5):
        """Después del paso: sube el contador de usos de la pieza, con una campanita."""
        pieza = self.piezas[clave]
        self.usos[clave] = self.usos.get(clave, 0) + 1
        # insignia: disco de color con el número de usos dentro (no se confunde con parte de la fórmula)
        disco = Circle(radius=0.17, fill_color=COLOR_TITULO, fill_opacity=1, stroke_width=0)
        numero = Tex(f"\\textbf{{{self.usos[clave]}}}", font_size=24).set_color(WHITE).move_to(disco)
        nuevo = VGroup(disco, numero).next_to(pieza, RIGHT, buff=0.3).shift(0.1*UP)
        self.escena.add_sound(CAMPANITA)
        if clave in self.contadores:
            self.escena.play(ReplacementTransform(self.contadores[clave], nuevo), run_time=run_time)
        else:
            self.escena.play(FadeIn(nuevo, scale=0.5), run_time=run_time)
        self.contadores[clave] = nuevo


def cabecera_y_enunciado(escena, texto, numero):
    """Cabecera de la escena (lleva el número de la propiedad) y enunciado de la propiedad `numero`
    (5 a 8), sin numerar, en el hueco entre los dos lados del panel."""
    cabecera = Tex(texto, tex_template=myTemplate, font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
    enunciado = MathTex(PROPIEDADES_PRODUCTO[numero-5], tex_template=myTemplate, font_size=40).set_color(COLOR_RESULTADO)
    enunciado.scale_to_fit_width(min(enunciado.width, 4.6)).move_to([-0.3, 2.2, 0])
    escena.add(cabecera)
    return cabecera, enunciado


def linea(*formula, de_reales=False):
    """Una línea de la cadena de igualdades (en teal si el paso es una operación entre números reales);
    en varios trozos si hay que resaltar una parte."""
    return MathTex(*formula, tex_template=myTemplate, font_size=36).set_color(COLOR_REGLA if de_reales else WHITE)


def coloca_cadena(cadena, y_sup=0.55, salto=0.66, x_izq=-3.3, sangria=0.6):
    """Coloca la cadena bajo el enunciado y entre los dos lados del panel: la primera línea en x_izq y
    las siguientes (que empiezan por '=') alineadas entre sí y desplazadas `sangria` a la derecha."""
    for k, l in enumerate(cadena):
        l.move_to([0, y_sup - k*salto, 0]).align_to([x_izq + (sangria if k else 0), 0, 0], LEFT)
    return cadena


def paso(escena, l, panel, clave, run_time=1, veces=1):
    """Un paso de la cadena: parpadea la pieza que se va a usar (la voz la acaba de nombrar), se
    escribe la línea y sube el contador con la campanita (dos veces si se aplica en dos sumandos)."""
    panel.senala(clave)
    escena.play(Write(l), run_time=run_time)
    for _ in range(veces):
        panel.cuenta(clave)


def concluye(escena, enunciado, texto_es, texto_en, cadena=None):
    """Cierre de cada demostración: i es cualquiera, luego los vectores son iguales (en la marca 'cc'
    se destacan los dos extremos de la cadena) y al final se enciende el enunciado."""
    with escena.voiceover(text=tr(texto_es, texto_en)) as tracker:
        # manim-voiceover sitúa al final del audio una marca en la posición 0 del texto (interpola
        # antes de la primera palabra): una marca al principio significa "ya", sin esperar
        bt = {m: (tracker.start_t if tracker.bookmark_distances[m] == 0 else t) for m, t in tracker.bookmark_times.items()}
        if cadena is not None and "cc" in bt:
            if bt["cc"] - escena.renderer.time > 0.01: escena.wait(bt["cc"] - escena.renderer.time)
            rt = min(3, max(0.8, bt["ok"] - bt["cc"])) if "ok" in bt else 1.5   # dura lo que la frase, hasta el recuadro
            escena.play(Indicate(cadena[0], color=COLOR_ESCALAR, scale_factor=1.15),
                        Indicate(cadena[-1], color=COLOR_ESCALAR, scale_factor=1.15), run_time=rt)
        if "ok" in bt:
            if bt["ok"] - escena.renderer.time > 0.01: escena.wait(bt["ok"] - escena.renderer.time)
        # lo demostrado: recuadro amarillo y parpadeo del enunciado
        marco = SurroundingRectangle(enunciado, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
        escena.play(Create(marco), Indicate(enunciado, color=COLOR_RESULTADO, scale_factor=1.15), run_time=1.5)
        restante = tracker.start_t + tracker.duration - escena.renderer.time
        escena.pausa(max(0.3, restante))

class L01_V07_PropiedadesDelProductoPorEscalares(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        
        titulo = Title(TITULO, tex_template=myTemplate, font_size=50).set_color(COLOR_TITULO)
        self.play(Write(titulo))
        
        with self.voiceover(text=tr("""En el vídeo anterior demostramos cuatro propiedades de la suma de vectores. En este demostraremos cuatro propiedades del producto por un escalar.""",
                                    """In the previous video we proved four properties of vector addition. In this one we will prove four properties of scalar multiplication.""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        # Cuatro ejemplos numéricos en R2 (ilustran, no demuestran): una fila por propiedad
        def v(x, y):
            return r"\begin{pmatrix}" + f"{x}\\\\{y}" + r"\end{pmatrix}"
        A, B = v(1, 2), v(2, 1)
        ESCALARES = {"2", "3", "1", r"(2+3)", r"(2\cdot 3)"}
        ejemplos = VGroup(
            MathTex("2", r"\left(", A, "+", B, r"\right)", "=", v(6, 6), "=", "2", A, "+", "2", B,
                    tex_template=myTemplate, font_size=36),
            MathTex(r"(2+3)", A, "=", v(5, 10), "=", "2", A, "+", "3", A, tex_template=myTemplate, font_size=36),
            MathTex("2", r"\left(", "3", A, r"\right)", "=", v(6, 12), "=", r"(2\cdot 3)", A, tex_template=myTemplate, font_size=36),
            MathTex("1", A, "=", A, tex_template=myTemplate, font_size=36))
        for ej in ejemplos:   # colores: a azul, b naranja, escalares amarillo
            for k, parte in enumerate(ej):
                texto = ej.tex_strings[k]
                if texto == A: parte.set_color(COLOR_A)
                elif texto == B: parte.set_color(COLOR_B)
                elif texto in ESCALARES: parte.set_color(COLOR_ESCALAR)
        ejemplos.arrange(DOWN, buff=0.35).next_to(titulo, DOWN, buff=0.5)
        pregunta = Tex(tr("¿Característica de los ejemplos, o propiedades generales?", "Peculiar to the examples, or general properties?"),
                       font_size=40).set_color(COLOR_ESCALAR).next_to(ejemplos, DOWN, buff=0.45)
        
        with self.voiceover(text=tr("""En los siguientes ejemplos vemos que: <bookmark mark='e1'/> reescalar una suma de vectores da lo mismo que sumar los reescalados, <bookmark mark='e2'/> y lo mismo ocurre al reescalar por una suma de escalares. <bookmark mark='e3'/> Reescalar dos veces es reescalar por el producto de los escalares. <bookmark mark='e4'/> Y reescalar por uno no cambia nada.""",
                                    """In the following examples we see that: <bookmark mark='e1'/> scaling a sum of vectors gives the same as adding the scaled vectors, <bookmark mark='e2'/> and the same happens when scaling by a sum of scalars. <bookmark mark='e3'/> Scaling twice is scaling by the product of the scalars. <bookmark mark='e4'/> And scaling by one changes nothing.""")) as tracker:
            for k, marca in enumerate(["e1", "e2", "e3", "e4"]):
                self.wait_until_bookmark(marca)
                self.play(FadeIn(ejemplos[k]), run_time=0.8)
        
        with self.voiceover(text=tr("""Como hicimos con la suma, vamos a demostrar que son propiedades generales del producto por un escalar.""",
                                    """As we did with addition, we are going to prove that these are general properties of scalar multiplication.""")) as tracker:
            self.play(Write(pregunta), run_time=1.5)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("El método", "The method"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.play(Write(cabecera))
        
        criterio = MathTex(r"\Vect{v}=\Vect{w}", r"\quad\Longleftrightarrow\quad",
                           r"\eleVR{v}{i}=\eleVR{w}{i}", tex_template=myTemplate, font_size=44)
        definiciones = VGroup(*[MathTex(f, tex_template=myTemplate, font_size=40) for _, f in DEFINICIONES]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        reales = VGroup(*[MathTex(f"{k}.\\;\\;", PROPIEDADES_REALES[k-1], tex_template=myTemplate, font_size=40).set_color(COLOR_REGLA)
                          for k in range(5, 9)]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        herramientas = VGroup(definiciones, reales).arrange(RIGHT, buff=1.5, aligned_edge=UP)
        una_regla = Tex(tr("una sola definición o una sola propiedad de los reales en cada paso",
                           "a single definition or a single property of the reals at each step"),
                        font_size=34).set_color(COLOR_REGLA)
        VGroup(criterio, herramientas, una_regla).arrange(DOWN, buff=0.7).next_to(cabecera, DOWN, buff=0.6)
        
        with self.voiceover(text=tr("""El método es el del vídeo anterior. Para demostrar que dos vectores son iguales, basta demostrar que <bookmark mark='cc'/> lo son componente a componente.<bookmark mark='v4'/>""",
                                    """The method is the one from the previous video. To prove that two vectors are equal, it is enough to prove that <bookmark mark='cc'/> they are equal component-wise.""")) as tracker:
            self.play(Write(criterio), run_time=2)
            self.wait_until_bookmark("cc")   # la igualdad de las componentes, cuando la voz dice "componente a componente"
            self.play(Indicate(criterio[2], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1.5)
        
        with self.voiceover(text=tr("""Hoy solo necesitamos dos definiciones: <bookmark mark='s'/> la suma, que distribuye el selector, <bookmark mark='p'/> y el producto por un escalar, que desplaza el paréntesis. Y, de las propiedades de los reales, <bookmark mark='r'/> las cuatro del producto.""",
                                    """Today we only need two definitions: <bookmark mark='s'/> addition, which distributes the selector, <bookmark mark='p'/> and scalar multiplication, which shifts the parentheses. And, of the properties of the reals, <bookmark mark='r'/> the four for multiplication.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(Write(definiciones[0]), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(Write(definiciones[1]), run_time=0.8)
            self.wait_until_bookmark("r")
            self.play(FadeIn(reales), run_time=1)
        
        with self.voiceover(text=tr("""Cada demostración es una cadena de igualdades con una sola definición o una sola propiedad de los reales en cada paso.""",
                                    """Each proof is a chain of equalities with a single definition or a single property of the reals at each step.""")) as tracker:
            self.play(FadeIn(una_regla), run_time=1)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 5: distributiva respecto de la suma de vectores",
                                                             "Property 5: distributive over vector addition"), 5)
        
        panel = Panel(self)
        with self.voiceover(text=tr("""De nuevo, las herramientas a la vista: a la izquierda, <bookmark mark='izq'/> las definiciones; a la derecha, <bookmark mark='der'/> las cuatro propiedades del producto de números reales.""",
                                    """Again, the tools in sight: on the left, <bookmark mark='izq'/> the definitions; on the right, <bookmark mark='der'/> the four properties of the multiplication of real numbers.""")) as tracker:
            self.wait_until_bookmark("izq")
            self.play(FadeIn(panel.izq), run_time=1)
            self.wait_until_bookmark("der")
            self.play(FadeIn(panel.der), run_time=1)
        
        with self.voiceover(text=tr("""Quinta propiedad: el producto por un escalar es distributivo respecto de la suma de vectores. Reescalar una suma es sumar los reescalados.""",
                                    """Fifth property: scalar multiplication is distributive over vector addition. Scaling a sum is adding the scaled vectors.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Para demostrarla necesitará <bookmark mark='p'/> las dos definiciones y la propiedad seis de los reales, la distributiva.<bookmark mark='v3'/>""",
                                    """To prove it you will need <bookmark mark='p'/> both definitions and property six of the reals, the distributive property.""")) as tracker:
            self.wait_until_bookmark("p")
            panel.pista("suma", "producto", 6)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemRp{\lambda(\Vect{a}+\Vect{b})}{i}"),
                                linea(r"=\lambda\big(\elemRp{\Vect{a}+\Vect{b}}{i}\big)"),
                                linea(r"=\lambda\big(\eleVR{a}{i}+\eleVR{b}{i}\big)"),
                                linea(r"=\lambda", r"\eleVRpE{a}{i}", r"+\lambda", r"\eleVRpE{b}{i}", de_reales=True),
                                linea(r"=\elemRp{\lambda\Vect{a}}{i}+\elemRp{\lambda\Vect{b}}{i}"),
                                linea(r"=\elemRp{\lambda\Vect{a}+\lambda\Vect{b}}{i}")])
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis. <bookmark mark='l1'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "producto")
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l2'/>""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, "suma")
        
        with self.voiceover(text=tr("""Ya todo son números reales, así que podemos aplicar la propiedad distributiva. <bookmark mark='l3'/>""",
                                    """Now everything is real numbers, so we can apply the distributive property. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 6)
        
        with self.voiceover(text=tr("""Cada componente va entre paréntesis para que quede claro que el escalar multiplica a la componente, y no al vector.""",
                                    """Each component goes in parentheses to make clear that the scalar multiplies the component, not the vector.""")) as tracker:
            self.play(Indicate(cadena[3][1], color=COLOR_ESCALAR, scale_factor=1.15),
                      Indicate(cadena[3][3], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1.5)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis en los dos sumandos. <bookmark mark='l4'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses in both terms. <bookmark mark='l4'/>""")) as tracker:
            self.wait_until_bookmark("l4")
            paso(self, cadena[4], panel, "producto", veces=2)
        
        with self.voiceover(text=tr("""Y por la definición de suma podemos sacar el selector como factor común. <bookmark mark='l5'/>""",
                                    """And by the definition of addition we can factor out the selector. <bookmark mark='l5'/>""")) as tracker:
            self.wait_until_bookmark("l5")
            paso(self, cadena[5], panel, "suma")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> los dos vectores son iguales. Hemos usado tres veces la definición de producto, dos la de suma y una sola vez la distributiva.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> the two vectors are equal. We have used the definition of scalar multiplication three times, that of addition twice, and the distributive property only once.""",
                 cadena=cadena)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 6: distributiva respecto de la suma de escalares",
                                                             "Property 6: distributive over scalar addition"), 6)
        panel = Panel(self)
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Sexta propiedad: también es distributivo respecto de la suma de escalares. Reescalar por una suma de escalares es sumar los reescalados.""",
                                    """Sixth property: it is also distributive over the addition of scalars. Scaling by a sum of scalars is adding the scaled vectors.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Esta vez hará falta más de una propiedad de los reales: necesitará <bookmark mark='p'/> las dos definiciones, la conmutativa y la distributiva.""",
                                    """This time more than one property of the reals will be needed: you will need <bookmark mark='p'/> both definitions, the commutative property and the distributive property.""")) as tracker:
            self.wait_until_bookmark("p")
            panel.pista("suma", "producto", 5, 6)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemRp{(\lambda+\varphi)\Vect{a}}{i}"),
                                linea(r"=(\lambda+\varphi)\eleVRpE{a}{i}"),
                                linea(r"=\eleVRpE{a}{i}(\lambda+\varphi)", de_reales=True),
                                linea(r"=\eleVRpE{a}{i}\lambda+\eleVRpE{a}{i}\varphi", de_reales=True),
                                linea(r"=\lambda\eleVRpE{a}{i}+\varphi\eleVRpE{a}{i}", de_reales=True),
                                linea(r"=\elemRp{\lambda\Vect{a}}{i}+\elemRp{\varphi\Vect{a}}{i}"),
                                linea(r"=\elemRp{\lambda\Vect{a}+\varphi\Vect{a}}{i}")],
                               salto=0.6)
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis. <bookmark mark='l1'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "producto")
        
        with self.voiceover(text=tr("""La distributiva que tenemos lleva el factor común a la izquierda. Así que primero, por la conmutativa, podemos cambiar el orden de los factores. <bookmark mark='l2'/>""",
                                    """The distributive property we have puts the common factor on the left. So first, by the commutative property, we can change the order of the factors. <bookmark mark='l2'/>""")) as tracker:
            panel.senala(6)   # "la distributiva que tenemos": la del panel
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, 5)
        
        with self.voiceover(text=tr("""Ahora sí podemos aplicar la distributiva. <bookmark mark='l3'/>""",
                                    """Now we can apply the distributive property. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 6)
        
        with self.voiceover(text=tr("""Y por la conmutativa podemos cambiar de nuevo el orden de los factores en los dos sumandos. <bookmark mark='l4'/>""",
                                    """And by the commutative property we can change the order of the factors again in both terms. <bookmark mark='l4'/>""")) as tracker:
            self.wait_until_bookmark("l4")
            paso(self, cadena[4], panel, 5, veces=2)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis en los dos sumandos. <bookmark mark='l5'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses in both terms. <bookmark mark='l5'/>""")) as tracker:
            self.wait_until_bookmark("l5")
            paso(self, cadena[5], panel, "producto", veces=2)
        
        with self.voiceover(text=tr("""Y por la definición de suma podemos sacar el selector como factor común. <bookmark mark='l6'/>""",
                                    """And by the definition of addition we can factor out the selector. <bookmark mark='l6'/>""")) as tracker:
            self.wait_until_bookmark("l6")
            paso(self, cadena[6], panel, "suma")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> los dos vectores son iguales. Esta vez hemos necesitado cuatro veces las propiedades de los reales, porque las reglas son exactamente las que son, y hay que aplicarlas tal como están escritas.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> the two vectors are equal. This time we have needed the properties of the reals four times, because the rules are exactly what they are, and they must be applied just as they are written.""",
                 cadena=cadena)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 7: asociativa", "Property 7: associative"), 7)
        panel = Panel(self)
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Séptima propiedad: reescalar dos veces es reescalar por el producto de los escalares.""",
                                    """Seventh property: scaling twice is scaling by the product of the scalars.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Para demostrarla necesitará <bookmark mark='p'/> la definición de producto y la propiedad siete de los reales, la asociativa.""",
                                    """To prove it you will need <bookmark mark='p'/> the definition of scalar multiplication and property seven of the reals, the associative property.""")) as tracker:
            self.wait_until_bookmark("p")
            panel.pista("producto", 7)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemRp{\lambda(\varphi\Vect{a})}{i}"),
                                linea(r"=\lambda\big(\elemRp{\varphi\Vect{a}}{i}\big)"),
                                linea(r"=\lambda\big(\varphi\eleVRpE{a}{i}\big)"),
                                linea(r"=(\lambda\varphi)\eleVRpE{a}{i}", de_reales=True),
                                linea(r"=\elemRp{(\lambda\varphi)\Vect{a}}{i}")])
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis. <bookmark mark='l1'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "producto")
        
        with self.voiceover(text=tr("""Y otra vez, dentro, podemos desplazar el paréntesis. <bookmark mark='l2'/>""",
                                    """And once more, inside, we can shift the parentheses. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, "producto")
        
        with self.voiceover(text=tr("""Ya todo son números reales, así que podemos aplicar la asociativa. <bookmark mark='l3'/>""",
                                    """Now everything is real numbers, so we can apply the associative property. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 7)
        
        with self.voiceover(text=tr("""Y por la definición de producto podemos desplazar de nuevo el paréntesis. <bookmark mark='l4'/>""",
                                    """And by the definition of scalar multiplication we can shift the parentheses again. <bookmark mark='l4'/>""")) as tracker:
            self.wait_until_bookmark("l4")
            paso(self, cadena[4], panel, "producto")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> los dos vectores son iguales. Hemos usado tres veces la definición de producto y una sola vez la asociativa.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> the two vectors are equal. We have used the definition of scalar multiplication three times and the associative property only once.""",
                 cadena=cadena)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 8: el uno es el elemento neutro",
                                                             "Property 8: one is the identity element"), 8)
        panel = Panel(self)
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Octava y última propiedad: reescalar por uno no cambia nada.""",
                                    """Eighth and last property: scaling by one changes nothing.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Para demostrarla bastan <bookmark mark='p'/> la definición de producto y la propiedad ocho de los reales.""",
                                    """To prove it, <bookmark mark='p'/> the definition of scalar multiplication and property eight of the reals are enough.""")) as tracker:
            self.wait_until_bookmark("p")
            panel.pista("producto", 8)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemRp{1\Vect{a}}{i}"),
                                linea(r"=1\eleVRpE{a}{i}"),
                                linea(r"=\eleVRpE{a}{i}", de_reales=True)])
        # la misma línea sin el paréntesis, que sobra (no es un paso de la demostración)
        sin_parentesis = linea(r"=\eleVR{a}{i}", de_reales=True).align_to(cadena[2], LEFT).align_to(cadena[2], DOWN)
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis. <bookmark mark='l1'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "producto")
        
        with self.voiceover(text=tr("""Y por la propiedad ocho de los reales podemos quitar el uno. <bookmark mark='l2'/>""",
                                    """And property eight of the reals lets us drop the one. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, 8)
        
        with self.voiceover(text=tr("""Los paréntesis indican el orden de las operaciones: primero se hace lo de dentro, y después lo de fuera. Aquí fuera no queda ninguna operación, así que el paréntesis sobra <bookmark mark='q'/> y podemos quitarlo.""",
                                    """Parentheses indicate the order of operations: first what is inside, and then what is outside. Here nothing is left outside, so the parentheses are unnecessary <bookmark mark='q'/> and we can drop them.""")) as tracker:
            self.play(Indicate(cadena[2], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1.5)
            self.wait_until_bookmark("q")
            self.play(TransformMatchingShapes(cadena[2], sin_parentesis), run_time=1)
            cadena[2] = sin_parentesis
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> reescalar por uno deja el vector igual. Es la demostración más corta: solo dos pasos.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> scaling by one leaves the vector unchanged. It is the shortest proof: just two steps.""",
                 cadena=cadena)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        para = Tex(tr(r"Para cualesquiera $\Vect{a},\Vect{b},\Vect{c}\in\R[n]$ y escalares $\lambda,\varphi$:",
                      r"For any $\Vect{a},\Vect{b},\Vect{c}\in\R[n]$ and scalars $\lambda,\varphi$:"),
                   tex_template=myTemplate, font_size=36).next_to(cabecera, DOWN, buff=0.4)
        col_suma = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=38)
                            for k, p in enumerate(PROPIEDADES_SUMA)]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        col_prod = VGroup(*[MathTex(f"{k+5}.\\;\\;", p, tex_template=myTemplate, font_size=38)
                            for k, p in enumerate(PROPIEDADES_PRODUCTO)]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        tabla = VGroup(col_suma, col_prod).arrange(RIGHT, buff=1.2, aligned_edge=UP).next_to(para, DOWN, buff=0.5)
        tabla.scale_to_fit_width(min(tabla.width, config.frame_width*0.9)).set_x(0)
        for k in range(4):   # misma rejilla de filas
            col_prod[k].set_y(col_suma[k].get_y())
        espacio = Tex(tr("Estas ocho propiedades definirán el \\emph{espacio vectorial}",
                         "These eight properties will define a \\emph{vector space}"),
                      font_size=36).set_color(COLOR_ESCALAR).next_to(tabla, DOWN, buff=0.6)
        
        with self.voiceover(text=tr("""Resumamos. Con este vídeo y el anterior hemos demostrado las ocho propiedades de las operaciones con vectores: <bookmark mark='s'/> cuatro de la suma <bookmark mark='p'/> y cuatro del producto por un escalar.""",
                                    """Let us sum up. With this video and the previous one we have proved the eight properties of the operations with vectors: <bookmark mark='s'/> four for addition <bookmark mark='p'/> and four for scalar multiplication.""")) as tracker:
            self.play(FadeIn(para), run_time=0.8)
            self.wait_until_bookmark("s")
            self.play(FadeIn(col_suma), run_time=1)
            self.wait_until_bookmark("p")
            self.play(FadeIn(col_prod), run_time=1)
        
        with self.voiceover(text=tr("""Más adelante en el curso, estas ocho propiedades serán las que definan qué es un espacio vectorial.""",
                                    """Later in the course, these eight properties will be the ones that define what a vector space is.""")) as tracker:
            self.play(FadeIn(espacio), run_time=1)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos los vectores como una forma de representar datos.""",
                                    """In the next video we will see vectors as a way of representing data.""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos_finales()


class L01_V07_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class L01_V07_E01_Ejemplos(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        
        titulo = Title(TITULO, tex_template=myTemplate, font_size=50).set_color(COLOR_TITULO)
        self.play(Write(titulo))
        
        with self.voiceover(text=tr("""En el vídeo anterior demostramos cuatro propiedades de la suma de vectores. En este demostraremos cuatro propiedades del producto por un escalar.""",
                                    """In the previous video we proved four properties of vector addition. In this one we will prove four properties of scalar multiplication.""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        # Cuatro ejemplos numéricos en R2 (ilustran, no demuestran): una fila por propiedad
        def v(x, y):
            return r"\begin{pmatrix}" + f"{x}\\\\{y}" + r"\end{pmatrix}"
        A, B = v(1, 2), v(2, 1)
        ESCALARES = {"2", "3", "1", r"(2+3)", r"(2\cdot 3)"}
        ejemplos = VGroup(
            MathTex("2", r"\left(", A, "+", B, r"\right)", "=", v(6, 6), "=", "2", A, "+", "2", B,
                    tex_template=myTemplate, font_size=36),
            MathTex(r"(2+3)", A, "=", v(5, 10), "=", "2", A, "+", "3", A, tex_template=myTemplate, font_size=36),
            MathTex("2", r"\left(", "3", A, r"\right)", "=", v(6, 12), "=", r"(2\cdot 3)", A, tex_template=myTemplate, font_size=36),
            MathTex("1", A, "=", A, tex_template=myTemplate, font_size=36))
        for ej in ejemplos:   # colores: a azul, b naranja, escalares amarillo
            for k, parte in enumerate(ej):
                texto = ej.tex_strings[k]
                if texto == A: parte.set_color(COLOR_A)
                elif texto == B: parte.set_color(COLOR_B)
                elif texto in ESCALARES: parte.set_color(COLOR_ESCALAR)
        ejemplos.arrange(DOWN, buff=0.35).next_to(titulo, DOWN, buff=0.5)
        pregunta = Tex(tr("¿Característica de los ejemplos, o propiedades generales?", "Peculiar to the examples, or general properties?"),
                       font_size=40).set_color(COLOR_ESCALAR).next_to(ejemplos, DOWN, buff=0.45)
        
        with self.voiceover(text=tr("""En los siguientes ejemplos vemos que: <bookmark mark='e1'/> reescalar una suma de vectores da lo mismo que sumar los reescalados, <bookmark mark='e2'/> y lo mismo ocurre al reescalar por una suma de escalares. <bookmark mark='e3'/> Reescalar dos veces es reescalar por el producto de los escalares. <bookmark mark='e4'/> Y reescalar por uno no cambia nada.""",
                                    """In the following examples we see that: <bookmark mark='e1'/> scaling a sum of vectors gives the same as adding the scaled vectors, <bookmark mark='e2'/> and the same happens when scaling by a sum of scalars. <bookmark mark='e3'/> Scaling twice is scaling by the product of the scalars. <bookmark mark='e4'/> And scaling by one changes nothing.""")) as tracker:
            for k, marca in enumerate(["e1", "e2", "e3", "e4"]):
                self.wait_until_bookmark(marca)
                self.play(FadeIn(ejemplos[k]), run_time=0.8)
        
        with self.voiceover(text=tr("""Como hicimos con la suma, vamos a demostrar que son propiedades generales del producto por un escalar.""",
                                    """As we did with addition, we are going to prove that these are general properties of scalar multiplication.""")) as tracker:
            self.play(Write(pregunta), run_time=1.5)
        
        self.pausa_media()


class L01_V07_E02_Metodo(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("El método", "The method"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.play(Write(cabecera))
        
        criterio = MathTex(r"\Vect{v}=\Vect{w}", r"\quad\Longleftrightarrow\quad",
                           r"\eleVR{v}{i}=\eleVR{w}{i}", tex_template=myTemplate, font_size=44)
        definiciones = VGroup(*[MathTex(f, tex_template=myTemplate, font_size=40) for _, f in DEFINICIONES]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        reales = VGroup(*[MathTex(f"{k}.\\;\\;", PROPIEDADES_REALES[k-1], tex_template=myTemplate, font_size=40).set_color(COLOR_REGLA)
                          for k in range(5, 9)]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        herramientas = VGroup(definiciones, reales).arrange(RIGHT, buff=1.5, aligned_edge=UP)
        una_regla = Tex(tr("una sola definición o una sola propiedad de los reales en cada paso",
                           "a single definition or a single property of the reals at each step"),
                        font_size=34).set_color(COLOR_REGLA)
        VGroup(criterio, herramientas, una_regla).arrange(DOWN, buff=0.7).next_to(cabecera, DOWN, buff=0.6)
        
        with self.voiceover(text=tr("""El método es el del vídeo anterior. Para demostrar que dos vectores son iguales, basta demostrar que <bookmark mark='cc'/> lo son componente a componente.<bookmark mark='v4'/>""",
                                    """The method is the one from the previous video. To prove that two vectors are equal, it is enough to prove that <bookmark mark='cc'/> they are equal component-wise.""")) as tracker:
            self.play(Write(criterio), run_time=2)
            self.wait_until_bookmark("cc")   # la igualdad de las componentes, cuando la voz dice "componente a componente"
            self.play(Indicate(criterio[2], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1.5)
        
        with self.voiceover(text=tr("""Hoy solo necesitamos dos definiciones: <bookmark mark='s'/> la suma, que distribuye el selector, <bookmark mark='p'/> y el producto por un escalar, que desplaza el paréntesis. Y, de las propiedades de los reales, <bookmark mark='r'/> las cuatro del producto.""",
                                    """Today we only need two definitions: <bookmark mark='s'/> addition, which distributes the selector, <bookmark mark='p'/> and scalar multiplication, which shifts the parentheses. And, of the properties of the reals, <bookmark mark='r'/> the four for multiplication.""")) as tracker:
            self.wait_until_bookmark("s")
            self.play(Write(definiciones[0]), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(Write(definiciones[1]), run_time=0.8)
            self.wait_until_bookmark("r")
            self.play(FadeIn(reales), run_time=1)
        
        with self.voiceover(text=tr("""Cada demostración es una cadena de igualdades con una sola definición o una sola propiedad de los reales en cada paso.""",
                                    """Each proof is a chain of equalities with a single definition or a single property of the reals at each step.""")) as tracker:
            self.play(FadeIn(una_regla), run_time=1)
        
        self.pausa_media()


class L01_V07_E03_DistributivaVectores(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 5: distributiva respecto de la suma de vectores",
                                                             "Property 5: distributive over vector addition"), 5)
        
        panel = Panel(self)
        with self.voiceover(text=tr("""De nuevo, las herramientas a la vista: a la izquierda, <bookmark mark='izq'/> las definiciones; a la derecha, <bookmark mark='der'/> las cuatro propiedades del producto de números reales.""",
                                    """Again, the tools in sight: on the left, <bookmark mark='izq'/> the definitions; on the right, <bookmark mark='der'/> the four properties of the multiplication of real numbers.""")) as tracker:
            self.wait_until_bookmark("izq")
            self.play(FadeIn(panel.izq), run_time=1)
            self.wait_until_bookmark("der")
            self.play(FadeIn(panel.der), run_time=1)
        
        with self.voiceover(text=tr("""Quinta propiedad: el producto por un escalar es distributivo respecto de la suma de vectores. Reescalar una suma es sumar los reescalados.""",
                                    """Fifth property: scalar multiplication is distributive over vector addition. Scaling a sum is adding the scaled vectors.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Para demostrarla necesitará <bookmark mark='p'/> las dos definiciones y la propiedad seis de los reales, la distributiva.<bookmark mark='v3'/>""",
                                    """To prove it you will need <bookmark mark='p'/> both definitions and property six of the reals, the distributive property.""")) as tracker:
            self.wait_until_bookmark("p")
            panel.pista("suma", "producto", 6)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemRp{\lambda(\Vect{a}+\Vect{b})}{i}"),
                                linea(r"=\lambda\big(\elemRp{\Vect{a}+\Vect{b}}{i}\big)"),
                                linea(r"=\lambda\big(\eleVR{a}{i}+\eleVR{b}{i}\big)"),
                                linea(r"=\lambda", r"\eleVRpE{a}{i}", r"+\lambda", r"\eleVRpE{b}{i}", de_reales=True),
                                linea(r"=\elemRp{\lambda\Vect{a}}{i}+\elemRp{\lambda\Vect{b}}{i}"),
                                linea(r"=\elemRp{\lambda\Vect{a}+\lambda\Vect{b}}{i}")])
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis. <bookmark mark='l1'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "producto")
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l2'/>""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, "suma")
        
        with self.voiceover(text=tr("""Ya todo son números reales, así que podemos aplicar la propiedad distributiva. <bookmark mark='l3'/>""",
                                    """Now everything is real numbers, so we can apply the distributive property. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 6)
        
        with self.voiceover(text=tr("""Cada componente va entre paréntesis para que quede claro que el escalar multiplica a la componente, y no al vector.""",
                                    """Each component goes in parentheses to make clear that the scalar multiplies the component, not the vector.""")) as tracker:
            self.play(Indicate(cadena[3][1], color=COLOR_ESCALAR, scale_factor=1.15),
                      Indicate(cadena[3][3], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1.5)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis en los dos sumandos. <bookmark mark='l4'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses in both terms. <bookmark mark='l4'/>""")) as tracker:
            self.wait_until_bookmark("l4")
            paso(self, cadena[4], panel, "producto", veces=2)
        
        with self.voiceover(text=tr("""Y por la definición de suma podemos sacar el selector como factor común. <bookmark mark='l5'/>""",
                                    """And by the definition of addition we can factor out the selector. <bookmark mark='l5'/>""")) as tracker:
            self.wait_until_bookmark("l5")
            paso(self, cadena[5], panel, "suma")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> los dos vectores son iguales. Hemos usado tres veces la definición de producto, dos la de suma y una sola vez la distributiva.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> the two vectors are equal. We have used the definition of scalar multiplication three times, that of addition twice, and the distributive property only once.""",
                 cadena=cadena)
        
        self.pausa_media()


class L01_V07_E04_DistributivaEscalares(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 6: distributiva respecto de la suma de escalares",
                                                             "Property 6: distributive over scalar addition"), 6)
        panel = Panel(self)
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Sexta propiedad: también es distributivo respecto de la suma de escalares. Reescalar por una suma de escalares es sumar los reescalados.""",
                                    """Sixth property: it is also distributive over the addition of scalars. Scaling by a sum of scalars is adding the scaled vectors.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Esta vez hará falta más de una propiedad de los reales: necesitará <bookmark mark='p'/> las dos definiciones, la conmutativa y la distributiva.""",
                                    """This time more than one property of the reals will be needed: you will need <bookmark mark='p'/> both definitions, the commutative property and the distributive property.""")) as tracker:
            self.wait_until_bookmark("p")
            panel.pista("suma", "producto", 5, 6)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemRp{(\lambda+\varphi)\Vect{a}}{i}"),
                                linea(r"=(\lambda+\varphi)\eleVRpE{a}{i}"),
                                linea(r"=\eleVRpE{a}{i}(\lambda+\varphi)", de_reales=True),
                                linea(r"=\eleVRpE{a}{i}\lambda+\eleVRpE{a}{i}\varphi", de_reales=True),
                                linea(r"=\lambda\eleVRpE{a}{i}+\varphi\eleVRpE{a}{i}", de_reales=True),
                                linea(r"=\elemRp{\lambda\Vect{a}}{i}+\elemRp{\varphi\Vect{a}}{i}"),
                                linea(r"=\elemRp{\lambda\Vect{a}+\varphi\Vect{a}}{i}")],
                               salto=0.6)
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis. <bookmark mark='l1'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "producto")
        
        with self.voiceover(text=tr("""La distributiva que tenemos lleva el factor común a la izquierda. Así que primero, por la conmutativa, podemos cambiar el orden de los factores. <bookmark mark='l2'/>""",
                                    """The distributive property we have puts the common factor on the left. So first, by the commutative property, we can change the order of the factors. <bookmark mark='l2'/>""")) as tracker:
            panel.senala(6)   # "la distributiva que tenemos": la del panel
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, 5)
        
        with self.voiceover(text=tr("""Ahora sí podemos aplicar la distributiva. <bookmark mark='l3'/>""",
                                    """Now we can apply the distributive property. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 6)
        
        with self.voiceover(text=tr("""Y por la conmutativa podemos cambiar de nuevo el orden de los factores en los dos sumandos. <bookmark mark='l4'/>""",
                                    """And by the commutative property we can change the order of the factors again in both terms. <bookmark mark='l4'/>""")) as tracker:
            self.wait_until_bookmark("l4")
            paso(self, cadena[4], panel, 5, veces=2)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis en los dos sumandos. <bookmark mark='l5'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses in both terms. <bookmark mark='l5'/>""")) as tracker:
            self.wait_until_bookmark("l5")
            paso(self, cadena[5], panel, "producto", veces=2)
        
        with self.voiceover(text=tr("""Y por la definición de suma podemos sacar el selector como factor común. <bookmark mark='l6'/>""",
                                    """And by the definition of addition we can factor out the selector. <bookmark mark='l6'/>""")) as tracker:
            self.wait_until_bookmark("l6")
            paso(self, cadena[6], panel, "suma")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> los dos vectores son iguales. Esta vez hemos necesitado cuatro veces las propiedades de los reales, porque las reglas son exactamente las que son, y hay que aplicarlas tal como están escritas.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> the two vectors are equal. This time we have needed the properties of the reals four times, because the rules are exactly what they are, and they must be applied just as they are written.""",
                 cadena=cadena)
        
        self.pausa_media()


class L01_V07_E05_Asociativa(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 7: asociativa", "Property 7: associative"), 7)
        panel = Panel(self)
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Séptima propiedad: reescalar dos veces es reescalar por el producto de los escalares.""",
                                    """Seventh property: scaling twice is scaling by the product of the scalars.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Para demostrarla necesitará <bookmark mark='p'/> la definición de producto y la propiedad siete de los reales, la asociativa.""",
                                    """To prove it you will need <bookmark mark='p'/> the definition of scalar multiplication and property seven of the reals, the associative property.""")) as tracker:
            self.wait_until_bookmark("p")
            panel.pista("producto", 7)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemRp{\lambda(\varphi\Vect{a})}{i}"),
                                linea(r"=\lambda\big(\elemRp{\varphi\Vect{a}}{i}\big)"),
                                linea(r"=\lambda\big(\varphi\eleVRpE{a}{i}\big)"),
                                linea(r"=(\lambda\varphi)\eleVRpE{a}{i}", de_reales=True),
                                linea(r"=\elemRp{(\lambda\varphi)\Vect{a}}{i}")])
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis. <bookmark mark='l1'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "producto")
        
        with self.voiceover(text=tr("""Y otra vez, dentro, podemos desplazar el paréntesis. <bookmark mark='l2'/>""",
                                    """And once more, inside, we can shift the parentheses. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, "producto")
        
        with self.voiceover(text=tr("""Ya todo son números reales, así que podemos aplicar la asociativa. <bookmark mark='l3'/>""",
                                    """Now everything is real numbers, so we can apply the associative property. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 7)
        
        with self.voiceover(text=tr("""Y por la definición de producto podemos desplazar de nuevo el paréntesis. <bookmark mark='l4'/>""",
                                    """And by the definition of scalar multiplication we can shift the parentheses again. <bookmark mark='l4'/>""")) as tracker:
            self.wait_until_bookmark("l4")
            paso(self, cadena[4], panel, "producto")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> los dos vectores son iguales. Hemos usado tres veces la definición de producto y una sola vez la asociativa.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> the two vectors are equal. We have used the definition of scalar multiplication three times and the associative property only once.""",
                 cadena=cadena)
        
        self.pausa_media()


class L01_V07_E06_Uno(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 8: el uno es el elemento neutro",
                                                             "Property 8: one is the identity element"), 8)
        panel = Panel(self)
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Octava y última propiedad: reescalar por uno no cambia nada.""",
                                    """Eighth and last property: scaling by one changes nothing.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Para demostrarla bastan <bookmark mark='p'/> la definición de producto y la propiedad ocho de los reales.""",
                                    """To prove it, <bookmark mark='p'/> the definition of scalar multiplication and property eight of the reals are enough.""")) as tracker:
            self.wait_until_bookmark("p")
            panel.pista("producto", 8)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemRp{1\Vect{a}}{i}"),
                                linea(r"=1\eleVRpE{a}{i}"),
                                linea(r"=\eleVRpE{a}{i}", de_reales=True)])
        # la misma línea sin el paréntesis, que sobra (no es un paso de la demostración)
        sin_parentesis = linea(r"=\eleVR{a}{i}", de_reales=True).align_to(cadena[2], LEFT).align_to(cadena[2], DOWN)
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de producto podemos desplazar el paréntesis. <bookmark mark='l1'/>""",
                                    """By the definition of scalar multiplication we can shift the parentheses. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "producto")
        
        with self.voiceover(text=tr("""Y por la propiedad ocho de los reales podemos quitar el uno. <bookmark mark='l2'/>""",
                                    """And property eight of the reals lets us drop the one. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, 8)
        
        with self.voiceover(text=tr("""Los paréntesis indican el orden de las operaciones: primero se hace lo de dentro, y después lo de fuera. Aquí fuera no queda ninguna operación, así que el paréntesis sobra <bookmark mark='q'/> y podemos quitarlo.""",
                                    """Parentheses indicate the order of operations: first what is inside, and then what is outside. Here nothing is left outside, so the parentheses are unnecessary <bookmark mark='q'/> and we can drop them.""")) as tracker:
            self.play(Indicate(cadena[2], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1.5)
            self.wait_until_bookmark("q")
            self.play(TransformMatchingShapes(cadena[2], sin_parentesis), run_time=1)
            cadena[2] = sin_parentesis
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> reescalar por uno deja el vector igual. Es la demostración más corta: solo dos pasos.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> scaling by one leaves the vector unchanged. It is the shortest proof: just two steps.""",
                 cadena=cadena)
        
        self.pausa_media()


class L01_V07_E07_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        para = Tex(tr(r"Para cualesquiera $\Vect{a},\Vect{b},\Vect{c}\in\R[n]$ y escalares $\lambda,\varphi$:",
                      r"For any $\Vect{a},\Vect{b},\Vect{c}\in\R[n]$ and scalars $\lambda,\varphi$:"),
                   tex_template=myTemplate, font_size=36).next_to(cabecera, DOWN, buff=0.4)
        col_suma = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=38)
                            for k, p in enumerate(PROPIEDADES_SUMA)]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        col_prod = VGroup(*[MathTex(f"{k+5}.\\;\\;", p, tex_template=myTemplate, font_size=38)
                            for k, p in enumerate(PROPIEDADES_PRODUCTO)]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        tabla = VGroup(col_suma, col_prod).arrange(RIGHT, buff=1.2, aligned_edge=UP).next_to(para, DOWN, buff=0.5)
        tabla.scale_to_fit_width(min(tabla.width, config.frame_width*0.9)).set_x(0)
        for k in range(4):   # misma rejilla de filas
            col_prod[k].set_y(col_suma[k].get_y())
        espacio = Tex(tr("Estas ocho propiedades definirán el \\emph{espacio vectorial}",
                         "These eight properties will define a \\emph{vector space}"),
                      font_size=36).set_color(COLOR_ESCALAR).next_to(tabla, DOWN, buff=0.6)
        
        with self.voiceover(text=tr("""Resumamos. Con este vídeo y el anterior hemos demostrado las ocho propiedades de las operaciones con vectores: <bookmark mark='s'/> cuatro de la suma <bookmark mark='p'/> y cuatro del producto por un escalar.""",
                                    """Let us sum up. With this video and the previous one we have proved the eight properties of the operations with vectors: <bookmark mark='s'/> four for addition <bookmark mark='p'/> and four for scalar multiplication.""")) as tracker:
            self.play(FadeIn(para), run_time=0.8)
            self.wait_until_bookmark("s")
            self.play(FadeIn(col_suma), run_time=1)
            self.wait_until_bookmark("p")
            self.play(FadeIn(col_prod), run_time=1)
        
        with self.voiceover(text=tr("""Más adelante en el curso, estas ocho propiedades serán las que definan qué es un espacio vectorial.""",
                                    """Later in the course, these eight properties will be the ones that define what a vector space is.""")) as tracker:
            self.play(FadeIn(espacio), run_time=1)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos los vectores como una forma de representar datos.""",
                                    """In the next video we will see vectors as a way of representing data.""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
