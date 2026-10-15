from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Propiedades de la suma de vectores de ", "Properties of vector addition in ") + r"\R[n]"

PROPIEDADES_REALES = [r"a+b=b+a", r"a+(b+c)=(a+b)+c", r"a+0=a", r"a+(-a)=0",
                      r"ab=ba", r"a(b+c)=ab+ac", r"a(bc)=(ab)c", r"1a=a"]

PROPIEDADES_SUMA = [r"\Vect{a}+\Vect{b}=\Vect{b}+\Vect{a}",
                    r"\Vect{a}+(\Vect{b}+\Vect{c})=(\Vect{a}+\Vect{b})+\Vect{c}",
                    r"\Vect{a}+\Vect{0}=\Vect{a}",
                    r"\Vect{a}+(-\Vect{a})=\Vect{0}"]

CAMPANITA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos", "campanita.wav")   # suena al subir un contador

DEFINICIONES = [("suma",     r"\elemRp{\Vect{a}+\Vect{b}}{i}=\eleVR{a}{i}+\eleVR{b}{i}"),
                ("producto", r"\elemRp{\lambda\Vect{a}}{i}=\lambda\eleVRpE{a}{i}"),
                ("nulo",     r"\eleVR{0}{i}=0"),
                ("opuesto",  r"\elemRp{-\Vect{a}}{i}=-\eleVRpE{a}{i}")]


