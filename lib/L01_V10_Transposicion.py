from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("La transposición", "Transposition")

A_EJ = [[4, -1, 0], [2, 2, 7]]      # la matriz A de V09 (transparencia "Matrices")
A_SEL = [[1, 2, 1], [7, 0, 3]]      # la matriz de los selectores de V09 (transparencia "Más notación")


def vector(valores, color=WHITE, decimales=0, escala=0.8):
    v = IntegerMatrix([[x] for x in valores], left_bracket="(", right_bracket=")", v_buff=0.62)
    v.get_entries().set_color(color)
    return v.scale(escala)


def matriz(filas, color=WHITE, escala=0.8, h_buff=1.0):
    m = IntegerMatrix(filas, v_buff=0.62, h_buff=h_buff)
    m.get_entries().set_color(color)
    return m.scale(escala)


def con_nombre(tex, mob, font_size=48):
    return VGroup(MathTex(tex, tex_template=myTemplate, font_size=font_size), mob).arrange(RIGHT, buff=0.2)


def franja_fila(m, i, color=COLOR_ESCALAR):
    """Franja sobre la fila i (desde 0) de la matriz m."""
    return Rectangle(width=m.width, height=0.45, stroke_width=0, fill_color=color,
                     fill_opacity=0.22).move_to([m.get_x(), m.get_rows()[i].get_y(), 0])


def franja_columna(m, j, color=COLOR_ESCALAR):
    """Franja sobre la columna j (desde 0) de la matriz m."""
    col = m.get_columns()[j]
    return Rectangle(width=col.width + 0.35, height=m.get_brackets()[0].height, stroke_width=0, fill_color=color,
                     fill_opacity=0.22).move_to([col.get_x(), m.get_y(), 0])


def columna_de_lineas(lineas, x0, y0, dy):
    """Fórmulas de varias partes una debajo de otra, con la parte 1 (el "=") alineada en x0."""
    for k, l in enumerate(lineas):
        l.shift([x0 - l[1].get_left()[0], y0 - k*dy - l.get_y(), 0])
    return VGroup(*lineas)


def copia_literal(escena, origen, destino, igual, run_time=1.2):
    """Copia la expresión origen tal cual, alineada a la izquierda donde irá destino, y escribe el igual."""
    copia = origen.copy()
    copia.shift((destino.get_left()[0] - copia.get_left()[0])*RIGHT)
    escena.play(FadeIn(igual), TransformFromCopy(origen, copia), run_time=run_time)
    return copia


def transforma_copia(escena, copia, destino, parejas, se_van=(), aparecen=(), run_time=1.5):
    """Sobre la copia: los glifos de se_van desaparecen, los de parejas (glifo de la copia, glifo de
    destino) van a su sitio, y los de aparecen (índices de destino) surgen donde van."""
    escena.play(*[FadeOut(copia[i]) for i in se_van],
                *[ReplacementTransform(copia[i], destino[j]) for i, j in parejas],
                *[FadeIn(destino[j]) for j in aparecen], run_time=run_time)


def rotulo(texto, junto_a, x=None, font_size=28):
    """Rótulo gris pequeño a la derecha de una línea (la regla que justifica el paso)."""
    r = Tex(texto, tex_template=myTemplate, font_size=font_size, color=GRAY_B)
    r.next_to(junto_a, RIGHT, buff=0.6)
    if x is not None:
        r.shift((x - r.get_left()[0])*RIGHT)
    return r


CAMPANITA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos", "campanita.wav")   # suena al subir un contador


class PanelV10:
    """Panel de herramientas como el de V06-V07, con una pieza a cada lado: [(cabecera, clave, fórmula), ...]
    (la primera a la izquierda, la segunda a la derecha). Pista (amarillo y recuadro), parpadeo antes de
    cada paso y contador de usos con campanita."""
    def __init__(self, escena, piezas, y_sup=2.95, font_size=36):
        self.escena, self.piezas, self.usos, self.contadores = escena, {}, {}, {}
        self.marcos = VGroup()
        lados = []
        for cab, clave, formula in piezas:
            m = MathTex(formula, tex_template=myTemplate, font_size=font_size)
            self.piezas[clave] = m
            lados.append(VGroup(Tex(cab, font_size=24).set_color(GRAY_B), m).arrange(DOWN, aligned_edge=LEFT, buff=0.2))
        lados[0].to_edge(LEFT, buff=0.5)
        lados[1].to_edge(RIGHT, buff=1.6)   # deja sitio al contador sin tocar la firma del margen
        for g in lados:
            g.align_to([0, y_sup, 0], UP)
        self.todo = VGroup(*lados)

    def pista(self, *claves, run_time=1):
        marcos = VGroup(*[SurroundingRectangle(self.piezas[c], color=COLOR_ESCALAR, buff=0.1,
                                               corner_radius=0.1, stroke_width=2) for c in claves])
        self.marcos.add(*marcos)
        self.escena.play(*[self.piezas[c].animate.set_color(COLOR_ESCALAR) for c in claves],
                         Create(marcos), run_time=run_time)

    def senala(self, clave, run_time=0.8):
        self.escena.play(Indicate(self.piezas[clave], color=COLOR_RESULTADO, scale_factor=1.12), run_time=run_time)

    def cuenta(self, clave, run_time=0.5):
        self.usos[clave] = self.usos.get(clave, 0) + 1
        disco = Circle(radius=0.17, fill_color=COLOR_TITULO, fill_opacity=1, stroke_width=0)
        numero = Tex(f"\\textbf{{{self.usos[clave]}}}", font_size=24).set_color(WHITE).move_to(disco)
        nuevo = VGroup(disco, numero).next_to(self.piezas[clave], RIGHT, buff=0.3).shift(0.1*UP)
        self.escena.add_sound(CAMPANITA)
        if clave in self.contadores:
            self.escena.play(ReplacementTransform(self.contadores[clave], nuevo), run_time=run_time)
        else:
            self.escena.play(FadeIn(nuevo, scale=0.5), run_time=run_time)
        self.contadores[clave] = nuevo

