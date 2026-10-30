from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Matrices: filas y columnas", "Matrices: rows and columns")

PAISES = [tr("España", "Spain"), tr("Francia", "France"), tr("Alemania", "Germany"),
          tr("Reino Unido", "United Kingdom"), tr("EE. UU.", "USA")]
PIB = {2003: [2.9, 0.9, -0.2, 2.5, 1.8], 2004: [3.1, 2.0, 1.1, 3.2, 3.1],
       2005: [3.3, 1.6, 0.7, 1.9, 3.7], 2006: [3.3, 2.0, 0.9, 1.5, 3.5]}   # Sección 1.3 del libro (fuente: ICAE)
ANYOS = list(PIB)
FILAS_PIB = [[PIB[a][k] for a in ANYOS] for k in range(len(PAISES))]

A_EJ = [[4, -1, 0], [2, 2, 7]]      # transparencia "Matrices": a=(4,2,), b=(-1,2,), c=(0,7,)
A_SEL = [[1, 2, 1], [7, 0, 3]]      # transparencia "Más notación"
COLOR_FILA, COLOR_COLUMNA = COLOR_A, COLOR_B   # índice de la fila y de la columna (letras del superíndice)


def vector(valores, color=WHITE, decimales=1, escala=0.8):
    conf = {"num_decimal_places": decimales, "group_with_commas": False}
    if decimales:
        v = DecimalMatrix([[x] for x in valores], left_bracket="(", right_bracket=")", v_buff=0.62, element_to_mobject_config=conf)
    else:
        v = IntegerMatrix([[x] for x in valores], left_bracket="(", right_bracket=")", v_buff=0.62)
    v.get_entries().set_color(color)
    return v.scale(escala)


def matriz(filas, color=WHITE, decimales=1, escala=0.8, h_buff=1.3):
    conf = {"num_decimal_places": decimales, "group_with_commas": False}
    if decimales:
        m = DecimalMatrix(filas, v_buff=0.62, h_buff=h_buff, element_to_mobject_config=conf)
    else:
        m = IntegerMatrix(filas, v_buff=0.62, h_buff=h_buff)
    m.get_entries().set_color(color)
    return m.scale(escala)


def con_nombre(tex, mob, font_size=48):
    return VGroup(MathTex(tex, tex_template=myTemplate, font_size=font_size), mob).arrange(RIGHT, buff=0.2)


def leyenda(rotulos, entradas, x_der, font_size=30):
    """Rótulos alineados a la derecha de x_der, cada uno a la altura de su entrada."""
    filas = VGroup(*[Tex(r, font_size=font_size) for r in rotulos])
    for f, e in zip(filas, entradas):
        f.move_to([x_der - f.width/2, e.get_y(), 0])
    return filas


def tabla_pib(centro=ORIGIN, font_size=30):
    """La matriz del PIB: [0] la matriz, [1] los países, [2] los años (encima de cada columna)."""
    M = matriz(FILAS_PIB).move_to(centro)
    paises = leyenda(PAISES, M.get_columns()[0], M.get_left()[0] - 0.3, font_size=font_size)
    anyos = VGroup(*[Tex(str(a), font_size=font_size, color=GRAY_B).next_to(col, UP, buff=0.35).set_y(M.get_top()[1] + 0.3)
                     for a, col in zip(ANYOS, M.get_columns())])
    return VGroup(M, paises, anyos)


def franja_fila(m, i, x0=None, x1=None, color=COLOR_ESCALAR):
    """Franja sobre la fila i (desde 0) de la matriz m, de x0 a x1 (por defecto, la matriz entera)."""
    x0 = m.get_left()[0] if x0 is None else x0
    x1 = m.get_right()[0] if x1 is None else x1
    y = m.get_rows()[i].get_y()
    return Rectangle(width=x1 - x0, height=0.45, stroke_width=0, fill_color=color,
                     fill_opacity=0.22).move_to([(x0 + x1)/2, y, 0])


def franja_columna(m, j, color=COLOR_ESCALAR):
    """Franja sobre la columna j (desde 0) de la matriz m."""
    col = m.get_columns()[j]
    return Rectangle(width=col.width + 0.35, height=m.get_brackets()[0].height, stroke_width=0, fill_color=color,
                     fill_opacity=0.22).move_to([col.get_x(), m.get_y(), 0])