class Panel:
    """Panel fijo de herramientas: definiciones a la izquierda y propiedades de los reales a la
    derecha. Las piezas se identifican por clave ("suma", "producto", "nulo", "opuesto", 1, 2, ...).
    `atenuadas` se muestran en segundo plano hasta que `enciende()` las trae al frente."""
    def __init__(self, escena, reales=range(1, 5), atenuadas=("nulo", "opuesto"), y_sup=2.95, font_size=28):
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
    """Cabecera de la escena (arriba, centrada; lleva el número de la propiedad) y enunciado de la
    propiedad `numero` de la suma, sin numerar, en el hueco entre los dos lados del panel."""
    cabecera = Tex(texto, tex_template=myTemplate, font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
    enunciado = MathTex(PROPIEDADES_SUMA[numero-1], tex_template=myTemplate, font_size=40).set_color(COLOR_RESULTADO)
    # en el hueco: entre los dos lados del panel y a media altura entre la cabecera y la primera línea de la cadena
    enunciado.scale_to_fit_width(min(enunciado.width, 4.6)).move_to([-0.3, 2.2, 0])
    escena.add(cabecera)
    return cabecera, enunciado


def linea(formula, de_reales=False):
    """Una línea de la cadena de igualdades (en teal si el paso es una operación entre números reales)."""
    return MathTex(formula, tex_template=myTemplate, font_size=36).set_color(COLOR_REGLA if de_reales else WHITE)


def coloca_cadena(cadena, y_sup=0.55, salto=0.66, x_izq=-3.3, sangria=0.6):
    """Coloca la cadena bajo el enunciado y entre los dos lados del panel: la primera línea en x_izq y
    las siguientes (que empiezan por '=') alineadas entre sí y desplazadas `sangria` a la derecha."""
    for k, l in enumerate(cadena):
        l.move_to([0, y_sup - k*salto, 0]).align_to([x_izq + (sangria if k else 0), 0, 0], LEFT)
    return cadena


def paso(escena, l, panel, clave, run_time=1):
    """Un paso de la cadena: primero parpadea en el panel la pieza que se va a usar (la voz la
    acaba de nombrar), después se escribe la línea, y por último sube el contador con la campanita."""
    panel.senala(clave)
    escena.play(Write(l), run_time=run_time)
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

class L01_V06_PropiedadesDeLaSumaDeVectores(MiEscenaConVoz):
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
        
        with self.voiceover(text=tr("""En el vídeo anterior vimos las nueve propiedades algebraicas de los números reales. En este demostraremos que la suma de vectores cumple propiedades parecidas a las cuatro primeras.""",
                                    """In the previous video we saw the nine algebraic properties of the real numbers. In this one we will prove that vector addition satisfies properties similar to the first four.""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        # Cuatro ejemplos numéricos en R2 (ilustran, no demuestran): una fila por propiedad
        def v(x, y):
            return r"\begin{pmatrix}" + f"{x}\\\\{y}" + r"\end{pmatrix}"
        A, B, C = v(1, 2), v(2, 1), v(1, 1)
        ejemplos = VGroup(
            MathTex(A, "+", B, "=", v(3, 3), "=", B, "+", A, tex_template=myTemplate, font_size=36),
            MathTex(A, "+", r"\left(", B, "+", C, r"\right)", "=", v(4, 4), "=", r"\left(", A, "+", B, r"\right)", "+", C,
                    tex_template=myTemplate, font_size=36),
            MathTex(A, "+", v(0, 0), "=", A, tex_template=myTemplate, font_size=36),
            MathTex(A, "+", v(-1, -2), "=", v(0, 0), tex_template=myTemplate, font_size=36))
        for ej in ejemplos:   # colores: a azul, b naranja, c verde
            for k, parte in enumerate(ej):
                texto = ej.tex_strings[k]
                if texto == A: parte.set_color(COLOR_A)
                elif texto == B: parte.set_color(COLOR_B)
                elif texto == C: parte.set_color(COLOR_C)
        ejemplos.arrange(DOWN, buff=0.35).next_to(titulo, DOWN, buff=0.5)
        pregunta = Tex(tr("¿Característica de los ejemplos, o propiedades generales?", "Peculiar to the examples, or general properties?"),
                       font_size=40).set_color(COLOR_ESCALAR).next_to(ejemplos, DOWN, buff=0.45)
        
        with self.voiceover(text=tr("""En los siguientes ejemplos vemos que: <bookmark mark='e1'/> da igual en qué orden sumemos dos vectores, <bookmark mark='e2'/> y si son tres, da igual por qué pareja empecemos. <bookmark mark='e3'/> Sumar un vector nulo no cambia nada. <bookmark mark='e4'/> Y sumar un vector y su opuesto da un vector nulo.""",
                                    """In the following examples we see that: <bookmark mark='e1'/> it does not matter in which order we add two vectors, <bookmark mark='e2'/> or which pair we add first if there are three. <bookmark mark='e3'/> Adding a zero vector changes nothing. <bookmark mark='e4'/> And a vector plus its opposite gives a zero vector.""")) as tracker:
            for k, marca in enumerate(["e1", "e2", "e3", "e4"]):
                self.wait_until_bookmark(marca)
                self.play(FadeIn(ejemplos[k]), run_time=0.8)
        
        with self.voiceover(text=tr("""Estos comportamientos podrían ser una característica particular de los ejemplos, o propiedades generales. Hoy vamos a demostrar que son propiedades generales.""",
                                    """Is this behaviour peculiar to the examples? Or are these general properties? Today we are going to prove that they are general properties.""")) as tracker:
            self.play(Write(pregunta), run_time=1.5)
        
        cabecera = Tex(tr("Dos vectores especiales", "Two special vectors"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        
        with self.voiceover(text=tr("""Antes necesitamos dos vectores especiales, que acaban de aparecer.""",
                                    """First we need two special vectors, which have just appeared.""")) as tracker:
            self.play(FadeOut(ejemplos), FadeOut(pregunta), ReplacementTransform(titulo, cabecera), run_time=1)
        
        # Vector nulo
        nulo_txt = Tex(tr(r"Vector nulo $\Vect{0}$ de $\R[n]$: sus $n$ componentes son cero",
                          r"Zero vector $\Vect{0}$ of $\R[n]$: its $n$ components are zero"),
                       tex_template=myTemplate, font_size=40).next_to(cabecera, DOWN, buff=0.5)
        nulo_ej = MathTex(r"\begin{pmatrix}0\\0\end{pmatrix}", r"\qquad", r"\begin{pmatrix}0\\0\\0\end{pmatrix}",
                          tex_template=myTemplate, font_size=40).next_to(nulo_txt, DOWN, buff=0.35)
        nulo_regla = MathTex(r"\eleVR{0}{i}=0", tex_template=myTemplate, font_size=48).set_color(COLOR_RESULTADO)
        nulo_regla.next_to(nulo_ej, RIGHT, buff=1.6)
        VGroup(nulo_ej, nulo_regla).set_x(0)   # cada elemento aparece ya en su posición final
        
        with self.voiceover(text=tr("""El vector nulo es el que tiene todas sus componentes nulas, y lo escribimos con un cero en negrita.""",
                                    """The zero vector is the one whose components are all zero, and we write it as a bold zero.""")) as tracker:
            self.play(FadeIn(nulo_txt), run_time=1)
        
        with self.voiceover(text=tr("""Por ejemplo, el vector nulo de R2 <bookmark mark='r2'/> tiene dos ceros, y el de R3 <bookmark mark='r3'/> tiene tres.""",
                                    """For example, the zero vector of R2 <bookmark mark='r2'/> has two zeros, and that of R3 <bookmark mark='r3'/> has three.""")) as tracker:
            self.wait_until_bookmark("r2")
            self.play(FadeIn(nulo_ej[0]), run_time=0.8)
            self.wait_until_bookmark("r3")
            self.play(FadeIn(nulo_ej[2]), run_time=0.8)
        
        with self.voiceover(text=tr("""En las demostraciones usaremos que toda componente de un vector nulo es cero.""",
                                    """In the proofs we will use that every component of a zero vector is zero.""")) as tracker:
            self.pausa(min(1.2, tracker.duration/3))
            self.play(Write(nulo_regla), run_time=1.2)
        
        # Vector opuesto
        op_txt = Tex(tr(r"Vector opuesto $-\Vect{a}$: sus componentes son las opuestas de las de $\Vect{a}$",
                        r"Opposite vector $-\Vect{a}$: its components are the opposites of those of $\Vect{a}$"),
                     tex_template=myTemplate, font_size=40).next_to(nulo_ej, DOWN, buff=0.7).set_x(0)
        op_ej = MathTex(r"\Vect{a}=\begin{pmatrix}0\\1\\2\end{pmatrix}", r"\qquad", r"-\Vect{a}=\begin{pmatrix}0\\-1\\-2\end{pmatrix}",
                        tex_template=myTemplate, font_size=40).next_to(op_txt, DOWN, buff=0.35)
        op_ej[0].set_color(COLOR_A)
        op_regla = MathTex(r"\elemRp{-\Vect{a}}{i}=-\eleVRpE{a}{i}", tex_template=myTemplate, font_size=48).set_color(COLOR_RESULTADO)
        op_regla.next_to(op_ej, RIGHT, buff=1.2)
        VGroup(op_ej, op_regla).set_x(0)
        
        with self.voiceover(text=tr("""El vector opuesto de a, <bookmark mark='ej'/> que escribimos menos a, es el vector cuyas componentes son las opuestas de las de a.<bookmark mark='v5'/>""",
                                    """The opposite vector of a, <bookmark mark='ej'/> which we write as minus a, is the vector whose components are the opposites of those of a.<bookmark mark='v5'/>""")) as tracker:
            self.play(FadeIn(op_txt), FadeIn(op_ej[0]), run_time=1)   # el ejemplo se ve mientras se define
            self.wait_until_bookmark("ej")
            self.play(FadeIn(op_ej[2]), run_time=0.8)
        
        with self.voiceover(text=tr("""En las demostraciones usaremos que cada componente del opuesto es el opuesto de la componente.""",
                                    """In the proofs we will use that each component of the opposite is the opposite of the component.""")) as tracker:
            self.pausa(min(1.0, tracker.duration/4))
            self.play(Write(op_regla), run_time=1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Cómo demostrar una igualdad entre vectores", "How to prove an equality between vectors"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.play(Write(cabecera))
        
        # (1) Igualdad componente a componente
        criterio = MathTex(r"\Vect{v}=\Vect{w}", r"\quad\Longleftrightarrow\quad",
                           r"\eleVR{v}{i}=\eleVR{w}{i}", tex_template=myTemplate, font_size=52)
        criterio_nota = Tex(tr(r"para toda componente $i$", r"for every component $i$"),
                            tex_template=myTemplate, font_size=36).set_color(GRAY_B)
        VGroup(criterio, criterio_nota).arrange(DOWN, buff=0.4).next_to(cabecera, DOWN, buff=1.0)
        
        with self.voiceover(text=tr("""Dos vectores son iguales cuando coinciden componente a componente. Por tanto basta demostrar que la componente i-ésima es la misma, <bookmark mark='i'/> para cualquier i: así la demostración vale para vectores de cualquier tamaño.<bookmark mark='v4'/>""",
                                    """Two vectors are equal when they coincide component-wise. Therefore it is enough to prove that the i-th component is the same, <bookmark mark='i'/> for any i: that way the proof holds for vectors of any size.""")) as tracker:
            self.play(Write(criterio), run_time=2)
            self.wait_until_bookmark("i")
            self.play(FadeIn(criterio_nota), run_time=0.8)
        
        self.pausa()
        self.play(FadeOut(criterio), FadeOut(criterio_nota), run_time=0.6)
        
        # (2) Las cuatro definiciones
        sub_def = Tex(tr("Definiciones", "Definitions"), font_size=40).set_color(COLOR_RESULTADO).next_to(cabecera, DOWN, buff=0.5)
        definiciones = VGroup(MathTex(r"\elemRp{\Vect{a}+\Vect{b}}{i}=\eleVR{a}{i}+\eleVR{b}{i}", tex_template=myTemplate, font_size=44),
                              MathTex(r"\elemRp{\lambda\Vect{a}}{i}=\lambda\eleVRpE{a}{i}",      tex_template=myTemplate, font_size=44),
                              MathTex(r"\eleVR{0}{i}=0",                                         tex_template=myTemplate, font_size=44),
                              MathTex(r"\elemRp{-\Vect{a}}{i}=-\eleVRpE{a}{i}",                   tex_template=myTemplate, font_size=44))
        definiciones.arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(sub_def, DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""Disponemos de cuatro definiciones, todas componente a componente: <bookmark mark='s'/> la suma, que distribuye el selector, <bookmark mark='p'/> el producto por un escalar, que desplaza el paréntesis, <bookmark mark='n'/> el vector nulo, <bookmark mark='o'/> y el opuesto, que también desplaza el paréntesis.""",
                                    """We have four definitions, all component-wise: <bookmark mark='s'/> addition, which distributes the selector, <bookmark mark='p'/> scalar multiplication, which moves the parentheses, <bookmark mark='n'/> the zero vector, <bookmark mark='o'/> and the opposite, which also moves the parentheses.""")) as tracker:
            self.play(FadeIn(sub_def), run_time=0.8)
            for k, marca in enumerate(["s", "p", "n", "o"]):
                self.wait_until_bookmark(marca)
                self.play(Write(definiciones[k]), run_time=0.8)
        
        self.pausa()
        self.play(FadeOut(sub_def), FadeOut(definiciones), run_time=0.6)
        
        # (3) Las ocho propiedades de los números reales
        sub_reales = Tex(tr("Propiedades de los números reales", "Properties of the real numbers"),
                         font_size=40).set_color(COLOR_REGLA).next_to(cabecera, DOWN, buff=0.5)
        cuadro = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=42)
                          for k, p in enumerate(PROPIEDADES_REALES[:4])]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        cuadro.next_to(sub_reales, DOWN, buff=0.5).set_x(0)
        
        with self.voiceover(text=tr("""De las nueve propiedades algebraicas de los reales, hoy solo necesitamos <bookmark mark='c1'/> las cuatro de la suma.""",
                                    """Of the nine algebraic properties of the reals, today we only need <bookmark mark='c1'/> the four for addition.""")) as tracker:
            self.play(FadeIn(sub_reales), run_time=0.8)
            self.wait_until_bookmark("c1")
            self.play(FadeIn(cuadro), run_time=1)
        
        self.pausa()
        self.play(FadeOut(sub_reales), FadeOut(cuadro), run_time=0.6)
        
        # (4) La disciplina: una cadena de igualdades, una regla por paso
        esquema = MathTex(r"\elemRp{\text{" + tr("lado izquierdo", "left-hand side") + r"}}{i}",
                          r"=\;\cdots\;=", r"\;\cdots\;=",
                          r"\elemRp{\text{" + tr("lado derecho", "right-hand side") + r"}}{i}",
                          tex_template=myTemplate, font_size=44).next_to(cabecera, DOWN, buff=1.0)
        una_regla = Tex(tr("una sola regla en cada paso", "a single rule at each step"),
                        font_size=36).set_color(COLOR_REGLA).next_to(esquema, DOWN, buff=0.5)
        with self.voiceover(text=tr("""La demostración de cada propiedad es una cadena de igualdades, desde <bookmark mark='li'/> la componente i-ésima del lado izquierdo hasta <bookmark mark='ld'/> la del lado derecho, aplicando en cada paso <bookmark mark='r'/> una sola definición o una sola propiedad de los reales.""",
                                    """The proof of each property is a chain of equalities, from <bookmark mark='li'/> the i-th component of the left-hand side to <bookmark mark='ld'/> that of the right-hand side, applying at each step <bookmark mark='r'/> a single definition or a single property of the reals.""")) as tracker:
            self.wait_until_bookmark("li")
            self.play(Write(esquema[0]), run_time=1)
            self.wait_until_bookmark("ld")
            self.play(Write(esquema[1:]), run_time=1.2)
            self.wait_until_bookmark("r")
            self.play(FadeIn(una_regla), run_time=1)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 1: la suma es conmutativa",
                                                             "Property 1: addition is commutative"), 1)
        
        # El panel de herramientas (se presenta aquí, la primera vez)
        panel = Panel(self)
        with self.voiceover(text=tr("""Tenga siempre delante las herramientas: en este vídeo pondremos a la izquierda <bookmark mark='izq'/> las definiciones, y a la derecha <bookmark mark='der'/> las cuatro propiedades de la suma de números reales.""",
                                    """Keep the tools in front of you at all times: in this video we will put on the left <bookmark mark='izq'/> the definitions, and on the right <bookmark mark='der'/> the four properties of the addition of real numbers.""")) as tracker:
            self.wait_until_bookmark("izq")
            self.play(FadeIn(panel.izq), run_time=1)
            self.wait_until_bookmark("der")
            self.play(FadeIn(panel.der), run_time=1)
        
        with self.voiceover(text=tr("""Empecemos por la propiedad conmutativa: el orden de los sumandos no altera la suma.""",
                                    """Let us start with the commutative property: the order of the terms does not change the sum.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        # Ritual: intentarlo, pista (las piezas en amarillo), intentarlo de nuevo
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrar la propiedad conmutativa.",
                                                 "Pause the video and try to prove the commutative property."),
                               pista=tr("Las piezas en amarillo.", "The pieces in yellow."),
                               pista_voz=tr("estas son las piezas que necesita.", "these are the pieces you need."),
                               al_dar_la_pista=lambda: panel.pista("suma", 1))
        
        # La demostración
        cadena = coloca_cadena([linea(r"\elemRp{\Vect{a}+\Vect{b}}{i}"),
                                linea(r"=\eleVR{a}{i}+\eleVR{b}{i}"),
                                linea(r"=\eleVR{b}{i}+\eleVR{a}{i}", de_reales=True),
                                linea(r"=\elemRp{\Vect{b}+\Vect{a}}{i}")])
        
        with self.voiceover(text=tr("""Empezamos con <bookmark mark='l0'/> la componente i-ésima del lado izquierdo.""",
                                    """We start with <bookmark mark='l0'/> the i-th component of the left-hand side.""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l1'/>""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "suma")
        
        with self.voiceover(text=tr("""Los dos sumandos son números reales, así que por la conmutativa podemos intercambiarlos. <bookmark mark='l2'/>""",
                                    """The two terms are real numbers, so by the commutative property we can swap them. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, 1)
        
        with self.voiceover(text=tr("""Y la definición de suma, leída ahora de derecha a izquierda, permite factorizar el selector. <bookmark mark='l3'/>""",
                                    """And the definition of addition, now read from right to left, lets us factor out the selector. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, "suma")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> los dos vectores son iguales. Observe los contadores: hemos usado dos veces la definición de suma y una sola vez la conmutativa.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> the two vectors are equal. Look at the counters: we have used the definition of addition twice and the commutative property only once.""",
                 cadena=cadena)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 2: la suma es asociativa",
                                                             "Property 2: addition is associative"), 2)
        panel = Panel(self)
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Segunda propiedad: la suma de vectores es asociativa. Con tres vectores, da igual por qué pareja empecemos.""",
                                    """Second property: vector addition is associative. With three vectors, it does not matter which pair we add first.""")) as tracker:
            self.play(Write(enunciado), run_time=2)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrar la propiedad asociativa.",
                                                 "Pause the video and try to prove the associative property."),
                               pista=tr("Las piezas en amarillo.", "The pieces in yellow."),
                               pista_voz=tr("estas son las piezas que necesita. La definición de suma se usa varias veces.",
                                            "these are the pieces you need. The definition of addition is used several times."),
                               al_dar_la_pista=lambda: panel.pista("suma", 2))
        
        cadena = coloca_cadena([linea(r"\elemR{\Big(\Vect{a}+\big(\Vect{b}+\Vect{c}\big)\Big)}{i}"),
                                linea(r"=\eleVR{a}{i}+\elemRp{\Vect{b}+\Vect{c}}{i}"),
                                linea(r"=\eleVR{a}{i}+\Big(\eleVR{b}{i}+\eleVR{c}{i}\Big)"),
                                linea(r"=\Big(\eleVR{a}{i}+\eleVR{b}{i}\Big)+\eleVR{c}{i}", de_reales=True),
                                linea(r"=\elemRp{\Vect{a}+\Vect{b}}{i}+\eleVR{c}{i}"),
                                linea(r"=\elemR{\Big(\big(\Vect{a}+\Vect{b}\big)+\Vect{c}\Big)}{i}")])
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l1'/>""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "suma")
        
        with self.voiceover(text=tr("""Y en el segundo sumando podemos distribuirlo otra vez. <bookmark mark='l2'/>""",
                                    """And on the second term we can distribute it again. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, "suma")
        
        with self.voiceover(text=tr("""Ya todo son números reales, así que por la asociativa podemos mover el paréntesis. <bookmark mark='l3'/>""",
                                    """Now everything is real numbers, so by the associative property we can move the parentheses. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 2)
        
        with self.voiceover(text=tr("""Ahora la definición de suma, leída de derecha a izquierda, permite factorizar el selector. <bookmark mark='l4'/>""",
                                    """Now the definition of addition, read from right to left, lets us factor out the selector. <bookmark mark='l4'/>""")) as tracker:
            self.wait_until_bookmark("l4")
            paso(self, cadena[4], panel, "suma")
        
        with self.voiceover(text=tr("""Y una vez más podemos factorizarlo. <bookmark mark='l5'/>""",
                                    """And once more we can factor it out. <bookmark mark='l5'/>""")) as tracker:
            self.wait_until_bookmark("l5")
            paso(self, cadena[5], panel, "suma")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> los dos vectores son iguales. Hemos usado cuatro veces la definición de suma y una sola vez la asociativa.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> the two vectors are equal. We have used the definition of addition four times and the associative property only once.""",
                 cadena=cadena)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 3: el vector nulo es el elemento neutro",
                                                             "Property 3: the zero vector is the identity element"), 3)
        panel = Panel(self)
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Tercera propiedad: el vector nulo es el elemento neutro de la suma. Sumarlo no cambia nada.""",
                                    """Third property: the zero vector is the identity element of addition. Adding it changes nothing.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Aquí entra en juego la definición del vector nulo. <bookmark mark='n'/> Para demostrarla necesitará <bookmark mark='p'/> la definición de suma, la del vector nulo y la propiedad tres de los reales.""",
                                    """Here the definition of the zero vector comes into play. <bookmark mark='n'/> To prove it you will need <bookmark mark='p'/> the definition of addition, that of the zero vector, and property three of the reals.""")) as tracker:
            self.wait_until_bookmark("n")
            panel.enciende("nulo")
            self.wait_until_bookmark("p")
            panel.pista("suma", "nulo", 3)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemRp{\Vect{a}+\Vect{0}}{i}"),
                                linea(r"=\eleVR{a}{i}+\eleVR{0}{i}"),
                                linea(r"=\eleVR{a}{i}+0"),
                                linea(r"=\eleVR{a}{i}", de_reales=True)])
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l1'/>""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "suma")
        
        with self.voiceover(text=tr("""Por la definición de vector nulo, su componente es el número cero. <bookmark mark='l2'/>""",
                                    """By the definition of the zero vector, its component is the number zero. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, "nulo")
        
        with self.voiceover(text=tr("""Y por la propiedad tres de los reales podemos quitar el cero. <bookmark mark='l3'/>""",
                                    """And by property three of the reals we can drop the zero. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 3)
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> 'a' más el vector nulo es a. Hemos usado cada una de las tres piezas una sola vez.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> 'a' plus the zero vector is 'a'. We have used each of the three pieces only once.""",
                 cadena=cadena)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 4: todo vector tiene un opuesto",
                                                             "Property 4: every vector has an opposite"), 4)
        panel = Panel(self, atenuadas=("opuesto",))
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Cuarta propiedad: todo vector tiene un opuesto. Sumados, dan el vector nulo.""",
                                    """Fourth property: every vector has an opposite. Added together, they give the zero vector.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Ahora entra en juego la definición del vector opuesto. <bookmark mark='o'/> Para demostrarla necesitará <bookmark mark='p'/> la definición de suma, la de opuesto, la propiedad cuatro de los reales, y también la definición de vector nulo.""",
                                    """Now the definition of the opposite vector comes into play. <bookmark mark='o'/> To prove it you will need <bookmark mark='p'/> the definition of addition, that of opposite, property four of the reals, and also the definition of the zero vector.""")) as tracker:
            self.wait_until_bookmark("o")
            panel.enciende("opuesto")
            self.wait_until_bookmark("p")
            panel.pista("suma", "opuesto", 4, "nulo")
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemR{\big(\Vect{a}+(-\Vect{a})\big)}{i}"),
                                linea(r"=\eleVR{a}{i}+\elemRp{-\Vect{a}}{i}"),
                                linea(r"=\eleVR{a}{i}+\big(-\eleVRpE{a}{i}\big)"),
                                linea(r"=0", de_reales=True),
                                linea(r"=\eleVR{0}{i}")])
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l1'/>""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "suma")
        
        with self.voiceover(text=tr("""Por la definición de opuesto podemos desplazar el paréntesis. <bookmark mark='l2'/>""",
                                    """By the definition of opposite we can move the parentheses. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, "opuesto")
        
        with self.voiceover(text=tr("""Y por la propiedad cuatro de los reales, un número más su opuesto es cero. <bookmark mark='l3'/>""",
                                    """And by property four of the reals, a number plus its opposite is zero. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 4)
        
        with self.voiceover(text=tr("""Y la definición de vector nulo cierra la cadena: <bookmark mark='l4'/> el cero es la componente i-ésima del vector nulo.<bookmark mark='v2'/>""",
                                    """And the definition of the zero vector closes the chain: <bookmark mark='l4'/> zero is the i-th component of the zero vector.""")) as tracker:
            self.wait_until_bookmark("l4")
            paso(self, cadena[4], panel, "nulo")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Este último paso parece innecesario, pero es el que nos lleva a la componente i-ésima del lado derecho.""",
                                    """This last step may seem unnecessary, but it is the one that takes us to the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> 'a' más su opuesto es el vector nulo. Hemos usado cada una de las cuatro piezas una sola vez.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> 'a' plus its opposite is the zero vector. We have used each of the four pieces only once.<bookmark mark='v3'/>""",
                 cadena=cadena)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        rotulo_reales   = Tex(tr("Números reales", "Real numbers"), font_size=38).set_color(COLOR_REGLA)
        rotulo_vectores = Tex(tr(r"Vectores de $\R[n]$", r"Vectors in $\R[n]$"), tex_template=myTemplate, font_size=38).set_color(COLOR_RESULTADO)
        col_reales   = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=42).set_color(COLOR_REGLA)
                                for k, p in enumerate(PROPIEDADES_REALES[:4])]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        col_vectores = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=42)
                                for k, p in enumerate(PROPIEDADES_SUMA)]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        tabla = VGroup(VGroup(rotulo_reales, col_reales).arrange(DOWN, buff=0.5),
                       VGroup(rotulo_vectores, col_vectores).arrange(DOWN, buff=0.5)).arrange(RIGHT, buff=1.8, aligned_edge=UP)
        tabla.next_to(cabecera, DOWN, buff=0.6).set_x(0)
        for k in range(4):   # misma rejilla de filas
            col_vectores[k].set_y(col_reales[k].get_y())
        
        with self.voiceover(text=tr("""Resumamos. La suma de vectores <bookmark mark='v1'/> es conmutativa, <bookmark mark='v2'/> es asociativa, <bookmark mark='v3'/> el vector nulo es su elemento neutro, <bookmark mark='v4'/> y todo vector tiene un opuesto.""",
                                    """Let us sum up. Vector addition <bookmark mark='v1'/> is commutative, <bookmark mark='v2'/> it is associative, <bookmark mark='v3'/> the zero vector is its identity element, <bookmark mark='v4'/> and every vector has an opposite.""")) as tracker:
            self.play(FadeIn(rotulo_vectores), run_time=0.8)
            for k, marca in enumerate(["v1", "v2", "v3", "v4"]):
                self.wait_until_bookmark(marca)
                self.play(FadeIn(col_vectores[k]), run_time=0.6)
        
        with self.voiceover(text=tr("""Son las mismas cuatro propiedades que cumple la suma de números reales.""",
                                    """They are the same four properties satisfied by the addition of real numbers.""")) as tracker:
            self.play(FadeIn(rotulo_reales), FadeIn(col_reales), run_time=1.2)
        
        with self.voiceover(text=tr("""Se escriben casi igual, pero a la derecha <bookmark mark='bv'/> las letras en negrita son vectores, y a la izquierda <bookmark mark='br'/> son números.""",
                                    """They look almost the same, but on the right <bookmark mark='bv'/> the bold letters are vectors, and on the left <bookmark mark='br'/> they are numbers.""")) as tracker:
            self.wait_until_bookmark("bv")
            self.play(Indicate(col_vectores, color=COLOR_ESCALAR, scale_factor=1.08), run_time=1.2)
            self.wait_until_bookmark("br")
            self.play(Indicate(col_reales, color=COLOR_ESCALAR, scale_factor=1.08), run_time=1.2)
        
        metodo = Tex(tr(r"igualdad componente a componente, definiciones,\\ y una sola propiedad de los reales en cada paso",
                        r"component-wise equality, definitions,\\ and a single property of the reals at each step"),
                     font_size=34).set_color(GRAY_B).next_to(tabla, DOWN, buff=0.7)
        metodo.scale_to_fit_width(min(metodo.width, config.frame_width*0.9))
        
        with self.voiceover(text=tr("""Y las hemos demostrado con un método que vale para vectores de cualquier tamaño: igualdad componente a componente, las definiciones, y una sola propiedad de los reales en cada paso.""",
                                    """And we have proved them with a method that works for vectors of any size: component-wise equality, the definitions, and a single property of the reals at each step.""")) as tracker:
            self.pausa(min(1.5, tracker.duration/3))
            self.play(FadeIn(metodo), run_time=1)
        
        with self.voiceover(text=tr("""En el próximo vídeo haremos lo mismo con el producto por escalares: cuatro propiedades más.""",
                                    """In the next video we will do the same with scalar multiplication: four more properties.""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos_finales()


class L01_V06_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class L01_V06_E01_VectoresEspeciales(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        
        titulo = Title(TITULO, tex_template=myTemplate, font_size=50).set_color(COLOR_TITULO)
        self.play(Write(titulo))
        
        with self.voiceover(text=tr("""En el vídeo anterior vimos las nueve propiedades algebraicas de los números reales. En este demostraremos que la suma de vectores cumple propiedades parecidas a las cuatro primeras.""",
                                    """In the previous video we saw the nine algebraic properties of the real numbers. In this one we will prove that vector addition satisfies properties similar to the first four.""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        # Cuatro ejemplos numéricos en R2 (ilustran, no demuestran): una fila por propiedad
        def v(x, y):
            return r"\begin{pmatrix}" + f"{x}\\\\{y}" + r"\end{pmatrix}"
        A, B, C = v(1, 2), v(2, 1), v(1, 1)
        ejemplos = VGroup(
            MathTex(A, "+", B, "=", v(3, 3), "=", B, "+", A, tex_template=myTemplate, font_size=36),
            MathTex(A, "+", r"\left(", B, "+", C, r"\right)", "=", v(4, 4), "=", r"\left(", A, "+", B, r"\right)", "+", C,
                    tex_template=myTemplate, font_size=36),
            MathTex(A, "+", v(0, 0), "=", A, tex_template=myTemplate, font_size=36),
            MathTex(A, "+", v(-1, -2), "=", v(0, 0), tex_template=myTemplate, font_size=36))
        for ej in ejemplos:   # colores: a azul, b naranja, c verde
            for k, parte in enumerate(ej):
                texto = ej.tex_strings[k]
                if texto == A: parte.set_color(COLOR_A)
                elif texto == B: parte.set_color(COLOR_B)
                elif texto == C: parte.set_color(COLOR_C)
        ejemplos.arrange(DOWN, buff=0.35).next_to(titulo, DOWN, buff=0.5)
        pregunta = Tex(tr("¿Característica de los ejemplos, o propiedades generales?", "Peculiar to the examples, or general properties?"),
                       font_size=40).set_color(COLOR_ESCALAR).next_to(ejemplos, DOWN, buff=0.45)
        
        with self.voiceover(text=tr("""En los siguientes ejemplos vemos que: <bookmark mark='e1'/> da igual en qué orden sumemos dos vectores, <bookmark mark='e2'/> y si son tres, da igual por qué pareja empecemos. <bookmark mark='e3'/> Sumar un vector nulo no cambia nada. <bookmark mark='e4'/> Y sumar un vector y su opuesto da un vector nulo.""",
                                    """In the following examples we see that: <bookmark mark='e1'/> it does not matter in which order we add two vectors, <bookmark mark='e2'/> or which pair we add first if there are three. <bookmark mark='e3'/> Adding a zero vector changes nothing. <bookmark mark='e4'/> And a vector plus its opposite gives a zero vector.""")) as tracker:
            for k, marca in enumerate(["e1", "e2", "e3", "e4"]):
                self.wait_until_bookmark(marca)
                self.play(FadeIn(ejemplos[k]), run_time=0.8)
        
        with self.voiceover(text=tr("""Estos comportamientos podrían ser una característica particular de los ejemplos, o propiedades generales. Hoy vamos a demostrar que son propiedades generales.""",
                                    """Is this behaviour peculiar to the examples? Or are these general properties? Today we are going to prove that they are general properties.""")) as tracker:
            self.play(Write(pregunta), run_time=1.5)
        
        cabecera = Tex(tr("Dos vectores especiales", "Two special vectors"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        
        with self.voiceover(text=tr("""Antes necesitamos dos vectores especiales, que acaban de aparecer.""",
                                    """First we need two special vectors, which have just appeared.""")) as tracker:
            self.play(FadeOut(ejemplos), FadeOut(pregunta), ReplacementTransform(titulo, cabecera), run_time=1)
        
        # Vector nulo
        nulo_txt = Tex(tr(r"Vector nulo $\Vect{0}$ de $\R[n]$: sus $n$ componentes son cero",
                          r"Zero vector $\Vect{0}$ of $\R[n]$: its $n$ components are zero"),
                       tex_template=myTemplate, font_size=40).next_to(cabecera, DOWN, buff=0.5)
        nulo_ej = MathTex(r"\begin{pmatrix}0\\0\end{pmatrix}", r"\qquad", r"\begin{pmatrix}0\\0\\0\end{pmatrix}",
                          tex_template=myTemplate, font_size=40).next_to(nulo_txt, DOWN, buff=0.35)
        nulo_regla = MathTex(r"\eleVR{0}{i}=0", tex_template=myTemplate, font_size=48).set_color(COLOR_RESULTADO)
        nulo_regla.next_to(nulo_ej, RIGHT, buff=1.6)
        VGroup(nulo_ej, nulo_regla).set_x(0)   # cada elemento aparece ya en su posición final
        
        with self.voiceover(text=tr("""El vector nulo es el que tiene todas sus componentes nulas, y lo escribimos con un cero en negrita.""",
                                    """The zero vector is the one whose components are all zero, and we write it as a bold zero.""")) as tracker:
            self.play(FadeIn(nulo_txt), run_time=1)
        
        with self.voiceover(text=tr("""Por ejemplo, el vector nulo de R2 <bookmark mark='r2'/> tiene dos ceros, y el de R3 <bookmark mark='r3'/> tiene tres.""",
                                    """For example, the zero vector of R2 <bookmark mark='r2'/> has two zeros, and that of R3 <bookmark mark='r3'/> has three.""")) as tracker:
            self.wait_until_bookmark("r2")
            self.play(FadeIn(nulo_ej[0]), run_time=0.8)
            self.wait_until_bookmark("r3")
            self.play(FadeIn(nulo_ej[2]), run_time=0.8)
        
        with self.voiceover(text=tr("""En las demostraciones usaremos que toda componente de un vector nulo es cero.""",
                                    """In the proofs we will use that every component of a zero vector is zero.""")) as tracker:
            self.pausa(min(1.2, tracker.duration/3))
            self.play(Write(nulo_regla), run_time=1.2)
        
        # Vector opuesto
        op_txt = Tex(tr(r"Vector opuesto $-\Vect{a}$: sus componentes son las opuestas de las de $\Vect{a}$",
                        r"Opposite vector $-\Vect{a}$: its components are the opposites of those of $\Vect{a}$"),
                     tex_template=myTemplate, font_size=40).next_to(nulo_ej, DOWN, buff=0.7).set_x(0)
        op_ej = MathTex(r"\Vect{a}=\begin{pmatrix}0\\1\\2\end{pmatrix}", r"\qquad", r"-\Vect{a}=\begin{pmatrix}0\\-1\\-2\end{pmatrix}",
                        tex_template=myTemplate, font_size=40).next_to(op_txt, DOWN, buff=0.35)
        op_ej[0].set_color(COLOR_A)
        op_regla = MathTex(r"\elemRp{-\Vect{a}}{i}=-\eleVRpE{a}{i}", tex_template=myTemplate, font_size=48).set_color(COLOR_RESULTADO)
        op_regla.next_to(op_ej, RIGHT, buff=1.2)
        VGroup(op_ej, op_regla).set_x(0)
        
        with self.voiceover(text=tr("""El vector opuesto de a, <bookmark mark='ej'/> que escribimos menos a, es el vector cuyas componentes son las opuestas de las de a.<bookmark mark='v5'/>""",
                                    """The opposite vector of a, <bookmark mark='ej'/> which we write as minus a, is the vector whose components are the opposites of those of a.<bookmark mark='v5'/>""")) as tracker:
            self.play(FadeIn(op_txt), FadeIn(op_ej[0]), run_time=1)   # el ejemplo se ve mientras se define
            self.wait_until_bookmark("ej")
            self.play(FadeIn(op_ej[2]), run_time=0.8)
        
        with self.voiceover(text=tr("""En las demostraciones usaremos que cada componente del opuesto es el opuesto de la componente.""",
                                    """In the proofs we will use that each component of the opposite is the opposite of the component.""")) as tracker:
            self.pausa(min(1.0, tracker.duration/4))
            self.play(Write(op_regla), run_time=1.2)
        
        self.pausa_media()


class L01_V06_E02_Metodo(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Cómo demostrar una igualdad entre vectores", "How to prove an equality between vectors"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.play(Write(cabecera))
        
        # (1) Igualdad componente a componente
        criterio = MathTex(r"\Vect{v}=\Vect{w}", r"\quad\Longleftrightarrow\quad",
                           r"\eleVR{v}{i}=\eleVR{w}{i}", tex_template=myTemplate, font_size=52)
        criterio_nota = Tex(tr(r"para toda componente $i$", r"for every component $i$"),
                            tex_template=myTemplate, font_size=36).set_color(GRAY_B)
        VGroup(criterio, criterio_nota).arrange(DOWN, buff=0.4).next_to(cabecera, DOWN, buff=1.0)
        
        with self.voiceover(text=tr("""Dos vectores son iguales cuando coinciden componente a componente. Por tanto basta demostrar que la componente i-ésima es la misma, <bookmark mark='i'/> para cualquier i: así la demostración vale para vectores de cualquier tamaño.<bookmark mark='v4'/>""",
                                    """Two vectors are equal when they coincide component-wise. Therefore it is enough to prove that the i-th component is the same, <bookmark mark='i'/> for any i: that way the proof holds for vectors of any size.""")) as tracker:
            self.play(Write(criterio), run_time=2)
            self.wait_until_bookmark("i")
            self.play(FadeIn(criterio_nota), run_time=0.8)
        
        self.pausa()
        self.play(FadeOut(criterio), FadeOut(criterio_nota), run_time=0.6)
        
        # (2) Las cuatro definiciones
        sub_def = Tex(tr("Definiciones", "Definitions"), font_size=40).set_color(COLOR_RESULTADO).next_to(cabecera, DOWN, buff=0.5)
        definiciones = VGroup(MathTex(r"\elemRp{\Vect{a}+\Vect{b}}{i}=\eleVR{a}{i}+\eleVR{b}{i}", tex_template=myTemplate, font_size=44),
                              MathTex(r"\elemRp{\lambda\Vect{a}}{i}=\lambda\eleVRpE{a}{i}",      tex_template=myTemplate, font_size=44),
                              MathTex(r"\eleVR{0}{i}=0",                                         tex_template=myTemplate, font_size=44),
                              MathTex(r"\elemRp{-\Vect{a}}{i}=-\eleVRpE{a}{i}",                   tex_template=myTemplate, font_size=44))
        definiciones.arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(sub_def, DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""Disponemos de cuatro definiciones, todas componente a componente: <bookmark mark='s'/> la suma, que distribuye el selector, <bookmark mark='p'/> el producto por un escalar, que desplaza el paréntesis, <bookmark mark='n'/> el vector nulo, <bookmark mark='o'/> y el opuesto, que también desplaza el paréntesis.""",
                                    """We have four definitions, all component-wise: <bookmark mark='s'/> addition, which distributes the selector, <bookmark mark='p'/> scalar multiplication, which moves the parentheses, <bookmark mark='n'/> the zero vector, <bookmark mark='o'/> and the opposite, which also moves the parentheses.""")) as tracker:
            self.play(FadeIn(sub_def), run_time=0.8)
            for k, marca in enumerate(["s", "p", "n", "o"]):
                self.wait_until_bookmark(marca)
                self.play(Write(definiciones[k]), run_time=0.8)
        
        self.pausa()
        self.play(FadeOut(sub_def), FadeOut(definiciones), run_time=0.6)
        
        # (3) Las ocho propiedades de los números reales
        sub_reales = Tex(tr("Propiedades de los números reales", "Properties of the real numbers"),
                         font_size=40).set_color(COLOR_REGLA).next_to(cabecera, DOWN, buff=0.5)
        cuadro = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=42)
                          for k, p in enumerate(PROPIEDADES_REALES[:4])]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        cuadro.next_to(sub_reales, DOWN, buff=0.5).set_x(0)
        
        with self.voiceover(text=tr("""De las nueve propiedades algebraicas de los reales, hoy solo necesitamos <bookmark mark='c1'/> las cuatro de la suma.""",
                                    """Of the nine algebraic properties of the reals, today we only need <bookmark mark='c1'/> the four for addition.""")) as tracker:
            self.play(FadeIn(sub_reales), run_time=0.8)
            self.wait_until_bookmark("c1")
            self.play(FadeIn(cuadro), run_time=1)
        
        self.pausa()
        self.play(FadeOut(sub_reales), FadeOut(cuadro), run_time=0.6)
        
        # (4) La disciplina: una cadena de igualdades, una regla por paso
        esquema = MathTex(r"\elemRp{\text{" + tr("lado izquierdo", "left-hand side") + r"}}{i}",
                          r"=\;\cdots\;=", r"\;\cdots\;=",
                          r"\elemRp{\text{" + tr("lado derecho", "right-hand side") + r"}}{i}",
                          tex_template=myTemplate, font_size=44).next_to(cabecera, DOWN, buff=1.0)
        una_regla = Tex(tr("una sola regla en cada paso", "a single rule at each step"),
                        font_size=36).set_color(COLOR_REGLA).next_to(esquema, DOWN, buff=0.5)
        with self.voiceover(text=tr("""La demostración de cada propiedad es una cadena de igualdades, desde <bookmark mark='li'/> la componente i-ésima del lado izquierdo hasta <bookmark mark='ld'/> la del lado derecho, aplicando en cada paso <bookmark mark='r'/> una sola definición o una sola propiedad de los reales.""",
                                    """The proof of each property is a chain of equalities, from <bookmark mark='li'/> the i-th component of the left-hand side to <bookmark mark='ld'/> that of the right-hand side, applying at each step <bookmark mark='r'/> a single definition or a single property of the reals.""")) as tracker:
            self.wait_until_bookmark("li")
            self.play(Write(esquema[0]), run_time=1)
            self.wait_until_bookmark("ld")
            self.play(Write(esquema[1:]), run_time=1.2)
            self.wait_until_bookmark("r")
            self.play(FadeIn(una_regla), run_time=1)
        
        self.pausa_media()


