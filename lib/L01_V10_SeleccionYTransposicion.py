from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Selección y transposición", "Selection and transposition")

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


def rotulo(texto, junto_a, x=None, font_size=28):
    """Rótulo gris pequeño a la derecha de una línea (la regla que justifica el paso)."""
    r = Tex(texto, tex_template=myTemplate, font_size=font_size, color=GRAY_B)
    r.next_to(junto_a, RIGHT, buff=0.6)
    if x is not None:
        r.shift((x - r.get_left()[0])*RIGHT)
    return r

class L01_V10_SeleccionYTransposicion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        A = matriz(A_SEL)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([0, 1.0, 0])
        comp = MathTex(r"\eleM{A}{2}{1}", r"=", r"7", tex_template=myTemplate, font_size=52).move_to([0, -1.4, 0])
        
        with self.voiceover(text=tr("""En el vídeo anterior vimos que el operador selector, actuando por ambos lados de una matriz, selecciona una componente.""",
                                    """In the previous video we saw that the selector operator, acting on both sides of a matrix, selects a component.""")) as tracker:
            self.play(Write(titulo), FadeIn(f_A), run_time=1.2)
            self.play(Write(comp), run_time=1.2)
        
        with self.voiceover(text=tr("""Esa componente está a la vez en una fila y en una columna: <bookmark mark='f'/> en la segunda fila <bookmark mark='c'/> y en la primera columna.""",
                                    """That component lies both in a row and in a column: <bookmark mark='f'/> in the second row <bookmark mark='c'/> and in the first column.""")) as tracker:
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 1)
            self.play(FadeIn(ff), run_time=0.5)
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0, color=COLOR_C)
            self.play(FadeIn(fc), run_time=0.5)
            self.play(Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
        
        with self.voiceover(text=tr("""Así que también debería poder obtenerse seleccionando primero la fila, o primero la columna.""",
                                    """So we should also be able to get it by selecting the row first, or the column first.""")) as tracker:
            self.play(Indicate(ff, color=COLOR_ESCALAR, scale_factor=1.05), run_time=1)
            self.play(Indicate(fc, color=COLOR_C, scale_factor=1.05), run_time=1)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Primero la fila o primero la columna", "Row first or column first"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A = matriz(A_SEL)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([0, 2.0, 0])
        por_fila = MathTex(r"\elemRp{\VectF{A}{2}}{1}", r"=", r"\elemR{(7,\ 0,\ 3,)}{1}", r"=", r"7", tex_template=myTemplate, font_size=48)
        por_col = MathTex(r"\elemLp{\VectC{A}{1}}{2}", r"=", r"\elemL{\begin{pmatrix}1\\ 7\end{pmatrix}}{2}", r"=", r"7", tex_template=myTemplate, font_size=48)
        lineas = columna_de_lineas([por_fila, por_col], x0=-1.6, y0=0.3, dy=1.45)
        convenio = MathTex(r"\eleVL{a}{i}", r"=", r"\eleVR{a}{i}", r"=", r"a_i", tex_template=myTemplate, font_size=52).move_to([0.8, -2.7, 0])
        idea = aviso("idea").next_to(convenio, LEFT, buff=0.8)
        conclusion = MathTex(r"\elemRp{\VectF{A}{2}}{1}", r"=", r"\elemLp{\VectC{A}{1}}{2}", r"=", r"\eleM{A}{2}{1}",
                             tex_template=myTemplate, font_size=52).move_to([0, 0.2, 0])
        
        with self.voiceover(text=tr("""Seleccionemos primero la segunda fila, <bookmark mark='f'/> que es un vector. <bookmark mark='c'/> Su primera componente es el siete.""",
                                    """Let us first select the second row, <bookmark mark='f'/> which is a vector. <bookmark mark='c'/> Its first component is the seven.""")) as tracker:
            self.play(Write(cabecera), FadeIn(f_A), FadeIn(por_fila[0]), run_time=1)
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 1)
            self.play(FadeIn(ff), FadeIn(por_fila[1:3]), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(FadeIn(por_fila[3:]), Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
        
        with self.voiceover(text=tr("""Ahora seleccionemos primero la primera columna, <bookmark mark='c'/> que también es un vector. <bookmark mark='s'/> El siete es su segunda componente.""",
                                    """Now let us first select the first column, <bookmark mark='c'/> which is also a vector. <bookmark mark='s'/> The seven is its second component.""")) as tracker:
            self.play(FadeOut(ff), FadeIn(por_col[0]), run_time=0.8)
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0, color=COLOR_C)
            self.play(FadeIn(fc), FadeIn(por_col[1:3]), run_time=0.8)
            self.wait_until_bookmark("s")
            self.play(FadeIn(por_col[3:]), Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
        
        with self.voiceover(text=tr("""Pero aquí el selector actúa por la izquierda de un vector. <bookmark mark='a'/> Para que esto tenga sentido, aceptaremos que el selector pueda actuar por cualquier lado de un vector, <bookmark mark='d'/> con el mismo resultado.""",
                                    """But here the selector acts on the left of a vector. <bookmark mark='a'/> For this to make sense, we will allow the selector to act on either side of a vector, <bookmark mark='d'/> with the same result.""")) as tracker:
            self.play(FadeOut(fc), Indicate(por_col[2], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1)
            self.wait_until_bookmark("a")
            self.play(FadeIn(idea), FadeIn(convenio[0]), run_time=0.8)
            self.wait_until_bookmark("d")
            self.play(FadeIn(convenio[1:]), run_time=0.8)
        
        with self.voiceover(text=tr("""Con este convenio, da igual seleccionar primero la fila o la columna: <bookmark mark='q'/> por eso podemos quitar los paréntesis y escribir el selector a ambos lados de la matriz.""",
                                    """With this convention, it makes no difference whether we select the row or the column first: <bookmark mark='q'/> that is why we can drop the parentheses and write the selector on both sides of the matrix.""")) as tracker:
            self.play(ReplacementTransform(por_fila[0], conclusion[0]), ReplacementTransform(por_col[0], conclusion[2]), FadeIn(conclusion[1]),
                      FadeOut(VGroup(por_fila[1:], por_col[1:])), run_time=1.2)
            self.wait_until_bookmark("q")
            self.play(FadeIn(conclusion[3:]), run_time=1)
        
        with self.voiceover(text=tr("""Lo hemos visto en un ejemplo, pero vale para cualquier componente de cualquier matriz, porque toda componente está a la vez en su fila y en su columna.""",
                                    """We have seen it in an example, but it holds for any component of any matrix, because every component lies both in its row and in its column.""")) as tracker:
            self.play(Indicate(conclusion[4], color=COLOR_ESCALAR, scale_factor=1.1), run_time=1)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("La transposición", "Transposition"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A = matriz(A_EJ)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([-3.3, 1.2, 0])
        T = matriz([list(f) for f in zip(*A_EJ)])
        f_T = con_nombre(r"\Mat{B}=", T).move_to([3.0, 1.2, 0])
        nombre_T = MathTex(r"\MatT{A}=", tex_template=myTemplate, font_size=48).move_to(f_T[0], aligned_edge=RIGHT)
        defin = MathTex(r"\VectTC{A}{i}", r"=", r"\VectF{A}{i}", tex_template=myTemplate, font_size=52).move_to([0, -1.5, 0])
        r_col = Tex(tr(r"columna $i$ de $\MatT{A}$", r"column $i$ of $\MatT{A}$"), tex_template=myTemplate, font_size=28, color=GRAY_B).next_to(defin[0], DOWN, buff=0.3)
        r_fil = Tex(tr(r"fila $i$ de $\Mat{A}$", r"row $i$ of $\Mat{A}$"), tex_template=myTemplate, font_size=28, color=GRAY_B).next_to(defin[2], DOWN, buff=0.3)
        orden = MathTex(r"\Mat{A}\in\R[m\times n]", r"\quad\Rightarrow\quad", r"\MatT{A}\in\R[n\times m]", tex_template=myTemplate, font_size=48).move_to([0, -3.0, 0])
        
        with self.voiceover(text=tr("""En el vídeo anterior formamos la matriz B con dos vectores: <bookmark mark='x'/> el primero llevaba los números de la primera fila de A, <bookmark mark='y'/> y el segundo, los de la segunda.""",
                                    """In the previous video we built the matrix B with two vectors: <bookmark mark='x'/> the first one carried the numbers of the first row of A, <bookmark mark='y'/> and the second one, those of the second row.""")) as tracker:
            self.play(Write(cabecera), FadeIn(f_A), FadeIn(f_T[0]), FadeIn(T.get_brackets()), run_time=1)
            for i, marca in enumerate(["x", "y"]):
                self.wait_until_bookmark(marca)
                fr = franja_fila(A, i)
                self.play(FadeIn(fr), run_time=0.4)
                self.play(TransformFromCopy(A.get_rows()[i], T.get_columns()[i]), run_time=1.2)
                self.play(FadeOut(fr), run_time=0.3)
        
        with self.voiceover(text=tr("""Convertir las filas de una matriz en columnas se llama transposición. <bookmark mark='t'/> La matriz B es la transpuesta de A, que se escribe con una T en el superíndice.""",
                                    """Turning the rows of a matrix into columns is called transposition. <bookmark mark='t'/> The matrix B is the transpose of A, which is written with a T as a superscript.""")) as tracker:
            self.wait_until_bookmark("t")
            self.play(FadeTransform(f_T[0], nombre_T), run_time=1.2)
        
        with self.voiceover(text=tr("""Es decir, cada columna de la transpuesta es la fila de A con el mismo índice: <bookmark mark='c1'/> la primera columna de A transpuesta es la primera fila de A, <bookmark mark='c2'/> y la segunda, la segunda.""",
                                    """That is, each column of the transpose is the row of A with the same index: <bookmark mark='c1'/> the first column of A transpose is the first row of A, <bookmark mark='c2'/> and the second, the second.""")) as tracker:
            self.play(Write(defin), FadeIn(r_col), FadeIn(r_fil), run_time=1.2)
            franjas = None
            for i, marca in enumerate(["c1", "c2"]):
                self.wait_until_bookmark(marca)
                nuevas = VGroup(franja_columna(T, i), franja_fila(A, i))
                self.play(FadeIn(nuevas) if franjas is None else ReplacementTransform(franjas, nuevas), run_time=0.6)
                franjas = nuevas
        
        with self.voiceover(text=tr("""Por eso, si A es de orden m por n, su transpuesta es de orden n por m.""",
                                    """That is why, if A is of order m by n, its transpose is of order n by m.""")) as tracker:
            self.play(FadeOut(franjas), FadeIn(orden), run_time=1)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Vector, matriz columna y matriz fila", "Vector, column matrix and row matrix"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        v = MathTex(r"\Vect{a}=(9,\ 2,)", tex_template=myTemplate, font_size=48)
        colm = MathTex(r"\begin{bmatrix}\Vect{a}\end{bmatrix}", r"=", r"\begin{bmatrix}9\\ 2\end{bmatrix}", tex_template=myTemplate, font_size=48)
        film = MathTex(r"{\begin{bmatrix}\Vect{a}\end{bmatrix}}^{\T}", r"=", r"\begin{bmatrix}9 & 2\end{bmatrix}", tex_template=myTemplate, font_size=48)
        r_v = Tex(tr("vector", "vector"), font_size=30, color=GRAY_B)
        r_c = Tex(tr(r"matriz columna, $2\times 1$", r"column matrix, $2\times 1$"), font_size=30, color=GRAY_B)
        r_f = Tex(tr(r"matriz fila, $1\times 2$", r"row matrix, $1\times 2$"), font_size=30, color=GRAY_B)
        grupos = VGroup(*[VGroup(f, r).arrange(DOWN, buff=0.4) for f, r in [(v, r_v), (colm, r_c), (film, r_f)]])
        grupos.arrange(RIGHT, buff=1.2, aligned_edge=DOWN).move_to([0, 0.6, 0])
        sis_c = MathTex(r"\begin{bmatrix}\begin{pmatrix}9\\ 2\end{pmatrix};\end{bmatrix}", tex_template=myTemplate, font_size=44).next_to(r_c, DOWN, buff=0.35)
        sis_f = MathTex(r"\left[(9,);\ (2,);\right]", tex_template=myTemplate, font_size=44).next_to(r_f, DOWN, buff=0.35).match_y(sis_c)
        l_c = Tex(tr(r"un vector de $\R[2]$", r"one vector of $\R[2]$"), tex_template=myTemplate, font_size=30, color=COLOR_ESCALAR).next_to(sis_c, DOWN, buff=0.25)
        l_f = Tex(tr(r"dos vectores de $\R[1]$", r"two vectors of $\R[1]$"), tex_template=myTemplate, font_size=30, color=COLOR_ESCALAR).next_to(sis_f, DOWN, buff=0.25).match_y(l_c)
        distintos = MathTex(r"(9,\ 2,)", r"\neq", r"\begin{bmatrix}9\\ 2\end{bmatrix}", r"\neq", r"\begin{bmatrix}9 & 2\end{bmatrix}",
                            font_size=48).move_to([0, -2.3, 0])
        
        with self.voiceover(text=tr("""En el vídeo anterior vimos que un vector entre corchetes es una matriz con una sola columna: <bookmark mark='c'/> una matriz columna.""",
                                    """In the previous video we saw that a vector in square brackets is a matrix with a single column: <bookmark mark='c'/> a column matrix.""")) as tracker:
            self.play(Write(cabecera), FadeIn(grupos[0]), run_time=1)
            self.play(FadeIn(colm), run_time=1)
            self.wait_until_bookmark("c")
            self.play(FadeIn(r_c), run_time=0.6)
        
        with self.voiceover(text=tr("""Su transpuesta tiene una sola fila: <bookmark mark='f'/> es una matriz fila.""",
                                    """Its transpose has a single row: <bookmark mark='f'/> it is a row matrix.""")) as tracker:
            self.play(FadeIn(film[0]), run_time=0.8)
            self.play(TransformFromCopy(colm[2], film[2]), FadeIn(film[1]), run_time=1.2)
            self.wait_until_bookmark("f")
            self.play(FadeIn(r_f), run_time=0.6)
        
        with self.voiceover(text=tr("""Escritas como listas se ve la diferencia: <bookmark mark='c'/> la matriz columna es una lista con un solo vector de dos componentes, <bookmark mark='f'/> y la matriz fila, una lista con dos vectores de una componente.""",
                                    """Written as lists, the difference shows: <bookmark mark='c'/> the column matrix is a list with a single vector of two components, <bookmark mark='f'/> and the row matrix, a list with two vectors of one component.""")) as tracker:
            self.wait_until_bookmark("c")
            self.play(TransformFromCopy(colm[2], sis_c), FadeIn(l_c), run_time=0.8)
            self.wait_until_bookmark("f")
            self.play(TransformFromCopy(film[2], sis_f), FadeIn(l_f), run_time=0.8)
            self.wait(max(0.5, tracker.get_remaining_duration() - 0.8))
            self.play(FadeOut(VGroup(sis_c, l_c, sis_f, l_f)), run_time=0.8)
        
        with self.voiceover(text=tr("""Así, un vector, una matriz columna y una matriz fila son tres objetos distintos, aunque tengan los mismos números.""",
                                    """So a vector, a column matrix and a row matrix are three different objects, even if they have the same numbers.""")) as tracker:
            self.play(FadeIn(distintos), run_time=1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Transponer es cambiar de lado los índices", "Transposing swaps the sides of the indices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        cadena = [MathTex(r"\eleMT{A}{i}{j}", r"=", r"\elemLp{\VectTC{A}{j}}{i}", tex_template=myTemplate, font_size=48),
                  MathTex(r"\phantom{\eleMT{A}{i}{j}}", r"=", r"\elemLp{\VectF{A}{j}}{i}", tex_template=myTemplate, font_size=48),
                  MathTex(r"\phantom{\eleMT{A}{i}{j}}", r"=", r"\elemRp{\VectF{A}{j}}{i}", tex_template=myTemplate, font_size=48),
                  MathTex(r"\phantom{\eleMT{A}{i}{j}}", r"=", r"\eleM{A}{j}{i}", tex_template=myTemplate, font_size=48)]
        columna_de_lineas(cadena, x0=-2.6, y0=1.6, dy=1.15)
        x_rot = 1.4
        reglas = [rotulo(tr("da igual el orden", "the order does not matter"), cadena[0], x=x_rot),
                  rotulo(tr("definición de transpuesta", "definition of the transpose"), cadena[1], x=x_rot),
                  rotulo(tr("el selector, por cualquier lado de un vector", "the selector, on either side of a vector"), cadena[2], x=x_rot),
                  rotulo(tr("da igual el orden", "the order does not matter"), cadena[3], x=x_rot)]
        regla = MathTex(r"\eleMT{A}{i}{j}", r"=", r"\eleM{A}{j}{i}", tex_template=myTemplate, font_size=56).move_to([1.2, 1.6, 0])
        idea = aviso("idea").next_to(regla, LEFT, buff=0.8)
        doble = MathTex(r"\elemLRp{\TransP*{\MatT{A}}}{i}{j}", r"=", r"\eleMT{A}{j}{i}", r"=", r"\eleM{A}{i}{j}", tex_template=myTemplate, font_size=52).move_to([0, -0.3, 0])
        final = MathTex(r"\TransP*{\MatT{A}}=\Mat{A}", tex_template=myTemplate, font_size=56).move_to([0, -1.8, 0])
        
        with self.voiceover(text=tr("""Veamos el efecto de la transposición sobre una componente. Empezamos por una componente cualquiera de la transpuesta.""",
                                    """Let us see the effect of transposition on a component. We start with any component of the transpose.""")) as tracker:
            self.play(Write(cabecera), FadeIn(cadena[0][0]), run_time=1.2)
        
        pasos = [(tr("""Como da igual el orden, podemos seleccionar primero la columna.""",
                     """Since the order does not matter, we can select the column first."""), cadena[0]),
                 (tr("""Por la definición de transpuesta, podemos sustituir esa columna por la fila de A con el mismo índice.""",
                     """By the definition of the transpose, we can replace that column with the row of A with the same index."""), cadena[1]),
                 (tr("""Esa fila es un vector, así que podemos pasar el selector al otro lado.""",
                     """That row is a vector, so we can move the selector to the other side."""), cadena[2]),
                 (tr("""Y como da igual el orden, podemos quitar los paréntesis.""",
                     """And since the order does not matter, we can drop the parentheses."""), cadena[3])]
        for k, (texto, linea) in enumerate(pasos):
            with self.voiceover(text=texto) as tracker:
                self.play(FadeIn(reglas[k]), run_time=0.6)
                self.play(Write(linea[1:]), run_time=1.2)
        
        with self.voiceover(text=tr("""Hemos demostrado que transponer intercambia los índices: <bookmark mark='f'/> el de la fila pasa a ser el de la columna, <bookmark mark='c'/> y el de la columna, el de la fila.""",
                                    """We have proved that transposing swaps the indices: <bookmark mark='f'/> the row index becomes the column index, <bookmark mark='c'/> and the column index becomes the row index.""")) as tracker:
            # cada pieza por separado: Indicate sobre un grupo escala el grupo entero y separa las piezas
            self.play(Indicate(cadena[0][0], color=COLOR_ESCALAR, scale_factor=1.1), Indicate(cadena[3][2], color=COLOR_ESCALAR, scale_factor=1.1), run_time=1)
            self.wait_until_bookmark("f")   # glifos: i | ( A T ) | j  y  j | A | i
            self.play(Indicate(cadena[0][0][0], color=COLOR_ESCALAR, scale_factor=1.8), Indicate(cadena[3][2][4], color=COLOR_ESCALAR, scale_factor=1.8), run_time=0.9)
            self.wait_until_bookmark("c")
            self.play(Indicate(cadena[0][0][7], color=COLOR_ESCALAR, scale_factor=1.8), Indicate(cadena[3][2][0], color=COLOR_ESCALAR, scale_factor=1.8), run_time=0.9)
        
        self.play(FadeOut(VGroup(cadena[0][1:], *cadena[1:3], cadena[3][:2], *reglas)), ReplacementTransform(cadena[0][0], regla[0]),
                  ReplacementTransform(cadena[3][2], regla[2]), FadeIn(regla[1]), run_time=1.2)   # la primera y la última línea forman la regla
        with self.voiceover(text=tr("""De aquí sale una regla de reescritura: podemos transponer, o quitar la transposición, si a la vez cambiamos de lado los índices.""",
                                    """This gives us a rewriting rule: we can transpose, or remove the transposition, if at the same time we swap the sides of the indices.""")) as tracker:
            self.play(FadeIn(idea), run_time=0.8)
        
        self.pausa_para_pensar(invitacion=tr("Demuestre que la transpuesta de la transpuesta es la matriz original.",
                                             "Prove that the transpose of the transpose is the original matrix."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que la transpuesta de la transpuesta de A es A.",
                                                 "Pause the video and try to prove that the transpose of the transpose of A is A."))
        
        with self.voiceover(text=tr("""Empezamos por una componente cualquiera. <bookmark mark='a'/> Por la regla, podemos quitar la transposición exterior cambiando de lado los índices, <bookmark mark='b'/> y, por la misma regla, podemos quitar la otra, y los índices vuelven a su sitio.""",
                                    """We start with any component. <bookmark mark='a'/> By the rule, we can remove the outer transposition by swapping the sides of the indices, <bookmark mark='b'/> and, by the same rule, we can remove the other one, and the indices go back to their places.""")) as tracker:
            self.play(FadeIn(doble[0]), run_time=1)
            self.wait_until_bookmark("a")
            self.play(Write(doble[1:3]), run_time=1)
            self.wait_until_bookmark("b")
            self.play(Write(doble[3:]), run_time=1)
        
        with self.voiceover(text=tr("""Las dos matrices tienen el mismo orden y las mismas componentes, así que son iguales.""",
                                    """Both matrices have the same order and the same components, so they are equal.""")) as tracker:
            self.play(Write(final), run_time=1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [r"\eleVL{a}{i}=\eleVR{a}{i}", r"\elemRp{\VectF{A}{i}}{j}=\elemLp{\VectC{A}{j}}{i}=\eleM{A}{i}{j}",
                    r"\VectTC{A}{i}=\VectF{A}{i}", r"\eleMT{A}{i}{j}=\eleM{A}{j}{i},\qquad \TransP*{\MatT{A}}=\Mat{A}"]
        rotulos = [tr("el selector, por cualquier lado de un vector", "the selector, on either side of a vector"),
                   tr("da igual el orden", "the order does not matter"),
                   tr("las columnas de la transpuesta son las filas", "the columns of the transpose are the rows"),
                   tr("transponer = cambiar de lado los índices", "transposing = swapping the sides of the indices")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=44), Tex(r, font_size=28, color=GRAY_B)).arrange(DOWN, buff=0.2)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.4).move_to([0, -0.5, 0])
        
        with self.voiceover(text=tr("""Resumamos. El operador selector puede actuar por cualquier lado de un vector, con el mismo resultado. <bookmark mark='o'/> Por eso, para seleccionar una componente de una matriz, da igual empezar por la fila o por la columna.""",
                                    """Let us sum up. The selector operator can act on either side of a vector, with the same result. <bookmark mark='o'/> That is why, to select a component of a matrix, it makes no difference whether we start with the row or with the column.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("o")
            self.play(FadeIn(filas[1]), run_time=0.8)
        
        with self.voiceover(text=tr("""Las columnas de la transpuesta de una matriz son las filas de la matriz. <bookmark mark='r'/> Transponer equivale a cambiar de lado los índices, y la transpuesta de la transpuesta es la matriz original.""",
                                    """The columns of the transpose of a matrix are the rows of the matrix. <bookmark mark='r'/> Transposing amounts to swapping the sides of the indices, and the transpose of the transpose is the original matrix.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.8)
            self.wait_until_bookmark("r")
            self.play(FadeIn(filas[3]), run_time=0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos algunas matrices especiales y las operaciones con matrices: la suma y el producto por un escalar.""",
                                    """In the next video we will meet some special matrices and the operations with matrices: addition and multiplication by a scalar.""")) as tracker:
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


class L01_V10_E01_Enlace(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        A = matriz(A_SEL)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([0, 1.0, 0])
        comp = MathTex(r"\eleM{A}{2}{1}", r"=", r"7", tex_template=myTemplate, font_size=52).move_to([0, -1.4, 0])
        
        with self.voiceover(text=tr("""En el vídeo anterior vimos que el operador selector, actuando por ambos lados de una matriz, selecciona una componente.""",
                                    """In the previous video we saw that the selector operator, acting on both sides of a matrix, selects a component.""")) as tracker:
            self.play(Write(titulo), FadeIn(f_A), run_time=1.2)
            self.play(Write(comp), run_time=1.2)
        
        with self.voiceover(text=tr("""Esa componente está a la vez en una fila y en una columna: <bookmark mark='f'/> en la segunda fila <bookmark mark='c'/> y en la primera columna.""",
                                    """That component lies both in a row and in a column: <bookmark mark='f'/> in the second row <bookmark mark='c'/> and in the first column.""")) as tracker:
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 1)
            self.play(FadeIn(ff), run_time=0.5)
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0, color=COLOR_C)
            self.play(FadeIn(fc), run_time=0.5)
            self.play(Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
        
        with self.voiceover(text=tr("""Así que también debería poder obtenerse seleccionando primero la fila, o primero la columna.""",
                                    """So we should also be able to get it by selecting the row first, or the column first.""")) as tracker:
            self.play(Indicate(ff, color=COLOR_ESCALAR, scale_factor=1.05), run_time=1)
            self.play(Indicate(fc, color=COLOR_C, scale_factor=1.05), run_time=1)
        
        self.pausa_media()


class L01_V10_E02_SelectorIzquierda(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Primero la fila o primero la columna", "Row first or column first"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A = matriz(A_SEL)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([0, 2.0, 0])
        por_fila = MathTex(r"\elemRp{\VectF{A}{2}}{1}", r"=", r"\elemR{(7,\ 0,\ 3,)}{1}", r"=", r"7", tex_template=myTemplate, font_size=48)
        por_col = MathTex(r"\elemLp{\VectC{A}{1}}{2}", r"=", r"\elemL{\begin{pmatrix}1\\ 7\end{pmatrix}}{2}", r"=", r"7", tex_template=myTemplate, font_size=48)
        lineas = columna_de_lineas([por_fila, por_col], x0=-1.6, y0=0.3, dy=1.45)
        convenio = MathTex(r"\eleVL{a}{i}", r"=", r"\eleVR{a}{i}", r"=", r"a_i", tex_template=myTemplate, font_size=52).move_to([0.8, -2.7, 0])
        idea = aviso("idea").next_to(convenio, LEFT, buff=0.8)
        conclusion = MathTex(r"\elemRp{\VectF{A}{2}}{1}", r"=", r"\elemLp{\VectC{A}{1}}{2}", r"=", r"\eleM{A}{2}{1}",
                             tex_template=myTemplate, font_size=52).move_to([0, 0.2, 0])
        
        with self.voiceover(text=tr("""Seleccionemos primero la segunda fila, <bookmark mark='f'/> que es un vector. <bookmark mark='c'/> Su primera componente es el siete.""",
                                    """Let us first select the second row, <bookmark mark='f'/> which is a vector. <bookmark mark='c'/> Its first component is the seven.""")) as tracker:
            self.play(Write(cabecera), FadeIn(f_A), FadeIn(por_fila[0]), run_time=1)
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 1)
            self.play(FadeIn(ff), FadeIn(por_fila[1:3]), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(FadeIn(por_fila[3:]), Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
        
        with self.voiceover(text=tr("""Ahora seleccionemos primero la primera columna, <bookmark mark='c'/> que también es un vector. <bookmark mark='s'/> El siete es su segunda componente.""",
                                    """Now let us first select the first column, <bookmark mark='c'/> which is also a vector. <bookmark mark='s'/> The seven is its second component.""")) as tracker:
            self.play(FadeOut(ff), FadeIn(por_col[0]), run_time=0.8)
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0, color=COLOR_C)
            self.play(FadeIn(fc), FadeIn(por_col[1:3]), run_time=0.8)
            self.wait_until_bookmark("s")
            self.play(FadeIn(por_col[3:]), Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
        
        with self.voiceover(text=tr("""Pero aquí el selector actúa por la izquierda de un vector. <bookmark mark='a'/> Para que esto tenga sentido, aceptaremos que el selector pueda actuar por cualquier lado de un vector, <bookmark mark='d'/> con el mismo resultado.""",
                                    """But here the selector acts on the left of a vector. <bookmark mark='a'/> For this to make sense, we will allow the selector to act on either side of a vector, <bookmark mark='d'/> with the same result.""")) as tracker:
            self.play(FadeOut(fc), Indicate(por_col[2], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1)
            self.wait_until_bookmark("a")
            self.play(FadeIn(idea), FadeIn(convenio[0]), run_time=0.8)
            self.wait_until_bookmark("d")
            self.play(FadeIn(convenio[1:]), run_time=0.8)
        
        with self.voiceover(text=tr("""Con este convenio, da igual seleccionar primero la fila o la columna: <bookmark mark='q'/> por eso podemos quitar los paréntesis y escribir el selector a ambos lados de la matriz.""",
                                    """With this convention, it makes no difference whether we select the row or the column first: <bookmark mark='q'/> that is why we can drop the parentheses and write the selector on both sides of the matrix.""")) as tracker:
            self.play(ReplacementTransform(por_fila[0], conclusion[0]), ReplacementTransform(por_col[0], conclusion[2]), FadeIn(conclusion[1]),
                      FadeOut(VGroup(por_fila[1:], por_col[1:])), run_time=1.2)
            self.wait_until_bookmark("q")
            self.play(FadeIn(conclusion[3:]), run_time=1)
        
        with self.voiceover(text=tr("""Lo hemos visto en un ejemplo, pero vale para cualquier componente de cualquier matriz, porque toda componente está a la vez en su fila y en su columna.""",
                                    """We have seen it in an example, but it holds for any component of any matrix, because every component lies both in its row and in its column.""")) as tracker:
            self.play(Indicate(conclusion[4], color=COLOR_ESCALAR, scale_factor=1.1), run_time=1)
        
        self.pausa_media()


class L01_V10_E03_Transposicion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La transposición", "Transposition"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A = matriz(A_EJ)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([-3.3, 1.2, 0])
        T = matriz([list(f) for f in zip(*A_EJ)])
        f_T = con_nombre(r"\Mat{B}=", T).move_to([3.0, 1.2, 0])
        nombre_T = MathTex(r"\MatT{A}=", tex_template=myTemplate, font_size=48).move_to(f_T[0], aligned_edge=RIGHT)
        defin = MathTex(r"\VectTC{A}{i}", r"=", r"\VectF{A}{i}", tex_template=myTemplate, font_size=52).move_to([0, -1.5, 0])
        r_col = Tex(tr(r"columna $i$ de $\MatT{A}$", r"column $i$ of $\MatT{A}$"), tex_template=myTemplate, font_size=28, color=GRAY_B).next_to(defin[0], DOWN, buff=0.3)
        r_fil = Tex(tr(r"fila $i$ de $\Mat{A}$", r"row $i$ of $\Mat{A}$"), tex_template=myTemplate, font_size=28, color=GRAY_B).next_to(defin[2], DOWN, buff=0.3)
        orden = MathTex(r"\Mat{A}\in\R[m\times n]", r"\quad\Rightarrow\quad", r"\MatT{A}\in\R[n\times m]", tex_template=myTemplate, font_size=48).move_to([0, -3.0, 0])
        
        with self.voiceover(text=tr("""En el vídeo anterior formamos la matriz B con dos vectores: <bookmark mark='x'/> el primero llevaba los números de la primera fila de A, <bookmark mark='y'/> y el segundo, los de la segunda.""",
                                    """In the previous video we built the matrix B with two vectors: <bookmark mark='x'/> the first one carried the numbers of the first row of A, <bookmark mark='y'/> and the second one, those of the second row.""")) as tracker:
            self.play(Write(cabecera), FadeIn(f_A), FadeIn(f_T[0]), FadeIn(T.get_brackets()), run_time=1)
            for i, marca in enumerate(["x", "y"]):
                self.wait_until_bookmark(marca)
                fr = franja_fila(A, i)
                self.play(FadeIn(fr), run_time=0.4)
                self.play(TransformFromCopy(A.get_rows()[i], T.get_columns()[i]), run_time=1.2)
                self.play(FadeOut(fr), run_time=0.3)
        
        with self.voiceover(text=tr("""Convertir las filas de una matriz en columnas se llama transposición. <bookmark mark='t'/> La matriz B es la transpuesta de A, que se escribe con una T en el superíndice.""",
                                    """Turning the rows of a matrix into columns is called transposition. <bookmark mark='t'/> The matrix B is the transpose of A, which is written with a T as a superscript.""")) as tracker:
            self.wait_until_bookmark("t")
            self.play(FadeTransform(f_T[0], nombre_T), run_time=1.2)
        
        with self.voiceover(text=tr("""Es decir, cada columna de la transpuesta es la fila de A con el mismo índice: <bookmark mark='c1'/> la primera columna de A transpuesta es la primera fila de A, <bookmark mark='c2'/> y la segunda, la segunda.""",
                                    """That is, each column of the transpose is the row of A with the same index: <bookmark mark='c1'/> the first column of A transpose is the first row of A, <bookmark mark='c2'/> and the second, the second.""")) as tracker:
            self.play(Write(defin), FadeIn(r_col), FadeIn(r_fil), run_time=1.2)
            franjas = None
            for i, marca in enumerate(["c1", "c2"]):
                self.wait_until_bookmark(marca)
                nuevas = VGroup(franja_columna(T, i), franja_fila(A, i))
                self.play(FadeIn(nuevas) if franjas is None else ReplacementTransform(franjas, nuevas), run_time=0.6)
                franjas = nuevas
        
        with self.voiceover(text=tr("""Por eso, si A es de orden m por n, su transpuesta es de orden n por m.""",
                                    """That is why, if A is of order m by n, its transpose is of order n by m.""")) as tracker:
            self.play(FadeOut(franjas), FadeIn(orden), run_time=1)
        
        self.pausa_media()


class L01_V10_E04_MatrizFila(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Vector, matriz columna y matriz fila", "Vector, column matrix and row matrix"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        v = MathTex(r"\Vect{a}=(9,\ 2,)", tex_template=myTemplate, font_size=48)
        colm = MathTex(r"\begin{bmatrix}\Vect{a}\end{bmatrix}", r"=", r"\begin{bmatrix}9\\ 2\end{bmatrix}", tex_template=myTemplate, font_size=48)
        film = MathTex(r"{\begin{bmatrix}\Vect{a}\end{bmatrix}}^{\T}", r"=", r"\begin{bmatrix}9 & 2\end{bmatrix}", tex_template=myTemplate, font_size=48)
        r_v = Tex(tr("vector", "vector"), font_size=30, color=GRAY_B)
        r_c = Tex(tr(r"matriz columna, $2\times 1$", r"column matrix, $2\times 1$"), font_size=30, color=GRAY_B)
        r_f = Tex(tr(r"matriz fila, $1\times 2$", r"row matrix, $1\times 2$"), font_size=30, color=GRAY_B)
        grupos = VGroup(*[VGroup(f, r).arrange(DOWN, buff=0.4) for f, r in [(v, r_v), (colm, r_c), (film, r_f)]])
        grupos.arrange(RIGHT, buff=1.2, aligned_edge=DOWN).move_to([0, 0.6, 0])
        sis_c = MathTex(r"\begin{bmatrix}\begin{pmatrix}9\\ 2\end{pmatrix};\end{bmatrix}", tex_template=myTemplate, font_size=44).next_to(r_c, DOWN, buff=0.35)
        sis_f = MathTex(r"\left[(9,);\ (2,);\right]", tex_template=myTemplate, font_size=44).next_to(r_f, DOWN, buff=0.35).match_y(sis_c)
        l_c = Tex(tr(r"un vector de $\R[2]$", r"one vector of $\R[2]$"), tex_template=myTemplate, font_size=30, color=COLOR_ESCALAR).next_to(sis_c, DOWN, buff=0.25)
        l_f = Tex(tr(r"dos vectores de $\R[1]$", r"two vectors of $\R[1]$"), tex_template=myTemplate, font_size=30, color=COLOR_ESCALAR).next_to(sis_f, DOWN, buff=0.25).match_y(l_c)
        distintos = MathTex(r"(9,\ 2,)", r"\neq", r"\begin{bmatrix}9\\ 2\end{bmatrix}", r"\neq", r"\begin{bmatrix}9 & 2\end{bmatrix}",
                            font_size=48).move_to([0, -2.3, 0])
        
        with self.voiceover(text=tr("""En el vídeo anterior vimos que un vector entre corchetes es una matriz con una sola columna: <bookmark mark='c'/> una matriz columna.""",
                                    """In the previous video we saw that a vector in square brackets is a matrix with a single column: <bookmark mark='c'/> a column matrix.""")) as tracker:
            self.play(Write(cabecera), FadeIn(grupos[0]), run_time=1)
            self.play(FadeIn(colm), run_time=1)
            self.wait_until_bookmark("c")
            self.play(FadeIn(r_c), run_time=0.6)
        
        with self.voiceover(text=tr("""Su transpuesta tiene una sola fila: <bookmark mark='f'/> es una matriz fila.""",
                                    """Its transpose has a single row: <bookmark mark='f'/> it is a row matrix.""")) as tracker:
            self.play(FadeIn(film[0]), run_time=0.8)
            self.play(TransformFromCopy(colm[2], film[2]), FadeIn(film[1]), run_time=1.2)
            self.wait_until_bookmark("f")
            self.play(FadeIn(r_f), run_time=0.6)
        
        with self.voiceover(text=tr("""Escritas como listas se ve la diferencia: <bookmark mark='c'/> la matriz columna es una lista con un solo vector de dos componentes, <bookmark mark='f'/> y la matriz fila, una lista con dos vectores de una componente.""",
                                    """Written as lists, the difference shows: <bookmark mark='c'/> the column matrix is a list with a single vector of two components, <bookmark mark='f'/> and the row matrix, a list with two vectors of one component.""")) as tracker:
            self.wait_until_bookmark("c")
            self.play(TransformFromCopy(colm[2], sis_c), FadeIn(l_c), run_time=0.8)
            self.wait_until_bookmark("f")
            self.play(TransformFromCopy(film[2], sis_f), FadeIn(l_f), run_time=0.8)
            self.wait(max(0.5, tracker.get_remaining_duration() - 0.8))
            self.play(FadeOut(VGroup(sis_c, l_c, sis_f, l_f)), run_time=0.8)
        
        with self.voiceover(text=tr("""Así, un vector, una matriz columna y una matriz fila son tres objetos distintos, aunque tengan los mismos números.""",
                                    """So a vector, a column matrix and a row matrix are three different objects, even if they have the same numbers.""")) as tracker:
            self.play(FadeIn(distintos), run_time=1.2)
        
        self.pausa_media()


class L01_V10_E05_Propiedades(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Transponer es cambiar de lado los índices", "Transposing swaps the sides of the indices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        cadena = [MathTex(r"\eleMT{A}{i}{j}", r"=", r"\elemLp{\VectTC{A}{j}}{i}", tex_template=myTemplate, font_size=48),
                  MathTex(r"\phantom{\eleMT{A}{i}{j}}", r"=", r"\elemLp{\VectF{A}{j}}{i}", tex_template=myTemplate, font_size=48),
                  MathTex(r"\phantom{\eleMT{A}{i}{j}}", r"=", r"\elemRp{\VectF{A}{j}}{i}", tex_template=myTemplate, font_size=48),
                  MathTex(r"\phantom{\eleMT{A}{i}{j}}", r"=", r"\eleM{A}{j}{i}", tex_template=myTemplate, font_size=48)]
        columna_de_lineas(cadena, x0=-2.6, y0=1.6, dy=1.15)
        x_rot = 1.4
        reglas = [rotulo(tr("da igual el orden", "the order does not matter"), cadena[0], x=x_rot),
                  rotulo(tr("definición de transpuesta", "definition of the transpose"), cadena[1], x=x_rot),
                  rotulo(tr("el selector, por cualquier lado de un vector", "the selector, on either side of a vector"), cadena[2], x=x_rot),
                  rotulo(tr("da igual el orden", "the order does not matter"), cadena[3], x=x_rot)]
        regla = MathTex(r"\eleMT{A}{i}{j}", r"=", r"\eleM{A}{j}{i}", tex_template=myTemplate, font_size=56).move_to([1.2, 1.6, 0])
        idea = aviso("idea").next_to(regla, LEFT, buff=0.8)
        doble = MathTex(r"\elemLRp{\TransP*{\MatT{A}}}{i}{j}", r"=", r"\eleMT{A}{j}{i}", r"=", r"\eleM{A}{i}{j}", tex_template=myTemplate, font_size=52).move_to([0, -0.3, 0])
        final = MathTex(r"\TransP*{\MatT{A}}=\Mat{A}", tex_template=myTemplate, font_size=56).move_to([0, -1.8, 0])
        
        with self.voiceover(text=tr("""Veamos el efecto de la transposición sobre una componente. Empezamos por una componente cualquiera de la transpuesta.""",
                                    """Let us see the effect of transposition on a component. We start with any component of the transpose.""")) as tracker:
            self.play(Write(cabecera), FadeIn(cadena[0][0]), run_time=1.2)
        
        pasos = [(tr("""Como da igual el orden, podemos seleccionar primero la columna.""",
                     """Since the order does not matter, we can select the column first."""), cadena[0]),
                 (tr("""Por la definición de transpuesta, podemos sustituir esa columna por la fila de A con el mismo índice.""",
                     """By the definition of the transpose, we can replace that column with the row of A with the same index."""), cadena[1]),
                 (tr("""Esa fila es un vector, así que podemos pasar el selector al otro lado.""",
                     """That row is a vector, so we can move the selector to the other side."""), cadena[2]),
                 (tr("""Y como da igual el orden, podemos quitar los paréntesis.""",
                     """And since the order does not matter, we can drop the parentheses."""), cadena[3])]
        for k, (texto, linea) in enumerate(pasos):
            with self.voiceover(text=texto) as tracker:
                self.play(FadeIn(reglas[k]), run_time=0.6)
                self.play(Write(linea[1:]), run_time=1.2)
        
        with self.voiceover(text=tr("""Hemos demostrado que transponer intercambia los índices: <bookmark mark='f'/> el de la fila pasa a ser el de la columna, <bookmark mark='c'/> y el de la columna, el de la fila.""",
                                    """We have proved that transposing swaps the indices: <bookmark mark='f'/> the row index becomes the column index, <bookmark mark='c'/> and the column index becomes the row index.""")) as tracker:
            # cada pieza por separado: Indicate sobre un grupo escala el grupo entero y separa las piezas
            self.play(Indicate(cadena[0][0], color=COLOR_ESCALAR, scale_factor=1.1), Indicate(cadena[3][2], color=COLOR_ESCALAR, scale_factor=1.1), run_time=1)
            self.wait_until_bookmark("f")   # glifos: i | ( A T ) | j  y  j | A | i
            self.play(Indicate(cadena[0][0][0], color=COLOR_ESCALAR, scale_factor=1.8), Indicate(cadena[3][2][4], color=COLOR_ESCALAR, scale_factor=1.8), run_time=0.9)
            self.wait_until_bookmark("c")
            self.play(Indicate(cadena[0][0][7], color=COLOR_ESCALAR, scale_factor=1.8), Indicate(cadena[3][2][0], color=COLOR_ESCALAR, scale_factor=1.8), run_time=0.9)
        
        self.play(FadeOut(VGroup(cadena[0][1:], *cadena[1:3], cadena[3][:2], *reglas)), ReplacementTransform(cadena[0][0], regla[0]),
                  ReplacementTransform(cadena[3][2], regla[2]), FadeIn(regla[1]), run_time=1.2)   # la primera y la última línea forman la regla
        with self.voiceover(text=tr("""De aquí sale una regla de reescritura: podemos transponer, o quitar la transposición, si a la vez cambiamos de lado los índices.""",
                                    """This gives us a rewriting rule: we can transpose, or remove the transposition, if at the same time we swap the sides of the indices.""")) as tracker:
            self.play(FadeIn(idea), run_time=0.8)
        
        self.pausa_para_pensar(invitacion=tr("Demuestre que la transpuesta de la transpuesta es la matriz original.",
                                             "Prove that the transpose of the transpose is the original matrix."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que la transpuesta de la transpuesta de A es A.",
                                                 "Pause the video and try to prove that the transpose of the transpose of A is A."))
        
        with self.voiceover(text=tr("""Empezamos por una componente cualquiera. <bookmark mark='a'/> Por la regla, podemos quitar la transposición exterior cambiando de lado los índices, <bookmark mark='b'/> y, por la misma regla, podemos quitar la otra, y los índices vuelven a su sitio.""",
                                    """We start with any component. <bookmark mark='a'/> By the rule, we can remove the outer transposition by swapping the sides of the indices, <bookmark mark='b'/> and, by the same rule, we can remove the other one, and the indices go back to their places.""")) as tracker:
            self.play(FadeIn(doble[0]), run_time=1)
            self.wait_until_bookmark("a")
            self.play(Write(doble[1:3]), run_time=1)
            self.wait_until_bookmark("b")
            self.play(Write(doble[3:]), run_time=1)
        
        with self.voiceover(text=tr("""Las dos matrices tienen el mismo orden y las mismas componentes, así que son iguales.""",
                                    """Both matrices have the same order and the same components, so they are equal.""")) as tracker:
            self.play(Write(final), run_time=1.2)
        
        self.pausa_media()


class L01_V10_E06_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [r"\eleVL{a}{i}=\eleVR{a}{i}", r"\elemRp{\VectF{A}{i}}{j}=\elemLp{\VectC{A}{j}}{i}=\eleM{A}{i}{j}",
                    r"\VectTC{A}{i}=\VectF{A}{i}", r"\eleMT{A}{i}{j}=\eleM{A}{j}{i},\qquad \TransP*{\MatT{A}}=\Mat{A}"]
        rotulos = [tr("el selector, por cualquier lado de un vector", "the selector, on either side of a vector"),
                   tr("da igual el orden", "the order does not matter"),
                   tr("las columnas de la transpuesta son las filas", "the columns of the transpose are the rows"),
                   tr("transponer = cambiar de lado los índices", "transposing = swapping the sides of the indices")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=44), Tex(r, font_size=28, color=GRAY_B)).arrange(DOWN, buff=0.2)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.4).move_to([0, -0.5, 0])
        
        with self.voiceover(text=tr("""Resumamos. El operador selector puede actuar por cualquier lado de un vector, con el mismo resultado. <bookmark mark='o'/> Por eso, para seleccionar una componente de una matriz, da igual empezar por la fila o por la columna.""",
                                    """Let us sum up. The selector operator can act on either side of a vector, with the same result. <bookmark mark='o'/> That is why, to select a component of a matrix, it makes no difference whether we start with the row or with the column.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("o")
            self.play(FadeIn(filas[1]), run_time=0.8)
        
        with self.voiceover(text=tr("""Las columnas de la transpuesta de una matriz son las filas de la matriz. <bookmark mark='r'/> Transponer equivale a cambiar de lado los índices, y la transpuesta de la transpuesta es la matriz original.""",
                                    """The columns of the transpose of a matrix are the rows of the matrix. <bookmark mark='r'/> Transposing amounts to swapping the sides of the indices, and the transpose of the transpose is the original matrix.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.8)
            self.wait_until_bookmark("r")
            self.play(FadeIn(filas[3]), run_time=0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos algunas matrices especiales y las operaciones con matrices: la suma y el producto por un escalar.""",
                                    """In the next video we will meet some special matrices and the operations with matrices: addition and multiplication by a scalar.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
