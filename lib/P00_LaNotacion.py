from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Otra notación para el álgebra lineal", "A different notation for linear algebra")
A_EJ = r"\begin{bmatrix}1&3\\2&4\end{bmatrix}"          # la matriz de los ejemplos de la introducción
COLOR_FILA, COLOR_COLUMNA = YELLOW, GREEN

# La asociatividad con sumatorios (introducción del libro) y con el selector
SUMAS = (r"\big[A(BC)\big]_{ij}=\sum_{k}a_{ik}\Big(\sum_{l}b_{kl}c_{lj}\Big)=\sum_{k}\sum_{l}a_{ik}b_{kl}c_{lj}"
         r"=\sum_{l}\Big(\sum_{k}a_{ik}b_{kl}\Big)c_{lj}=\big[(AB)C\big]_{ij}")
CADENA = [r"\elemR{\Big(\Mat{A}\big(\Mat{BC}\big)\Big)}{j}", r"=\Mat{A}\Big(\elemR{\big(\Mat{BC}\big)}{j}\Big)",
          r"=\Mat{A}\Big(\Mat{B}\big(\VectC{C}{j}\big)\Big)", r"=\Big(\MN{A}{B}\Big)\big(\VectC{C}{j}\big)",
          r"=\elemR{\Big(\big(\MN{A}{B}\big)\Mat{C}\Big)}{j}"]
REGLAS = [tr("definición del producto", "definition of the product"), tr("definición del producto", "definition of the product"),
          tr("propiedad del producto matriz por vector", "property of the matrix-vector product"),
          tr("definición del producto", "definition of the product")]


class EscenaP00(MiEscenaConVoz):
    """Ritmo sosegado (Marcos, 2026-11-15): tras cada locución, una pausa para asimilar lo visto y lo oído.
    pausa=1.2 por defecto; las ideas principales llevan pausa=2.5 en su voiceover."""
    @contextmanager
    def voiceover(self, text=None, pausa=1.2, **kwargs):
        with super().voiceover(text=text, **kwargs) as tracker:
            yield tracker
        self.wait(pausa)


def mat(filas, fs=32):
    """Matriz numérica entre corchetes, con acceso a filas, columnas y componentes para resaltarlas."""
    m = Matrix(filas, v_buff=0.55, h_buff=0.9, bracket_h_buff=0.12, bracket_v_buff=0.12, element_to_mobject=lambda x: MathTex(str(x)))
    return m.scale(fs/48)


def pinta(escena, color, *mobs, run_time=0.5):
    """Resaltado sostenido: lo que la voz nombra cambia de color."""
    escena.play(*[m.animate.set_color(color) for m in mobs], run_time=run_time)


def orden(mob, texto, fs=26, color=GRAY_B, buff=0.25):
    """El orden de una matriz, escrito debajo de ella."""
    return MathTex(texto, font_size=fs).set_color(color).next_to(mob, DOWN, buff=buff)


def M(formula, fs=36, color=None):
    m = MathTex(formula, tex_template=myTemplate, font_size=fs)
    return m.set_color(color) if color else m


def T(es, en=None, fs=30, color=WHITE):
    return Tex(tr(es, en if en is not None else es), tex_template=myTemplate, font_size=fs).set_color(color)


def cabecera(es, en):
    return T(es, en, 40, COLOR_TITULO).to_edge(UP, buff=0.3)


def cita(lineas, fuente, fs=30):
    """Una cita (lista de líneas) en cursiva, con su fuente debajo, a la derecha."""
    texto = VGroup(*[Tex(r"\emph{" + l + "}", tex_template=myTemplate, font_size=fs) for l in lineas]).arrange(DOWN, buff=0.15)
    autor = Tex(fuente, tex_template=myTemplate, font_size=fs - 6).set_color(GRAY_B)
    return VGroup(texto, autor).arrange(DOWN, buff=0.25, aligned_edge=RIGHT)


def coste(es, en):
    """El coste de la decisión, al pie de la escena."""
    r = T(r"\textbf{Coste:} " + es, r"\textbf{Cost:} " + en, 30, COLOR_ESCALAR)
    marco = RoundedRectangle(corner_radius=0.15, width=r.width + 0.5, height=r.height + 0.35, stroke_color=COLOR_ESCALAR, stroke_width=2)
    return VGroup(marco, r).to_edge(DOWN, buff=0.35)


def en_marca(escena, marca, *mobs, run_time=0.8, anim=FadeIn):
    """Al llegar la voz a la marca, aparecen los objetos."""
    escena.wait_until_bookmark(marca)
    escena.play(*[anim(m) for m in mobs], run_time=run_time)


def limpia(escena, *mobs, run_time=0.6):
    escena.play(*[FadeOut(m) for m in mobs], run_time=run_time)


def columna(mobs, x, y_sup, salto, alineado=LEFT):
    for k, m in enumerate(mobs):
        m.move_to([0, y_sup - k*salto, 0]).align_to([x, 0, 0], alineado)
    return VGroup(*mobs)


def cadena_asociativa(fs=34, x=-4.6, y_sup=1.2, salto=0.85, x_regla=0.4):
    lineas = [M(f, fs) for f in CADENA]
    for k, l in enumerate(lineas):
        l.move_to([0, y_sup - k*salto, 0]).align_to([x + (0.6 if k else 0), 0, 0], LEFT)
    reglas = [T(r, r, 24, COLOR_REGLA).move_to([0, l.get_y(), 0]).align_to([x_regla, 0, 0], LEFT) for r, l in zip(REGLAS, lineas[1:])]
    return lineas, reglas


def nace(escena, origen, destino, fijos, moviles=(), aparecen=(), extra=(), marca=None, t_fijos=0.7, t_moviles=0.9):
    """Una expresión nace de la anterior (como en V13 y V14): primero se copia lo que no cambia y aparece el
    igual; después, en la marca, viaja lo que el paso mueve. origen y destino son listas de glifos."""
    cubiertos = sorted({j for _, j in fijos} | {j for _, j in moviles} | set(aparecen) | {0})
    assert cubiertos == list(range(len(destino))), (cubiertos, len(destino))
    escena.play(*extra, FadeIn(destino[0]), *[TransformFromCopy(origen[i], destino[j]) for i, j in fijos], run_time=t_fijos)
    if marca is not None:
        escena.wait_until_bookmark(marca)
    escena.play(*[TransformFromCopy(origen[i], destino[j]) for i, j in moviles], *[FadeIn(destino[j]) for j in aparecen], run_time=t_moviles)