class L01_V06_E03_Conmutativa(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 1: la suma es conmutativa",
                                                             "Property 1: addition is commutative"), 1)
        
        # El panel de herramientas (se presenta aquí, la primera vez)
        panel = Panel(self)
        with self.voiceover(text=tr("""Tenga siempre delante las herramientas: en este vídeo pondremos a la izquierda <bookmark mark='izq'/> las definiciones, y a la derecha <bookmark mark='der'/> las cuatro propiedades de la suma de números reales.""",
                                    """Keep the tools in front of you at all times: in this video we will put on the left <bookmark mark='izq'/> the definitions, and on the right <bookmark mark='der'/> the four properties of the addition of real numbers.""")) as tracker:
            self.wait_until_bookmark("izq")
            self.play(FadeIn(panel.izq), run_time=1)
            self.wait_until_bookmark("der")
            self.play(FadeIn(panel.der), run_time=1)
        
        with self.voiceover(text=tr("""Empecemos por la propiedad conmutativa: el orden de los sumandos no altera la suma.""",
                                    """Let us start with the commutative property: the order of the terms does not change the sum.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        # Ritual: intentarlo, pista (las piezas en amarillo), intentarlo de nuevo
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrar la propiedad conmutativa.",
                                                 "Pause the video and try to prove the commutative property."),
                               pista=tr("Las piezas en amarillo.", "The pieces in yellow."),
                               pista_voz=tr("estas son las piezas que necesita.", "these are the pieces you need."),
                               al_dar_la_pista=lambda: panel.pista("suma", 1))
        
        # La demostración
        cadena = coloca_cadena([linea(r"\elemRp{\Vect{a}+\Vect{b}}{i}"),
                                linea(r"=\eleVR{a}{i}+\eleVR{b}{i}"),
                                linea(r"=\eleVR{b}{i}+\eleVR{a}{i}", de_reales=True),
                                linea(r"=\elemRp{\Vect{b}+\Vect{a}}{i}")])
        
        with self.voiceover(text=tr("""Empezamos con <bookmark mark='l0'/> la componente i-ésima del lado izquierdo.""",
                                    """We start with <bookmark mark='l0'/> the i-th component of the left-hand side.""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l1'/>""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "suma")
        
        with self.voiceover(text=tr("""Los dos sumandos son números reales, así que por la conmutativa podemos intercambiarlos. <bookmark mark='l2'/>""",
                                    """The two terms are real numbers, so by the commutative property we can swap them. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, 1)
        
        with self.voiceover(text=tr("""Y la definición de suma, leída ahora de derecha a izquierda, permite factorizar el selector. <bookmark mark='l3'/>""",
                                    """And the definition of addition, now read from right to left, lets us factor out the selector. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, "suma")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> los dos vectores son iguales. Observe los contadores: hemos usado dos veces la definición de suma y una sola vez la conmutativa.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> the two vectors are equal. Look at the counters: we have used the definition of addition twice and the commutative property only once.""",
                 cadena=cadena)
        
        self.pausa_media()


class L01_V06_E04_Asociativa(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 2: la suma es asociativa",
                                                             "Property 2: addition is associative"), 2)
        panel = Panel(self)
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Segunda propiedad: la suma de vectores es asociativa. Con tres vectores, da igual por qué pareja empecemos.""",
                                    """Second property: vector addition is associative. With three vectors, it does not matter which pair we add first.""")) as tracker:
            self.play(Write(enunciado), run_time=2)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrar la propiedad asociativa.",
                                                 "Pause the video and try to prove the associative property."),
                               pista=tr("Las piezas en amarillo.", "The pieces in yellow."),
                               pista_voz=tr("estas son las piezas que necesita. La definición de suma se usa varias veces.",
                                            "these are the pieces you need. The definition of addition is used several times."),
                               al_dar_la_pista=lambda: panel.pista("suma", 2))
        
        cadena = coloca_cadena([linea(r"\elemR{\Big(\Vect{a}+\big(\Vect{b}+\Vect{c}\big)\Big)}{i}"),
                                linea(r"=\eleVR{a}{i}+\elemRp{\Vect{b}+\Vect{c}}{i}"),
                                linea(r"=\eleVR{a}{i}+\Big(\eleVR{b}{i}+\eleVR{c}{i}\Big)"),
                                linea(r"=\Big(\eleVR{a}{i}+\eleVR{b}{i}\Big)+\eleVR{c}{i}", de_reales=True),
                                linea(r"=\elemRp{\Vect{a}+\Vect{b}}{i}+\eleVR{c}{i}"),
                                linea(r"=\elemR{\Big(\big(\Vect{a}+\Vect{b}\big)+\Vect{c}\Big)}{i}")])
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l1'/>""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "suma")
        
        with self.voiceover(text=tr("""Y en el segundo sumando podemos distribuirlo otra vez. <bookmark mark='l2'/>""",
                                    """And on the second term we can distribute it again. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, "suma")
        
        with self.voiceover(text=tr("""Ya todo son números reales, así que por la asociativa podemos mover el paréntesis. <bookmark mark='l3'/>""",
                                    """Now everything is real numbers, so by the associative property we can move the parentheses. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 2)
        
        with self.voiceover(text=tr("""Ahora la definición de suma, leída de derecha a izquierda, permite factorizar el selector. <bookmark mark='l4'/>""",
                                    """Now the definition of addition, read from right to left, lets us factor out the selector. <bookmark mark='l4'/>""")) as tracker:
            self.wait_until_bookmark("l4")
            paso(self, cadena[4], panel, "suma")
        
        with self.voiceover(text=tr("""Y una vez más podemos factorizarlo. <bookmark mark='l5'/>""",
                                    """And once more we can factor it out. <bookmark mark='l5'/>""")) as tracker:
            self.wait_until_bookmark("l5")
            paso(self, cadena[5], panel, "suma")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> los dos vectores son iguales. Hemos usado cuatro veces la definición de suma y una sola vez la asociativa.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> the two vectors are equal. We have used the definition of addition four times and the associative property only once.""",
                 cadena=cadena)
        
        self.pausa_media()


class L01_V06_E05_VectorNulo(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 3: el vector nulo es el elemento neutro",
                                                             "Property 3: the zero vector is the identity element"), 3)
        panel = Panel(self)
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Tercera propiedad: el vector nulo es el elemento neutro de la suma. Sumarlo no cambia nada.""",
                                    """Third property: the zero vector is the identity element of addition. Adding it changes nothing.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Aquí entra en juego la definición del vector nulo. <bookmark mark='n'/> Para demostrarla necesitará <bookmark mark='p'/> la definición de suma, la del vector nulo y la propiedad tres de los reales.""",
                                    """Here the definition of the zero vector comes into play. <bookmark mark='n'/> To prove it you will need <bookmark mark='p'/> the definition of addition, that of the zero vector, and property three of the reals.""")) as tracker:
            self.wait_until_bookmark("n")
            panel.enciende("nulo")
            self.wait_until_bookmark("p")
            panel.pista("suma", "nulo", 3)
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemRp{\Vect{a}+\Vect{0}}{i}"),
                                linea(r"=\eleVR{a}{i}+\eleVR{0}{i}"),
                                linea(r"=\eleVR{a}{i}+0"),
                                linea(r"=\eleVR{a}{i}", de_reales=True)])
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l1'/>""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "suma")
        
        with self.voiceover(text=tr("""Por la definición de vector nulo, su componente es el número cero. <bookmark mark='l2'/>""",
                                    """By the definition of the zero vector, its component is the number zero. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, "nulo")
        
        with self.voiceover(text=tr("""Y por la propiedad tres de los reales podemos quitar el cero. <bookmark mark='l3'/>""",
                                    """And by property three of the reals we can drop the zero. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 3)
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Hemos llegado a la componente i-ésima del lado derecho.""",
                                    """We have reached the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> 'a' más el vector nulo es a. Hemos usado cada una de las tres piezas una sola vez.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> 'a' plus the zero vector is 'a'. We have used each of the three pieces only once.""",
                 cadena=cadena)
        
        self.pausa_media()


class L01_V06_E06_Opuesto(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera, enunciado = cabecera_y_enunciado(self, tr("Propiedad 4: todo vector tiene un opuesto",
                                                             "Property 4: every vector has an opposite"), 4)
        panel = Panel(self, atenuadas=("opuesto",))
        self.add(panel.todo)
        
        with self.voiceover(text=tr("""Cuarta propiedad: todo vector tiene un opuesto. Sumados, dan el vector nulo.""",
                                    """Fourth property: every vector has an opposite. Added together, they give the zero vector.""")) as tracker:
            self.play(Write(enunciado), run_time=1.5)
        
        with self.voiceover(text=tr("""Ahora entra en juego la definición del vector opuesto. <bookmark mark='o'/> Para demostrarla necesitará <bookmark mark='p'/> la definición de suma, la de opuesto, la propiedad cuatro de los reales, y también la definición de vector nulo.""",
                                    """Now the definition of the opposite vector comes into play. <bookmark mark='o'/> To prove it you will need <bookmark mark='p'/> the definition of addition, that of opposite, property four of the reals, and also the definition of the zero vector.""")) as tracker:
            self.wait_until_bookmark("o")
            panel.enciende("opuesto")
            self.wait_until_bookmark("p")
            panel.pista("suma", "opuesto", 4, "nulo")
        
        self.pausa_para_pensar(invitacion_voz=tr("Pause el vídeo e intente demostrarlo.", "Pause the video and try to prove it."))
        
        cadena = coloca_cadena([linea(r"\elemR{\big(\Vect{a}+(-\Vect{a})\big)}{i}"),
                                linea(r"=\eleVR{a}{i}+\elemRp{-\Vect{a}}{i}"),
                                linea(r"=\eleVR{a}{i}+\big(-\eleVRpE{a}{i}\big)"),
                                linea(r"=0", de_reales=True),
                                linea(r"=\eleVR{0}{i}")])
        
        with self.voiceover(text=tr("""Empezamos por la componente i-ésima del lado izquierdo. <bookmark mark='l0'/>""",
                                    """We start with the i-th component of the left-hand side. <bookmark mark='l0'/>""")) as tracker:
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l1'/>""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l1'/>""")) as tracker:
            self.wait_until_bookmark("l1")
            paso(self, cadena[1], panel, "suma")
        
        with self.voiceover(text=tr("""Por la definición de opuesto podemos desplazar el paréntesis. <bookmark mark='l2'/>""",
                                    """By the definition of opposite we can move the parentheses. <bookmark mark='l2'/>""")) as tracker:
            self.wait_until_bookmark("l2")
            paso(self, cadena[2], panel, "opuesto")
        
        with self.voiceover(text=tr("""Y por la propiedad cuatro de los reales, un número más su opuesto es cero. <bookmark mark='l3'/>""",
                                    """And by property four of the reals, a number plus its opposite is zero. <bookmark mark='l3'/>""")) as tracker:
            self.wait_until_bookmark("l3")
            paso(self, cadena[3], panel, 4)
        
        with self.voiceover(text=tr("""Y la definición de vector nulo cierra la cadena: <bookmark mark='l4'/> el cero es la componente i-ésima del vector nulo.<bookmark mark='v2'/>""",
                                    """And the definition of the zero vector closes the chain: <bookmark mark='l4'/> zero is the i-th component of the zero vector.""")) as tracker:
            self.wait_until_bookmark("l4")
            paso(self, cadena[4], panel, "nulo")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Este último paso parece innecesario, pero es el que nos lleva a la componente i-ésima del lado derecho.""",
                                    """This last step may seem unnecessary, but it is the one that takes us to the i-th component of the right-hand side.""")) as tracker:
            pass
        
        concluye(self, enunciado,
                 """<bookmark mark='cc'/> Como esto es cierto para cualquier componente del vector, <bookmark mark='ok'/> 'a' más su opuesto es el vector nulo. Hemos usado cada una de las cuatro piezas una sola vez.""",
                 """<bookmark mark='cc'/> Since this holds for any component of the vector, <bookmark mark='ok'/> 'a' plus its opposite is the zero vector. We have used each of the four pieces only once.<bookmark mark='v3'/>""",
                 cadena=cadena)
        
        self.pausa_media()


class L01_V06_E07_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        rotulo_reales   = Tex(tr("Números reales", "Real numbers"), font_size=38).set_color(COLOR_REGLA)
        rotulo_vectores = Tex(tr(r"Vectores de $\R[n]$", r"Vectors in $\R[n]$"), tex_template=myTemplate, font_size=38).set_color(COLOR_RESULTADO)
        col_reales   = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=42).set_color(COLOR_REGLA)
                                for k, p in enumerate(PROPIEDADES_REALES[:4])]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        col_vectores = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=42)
                                for k, p in enumerate(PROPIEDADES_SUMA)]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        tabla = VGroup(VGroup(rotulo_reales, col_reales).arrange(DOWN, buff=0.5),
                       VGroup(rotulo_vectores, col_vectores).arrange(DOWN, buff=0.5)).arrange(RIGHT, buff=1.8, aligned_edge=UP)
        tabla.next_to(cabecera, DOWN, buff=0.6).set_x(0)
        for k in range(4):   # misma rejilla de filas
            col_vectores[k].set_y(col_reales[k].get_y())
        
        with self.voiceover(text=tr("""Resumamos. La suma de vectores <bookmark mark='v1'/> es conmutativa, <bookmark mark='v2'/> es asociativa, <bookmark mark='v3'/> el vector nulo es su elemento neutro, <bookmark mark='v4'/> y todo vector tiene un opuesto.""",
                                    """Let us sum up. Vector addition <bookmark mark='v1'/> is commutative, <bookmark mark='v2'/> it is associative, <bookmark mark='v3'/> the zero vector is its identity element, <bookmark mark='v4'/> and every vector has an opposite.""")) as tracker:
            self.play(FadeIn(rotulo_vectores), run_time=0.8)
            for k, marca in enumerate(["v1", "v2", "v3", "v4"]):
                self.wait_until_bookmark(marca)
                self.play(FadeIn(col_vectores[k]), run_time=0.6)
        
        with self.voiceover(text=tr("""Son las mismas cuatro propiedades que cumple la suma de números reales.""",
                                    """They are the same four properties satisfied by the addition of real numbers.""")) as tracker:
            self.play(FadeIn(rotulo_reales), FadeIn(col_reales), run_time=1.2)
        
        with self.voiceover(text=tr("""Se escriben casi igual, pero a la derecha <bookmark mark='bv'/> las letras en negrita son vectores, y a la izquierda <bookmark mark='br'/> son números.""",
                                    """They look almost the same, but on the right <bookmark mark='bv'/> the bold letters are vectors, and on the left <bookmark mark='br'/> they are numbers.""")) as tracker:
            self.wait_until_bookmark("bv")
            self.play(Indicate(col_vectores, color=COLOR_ESCALAR, scale_factor=1.08), run_time=1.2)
            self.wait_until_bookmark("br")
            self.play(Indicate(col_reales, color=COLOR_ESCALAR, scale_factor=1.08), run_time=1.2)
        
        metodo = Tex(tr(r"igualdad componente a componente, definiciones,\\ y una sola propiedad de los reales en cada paso",
                        r"component-wise equality, definitions,\\ and a single property of the reals at each step"),
                     font_size=34).set_color(GRAY_B).next_to(tabla, DOWN, buff=0.7)
        metodo.scale_to_fit_width(min(metodo.width, config.frame_width*0.9))
        
        with self.voiceover(text=tr("""Y las hemos demostrado con un método que vale para vectores de cualquier tamaño: igualdad componente a componente, las definiciones, y una sola propiedad de los reales en cada paso.""",
                                    """And we have proved them with a method that works for vectors of any size: component-wise equality, the definitions, and a single property of the reals at each step.""")) as tracker:
            self.pausa(min(1.5, tracker.duration/3))
            self.play(FadeIn(metodo), run_time=1)
        
        with self.voiceover(text=tr("""En el próximo vídeo haremos lo mismo con el producto por escalares: cuatro propiedades más.""",
                                    """In the next video we will do the same with scalar multiplication: four more properties.""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