class L01_V10_Transposicion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        # Aᵀ a la izquierda y A a la derecha, como los lados de la definición (Aᵀ)|i = i|A que va debajo (Marcos, 2026-11-03)
        A = matriz(A_EJ)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([3.0, 1.2, 0])
        T = matriz([list(f) for f in zip(*A_EJ)])
        f_T = con_nombre(r"\Mat{B}=", T).move_to([-3.3, 1.2, 0])
        nombre_T = MathTex(r"\MatT{A}=", tex_template=myTemplate, font_size=48).move_to(f_T[0], aligned_edge=RIGHT)
        defin = MathTex(r"\VectTC{A}{i}", r"=", r"\VectF{A}{i}", tex_template=myTemplate, font_size=52).move_to([0, -1.5, 0])
        r_col = Tex(tr(r"columna $i$ de $\MatT{A}$", r"column $i$ of $\MatT{A}$"), tex_template=myTemplate, font_size=28, color=GRAY_B).next_to(defin[0], DOWN, buff=0.3)
        r_fil = Tex(tr(r"fila $i$ de $\Mat{A}$", r"row $i$ of $\Mat{A}$"), tex_template=myTemplate, font_size=28, color=GRAY_B).next_to(defin[2], DOWN, buff=0.3)
        orden = MathTex(r"\Mat{A}\in\R[m\times n]", r"\quad\Rightarrow\quad", r"\MatT{A}\in\R[n\times m]", tex_template=myTemplate, font_size=48).move_to([0, -3.0, 0])
        
        # arranque: qué se va a ver en este vídeo (el resto de la escena recuerda V09 solo donde lo usa)
        with self.voiceover(text=tr("""En este vídeo veremos una operación con matrices: la transposición.""",
                                    """In this video we will see an operation on matrices: transposition.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        with self.voiceover(text=tr("""En el vídeo anterior formamos la matriz B con dos vectores: <bookmark mark='x'/> el primero llevaba los números de la primera fila de A, <bookmark mark='y'/> y el segundo, los de la segunda.""",
                                    """In the previous video we built the matrix B with two vectors: <bookmark mark='x'/> the first one carried the numbers of the first row of A, <bookmark mark='y'/> and the second one, those of the second row.""")) as tracker:
            self.play(FadeIn(f_A), FadeIn(f_T[0]), FadeIn(T.get_brackets()), run_time=1)
            for i, marca in enumerate(["x", "y"]):
                self.wait_until_bookmark(marca)
                fr = franja_fila(A, i)
                self.play(FadeIn(fr), run_time=0.4)
                self.play(TransformFromCopy(A.get_rows()[i], T.get_columns()[i]), run_time=1.2)
                self.play(FadeOut(fr), run_time=0.3)
        
        with self.voiceover(text=tr("""Convertir las filas de una matriz en las columnas de otra se llama transposición. <bookmark mark='t'/> La matriz B es la transpuesta de A, que se escribe con una T en el superíndice.""",
                                    """Turning the rows of a matrix into the columns of another is called transposition. <bookmark mark='t'/> The matrix B is the transpose of A, which is written with a T as a superscript.""")) as tracker:
            self.wait_until_bookmark("t")
            self.play(FadeTransform(f_T[0], nombre_T), run_time=1.2)
        
        # la correspondencia se contaba tres veces; queda la regla general (Marcos, 2026-10-31)
        with self.voiceover(text=tr("""Cada columna de la transpuesta es la fila de A <bookmark mark='m'/> con el mismo índice.""",
                                    """Each column of the transpose is the row of A <bookmark mark='m'/> with the same index.""")) as tracker:
            self.play(Write(defin), FadeIn(r_col), FadeIn(r_fil), run_time=1.2)
            self.wait_until_bookmark("m")
            franjas = None
            for i in range(2):   # el mismo índice, ilustrado con las dos columnas
                nuevas = VGroup(franja_columna(T, i), franja_fila(A, i))
                self.play(FadeIn(nuevas) if franjas is None else ReplacementTransform(franjas, nuevas), run_time=0.6)
                self.wait(0.4)
                franjas = nuevas
        
        with self.voiceover(text=tr("""Si A tiene m filas de n componentes, su transpuesta tiene m columnas de n componentes: es de orden 'n' por 'm'.<bookmark mark='v2'/>""",  # comillas y tirada 2: sin ellas sonaba «m por m» (Marcos)
                                    """If A has m rows of n components, its transpose has m columns of n components: it is of order n by m.""")) as tracker:
            self.play(FadeOut(franjas), FadeIn(orden), run_time=1)
        
        # Antes era la escena 4, de una sola frase con su cabecera; ahora ocupa el sitio de la definición
        # (Marcos, 2026-11-01). Con «Por ejemplo» ilustra la regla del orden que se acaba de decir.
        colm = MathTex(r"\begin{bmatrix}9\\ 2\end{bmatrix}", tex_template=myTemplate, font_size=52)
        film = MathTex(r"{\begin{bmatrix}9\\ 2\end{bmatrix}}^{\T}", r"=", r"\begin{bmatrix}9 & 2\end{bmatrix}", tex_template=myTemplate, font_size=52)
        r_c = Tex(tr(r"matriz columna, $2\times 1$", r"column matrix, $2\times 1$"), font_size=32, color=GRAY_B)
        r_f = Tex(tr(r"matriz fila, $1\times 2$", r"row matrix, $1\times 2$"), font_size=32, color=GRAY_B)
        grupos = VGroup(*[VGroup(f, r).arrange(DOWN, buff=0.4) for f, r in [(colm, r_c), (film, r_f)]])
        grupos.arrange(RIGHT, buff=1.6, aligned_edge=DOWN).move_to([0, -1.25, 0])
        
        with self.voiceover(text=tr("""Por ejemplo, <bookmark mark='c'/> la transpuesta de una matriz columna <bookmark mark='f'/> es una matriz fila.""",
                                    """For example, <bookmark mark='c'/> the transpose of a column matrix <bookmark mark='f'/> is a row matrix.""")) as tracker:
            self.play(FadeOut(VGroup(defin, r_col, r_fil)), run_time=0.6)
            self.wait_until_bookmark("c")
            self.play(FadeIn(colm), FadeIn(r_c), run_time=0.8)
            self.wait_until_bookmark("f")
            self.play(FadeIn(film), FadeIn(r_f), run_time=1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Transponer es cambiar de lado los índices", "Transposing swaps the sides of the indices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        orden_sel = tr("da igual el orden de selección", "the order of selection does not matter")
        x_rot = 1.6
        # Ida. Glifos:
        #   ida[0]: ( A T ) | j        =  j | A
        #   ida[1]: i | ( ( A T ) | j )  =  ( j | A ) | i
        #   ida[2]: i | ( A T ) | j      =  j | A | i
        ida = [MathTex(r"\VectTC{A}{j}", r"=", r"\VectF{A}{j}", tex_template=myTemplate, font_size=48),
               MathTex(r"\elemLp{\VectTC{A}{j}}{i}", r"=", r"\elemRp{\VectF{A}{j}}{i}", tex_template=myTemplate, font_size=48),
               MathTex(r"\eleMT{A}{i}{j}", r"=", r"\eleM{A}{j}{i}", tex_template=myTemplate, font_size=48)]
        columna_de_lineas(ida, x0=-1.0, y0=1.6, dy=1.2)
        rot_ida = [rotulo(tr("definición de transpuesta", "definition of the transpose"), ida[0], x=x_rot),
                   rotulo(tr("vectores iguales: mismas componentes", "equal vectors: same components"), ida[1], x=x_rot),
                   rotulo(orden_sel, ida[2], x=x_rot)]
        regla = MathTex(r"\eleMT{A}{i}{j}", r"=", r"\eleM{A}{j}{i}", tex_template=myTemplate, font_size=56).move_to([1.2, 1.6, 0])
        idea = aviso("idea").next_to(regla, LEFT, buff=0.8)
        # Vuelta. Glifos:
        #   vuelta[0]: ( i | ( A T ) ) | j  =  j | ( A | i )
        #   vuelta[1]: i | ( A T )          =  A | i
        vuelta = [MathTex(r"\elemRp{\VectTF{A}{i}}{j}", r"=", r"\elemLp{\VectC{A}{i}}{j}", tex_template=myTemplate, font_size=48),
                  MathTex(r"\elemLp{\MatT{A}}{i}", r"=", r"\VectC{A}{i}", tex_template=myTemplate, font_size=48)]
        columna_de_lineas(vuelta, x0=-1.0, y0=0.1, dy=1.3)
        rot_vuelta = [rotulo(orden_sel, vuelta[0], x=x_rot),
                      rotulo(tr("vale para cualquier componente", "holds for any component"), vuelta[1], x=x_rot)]
        
        
        def copia(origen, destino, parejas):
            return [TransformFromCopy(origen[i], destino[j]) for i, j in parejas]
        
        
        with self.voiceover(text=tr("""Partimos de la definición de transpuesta: <bookmark mark='d'/> cada columna de la transpuesta es la fila de A con el mismo índice.""",
                                    """We start from the definition of the transpose: <bookmark mark='d'/> each column of the transpose is the row of A with the same index.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("d")
            self.play(FadeIn(ida[0]), FadeIn(rot_ida[0]), run_time=1)
        
        with self.voiceover(text=tr("""Son dos vectores iguales, así que tienen las mismas componentes. <bookmark mark='y'/> Seleccionamos la componente i-ésima de los dos: <bookmark mark='x1'/> en la columna, por la izquierda, <bookmark mark='x2'/> y en la fila, por la derecha.""",
                                    """They are two equal vectors, so they have the same components. <bookmark mark='y'/> We select the i-th component of both: <bookmark mark='x1'/> in the column, from the left, <bookmark mark='x2'/> and in the row, from the right.""")) as tracker:
            self.play(FadeIn(rot_ida[1]), run_time=0.6)
            self.wait_until_bookmark("y")
            self.play(FadeIn(ida[1][1]), *copia(ida[0][0], ida[1][0], [(0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8)]),
                      *copia(ida[0][2], ida[1][2], [(0, 1), (1, 2), (2, 3)]), run_time=1.2)
            self.wait_until_bookmark("x1")
            self.play(FadeIn(ida[1][0][0:3]), FadeIn(ida[1][0][9]), run_time=0.8)   # i|( ... )
            self.wait_until_bookmark("x2")
            self.play(FadeIn(ida[1][2][0]), FadeIn(ida[1][2][4:]), run_time=0.8)    # ( ... )|i
        
        # «da igual el orden de selección» se demostró en V09 (escena 7): se recuerda la primera vez que se usa
        # la línea nueva nace cuando la voz dice «podemos quitar los paréntesis», no antes (Marcos, 2026-11-02)
        # recordatorio del motivo (Marcos, 2026-11-03), como en V09: los paréntesis exteriores de los dos lados se ponen en
        # amarillo y viajan a la otra colocación y vuelven mientras la voz dice «da igual el orden...».
        # glifos: ida[1][0] = i | ( ( A T ) | j )  ->  ( i | ( A T ) ) | j ;  ida[1][2] = ( j | A ) | i  ->  j | ( A | i )
        otra_izq = MathTex(r"\elemRp{\VectTF{A}{i}}{j}", tex_template=myTemplate, font_size=48).move_to(ida[1][0])
        otra_der = MathTex(r"\elemLp{\VectC{A}{i}}{j}", tex_template=myTemplate, font_size=48).move_to(ida[1][2])
        parentesis = [ida[1][0][2], ida[1][0][9], ida[1][2][0], ida[1][2][4]]
        with self.voiceover(text=tr("""En el vídeo anterior vimos que <bookmark mark='o'/> da igual el orden en que se aplican los selectores, así que <bookmark mark='x'/> podemos quitar los paréntesis.""",
                                    """In the previous video we saw that <bookmark mark='o'/> the order in which the selectors are applied does not matter, so <bookmark mark='x'/> we can drop the parentheses.""")) as tracker:
            self.play(FadeIn(rot_ida[2]), run_time=0.6)
            self.wait_until_bookmark("o")
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.3) for x in parentesis], run_time=0.3)
            self.play(*[Transform(ida[1][0][i], otra_izq[0][j], rate_func=rate_functions.there_and_back_with_pause)
                        for i, j in zip(range(10), [1, 2, 0, 3, 4, 5, 6, 8, 9, 7])],
                      *[Transform(ida[1][2][i], otra_der[0][j], rate_func=rate_functions.there_and_back_with_pause)
                        for i, j in zip(range(7), [2, 0, 1, 3, 6, 4, 5])], run_time=2.0)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.3) for x in parentesis], run_time=0.3)
            self.wait_until_bookmark("x")
            self.play(FadeIn(ida[2][1]), *copia(ida[1][0], ida[2][0], [(0, 0), (1, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7)]),
                      *copia(ida[1][2], ida[2][2], [(1, 0), (2, 1), (3, 2), (5, 3), (6, 4)]), run_time=1.5)   # los paréntesis no aparecen
        
        # «Así que», no «Hemos demostrado»: la cadena constata que la notación funciona como debe, es una regla de
        # lectura de la notación, no un resultado sobre matrices (Marcos, 2026-11-02)
        # «Por tanto», no «Así que»: la frase anterior ya acaba en «así que podemos quitar los paréntesis» (Marcos, 2026-11-02)
        with self.voiceover(text=tr("""Por tanto, transponer intercambia los índices <bookmark mark='f'/> de la fila <bookmark mark='c'/> y de la columna.""",
                                    """Therefore, transposing swaps <bookmark mark='f'/> the row index <bookmark mark='c'/> and the column index.""")) as tracker:
            # resaltados inmediatos y sostenidos (la frase es corta): las dos i al decir «fila», las dos j al decir «columna»
            ies, jotas = [ida[2][0][0], ida[2][2][4]], [ida[2][0][7], ida[2][2][0]]   # glifos: i | ( A T ) | j  y  j | A | i
            self.wait_until_bookmark("f")
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.5) for x in ies], run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in ies], *[x.animate.set_color(COLOR_C).scale(1.5) for x in jotas], run_time=0.25)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in jotas], run_time=0.4)
        
        self.play(FadeOut(VGroup(ida[0], ida[1], *rot_ida)), ReplacementTransform(ida[2], regla), run_time=1.2)   # la última línea es la regla
        with self.voiceover(text=tr("""De aquí sale una regla de reescritura: transponer, o quitar la transposición, intercambia los índices de lado.""",
                                    """This gives us a rewriting rule: transposing, or removing the transposition, swaps the sides of the indices.""")) as tracker:
            self.play(FadeIn(idea), run_time=0.8)
        
        # Vuelta: en la regla se vuelven a poner los paréntesis (fila de la transpuesta y columna de A)
        # al decir «una fila de la transpuesta» se destaca el selector i| sobre Aᵀ (amarillo, color de fila) y al decir
        # «una columna de A», el |i sobre A (verde, color de columna) (Marcos, 2026-11-03)
        sel_fila_T, sel_col_A = vuelta[0][0][1:3], vuelta[0][2][4:6]   # glifos: ( i | ( A T ) ) | j  y  j | ( A | i )
        with self.voiceover(text=tr("""Esta regla también describe las filas de la transpuesta. <bookmark mark='y'/> Como da igual el orden en que se aplican los selectores, <bookmark mark='x'/> podemos seleccionar primero <bookmark mark='f'/> una fila de la transpuesta <bookmark mark='c'/> y una columna de A.""",
                                    """This rule also describes the rows of the transpose. <bookmark mark='y'/> Since the order in which the selectors are applied does not matter, <bookmark mark='x'/> we can select <bookmark mark='f'/> a row of the transpose <bookmark mark='c'/> and a column of A first.""")) as tracker:
            self.wait_until_bookmark("y")
            self.play(FadeIn(rot_vuelta[0]), FadeIn(vuelta[0][1]),
                      *copia(regla[0], vuelta[0][0], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8), (7, 9)]),
                      *copia(regla[2], vuelta[0][2], [(0, 0), (1, 1), (2, 3), (3, 4), (4, 5)]), run_time=1.2)
            self.wait_until_bookmark("x")
            self.play(FadeIn(VGroup(vuelta[0][0][0], vuelta[0][0][7], vuelta[0][2][2], vuelta[0][2][6])), run_time=0.8)   # los paréntesis
            self.wait_until_bookmark("f")
            self.play(sel_fila_T.animate.set_color(COLOR_ESCALAR).scale(1.4), run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(sel_fila_T.animate.set_color(WHITE).scale(1/1.4), sel_col_A.animate.set_color(COLOR_C).scale(1.4), run_time=0.25)
            self.wait(0.8)
            self.play(sel_col_A.animate.set_color(WHITE).scale(1/1.4), run_time=0.4)
        
        # «la fila de la transpuesta» destaca i| sobre Aᵀ y «la columna de A» el |i sobre A, en la línea nueva (Marcos, 2026-11-03)
        sel_fila_T2, sel_col_A2 = vuelta[1][0][0:2], vuelta[1][2][1:3]   # glifos: i | ( A T )  y  A | i
        with self.voiceover(text=tr("""Los dos vectores tienen las mismas componentes, <bookmark mark='f'/> así que <bookmark mark='r'/> la fila de la transpuesta es <bookmark mark='c'/> la columna de A con el mismo índice.<bookmark mark='v4'/>""",
                                    """The two vectors have the same components, <bookmark mark='f'/> so <bookmark mark='r'/> the row of the transpose is <bookmark mark='c'/> the column of A with the same index.<bookmark mark='v4'/>""")) as tracker:
            jotas = [vuelta[0][0][9], vuelta[0][2][0]]   # el índice de la componente, que va a desaparecer
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.5) for x in jotas], run_time=0.3)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in jotas], run_time=0.3)
            self.wait_until_bookmark("f")
            self.play(FadeIn(rot_vuelta[1]), FadeIn(vuelta[1][1]), *copia(vuelta[0][0], vuelta[1][0], [(g, g-1) for g in range(1, 7)]),
                      *copia(vuelta[0][2], vuelta[1][2], [(3, 0), (4, 1), (5, 2)]), run_time=1.0)
            self.wait_until_bookmark("r")
            self.play(sel_fila_T2.animate.set_color(COLOR_ESCALAR).scale(1.4), run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(sel_fila_T2.animate.set_color(WHITE).scale(1/1.4), sel_col_A2.animate.set_color(COLOR_C).scale(1.4), run_time=0.25)
            self.wait(0.8)
            self.play(sel_col_A2.animate.set_color(WHITE).scale(1/1.4), run_time=0.4)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("La transpuesta de la transpuesta", "The transpose of the transpose"), font_size=40).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = PanelV10(self, [(tr("Definición", "Definition"), "def", r"\VectTC{A}{i}=\VectF{A}{i}"),
                                (tr("Ya demostrado", "Already proved"), "filas", r"\elemLp{\MatT{A}}{i}=\VectC{A}{i}")])
        enunciado = MathTex(r"\TransP*{\MatT{A}}", r"=", r"\Mat{A}", tex_template=myTemplate, font_size=48).move_to([0, 2.2, 0])
        # Glifos: ( ( A T ) T ) | i  =  i | ( A T )  =  A | i
        doble = MathTex(r"\elemRp{\TransP*{\MatT{A}}}{i}", r"=", r"\elemLp{\MatT{A}}{i}", r"=", r"\VectC{A}{i}", tex_template=myTemplate, font_size=52).move_to([0, 0.2, 0])
        
        with self.voiceover(text=tr("""Por último, transponer dos veces devuelve la matriz original.""",
                                    """Finally, transposing twice gives back the original matrix.""")) as tracker:
            self.play(Write(cabecera), FadeIn(panel.todo), run_time=1)
            self.play(Write(enunciado), run_time=1.2)
        
        with self.voiceover(text=tr("""Para demostrarlo necesitará <bookmark mark='p'/> la definición de transpuesta <bookmark mark='q'/> y lo que acabamos de ver sobre sus filas.""",
                                    """To prove it you will need <bookmark mark='p'/> the definition of the transpose <bookmark mark='q'/> and what we have just seen about its rows.""")) as tracker:
            # cada pieza se remarca cuando la voz la nombra
            self.wait_until_bookmark("p")
            panel.pista("def")
            self.wait_until_bookmark("q")
            panel.pista("filas")
        
        self.pausa_para_pensar(invitacion=tr("Demuestre que la transpuesta de la transpuesta es la matriz original.",
                                             "Prove that the transpose of the transpose is the original matrix."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que la transpuesta de la transpuesta de A es A.",
                                                 "Pause the video and try to prove that the transpose of the transpose of A is A."))
        
        with self.voiceover(text=tr("""Empezamos por <bookmark mark='c'/> una columna cualquiera del lado izquierdo.""",
                                    """We start with <bookmark mark='c'/> any column of the left-hand side.""")) as tracker:
            # el lado izquierdo del enunciado baja a la cadena y, al decir «columna», le aparece el selector en verde (Marcos, 2026-11-03)
            self.play(TransformFromCopy(enunciado[0], doble[0][1:6]), run_time=0.8)
            self.wait_until_bookmark("c")
            sel_col = doble[0][7:9]   # glifos: ( ( A T ) T ) | i
            sel_col.set_color(COLOR_C).scale(1.4)
            self.play(FadeIn(doble[0][0]), FadeIn(doble[0][6:]), run_time=0.5)
            self.wait(0.8)
            self.play(sel_col.animate.set_color(WHITE).scale(1/1.4), run_time=0.4)
        
        with self.voiceover(text=tr("""Por la definición de transpuesta, <bookmark mark='a'/> podemos quitar la transposición exterior <bookmark mark='x'/> cambiando de lado el índice.""",
                                    """By the definition of the transpose, <bookmark mark='a'/> we can remove the outer transposition <bookmark mark='x'/> by swapping the side of the index.""")) as tracker:
            panel.senala("def")
            self.wait_until_bookmark("a")
            copia = copia_literal(self, doble[0], doble[2], doble[1])
            self.wait_until_bookmark("x")
            transforma_copia(self, copia, doble[2], [(1, 2), (2, 3), (3, 4), (4, 5), (7, 1), (8, 0)], se_van=[0, 5, 6])
            panel.cuenta("def")
        
        with self.voiceover(text=tr("""Y como cada fila de la transpuesta es la columna de A con el mismo índice, <bookmark mark='b'/> podemos quitar la transposición que queda, <bookmark mark='x'/> y el índice vuelve a su sitio original.""",
                                    """And since each row of the transpose is the column of A with the same index, <bookmark mark='b'/> we can remove the remaining transposition, <bookmark mark='x'/> and the index goes back to its original place.""")) as tracker:
            panel.senala("filas")
            self.wait_until_bookmark("b")
            copia = copia_literal(self, doble[2], doble[4], doble[3])
            self.wait_until_bookmark("x")
            transforma_copia(self, copia, doble[4], [(3, 0), (1, 1), (0, 2)], se_van=[2, 4, 5])
            panel.cuenta("filas")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Como esto es cierto para <bookmark mark='c'/> cualquier columna, <bookmark mark='ok'/> las dos matrices son iguales.""",
                                    """Since this holds for <bookmark mark='c'/> any column, <bookmark mark='ok'/> the two matrices are equal.""")) as tracker:
            self.wait_until_bookmark("c")
            indices = [doble[0][8], doble[4][2]]   # los índices de las columnas, a los dos extremos
            self.play(*[x.animate.set_color(COLOR_C).scale(1.5) for x in indices], run_time=0.3)
            self.wait_until_bookmark("ok")
            marco = SurroundingRectangle(enunciado, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in indices],
                      Create(marco), Indicate(enunciado, color=COLOR_RESULTADO, scale_factor=1.15), run_time=1.5)
        
        with self.voiceover(text=tr("""Hemos usado una vez la definición de transpuesta y una vez lo que vimos sobre sus filas.""",
                                    """We have used the definition of the transpose once, and what we saw about its rows once.""")) as tracker:
            self.play(*[Indicate(panel.contadores[c], color=COLOR_ESCALAR) for c in ("def", "filas")], run_time=1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [r"\VectTC{A}{i}=\VectF{A}{i},\qquad \elemLp{\MatT{A}}{i}=\VectC{A}{i}", r"\eleMT{A}{i}{j}=\eleM{A}{j}{i},\qquad \TransP*{\MatT{A}}=\Mat{A}"]
        rotulos = [tr("transponer convierte las filas en columnas, y viceversa", "transposing turns rows into columns, and vice versa"),
                   tr("transponer = cambiar de lado los índices", "transposing = swapping the sides of the indices")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=44), Tex(r, font_size=28, color=GRAY_B)).arrange(DOWN, buff=0.2)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.7).move_to([0, -0.2, 0])
        
        # «transponer dos veces devuelve» y no «la transpuesta de la transpuesta es»: Tristan pausaba 320-610 ms antes del
        # segundo «de» en todas las tiradas (Marcos lo oyó, 2026-11-02); con el verbo, 40-60 ms
        with self.voiceover(text=tr("""Resumamos. La transposición transforma las filas en columnas, y viceversa. <bookmark mark='r'/> Transponer equivale a cambiar de lado los índices, y transponer dos veces devuelve la matriz original.""",
                                    """Let us sum up. Transposition turns rows into columns, and vice versa. <bookmark mark='r'/> Transposing amounts to swapping the sides of the indices, and transposing twice returns the original matrix.""")) as tracker:   # «returns»: Ollie pausaba 320-370 ms antes de «gives back» en todas las tiradas; con «returns», 180 ms
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(filas[1]), run_time=0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos distintos tipos de matrices.""",
                                    """In the next video we will see different types of matrices.""")) as tracker:
            pass
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos_finales()