class P00_E00_Portada(EscenaP00):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=56).set_color(COLOR_TITULO)
        sub = T("Las razones y el coste", "The reasons and the cost", 40)
        para = T("Para quien ya enseña álgebra lineal", "For those who already teach linear algebra", 28, GRAY_B)
        g = VGroup(portada, sub, para).arrange(DOWN, buff=0.5)
        self.play(FadeIn(g, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class P00_E01_Resultado(EscenaP00):
    def construct(self):
        self.creditos()
        titulo = Tex(TITULO, tex_template=myTemplate, font_size=40).set_color(COLOR_TITULO).to_edge(UP, buff=0.3)
        sumas = M(SUMAS, 26); sumas.scale_to_fit_width(12.6).move_to([0, 2.35, 0])
        citas = columna([T(r"Strang, p. 73: \emph{``The direct proof is sort of awkward''}", None, 28),
                         T(r"Poole, p. 214: composición de transformaciones lineales", r"Poole: composition of linear transformations", 28),
                         T(r"Larson, p. 62: ejercicio", r"Larson: left as an exercise", 28)], -4.6, 0.6, 0.7)
        lineas, reglas = cadena_asociativa(fs=32, y_sup=1.25, salto=0.78)
        cuenta = VGroup(T(r"dos sumatorios", r"two summations", 28, COLOR_ESCALAR), T(r"cuatro índices: $i,\ j,\ k,\ l$", r"four indices: $i,\ j,\ k,\ l$", 28, COLOR_ESCALAR),
                        T(r"intercambiar $\sum_k\sum_l$ por $\sum_l\sum_k$", r"exchange $\sum_k\sum_l$ for $\sum_l\sum_k$", 28, COLOR_ESCALAR)).arrange(RIGHT, buff=0.9).next_to(sumas, DOWN, buff=0.35)
        pregunta = T("Las decisiones, lo que resuelven y lo que cuestan", "The decisions, what they solve and what they cost", 32, COLOR_ESCALAR).to_edge(DOWN, buff=0.4)
        
        with self.voiceover(text=tr("""Este vídeo está dirigido a quien ya conoce el álgebra lineal, y en particular a quien la enseña. Presenta la notación del libro Curso de Álgebra Lineal y las razones que la sostienen.""",
                                    """This video is for those who already know linear algebra, and in particular for those who teach it. It presents the notation of the book Curso de Álgebra Lineal and the reasons behind it.""")) as tracker:
            self.play(Write(titulo), run_time=1.5)
        
        with self.voiceover(text=tr("""Empecemos por una propiedad que todos enseñamos: el producto de matrices es asociativo. <bookmark mark='d'/> Esta es la demostración por componentes. Necesita <bookmark mark='s'/> dos sumatorios <bookmark mark='i'/> y cuatro índices, y hay que <bookmark mark='o'/> intercambiar el orden de las sumas.""",
                                    """Let us start with a property we all teach: matrix multiplication is associative. <bookmark mark='d'/> This is the proof by components. It needs <bookmark mark='s'/> two summations <bookmark mark='i'/> and four indices, and <bookmark mark='o'/> the order of the sums has to be exchanged.""")) as tracker:
            en_marca(self, "d", sumas, run_time=1.2)
            for m, r in zip("sio", cuenta):
                en_marca(self, m, r, run_time=0.5)
        
        with self.voiceover(text=tr("""Varios manuales excelentes la evitan. <bookmark mark='s'/> Strang dice que la demostración directa es algo incómoda. <bookmark mark='p'/> Poole la sustituye por la composición de transformaciones lineales. <bookmark mark='l'/> Y el manual de Larson la deja como ejercicio.""",
                                    """Several excellent textbooks avoid it. <bookmark mark='s'/> Strang says the direct proof is sort of awkward. <bookmark mark='p'/> Poole replaces it with the composition of linear transformations. <bookmark mark='l'/> And Larson's textbook leaves it as an exercise.""")) as tracker:
            for m, c in zip("spl", citas):
                en_marca(self, m, c, run_time=0.6)
        
        with self.voiceover(pausa=2.5, text=tr("""<bookmark mark='n'/> Esta es la misma demostración con la notación del libro. Son cuatro igualdades. <bookmark mark='r'/> Cada una aplica una regla que tiene nombre, y no aparece ningún índice de suma.""",
                                    """<bookmark mark='n'/> This is the same proof in the notation of the book. There are four equalities. <bookmark mark='r'/> Each one applies a rule that has a name, and no summation index appears.""")) as tracker:
            self.play(FadeOut(citas), FadeOut(cuenta), run_time=0.5)
            self.play(FadeIn(lineas[0]), run_time=0.6)
            for l in lineas[1:]:
                self.play(FadeIn(l), run_time=0.7)
            self.wait_until_bookmark("r")
            for r in reglas:
                self.play(FadeIn(r), run_time=0.5)
        
        with self.voiceover(pausa=2.5, text=tr("""Escribir así exige una notación distinta de la habitual, y aprenderla tiene un coste. <bookmark mark='q'/> En este vídeo veremos las decisiones que hay detrás de esa notación, lo que resuelve cada una y el coste de adoptarla.""",
                                    """Writing like this requires a notation different from the usual one, and learning it has a cost. <bookmark mark='q'/> In this video we will see the decisions behind that notation, what each one solves, and the cost of adopting it.""")) as tracker:
            en_marca(self, "q", pregunta)
        
        self.pausa_media()


class P00_E02_Comodidad(EscenaP00):
    def construct(self):
        self.creditos()
        cab = cabecera("La comodidad de la notación habitual", "Why the usual notation is convenient")
        ig = lambda: M("=", 36)
        A1, e2, r1 = mat([[1, 3], [2, 4]]), mat([[0], [1]]), mat([[3], [4]])
        f1, A2, e2b, r2 = mat([[1, 0]]), mat([[1, 3], [2, 4]]), mat([[0], [1]]), mat([[3]])
        E, A3, R = mat([[1, 0], [-2, 1]]), mat([[1, 3], [2, 4]]), mat([[1, 3], [0, -2]])
        u, v, r3 = mat([[1, 1]]), mat([[2], [1]]), mat([[3]])
        ejs = columna([VGroup(A1, e2, ig(), r1).arrange(RIGHT, buff=0.15), VGroup(f1, A2, e2b, ig(), r2).arrange(RIGHT, buff=0.15),
                       VGroup(E, A3, ig(), R).arrange(RIGHT, buff=0.15), VGroup(u, v, ig(), r3).arrange(RIGHT, buff=0.15)], -6.2, 2.0, 1.2)
        notas = [T(e, i, 28, c).move_to([0, ej.get_y(), 0]).align_to([-0.6, 0, 0], LEFT) for (e, i, c), ej in zip(
            [("selecciona la columna 2", "selects column 2", COLOR_COLUMNA), ("selecciona la componente de la fila 1 y la columna 2", "selects the component in row 1, column 2", COLOR_COLUMNA),
             ("resta a la fila 2 el doble de la fila 1", "subtracts twice row 1 from row 2", COLOR_COLUMNA), (r"producto punto: $1\cdot 2+1\cdot 1$", r"dot product: $1\cdot 2+1\cdot 1$", COLOR_COLUMNA)], ejs)]
        asoc = M(r"(\Mat{A}\Mat{B})\Mat{E}=\Mat{A}(\Mat{B}\Mat{E})", 44).move_to([-3.6, -2.9, 0])
        lectura = T(r"columna de $\Mat{AB}$ = $\Mat{A}$ por columna de $\Mat{B}$", r"column of $\Mat{AB}$ = $\Mat{A}$ times column of $\Mat{B}$", 28, GRAY_B).next_to(asoc, RIGHT, buff=0.7)
        matlab = T(r"Matlab = \emph{Matrix Laboratory}: todo es una matriz", r"Matlab = \emph{Matrix Laboratory}: everything is a matrix", 30, COLOR_ESCALAR).next_to(asoc, RIGHT, buff=0.7)
        
        with self.voiceover(text=tr("""La notación habitual tiene una gran virtud: casi todo se puede escribir como un producto de matrices. Veamos tres ejemplos.""",
                                    """The usual notation has a great virtue: almost everything can be written as a product of matrices. Let us see three examples.""")) as tracker:
            self.play(Write(cab), run_time=1)
        
        with self.voiceover(text=tr("""Para seleccionar <bookmark mark='a'/> una columna de una matriz, la multiplicamos por una columna de la matriz identidad. Si además multiplicamos por la izquierda <bookmark mark='b'/> por una fila de la identidad, obtenemos una componente.""",
                                    """To select <bookmark mark='a'/> a column of a matrix, we multiply it by a column of the identity matrix. If we also multiply on the left <bookmark mark='b'/> by a row of the identity, we get a component.""")) as tracker:
            en_marca(self, "a", ejs[0])
            pinta(self, COLOR_ESCALAR, e2.get_entries())
            pinta(self, COLOR_COLUMNA, A1.get_columns()[1], r1.get_entries())
            self.play(FadeIn(notas[0]), run_time=0.5)
            en_marca(self, "b", ejs[1])
            pinta(self, COLOR_ESCALAR, f1.get_entries(), e2b.get_entries())
            pinta(self, COLOR_COLUMNA, A2.get_rows()[0][1], r2.get_entries())
            self.play(FadeIn(notas[1]), run_time=0.5)
        
        with self.voiceover(text=tr("""Para restar a la segunda fila el doble de la primera, <bookmark mark='c'/> multiplicamos por una matriz elemental.""",
                                    """To subtract twice the first row from the second, <bookmark mark='c'/> we multiply by an elementary matrix.""")) as tracker:
            en_marca(self, "c", ejs[2])
            pinta(self, COLOR_ESCALAR, E.get_rows()[1])
            pinta(self, COLOR_COLUMNA, R.get_rows()[1])
            self.play(FadeIn(notas[2]), run_time=0.5)
        
        with self.voiceover(text=tr("""Y el producto punto de dos vectores <bookmark mark='d'/> se escribe como una fila por una columna.""",
                                    """And the dot product of two vectors <bookmark mark='d'/> is written as a row times a column.""")) as tracker:
            en_marca(self, "d", ejs[3])
            pinta(self, COLOR_COLUMNA, r3.get_entries())
            self.play(FadeIn(notas[3]), run_time=0.5)
        
        with self.voiceover(pausa=2.5, text=tr("""El producto de matrices es asociativo, así que en estas expresiones sobran los paréntesis. <bookmark mark='e'/> Esta igualdad, por ejemplo, dice que cada columna de un producto es la primera matriz por la columna correspondiente de la segunda. No hace falta demostrarlo aparte: basta la asociatividad.""",
                                    """Matrix multiplication is associative, so in these expressions the parentheses are unnecessary. <bookmark mark='e'/> This equality, for example, says that each column of a product is the first matrix times the corresponding column of the second. It needs no separate proof: associativity is enough.""")) as tracker:
            en_marca(self, "e", asoc)
            self.play(FadeIn(lectura), run_time=0.8)
        
        with self.voiceover(pausa=2.0, text=tr("""Es el planteamiento <bookmark mark='m'/> de Matlab. Si todos los objetos son matrices, basta una operación, y las expresiones se escriben sin paréntesis.""",
                                    """This is the approach <bookmark mark='m'/> of Matlab. If every object is a matrix, one operation is enough, and expressions are written without parentheses.""")) as tracker:
            self.wait_until_bookmark("m")
            self.play(FadeOut(lectura), FadeIn(matlab), run_time=0.8)


class P00_E03_Precio(EscenaP00):
    def construct(self):
        self.creditos()
        cab = cabecera("El precio: todo acaba siendo una matriz", "The price: everything ends up being a matrix")
        # dos resultados de la escena anterior, con su orden debajo: la columna (debería ser un vector) y la de orden 1 (debería
        # ser un número). Antes eran tres, con dos [3] iguales que no se sabía de dónde venían (Marcos, 2026-11-23)
        r1, r2 = mat([[3], [4]], 36), mat([[3]], 36)
        res = VGroup(r1, r2).arrange(RIGHT, buff=1.6).move_to([-2.2, 1.9, 0])
        ords = VGroup(orden(r1, r"2\times 1"), orden(r2, r"1\times 1"))
        for o in ords:
            o.set_y(ords[0].get_y())
        res_rot = T("dos matrices: ni un vector, ni un número", "two matrices: not a vector, not a number", 30, COLOR_ESCALAR).next_to(res, RIGHT, buff=0.9)
        tipos = T(r"Enseñamos tres tipos de objetos: \quad número \quad vector \quad matriz", r"We teach three kinds of objects: \quad number \quad vector \quad matrix", 32).move_to([0, 0.1, 0])
        ident = columna([T(r"matriz con una fila o una columna $\;\longrightarrow\;$ se trata como un vector", r"matrix with one row or one column $\;\longrightarrow\;$ treated as a vector", 32),
                         T(r"matriz de orden 1 $\;\longrightarrow\;$ se trata como un número", r"matrix of order 1 $\;\longrightarrow\;$ treated as a number", 32)], -5.2, -1.2, 0.85)
        strang = cita([r"``The row vector $[\,1\ \,1\ -1\,]$ is absolutely different,", r"even though it has the same three components.''"], "Strang, p. 4", 32).move_to([-1.6, 1.6, 0])
        filacol = VGroup(mat([[1, 1, -1]], 30), M(r"\ne", 40), mat([[1], [1], [-1]], 30)).arrange(RIGHT, buff=0.3).next_to(strang, RIGHT, buff=0.7)
        poole = cita(tr([r"``Técnicamente, existe una distinción entre matrices renglón/columna", r"y vectores, pero no abundaremos en esta distinción.''"],
                        [r"A footnote: row and column matrices are, technically,", r"distinct from vectors; the distinction is not pursued."]),
                     tr("Poole, p. 134, nota al pie", "Poole, footnote (paraphrased)"), 32).move_to([0, -1.3, 0])
        preguntas = columna([T(r"¿Qué más determina un vector?", r"What else determines a vector?", 36, COLOR_ESCALAR),
                             T(r"¿Un vector es una fila o una columna?", r"Is a vector a row or a column?", 36, COLOR_ESCALAR),
                             T(r"En $\boldsymbol{y}^{T}\!A$, ¿$\boldsymbol{y}$ es un vector o una matriz?", r"In $\boldsymbol{y}^{T}\!A$, is $\boldsymbol{y}$ a vector or a matrix?", 36, COLOR_ESCALAR),
                             T(r"¿Una matriz es una tabla de matrices de orden 1?", r"Is a matrix an array of matrices of order 1?", 36, COLOR_ESCALAR)], -4.2, 1.7, 0.95)
        
        # La proyección de Strang (p. 209), con el orden de cada factor debajo
        aT, b, a = r"\boldsymbol{a}^{T}", r"\boldsymbol{b}", r"\boldsymbol{a}"
        f1 = MathTex(r"\boldsymbol{p}=", r"\frac{" + aT + b + "}{" + aT + a + "}", r"\," + a, font_size=38).move_to([-3.7, 2.1, 0])
        f2 = MathTex(r"\boldsymbol{p}=" + a + r"\,", r"\frac{" + aT + b + "}{" + aT + a + "}", r"=P" + b + r",\quad P=\frac{" + a + aT + "}{" + aT + a + "}", font_size=38).move_to([3.0, 2.1, 0])
        fuente = T("Strang, p. 209", None, 24, GRAY_B).to_edge(UP, buff=0.95)
        # cada orden centrado bajo su factor (Marcos, 2026-11-23: antes se desplazaban hacia los paréntesis); para que no se
        # solapen, un poco de espacio entre los factores
        s1 = MathTex(r"\big(", aT, r"\;\;" + b, r"\big)", r"\;" + a, font_size=60).move_to([-3.7, 0.2, 0])
        o_aT, o_b = orden(s1[1], r"1\times n", 28), orden(s1[2], r"n\times 1", 28)
        o_aT.set_y(min(o_aT.get_y(), o_b.get_y())); o_b.set_y(o_aT.get_y())
        llave1 = Brace(VGroup(s1[0], s1[3]), DOWN, buff=0.75)
        o_p = MathTex(r"1\times 1", font_size=30).next_to(llave1, DOWN, buff=0.1)
        o_a = MathTex(r"n\times 1", font_size=30).move_to([s1[4].get_x(), o_p.get_y(), 0])
        mal = T(r"$(1\times 1)(n\times 1)$: los órdenes no encajan", r"$(1\times 1)(n\times 1)$: the orders do not match", 28, RED).move_to([-3.7, -2.0, 0])
        num = T(r"aquí $" + aT + b + r"$ tiene que ser un \textbf{número}", r"here $" + aT + b + r"$ has to be a \textbf{number}", 30, COLOR_ESCALAR).next_to(mal, DOWN, buff=0.3)
        s2 = MathTex(a, r"\;\big(", aT, b, r"\big)", "=", r"\big(", a, aT, r"\big)", r"\;" + b, font_size=60).move_to([3.1, 0.2, 0])
        llave2 = Brace(VGroup(s2[1], s2[4]), DOWN, buff=0.3)
        p_a = orden(s2[0], r"n\times 1", 28); p_p = MathTex(r"1\times 1", font_size=28).next_to(llave2, DOWN, buff=0.1)
        p_a.set_y(p_p.get_y())
        llave3 = Brace(VGroup(s2[6], s2[9]), DOWN, buff=0.3)
        p_n = MathTex(r"n\times n", font_size=28).next_to(llave3, DOWN, buff=0.1)
        p_b = MathTex(r"n\times 1", font_size=28).move_to([s2[10].get_x(), p_n.get_y(), 0])
        bien = T(r"los órdenes encajan; se reagrupa por la asociatividad", r"the orders match; regrouped by associativity", 28, GREEN).move_to([3.1, -2.0, 0])
        matz = T(r"aquí $" + aT + b + r"$ tiene que ser una \textbf{matriz}", r"here $" + aT + b + r"$ has to be a \textbf{matrix}", 30, COLOR_ESCALAR).next_to(bien, DOWN, buff=0.3)
        polya = cita([r"``It is inadmissible that the same symbol denote", r"two different objects in the same inquiry.''"], r"Polya, \emph{How to Solve It}, p. 136", 34).move_to([0, 0.3, 0])
        ctx = columna([T("El estudiante aún no tiene el contexto", "The student does not have the context yet", 32), T("Un programa no decide por el contexto", "A program cannot decide from the context", 32)], -3.4, -1.9, 0.75)
        
        # la primera locución es un trozo de la toma anterior; la segunda, nueva (tirada 1)
        with self.voiceover(pausa=0.4, text=tr("""Esa comodidad tiene un precio. El producto de dos matrices siempre es una matriz.""",
                                    """That convenience has a price. The product of two matrices is always a matrix.""")) as tracker:
            self.play(Write(cab), run_time=1)
        
        with self.voiceover(pausa=2.5, text=tr("""Por tanto, estos resultados son matrices: <bookmark mark='a'/> una matriz con una sola columna <bookmark mark='b'/> y una matriz de orden uno. <bookmark mark='n'/> La primera no es un vector, y la segunda no es un número.""",
                                    """So these results are matrices: <bookmark mark='a'/> a matrix with a single column <bookmark mark='b'/> and a matrix of order one. <bookmark mark='n'/> The first is not a vector, and the second is not a number.""")) as tracker:
            self.play(FadeIn(res), run_time=0.8)
            en_marca(self, "a", ords[0], run_time=0.5)
            en_marca(self, "b", ords[1], run_time=0.5)
            en_marca(self, "n", res_rot)
        
        with self.voiceover(text=tr("""Sin embargo, enseñamos que hay <bookmark mark='t'/> tres tipos de objetos: números, vectores y matrices. El producto punto de dos vectores es un número, y el producto de una matriz por un vector es un vector.""",
                                    """Yet we teach that there are <bookmark mark='t'/> three kinds of objects: numbers, vectors and matrices. The dot product of two vectors is a number, and the product of a matrix and a vector is a vector.""")) as tracker:
            en_marca(self, "t", tipos)
        
        with self.voiceover(pausa=2.5, text=tr("""La notación habitual salva la diferencia con dos identificaciones. <bookmark mark='a'/> Una matriz con una sola fila o una sola columna se trata como un vector. <bookmark mark='b'/> Y una matriz de orden uno se trata como un número.""",
                                    """The usual notation bridges the gap with two identifications. <bookmark mark='a'/> A matrix with a single row or a single column is treated as a vector. <bookmark mark='b'/> And a matrix of order one is treated as a number.""")) as tracker:
            en_marca(self, "a", ident[0])
            en_marca(self, "b", ident[1])
        
        with self.voiceover(text=tr("""Las encontramos en los mejores manuales. La objeción no va contra ellos, sino contra un convenio que comparten casi todos los textos.""",
                                    """We find them in the best textbooks. The objection is not to those books, but to a convention shared by almost every text.""")) as tracker:
            limpia(self, res, ords, res_rot, tipos, ident)
        
        with self.voiceover(pausa=2.0, text=tr("""<bookmark mark='s'/> Strang escribe que el vector fila es absolutamente diferente del vector columna, aunque tiene las mismas tres componentes. <bookmark mark='p'/> Poole advierte en una nota al pie que, técnicamente, una matriz columna y un vector son cosas distintas, y añade que no entrará en esa distinción.""",
                                    """<bookmark mark='s'/> Strang writes that the row vector is absolutely different from the column vector, even though it has the same three components. <bookmark mark='p'/> Poole warns in a footnote that, technically, a column matrix and a vector are different things, and adds that he will not dwell on that distinction.""")) as tracker:
            self.play(FadeIn(strang), FadeIn(filacol), run_time=0.8)
            en_marca(self, "p", poole)
        
        # la última pregunta va en una locución propia, en forma de pregunta (Marcos, 2026-11-23: «una matriz sería una tabla
        # de matrices» se entendía mal; tirada A1, que sube al final); lo anterior es un trozo de la toma que había
        with self.voiceover(pausa=0.5, text=tr("""Un estudiante atento puede hacerse entonces varias preguntas. <bookmark mark='a'/> Si dos vectores con las mismas componentes, en el mismo orden, son diferentes, algo más debe determinar un vector. <bookmark mark='b'/> No sabe si un vector es una fila o una columna. <bookmark mark='c'/> Cuando se transpone un vector, no sabe si ese símbolo representa un vector o una matriz.""",
                                    """An attentive student may then ask several questions. <bookmark mark='a'/> If two vectors with the same components, in the same order, are different, something else must determine a vector. <bookmark mark='b'/> The student cannot tell whether a vector is a row or a column. <bookmark mark='c'/> When a vector is transposed, the student cannot tell whether that symbol stands for a vector or a matrix.""")) as tracker:
            limpia(self, strang, filacol, poole)
            for m, q in zip("abc", preguntas):
                en_marca(self, m, q, run_time=0.6)
        
        with self.voiceover(pausa=2.5, text=tr("""Y si los números son matrices de orden uno, ¿una matriz es una tabla de matrices de orden uno?""",
                                    """And if numbers are matrices of order one, is a matrix an array of matrices of order one?""")) as tracker:
            self.play(FadeIn(preguntas[3]), run_time=0.6)
        
        with self.voiceover(text=tr("""Hay un caso en el que el problema aparece dentro de una fórmula. <bookmark mark='a'/> Esta es la proyección de un vector sobre una recta, tal como la escribe Strang.""",
                                    """There is a case where the problem shows up inside a formula. <bookmark mark='a'/> This is the projection of a vector onto a line, as Strang writes it.""")) as tracker:
            limpia(self, preguntas)
            en_marca(self, "a", f1, fuente)
        
        with self.voiceover(pausa=3.0, text=tr("""Veamos los órdenes de los factores del numerador. <bookmark mark='t'/> El primero es una matriz con una sola fila, <bookmark mark='b'/> y el segundo, una matriz con una sola columna, <bookmark mark='p'/> así que su producto es una matriz de orden uno. <bookmark mark='c'/> Pero una matriz de orden uno no se puede multiplicar por una matriz columna: <bookmark mark='x'/> los órdenes no encajan. <bookmark mark='n'/> Para que la fórmula tenga sentido, ese producto tiene que ser un número.""",
                                    """Let us look at the orders of the factors in the numerator. <bookmark mark='t'/> The first is a matrix with a single row, <bookmark mark='b'/> and the second, a matrix with a single column, <bookmark mark='p'/> so their product is a matrix of order one. <bookmark mark='c'/> But a matrix of order one cannot be multiplied by a column matrix: <bookmark mark='x'/> the orders do not match. <bookmark mark='n'/> For the formula to make sense, that product has to be a number.""")) as tracker:
            pinta(self, COLOR_ESCALAR, f1[1][0:3])
            self.play(TransformFromCopy(f1[1][0:3], VGroup(s1[1], s1[2])), TransformFromCopy(f1[2], s1[4]), FadeIn(s1[0]), FadeIn(s1[3]), run_time=1.0)
            en_marca(self, "t", o_aT, run_time=0.5)
            en_marca(self, "b", o_b, run_time=0.5)
            en_marca(self, "p", llave1, o_p, run_time=0.6)
            en_marca(self, "c", o_a, run_time=0.5)
            self.wait_until_bookmark("x")
            self.play(FadeIn(mal), o_p.animate.set_color(RED), o_a.animate.set_color(RED), run_time=0.6)
            self.wait_until_bookmark("n")
            self.play(FadeIn(num), VGroup(s1[1], s1[2]).animate.set_color(COLOR_ESCALAR), run_time=0.8)
        
        with self.voiceover(pausa=3.0, text=tr("""Después, para que se vea la matriz de proyección, <bookmark mark='f'/> el cociente pasa a la derecha. <bookmark mark='o'/> Ahora los órdenes sí encajan: una matriz columna por una matriz de orden uno. <bookmark mark='r'/> Y la asociatividad permite reagrupar los factores, hasta obtener una matriz cuadrada por una matriz columna. <bookmark mark='m'/> Pero en este paso, el mismo producto tiene que ser una matriz.""",
                                    """Then, to make the projection matrix visible, <bookmark mark='f'/> the quotient moves to the right. <bookmark mark='o'/> Now the orders do match: a column matrix times a matrix of order one. <bookmark mark='r'/> And associativity lets us regroup the factors, until we get a square matrix times a column matrix. <bookmark mark='m'/> But in this step, the same product has to be a matrix.""")) as tracker:
            en_marca(self, "f", f2)
            pinta(self, COLOR_ESCALAR, f2[1][0:3])
            self.play(FadeIn(VGroup(*s2[0:5])), run_time=0.8)
            en_marca(self, "o", p_a, llave2, p_p, run_time=0.7)
            self.wait_until_bookmark("r")
            self.play(FadeIn(VGroup(*s2[5:])), run_time=0.8)
            self.play(FadeIn(llave3), FadeIn(p_n), FadeIn(p_b), FadeIn(bien), run_time=0.8)
            self.wait_until_bookmark("m")
            self.play(FadeIn(matz), VGroup(s2[2], s2[3]).animate.set_color(COLOR_ESCALAR), run_time=0.8)
        
        with self.voiceover(pausa=3.0, text=tr("""El mismo símbolo es <bookmark mark='a'/> un número en una fórmula <bookmark mark='b'/> y una matriz en la siguiente, y la notación no lo indica.""",
                                    """The same symbol is <bookmark mark='a'/> a number in one formula <bookmark mark='b'/> and a matrix in the next, and the notation does not show it.""")) as tracker:
            self.wait_until_bookmark("a")
            self.play(Indicate(num, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.0)
            self.wait_until_bookmark("b")
            self.play(Indicate(matz, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.0)
        
        with self.voiceover(pausa=2.5, text=tr("""Quien tiene experiencia resuelve todo esto por el contexto. <bookmark mark='e'/> Pero el estudiante todavía no tiene ese contexto. <bookmark mark='p'/> Polya considera inadmisible que un mismo símbolo denote dos objetos distintos en un mismo problema. <bookmark mark='o'/> Y un programa de ordenador no puede decidir por el contexto.""",
                                    """An experienced reader settles all this from the context. <bookmark mark='e'/> But the student does not have that context yet. <bookmark mark='p'/> Polya considers it inadmissible that the same symbol denote two different objects in the same inquiry. <bookmark mark='o'/> And a computer program cannot decide from the context.""")) as tracker:
            self.play(*[FadeOut(m) for m in (f1, f2, fuente, s1, o_aT, o_b, llave1, o_p, o_a, mal, num, s2, llave2, p_a, p_p, llave3, p_n, p_b, bien, matz)], run_time=0.8)
            en_marca(self, "e", ctx[0])
            en_marca(self, "p", polya)
            en_marca(self, "o", ctx[1])


class P00_E04_TresObjetos(EscenaP00):
    def construct(self):
        self.creditos()
        cab = cabecera("Primera decisión: tres tipos de objetos", "First decision: three kinds of objects")
        vec = M(r"\Vect{a}=(1,2,3,)=\begin{pmatrix}1\\2\\3\end{pmatrix}", 38).move_to([-3.6, 1.6, 0])
        mat = M(r"\Mat{A}=\big[\Vect{a};\Vect{b};\Vect{c};\big]", 38).move_to([2.2, 2.1, 0])
        dist = M(r"\begin{bmatrix}1\\2\\3\end{bmatrix}\ne\begin{pmatrix}1\\2\\3\end{pmatrix}", 38).move_to([2.6, 0.7, 0])
        tres = VGroup(*[VGroup(M(f, 52), T(e, i, 26, GRAY_B)).arrange(DOWN, buff=0.3) for f, e, i in
                        [("3", "número", "number"), ("(3,)", "vector", "vector"), ("[3]", "matriz", "matrix")]]).arrange(RIGHT, buff=1.6).move_to([0, 0.9, 0])
        python = Text("Python:  (3,)", font="monospace", font_size=24, color=GRAY_B).next_to(tres, DOWN, buff=0.5)
        filas = columna([T(r"No hay vectores fila ni vectores columna", r"No row vectors, no column vectors", 32),
                         T(r"Sí hay matrices fila y matrices columna", r"There are row matrices and column matrices", 32),
                         T(r"Solo se transponen matrices: $\MatT{A}$", r"Only matrices are transposed: $\MatT{A}$", 32)], -3.9, 1.6, 0.8)
        punto = M(r"\begin{pmatrix}1,&1,\end{pmatrix}\cdot\begin{pmatrix}2,&1,\end{pmatrix}=3", 40).move_to([0, -1.3, 0])
        cst = coste("una coma, y mirar si hay paréntesis o corchetes", "a comma, and checking for parentheses or square brackets")
        
        with self.voiceover(text=tr("""La primera decisión del libro es que los números, los vectores y las matrices son objetos distintos, y que la escritura los distingue.""",
                                    """The first decision of the book is that numbers, vectors and matrices are different objects, and that the writing tells them apart.""")) as tracker:
            self.play(Write(cab), run_time=1)
        
        # «es la misma lista», no «el mismo vector» (Marcos, 2026-11-23); la primera frase es un trozo de la toma anterior
        with self.voiceover(pausa=0.3, text=tr("""Un vector es <bookmark mark='v'/> una lista ordenada de números, y se escribe entre paréntesis.""",
                                    """A vector is <bookmark mark='v'/> an ordered list of numbers, and it is written between parentheses.""")) as tracker:
            en_marca(self, "v", vec)
        with self.voiceover(text=tr("""Da igual escribirla en horizontal o en vertical: es la misma lista.""",
                                    """It does not matter whether it is written horizontally or vertically: it is the same list.""")) as tracker:
            pass
        
        with self.voiceover(text=tr("""Una matriz es <bookmark mark='m'/> una lista ordenada de vectores, y se escribe entre corchetes. <bookmark mark='d'/> Una matriz con una sola columna no es un vector.""",
                                    """A matrix is <bookmark mark='m'/> an ordered list of vectors, and it is written between square brackets. <bookmark mark='d'/> A matrix with a single column is not a vector.""")) as tracker:
            en_marca(self, "m", mat)
            en_marca(self, "d", dist)
        
        with self.voiceover(pausa=2.5, text=tr("""Así, la notación distingue <bookmark mark='a'/> el número tres, <bookmark mark='b'/> el vector cuya única componente es tres, <bookmark mark='c'/> y la matriz de orden uno. En el vector, la coma final lo distingue de un tres escrito entre paréntesis. <bookmark mark='p'/> Es la escritura de Python para una lista con un solo elemento, y el libro la justifica con una construcción formal de las listas.""",
                                    """So the notation tells apart <bookmark mark='a'/> the number three, <bookmark mark='b'/> the vector whose only component is three, <bookmark mark='c'/> and the matrix of order one. In the vector, the final comma tells it apart from a three written between parentheses. <bookmark mark='p'/> It is how Python writes a list with a single element, and the book justifies it with a formal construction of lists.""")) as tracker:
            limpia(self, vec, mat, dist)
            for m, t in zip("abc", tres):
                en_marca(self, m, t, run_time=0.5)
            en_marca(self, "p", python)
        
        # el final, más corto y tajante (Marcos, 2026-11-23): «…, jamás sobre un vector» (tirada v3, con pausa antes de «jamás»);
        # lo anterior es un trozo de la toma que había
        with self.voiceover(pausa=0.5, text=tr("""En consecuencia, <bookmark mark='a'/> en el libro no hay vectores fila ni vectores columna. Las filas y las columnas de una matriz son vectores, es decir, listas de números. <bookmark mark='b'/> Sí hay matrices fila y matrices columna.""",
                                    """As a consequence, <bookmark mark='a'/> in the book there are no row vectors and no column vectors. The rows and the columns of a matrix are vectors, that is, lists of numbers. <bookmark mark='b'/> There are row matrices and column matrices.""")) as tracker:
            limpia(self, tres, python)
            for m, f in zip("ab", filas):
                en_marca(self, m, f, run_time=0.6)
        with self.voiceover(pausa=2.5, text=tr("""Y la transposición es una operación sobre matrices, jamás sobre un vector.<bookmark mark='v3'/>""",
                                    """And transposition is an operation on matrices, never on a vector.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.6)
        
        with self.voiceover(text=tr("""El producto punto de dos vectores <bookmark mark='p'/> se escribe con un punto, y su resultado es un número. No interviene ninguna matriz.""",
                                    """The dot product of two vectors <bookmark mark='p'/> is written with a dot, and its result is a number. No matrix is involved.""")) as tracker:
            en_marca(self, "p", punto)
        
        with self.voiceover(text=tr("""El coste de esta decisión <bookmark mark='c'/> es pequeño: una coma, y la costumbre de mirar si hay paréntesis o corchetes. Pero falta lo principal. Sin las identificaciones hemos perdido la manera de seleccionar y de transformar con productos. Las dos decisiones siguientes la recuperan.""",
                                    """The cost of this decision <bookmark mark='c'/> is small: a comma, and the habit of checking whether there are parentheses or square brackets. But the main thing is still missing. Without the identifications we have lost the way to select and to transform with products. The next two decisions bring it back.""")) as tracker:
            en_marca(self, "c", cst)
        
        self.pausa_media()


class P00_E05_Selector(EscenaP00):
    def construct(self):
        self.creditos()
        cab = cabecera("Segunda decisión: el operador selector", "Second decision: the selector operator")
        selR = M(r"\elemR{" + A_EJ + r"}{2}=\begin{pmatrix}3\\4\end{pmatrix}", 38).move_to([-3.5, 1.7, 0])
        selL = M(r"\elemL{" + A_EJ + r"}{1}=\begin{pmatrix}1,&3,\end{pmatrix}", 38).move_to([2.6, 1.7, 0])
        rotR = T("columna", "column", 26, COLOR_COLUMNA).next_to(selR, DOWN, buff=0.25)
        rotL = T("fila", "row", 26, COLOR_FILA).next_to(selL, DOWN, buff=0.25)
        selV = M(r"\eleVL{a}{i}\;=\;\eleVR{a}{i}\;=\;a_i", 40).move_to([0, -0.2, 0])
        regla = M(r"\elemRp{\VectF{A}{i}}{j}=\elemLp{\VectC{A}{j}}{i}", 40).move_to([0, -1.4, 0])
        aij = M(r"\elemLR{\Mat{A}}{i}{j}\;=\;a_{ij}", 44).move_to([0, -2.5, 0])
        hab = columna([T(r"Notación habitual", r"Usual notation", 28, GRAY_B), M(r"\mathbf{a}_1,\ \mathbf{a}_2", 38), M(r"\mathbf{a}_1,\ \mathbf{a}_2", 38), M(r"a_1,\ a_2", 38)], -1.0, 2.1, 0.9)
        lib = columna([T(r"Con el selector", r"With the selector", 28, GRAY_B), M(r"\Vect[1]{a},\ \Vect[2]{a}", 38), M(r"\VectC{A}{1},\ \VectC{A}{2}", 38), M(r"\eleVR{a}{1},\ \eleVR{a}{2}", 38)], 2.6, 2.1, 0.9)
        que = columna([T("vectores de una lista", "vectors of a list", 28), T("columnas de una matriz", "columns of a matrix", 28), T("componentes de un vector", "components of a vector", 28)], -6.2, 1.2, 0.9)
        lin = columna([M(r"\elemRp{\Mat{A}+\Mat{B}}{j}=\VectC{A}{j}+\VectC{B}{j}", 36), M(r"\elemRp{\lambda\Mat{A}}{j}=\lambda\big(\VectC{A}{j}\big)", 36), M(r"\VectTF{A}{i}=\VectC{A}{i}", 36)], -5.6, -1.0, 0.85)
        fac = columna([M(r"(\Mat{A}+\Mat{B})\Mat{E}=\Mat{A}\Mat{E}+\Mat{B}\Mat{E}", 32, GRAY_B), M(r"(\lambda\Mat{A})\Mat{E}=\lambda(\Mat{A}\Mat{E})", 32, GRAY_B)], 1.2, -1.0, 0.85)
        cst = coste("leer una barra a la izquierda de una matriz", "reading a bar on the left of a matrix")
        
        with self.voiceover(text=tr("""La segunda decisión es introducir un operador que selecciona. Se escribe con una barra vertical y un índice.""",
                                    """The second decision is to introduce an operator that selects. It is written with a vertical bar and an index.""")) as tracker:
            self.play(Write(cab), run_time=1)
        
        with self.voiceover(text=tr("""<bookmark mark='d'/> A la derecha de una matriz selecciona una columna. <bookmark mark='i'/> A la izquierda selecciona una fila. Los dos resultados son vectores, no matrices.""",
                                    """<bookmark mark='d'/> On the right of a matrix it selects a column. <bookmark mark='i'/> On the left it selects a row. Both results are vectors, not matrices.""")) as tracker:
            self.play(FadeIn(selR), FadeIn(rotR), run_time=0.8)
            pinta(self, COLOR_COLUMNA, *[selR[0][k] for k in (2, 4, 10, 11)])
            en_marca(self, "i", selL, rotL)
            pinta(self, COLOR_FILA, *[selL[0][k] for k in (3, 4, 10, 12)])
        
        with self.voiceover(text=tr("""Junto a un vector <bookmark mark='v'/> selecciona una componente, y el resultado es un número. Da igual escribirlo a la derecha o a la izquierda.""",
                                    """Next to a vector <bookmark mark='v'/> it selects a component, and the result is a number. It does not matter whether it is written on the right or on the left.""")) as tracker:
            en_marca(self, "v", selV)
        
        with self.voiceover(pausa=2.5, text=tr("""Para seleccionar una componente de una matriz, <bookmark mark='r'/> da igual seleccionar primero la fila o la columna. Esta regla hace el papel de la asociatividad: <bookmark mark='p'/> permite escribir la expresión sin paréntesis.""",
                                    """To select a component of a matrix, <bookmark mark='r'/> it does not matter whether we select the row or the column first. This rule plays the role of associativity: <bookmark mark='p'/> it lets us write the expression without parentheses.""")) as tracker:
            en_marca(self, "r", regla)
            en_marca(self, "p", aij)
        
        # cada fila se resalta cuando la voz la nombra, primero con la escritura habitual y después con la del libro, que
        # aparece fila a fila (Marcos, 2026-11-23: la notación es nueva para el espectador). Marcas l, c, k injertadas en la
        # toma que había; la locución siguiente es nueva («sin selector»: Marcos; tirada 1)
        def fila(k, *otros):
            return [que[k].animate.set_color(COLOR_ESCALAR), *[x.animate.set_color(COLOR_ESCALAR) for x in otros]]
        def apaga_fila(k, *otros):
            return [que[k].animate.set_color(WHITE), *[x.animate.set_color(WHITE) for x in otros]]
        
        with self.voiceover(pausa=0.5, text=tr("""El selector resuelve además una ambigüedad del subíndice. <bookmark mark='h'/> En la notación habitual, el subíndice distingue <bookmark mark='l'/> los vectores de una lista, señala <bookmark mark='c'/> las columnas de una matriz o señala <bookmark mark='k'/> las componentes de un vector. Entre unos y otros solo cambia el tipo de letra. <bookmark mark='n'/> Con el selector, cada significado tiene su escritura.""",
                                    """The selector also resolves an ambiguity of the subscript. <bookmark mark='h'/> In the usual notation, the subscript tells apart <bookmark mark='l'/> the vectors of a list, points at <bookmark mark='c'/> the columns of a matrix, or points at <bookmark mark='k'/> the components of a vector. Only the typeface changes between them. <bookmark mark='n'/> With the selector, each meaning has its own writing.""")) as tracker:
            limpia(self, selR, selL, rotR, rotL, selV, regla, aij)
            en_marca(self, "h", hab, que)
            for k, m in enumerate("lck"):
                self.wait_until_bookmark(m)
                self.play(*fila(k, hab[k+1]), *(apaga_fila(k-1, hab[k]) if k else []), run_time=0.25)
            self.wait_until_bookmark("n")
            self.play(*apaga_fila(2, hab[3]), FadeIn(lib[0]), run_time=0.5)
        
        with self.voiceover(pausa=2.5, text=tr("""El subíndice sin selector queda para distinguir los vectores de una lista. <bookmark mark='c'/> La barra a la derecha de una matriz selecciona sus columnas, <bookmark mark='k'/> y a la derecha de un vector, sus componentes.""",
                                    """The subscript without a selector is left to tell apart the vectors of a list. <bookmark mark='c'/> The bar on the right of a matrix selects its columns, <bookmark mark='k'/> and on the right of a vector, its components.""")) as tracker:
            for k, m in enumerate([None, "c", "k"]):
                if m:
                    self.wait_until_bookmark(m)
                lib[k+1].set_color(COLOR_ESCALAR)
                self.play(FadeIn(lib[k+1]), *fila(k), *(apaga_fila(k-1, lib[k]) if k else []), run_time=0.4)
            self.wait(0.8)
            self.play(*apaga_fila(2, lib[3]), run_time=0.3)
        
        with self.voiceover(pausa=2.5, text=tr("""El selector cumple las mismas reglas que un factor de un producto. <bookmark mark='a'/> Se distribuye en una suma, <bookmark mark='b'/> deja fuera a los escalares, <bookmark mark='c'/> y la transposición lo cambia de lado. Quien lo trate como un factor no se equivocará.""",
                                    """The selector obeys the same rules as a factor of a product. <bookmark mark='a'/> It distributes over a sum, <bookmark mark='b'/> it leaves scalars outside, <bookmark mark='c'/> and transposition moves it to the other side. Anyone who treats it as a factor will not go wrong.""")) as tracker:
            limpia(self, hab, que, lib)
            en_marca(self, "a", lin[0], fac[0])
            en_marca(self, "b", lin[1], fac[1])
            en_marca(self, "c", lin[2])
        
        with self.voiceover(text=tr("""El coste <bookmark mark='c'/> es aprender a leer una barra a la izquierda de una matriz. A cambio, las filas y las columnas ya no necesitan nombres propios.""",
                                    """The cost <bookmark mark='c'/> is learning to read a bar on the left of a matrix. In exchange, rows and columns no longer need names of their own.""")) as tracker:
            en_marca(self, "c", cst)
        
        self.pausa_media()


class P00_E06_Transformaciones(EscenaP00):
    def construct(self):
        self.creditos()
        cab = cabecera("Tercera decisión: las transformaciones elementales", "Third decision: elementary transformations")
        R_EJ = r"\begin{bmatrix}1&3\\0&-2\end{bmatrix}"
        anot = M(A_EJ + r"\xrightarrow{\;R_2-2R_1\;}" + R_EJ, 36).move_to([-3.4, 1.7, 0])
        anot_n = T("no forma parte de ninguna expresión", "not part of any expression", 26, COLOR_ESCALAR).next_to(anot, DOWN, buff=0.3)
        elem = M(r"\begin{bmatrix}1&0\\-2&1\end{bmatrix}" + A_EJ + "=" + R_EJ, 36).move_to([3.3, 1.7, 0])
        elem_n = T(r"$\Mat{E}_1,\ \Mat{E}_2,\dots$: el nombre no dice lo que hace", r"$\Mat{E}_1,\ \Mat{E}_2,\dots$: the name does not say what it does", 26, COLOR_ESCALAR).next_to(elem, DOWN, buff=0.3)
        op = M(r"\TESF{-2}{1}{2}{" + A_EJ + "}=" + R_EJ, 40).move_to([0, -0.9, 0])
        op_n = T("a la izquierda, filas; a la derecha, columnas", "on the left, rows; on the right, columns", 26, GRAY_B).next_to(op, DOWN, buff=0.35)
        sec = M(r"\TrC[\OpE{\su{-2}{1}{3}}\OpE{\pr{5}{2}}\OpE{\pe{1}{4}}\OpE{\su{1}{3}{7}}]{\Mat{A}}", 48).move_to([0, 1.5, 0])
        sec_e = M(r"\Mat{A}\,\Mat{E}_1\Mat{E}_2\Mat{E}_3\Mat{E}_4", 44, GRAY_B).move_to([0, 0.1, 0])
        regla = M(r"\TrC[\dSOEgE{1}{q}{*}]{\TrFPE[\dSOEg{p}{1}]{\Mat{A}}}=\TrF[\dSOEg{p}{1}]{\TrCPE[\dSOEgE{1}{q}{*}]{\Mat{A}}}", 36).move_to([0, -1.3, 0])
        el = M(r"\TEC{\Mat{A}} \;=\; \TECp*{\Mat{A}\Mat{I}} \;=\; \Mat{A}\TECpE*{\Mat{I}}", 46).move_to([0, 0.6, 0])
        el_n = T("la matriz elemental, cuando hace falta", "the elementary matrix, when it is needed", 28, GRAY_B).next_to(el, DOWN, buff=0.45)
        cst = coste("un símbolo nuevo y tres abreviaturas", "one new symbol and three abbreviations")
        
        with self.voiceover(text=tr("""La tercera decisión se refiere a las transformaciones elementales. Los manuales las describen de dos maneras.""",
                                    """The third decision concerns elementary transformations. Textbooks describe them in two ways.""")) as tracker:
            self.play(Write(cab), run_time=1)
        
        with self.voiceover(text=tr("""La primera es <bookmark mark='a'/> una anotación junto a la flecha o junto a la matriz. Indica la operación realizada, <bookmark mark='n'/> pero no forma parte de ninguna expresión, así que no se puede operar con ella.""",
                                    """The first is <bookmark mark='a'/> an annotation next to the arrow or next to the matrix. It tells which operation was carried out, <bookmark mark='n'/> but it is not part of any expression, so we cannot operate with it.""")) as tracker:
            en_marca(self, "a", anot)
            en_marca(self, "n", anot_n)
        
        with self.voiceover(pausa=2.5, text=tr("""La segunda es <bookmark mark='a'/> el producto por una matriz elemental. Con el producto sí se puede operar. <bookmark mark='n'/> Pero el nombre de la matriz no indica la transformación que realiza, y su orden depende de la matriz que se transforma.""",
                                    """The second is <bookmark mark='a'/> the product by an elementary matrix. With a product we can operate. <bookmark mark='n'/> But the name of the matrix does not tell which transformation it carries out, and its order depends on the matrix being transformed.""")) as tracker:
            en_marca(self, "a", elem)
            en_marca(self, "n", elem_n)
        
        with self.voiceover(text=tr("""El libro usa <bookmark mark='o'/> un operador que reúne las dos cosas. Bajo el operador se escribe una abreviatura de la transformación. <bookmark mark='n'/> A la izquierda de la matriz transforma sus filas, y a la derecha transforma sus columnas.""",
                                    """The book uses <bookmark mark='o'/> an operator that brings the two together. Under the operator we write an abbreviation of the transformation. <bookmark mark='n'/> On the left of the matrix it transforms its rows, and on the right it transforms its columns.""")) as tracker:
            en_marca(self, "o", op)
            en_marca(self, "n", op_n)
        
        with self.voiceover(pausa=2.5, text=tr("""<bookmark mark='s'/> Una secuencia de transformaciones se escribe con las abreviaturas una detrás de otra, y se puede leer. <bookmark mark='e'/> Con matrices elementales, esta misma secuencia es un producto de cuatro matrices de orden siete, y sus nombres no indican nada.""",
                                    """<bookmark mark='s'/> A sequence of transformations is written with the abbreviations one after another, and it can be read. <bookmark mark='e'/> With elementary matrices, this same sequence is a product of four matrices of order seven, and their names tell nothing.""")) as tracker:
            limpia(self, anot, anot_n, elem, elem_n, op, op_n)
            self.play(FadeIn(sec), run_time=0.8)
            en_marca(self, "e", sec_e)
        
        with self.voiceover(text=tr("""Este operador también se comporta como un factor. <bookmark mark='r'/> Transformar primero las filas y después las columnas da lo mismo que hacerlo en el orden contrario, y por eso tampoco hacen falta paréntesis.""",
                                    """This operator also behaves like a factor. <bookmark mark='r'/> Transforming the rows first and the columns afterwards gives the same as doing it the other way round, so no parentheses are needed here either.""")) as tracker:
            en_marca(self, "r", regla)
        
        with self.voiceover(pausa=2.5, text=tr("""Las matrices elementales no desaparecen: se obtienen cuando hacen falta. <bookmark mark='e'/> Transformar las columnas de una matriz da lo mismo que multiplicarla por la identidad transformada. Dos de los manuales citados enuncian este resultado sin demostración. Con el operador se deduce en una línea.""",
                                    """Elementary matrices do not disappear: we get them when they are needed. <bookmark mark='e'/> Transforming the columns of a matrix gives the same as multiplying it by the transformed identity. Two of the textbooks quoted state this result without proof. With the operator it follows in one line.""")) as tracker:
            limpia(self, sec, sec_e, regla)
            en_marca(self, "e", el, el_n)
        
        with self.voiceover(text=tr("""El coste <bookmark mark='c'/> es un símbolo nuevo y tres abreviaturas.""",
                                    """The cost <bookmark mark='c'/> is one new symbol and three abbreviations.""")) as tracker:
            en_marca(self, "c", cst)
        
        self.pausa_media()


class P00_E07_Producto(EscenaP00):
    def construct(self):
        self.creditos()
        cab = cabecera("Cuarta decisión: definir por lo que es", "Fourth decision: defining by what it is")
        larson = M(r"AB=[c_{ij}],\qquad c_{ij}=\sum_{k=1}^n a_{ik}b_{kj}", 38).move_to([0, 1.9, 0])
        larson_n = T("Larson, p. 49", None, 24, GRAY_B).next_to(larson, DOWN, buff=0.25)
        mv = M(r"\MV{A}{b} = b_1\VectCpE*{A}{1}+\cdots+b_n\VectCpE*{A}{n}", 40).move_to([0, 0.3, 0])
        mv_n = T("Strang, p. 23", None, 24, GRAY_B).next_to(mv, DOWN, buff=0.25)
        defAB = M(r"\VectCp{AB}{j}=\Mat{A}\VectCpE{B}{j}", 44).move_to([-2.4, -1.5, 0])
        asoc = M(r"(\Mat{A}\Mat{B})\Mat{E}=\Mat{A}(\Mat{B}\Mat{E})", 34, GRAY_B).move_to([3.4, -1.5, 0])
        # la componente del producto y sus tres lecturas, en el mismo sitio
        e0 = M(r"\eleM{AB}{i}{j}", 64).move_to([0, 1.7, 0])
        lect = [M(f, 64).move_to([0, 1.7, 0]) for f in (r"\elemL{\Mat{A}\VectCpE{B}{j}}{i}", r"\elemR{\VectFpE{A}{i}\Mat{B}}{j}", r"\dotProd{\VectFpE{A}{i}}{\VectCpE{B}{j}}")]
        frases = columna([T(r"las columnas de $\Mat{AB}$ son combinaciones lineales de las columnas de $\Mat{A}$", r"the columns of $\Mat{AB}$ are linear combinations of the columns of $\Mat{A}$", 28),
                          T(r"las filas de $\Mat{AB}$ son combinaciones lineales de las filas de $\Mat{B}$", r"the rows of $\Mat{AB}$ are linear combinations of the rows of $\Mat{B}$", 28),
                          T(r"cada componente es el producto punto de una fila de $\Mat{A}$ por una columna de $\Mat{B}$", r"each component is the dot product of a row of $\Mat{A}$ and a column of $\Mat{B}$", 28)], -5.6, 0.2, 0.7)
        caja_t = T(r"Una expresión sin paréntesis admite varias lecturas, y todas son correctas", r"An expression without parentheses admits several readings, and all of them are correct", 28, COLOR_ESCALAR)
        caja = VGroup(SurroundingRectangle(caja_t, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.12, stroke_width=2), caja_t).move_to([0, -2.1, 0])
        polya = T(r"Polya, pp. 138--139: una notación \emph{expresiva}", r"Polya, pp. 138--139: an \emph{expressive} notation", 26, GRAY_B).next_to(caja, DOWN, buff=0.25)
        cst = coste("fila por columna deja de ser el punto de partida", "row times column is no longer the starting point")
        
        with self.voiceover(text=tr("""La cuarta decisión afecta a las definiciones. <bookmark mark='l'/> Esta es la definición habitual del producto de matrices. Indica el cálculo de cada componente, y nada más. No muestra la relación entre las columnas del producto y las columnas del primer factor.""",
                                    """The fourth decision affects the definitions. <bookmark mark='l'/> This is the usual definition of the product of matrices. It tells how to compute each component, and nothing else. It does not show the relation between the columns of the product and the columns of the first factor.""")) as tracker:
            self.play(Write(cab), run_time=1)
            en_marca(self, "l", larson, larson_n)
        
        with self.voiceover(text=tr("""El libro empieza por el producto de una matriz por un vector, <bookmark mark='m'/> y lo define como una combinación lineal de las columnas de la matriz. Es la definición que usa Strang. No describe un cálculo: dice lo que es el resultado.""",
                                    """The book starts with the product of a matrix and a vector, <bookmark mark='m'/> and defines it as a linear combination of the columns of the matrix. It is the definition Strang uses. It does not describe a computation: it says what the result is.""")) as tracker:
            en_marca(self, "m", mv, mv_n)
        
        with self.voiceover(pausa=2.5, text=tr("""El producto de dos matrices <bookmark mark='d'/> se define columna a columna: cada columna del producto es la primera matriz por la columna correspondiente de la segunda. <bookmark mark='a'/> Es la igualdad que antes salía de la asociatividad. Ahora es la definición, y la asociatividad se demuestra a partir de ella.""",
                                    """The product of two matrices <bookmark mark='d'/> is defined column by column: each column of the product is the first matrix times the corresponding column of the second. <bookmark mark='a'/> It is the equality that earlier came from associativity. Now it is the definition, and associativity is proved from it.""")) as tracker:
            en_marca(self, "d", defAB)
            en_marca(self, "a", asoc)
        
        with self.voiceover(text=tr("""Veamos lo que da de sí esta escritura. <bookmark mark='e'/> Esta expresión es una componente del producto, escrita sin paréntesis. Los paréntesis se pueden colocar de tres maneras.""",
                                    """Let us see how far this writing goes. <bookmark mark='e'/> This expression is a component of the product, written without parentheses. The parentheses can be placed in three ways.""")) as tracker:
            limpia(self, larson, larson_n, mv, mv_n, defAB, asoc)
            en_marca(self, "e", e0)
        
        actual = e0
        for k, (es, en) in enumerate([
                ("""Si agrupamos <bookmark mark='a'/> la segunda matriz con su selector, leemos que las columnas del producto son combinaciones lineales de las columnas de la primera matriz.""",
                 """If we group <bookmark mark='a'/> the second matrix with its selector, we read that the columns of the product are linear combinations of the columns of the first matrix."""),
                ("""Si agrupamos <bookmark mark='a'/> la primera matriz con el suyo, leemos que las filas del producto son combinaciones lineales de las filas de la segunda.""",
                 """If we group <bookmark mark='a'/> the first matrix with its own, we read that the rows of the product are linear combinations of the rows of the second."""),
                ("""Y si agrupamos <bookmark mark='a'/> cada matriz con su selector, quedan juntos dos vectores, una fila y una columna. El producto de dos vectores es el producto punto, y por eso aparece el punto. Es la regla de cálculo de la definición habitual.""",
                 """And if we group <bookmark mark='a'/> each matrix with its selector, two vectors end up side by side, a row and a column. The product of two vectors is the dot product, and that is why the dot appears. It is the computing rule of the usual definition.""")]):
            with self.voiceover(pausa=2.5, text=tr(es, en)) as tracker:
                self.wait_until_bookmark("a")
                self.play(TransformMatchingShapes(actual, lect[k]), run_time=1.0)
                self.play(FadeIn(frases[k]), run_time=0.6)
                actual = lect[k]
        
        with self.voiceover(pausa=2.5, text=tr("""<bookmark mark='c'/> Una expresión sin paréntesis admite varias lecturas, y todas son correctas. Strang las presenta como maneras distintas de multiplicar matrices. Aquí salen de una sola expresión, desplazando los paréntesis.""",
                                    """<bookmark mark='c'/> An expression without parentheses admits several readings, and all of them are correct. Strang presents them as different ways to multiply matrices. Here they come from a single expression, by moving the parentheses.""")) as tracker:
            self.play(TransformMatchingShapes(actual, e0.copy().move_to([0, 1.7, 0])), FadeIn(caja), run_time=1.0)
        
        with self.voiceover(text=tr("""Polya llama <bookmark mark='p'/> expresiva a una notación de la que se deducen consecuencias. Esta lo es.""",
                                    """Polya calls <bookmark mark='p'/> a notation expressive when consequences can be drawn from it. This one is.""")) as tracker:
            en_marca(self, "p", polya)
        
        with self.voiceover(text=tr("""El coste <bookmark mark='c'/> es que la regla de fila por columna deja de ser el punto de partida y pasa a ser una consecuencia.""",
                                    """The cost <bookmark mark='c'/> is that the row-times-column rule stops being the starting point and becomes a consequence.""")) as tracker:
            self.wait_until_bookmark("c")
            self.play(FadeOut(caja), FadeOut(polya), FadeIn(cst), run_time=0.8)
        
        self.pausa_media()


class P00_E08_Demostraciones(EscenaP00):
    def construct(self):
        self.creditos()
        cab = cabecera("Las demostraciones", "The proofs")
        lineas, reglas = cadena_asociativa(fs=36, x=-5.0, y_sup=1.9, salto=0.9, x_regla=0.6)
        strang = T("El argumento: Strang, p. 82 (problema)", "The argument: Strang, p. 82 (a problem)", 24, GRAY_B).to_edge(DOWN, buff=0.5)
        # Glifos de la cadena: ( A ( B C ) ) | j (0-8);  = A ( ( B C ) | j ) (0-9);  = A ( B ( C | j ) ) (0-9);
        #                      = ( A B ) ( C | j ) (0-9);  = ( ( A B ) C ) | j (0-9)
        PASOS = [([(1, 1), (2, 3), (3, 4), (4, 5), (5, 6)], [(0, 2), (6, 9), (7, 7), (8, 8)]),
                 ([(1, 1), (2, 2), (4, 3), (5, 5), (9, 9)], [(3, 4), (6, 8), (7, 6), (8, 7)]),
                 ([(1, 2), (3, 3), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)], [(2, 1), (9, 4)]),
                 ([(1, 2), (2, 3), (3, 4), (4, 5), (6, 6)], [(5, 1), (9, 7), (7, 8), (8, 9)])]
        tit_t = M(r"\Transp{\Mat{AB}}=\MatTpE{B}\MatTpE{A}", 40).move_to([0, 2.3, 0])
        sumas_t = columna([M(r"\big((AB)^T\big)_{ij} = (AB)_{ji} = \sum_{k=1}^n a_{jk}b_{ki}", 28),
                           M(r"({B}^T{A}^T)_{ij}=\sum_{k=1}^n{(B^T)}_{ik}{(A^T)}_{kj}=\sum_{k=1}^nb_{ki}a_{jk}", 28)], -6.6, 1.0, 1.3)
        cad_t = [M(f, 32) for f in (r"\elemR{\Transp{\Mat{AB}}}{j}", r"=\elemLp{\Mat{AB}}{j}", r"=\VectFpE{A}{j}\Mat{B}", r"=\Big(\VectTC{A}{j}\Big)\Mat{B}",
                                     r"=\MatTpE{B}\Big(\VectTC{A}{j}\Big)", r"=\elemRP{\MatTpE{B}\MatTpE{A}}{j}")]
        for k, l in enumerate(cad_t):
            l.move_to([0, 1.4 - 0.72*k, 0]).align_to([0.6 + (0.5 if k else 0), 0, 0], LEFT)
        reg_t = [T(e, i, 22, COLOR_REGLA).move_to([0, l.get_y(), 0]).align_to([3.9, 0, 0], LEFT) for (e, i), l in zip(
            [("cambia de lado el selector", "moves the selector"), ("la fila de un producto", "the row of a product"), ("cambia de lado el selector", "moves the selector"),
             ("cambia de lado el vector", "moves the vector"), ("definición del producto", "definition of the product")], cad_t[1:])]
        balance = columna([T("No son más cortas", "They are not shorter", 34), T("En la distributiva, las dos notaciones empatan", "For the distributive property, a tie", 34),
                           T("Sin índices de suma; cada paso tiene nombre", "No summation indices; every step has a name", 34, COLOR_ESCALAR)], -4.2, 0.9, 0.95)
        
        with self.voiceover(text=tr("""Volvamos a la demostración del principio, ahora paso a paso. Dos matrices son iguales si lo son columna a columna, <bookmark mark='c'/> así que seleccionamos una columna.""",
                                    """Let us go back to the proof from the beginning, now step by step. Two matrices are equal if they are equal column by column, <bookmark mark='c'/> so we select a column.""")) as tracker:
            self.play(Write(cab), run_time=1)
            en_marca(self, "c", lineas[0])
        
        with self.voiceover(pausa=2.5, text=tr("""Por la definición del producto, <bookmark mark='a'/> el selector pasa al segundo factor. Por la misma definición, <bookmark mark='b'/> pasa a la tercera matriz. Lo que queda es un producto de matrices por un vector, <bookmark mark='c'/> y para ese producto la propiedad ya está demostrada, una sola vez, con la linealidad. Y por la definición del producto, <bookmark mark='d'/> el selector vuelve a salir.""",
                                    """By the definition of the product, <bookmark mark='a'/> the selector moves to the second factor. By the same definition, <bookmark mark='b'/> it moves to the third matrix. What remains is a product of matrices times a vector, <bookmark mark='c'/> and for that product the property has already been proved, just once, using linearity. And by the definition of the product, <bookmark mark='d'/> the selector comes back out.""")) as tracker:
            for k, m in enumerate("abcd"):
                self.wait_until_bookmark(m)
                nace(self, lineas[k][0], lineas[k + 1][0], PASOS[k][0], PASOS[k][1], extra=[FadeIn(reglas[k])])
        
        with self.voiceover(pausa=2.5, text=tr("""No ha aparecido ningún índice de suma. La suma está en una propiedad del producto de una matriz por un vector, que se demuestra una vez y después se usa. <bookmark mark='s'/> El argumento no es nuevo: Strang lo propone en un problema. Lo nuevo es que estas cuatro igualdades son la demostración completa.""",
                                    """No summation index has appeared. The sum lives in a property of the product of a matrix and a vector, which is proved once and then used. <bookmark mark='s'/> The argument is not new: Strang suggests it in a problem. What is new is that these four equalities are the complete proof.""")) as tracker:
            en_marca(self, "s", strang)
        
        with self.voiceover(text=tr("""<bookmark mark='t'/> La transpuesta de un producto se demuestra del mismo modo. <bookmark mark='s'/> Con sumatorios hay que decidir las componentes que intervienen cuando las matrices están transpuestas. <bookmark mark='n'/> Con el selector, cada paso aplica una regla: la transposición cambia de lado el selector, y cambia de lado el vector.""",
                                    """<bookmark mark='t'/> The transpose of a product is proved in the same way. <bookmark mark='s'/> With summations we have to decide which components are involved when the matrices are transposed. <bookmark mark='n'/> With the selector, each step applies a rule: transposition moves the selector to the other side, and moves the vector to the other side.""")) as tracker:
            self.play(*[FadeOut(l) for l in lineas], *[FadeOut(r) for r in reglas], FadeOut(strang), run_time=0.6)
            self.play(FadeIn(tit_t), run_time=0.6)
            en_marca(self, "s", sumas_t)
            self.wait_until_bookmark("n")
            self.play(LaggedStart(*[FadeIn(l) for l in cad_t], lag_ratio=0.3), run_time=2.0)
            self.play(*[FadeIn(r) for r in reg_t], run_time=0.8)
        
        with self.voiceover(pausa=2.5, text=tr("""<bookmark mark='a'/> Estas demostraciones no son más cortas. <bookmark mark='b'/> En la propiedad distributiva, las dos notaciones quedan a la par. La diferencia es otra. <bookmark mark='c'/> Aquí solo aparecen las matrices y el selector, y cada igualdad aplica una regla que el estudiante puede nombrar.""",
                                    """<bookmark mark='a'/> These proofs are not shorter. <bookmark mark='b'/> For the distributive property, the two notations are on a par. The difference lies elsewhere. <bookmark mark='c'/> Here only the matrices and the selector appear, and each equality applies a rule the student can name.""")) as tracker:
            self.play(FadeOut(tit_t), FadeOut(sumas_t), *[FadeOut(l) for l in cad_t], *[FadeOut(r) for r in reg_t], run_time=0.6)
            self.play(FadeIn(balance[0]), run_time=0.6)
            en_marca(self, "b", balance[1])
            en_marca(self, "c", balance[2])
        
        self.pausa_media()


class P00_E09_Programa(EscenaP00):
    def construct(self):
        self.creditos()
        cab = cabecera("Una notación que se puede programar", "A notation that can be programmed")
        def codigo(t, fs=22, color=WHITE):
            return Text(t, font="monospace", font_size=fs, color=color)
        nacal = T(r"NAcAL, módulo de Python \quad \texttt{github.com/mbujosab/nacallib}", r"NAcAL, a Python module \quad \texttt{github.com/mbujosab/nacallib}", 28, GRAY_B).move_to([0, 2.5, 0])
        # Las dos líneas de la introducción del libro; en amarillo, solo lo que coincide con la fórmula
        d1 = M(r"\elemR{(\Vect{a}+\Vect{b})}{i}=\eleVR{a}{i}+\eleVR{b}{i}", 40).move_to([0, 1.6, 0])
        c1 = Text("Vector([ (self|i) + (other|i) for i in range(1, len(self)+1) ])", font="monospace", font_size=22, color=GRAY_B,
                  t2c={"(self|i) + (other|i)": COLOR_ESCALAR}).next_to(d1, DOWN, buff=0.3)
        d2 = M(r"\elemR{(\Mat{A}\Mat{X})}{j}=\Mat{A}(\VectC{X}{j})", 40).move_to([0, -0.5, 0])
        c2 = Text("Matrix([ self*(x|j) for j in range(1, x.n+1) ])", font="monospace", font_size=22, color=GRAY_B,
                  t2c={"self*(x|j)": COLOR_ESCALAR}).next_to(d2, DOWN, buff=0.3)
        tipos = columna([T(r"vector $\cdot$ vector $\longrightarrow$ número", r"vector $\cdot$ vector $\longrightarrow$ number", 32),
                         T(r"matriz$\getItem j$ $\longrightarrow$ vector", r"matrix$\getItem j$ $\longrightarrow$ vector", 32),
                         T(r"matriz $\cdot$ matriz $\longrightarrow$ matriz", r"matrix $\cdot$ matrix $\longrightarrow$ matrix", 32)], -2.8, 1.5, 0.85)
        numpy = columna([codigo("NumPy", 24, GRAY_B), codigo("A[:, 1]      lista de números" if LANG == "es" else "A[:, 1]      list of numbers", 24),
                         codigo("A[:, [1]]    tabla con una columna" if LANG == "es" else "A[:, [1]]    table with one column", 24),
                         codigo("a @ b        un número" if LANG == "es" else "a @ b        a number", 24)], -6.4, 1.7, 0.6)
        matlab = columna([codigo("Matlab", 24, GRAY_B), codigo("(a'*b)*c     definido" if LANG == "es" else "(a'*b)*c     defined", 24, GREEN),
                          codigo("a'*(b*c)     no definido" if LANG == "es" else "a'*(b*c)     not defined", 24, RED)], 1.7, 1.7, 0.6)
        # el escalar a la derecha (Marcos, 2026-11-21): convenio no habitual que salió de programar el curso; no hay que
        # distinguir el lado porque el producto de números reales es conmutativo (pregunta de Andrés al ver V15)
        conv = VGroup(M(r"\Vect{b}\lambda=\lambda\Vect{b}", 48), M(r"\Mat{A}\lambda=\lambda\Mat{A}", 48)).arrange(RIGHT, buff=1.6).move_to([0, 1.2, 0])
        conv_n = T("el escalar de un producto, también a la derecha", "the scalar of a product, also on the right", 30, GRAY_B).next_to(conv, DOWN, buff=0.45)
        conm = VGroup(M(r"\lambda\mu=\mu\lambda", 44, COLOR_ESCALAR),
                      T("el producto de números reales es conmutativo", "the product of real numbers is commutative", 30, GRAY_B)).arrange(DOWN, buff=0.35).move_to([0, -1.7, 0])
        algos = columna([T("resuelve sistemas", "solves systems", 32), T("invierte matrices", "inverts matrices", 32), T("diagonaliza", "diagonalizes", 32),
                         T("y muestra cada paso con la notación del libro", "and shows each step in the notation of the book", 32, COLOR_ESCALAR)], -3.6, 1.4, 0.8)
        
        with self.voiceover(text=tr("""Hay una prueba más, y es externa. La notación está implementada <bookmark mark='n'/> en un módulo de Python, llamado Nacal.""",
                                    """There is one more piece of evidence, and it is external. The notation is implemented <bookmark mark='n'/> in a Python module, called Nacal.""")) as tracker:
            self.play(Write(cab), run_time=1)
            en_marca(self, "n", nacal)
        
        with self.voiceover(pausa=2.5, text=tr("""<bookmark mark='a'/> Esta es la definición de la suma de vectores, <bookmark mark='b'/> y esta es su implementación. <bookmark mark='c'/> Esta es la definición del producto de matrices, <bookmark mark='d'/> y esta es la suya. El código usa la misma barra vertical, y es tan breve como la definición.""",
                                    """<bookmark mark='a'/> This is the definition of vector addition, <bookmark mark='b'/> and this is its implementation. <bookmark mark='c'/> This is the definition of the product of matrices, <bookmark mark='d'/> and this is its own. The code uses the same vertical bar, and it is as short as the definition.""")) as tracker:
            self.play(FadeIn(d1), run_time=0.6)
            for m, x in zip("bcd", (c1, d2, c2)):
                en_marca(self, m, x, run_time=0.6)
        
        with self.voiceover(text=tr("""Un programa solo puede evaluar una operación si está definida para los tipos de sus operandos. <bookmark mark='t'/> Por eso, programar la notación obliga a que cada operación tenga un resultado de un tipo determinado. Buena parte de las decisiones que hemos visto salieron de ese trabajo.""",
                                    """A program can only evaluate an operation if it is defined for the types of its operands. <bookmark mark='t'/> So programming the notation forces every operation to have a result of a definite type. A good part of the decisions we have seen came out of that work.""")) as tracker:
            limpia(self, d1, c1, d2, c2)
            en_marca(self, "t", tipos)
        
        with self.voiceover(text=tr("""También salió de ese trabajo un convenio que no es el habitual: <bookmark mark='f'/> el libro permite escribir a la derecha el escalar de un producto. <bookmark mark='s'/> Así las expresiones se simplifican mucho, y con ellas el código.""",
                                    """That work also produced a convention that is not the usual one: <bookmark mark='f'/> the book allows writing the scalar of a product on the right. <bookmark mark='s'/> This makes the expressions much simpler, and the code with them.""")) as tracker:
            limpia(self, tipos)
            en_marca(self, "f", conv)
            en_marca(self, "s", conv_n)
        
        with self.voiceover(pausa=2.5, text=tr("""En general, escribir los escalares a la izquierda o a la derecha da estructuras distintas. <bookmark mark='c'/> Aquí no, porque el producto de números reales es conmutativo.""",
                                               """In general, writing scalars on the left or on the right gives different structures. <bookmark mark='c'/> Not here, because the product of real numbers is commutative.""")) as tracker:
            en_marca(self, "c", conm)
        
        with self.voiceover(text=tr("""La distinción entre un vector y una matriz columna tampoco es exclusiva del libro. <bookmark mark='n'/> La biblioteca NumPy distingue una lista de números de una tabla con una sola columna, y multiplica dos listas sin transponer nada.""",
                                    """The distinction between a vector and a column matrix is not exclusive to the book either. <bookmark mark='n'/> The NumPy library tells a list of numbers apart from a table with a single column, and it multiplies two lists without transposing anything.""")) as tracker:
            limpia(self, conv, conv_n, conm)
            en_marca(self, "n", numpy)
        
        with self.voiceover(pausa=2.5, text=tr("""<bookmark mark='m'/> En Matlab, en cambio, una matriz de orden uno actúa además como un número. Con esa regla, el primero de estos productos está definido y el segundo no. Tratar todos los objetos como matrices acaba rompiendo la asociatividad que se quería aprovechar.""",
                                    """<bookmark mark='m'/> In Matlab, by contrast, a matrix of order one also acts as a number. With that rule, the first of these products is defined and the second is not. Treating every object as a matrix ends up breaking the very associativity it was meant to exploit.""")) as tracker:
            self.play(FadeIn(matlab), run_time=0.8)
        
        with self.voiceover(text=tr("""Los algoritmos del libro también están en el módulo. <bookmark mark='a'/> Resuelve sistemas, invierte matrices y las diagonaliza, <bookmark mark='p'/> y muestra cada paso con la notación del libro.""",
                                    """The algorithms of the book are in the module too. <bookmark mark='a'/> It solves systems, inverts matrices and diagonalizes them, <bookmark mark='p'/> and it shows each step in the notation of the book.""")) as tracker:
            limpia(self, numpy, matlab)
            en_marca(self, "a", *algos[:3])
            en_marca(self, "p", algos[3])
        
        self.pausa_media()


class P00_E10_Coste(EscenaP00):
    def construct(self):
        self.creditos()
        cab = cabecera("El coste", "The cost")
        polya = cita([r"``To learn a new notation is a burden for the memory.", r"The intelligent student refuses to assume the burden", r"if he does not see any compensation for it.''"],
                     r"Polya, \emph{How to Solve It}, p. 141", 30).move_to([0, 1.2, 0])
        costes = columna([T("1. Pasar de una notación a otra", "1. Moving between notations", 30), T("2. La coma final y el selector a la izquierda", "2. The final comma and the left selector", 30),
                          T("3. Las asignaturas siguientes usan la habitual", "3. Later courses use the usual notation", 30), T("4. Sin manuales de apoyo para el profesor", "4. No supporting textbooks for the teacher", 30)], -6.6, 2.0, 0.75)
        filas_t = [("componente de un vector", "component of a vector", r"\eleVR{a}{i}", r"a_i"), ("columna de una matriz", "column of a matrix", r"\VectC{A}{j}", r"\mathbf{a}_j,\ A_{*j}"),
                   ("fila de una matriz", "row of a matrix", r"\VectF{A}{i}", r"\mathbf{a}_i^T,\ A_{i*}"), ("componente de una matriz", "component of a matrix", r"\eleM{A}{i}{j}", r"a_{ij}"),
                   ("producto punto", "dot product", r"\dotprod{a}{b}", r"\mathbf{a}^T\mathbf{b}"), ("vector por matriz", "vector times matrix", r"\VM{a}{B}", r"\mathbf{a}^TB"),
                   ("transformar columnas", "transforming columns", r"\TEC{\Mat{A}}", r"AE")]
        tabla = VGroup(*[x for e, i, a, b in filas_t for x in (T(e, i, 24, GRAY_B), M(a, 30), M(b, 30))]).arrange_in_grid(cols=3, buff=(0.5, 0.22), cell_alignment=LEFT)
        cabt = VGroup(T("", "", 24), T("libro", "book", 24, COLOR_ESCALAR), T("habitual", "usual", 24, COLOR_ESCALAR))
        for c, ref in zip(cabt[1:], tabla[1:3]):
            c.next_to(ref, UP, buff=0.25).align_to(ref, LEFT)
        tabla = VGroup(tabla, cabt[1:]).scale_to_fit_height(3.9).move_to([3.3, -1.2, 0])
        recursos = columna([T(r"Libro (CC BY-SA 4.0): \texttt{github.com/mbujosab/CursoDeAlgebraLineal}", r"Book (CC BY-SA 4.0, in Spanish): \texttt{github.com/mbujosab/CursoDeAlgebraLineal}", 26),
                            T(r"Macros de \LaTeX{}: \texttt{github.com/mbujosab/nacal-latex-package}", r"\LaTeX{} macros: \texttt{github.com/mbujosab/nacal-latex-package}", 26),
                            T(r"Transparencias y vídeos del curso", r"Class slides and course videos", 26)], -6.6, -1.3, 0.6)
        balance = columna([T(r"\textbf{Inequívoca}: ningún símbolo denota objetos de dos tipos", r"\textbf{Unambiguous}: no symbol denotes objects of two kinds", 30),
                           T(r"\textbf{Fácil de recordar}: a la izquierda, filas; a la derecha, columnas", r"\textbf{Easy to remember}: on the left, rows; on the right, columns", 30),
                           T(r"\textbf{Expresiva}: las definiciones dicen lo que son los objetos", r"\textbf{Expressive}: definitions say what the objects are", 30),
                           T(r"\textbf{Operativa}: demostraciones paso a paso, con reglas que tienen nombre", r"\textbf{Operational}: step-by-step proofs, with rules that have names", 30)], -6.4, 1.6, 0.95)
        
        with self.voiceover(text=tr("""Queda pesar el coste. <bookmark mark='p'/> Polya advierte que aprender una notación nueva es una carga para la memoria, y que el estudiante inteligente la rechaza si no ve una compensación. Lo mismo vale para un profesor.""",
                                    """It remains to weigh the cost. <bookmark mark='p'/> Polya warns that learning a new notation is a burden for the memory, and that the intelligent student refuses the burden without seeing some compensation for it. The same holds for a teacher.""")) as tracker:
            self.play(Write(cab), run_time=1)
            en_marca(self, "p", polya)
        
        with self.voiceover(pausa=2.5, text=tr("""Los costes son cuatro. <bookmark mark='a'/> Quien consulte otros textos tiene que pasar de una notación a otra, <bookmark mark='t'/> y para eso el libro incluye este cuadro de equivalencias. <bookmark mark='b'/> La coma final y el selector a la izquierda son escrituras nuevas. <bookmark mark='c'/> El estudiante que siga con otras asignaturas tendrá que aprender la notación habitual. <bookmark mark='d'/> Y el profesor no puede apoyar sus clases en los manuales de siempre.""",
                                    """There are four costs. <bookmark mark='a'/> Anyone who consults other texts has to move from one notation to the other, <bookmark mark='t'/> and for that the book includes this table of equivalences. <bookmark mark='b'/> The final comma and the selector on the left are new ways of writing. <bookmark mark='c'/> A student who goes on to other courses will have to learn the usual notation. <bookmark mark='d'/> And the teacher cannot rely on the usual textbooks in class.""")) as tracker:
            limpia(self, polya)
            en_marca(self, "a", costes[0], run_time=0.6)
            en_marca(self, "t", tabla)
            for m, c in zip("bcd", costes[1:]):
                en_marca(self, m, c, run_time=0.6)
        
        with self.voiceover(text=tr("""Para este último coste hay ayuda. <bookmark mark='r'/> El libro es libre, y lo acompañan un paquete de LaTeX con las macros de la notación, las transparencias de clase y los vídeos del curso.""",
                                    """For this last cost there is help. <bookmark mark='r'/> The book is free, and it comes with a LaTeX package with the macros of the notation, the class slides and the videos of the course.""")) as tracker:
            self.wait_until_bookmark("r")
            self.play(FadeOut(tabla), FadeIn(recursos), run_time=0.8)
        
        with self.voiceover(pausa=2.5, text=tr("""Frente a esos costes está lo que hemos visto. <bookmark mark='a'/> Ningún símbolo denota objetos de dos tipos. <bookmark mark='b'/> Una sola regla de posición sirve para todo: a la izquierda de una matriz se actúa sobre sus filas, a la derecha sobre sus columnas, y la transposición cambia de lado. <bookmark mark='c'/> Las definiciones dicen lo que son los objetos, y los cálculos se deducen. <bookmark mark='d'/> Y las demostraciones se escriben paso a paso, con reglas que tienen nombre.""",
                                    """Against those costs stands what we have seen. <bookmark mark='a'/> No symbol denotes objects of two kinds. <bookmark mark='b'/> A single rule of position works for everything: on the left of a matrix we act on its rows, on the right on its columns, and transposition changes sides. <bookmark mark='c'/> Definitions say what the objects are, and computations follow. <bookmark mark='d'/> And proofs are written step by step, with rules that have names.""")) as tracker:
            limpia(self, costes, recursos)
            for m, b in zip("abcd", balance):
                en_marca(self, m, b, run_time=0.6)
        
        self.pausa_media()


class P00_E11_Cierre(EscenaP00):
    def construct(self):
        self.creditos()
        godement = cita(tr([r"``Si estas gentes tuviesen razón resultaría que [\dots] los principiantes", r"comprenden tanto mejor un texto cuanto peor escrito esté.''"],
                           [r"``If this view were correct it would imply that [\dots] the worst-written", r"textbooks would be those most easily understood by the beginner.''"]),
                        r"Godement, \emph{Álgebra}, prefacio", 30).move_to([0, 1.9, 0])
        vanloan = VGroup(T(r"``La notación lo es todo''", r"``Notation is everything''", 56, COLOR_ESCALAR), T("Charles F. Van Loan", None, 28, GRAY_B)).arrange(DOWN, buff=0.35).move_to([0, 0.6, 0])
        polya = cita([r"``We should choose our notation carefully,", r"and have some good reason for our choice.''"], r"Polya, \emph{How to Solve It}, p. 140", 30).move_to([0, -1.2, 0])
        enlaces = columna([T(r"Libro: \texttt{github.com/mbujosab/CursoDeAlgebraLineal}", r"Book (in Spanish): \texttt{github.com/mbujosab/CursoDeAlgebraLineal}", 26),
                           T(r"NAcAL: \texttt{github.com/mbujosab/nacallib}", None, 26), T(r"Licencia CC BY-SA 4.0", r"Licence CC BY-SA 4.0", 26, GRAY_B)], -4.4, -1.9, 0.5)
        
        with self.voiceover(text=tr("""Se suele pensar que el rigor y una notación precisa añaden dificultad a quien empieza. <bookmark mark='g'/> Godement respondía que, si fuera así, los principiantes entenderían mejor un texto cuanto peor escrito estuviera.""",
                                    """It is often thought that rigour and a precise notation make things harder for beginners. <bookmark mark='g'/> Godement replied that, if that were so, the worst-written textbooks would be the ones beginners understand most easily.""")) as tracker:
            en_marca(self, "g", godement)
        
        with self.voiceover(pausa=2.5, text=tr("""Van Loan lo dijo con menos palabras: <bookmark mark='v'/> la notación lo es todo.""",
                                    """Van Loan said it in fewer words: <bookmark mark='v'/> notation is everything.""")) as tracker:
            self.play(FadeOut(godement), run_time=0.5)
            en_marca(self, "v", vanloan)
        
        with self.voiceover(text=tr("""<bookmark mark='p'/> Polya pide que la notación se elija con cuidado, y que haya alguna buena razón para la elección. Estas son las razones del libro. La valoración le corresponde a usted, y la mejor manera de hacerla es leer una lección.""",
                                    """<bookmark mark='p'/> Polya asks that we choose our notation carefully, and have some good reason for our choice. These are the reasons of the book. The judgement is yours, and the best way to form it is to read one lesson.""")) as tracker:
            self.play(FadeIn(polya), run_time=0.8)
        
        with self.voiceover(text=tr("""En la descripción están los enlaces al libro, al módulo Nacal y a los vídeos del curso.""",
                                    """In the description you will find the links to the book, to the Nacal module and to the videos of the course. Please note that the book is in Spanish.""")) as tracker:
            self.play(FadeOut(polya), FadeIn(enlaces), run_time=0.8)
        
        self.pausa_larga()
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