class L01_V09_MatricesFilasYColumnas(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        tabla = tabla_pib([0.8, -0.6, 0], font_size=32)
        M = tabla[0]
        defin = Tex(tr(r"Una \emph{matriz} de ", r"A \emph{matrix} in "), r"$\R[m\times n]$",
                    tr(r" es una lista ordenada\\ de ", r" is an ordered list\\ of "), r"$n$",
                    tr(r" vectores de ", r" vectors in "), r"$\R[m]$", tr(r": sus \emph{columnas}.", r": its \emph{columns}."),
                    tex_template=myTemplate, font_size=48).move_to([0, 0.6, 0])
        m_s = VGroup(defin[1][1], defin[5][1])    # la m del superíndice y la de R^m
        n_s = VGroup(defin[1][3], defin[3][0])    # la n del superíndice y la de "n vectores"
        
        with self.voiceover(text=tr("""En el vídeo anterior pusimos uno al lado del otro los cuatro vectores con el crecimiento del PIB de cinco países, y obtuvimos esta tabla de números.""",
                                    """In the previous video we placed side by side the four vectors with the GDP growth of five countries, and we got this table of numbers.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
            self.play(FadeIn(tabla), run_time=1.5)
        
        with self.voiceover(text=tr("""Cada columna de la tabla es uno de esos vectores. <bookmark mark='m'/> Una lista ordenada de vectores como esta se llama matriz.""",
                                    """Each column of the table is one of those vectors. <bookmark mark='m'/> An ordered list of vectors like this one is called a matrix.""")) as tracker:
            franja = None
            for j in range(4):
                nueva = franja_columna(M, j)
                self.play(FadeIn(nueva) if franja is None else ReplacementTransform(franja, nueva), run_time=0.5)
                franja = nueva
            self.play(FadeOut(franja), run_time=0.4)
            self.wait_until_bookmark("m")
            self.play(FadeOut(tabla[1]), FadeOut(tabla[2]), M.animate.move_to([0, -0.6, 0]), run_time=1)   # solo la matriz, en el centro
        
        self.wait(0.5)   # una pausa antes de la definición general (Marcos, 2026-10-26)
        with self.voiceover(text=tr("""En general, una matriz es una lista ordenada de vectores, todos con el mismo número de componentes, que constituyen sus columnas.""",
                                    """In general, a matrix is an ordered list of vectors, all with the same number of components, which make up its columns.""")) as tracker:
            self.play(FadeOut(M), run_time=0.8)
            self.play(FadeIn(defin), run_time=1)
        
        with self.voiceover(text=tr("""En el superíndice, la primera letra indica cuántas componentes tiene cada vector, <bookmark mark='n'/> y la segunda, cuántos vectores hay en la lista.""",
                                    """In the superscript, the first letter tells how many components each vector has, <bookmark mark='n'/> and the second, how many vectors there are in the list.""")) as tracker:
            self.play(Indicate(m_s, color=COLOR_FILA, scale_factor=1.5), run_time=1)
            self.play(m_s.animate.set_color(COLOR_FILA), run_time=0.3)   # Indicate devuelve el color original
            self.wait_until_bookmark("n")
            self.play(Indicate(n_s, color=COLOR_COLUMNA, scale_factor=1.5), run_time=1)
            self.play(n_s.animate.set_color(COLOR_COLUMNA), run_time=0.3)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Ejemplos", "Examples"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        cols = list(zip(*A_EJ))   # las columnas de A: a, b y c
        COLORES = [COLOR_A, COLOR_B, COLOR_C]   # un color por vector, para seguirlos cuando cambian de sitio
        vs = [vector(c, color=k, decimales=0) for c, k in zip(cols, COLORES)]
        vecs = VGroup(*[con_nombre(rf"\Vect{{{l}}}=", v) for l, v in zip("abc", vs)]).arrange(RIGHT, buff=1.0).move_to([0, 1.9, 0])
        for v, k in zip(vecs, COLORES):
            v[0][0][0].set_color(k)   # la letra del vector
        A = matriz(A_EJ, decimales=0, h_buff=1.0)
        f_A = con_nombre(r"\Mat{A}=\begin{bmatrix}\Vect{a}; & \Vect{b}; & \Vect{c};\end{bmatrix}=", A).move_to([0, -0.1, 0])
        ORDEN = (1, 2, 0)   # la nueva lista [b; c; a]: todos los vectores cambian de sitio
        POS = {j: p for p, j in enumerate(ORDEN)}   # posición de cada vector en la nueva lista
        C = matriz([[r[j] for j in ORDEN] for r in A_EJ], decimales=0, h_buff=1.0)
        f_C = VGroup(MathTex(r"\begin{bmatrix}\Vect{b}; & \Vect{c}; & \Vect{a};\end{bmatrix}=", tex_template=myTemplate, font_size=48), C,
                     MathTex(r"\neq\Mat{A}", tex_template=myTemplate, font_size=48)).arrange(RIGHT, buff=0.2).move_to([0, -2.4, 0])
        f_C.shift((f_A[1].get_x() - C.get_x())*RIGHT)   # las dos matrices numéricas, una encima de la otra
        # glifos: f_A[0] = A = [ a ; b ; c ; ] =  (letras 3, 5, 7);  f_C[0] = [ b ; c ; a ; ] =  (letras 1, 3, 5)
        letras_A = [f_A[0][0][3], f_A[0][0][5], f_A[0][0][7]]
        letras_C = [f_C[0][0][1 + 2*POS[j]] for j in range(3)]   # dónde acaba cada vector (a, b, c)
        for k, la, lc in zip(COLORES, letras_A, letras_C):
            la.set_color(k); lc.set_color(k)
        for j, k in enumerate(COLORES):
            A.get_columns()[j].set_color(k)
            C.get_columns()[POS[j]].set_color(k)
        resto_C = VGroup(*[g for g in f_C[0][0] if all(g is not l for l in letras_C)], C.get_brackets(), f_C[2])
        
        with self.voiceover(text=tr("""Veamos un ejemplo con tres vectores de dos componentes.""",
                                    """Let us look at an example with three vectors of two components.""")) as tracker:
            self.play(Write(cabecera), LaggedStart(*[FadeIn(v) for v in vecs], lag_ratio=0.4), run_time=1.5)
        
        with self.voiceover(text=tr("""Con ellos formamos la matriz A, <bookmark mark='l'/> que es la lista de los tres vectores entre corchetes. <bookmark mark='c'/> Cada vector es una columna, y las columnas se escriben una al lado de la otra.""",
                                    """With them we build the matrix A, <bookmark mark='l'/> which is the list of the three vectors in square brackets. <bookmark mark='c'/> Each vector is a column, and the columns are written side by side.""")) as tracker:
            self.wait_until_bookmark("l")
            self.play(Write(f_A[0]), run_time=1.2)
            self.wait_until_bookmark("c")
            self.play(FadeIn(A.get_brackets()), run_time=0.4)
            self.play(LaggedStart(*[TransformFromCopy(v.get_entries(), col) for v, col in zip(vs, A.get_columns())], lag_ratio=0.5), run_time=2)
        
        with self.voiceover(text=tr("""Como en los vectores, la posición importa: <bookmark mark='o'/> si colocamos los vectores en otro lugar de la lista, obtenemos una matriz distinta.""",
                                    """As with vectors, position matters: <bookmark mark='o'/> if we place the vectors elsewhere in the list, we get a different matrix.""")) as tracker:
            self.wait_until_bookmark("o")
            self.play(FadeIn(resto_C), run_time=0.6)
            for j in ORDEN:   # b, c y a, por el orden de la nueva lista: copias de las columnas de A
                fr = franja_columna(A, j)
                self.play(FadeIn(fr), run_time=0.3)
                self.play(TransformFromCopy(letras_A[j], letras_C[j]), TransformFromCopy(A.get_columns()[j], C.get_columns()[POS[j]]), run_time=0.9)
                self.play(FadeOut(fr), run_time=0.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("El orden de una matriz", "The order of a matrix"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A = matriz(A_EJ, decimales=0, h_buff=1.0)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([-4.2, 0.9, 0])
        ll_f = Brace(A, RIGHT, buff=0.1)
        ll_c = Brace(A, UP, buff=0.15)
        r_f = ll_f.get_tex(tr(r"2\ \text{filas}", r"2\ \text{rows}"), buff=0.1).scale(0.8)
        r_c = ll_c.get_tex(tr(r"3\ \text{columnas}", r"3\ \text{columns}"), buff=0.1).scale(0.8)
        B = matriz([list(f) for f in zip(*A_EJ)], decimales=0, h_buff=1.0)
        f_B = con_nombre(r"\Mat{B}=", B).move_to([2.0, 0.9, 0])   # deja sitio a A escrita como lista
        llB_f = Brace(B, RIGHT, buff=0.1)
        llB_c = Brace(B, UP, buff=0.15)
        rB_f = llB_f.get_tex(tr(r"3\ \text{filas}", r"3\ \text{rows}"), buff=0.1).scale(0.8)
        rB_c = llB_c.get_tex(tr(r"2\ \text{columnas}", r"2\ \text{columns}"), buff=0.1).scale(0.8)
        dimA = MathTex(r"\Matdim{A}{2}{3}", tex_template=myTemplate, font_size=56)
        dimB = MathTex(r"\Matdim{B}{3}{2}", tex_template=myTemplate, font_size=56)
        neq = MathTex(r"\neq", font_size=56)
        abajo = VGroup(dimA, neq, dimB).arrange(RIGHT, buff=0.5).move_to([-1.2, -2.6, 0])
        conj = MathTex(r"\Mat{A}\in\R[2\times 3]", r"\qquad", r"\Mat{B}\in\R[3\times 2]", tex_template=myTemplate, font_size=52).move_to(abajo)
        om = omega("duda", mira=LEFT, alto=1.4).to_corner(DR, buff=0.3)
        globo = bocadillo(tr(r"¿La misma matriz?", r"The same matrix?"), om, ancho=3.0)
        
        def como_lista(filas, m):
            """La matriz m escrita como en el libro: la lista de sus columnas, cada una entre paréntesis y seguida de ";"."""
            cols = [r"\begin{pmatrix}" + r"\\ ".join(str(x) for x in c) + r"\end{pmatrix};" for c in zip(*filas)]
            lista = MathTex(r"\begin{bmatrix}" + r" & ".join(cols) + r"\end{bmatrix}", font_size=40)
            return lista.move_to(m, aligned_edge=LEFT)
        
        A_lista = como_lista(A_EJ, A)
        B_lista = como_lista([list(f) for f in zip(*A_EJ)], B)
        A_de_nuevo, B_de_nuevo = A.copy(), B.copy()
        
        with self.voiceover(text=tr("""Formemos ahora otra matriz B con dos vectores de tres componentes: <bookmark mark='x'/> el primero lleva los números de la primera fila de A, <bookmark mark='y'/> y el segundo, los de la segunda.<bookmark mark='v3'/>""",
                                    """Now let us build another matrix B with two vectors of three components: <bookmark mark='x'/> the first one carries the numbers of the first row of A, <bookmark mark='y'/> and the second one, those of the second row.<bookmark mark='v2'/>""")) as tracker:
            self.play(Write(cabecera), FadeIn(f_A), run_time=0.8)
            self.play(FadeIn(f_B[0]), FadeIn(B.get_brackets()), run_time=0.8)
            for i, marca in enumerate(["x", "y"]):
                self.wait_until_bookmark(marca)
                fr = franja_fila(A, i)
                self.play(FadeIn(fr), run_time=0.4)
                self.play(TransformFromCopy(A.get_rows()[i], B.get_columns()[i]), run_time=1.2)
                self.play(FadeOut(fr), run_time=0.3)
        
        with self.voiceover(text=tr("""Omega cree que las matrices A y B son la misma, porque tienen los mismos números.""",
                                    """Omega thinks that the matrices A and B are the same, because they have the same numbers.""")) as tracker:
            entra(self, om)
            self.play(FadeIn(globo, scale=0.8), run_time=0.6)
        
        with self.voiceover(text=tr("""Pero son listas distintas: <bookmark mark='a'/> la matriz A es una lista de tres vectores, con dos números cada uno, <bookmark mark='b'/> y B es una lista de solo dos vectores, con tres números cada uno.<bookmark mark='v4'/>""",
                                    """But they are different lists: <bookmark mark='a'/> the matrix A is a list of three vectors, with two numbers each, <bookmark mark='b'/> and B is a list of only two vectors, with three numbers each.""")) as tracker:
            self.play(FadeOut(globo), run_time=0.4)
            cambia(self, om, "sorpresa")
            self.wait(0.6)
            cambia(self, om, "normal", mira=UL)   # la sorpresa dura un instante; ahora atiende
            self.wait_until_bookmark("a")
            self.play(FadeTransform(A, A_lista), run_time=1.2)   # la lista de vectores, como en el libro
            self.wait_until_bookmark("b")
            self.play(FadeTransform(B, B_lista), run_time=1.2)
        
        with self.voiceover(text=tr("""El orden de una matriz indica precisamente esos números: primero el número de componentes de sus vectores, <bookmark mark='f'/> que es el número de filas, y después el número de vectores de la lista, <bookmark mark='c'/> que es el número de columnas. <bookmark mark='o'/> La matriz A es de orden dos por tres, <bookmark mark='p'/> y B, de orden tres por dos.""",
                                    """The order of a matrix gives precisely those numbers: first the number of components of its vectors, <bookmark mark='f'/> which is the number of rows, and then the number of vectors in the list, <bookmark mark='c'/> which is the number of columns. <bookmark mark='o'/> The matrix A is of order two by three, <bookmark mark='p'/> and B is of order three by two.""")) as tracker:
            self.play(FadeTransform(A_lista, A_de_nuevo), FadeTransform(B_lista, B_de_nuevo), run_time=1)
            self.wait_until_bookmark("f")
            self.play(GrowFromCenter(ll_f), FadeIn(r_f), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(GrowFromCenter(ll_c), FadeIn(r_c), run_time=0.8)
            self.wait_until_bookmark("o")
            self.play(Write(dimA), run_time=1)
            self.wait_until_bookmark("p")
            self.play(GrowFromCenter(llB_f), FadeIn(rB_f), GrowFromCenter(llB_c), FadeIn(rB_c), run_time=0.8)
            self.play(Write(dimB), run_time=1)
        
        with self.voiceover(text=tr("""Dos matrices de distinto orden son necesariamente distintas.""",
                                    """Two matrices of different orders are necessarily different.""")) as tracker:
            self.play(Write(neq), run_time=0.6)
        
        with self.voiceover(text=tr("""Otra forma de indicar el orden de estas matrices es decir que <bookmark mark='a'/> A pertenece al conjunto de las matrices de dos por tres, <bookmark mark='b'/> y B, al de las matrices de tres por dos.""",
                                    """Another way to give the order of these matrices is to say that <bookmark mark='a'/> A belongs to the set of two-by-three matrices, <bookmark mark='b'/> and B to the set of three-by-two matrices.""")) as tracker:
            self.wait_until_bookmark("a")   # la pertenencia de A, cuando la voz la nombra (Marcos, 2026-10-27)
            self.play(ReplacementTransform(VGroup(dimA, neq), conj[0]), run_time=1)
            self.wait_until_bookmark("b")
            self.play(ReplacementTransform(dimB, conj[2]), run_time=1)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        A = matriz(A_EJ, decimales=0, h_buff=1.0)
        B = matriz(A_EJ, decimales=0, h_buff=1.0)
        par = VGroup(con_nombre(r"\Mat{A}=", A), con_nombre(r"\Mat{B}=", B)).arrange(RIGHT, buff=1.5).move_to([0, 1, 0])
        # en palabras: el selector por la derecha (A|j) no se presenta hasta la escena 6 (Marcos, 2026-10-30)
        criterio = MathTex(r"\Mat{A}=\Mat{B}", r"\iff",
                           tr(r"\text{columna } j \text{ de } \Mat{A}=\text{columna } j \text{ de } \Mat{B}",
                              r"\text{column } j \text{ of } \Mat{A}=\text{column } j \text{ of } \Mat{B}"),
                           tex_template=myTemplate, font_size=48)
        rango = MathTex(tr(r"\text{para } j=1:n", r"\text{for } j=1:n"), tex_template=myTemplate, font_size=48)
        criterio = VGroup(criterio, rango).arrange(DOWN, buff=0.3).move_to([0, -1.9, 0])   # en una línea no cabe en español
        cabecera = Tex(tr("Igualdad de matrices", "Equality of matrices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        
        with self.voiceover(text=tr("""Como ocurre con los vectores, dos matrices son iguales si, y solo si, lo son sus respectivas listas: <bookmark mark='c1'/> la primera columna de una es igual a la primera de la otra, <bookmark mark='c2'/> la segunda a la segunda, <bookmark mark='c3'/> y así con todas.""",
                                    """As with vectors, two matrices are equal if, and only if, their respective lists are equal: <bookmark mark='c1'/> the first column of one equals the first column of the other, <bookmark mark='c2'/> the second the second, <bookmark mark='c3'/> and so on with all of them.<bookmark mark='v2'/>""")) as tracker:
            self.play(Write(cabecera), FadeIn(par), run_time=1)
            franjas = None
            for j, marca in enumerate(["c1", "c2", "c3"]):
                self.wait_until_bookmark(marca)
                nuevas = VGroup(franja_columna(A, j), franja_columna(B, j))
                self.play(FadeIn(nuevas) if franjas is None else ReplacementTransform(franjas, nuevas), run_time=0.6)
                franjas = nuevas
        
        with self.voiceover(text=tr("""Es decir, columna a columna. <bookmark mark='r'/> Las operaciones con matrices también se definirán columna a columna.""",
                                    """That is, column by column. <bookmark mark='r'/> The operations with matrices will also be defined column by column.""")) as tracker:
            self.play(FadeOut(franjas), Write(criterio), run_time=1.5)
            self.wait_until_bookmark("r")
            self.play(Indicate(criterio[0][2], color=COLOR_ESCALAR, scale_factor=1.1), run_time=1)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Notación", "Notation"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        # 1. paréntesis y corchetes
        v_ej = con_nombre(r"\Vect{a}=", MathTex(r"(4,\ 2,)", font_size=48))
        A1 = MathTex(r"\Mat{A}=", r"\begin{bmatrix}\Vect{a}; & \Vect{b}; & \Vect{c};\end{bmatrix}", tex_template=myTemplate, font_size=48)
        bloque1 = VGroup(v_ej, A1).arrange(RIGHT, buff=2.0).move_to([0, 1.2, 0])
        # 2. horizontal o vertical; matriz columna, matriz fila y vector, escritos un instante como listas del libro
        def par(izq, der, r_izq, r_der, x=0, y=1.0):
            """Dos objetos separados por "≠", con un rótulo gris debajo de cada uno."""
            g = VGroup(VGroup(izq, Tex(r_izq, font_size=30, color=GRAY_B)).arrange(DOWN, buff=0.3),
                       MathTex(r"\neq", font_size=48),
                       VGroup(der, Tex(r_der, font_size=30, color=GRAY_B)).arrange(DOWN, buff=0.3))
            g.arrange(RIGHT, buff=0.6)
            g[2][0].match_y(g[0][0]); g[2][1].match_y(g[0][1]); g[1].match_y(g[0][0])   # objetos y rótulos a la misma altura
            return g.move_to([x, y, 0])
        def como_lista(tex, rotulo, sobre):
            """La forma de lista del libro, debajo de su objeto, con un rótulo amarillo."""
            l = MathTex(tex, tex_template=myTemplate, font_size=44).next_to(sobre, DOWN, buff=1.0)
            return VGroup(l, Tex(rotulo, tex_template=myTemplate, font_size=30, color=COLOR_ESCALAR).next_to(l, DOWN, buff=0.25))
        hv = MathTex(r"(4,\ 2,)", r"=", r"\begin{pmatrix}4\\ 2\end{pmatrix}", font_size=48)
        bloque_hv = VGroup(hv, Tex(tr("el mismo vector", "the same vector"), font_size=30, color=GRAY_B)).arrange(DOWN, buff=0.3).move_to([0, -1.6, 0])
        COL = r"\begin{bmatrix}4\\ 2\end{bmatrix}"
        FIL = r"\begin{bmatrix}4 & 2\end{bmatrix}"
        # vector, matriz columna y matriz fila: tres objetos distintos (Marcos, 2026-10-27)
        vf = par(MathTex(r"\begin{pmatrix}4\\ 2\end{pmatrix}", font_size=48), MathTex(COL, font_size=48), tr("vector", "vector"), tr("matriz columna", "column matrix"))
        vf_f = VGroup(MathTex(r"\neq", font_size=48), VGroup(MathTex(FIL, font_size=48), Tex(tr("matriz fila", "row matrix"), font_size=30, color=GRAY_B)).arrange(DOWN, buff=0.3))
        vf_f.arrange(RIGHT, buff=0.6).next_to(vf, RIGHT, buff=0.6)
        vf_f[1][0].match_y(vf[0][0]); vf_f[1][1].match_y(vf[0][1]); vf_f[0].match_y(vf[0][0])
        vf.add(*vf_f).move_to([0, 1.0, 0])
        l_vec = como_lista(r"(4,\ 2,)", tr("dos números", "two numbers"), vf[0])
        l_vc = como_lista(r"\begin{bmatrix}\begin{pmatrix}4\\ 2\end{pmatrix};\end{bmatrix}", tr(r"un vector de $\R[2]$", r"one vector of $\R[2]$"), vf[2])
        l_vf = como_lista(r"\left[(4,);\ (2,);\right]", tr(r"dos vectores de $\R[1]$", r"two vectors of $\R[1]$"), vf[4])
        for l in (l_vc, l_vf): l.match_y(l_vec)
        # número, vector y matriz con un solo número
        tres = MathTex(r"3", r"\neq", r"(3,)", r"\neq", r"\begin{bmatrix}3\end{bmatrix}", font_size=48)
        r_tr = Tex(tr("número, vector y matriz", "number, vector and matrix"), font_size=30, color=GRAY_B)
        fila3 = VGroup(tres, r_tr).arrange(DOWN, buff=0.3).move_to([-0.4, -1.6, 0])   # hueco a la derecha para [(3,);]
        lista3 = MathTex(r"\begin{bmatrix}(3,);\end{bmatrix}", font_size=48).move_to(tres[4], aligned_edge=LEFT)   # una lista con un vector que contiene un número
        tres_de_nuevo = tres[4].copy()
        # 3. letras y matriz nula
        letras = MathTex(r"\Mat{A},\ \Mat{B},\ \Mat{C},\ \ldots", tex_template=myTemplate, font_size=56).move_to([0, 1.2, 0])
        ceros = VGroup(*[con_nombre(r"\Mat{0}=", matriz([[0]*n for _ in range(m)], decimales=0, h_buff=0.8))
                         for m, n in [(2, 2), (2, 3), (3, 2)]]).arrange(RIGHT, buff=0.8).move_to([0, -1.5, 0])
        # el mismo cero con su orden debajo, para cuando el contexto no lo deja claro
        ceros_dim = [MathTex(rf"\Matdim{{0}}{{{m}}}{{{n}}}", tex_template=myTemplate, font_size=48) for m, n in [(2, 2), (2, 3), (3, 2)]]
        for c, d in zip(ceros, ceros_dim):
            cero = max(d[0], key=lambda g: g.height)   # el cero en negrita (el orden va en pequeño)
            d.shift(c[0][0][0].get_center() - cero.get_center())
        
        with self.voiceover(text=tr("""Repasemos la notación que ya conocemos. Unos paréntesis alrededor de una lista de números, <bookmark mark='cm'/> cada uno seguido de una coma, denotan un vector, <bookmark mark='k'/> y unos corchetes alrededor de una lista de vectores, <bookmark mark='pc'/> cada uno seguido de un punto y coma, denotan una matriz.""",
                                    """Let us review the notation we already know. Parentheses around a list of numbers, <bookmark mark='cm'/> each followed by a comma, denote a vector, <bookmark mark='k'/> and square brackets around a list of vectors, <bookmark mark='pc'/> each followed by a semicolon, denote a matrix.""")) as tracker:
            self.play(Write(cabecera), FadeIn(v_ej), run_time=1)
            self.wait_until_bookmark("cm")
            self.play(Indicate(VGroup(v_ej[1][0][2], v_ej[1][0][4]), color=COLOR_ESCALAR, scale_factor=2), run_time=1)
            self.wait_until_bookmark("k")
            self.play(FadeIn(A1), run_time=1)
            self.wait_until_bookmark("pc")
            self.play(Indicate(VGroup(*[A1[1][k] for k in (2, 4, 6)]), color=COLOR_ESCALAR, scale_factor=2), run_time=1)
        
        with self.voiceover(text=tr("""Un vector se puede escribir en horizontal o en vertical. <bookmark mark='c'/> En una matriz, en cambio, cada vector de la lista se escribe en vertical, como una columna.<bookmark mark='v2'/>""",
                                    """A vector can be written horizontally or vertically. <bookmark mark='c'/> In a matrix, however, each vector in the list is written vertically, as a column.""")) as tracker:
            self.play(FadeIn(bloque_hv), run_time=1)
            self.wait_until_bookmark("c")
            self.play(Indicate(A1[1], color=COLOR_ESCALAR, scale_factor=1.05), run_time=1)
        
        # la escena se despeja para comparar (Marcos, 2026-10-27)
        self.play(FadeOut(VGroup(bloque1, bloque_hv)), run_time=0.8)
        with self.voiceover(text=tr("""Un vector, una matriz columna y una matriz fila con los mismos números son objetos distintos: <bookmark mark='v'/> el vector es una lista de n números, <bookmark mark='c'/> la matriz columna, una lista con un solo vector de n componentes, <bookmark mark='f'/> y la matriz fila, una lista de n vectores de una componente.""",
                                    """A vector, a column matrix and a row matrix with the same numbers are different objects: <bookmark mark='v'/> the vector is a list of n numbers, <bookmark mark='c'/> the column matrix, a list with a single vector of n components, <bookmark mark='f'/> and the row matrix, a list of n vectors of one component.""")) as tracker:
            self.play(FadeIn(vf), run_time=1)
            for marca, k, l in [("v", 0, l_vec), ("c", 2, l_vc), ("f", 4, l_vf)]:
                self.wait_until_bookmark(marca)
                self.play(TransformFromCopy(vf[k][0], l[0]), FadeIn(l[1]), run_time=0.8)
        
        self.wait(2.5)   # tiempo para mirar las listas antes de quitarlas (Marcos, 2026-10-27)
        self.play(FadeOut(VGroup(l_vec, l_vc, l_vf)), run_time=0.8)
        
        with self.voiceover(text=tr("""Del mismo modo, un número, un vector con un solo número y una matriz con un solo número son objetos distintos: <bookmark mark='n'/> un número, <bookmark mark='l'/> una lista de números, <bookmark mark='ll'/> y una lista de listas de números.<bookmark mark='v2'/>""",
                                    """Likewise, a number, a vector with a single number and a matrix with a single number are different objects: <bookmark mark='n'/> a number, <bookmark mark='l'/> a list of numbers, <bookmark mark='ll'/> and a list of lists of numbers.""")) as tracker:
            self.play(FadeIn(fila3), run_time=1)
            self.wait_until_bookmark("n")
            self.play(Indicate(tres[0], color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.7)
            self.wait_until_bookmark("l")
            self.play(Indicate(tres[2], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.7)
            self.wait_until_bookmark("ll")
            self.play(FadeTransform(tres[4], lista3), run_time=1)   # la matriz, como lista con un vector de un número
        
        self.play(FadeTransform(lista3, tres_de_nuevo), run_time=1)   # vuelve a su forma habitual
        self.wait(0.5)
        self.play(FadeOut(VGroup(vf, fila3, tres_de_nuevo)), run_time=0.8)
        with self.voiceover(text=tr("""Para denotar matrices usaremos letras mayúsculas en negrita.""",
                                    """To denote matrices we will use bold capital letters.""")) as tracker:
            self.play(FadeIn(letras), run_time=1)
        
        with self.voiceover(text=tr("""Un cero en negrita denota una matriz cuyas componentes son todas nulas. <bookmark mark='o'/> Como con el vector nulo, frecuentemente su orden se deduce del contexto. <bookmark mark='e'/> Cuando no está claro, se puede indicar explícitamente debajo del cero.<bookmark mark='v2'/>""",
                                    """A bold zero denotes a matrix whose components are all zero. <bookmark mark='o'/> As with the zero vector, its order can often be deduced from the context. <bookmark mark='e'/> When it is not clear, it can be shown explicitly under the zero.""")) as tracker:
            self.play(FadeIn(ceros[0]), run_time=1)
            self.wait_until_bookmark("o")
            self.play(LaggedStart(*[FadeIn(c) for c in ceros[1:]], lag_ratio=0.5), run_time=1.5)
            self.wait_until_bookmark("e")
            self.play(*[ReplacementTransform(c[0][0][0], d) for c, d in zip(ceros, ceros_dim)], run_time=1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Componentes, filas y columnas", "Components, rows and columns"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A = matriz(A_SEL, decimales=0, h_buff=1.0)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([0, 2.0, 0])
        x0 = -4.6
        comp = MathTex(r"\eleM{A}{2}{1}", r"\;=\;", r"a_{21}", r"\;=\;7", tex_template=myTemplate, font_size=48)
        fila = MathTex(r"\VectF{A}{1}", r"\;=\;(1,\ 2,\ 1,)", tex_template=myTemplate, font_size=48)
        col = MathTex(r"\VectC{A}{1}", r"\;=\;\begin{pmatrix}1\\ 7\end{pmatrix}", tex_template=myTemplate, font_size=48)
        for linea, y in [(comp, 0.3), (fila, -1.1), (col, -2.8)]:   # hueco para la fila en vertical
            linea.move_to([x0 + linea.width/2, y, 0])
        for linea in (fila, col):   # el "=" que sigue al selector, alineado con el de la componente
            linea.shift((comp[1].get_left()[0] - linea[1].get_left()[0])*RIGHT)
        r_hab = Tex(tr("lo habitual", "the usual way"), font_size=28, color=GRAY_B).next_to(comp[2], UP, buff=0.2)
        r_sel = Tex(tr("selector", "selector"), font_size=28, color=GRAY_B).next_to(comp[0], UP, buff=0.2)
        # glifos: a_{21} = a, 2, 1; 2|A|1 = 2, |, A, |, 1
        sub_f, sub_c = comp[2][1], comp[2][2]
        sel_i, sel_d = comp[0][0:2], comp[0][3:5]
        # la fila y la columna, primero con un índice genérico (i, j) que pasa a ser 1 en el ejemplo
        fila_g = MathTex(r"\VectF{A}{i}", tex_template=myTemplate, font_size=48)
        fila_g.shift(fila[0][2].get_center() - fila_g[0][2].get_center())   # glifos: i, |, A
        col_g = MathTex(r"\VectC{A}{j}", tex_template=myTemplate, font_size=48)
        col_g.shift(col[0][0].get_center() - col_g[0][0].get_center())       # glifos: A, |, j
        # la otra forma de escribir la fila y la columna, detrás de un "=" (Marcos, 2026-10-27)
        fila_v = MathTex(r"=\begin{pmatrix}1\\ 2\\ 1\end{pmatrix}", font_size=48).next_to(fila, RIGHT, buff=0.25)
        col_h = MathTex(r"=(1,\ 7,)", font_size=48).next_to(col, RIGHT, buff=0.25)
        
        with self.voiceover(text=tr("""Para seleccionar una componente de un vector, el operador selector necesita un índice. En una matriz necesita dos: <bookmark mark='f'/> el de la fila <bookmark mark='c'/> y el de la columna.""",
                                    """To select a component of a vector, the selector operator needs one index. In a matrix it needs two: <bookmark mark='f'/> the row index <bookmark mark='c'/> and the column index.""")) as tracker:
            self.play(Write(cabecera), FadeIn(f_A), run_time=1)
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 1)
            self.play(FadeIn(ff), run_time=0.5)
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0)
            self.play(FadeIn(fc), run_time=0.5)
            self.play(Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
        
        with self.voiceover(text=tr("""Lo habitual es escribir la componente con la letra de la matriz en minúscula y dos subíndices: <bookmark mark='i'/> primero el de la fila <bookmark mark='j'/> y después el de la columna.""",
                                    """The usual way is to write the component with the letter of the matrix in lower case and two subscripts: <bookmark mark='i'/> first the row <bookmark mark='j'/> and then the column.""")) as tracker:
            self.play(FadeIn(comp[2:]), FadeIn(r_hab), run_time=1)
            self.wait_until_bookmark("i")
            self.play(Indicate(sub_f, color=COLOR_ESCALAR, scale_factor=1.8), run_time=0.8)
            self.wait_until_bookmark("j")
            self.play(Indicate(sub_c, color=COLOR_ESCALAR, scale_factor=1.8), run_time=0.8)
        
        with self.voiceover(text=tr("""Pero en este curso, como con los vectores, usaremos principalmente el operador selector, <bookmark mark='s'/> con el índice de la fila a la izquierda de la matriz <bookmark mark='d'/> y el de la columna a la derecha.""",
                                    """But in this course, as with vectors, we will mainly use the selector operator, <bookmark mark='s'/> with the row index on the left of the matrix <bookmark mark='d'/> and the column index on the right.""")) as tracker:
            self.play(FadeIn(comp[:2]), FadeIn(r_sel), run_time=1)
            self.wait_until_bookmark("s")
            self.play(Indicate(sel_i, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("d")
            self.play(Indicate(sel_d, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
        
        # el símbolo aparece un instante antes de que la voz lo describa (Marcos, 2026-10-18)
        self.play(FadeOut(ff), FadeOut(fc), FadeIn(fila_g), run_time=0.6)
        with self.voiceover(text=tr("""Si el operador actúa solo por la izquierda, selecciona una fila: la que indica el índice. <bookmark mark='e'/> Por ejemplo, con el índice uno, <bookmark mark='f'/> selecciona la primera fila de A, que es un vector.""",
                                    """If the operator acts only on the left, it selects a row: the one given by the index. <bookmark mark='e'/> For example, with index one, <bookmark mark='f'/> it selects the first row of A, which is a vector.""")) as tracker:
            self.play(Indicate(fila_g[0][0:2], color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("e")
            self.play(ReplacementTransform(fila_g, fila[0]), run_time=0.8)   # i pasa a ser 1
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 0)
            self.play(FadeIn(ff), FadeIn(fila[1]), run_time=0.8)
        
        self.play(FadeOut(ff), FadeIn(col_g), run_time=0.6)
        with self.voiceover(text=tr("""Y si actúa solo por la derecha, selecciona una columna. <bookmark mark='e'/> Por ejemplo, con el índice uno, <bookmark mark='c'/> selecciona la primera columna de A, que también es un vector.""",
                                    """And if it acts only on the right, it selects a column. <bookmark mark='e'/> For example, with index one, <bookmark mark='c'/> it selects the first column of A, which is also a vector.""")) as tracker:
            self.play(Indicate(col_g[0][1:3], color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("e")
            self.play(ReplacementTransform(col_g, col[0]), run_time=0.8)   # j pasa a ser 1
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0)
            self.play(FadeIn(fc), FadeIn(col[1]), run_time=0.8)
        
        self.wait(0.6)   # una pausa antes de la conclusión (Marcos, 2026-10-27)
        with self.voiceover(text=tr("""Filas y columnas son vectores, y por eso las podemos escribir indistintamente en horizontal <bookmark mark='h'/> o en vertical, <bookmark mark='p'/> con sus listas de números siempre entre paréntesis.""",
                                    """Rows and columns are vectors, so we can write them either horizontally <bookmark mark='h'/> or vertically, <bookmark mark='p'/> with their lists of numbers always in parentheses.""")) as tracker:
            self.play(FadeOut(fc), run_time=0.5)
            self.wait_until_bookmark("h")
            self.play(FadeIn(fila_v), FadeIn(col_h), run_time=1)
            self.wait_until_bookmark("p")
            self.play(*[Indicate(m, color=COLOR_ESCALAR, scale_factor=1.1) for m in (fila[1], col[1], fila_v, col_h)], run_time=1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        defin = Tex(tr(r"Matriz de ", r"Matrix in "), r"$\R[m\times n]$", tr(r": ", r": an "), tr(r"lista ordenada", r"ordered list"), tr(r" de ", r" of "),
                    r"$n$", tr(r" vectores de ", r" vectors in "), r"$\R[m]$", tr(r"\\ (sus columnas), entre corchetes.", r"\\ (its columns), in square brackets."),
                    tex_template=myTemplate, font_size=34)
        orden = Tex(tr(r"Orden ", r"Order "), r"$m\times n$", tr(r": primero las filas, después las columnas.", r": rows first, then columns."),
                    tex_template=myTemplate, font_size=34)
        # glifos: orden[1] = m, ×, n
        encabezados = [tr("fila $i$", "row $i$"), tr("componente $ij$", "component $ij$"), tr("columna $j$", "column $j$")]
        formulas = [r"\VectF{A}{i}\in\R[n]", r"\eleM{A}{i}{j}=a_{ij}", r"\VectC{A}{j}\in\R[m]"]
        tabla = VGroup(*[VGroup(Tex(e, tex_template=myTemplate, font_size=32, color=GRAY_B), MathTex(f, tex_template=myTemplate, font_size=44)).arrange(DOWN, buff=0.3)
                         for e, f in zip(encabezados, formulas)]).arrange(RIGHT, buff=1.2)
        bloque = VGroup(defin, orden, tabla).arrange(DOWN, buff=0.6).next_to(cabecera, DOWN, buff=0.7)
        
        # señales en la definición (Marcos, 2026-10-27): un efecto cada vez, cuando la voz lo nombra
        with self.voiceover(text=tr("""Resumamos. Una matriz es una <bookmark mark='l'/> lista ordenada <bookmark mark='n'/> de vectores <bookmark mark='m'/> con el mismo número de componentes; dichos vectores son las columnas de la matriz. La lista de vectores se escribe entre corchetes. <bookmark mark='o'/> Su orden indica <bookmark mark='f'/> el número de filas primero <bookmark mark='c'/> y el número de columnas después.""",
                                    """Let us sum up. A matrix is an <bookmark mark='l'/> ordered list <bookmark mark='n'/> of vectors <bookmark mark='m'/> with the same number of components; these vectors are the columns of the matrix. The list of vectors is written in square brackets. <bookmark mark='o'/> Its order gives <bookmark mark='f'/> the number of rows first <bookmark mark='c'/> and the number of columns second.""")) as tracker:
            self.play(Write(cabecera), FadeIn(defin), run_time=1)
            self.wait_until_bookmark("l")
            self.play(Circumscribe(defin[3], color=COLOR_ESCALAR, buff=0.08), run_time=1)
            # (los Indicate de m y n en la definición se quitaron: no daban el efecto buscado; Marcos, 2026-10-27)
            self.wait_until_bookmark("o")
            self.play(FadeIn(orden), run_time=0.8)
            self.wait_until_bookmark("f")
            self.play(Indicate(orden[1][0], color=COLOR_FILA, scale_factor=1.8), run_time=1)
            self.wait_until_bookmark("c")
            self.play(Indicate(orden[1][2], color=COLOR_COLUMNA, scale_factor=1.8), run_time=1)
        
        # el operador se destaca cuando la voz dice por qué lado actúa (Marcos, 2026-10-27)
        # glifos: tabla[0][1] = i, |, A, ...;  tabla[1][1] = i, |, A, |, j, ...;  tabla[2][1] = A, |, j, ...
        sel_fila, sel_col = tabla[0][1][0][0:2], tabla[2][1][0][1:3]
        sel_comp = [tabla[1][1][0][0:2], tabla[1][1][0][3:5]]
        with self.voiceover(text=tr("""Con el operador selector actuando <bookmark mark='i'/> por la izquierda, seleccionamos una fila. <bookmark mark='c'/> Con el operador selector actuando <bookmark mark='d'/> por la derecha, una columna. <bookmark mark='e'/> Y con el operador selector actuando <bookmark mark='a'/> por ambos lados, seleccionamos una componente.""",
                                    """With the selector operator acting <bookmark mark='i'/> on the left, we select a row. <bookmark mark='c'/> With the selector operator acting <bookmark mark='d'/> on the right, a column. <bookmark mark='e'/> And with the selector operator acting <bookmark mark='a'/> on both sides, we select a component.<bookmark mark='v3'/>""")) as tracker:
            self.play(FadeIn(tabla[0]), run_time=0.8)
            self.wait_until_bookmark("i")
            self.play(Indicate(sel_fila, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("c")
            self.play(FadeIn(tabla[2]), run_time=0.8)
            self.wait_until_bookmark("d")
            self.play(Indicate(sel_col, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("e")
            self.play(FadeIn(tabla[1]), run_time=0.8)
            self.wait_until_bookmark("a")
            self.play(*[Indicate(g, color=COLOR_ESCALAR, scale_factor=1.6) for g in sel_comp], run_time=0.9)
        
        self.wait(0.5)   # una pausa antes de anunciar el próximo vídeo, como en V08
        with self.voiceover(text=tr("""En el próximo vídeo veremos que, para seleccionar una componente de una matriz, da igual empezar por la fila o por la columna. También veremos la transposición, que convierte las filas de una matriz en columnas, como hicimos al formar la matriz B.<bookmark mark='w3'/>""",
                                    """In the next video we will see that, to select a component of a matrix, it makes no difference whether we start with the row or with the column. We will also meet transposition, which turns the rows of a matrix into columns, as we did when we built the matrix B.<bookmark mark='v2'/>""")) as tracker:
            pass
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos_finales()


class L01_V09_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class L01_V09_E01_LaMatriz(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        tabla = tabla_pib([0.8, -0.6, 0], font_size=32)
        M = tabla[0]
        defin = Tex(tr(r"Una \emph{matriz} de ", r"A \emph{matrix} in "), r"$\R[m\times n]$",
                    tr(r" es una lista ordenada\\ de ", r" is an ordered list\\ of "), r"$n$",
                    tr(r" vectores de ", r" vectors in "), r"$\R[m]$", tr(r": sus \emph{columnas}.", r": its \emph{columns}."),
                    tex_template=myTemplate, font_size=48).move_to([0, 0.6, 0])
        m_s = VGroup(defin[1][1], defin[5][1])    # la m del superíndice y la de R^m
        n_s = VGroup(defin[1][3], defin[3][0])    # la n del superíndice y la de "n vectores"
        
        with self.voiceover(text=tr("""En el vídeo anterior pusimos uno al lado del otro los cuatro vectores con el crecimiento del PIB de cinco países, y obtuvimos esta tabla de números.""",
                                    """In the previous video we placed side by side the four vectors with the GDP growth of five countries, and we got this table of numbers.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
            self.play(FadeIn(tabla), run_time=1.5)
        
        with self.voiceover(text=tr("""Cada columna de la tabla es uno de esos vectores. <bookmark mark='m'/> Una lista ordenada de vectores como esta se llama matriz.""",
                                    """Each column of the table is one of those vectors. <bookmark mark='m'/> An ordered list of vectors like this one is called a matrix.""")) as tracker:
            franja = None
            for j in range(4):
                nueva = franja_columna(M, j)
                self.play(FadeIn(nueva) if franja is None else ReplacementTransform(franja, nueva), run_time=0.5)
                franja = nueva
            self.play(FadeOut(franja), run_time=0.4)
            self.wait_until_bookmark("m")
            self.play(FadeOut(tabla[1]), FadeOut(tabla[2]), M.animate.move_to([0, -0.6, 0]), run_time=1)   # solo la matriz, en el centro
        
        self.wait(0.5)   # una pausa antes de la definición general (Marcos, 2026-10-26)
        with self.voiceover(text=tr("""En general, una matriz es una lista ordenada de vectores, todos con el mismo número de componentes, que constituyen sus columnas.""",
                                    """In general, a matrix is an ordered list of vectors, all with the same number of components, which make up its columns.""")) as tracker:
            self.play(FadeOut(M), run_time=0.8)
            self.play(FadeIn(defin), run_time=1)
        
        with self.voiceover(text=tr("""En el superíndice, la primera letra indica cuántas componentes tiene cada vector, <bookmark mark='n'/> y la segunda, cuántos vectores hay en la lista.""",
                                    """In the superscript, the first letter tells how many components each vector has, <bookmark mark='n'/> and the second, how many vectors there are in the list.""")) as tracker:
            self.play(Indicate(m_s, color=COLOR_FILA, scale_factor=1.5), run_time=1)
            self.play(m_s.animate.set_color(COLOR_FILA), run_time=0.3)   # Indicate devuelve el color original
            self.wait_until_bookmark("n")
            self.play(Indicate(n_s, color=COLOR_COLUMNA, scale_factor=1.5), run_time=1)
            self.play(n_s.animate.set_color(COLOR_COLUMNA), run_time=0.3)
        
        self.pausa_media()


class L01_V09_E02_Ejemplos(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Ejemplos", "Examples"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        cols = list(zip(*A_EJ))   # las columnas de A: a, b y c
        COLORES = [COLOR_A, COLOR_B, COLOR_C]   # un color por vector, para seguirlos cuando cambian de sitio
        vs = [vector(c, color=k, decimales=0) for c, k in zip(cols, COLORES)]
        vecs = VGroup(*[con_nombre(rf"\Vect{{{l}}}=", v) for l, v in zip("abc", vs)]).arrange(RIGHT, buff=1.0).move_to([0, 1.9, 0])
        for v, k in zip(vecs, COLORES):
            v[0][0][0].set_color(k)   # la letra del vector
        A = matriz(A_EJ, decimales=0, h_buff=1.0)
        f_A = con_nombre(r"\Mat{A}=\begin{bmatrix}\Vect{a}; & \Vect{b}; & \Vect{c};\end{bmatrix}=", A).move_to([0, -0.1, 0])
        ORDEN = (1, 2, 0)   # la nueva lista [b; c; a]: todos los vectores cambian de sitio
        POS = {j: p for p, j in enumerate(ORDEN)}   # posición de cada vector en la nueva lista
        C = matriz([[r[j] for j in ORDEN] for r in A_EJ], decimales=0, h_buff=1.0)
        f_C = VGroup(MathTex(r"\begin{bmatrix}\Vect{b}; & \Vect{c}; & \Vect{a};\end{bmatrix}=", tex_template=myTemplate, font_size=48), C,
                     MathTex(r"\neq\Mat{A}", tex_template=myTemplate, font_size=48)).arrange(RIGHT, buff=0.2).move_to([0, -2.4, 0])
        f_C.shift((f_A[1].get_x() - C.get_x())*RIGHT)   # las dos matrices numéricas, una encima de la otra
        # glifos: f_A[0] = A = [ a ; b ; c ; ] =  (letras 3, 5, 7);  f_C[0] = [ b ; c ; a ; ] =  (letras 1, 3, 5)
        letras_A = [f_A[0][0][3], f_A[0][0][5], f_A[0][0][7]]
        letras_C = [f_C[0][0][1 + 2*POS[j]] for j in range(3)]   # dónde acaba cada vector (a, b, c)
        for k, la, lc in zip(COLORES, letras_A, letras_C):
            la.set_color(k); lc.set_color(k)
        for j, k in enumerate(COLORES):
            A.get_columns()[j].set_color(k)
            C.get_columns()[POS[j]].set_color(k)
        resto_C = VGroup(*[g for g in f_C[0][0] if all(g is not l for l in letras_C)], C.get_brackets(), f_C[2])
        
        with self.voiceover(text=tr("""Veamos un ejemplo con tres vectores de dos componentes.""",
                                    """Let us look at an example with three vectors of two components.""")) as tracker:
            self.play(Write(cabecera), LaggedStart(*[FadeIn(v) for v in vecs], lag_ratio=0.4), run_time=1.5)
        
        with self.voiceover(text=tr("""Con ellos formamos la matriz A, <bookmark mark='l'/> que es la lista de los tres vectores entre corchetes. <bookmark mark='c'/> Cada vector es una columna, y las columnas se escriben una al lado de la otra.""",
                                    """With them we build the matrix A, <bookmark mark='l'/> which is the list of the three vectors in square brackets. <bookmark mark='c'/> Each vector is a column, and the columns are written side by side.""")) as tracker:
            self.wait_until_bookmark("l")
            self.play(Write(f_A[0]), run_time=1.2)
            self.wait_until_bookmark("c")
            self.play(FadeIn(A.get_brackets()), run_time=0.4)
            self.play(LaggedStart(*[TransformFromCopy(v.get_entries(), col) for v, col in zip(vs, A.get_columns())], lag_ratio=0.5), run_time=2)
        
        with self.voiceover(text=tr("""Como en los vectores, la posición importa: <bookmark mark='o'/> si colocamos los vectores en otro lugar de la lista, obtenemos una matriz distinta.""",
                                    """As with vectors, position matters: <bookmark mark='o'/> if we place the vectors elsewhere in the list, we get a different matrix.""")) as tracker:
            self.wait_until_bookmark("o")
            self.play(FadeIn(resto_C), run_time=0.6)
            for j in ORDEN:   # b, c y a, por el orden de la nueva lista: copias de las columnas de A
                fr = franja_columna(A, j)
                self.play(FadeIn(fr), run_time=0.3)
                self.play(TransformFromCopy(letras_A[j], letras_C[j]), TransformFromCopy(A.get_columns()[j], C.get_columns()[POS[j]]), run_time=0.9)
                self.play(FadeOut(fr), run_time=0.2)
        
        self.pausa_media()


class L01_V09_E03_Orden(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("El orden de una matriz", "The order of a matrix"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A = matriz(A_EJ, decimales=0, h_buff=1.0)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([-4.2, 0.9, 0])
        ll_f = Brace(A, RIGHT, buff=0.1)
        ll_c = Brace(A, UP, buff=0.15)
        r_f = ll_f.get_tex(tr(r"2\ \text{filas}", r"2\ \text{rows}"), buff=0.1).scale(0.8)
        r_c = ll_c.get_tex(tr(r"3\ \text{columnas}", r"3\ \text{columns}"), buff=0.1).scale(0.8)
        B = matriz([list(f) for f in zip(*A_EJ)], decimales=0, h_buff=1.0)
        f_B = con_nombre(r"\Mat{B}=", B).move_to([2.0, 0.9, 0])   # deja sitio a A escrita como lista
        llB_f = Brace(B, RIGHT, buff=0.1)
        llB_c = Brace(B, UP, buff=0.15)
        rB_f = llB_f.get_tex(tr(r"3\ \text{filas}", r"3\ \text{rows}"), buff=0.1).scale(0.8)
        rB_c = llB_c.get_tex(tr(r"2\ \text{columnas}", r"2\ \text{columns}"), buff=0.1).scale(0.8)
        dimA = MathTex(r"\Matdim{A}{2}{3}", tex_template=myTemplate, font_size=56)
        dimB = MathTex(r"\Matdim{B}{3}{2}", tex_template=myTemplate, font_size=56)
        neq = MathTex(r"\neq", font_size=56)
        abajo = VGroup(dimA, neq, dimB).arrange(RIGHT, buff=0.5).move_to([-1.2, -2.6, 0])
        conj = MathTex(r"\Mat{A}\in\R[2\times 3]", r"\qquad", r"\Mat{B}\in\R[3\times 2]", tex_template=myTemplate, font_size=52).move_to(abajo)
        om = omega("duda", mira=LEFT, alto=1.4).to_corner(DR, buff=0.3)
        globo = bocadillo(tr(r"¿La misma matriz?", r"The same matrix?"), om, ancho=3.0)
        
        def como_lista(filas, m):
            """La matriz m escrita como en el libro: la lista de sus columnas, cada una entre paréntesis y seguida de ";"."""
            cols = [r"\begin{pmatrix}" + r"\\ ".join(str(x) for x in c) + r"\end{pmatrix};" for c in zip(*filas)]
            lista = MathTex(r"\begin{bmatrix}" + r" & ".join(cols) + r"\end{bmatrix}", font_size=40)
            return lista.move_to(m, aligned_edge=LEFT)
        
        A_lista = como_lista(A_EJ, A)
        B_lista = como_lista([list(f) for f in zip(*A_EJ)], B)
        A_de_nuevo, B_de_nuevo = A.copy(), B.copy()
        
        with self.voiceover(text=tr("""Formemos ahora otra matriz B con dos vectores de tres componentes: <bookmark mark='x'/> el primero lleva los números de la primera fila de A, <bookmark mark='y'/> y el segundo, los de la segunda.<bookmark mark='v3'/>""",
                                    """Now let us build another matrix B with two vectors of three components: <bookmark mark='x'/> the first one carries the numbers of the first row of A, <bookmark mark='y'/> and the second one, those of the second row.<bookmark mark='v2'/>""")) as tracker:
            self.play(Write(cabecera), FadeIn(f_A), run_time=0.8)
            self.play(FadeIn(f_B[0]), FadeIn(B.get_brackets()), run_time=0.8)
            for i, marca in enumerate(["x", "y"]):
                self.wait_until_bookmark(marca)
                fr = franja_fila(A, i)
                self.play(FadeIn(fr), run_time=0.4)
                self.play(TransformFromCopy(A.get_rows()[i], B.get_columns()[i]), run_time=1.2)
                self.play(FadeOut(fr), run_time=0.3)
        
        with self.voiceover(text=tr("""Omega cree que las matrices A y B son la misma, porque tienen los mismos números.""",
                                    """Omega thinks that the matrices A and B are the same, because they have the same numbers.""")) as tracker:
            entra(self, om)
            self.play(FadeIn(globo, scale=0.8), run_time=0.6)
        
        with self.voiceover(text=tr("""Pero son listas distintas: <bookmark mark='a'/> la matriz A es una lista de tres vectores, con dos números cada uno, <bookmark mark='b'/> y B es una lista de solo dos vectores, con tres números cada uno.<bookmark mark='v4'/>""",
                                    """But they are different lists: <bookmark mark='a'/> the matrix A is a list of three vectors, with two numbers each, <bookmark mark='b'/> and B is a list of only two vectors, with three numbers each.""")) as tracker:
            self.play(FadeOut(globo), run_time=0.4)
            cambia(self, om, "sorpresa")
            self.wait(0.6)
            cambia(self, om, "normal", mira=UL)   # la sorpresa dura un instante; ahora atiende
            self.wait_until_bookmark("a")
            self.play(FadeTransform(A, A_lista), run_time=1.2)   # la lista de vectores, como en el libro
            self.wait_until_bookmark("b")
            self.play(FadeTransform(B, B_lista), run_time=1.2)
        
        with self.voiceover(text=tr("""El orden de una matriz indica precisamente esos números: primero el número de componentes de sus vectores, <bookmark mark='f'/> que es el número de filas, y después el número de vectores de la lista, <bookmark mark='c'/> que es el número de columnas. <bookmark mark='o'/> La matriz A es de orden dos por tres, <bookmark mark='p'/> y B, de orden tres por dos.""",
                                    """The order of a matrix gives precisely those numbers: first the number of components of its vectors, <bookmark mark='f'/> which is the number of rows, and then the number of vectors in the list, <bookmark mark='c'/> which is the number of columns. <bookmark mark='o'/> The matrix A is of order two by three, <bookmark mark='p'/> and B is of order three by two.""")) as tracker:
            self.play(FadeTransform(A_lista, A_de_nuevo), FadeTransform(B_lista, B_de_nuevo), run_time=1)
            self.wait_until_bookmark("f")
            self.play(GrowFromCenter(ll_f), FadeIn(r_f), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(GrowFromCenter(ll_c), FadeIn(r_c), run_time=0.8)
            self.wait_until_bookmark("o")
            self.play(Write(dimA), run_time=1)
            self.wait_until_bookmark("p")
            self.play(GrowFromCenter(llB_f), FadeIn(rB_f), GrowFromCenter(llB_c), FadeIn(rB_c), run_time=0.8)
            self.play(Write(dimB), run_time=1)
        
        with self.voiceover(text=tr("""Dos matrices de distinto orden son necesariamente distintas.""",
                                    """Two matrices of different orders are necessarily different.""")) as tracker:
            self.play(Write(neq), run_time=0.6)
        
        with self.voiceover(text=tr("""Otra forma de indicar el orden de estas matrices es decir que <bookmark mark='a'/> A pertenece al conjunto de las matrices de dos por tres, <bookmark mark='b'/> y B, al de las matrices de tres por dos.""",
                                    """Another way to give the order of these matrices is to say that <bookmark mark='a'/> A belongs to the set of two-by-three matrices, <bookmark mark='b'/> and B to the set of three-by-two matrices.""")) as tracker:
            self.wait_until_bookmark("a")   # la pertenencia de A, cuando la voz la nombra (Marcos, 2026-10-27)
            self.play(ReplacementTransform(VGroup(dimA, neq), conj[0]), run_time=1)
            self.wait_until_bookmark("b")
            self.play(ReplacementTransform(dimB, conj[2]), run_time=1)
        
        self.pausa_media()


class L01_V09_E04_Igualdad(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        A = matriz(A_EJ, decimales=0, h_buff=1.0)
        B = matriz(A_EJ, decimales=0, h_buff=1.0)
        par = VGroup(con_nombre(r"\Mat{A}=", A), con_nombre(r"\Mat{B}=", B)).arrange(RIGHT, buff=1.5).move_to([0, 1, 0])
        # en palabras: el selector por la derecha (A|j) no se presenta hasta la escena 6 (Marcos, 2026-10-30)
        criterio = MathTex(r"\Mat{A}=\Mat{B}", r"\iff",
                           tr(r"\text{columna } j \text{ de } \Mat{A}=\text{columna } j \text{ de } \Mat{B}",
                              r"\text{column } j \text{ of } \Mat{A}=\text{column } j \text{ of } \Mat{B}"),
                           tex_template=myTemplate, font_size=48)
        rango = MathTex(tr(r"\text{para } j=1:n", r"\text{for } j=1:n"), tex_template=myTemplate, font_size=48)
        criterio = VGroup(criterio, rango).arrange(DOWN, buff=0.3).move_to([0, -1.9, 0])   # en una línea no cabe en español
        cabecera = Tex(tr("Igualdad de matrices", "Equality of matrices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        
        with self.voiceover(text=tr("""Como ocurre con los vectores, dos matrices son iguales si, y solo si, lo son sus respectivas listas: <bookmark mark='c1'/> la primera columna de una es igual a la primera de la otra, <bookmark mark='c2'/> la segunda a la segunda, <bookmark mark='c3'/> y así con todas.""",
                                    """As with vectors, two matrices are equal if, and only if, their respective lists are equal: <bookmark mark='c1'/> the first column of one equals the first column of the other, <bookmark mark='c2'/> the second the second, <bookmark mark='c3'/> and so on with all of them.<bookmark mark='v2'/>""")) as tracker:
            self.play(Write(cabecera), FadeIn(par), run_time=1)
            franjas = None
            for j, marca in enumerate(["c1", "c2", "c3"]):
                self.wait_until_bookmark(marca)
                nuevas = VGroup(franja_columna(A, j), franja_columna(B, j))
                self.play(FadeIn(nuevas) if franjas is None else ReplacementTransform(franjas, nuevas), run_time=0.6)
                franjas = nuevas
        
        with self.voiceover(text=tr("""Es decir, columna a columna. <bookmark mark='r'/> Las operaciones con matrices también se definirán columna a columna.""",
                                    """That is, column by column. <bookmark mark='r'/> The operations with matrices will also be defined column by column.""")) as tracker:
            self.play(FadeOut(franjas), Write(criterio), run_time=1.5)
            self.wait_until_bookmark("r")
            self.play(Indicate(criterio[0][2], color=COLOR_ESCALAR, scale_factor=1.1), run_time=1)
        
        self.pausa_media()


class L01_V09_E05_Notacion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Notación", "Notation"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        # 1. paréntesis y corchetes
        v_ej = con_nombre(r"\Vect{a}=", MathTex(r"(4,\ 2,)", font_size=48))
        A1 = MathTex(r"\Mat{A}=", r"\begin{bmatrix}\Vect{a}; & \Vect{b}; & \Vect{c};\end{bmatrix}", tex_template=myTemplate, font_size=48)
        bloque1 = VGroup(v_ej, A1).arrange(RIGHT, buff=2.0).move_to([0, 1.2, 0])
        # 2. horizontal o vertical; matriz columna, matriz fila y vector, escritos un instante como listas del libro
        def par(izq, der, r_izq, r_der, x=0, y=1.0):
            """Dos objetos separados por "≠", con un rótulo gris debajo de cada uno."""
            g = VGroup(VGroup(izq, Tex(r_izq, font_size=30, color=GRAY_B)).arrange(DOWN, buff=0.3),
                       MathTex(r"\neq", font_size=48),
                       VGroup(der, Tex(r_der, font_size=30, color=GRAY_B)).arrange(DOWN, buff=0.3))
            g.arrange(RIGHT, buff=0.6)
            g[2][0].match_y(g[0][0]); g[2][1].match_y(g[0][1]); g[1].match_y(g[0][0])   # objetos y rótulos a la misma altura
            return g.move_to([x, y, 0])
        def como_lista(tex, rotulo, sobre):
            """La forma de lista del libro, debajo de su objeto, con un rótulo amarillo."""
            l = MathTex(tex, tex_template=myTemplate, font_size=44).next_to(sobre, DOWN, buff=1.0)
            return VGroup(l, Tex(rotulo, tex_template=myTemplate, font_size=30, color=COLOR_ESCALAR).next_to(l, DOWN, buff=0.25))
        hv = MathTex(r"(4,\ 2,)", r"=", r"\begin{pmatrix}4\\ 2\end{pmatrix}", font_size=48)
        bloque_hv = VGroup(hv, Tex(tr("el mismo vector", "the same vector"), font_size=30, color=GRAY_B)).arrange(DOWN, buff=0.3).move_to([0, -1.6, 0])
        COL = r"\begin{bmatrix}4\\ 2\end{bmatrix}"
        FIL = r"\begin{bmatrix}4 & 2\end{bmatrix}"
        # vector, matriz columna y matriz fila: tres objetos distintos (Marcos, 2026-10-27)
        vf = par(MathTex(r"\begin{pmatrix}4\\ 2\end{pmatrix}", font_size=48), MathTex(COL, font_size=48), tr("vector", "vector"), tr("matriz columna", "column matrix"))
        vf_f = VGroup(MathTex(r"\neq", font_size=48), VGroup(MathTex(FIL, font_size=48), Tex(tr("matriz fila", "row matrix"), font_size=30, color=GRAY_B)).arrange(DOWN, buff=0.3))
        vf_f.arrange(RIGHT, buff=0.6).next_to(vf, RIGHT, buff=0.6)
        vf_f[1][0].match_y(vf[0][0]); vf_f[1][1].match_y(vf[0][1]); vf_f[0].match_y(vf[0][0])
        vf.add(*vf_f).move_to([0, 1.0, 0])
        l_vec = como_lista(r"(4,\ 2,)", tr("dos números", "two numbers"), vf[0])
        l_vc = como_lista(r"\begin{bmatrix}\begin{pmatrix}4\\ 2\end{pmatrix};\end{bmatrix}", tr(r"un vector de $\R[2]$", r"one vector of $\R[2]$"), vf[2])
        l_vf = como_lista(r"\left[(4,);\ (2,);\right]", tr(r"dos vectores de $\R[1]$", r"two vectors of $\R[1]$"), vf[4])
        for l in (l_vc, l_vf): l.match_y(l_vec)
        # número, vector y matriz con un solo número
        tres = MathTex(r"3", r"\neq", r"(3,)", r"\neq", r"\begin{bmatrix}3\end{bmatrix}", font_size=48)
        r_tr = Tex(tr("número, vector y matriz", "number, vector and matrix"), font_size=30, color=GRAY_B)
        fila3 = VGroup(tres, r_tr).arrange(DOWN, buff=0.3).move_to([-0.4, -1.6, 0])   # hueco a la derecha para [(3,);]
        lista3 = MathTex(r"\begin{bmatrix}(3,);\end{bmatrix}", font_size=48).move_to(tres[4], aligned_edge=LEFT)   # una lista con un vector que contiene un número
        tres_de_nuevo = tres[4].copy()
        # 3. letras y matriz nula
        letras = MathTex(r"\Mat{A},\ \Mat{B},\ \Mat{C},\ \ldots", tex_template=myTemplate, font_size=56).move_to([0, 1.2, 0])
        ceros = VGroup(*[con_nombre(r"\Mat{0}=", matriz([[0]*n for _ in range(m)], decimales=0, h_buff=0.8))
                         for m, n in [(2, 2), (2, 3), (3, 2)]]).arrange(RIGHT, buff=0.8).move_to([0, -1.5, 0])
        # el mismo cero con su orden debajo, para cuando el contexto no lo deja claro
        ceros_dim = [MathTex(rf"\Matdim{{0}}{{{m}}}{{{n}}}", tex_template=myTemplate, font_size=48) for m, n in [(2, 2), (2, 3), (3, 2)]]
        for c, d in zip(ceros, ceros_dim):
            cero = max(d[0], key=lambda g: g.height)   # el cero en negrita (el orden va en pequeño)
            d.shift(c[0][0][0].get_center() - cero.get_center())
        
        with self.voiceover(text=tr("""Repasemos la notación que ya conocemos. Unos paréntesis alrededor de una lista de números, <bookmark mark='cm'/> cada uno seguido de una coma, denotan un vector, <bookmark mark='k'/> y unos corchetes alrededor de una lista de vectores, <bookmark mark='pc'/> cada uno seguido de un punto y coma, denotan una matriz.""",
                                    """Let us review the notation we already know. Parentheses around a list of numbers, <bookmark mark='cm'/> each followed by a comma, denote a vector, <bookmark mark='k'/> and square brackets around a list of vectors, <bookmark mark='pc'/> each followed by a semicolon, denote a matrix.""")) as tracker:
            self.play(Write(cabecera), FadeIn(v_ej), run_time=1)
            self.wait_until_bookmark("cm")
            self.play(Indicate(VGroup(v_ej[1][0][2], v_ej[1][0][4]), color=COLOR_ESCALAR, scale_factor=2), run_time=1)
            self.wait_until_bookmark("k")
            self.play(FadeIn(A1), run_time=1)
            self.wait_until_bookmark("pc")
            self.play(Indicate(VGroup(*[A1[1][k] for k in (2, 4, 6)]), color=COLOR_ESCALAR, scale_factor=2), run_time=1)
        
        with self.voiceover(text=tr("""Un vector se puede escribir en horizontal o en vertical. <bookmark mark='c'/> En una matriz, en cambio, cada vector de la lista se escribe en vertical, como una columna.<bookmark mark='v2'/>""",
                                    """A vector can be written horizontally or vertically. <bookmark mark='c'/> In a matrix, however, each vector in the list is written vertically, as a column.""")) as tracker:
            self.play(FadeIn(bloque_hv), run_time=1)
            self.wait_until_bookmark("c")
            self.play(Indicate(A1[1], color=COLOR_ESCALAR, scale_factor=1.05), run_time=1)
        
        # la escena se despeja para comparar (Marcos, 2026-10-27)
        self.play(FadeOut(VGroup(bloque1, bloque_hv)), run_time=0.8)
        with self.voiceover(text=tr("""Un vector, una matriz columna y una matriz fila con los mismos números son objetos distintos: <bookmark mark='v'/> el vector es una lista de n números, <bookmark mark='c'/> la matriz columna, una lista con un solo vector de n componentes, <bookmark mark='f'/> y la matriz fila, una lista de n vectores de una componente.""",
                                    """A vector, a column matrix and a row matrix with the same numbers are different objects: <bookmark mark='v'/> the vector is a list of n numbers, <bookmark mark='c'/> the column matrix, a list with a single vector of n components, <bookmark mark='f'/> and the row matrix, a list of n vectors of one component.""")) as tracker:
            self.play(FadeIn(vf), run_time=1)
            for marca, k, l in [("v", 0, l_vec), ("c", 2, l_vc), ("f", 4, l_vf)]:
                self.wait_until_bookmark(marca)
                self.play(TransformFromCopy(vf[k][0], l[0]), FadeIn(l[1]), run_time=0.8)
        
        self.wait(2.5)   # tiempo para mirar las listas antes de quitarlas (Marcos, 2026-10-27)
        self.play(FadeOut(VGroup(l_vec, l_vc, l_vf)), run_time=0.8)
        
        with self.voiceover(text=tr("""Del mismo modo, un número, un vector con un solo número y una matriz con un solo número son objetos distintos: <bookmark mark='n'/> un número, <bookmark mark='l'/> una lista de números, <bookmark mark='ll'/> y una lista de listas de números.<bookmark mark='v2'/>""",
                                    """Likewise, a number, a vector with a single number and a matrix with a single number are different objects: <bookmark mark='n'/> a number, <bookmark mark='l'/> a list of numbers, <bookmark mark='ll'/> and a list of lists of numbers.""")) as tracker:
            self.play(FadeIn(fila3), run_time=1)
            self.wait_until_bookmark("n")
            self.play(Indicate(tres[0], color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.7)
            self.wait_until_bookmark("l")
            self.play(Indicate(tres[2], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.7)
            self.wait_until_bookmark("ll")
            self.play(FadeTransform(tres[4], lista3), run_time=1)   # la matriz, como lista con un vector de un número
        
        self.play(FadeTransform(lista3, tres_de_nuevo), run_time=1)   # vuelve a su forma habitual
        self.wait(0.5)
        self.play(FadeOut(VGroup(vf, fila3, tres_de_nuevo)), run_time=0.8)
        with self.voiceover(text=tr("""Para denotar matrices usaremos letras mayúsculas en negrita.""",
                                    """To denote matrices we will use bold capital letters.""")) as tracker:
            self.play(FadeIn(letras), run_time=1)
        
        with self.voiceover(text=tr("""Un cero en negrita denota una matriz cuyas componentes son todas nulas. <bookmark mark='o'/> Como con el vector nulo, frecuentemente su orden se deduce del contexto. <bookmark mark='e'/> Cuando no está claro, se puede indicar explícitamente debajo del cero.<bookmark mark='v2'/>""",
                                    """A bold zero denotes a matrix whose components are all zero. <bookmark mark='o'/> As with the zero vector, its order can often be deduced from the context. <bookmark mark='e'/> When it is not clear, it can be shown explicitly under the zero.""")) as tracker:
            self.play(FadeIn(ceros[0]), run_time=1)
            self.wait_until_bookmark("o")
            self.play(LaggedStart(*[FadeIn(c) for c in ceros[1:]], lag_ratio=0.5), run_time=1.5)
            self.wait_until_bookmark("e")
            self.play(*[ReplacementTransform(c[0][0][0], d) for c, d in zip(ceros, ceros_dim)], run_time=1.2)
        
        self.pausa_media()


class L01_V09_E06_Selectores(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Componentes, filas y columnas", "Components, rows and columns"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A = matriz(A_SEL, decimales=0, h_buff=1.0)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([0, 2.0, 0])
        x0 = -4.6
        comp = MathTex(r"\eleM{A}{2}{1}", r"\;=\;", r"a_{21}", r"\;=\;7", tex_template=myTemplate, font_size=48)
        fila = MathTex(r"\VectF{A}{1}", r"\;=\;(1,\ 2,\ 1,)", tex_template=myTemplate, font_size=48)
        col = MathTex(r"\VectC{A}{1}", r"\;=\;\begin{pmatrix}1\\ 7\end{pmatrix}", tex_template=myTemplate, font_size=48)
        for linea, y in [(comp, 0.3), (fila, -1.1), (col, -2.8)]:   # hueco para la fila en vertical
            linea.move_to([x0 + linea.width/2, y, 0])
        for linea in (fila, col):   # el "=" que sigue al selector, alineado con el de la componente
            linea.shift((comp[1].get_left()[0] - linea[1].get_left()[0])*RIGHT)
        r_hab = Tex(tr("lo habitual", "the usual way"), font_size=28, color=GRAY_B).next_to(comp[2], UP, buff=0.2)
        r_sel = Tex(tr("selector", "selector"), font_size=28, color=GRAY_B).next_to(comp[0], UP, buff=0.2)
        # glifos: a_{21} = a, 2, 1; 2|A|1 = 2, |, A, |, 1
        sub_f, sub_c = comp[2][1], comp[2][2]
        sel_i, sel_d = comp[0][0:2], comp[0][3:5]
        # la fila y la columna, primero con un índice genérico (i, j) que pasa a ser 1 en el ejemplo
        fila_g = MathTex(r"\VectF{A}{i}", tex_template=myTemplate, font_size=48)
        fila_g.shift(fila[0][2].get_center() - fila_g[0][2].get_center())   # glifos: i, |, A
        col_g = MathTex(r"\VectC{A}{j}", tex_template=myTemplate, font_size=48)
        col_g.shift(col[0][0].get_center() - col_g[0][0].get_center())       # glifos: A, |, j
        # la otra forma de escribir la fila y la columna, detrás de un "=" (Marcos, 2026-10-27)
        fila_v = MathTex(r"=\begin{pmatrix}1\\ 2\\ 1\end{pmatrix}", font_size=48).next_to(fila, RIGHT, buff=0.25)
        col_h = MathTex(r"=(1,\ 7,)", font_size=48).next_to(col, RIGHT, buff=0.25)
        
        with self.voiceover(text=tr("""Para seleccionar una componente de un vector, el operador selector necesita un índice. En una matriz necesita dos: <bookmark mark='f'/> el de la fila <bookmark mark='c'/> y el de la columna.""",
                                    """To select a component of a vector, the selector operator needs one index. In a matrix it needs two: <bookmark mark='f'/> the row index <bookmark mark='c'/> and the column index.""")) as tracker:
            self.play(Write(cabecera), FadeIn(f_A), run_time=1)
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 1)
            self.play(FadeIn(ff), run_time=0.5)
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0)
            self.play(FadeIn(fc), run_time=0.5)
            self.play(Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
        
        with self.voiceover(text=tr("""Lo habitual es escribir la componente con la letra de la matriz en minúscula y dos subíndices: <bookmark mark='i'/> primero el de la fila <bookmark mark='j'/> y después el de la columna.""",
                                    """The usual way is to write the component with the letter of the matrix in lower case and two subscripts: <bookmark mark='i'/> first the row <bookmark mark='j'/> and then the column.""")) as tracker:
            self.play(FadeIn(comp[2:]), FadeIn(r_hab), run_time=1)
            self.wait_until_bookmark("i")
            self.play(Indicate(sub_f, color=COLOR_ESCALAR, scale_factor=1.8), run_time=0.8)
            self.wait_until_bookmark("j")
            self.play(Indicate(sub_c, color=COLOR_ESCALAR, scale_factor=1.8), run_time=0.8)
        
        with self.voiceover(text=tr("""Pero en este curso, como con los vectores, usaremos principalmente el operador selector, <bookmark mark='s'/> con el índice de la fila a la izquierda de la matriz <bookmark mark='d'/> y el de la columna a la derecha.""",
                                    """But in this course, as with vectors, we will mainly use the selector operator, <bookmark mark='s'/> with the row index on the left of the matrix <bookmark mark='d'/> and the column index on the right.""")) as tracker:
            self.play(FadeIn(comp[:2]), FadeIn(r_sel), run_time=1)
            self.wait_until_bookmark("s")
            self.play(Indicate(sel_i, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("d")
            self.play(Indicate(sel_d, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
        
        # el símbolo aparece un instante antes de que la voz lo describa (Marcos, 2026-10-18)
        self.play(FadeOut(ff), FadeOut(fc), FadeIn(fila_g), run_time=0.6)
        with self.voiceover(text=tr("""Si el operador actúa solo por la izquierda, selecciona una fila: la que indica el índice. <bookmark mark='e'/> Por ejemplo, con el índice uno, <bookmark mark='f'/> selecciona la primera fila de A, que es un vector.""",
                                    """If the operator acts only on the left, it selects a row: the one given by the index. <bookmark mark='e'/> For example, with index one, <bookmark mark='f'/> it selects the first row of A, which is a vector.""")) as tracker:
            self.play(Indicate(fila_g[0][0:2], color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("e")
            self.play(ReplacementTransform(fila_g, fila[0]), run_time=0.8)   # i pasa a ser 1
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 0)
            self.play(FadeIn(ff), FadeIn(fila[1]), run_time=0.8)
        
        self.play(FadeOut(ff), FadeIn(col_g), run_time=0.6)
        with self.voiceover(text=tr("""Y si actúa solo por la derecha, selecciona una columna. <bookmark mark='e'/> Por ejemplo, con el índice uno, <bookmark mark='c'/> selecciona la primera columna de A, que también es un vector.""",
                                    """And if it acts only on the right, it selects a column. <bookmark mark='e'/> For example, with index one, <bookmark mark='c'/> it selects the first column of A, which is also a vector.""")) as tracker:
            self.play(Indicate(col_g[0][1:3], color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("e")
            self.play(ReplacementTransform(col_g, col[0]), run_time=0.8)   # j pasa a ser 1
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0)
            self.play(FadeIn(fc), FadeIn(col[1]), run_time=0.8)
        
        self.wait(0.6)   # una pausa antes de la conclusión (Marcos, 2026-10-27)
        with self.voiceover(text=tr("""Filas y columnas son vectores, y por eso las podemos escribir indistintamente en horizontal <bookmark mark='h'/> o en vertical, <bookmark mark='p'/> con sus listas de números siempre entre paréntesis.""",
                                    """Rows and columns are vectors, so we can write them either horizontally <bookmark mark='h'/> or vertically, <bookmark mark='p'/> with their lists of numbers always in parentheses.""")) as tracker:
            self.play(FadeOut(fc), run_time=0.5)
            self.wait_until_bookmark("h")
            self.play(FadeIn(fila_v), FadeIn(col_h), run_time=1)
            self.wait_until_bookmark("p")
            self.play(*[Indicate(m, color=COLOR_ESCALAR, scale_factor=1.1) for m in (fila[1], col[1], fila_v, col_h)], run_time=1.2)
        
        self.pausa_media()


class L01_V09_E07_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        defin = Tex(tr(r"Matriz de ", r"Matrix in "), r"$\R[m\times n]$", tr(r": ", r": an "), tr(r"lista ordenada", r"ordered list"), tr(r" de ", r" of "),
                    r"$n$", tr(r" vectores de ", r" vectors in "), r"$\R[m]$", tr(r"\\ (sus columnas), entre corchetes.", r"\\ (its columns), in square brackets."),
                    tex_template=myTemplate, font_size=34)
        orden = Tex(tr(r"Orden ", r"Order "), r"$m\times n$", tr(r": primero las filas, después las columnas.", r": rows first, then columns."),
                    tex_template=myTemplate, font_size=34)
        # glifos: orden[1] = m, ×, n
        encabezados = [tr("fila $i$", "row $i$"), tr("componente $ij$", "component $ij$"), tr("columna $j$", "column $j$")]
        formulas = [r"\VectF{A}{i}\in\R[n]", r"\eleM{A}{i}{j}=a_{ij}", r"\VectC{A}{j}\in\R[m]"]
        tabla = VGroup(*[VGroup(Tex(e, tex_template=myTemplate, font_size=32, color=GRAY_B), MathTex(f, tex_template=myTemplate, font_size=44)).arrange(DOWN, buff=0.3)
                         for e, f in zip(encabezados, formulas)]).arrange(RIGHT, buff=1.2)
        bloque = VGroup(defin, orden, tabla).arrange(DOWN, buff=0.6).next_to(cabecera, DOWN, buff=0.7)
        
        # señales en la definición (Marcos, 2026-10-27): un efecto cada vez, cuando la voz lo nombra
        with self.voiceover(text=tr("""Resumamos. Una matriz es una <bookmark mark='l'/> lista ordenada <bookmark mark='n'/> de vectores <bookmark mark='m'/> con el mismo número de componentes; dichos vectores son las columnas de la matriz. La lista de vectores se escribe entre corchetes. <bookmark mark='o'/> Su orden indica <bookmark mark='f'/> el número de filas primero <bookmark mark='c'/> y el número de columnas después.""",
                                    """Let us sum up. A matrix is an <bookmark mark='l'/> ordered list <bookmark mark='n'/> of vectors <bookmark mark='m'/> with the same number of components; these vectors are the columns of the matrix. The list of vectors is written in square brackets. <bookmark mark='o'/> Its order gives <bookmark mark='f'/> the number of rows first <bookmark mark='c'/> and the number of columns second.""")) as tracker:
            self.play(Write(cabecera), FadeIn(defin), run_time=1)
            self.wait_until_bookmark("l")
            self.play(Circumscribe(defin[3], color=COLOR_ESCALAR, buff=0.08), run_time=1)
            # (los Indicate de m y n en la definición se quitaron: no daban el efecto buscado; Marcos, 2026-10-27)
            self.wait_until_bookmark("o")
            self.play(FadeIn(orden), run_time=0.8)
            self.wait_until_bookmark("f")
            self.play(Indicate(orden[1][0], color=COLOR_FILA, scale_factor=1.8), run_time=1)
            self.wait_until_bookmark("c")
            self.play(Indicate(orden[1][2], color=COLOR_COLUMNA, scale_factor=1.8), run_time=1)
        
        # el operador se destaca cuando la voz dice por qué lado actúa (Marcos, 2026-10-27)
        # glifos: tabla[0][1] = i, |, A, ...;  tabla[1][1] = i, |, A, |, j, ...;  tabla[2][1] = A, |, j, ...
        sel_fila, sel_col = tabla[0][1][0][0:2], tabla[2][1][0][1:3]
        sel_comp = [tabla[1][1][0][0:2], tabla[1][1][0][3:5]]
        with self.voiceover(text=tr("""Con el operador selector actuando <bookmark mark='i'/> por la izquierda, seleccionamos una fila. <bookmark mark='c'/> Con el operador selector actuando <bookmark mark='d'/> por la derecha, una columna. <bookmark mark='e'/> Y con el operador selector actuando <bookmark mark='a'/> por ambos lados, seleccionamos una componente.""",
                                    """With the selector operator acting <bookmark mark='i'/> on the left, we select a row. <bookmark mark='c'/> With the selector operator acting <bookmark mark='d'/> on the right, a column. <bookmark mark='e'/> And with the selector operator acting <bookmark mark='a'/> on both sides, we select a component.<bookmark mark='v3'/>""")) as tracker:
            self.play(FadeIn(tabla[0]), run_time=0.8)
            self.wait_until_bookmark("i")
            self.play(Indicate(sel_fila, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("c")
            self.play(FadeIn(tabla[2]), run_time=0.8)
            self.wait_until_bookmark("d")
            self.play(Indicate(sel_col, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("e")
            self.play(FadeIn(tabla[1]), run_time=0.8)
            self.wait_until_bookmark("a")
            self.play(*[Indicate(g, color=COLOR_ESCALAR, scale_factor=1.6) for g in sel_comp], run_time=0.9)
        
        self.wait(0.5)   # una pausa antes de anunciar el próximo vídeo, como en V08
        with self.voiceover(text=tr("""En el próximo vídeo veremos que, para seleccionar una componente de una matriz, da igual empezar por la fila o por la columna. También veremos la transposición, que convierte las filas de una matriz en columnas, como hicimos al formar la matriz B.<bookmark mark='w3'/>""",
                                    """In the next video we will see that, to select a component of a matrix, it makes no difference whether we start with the row or with the column. We will also meet transposition, which turns the rows of a matrix into columns, as we did when we built the matrix B.<bookmark mark='v2'/>""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