class L01_V10_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class L01_V10_E01_Transposicion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        # Aᵀ a la izquierda y A a la derecha, como los lados de la definición (Aᵀ)|i = i|A que va debajo (Marcos, 2026-11-03)
        A = matriz(A_EJ)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([3.0, 1.2, 0])
        T = matriz([list(f) for f in zip(*A_EJ)])
        f_T = con_nombre(r"\Mat{B}=", T).move_to([-3.3, 1.2, 0])
        nombre_T = MathTex(r"\MatT{A}=", tex_template=myTemplate, font_size=48).move_to(f_T[0], aligned_edge=RIGHT)
        defin = MathTex(r"\VectTC{A}{i}", r"=", r"\VectF{A}{i}", tex_template=myTemplate, font_size=52).move_to([0, -1.5, 0])
        r_col = Tex(tr(r"columna $i$ de $\MatT{A}$", r"column $i$ of $\MatT{A}$"), tex_template=myTemplate, font_size=28, color=GRAY_B).next_to(defin[0], DOWN, buff=0.3)
        r_fil = Tex(tr(r"fila $i$ de $\Mat{A}$", r"row $i$ of $\Mat{A}$"), tex_template=myTemplate, font_size=28, color=GRAY_B).next_to(defin[2], DOWN, buff=0.3)
        orden = MathTex(r"\Mat{A}\in\R[m\times n]", r"\quad\Rightarrow\quad", r"\MatT{A}\in\R[n\times m]", tex_template=myTemplate, font_size=48).move_to([0, -3.0, 0])
        
        # arranque: qué se va a ver en este vídeo (el resto de la escena recuerda V09 solo donde lo usa)
        with self.voiceover(text=tr("""En este vídeo veremos una operación con matrices: la transposición.""",
                                    """In this video we will see an operation on matrices: transposition.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        with self.voiceover(text=tr("""En el vídeo anterior formamos la matriz B con dos vectores: <bookmark mark='x'/> el primero llevaba los números de la primera fila de A, <bookmark mark='y'/> y el segundo, los de la segunda.""",
                                    """In the previous video we built the matrix B with two vectors: <bookmark mark='x'/> the first one carried the numbers of the first row of A, <bookmark mark='y'/> and the second one, those of the second row.""")) as tracker:
            self.play(FadeIn(f_A), FadeIn(f_T[0]), FadeIn(T.get_brackets()), run_time=1)
            for i, marca in enumerate(["x", "y"]):
                self.wait_until_bookmark(marca)
                fr = franja_fila(A, i)
                self.play(FadeIn(fr), run_time=0.4)
                self.play(TransformFromCopy(A.get_rows()[i], T.get_columns()[i]), run_time=1.2)
                self.play(FadeOut(fr), run_time=0.3)
        
        with self.voiceover(text=tr("""Convertir las filas de una matriz en las columnas de otra se llama transposición. <bookmark mark='t'/> La matriz B es la transpuesta de A, que se escribe con una T en el superíndice.""",
                                    """Turning the rows of a matrix into the columns of another is called transposition. <bookmark mark='t'/> The matrix B is the transpose of A, which is written with a T as a superscript.""")) as tracker:
            self.wait_until_bookmark("t")
            self.play(FadeTransform(f_T[0], nombre_T), run_time=1.2)
        
        # la correspondencia se contaba tres veces; queda la regla general (Marcos, 2026-10-31)
        with self.voiceover(text=tr("""Cada columna de la transpuesta es la fila de A <bookmark mark='m'/> con el mismo índice.""",
                                    """Each column of the transpose is the row of A <bookmark mark='m'/> with the same index.""")) as tracker:
            self.play(Write(defin), FadeIn(r_col), FadeIn(r_fil), run_time=1.2)
            self.wait_until_bookmark("m")
            franjas = None
            for i in range(2):   # el mismo índice, ilustrado con las dos columnas
                nuevas = VGroup(franja_columna(T, i), franja_fila(A, i))
                self.play(FadeIn(nuevas) if franjas is None else ReplacementTransform(franjas, nuevas), run_time=0.6)
                self.wait(0.4)
                franjas = nuevas
        
        with self.voiceover(text=tr("""Si A tiene m filas de n componentes, su transpuesta tiene m columnas de n componentes: es de orden 'n' por 'm'.<bookmark mark='v2'/>""",  # comillas y tirada 2: sin ellas sonaba «m por m» (Marcos)
                                    """If A has m rows of n components, its transpose has m columns of n components: it is of order n by m.""")) as tracker:
            self.play(FadeOut(franjas), FadeIn(orden), run_time=1)
        
        # Antes era la escena 4, de una sola frase con su cabecera; ahora ocupa el sitio de la definición
        # (Marcos, 2026-11-01). Con «Por ejemplo» ilustra la regla del orden que se acaba de decir.
        colm = MathTex(r"\begin{bmatrix}9\\ 2\end{bmatrix}", tex_template=myTemplate, font_size=52)
        film = MathTex(r"{\begin{bmatrix}9\\ 2\end{bmatrix}}^{\T}", r"=", r"\begin{bmatrix}9 & 2\end{bmatrix}", tex_template=myTemplate, font_size=52)
        r_c = Tex(tr(r"matriz columna, $2\times 1$", r"column matrix, $2\times 1$"), font_size=32, color=GRAY_B)
        r_f = Tex(tr(r"matriz fila, $1\times 2$", r"row matrix, $1\times 2$"), font_size=32, color=GRAY_B)
        grupos = VGroup(*[VGroup(f, r).arrange(DOWN, buff=0.4) for f, r in [(colm, r_c), (film, r_f)]])
        grupos.arrange(RIGHT, buff=1.6, aligned_edge=DOWN).move_to([0, -1.25, 0])
        
        with self.voiceover(text=tr("""Por ejemplo, <bookmark mark='c'/> la transpuesta de una matriz columna <bookmark mark='f'/> es una matriz fila.""",
                                    """For example, <bookmark mark='c'/> the transpose of a column matrix <bookmark mark='f'/> is a row matrix.""")) as tracker:
            self.play(FadeOut(VGroup(defin, r_col, r_fil)), run_time=0.6)
            self.wait_until_bookmark("c")
            self.play(FadeIn(colm), FadeIn(r_c), run_time=0.8)
            self.wait_until_bookmark("f")
            self.play(FadeIn(film), FadeIn(r_f), run_time=1.2)
        
        self.pausa_media()


class L01_V10_E02_CambioDeIndices(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Transponer es cambiar de lado los índices", "Transposing swaps the sides of the indices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        orden_sel = tr("da igual el orden de selección", "the order of selection does not matter")
        x_rot = 1.6
        # Ida. Glifos:
        #   ida[0]: ( A T ) | j        =  j | A
        #   ida[1]: i | ( ( A T ) | j )  =  ( j | A ) | i
        #   ida[2]: i | ( A T ) | j      =  j | A | i
        ida = [MathTex(r"\VectTC{A}{j}", r"=", r"\VectF{A}{j}", tex_template=myTemplate, font_size=48),
               MathTex(r"\elemLp{\VectTC{A}{j}}{i}", r"=", r"\elemRp{\VectF{A}{j}}{i}", tex_template=myTemplate, font_size=48),
               MathTex(r"\eleMT{A}{i}{j}", r"=", r"\eleM{A}{j}{i}", tex_template=myTemplate, font_size=48)]
        columna_de_lineas(ida, x0=-1.0, y0=1.6, dy=1.2)
        rot_ida = [rotulo(tr("definición de transpuesta", "definition of the transpose"), ida[0], x=x_rot),
                   rotulo(tr("vectores iguales: mismas componentes", "equal vectors: same components"), ida[1], x=x_rot),
                   rotulo(orden_sel, ida[2], x=x_rot)]
        regla = MathTex(r"\eleMT{A}{i}{j}", r"=", r"\eleM{A}{j}{i}", tex_template=myTemplate, font_size=56).move_to([1.2, 1.6, 0])
        idea = aviso("idea").next_to(regla, LEFT, buff=0.8)
        # Vuelta. Glifos:
        #   vuelta[0]: ( i | ( A T ) ) | j  =  j | ( A | i )
        #   vuelta[1]: i | ( A T )          =  A | i
        vuelta = [MathTex(r"\elemRp{\VectTF{A}{i}}{j}", r"=", r"\elemLp{\VectC{A}{i}}{j}", tex_template=myTemplate, font_size=48),
                  MathTex(r"\elemLp{\MatT{A}}{i}", r"=", r"\VectC{A}{i}", tex_template=myTemplate, font_size=48)]
        columna_de_lineas(vuelta, x0=-1.0, y0=0.1, dy=1.3)
        rot_vuelta = [rotulo(orden_sel, vuelta[0], x=x_rot),
                      rotulo(tr("vale para cualquier componente", "holds for any component"), vuelta[1], x=x_rot)]
        
        
        def copia(origen, destino, parejas):
            return [TransformFromCopy(origen[i], destino[j]) for i, j in parejas]
        
        
        with self.voiceover(text=tr("""Partimos de la definición de transpuesta: <bookmark mark='d'/> cada columna de la transpuesta es la fila de A con el mismo índice.""",
                                    """We start from the definition of the transpose: <bookmark mark='d'/> each column of the transpose is the row of A with the same index.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("d")
            self.play(FadeIn(ida[0]), FadeIn(rot_ida[0]), run_time=1)
        
        with self.voiceover(text=tr("""Son dos vectores iguales, así que tienen las mismas componentes. <bookmark mark='y'/> Seleccionamos la componente i-ésima de los dos: <bookmark mark='x1'/> en la columna, por la izquierda, <bookmark mark='x2'/> y en la fila, por la derecha.""",
                                    """They are two equal vectors, so they have the same components. <bookmark mark='y'/> We select the i-th component of both: <bookmark mark='x1'/> in the column, from the left, <bookmark mark='x2'/> and in the row, from the right.""")) as tracker:
            self.play(FadeIn(rot_ida[1]), run_time=0.6)
            self.wait_until_bookmark("y")
            self.play(FadeIn(ida[1][1]), *copia(ida[0][0], ida[1][0], [(0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8)]),
                      *copia(ida[0][2], ida[1][2], [(0, 1), (1, 2), (2, 3)]), run_time=1.2)
            self.wait_until_bookmark("x1")
            self.play(FadeIn(ida[1][0][0:3]), FadeIn(ida[1][0][9]), run_time=0.8)   # i|( ... )
            self.wait_until_bookmark("x2")
            self.play(FadeIn(ida[1][2][0]), FadeIn(ida[1][2][4:]), run_time=0.8)    # ( ... )|i
        
        # «da igual el orden de selección» se demostró en V09 (escena 7): se recuerda la primera vez que se usa
        # la línea nueva nace cuando la voz dice «podemos quitar los paréntesis», no antes (Marcos, 2026-11-02)
        # recordatorio del motivo (Marcos, 2026-11-03), como en V09: los paréntesis exteriores de los dos lados se ponen en
        # amarillo y viajan a la otra colocación y vuelven mientras la voz dice «da igual el orden...».
        # glifos: ida[1][0] = i | ( ( A T ) | j )  ->  ( i | ( A T ) ) | j ;  ida[1][2] = ( j | A ) | i  ->  j | ( A | i )
        otra_izq = MathTex(r"\elemRp{\VectTF{A}{i}}{j}", tex_template=myTemplate, font_size=48).move_to(ida[1][0])
        otra_der = MathTex(r"\elemLp{\VectC{A}{i}}{j}", tex_template=myTemplate, font_size=48).move_to(ida[1][2])
        parentesis = [ida[1][0][2], ida[1][0][9], ida[1][2][0], ida[1][2][4]]
        with self.voiceover(text=tr("""En el vídeo anterior vimos que <bookmark mark='o'/> da igual el orden en que se aplican los selectores, así que <bookmark mark='x'/> podemos quitar los paréntesis.""",
                                    """In the previous video we saw that <bookmark mark='o'/> the order in which the selectors are applied does not matter, so <bookmark mark='x'/> we can drop the parentheses.""")) as tracker:
            self.play(FadeIn(rot_ida[2]), run_time=0.6)
            self.wait_until_bookmark("o")
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.3) for x in parentesis], run_time=0.3)
            self.play(*[Transform(ida[1][0][i], otra_izq[0][j], rate_func=rate_functions.there_and_back_with_pause)
                        for i, j in zip(range(10), [1, 2, 0, 3, 4, 5, 6, 8, 9, 7])],
                      *[Transform(ida[1][2][i], otra_der[0][j], rate_func=rate_functions.there_and_back_with_pause)
                        for i, j in zip(range(7), [2, 0, 1, 3, 6, 4, 5])], run_time=2.0)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.3) for x in parentesis], run_time=0.3)
            self.wait_until_bookmark("x")
            self.play(FadeIn(ida[2][1]), *copia(ida[1][0], ida[2][0], [(0, 0), (1, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7)]),
                      *copia(ida[1][2], ida[2][2], [(1, 0), (2, 1), (3, 2), (5, 3), (6, 4)]), run_time=1.5)   # los paréntesis no aparecen
        
        # «Así que», no «Hemos demostrado»: la cadena constata que la notación funciona como debe, es una regla de
        # lectura de la notación, no un resultado sobre matrices (Marcos, 2026-11-02)
        # «Por tanto», no «Así que»: la frase anterior ya acaba en «así que podemos quitar los paréntesis» (Marcos, 2026-11-02)
        with self.voiceover(text=tr("""Por tanto, transponer intercambia los índices <bookmark mark='f'/> de la fila <bookmark mark='c'/> y de la columna.""",
                                    """Therefore, transposing swaps <bookmark mark='f'/> the row index <bookmark mark='c'/> and the column index.""")) as tracker:
            # resaltados inmediatos y sostenidos (la frase es corta): las dos i al decir «fila», las dos j al decir «columna»
            ies, jotas = [ida[2][0][0], ida[2][2][4]], [ida[2][0][7], ida[2][2][0]]   # glifos: i | ( A T ) | j  y  j | A | i
            self.wait_until_bookmark("f")
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.5) for x in ies], run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in ies], *[x.animate.set_color(COLOR_C).scale(1.5) for x in jotas], run_time=0.25)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in jotas], run_time=0.4)
        
        self.play(FadeOut(VGroup(ida[0], ida[1], *rot_ida)), ReplacementTransform(ida[2], regla), run_time=1.2)   # la última línea es la regla
        with self.voiceover(text=tr("""De aquí sale una regla de reescritura: transponer, o quitar la transposición, intercambia los índices de lado.""",
                                    """This gives us a rewriting rule: transposing, or removing the transposition, swaps the sides of the indices.""")) as tracker:
            self.play(FadeIn(idea), run_time=0.8)
        
        # Vuelta: en la regla se vuelven a poner los paréntesis (fila de la transpuesta y columna de A)
        # al decir «una fila de la transpuesta» se destaca el selector i| sobre Aᵀ (amarillo, color de fila) y al decir
        # «una columna de A», el |i sobre A (verde, color de columna) (Marcos, 2026-11-03)
        sel_fila_T, sel_col_A = vuelta[0][0][1:3], vuelta[0][2][4:6]   # glifos: ( i | ( A T ) ) | j  y  j | ( A | i )
        with self.voiceover(text=tr("""Esta regla también describe las filas de la transpuesta. <bookmark mark='y'/> Como da igual el orden en que se aplican los selectores, <bookmark mark='x'/> podemos seleccionar primero <bookmark mark='f'/> una fila de la transpuesta <bookmark mark='c'/> y una columna de A.""",
                                    """This rule also describes the rows of the transpose. <bookmark mark='y'/> Since the order in which the selectors are applied does not matter, <bookmark mark='x'/> we can select <bookmark mark='f'/> a row of the transpose <bookmark mark='c'/> and a column of A first.""")) as tracker:
            self.wait_until_bookmark("y")
            self.play(FadeIn(rot_vuelta[0]), FadeIn(vuelta[0][1]),
                      *copia(regla[0], vuelta[0][0], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8), (7, 9)]),
                      *copia(regla[2], vuelta[0][2], [(0, 0), (1, 1), (2, 3), (3, 4), (4, 5)]), run_time=1.2)
            self.wait_until_bookmark("x")
            self.play(FadeIn(VGroup(vuelta[0][0][0], vuelta[0][0][7], vuelta[0][2][2], vuelta[0][2][6])), run_time=0.8)   # los paréntesis
            self.wait_until_bookmark("f")
            self.play(sel_fila_T.animate.set_color(COLOR_ESCALAR).scale(1.4), run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(sel_fila_T.animate.set_color(WHITE).scale(1/1.4), sel_col_A.animate.set_color(COLOR_C).scale(1.4), run_time=0.25)
            self.wait(0.8)
            self.play(sel_col_A.animate.set_color(WHITE).scale(1/1.4), run_time=0.4)
        
        # «la fila de la transpuesta» destaca i| sobre Aᵀ y «la columna de A» el |i sobre A, en la línea nueva (Marcos, 2026-11-03)
        sel_fila_T2, sel_col_A2 = vuelta[1][0][0:2], vuelta[1][2][1:3]   # glifos: i | ( A T )  y  A | i
        with self.voiceover(text=tr("""Los dos vectores tienen las mismas componentes, <bookmark mark='f'/> así que <bookmark mark='r'/> la fila de la transpuesta es <bookmark mark='c'/> la columna de A con el mismo índice.<bookmark mark='v4'/>""",
                                    """The two vectors have the same components, <bookmark mark='f'/> so <bookmark mark='r'/> the row of the transpose is <bookmark mark='c'/> the column of A with the same index.<bookmark mark='v4'/>""")) as tracker:
            jotas = [vuelta[0][0][9], vuelta[0][2][0]]   # el índice de la componente, que va a desaparecer
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.5) for x in jotas], run_time=0.3)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in jotas], run_time=0.3)
            self.wait_until_bookmark("f")
            self.play(FadeIn(rot_vuelta[1]), FadeIn(vuelta[1][1]), *copia(vuelta[0][0], vuelta[1][0], [(g, g-1) for g in range(1, 7)]),
                      *copia(vuelta[0][2], vuelta[1][2], [(3, 0), (4, 1), (5, 2)]), run_time=1.0)
            self.wait_until_bookmark("r")
            self.play(sel_fila_T2.animate.set_color(COLOR_ESCALAR).scale(1.4), run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(sel_fila_T2.animate.set_color(WHITE).scale(1/1.4), sel_col_A2.animate.set_color(COLOR_C).scale(1.4), run_time=0.25)
            self.wait(0.8)
            self.play(sel_col_A2.animate.set_color(WHITE).scale(1/1.4), run_time=0.4)
        
        self.pausa_media()


class L01_V10_E03_TranspuestaDeLaTranspuesta(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La transpuesta de la transpuesta", "The transpose of the transpose"), font_size=40).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = PanelV10(self, [(tr("Definición", "Definition"), "def", r"\VectTC{A}{i}=\VectF{A}{i}"),
                                (tr("Ya demostrado", "Already proved"), "filas", r"\elemLp{\MatT{A}}{i}=\VectC{A}{i}")])
        enunciado = MathTex(r"\TransP*{\MatT{A}}", r"=", r"\Mat{A}", tex_template=myTemplate, font_size=48).move_to([0, 2.2, 0])
        # Glifos: ( ( A T ) T ) | i  =  i | ( A T )  =  A | i
        doble = MathTex(r"\elemRp{\TransP*{\MatT{A}}}{i}", r"=", r"\elemLp{\MatT{A}}{i}", r"=", r"\VectC{A}{i}", tex_template=myTemplate, font_size=52).move_to([0, 0.2, 0])
        
        with self.voiceover(text=tr("""Por último, transponer dos veces devuelve la matriz original.""",
                                    """Finally, transposing twice gives back the original matrix.""")) as tracker:
            self.play(Write(cabecera), FadeIn(panel.todo), run_time=1)
            self.play(Write(enunciado), run_time=1.2)
        
        with self.voiceover(text=tr("""Para demostrarlo necesitará <bookmark mark='p'/> la definición de transpuesta <bookmark mark='q'/> y lo que acabamos de ver sobre sus filas.""",
                                    """To prove it you will need <bookmark mark='p'/> the definition of the transpose <bookmark mark='q'/> and what we have just seen about its rows.""")) as tracker:
            # cada pieza se remarca cuando la voz la nombra
            self.wait_until_bookmark("p")
            panel.pista("def")
            self.wait_until_bookmark("q")
            panel.pista("filas")
        
        self.pausa_para_pensar(invitacion=tr("Demuestre que la transpuesta de la transpuesta es la matriz original.",
                                             "Prove that the transpose of the transpose is the original matrix."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que la transpuesta de la transpuesta de A es A.",
                                                 "Pause the video and try to prove that the transpose of the transpose of A is A."))
        
        with self.voiceover(text=tr("""Empezamos por <bookmark mark='c'/> una columna cualquiera del lado izquierdo.""",
                                    """We start with <bookmark mark='c'/> any column of the left-hand side.""")) as tracker:
            # el lado izquierdo del enunciado baja a la cadena y, al decir «columna», le aparece el selector en verde (Marcos, 2026-11-03)
            self.play(TransformFromCopy(enunciado[0], doble[0][1:6]), run_time=0.8)
            self.wait_until_bookmark("c")
            sel_col = doble[0][7:9]   # glifos: ( ( A T ) T ) | i
            sel_col.set_color(COLOR_C).scale(1.4)
            self.play(FadeIn(doble[0][0]), FadeIn(doble[0][6:]), run_time=0.5)
            self.wait(0.8)
            self.play(sel_col.animate.set_color(WHITE).scale(1/1.4), run_time=0.4)
        
        with self.voiceover(text=tr("""Por la definición de transpuesta, <bookmark mark='a'/> podemos quitar la transposición exterior <bookmark mark='x'/> cambiando de lado el índice.""",
                                    """By the definition of the transpose, <bookmark mark='a'/> we can remove the outer transposition <bookmark mark='x'/> by swapping the side of the index.""")) as tracker:
            panel.senala("def")
            self.wait_until_bookmark("a")
            copia = copia_literal(self, doble[0], doble[2], doble[1])
            self.wait_until_bookmark("x")
            transforma_copia(self, copia, doble[2], [(1, 2), (2, 3), (3, 4), (4, 5), (7, 1), (8, 0)], se_van=[0, 5, 6])
            panel.cuenta("def")
        
        with self.voiceover(text=tr("""Y como cada fila de la transpuesta es la columna de A con el mismo índice, <bookmark mark='b'/> podemos quitar la transposición que queda, <bookmark mark='x'/> y el índice vuelve a su sitio original.""",
                                    """And since each row of the transpose is the column of A with the same index, <bookmark mark='b'/> we can remove the remaining transposition, <bookmark mark='x'/> and the index goes back to its original place.""")) as tracker:
            panel.senala("filas")
            self.wait_until_bookmark("b")
            copia = copia_literal(self, doble[2], doble[4], doble[3])
            self.wait_until_bookmark("x")
            transforma_copia(self, copia, doble[4], [(3, 0), (1, 1), (0, 2)], se_van=[2, 4, 5])
            panel.cuenta("filas")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Como esto es cierto para <bookmark mark='c'/> cualquier columna, <bookmark mark='ok'/> las dos matrices son iguales.""",
                                    """Since this holds for <bookmark mark='c'/> any column, <bookmark mark='ok'/> the two matrices are equal.""")) as tracker:
            self.wait_until_bookmark("c")
            indices = [doble[0][8], doble[4][2]]   # los índices de las columnas, a los dos extremos
            self.play(*[x.animate.set_color(COLOR_C).scale(1.5) for x in indices], run_time=0.3)
            self.wait_until_bookmark("ok")
            marco = SurroundingRectangle(enunciado, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in indices],
                      Create(marco), Indicate(enunciado, color=COLOR_RESULTADO, scale_factor=1.15), run_time=1.5)
        
        with self.voiceover(text=tr("""Hemos usado una vez la definición de transpuesta y una vez lo que vimos sobre sus filas.""",
                                    """We have used the definition of the transpose once, and what we saw about its rows once.""")) as tracker:
            self.play(*[Indicate(panel.contadores[c], color=COLOR_ESCALAR) for c in ("def", "filas")], run_time=1.2)
        
        self.pausa_media()


class L01_V10_E04_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [r"\VectTC{A}{i}=\VectF{A}{i},\qquad \elemLp{\MatT{A}}{i}=\VectC{A}{i}", r"\eleMT{A}{i}{j}=\eleM{A}{j}{i},\qquad \TransP*{\MatT{A}}=\Mat{A}"]
        rotulos = [tr("transponer convierte las filas en columnas, y viceversa", "transposing turns rows into columns, and vice versa"),
                   tr("transponer = cambiar de lado los índices", "transposing = swapping the sides of the indices")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=44), Tex(r, font_size=28, color=GRAY_B)).arrange(DOWN, buff=0.2)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.7).move_to([0, -0.2, 0])
        
        # «transponer dos veces devuelve» y no «la transpuesta de la transpuesta es»: Tristan pausaba 320-610 ms antes del
        # segundo «de» en todas las tiradas (Marcos lo oyó, 2026-11-02); con el verbo, 40-60 ms
        with self.voiceover(text=tr("""Resumamos. La transposición transforma las filas en columnas, y viceversa. <bookmark mark='r'/> Transponer equivale a cambiar de lado los índices, y transponer dos veces devuelve la matriz original.""",
                                    """Let us sum up. Transposition turns rows into columns, and vice versa. <bookmark mark='r'/> Transposing amounts to swapping the sides of the indices, and transposing twice returns the original matrix.""")) as tracker:   # «returns»: Ollie pausaba 320-370 ms antes de «gives back» en todas las tiradas; con «returns», 180 ms
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(filas[1]), run_time=0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos distintos tipos de matrices.""",
                                    """In the next video we will see different types of matrices.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
