from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Tipos de matrices", "Types of matrices")

C_EJ = [[1, 2, 0], [3, -1, 4], [0, 5, 2]]      # cuadrada de orden 3
R_EJ = [[1, 2, 0], [3, -1, 4]]                 # rectangular de orden 2 por 3
D_EJ = [[2, 0, 0], [0, -1, 0], [0, 0, 5]]      # diagonal y cuadrada
F_EJ = [[3, 0, 0], [0, 7, 0]]                  # diagonal de orden 2 por 3
G_EJ = [[4, 0], [0, 1], [0, 0]]                # diagonal de orden 3 por 2
S_EJ = [[3, 1, 7], [1, 2, 9], [7, 9, 1]]       # simétrica (transparencia "Matrices transpuestas")


def matriz(filas, color=WHITE, escala=0.8, h_buff=1.0):
    m = IntegerMatrix(filas, v_buff=0.62, h_buff=h_buff)
    m.get_entries().set_color(color)
    return m.scale(escala)


def con_nombre(tex, mob, font_size=48):
    return VGroup(MathTex(tex, tex_template=myTemplate, font_size=font_size), mob).arrange(RIGHT, buff=0.2)


def diagonal(m):
    """Las componentes de la diagonal principal de la matriz m (también si es rectangular)."""
    filas = m.get_rows()
    return [filas[k][k] for k in range(min(len(filas), len(filas[0])))]


def resalta(escena, mobs, color=COLOR_ESCALAR, factor=1.3, run_time=0.3):
    """Resaltado inmediato y sostenido (color y tamaño), sin la subida lenta de Indicate."""
    escena.play(*[x.animate.set_color(color).scale(factor) for x in mobs], run_time=run_time)


def apaga(escena, mobs, color=WHITE, factor=1.3, run_time=0.3):
    escena.play(*[x.animate.set_color(color).scale(1/factor) for x in mobs], run_time=run_time)


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


def construye_transpuesta(escena, M, MT, nombreT=None, run_time=0.6):
    """Ejemplo de transposición: cada fila de M viaja a la columna del mismo índice de MT, una a una."""
    escena.play(*([FadeIn(nombreT)] if nombreT is not None else []), FadeIn(MT.get_brackets()), run_time=0.5)
    filas, cols = M.get_rows(), MT.get_columns()
    for r in range(len(filas)):
        escena.play(*[TransformFromCopy(filas[r][c], cols[r][c]) for c in range(len(filas[r]))], run_time=run_time)


def rotulo(texto, junto_a, x=None, font_size=28):
    """Rótulo gris pequeño a la derecha de una línea (la regla que justifica el paso)."""
    r = Tex(texto, tex_template=myTemplate, font_size=font_size, color=GRAY_B)
    r.next_to(junto_a, RIGHT, buff=0.6)
    if x is not None:
        r.shift((x - r.get_left()[0])*RIGHT)
    return r


CAMPANITA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos", "campanita.wav")   # suena al subir un contador


class Panel:
    """Panel de herramientas como el de V06-V07 (copia del PanelV10 de V10), con una pieza a cada lado:
    [(cabecera, clave, fórmula), ...]. Pista (amarillo y recuadro), parpadeo antes de cada paso y
    contador de usos con campanita."""
    def __init__(self, escena, piezas, y_sup=2.95, font_size=36):
        self.escena, self.piezas, self.usos, self.contadores = escena, {}, {}, {}
        self.marcos = VGroup()
        lados = []
        for cab, clave, formula in piezas:
            m = MathTex(*formula, tex_template=myTemplate, font_size=font_size) if isinstance(formula, (list, tuple)) \
                else MathTex(formula, tex_template=myTemplate, font_size=font_size)
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

class L01_V11_TiposDeMatrices(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        C, R = matriz(C_EJ), matriz(R_EJ)
        r_C = Tex(r"$3\times 3$", font_size=34, color=GRAY_B)
        r_R = Tex(r"$2\times 3$", font_size=34, color=GRAY_B)
        gC, gR = VGroup(C, r_C).arrange(DOWN, buff=0.45), VGroup(R, r_R).arrange(DOWN, buff=0.45)
        VGroup(gC, gR).arrange(RIGHT, buff=2.0, aligned_edge=DOWN).move_to([0, -0.5, 0])
        n_C = Tex(tr("cuadrada, de orden 3", "square, of order 3"), font_size=34, color=GRAY_B).move_to(r_C)
        n_R = Tex(tr(r"rectangular, de orden $2\times 3$", r"rectangular, of order $2\times 3$"), font_size=34, color=GRAY_B).move_to(r_R)
        
        with self.voiceover(text=tr("""En este vídeo vamos a dar nombre a distintos tipos de matrices, según su forma y la disposición de sus componentes.""",
                                    """In this video we are going to name different types of matrices, according to their shape and the arrangement of their components.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        with self.voiceover(text=tr("""Una matriz es cuadrada cuando tiene el mismo número de filas que de columnas.""",
                                    """A matrix is square when it has the same number of rows as columns.""")) as tracker:
            self.play(FadeIn(C), run_time=1)
            self.play(FadeIn(r_C), run_time=0.6)
        
        with self.voiceover(text=tr("""Como el número de filas y el de columnas coinciden, su orden se indica con un solo número. <bookmark mark='o'/> Así, decir que una matriz es de orden 'n', a secas, ya indica que es cuadrada.""",
                                    """Since the number of rows and the number of columns are the same, its order is given with a single number. <bookmark mark='o'/> So saying just that a matrix is of order 'n' already tells us that it is square.""")) as tracker:
            self.wait_until_bookmark("o")
            self.play(FadeTransform(r_C, n_C), run_time=1)
        
        with self.voiceover(text=tr("""Las matrices que no son cuadradas se llaman rectangulares. <bookmark mark='r'/> Para indicar su orden hacen falta los dos números.""",
                                    """Matrices that are not square are called rectangular. <bookmark mark='r'/> To give their order we need both numbers.""")) as tracker:
            self.play(FadeIn(R), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(n_R), run_time=0.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        # primero la diagonal de una matriz cualquiera; la cabecera cambia al definir las matrices diagonales (Marcos, 2026-11-02)
        cab_diag = Tex(tr("Diagonal de una matriz", "Diagonal of a matrix"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        cabecera = Tex(tr("Matrices diagonales", "Diagonal matrices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        C = matriz(C_EJ).move_to([-2.2, 0.0, 0])
        diag_C = diagonal(C)
        fuera_C = [x for x in C.get_entries() if x not in diag_C]
        # \eleM{A}{i}{i} tiene cinco glifos (i | A | i): solo cambian los índices (0 y 4) y |A| no se mueve.
        # Partir la fórmula para TransformMatchingTex cambiaba el espaciado del libro (Marcos, 2026-11-02).
        def componente(k):
            return MathTex(rf"\eleM{{A}}{{{k}}}{{{k}}}", tex_template=myTemplate, font_size=56)
        a_ii = componente("i").move_to([2.6, 0.0, 0])
        a_kk = [componente(str(k)) for k in (1, 2, 3)]
        a_ii_fin = componente("i")
        for m in a_kk + [a_ii_fin]:
            m.shift(a_ii[0][2].get_center() - m[0][2].get_center())   # la A, en el mismo sitio
        
        D, F, G = matriz(D_EJ), matriz(F_EJ), matriz(G_EJ)
        ordenes = [r"$3\times 3$", r"$2\times 3$", r"$3\times 2$"]
        ejemplos = VGroup(*[VGroup(m, Tex(o, font_size=32, color=GRAY_B)).arrange(DOWN, buff=0.35) for m, o in zip((D, F, G), ordenes)])
        ejemplos.arrange(RIGHT, buff=1.1, aligned_edge=DOWN).move_to([-0.4, 0.4, 0])
        for m in (D, F, G):
            for x in diagonal(m):
                x.set_color(COLOR_ESCALAR)
        om = omega("duda", mira=UL, alto=1.2).to_corner(DR, buff=0.3)
        globo = bocadillo(tr(r"¿Diagonal, luego cuadrada?", r"Diagonal, hence square?"), om, ancho=3.4)
        cero = con_nombre(r"\Mat{0}=", matriz([[0, 0, 0], [0, 0, 0]])).move_to([0, 1.3, 0])
        I2 = con_nombre(r"\Matdim{I}{2}{2}=", matriz([[1, 0], [0, 1]])).move_to([-3.0, -1.6, 0])
        I3 = con_nombre(r"\Matdim{I}{3}{3}=", matriz([[1, 0, 0], [0, 1, 0], [0, 0, 1]])).move_to([3.0, -1.6, 0])
        unos = [x for I in (I2, I3) for x in diagonal(I[1])]
        
        with self.voiceover(text=tr("""La diagonal principal de una matriz la forman <bookmark mark='g'/> las componentes cuyos dos índices son iguales: <bookmark mark='a'/> la de la primera fila y la primera columna, <bookmark mark='b'/> la de la segunda fila y la segunda columna, <bookmark mark='c'/> y así sucesivamente.""",
                                    """The main diagonal of a matrix is made up of <bookmark mark='g'/> the components whose two indices are equal: <bookmark mark='a'/> the one in the first row and the first column, <bookmark mark='b'/> the one in the second row and the second column, <bookmark mark='c'/> and so on.""")) as tracker:
            self.play(Write(cab_diag), FadeIn(C), run_time=1)
            self.wait_until_bookmark("g")
            # la diagonal en amarillo y lo de fuera atenuado, a la vez que aparece i|A|i
            self.play(Write(a_ii), *[x.animate.set_color(COLOR_ESCALAR) for x in diag_C],
                      *[x.animate.set_opacity(0.3) for x in fuera_C], run_time=1)
            actual = a_ii
            for k, marca in enumerate(["a", "b", "c"]):
                self.wait_until_bookmark(marca)
                # i|A|i pasa a k|A|k mientras la componente k crece
                self.play(diag_C[k].animate.scale(1.35), *([diag_C[k-1].animate.scale(1/1.35)] if k else []),
                          FadeTransform(actual[0][0], a_kk[k][0][0]), FadeTransform(actual[0][4], a_kk[k][0][4]), run_time=0.4)
                self.remove(actual, *actual[0]); self.add(a_kk[k])
                actual = a_kk[k]
            self.wait(0.6)
            self.play(diag_C[2].animate.scale(1/1.35), FadeTransform(actual[0][0], a_ii_fin[0][0]),
                      FadeTransform(actual[0][4], a_ii_fin[0][4]), run_time=0.5)
            self.remove(actual, *actual[0]); self.add(a_ii_fin)
        
        with self.voiceover(text=tr("""Una matriz es diagonal cuando todas las componentes fuera de su diagonal principal son nulas. <bookmark mark='d'/> Por ejemplo, esta matriz de orden tres.""",
                                    """A matrix is diagonal when all the components outside its main diagonal are zero. <bookmark mark='d'/> For example, this matrix of order three.""")) as tracker:
            self.play(FadeOut(C), FadeOut(a_ii_fin), ReplacementTransform(cab_diag, cabecera), run_time=0.8)
            self.wait_until_bookmark("d")
            self.play(FadeIn(ejemplos[0]), run_time=1)
        
        with self.voiceover(text=tr("""Omega cree que una matriz diagonal tiene que ser cuadrada.""",
                                    """Omega thinks that a diagonal matrix has to be square.""")) as tracker:
            entra(self, om)
            self.play(FadeIn(globo, scale=0.8), run_time=0.6)
        
        with self.voiceover(text=tr("""Pero la definición solo exige ceros fuera de la diagonal principal: <bookmark mark='f'/> estas dos matrices rectangulares también son diagonales.""",
                                    """But the definition only asks for zeros outside the main diagonal: <bookmark mark='f'/> these two rectangular matrices are diagonal too.""")) as tracker:
            self.play(FadeOut(globo), run_time=0.4)
            self.wait_until_bookmark("f")
            cambia(self, om, "sorpresa")
            self.play(FadeIn(ejemplos[1]), FadeIn(ejemplos[2]), run_time=1)
            cambia(self, om, "normal", mira=UL)   # la sorpresa dura un instante; ahora atiende
        
        with self.voiceover(text=tr("""Las componentes de la diagonal principal pueden ser cualquier número, también cero. <bookmark mark='z'/> Por eso la matriz nula, que tiene ceros en todas partes, también es diagonal.""",
                                    """The components of the main diagonal can be any number, zero included. <bookmark mark='z'/> That is why the zero matrix, with zeros everywhere, is diagonal too.""")) as tracker:
            self.play(FadeOut(ejemplos), FadeOut(om), run_time=0.8)
            self.wait_until_bookmark("z")
            self.play(FadeIn(cero), run_time=1)
        
        with self.voiceover(text=tr("""Una matriz diagonal muy importante es la matriz identidad: <bookmark mark='i'/> es cuadrada, <bookmark mark='u'/> y todas las componentes de su diagonal principal son unos. <bookmark mark='e'/> Se escribe con la letra i mayúscula en negrita, con su orden debajo cuando hace falta.""",
                                    """A very important diagonal matrix is the identity matrix: <bookmark mark='i'/> it is square, <bookmark mark='u'/> and all the components of its main diagonal are ones. <bookmark mark='e'/> It is written with a bold capital letter I, with its order below when needed.""")) as tracker:
            self.wait_until_bookmark("i")
            self.play(FadeIn(I2[1]), FadeIn(I3[1]), run_time=1)
            self.wait_until_bookmark("u")
            resalta(self, unos)
            self.wait_until_bookmark("e")
            self.play(Write(I2[0]), Write(I3[0]), run_time=1)
            apaga(self, unos)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Matrices simétricas", "Symmetric matrices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        defin = MathTex(r"\Mat{A}", r"=", r"\MatT{A}", tex_template=myTemplate, font_size=56).move_to([0, 2.0, 0])
        o_A = MathTex(r"\Mat{A}\in\R[m\times n]", tex_template=myTemplate, font_size=48)
        o_T = MathTex(r"\MatT{A}\in\R[n\times m]", tex_template=myTemplate, font_size=48)
        o_ig = MathTex(r"\Rightarrow\quad m=n", tex_template=myTemplate, font_size=48)
        ordenes = VGroup(o_A, o_T, o_ig).arrange(RIGHT, buff=0.9).move_to([0, 0.3, 0])
        # ejemplos antes de lo general (Marcos, 2026-11-02): una simétrica y una rectangular que no puede serlo
        S1, S1T = matriz(S_EJ), matriz([list(f) for f in zip(*S_EJ)])
        ej_S = VGroup(con_nombre(r"\Mat{S}=", S1), con_nombre(r"\MatT{S}=", S1T)).arrange(RIGHT, buff=1.2).move_to([0, -0.5, 0])
        R1, R1T = matriz(R_EJ), matriz([list(f) for f in zip(*R_EJ)])
        ej_R = VGroup(con_nombre(r"\Mat{B}=", R1), con_nombre(r"\MatT{B}=", R1T)).arrange(RIGHT, buff=1.2).move_to([0, -0.3, 0])
        ord_R = VGroup(Tex(r"$2\times 3$", font_size=32, color=GRAY_B).next_to(R1, DOWN, buff=0.35),
                       Tex(r"$3\times 2$", font_size=32, color=GRAY_B).next_to(R1T, DOWN, buff=0.35))
        # igualdad de matrices componente a componente (consecuencia de V09; no se había dicho)
        igualdad = MathTex(r"\Mat{A}=\Mat{B}", r"\iff", r"\eleM{A}{i}{j}=\eleM{B}{i}{j}", tex_template=myTemplate, font_size=52).move_to([0, 0.3, 0])
        igualdad_nota = Tex(tr(r"del mismo orden, para todo $i$ y todo $j$", r"of the same order, for all $i$ and $j$"),
                            font_size=30, color=GRAY_B).next_to(igualdad, DOWN, buff=0.4)
        # Glifos: i | A | j  =  i | ( A T ) | j  =  j | A | i
        cadena = MathTex(r"\eleM{A}{i}{j}", r"=", r"\eleMT{A}{i}{j}", r"=", r"\eleM{A}{j}{i}", tex_template=myTemplate, font_size=56).move_to([0, -0.1, 0])
        r1 = Tex(r"$\Mat{A}=\MatT{A}$", tex_template=myTemplate, font_size=28, color=GRAY_B).next_to(cadena[1], UP, buff=0.45)
        r2 = Tex(tr("regla de los índices", "index rule"), font_size=28, color=GRAY_B).next_to(cadena[3], UP, buff=0.45)
        S = matriz(S_EJ).move_to([0, -2.4, 0])
        filas_S = S.get_rows()
        arriba = [filas_S[i][j] for i in range(3) for j in range(3) if i <= j]
        debajo = [(filas_S[j][i], filas_S[i][j]) for i in range(3) for j in range(3) if i > j]   # (origen arriba, destino abajo)
        
        with self.voiceover(text=tr("""Aquí nos sirve la transposición del vídeo anterior: una matriz es simétrica cuando es igual a su transpuesta.""",
                                    """Here the transposition of the previous video comes in: a matrix is symmetric when it is equal to its transpose.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.play(Write(defin), run_time=1.2)
        
        with self.voiceover(text=tr("""Por ejemplo, tomemos esta matriz. <bookmark mark='t'/> Al transponerla, sus filas pasan a ser las columnas de la transpuesta, <bookmark mark='i'/> y obtenemos la misma matriz: es simétrica.""",
                                    """For example, take this matrix. <bookmark mark='t'/> When we transpose it, its rows become the columns of the transpose, <bookmark mark='i'/> and we get the same matrix: it is symmetric.""")) as tracker:
            self.play(FadeIn(ej_S[0]), run_time=0.8)
            self.wait_until_bookmark("t")
            construye_transpuesta(self, S1, S1T, nombreT=ej_S[1][0])
            self.wait_until_bookmark("i")
            self.play(Indicate(S1.get_entries(), color=COLOR_A, scale_factor=1.1), Indicate(S1T.get_entries(), color=COLOR_A, scale_factor=1.1), run_time=1.2)
        
        with self.voiceover(text=tr("""En cambio, esta matriz de orden dos por tres no puede ser simétrica: <bookmark mark='t'/> su transpuesta es de orden tres por dos.""",
                                    """On the other hand, this matrix of order two by three cannot be symmetric: <bookmark mark='t'/> its transpose is of order three by two.""")) as tracker:
            self.play(FadeOut(ej_S), run_time=0.6)
            self.play(FadeIn(ej_R[0]), FadeIn(ord_R[0]), run_time=0.8)
            self.wait_until_bookmark("t")
            construye_transpuesta(self, R1, R1T, nombreT=ej_R[1][0], run_time=0.5)
            self.play(FadeIn(ord_R[1]), run_time=0.5)
        
        with self.voiceover(text=tr("""En general, toda matriz simétrica es cuadrada: <bookmark mark='a'/> si A es de orden 'm' por 'n', <bookmark mark='t'/> su transpuesta es de orden 'n' por 'm', <bookmark mark='i'/> y dos matrices iguales tienen el mismo orden.""",
                                    """In general, every symmetric matrix is square: <bookmark mark='a'/> if A is of order 'm' by 'n', <bookmark mark='t'/> its transpose is of order 'n' by 'm', <bookmark mark='i'/> and two equal matrices have the same order.""")) as tracker:
            self.play(FadeOut(ej_R), FadeOut(ord_R), run_time=0.6)
            self.wait_until_bookmark("a")
            self.play(FadeIn(o_A), run_time=0.8)
            self.wait_until_bookmark("t")
            self.play(FadeIn(o_T), run_time=0.8)
            self.wait_until_bookmark("i")
            self.play(FadeIn(o_ig), run_time=0.8)
        
        with self.voiceover(text=tr("""Dos matrices son iguales cuando lo son sus columnas, <bookmark mark='c'/> y dos columnas lo son cuando tienen las mismas componentes. <bookmark mark='m'/> Así que dos matrices del mismo orden son iguales cuando tienen las mismas componentes.""",
                                    """Two matrices are equal when their columns are, <bookmark mark='c'/> and two columns are equal when they have the same components. <bookmark mark='m'/> So two matrices of the same order are equal when they have the same components.""")) as tracker:
            self.play(FadeOut(ordenes), run_time=0.6)
            self.play(FadeIn(igualdad[0]), run_time=0.8)
            self.wait_until_bookmark("m")
            self.play(FadeIn(igualdad[1]), FadeIn(igualdad[2]), FadeIn(igualdad_nota), run_time=1)
        
        with self.voiceover(text=tr("""Veamos ahora las componentes de A. <bookmark mark='c'/> Como A es igual a su transpuesta, las dos tienen las mismas componentes. <bookmark mark='r'/> Y por la regla de los índices del vídeo anterior, podemos quitar la transposición <bookmark mark='x'/> intercambiando los índices de lado.""",
                                    """Let us now look at the components of A. <bookmark mark='c'/> Since A is equal to its transpose, both have the same components. <bookmark mark='r'/> And by the index rule of the previous video, we can remove the transposition <bookmark mark='x'/> by moving each index to the other side.""")) as tracker:
            self.play(FadeOut(igualdad), FadeOut(igualdad_nota), run_time=0.6)
            self.play(FadeIn(cadena[0]), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(FadeIn(r1), FadeIn(cadena[1]), FadeIn(VGroup(cadena[2][2], cadena[2][4], cadena[2][5])),
                      *[TransformFromCopy(cadena[0][i], cadena[2][j]) for i, j in [(0, 0), (1, 1), (2, 3), (3, 6), (4, 7)]], run_time=1.2)
            self.wait_until_bookmark("r")
            copia = copia_literal(self, cadena[2], cadena[4], cadena[3])
            self.play(FadeIn(r2), run_time=0.5)
            self.wait_until_bookmark("x")
            transforma_copia(self, copia, cadena[4], [(0, 4), (1, 3), (3, 2), (6, 1), (7, 0)], se_van=[2, 4, 5])
        
        with self.voiceover(text=tr("""Así pues, si intercambiamos el índice de la fila y el de la columna, la componente no cambia.""",
                                    """So if we swap the row index and the column index, the component does not change.""")) as tracker:
            ies, jotas = [cadena[0][0], cadena[4][4]], [cadena[0][4], cadena[4][0]]
            resalta(self, ies, factor=1.5)
            resalta(self, jotas, color=COLOR_C, factor=1.5)
            self.wait(1)
            apaga(self, ies, factor=1.5)
            apaga(self, jotas, factor=1.5)
        
        with self.voiceover(text=tr("""Volvamos a la matriz del ejemplo. <bookmark mark='e'/> Basta conocer la diagonal principal y las componentes que hay por encima: <bookmark mark='r'/> las de debajo son su reflejo, como en un espejo.""",
                                    """Back to the matrix of the example. <bookmark mark='e'/> It is enough to know the main diagonal and the components above it: <bookmark mark='r'/> the ones below are their mirror image.""")) as tracker:
            self.play(FadeIn(S.get_brackets()), FadeIn(VGroup(*arriba)), run_time=1)
            self.wait_until_bookmark("e")
            resalta(self, [x for x in arriba if x not in diagonal(S)], color=COLOR_A, factor=1.2)
            self.wait_until_bookmark("r")
            self.play(*[TransformFromCopy(o, d) for o, d in debajo], run_time=1.6)
            self.play(*[d.animate.set_color(COLOR_A) for o, d in debajo], run_time=0.3)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Diagonal y cuadrada, luego simétrica", "Square diagonal, hence symmetric"), font_size=40).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self, [(tr("Matriz diagonal", "Diagonal matrix"), "diag", [r"\eleM{D}{i}{j}", r"=0\quad (i\neq j)"]),
                             (tr("Vídeo anterior", "Previous video"), "regla", r"\eleMT{A}{i}{j}=\eleM{A}{j}{i}")])
        enunciado = VGroup(Tex(tr(r"$\Mat{D}$ diagonal y cuadrada:", r"$\Mat{D}$ square diagonal:"), tex_template=myTemplate, font_size=40),
                           MathTex(r"\MatT{D}", r"=", r"\Mat{D}", tex_template=myTemplate, font_size=48)).arrange(RIGHT, buff=0.4).move_to([0, 1.2, 0])   # bajo el panel: su recuadro no toca los del panel
        # Glifos: i | ( D T ) | i  =  i | D | i
        l1 = MathTex(r"\eleMT{D}{i}{i}", r"=", r"\eleM{D}{i}{i}", tex_template=myTemplate, font_size=52)
        # Glifos: i | ( D T ) | j  =  j | D | i  =  0  =  i | D | j
        l2 = MathTex(r"\eleMT{D}{i}{j}", r"=", r"\eleM{D}{j}{i}", r"=", r"0", r"=", r"\eleM{D}{i}{j}", tex_template=myTemplate, font_size=52)
        columna_de_lineas([l1, l2], x0=-1.2, y0=-0.2, dy=1.3)
        c1 = Tex(r"$i=j$:", font_size=34, color=GRAY_B).next_to(l1, LEFT, buff=0.6)
        c2 = Tex(r"$i\neq j$:", font_size=34, color=GRAY_B).next_to(l2, LEFT, buff=0.6)
        CAMBIO = [(0, 4), (1, 3), (3, 2), (6, 1), (7, 0)]   # quitar la transposición: los índices cambian de lado
        
        D1, D1T = matriz(D_EJ), matriz([list(f) for f in zip(*D_EJ)])
        ej_D = VGroup(con_nombre(r"\Mat{D}=", D1), con_nombre(r"\MatT{D}=", D1T)).arrange(RIGHT, buff=1.2).move_to([0, 0.2, 0])
        
        with self.voiceover(text=tr("""Para terminar, tomemos esta matriz diagonal. <bookmark mark='t'/> Al transponerla, sus filas pasan a ser columnas <bookmark mark='i'/> y, como fuera de la diagonal solo hay ceros, obtenemos la misma matriz.""",
                                    """To finish, take this diagonal matrix. <bookmark mark='t'/> When we transpose it, its rows become columns <bookmark mark='i'/> and, since there are only zeros outside the diagonal, we get the same matrix.""")) as tracker:
            self.play(Write(cabecera), FadeIn(ej_D[0]), run_time=1)
            self.wait_until_bookmark("t")
            construye_transpuesta(self, D1, D1T, nombreT=ej_D[1][0])
            self.wait_until_bookmark("i")
            self.play(Indicate(D1.get_entries(), color=COLOR_A, scale_factor=1.1), Indicate(D1T.get_entries(), color=COLOR_A, scale_factor=1.1), run_time=1.2)
        
        with self.voiceover(text=tr("""El ejemplo solo lo ilustra. Ahora vamos a demostrar que toda matriz diagonal y cuadrada es simétrica.""",
                                    """The example only illustrates it. Now we are going to prove that every square diagonal matrix is symmetric.""")) as tracker:
            self.play(FadeOut(ej_D), run_time=0.6)
            self.play(FadeIn(panel.todo), Write(enunciado), run_time=1.2)
        
        with self.voiceover(text=tr("""Para demostrarlo necesitará <bookmark mark='p'/> la definición de matriz diagonal <bookmark mark='q'/> y la regla de los índices del vídeo anterior.""",
                                    """To prove it you will need <bookmark mark='p'/> the definition of a diagonal matrix <bookmark mark='q'/> and the index rule of the previous video.""")) as tracker:
            self.wait_until_bookmark("p")
            panel.pista("diag")
            self.wait_until_bookmark("q")
            panel.pista("regla")
        
        self.pausa_para_pensar(invitacion=tr("Demuestre que toda matriz diagonal y cuadrada es simétrica.",
                                             "Prove that every square diagonal matrix is symmetric."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que toda matriz diagonal y cuadrada es igual a su transpuesta.",
                                                 "Pause the video and try to prove that every square diagonal matrix is equal to its transpose."))
        
        with self.voiceover(text=tr("""Como D es cuadrada, su transpuesta tiene el mismo orden, así que podemos comparar las componentes de las dos una a una.""",
                                    """Since D is square, its transpose has the same order, so we can compare their components one by one.""")) as tracker:
            self.play(Indicate(enunciado[0], color=COLOR_ESCALAR, scale_factor=1.08), run_time=1.2)
        
        with self.voiceover(text=tr("""En la diagonal principal, los dos índices son iguales, <bookmark mark='a'/> así que la regla de los índices no cambia nada.""",
                                    """On the main diagonal the two indices are equal, <bookmark mark='a'/> so the index rule changes nothing.""")) as tracker:
            self.play(FadeIn(c1), TransformFromCopy(enunciado[1][0], l1[0]), run_time=1)
            panel.senala("regla")
            self.wait_until_bookmark("a")
            copia = copia_literal(self, l1[0], l1[2], l1[1])
            transforma_copia(self, copia, l1[2], CAMBIO, se_van=[2, 4, 5])
            panel.cuenta("regla")
        
        with self.voiceover(text=tr("""Fuera de la diagonal principal, los índices son distintos. <bookmark mark='a'/> Por la regla de los índices, podemos quitar la transposición <bookmark mark='x'/> intercambiando los índices de lado.""",
                                    """Outside the main diagonal, the indices are different. <bookmark mark='a'/> By the index rule, we can remove the transposition <bookmark mark='x'/> by moving each index to the other side.""")) as tracker:
            self.play(FadeIn(c2), TransformFromCopy(enunciado[1][0], l2[0]), run_time=1)
            panel.senala("regla")
            self.wait_until_bookmark("a")
            copia = copia_literal(self, l2[0], l2[2], l2[1])
            self.wait_until_bookmark("x")
            transforma_copia(self, copia, l2[2], CAMBIO, se_van=[2, 4, 5])
            panel.cuenta("regla")
        
        with self.voiceover(text=tr("""Por la definición de matriz diagonal, <bookmark mark='a'/> la componente que hemos obtenido es cero. <bookmark mark='b'/> Por la misma razón, también es cero la de la fila i y la columna j.""",
                                    """By the definition of a diagonal matrix, <bookmark mark='a'/> the component we have obtained is zero. <bookmark mark='b'/> For the same reason, the one in row i and column j is zero too.""")) as tracker:
            panel.senala("diag")
            self.wait_until_bookmark("a")
            self.play(FadeIn(l2[3]), ReplacementTransform(l2[2].copy(), l2[4]), run_time=1)
            panel.cuenta("diag")
            self.wait_until_bookmark("b")
            self.play(FadeIn(l2[5]), TransformFromCopy(panel.piezas["diag"][0], l2[6]), run_time=1.2)
            panel.cuenta("diag")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Así que D y su transpuesta tienen las mismas componentes, <bookmark mark='ok'/> y por tanto son iguales.""",
                                    """So D and its transpose have the same components, <bookmark mark='ok'/> and therefore they are equal.""")) as tracker:
            self.play(Indicate(VGroup(l1, l2), color=COLOR_ESCALAR, scale_factor=1.04), run_time=1)
            self.wait_until_bookmark("ok")
            marco = SurroundingRectangle(enunciado[1], color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
            self.play(Create(marco), Indicate(enunciado[1], color=COLOR_RESULTADO, scale_factor=1.15), run_time=1.5)
        
        with self.voiceover(text=tr("""Hemos usado dos veces la regla de los índices y dos veces la definición de matriz diagonal. En particular, la matriz identidad, que es diagonal y cuadrada, es simétrica.""",
                                    """We have used the index rule twice and the definition of a diagonal matrix twice. In particular, the identity matrix, which is a square diagonal matrix, is symmetric.""")) as tracker:
            self.play(*[Indicate(panel.contadores[c], color=COLOR_ESCALAR) for c in ("regla", "diag")], run_time=1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [r"\Mat{A}\in\R[n\times n]", r"\eleM{D}{i}{j}=0\quad (i\neq j)", r"\eleM{I}{i}{i}=1,\quad \eleM{I}{i}{j}=0\quad (i\neq j)",
                    r"\Mat{A}=\MatT{A}\quad\Rightarrow\quad \eleM{A}{i}{j}=\eleM{A}{j}{i}", r"\MatT{D}=\Mat{D}"]
        rotulos = [tr("cuadrada: tantas filas como columnas (de orden $n$)", "square: as many rows as columns (of order $n$)"),
                   tr("diagonal: ceros fuera de la diagonal principal", "diagonal: zeros outside the main diagonal"),
                   tr("identidad: cuadrada y diagonal, con unos en la diagonal", "identity: square and diagonal, with ones on the diagonal"),
                   tr("simétrica: igual a su transpuesta", "symmetric: equal to its transpose"),
                   tr("si $\\Mat{D}$ es diagonal y cuadrada, es simétrica", "if $\\Mat{D}$ is square and diagonal, it is symmetric")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=40), Tex(r, tex_template=myTemplate, font_size=26, color=GRAY_B)).arrange(DOWN, buff=0.15)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.3).move_to([0, -0.4, 0])
        
        with self.voiceover(text=tr("""Resumamos. Una matriz es cuadrada si tiene tantas filas como columnas, <bookmark mark='d'/> y es diagonal si todas sus componentes fuera de la diagonal principal son nulas. <bookmark mark='i'/> La matriz identidad es cuadrada y diagonal, con unos en la diagonal principal.""",
                                    """Let us sum up. A matrix is square if it has as many rows as columns, <bookmark mark='d'/> and it is diagonal if all its components outside the main diagonal are zero. <bookmark mark='i'/> The identity matrix is square and diagonal, with ones on the main diagonal.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("d")
            self.play(FadeIn(filas[1]), run_time=0.8)
            self.wait_until_bookmark("i")
            self.play(FadeIn(filas[2]), run_time=0.8)
        
        with self.voiceover(text=tr("""Una matriz es simétrica si es igual a su transpuesta. Entonces es cuadrada, y sus componentes no cambian al intercambiar los índices. <bookmark mark='x'/> Y toda matriz diagonal y cuadrada es simétrica.""",
                                    """A matrix is symmetric if it is equal to its transpose. Then it is square, and its components do not change when the indices are swapped. <bookmark mark='x'/> And every square diagonal matrix is symmetric.""")) as tracker:
            self.play(FadeIn(filas[3]), run_time=0.8)
            self.wait_until_bookmark("x")
            self.play(FadeIn(filas[4]), run_time=0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos las operaciones con matrices: la suma y el producto por un escalar.""",
                                    """In the next video we will see the operations with matrices: addition and multiplication by a scalar.""")) as tracker:
            pass
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos_finales()


class L01_V11_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class L01_V11_E01_Cuadradas(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        C, R = matriz(C_EJ), matriz(R_EJ)
        r_C = Tex(r"$3\times 3$", font_size=34, color=GRAY_B)
        r_R = Tex(r"$2\times 3$", font_size=34, color=GRAY_B)
        gC, gR = VGroup(C, r_C).arrange(DOWN, buff=0.45), VGroup(R, r_R).arrange(DOWN, buff=0.45)
        VGroup(gC, gR).arrange(RIGHT, buff=2.0, aligned_edge=DOWN).move_to([0, -0.5, 0])
        n_C = Tex(tr("cuadrada, de orden 3", "square, of order 3"), font_size=34, color=GRAY_B).move_to(r_C)
        n_R = Tex(tr(r"rectangular, de orden $2\times 3$", r"rectangular, of order $2\times 3$"), font_size=34, color=GRAY_B).move_to(r_R)
        
        with self.voiceover(text=tr("""En este vídeo vamos a dar nombre a distintos tipos de matrices, según su forma y la disposición de sus componentes.""",
                                    """In this video we are going to name different types of matrices, according to their shape and the arrangement of their components.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        with self.voiceover(text=tr("""Una matriz es cuadrada cuando tiene el mismo número de filas que de columnas.""",
                                    """A matrix is square when it has the same number of rows as columns.""")) as tracker:
            self.play(FadeIn(C), run_time=1)
            self.play(FadeIn(r_C), run_time=0.6)
        
        with self.voiceover(text=tr("""Como el número de filas y el de columnas coinciden, su orden se indica con un solo número. <bookmark mark='o'/> Así, decir que una matriz es de orden 'n', a secas, ya indica que es cuadrada.""",
                                    """Since the number of rows and the number of columns are the same, its order is given with a single number. <bookmark mark='o'/> So saying just that a matrix is of order 'n' already tells us that it is square.""")) as tracker:
            self.wait_until_bookmark("o")
            self.play(FadeTransform(r_C, n_C), run_time=1)
        
        with self.voiceover(text=tr("""Las matrices que no son cuadradas se llaman rectangulares. <bookmark mark='r'/> Para indicar su orden hacen falta los dos números.""",
                                    """Matrices that are not square are called rectangular. <bookmark mark='r'/> To give their order we need both numbers.""")) as tracker:
            self.play(FadeIn(R), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(n_R), run_time=0.8)
        
        self.pausa_media()


class L01_V11_E02_Diagonales(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        # primero la diagonal de una matriz cualquiera; la cabecera cambia al definir las matrices diagonales (Marcos, 2026-11-02)
        cab_diag = Tex(tr("Diagonal de una matriz", "Diagonal of a matrix"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        cabecera = Tex(tr("Matrices diagonales", "Diagonal matrices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        C = matriz(C_EJ).move_to([-2.2, 0.0, 0])
        diag_C = diagonal(C)
        fuera_C = [x for x in C.get_entries() if x not in diag_C]
        # \eleM{A}{i}{i} tiene cinco glifos (i | A | i): solo cambian los índices (0 y 4) y |A| no se mueve.
        # Partir la fórmula para TransformMatchingTex cambiaba el espaciado del libro (Marcos, 2026-11-02).
        def componente(k):
            return MathTex(rf"\eleM{{A}}{{{k}}}{{{k}}}", tex_template=myTemplate, font_size=56)
        a_ii = componente("i").move_to([2.6, 0.0, 0])
        a_kk = [componente(str(k)) for k in (1, 2, 3)]
        a_ii_fin = componente("i")
        for m in a_kk + [a_ii_fin]:
            m.shift(a_ii[0][2].get_center() - m[0][2].get_center())   # la A, en el mismo sitio
        
        D, F, G = matriz(D_EJ), matriz(F_EJ), matriz(G_EJ)
        ordenes = [r"$3\times 3$", r"$2\times 3$", r"$3\times 2$"]
        ejemplos = VGroup(*[VGroup(m, Tex(o, font_size=32, color=GRAY_B)).arrange(DOWN, buff=0.35) for m, o in zip((D, F, G), ordenes)])
        ejemplos.arrange(RIGHT, buff=1.1, aligned_edge=DOWN).move_to([-0.4, 0.4, 0])
        for m in (D, F, G):
            for x in diagonal(m):
                x.set_color(COLOR_ESCALAR)
        om = omega("duda", mira=UL, alto=1.2).to_corner(DR, buff=0.3)
        globo = bocadillo(tr(r"¿Diagonal, luego cuadrada?", r"Diagonal, hence square?"), om, ancho=3.4)
        cero = con_nombre(r"\Mat{0}=", matriz([[0, 0, 0], [0, 0, 0]])).move_to([0, 1.3, 0])
        I2 = con_nombre(r"\Matdim{I}{2}{2}=", matriz([[1, 0], [0, 1]])).move_to([-3.0, -1.6, 0])
        I3 = con_nombre(r"\Matdim{I}{3}{3}=", matriz([[1, 0, 0], [0, 1, 0], [0, 0, 1]])).move_to([3.0, -1.6, 0])
        unos = [x for I in (I2, I3) for x in diagonal(I[1])]
        
        with self.voiceover(text=tr("""La diagonal principal de una matriz la forman <bookmark mark='g'/> las componentes cuyos dos índices son iguales: <bookmark mark='a'/> la de la primera fila y la primera columna, <bookmark mark='b'/> la de la segunda fila y la segunda columna, <bookmark mark='c'/> y así sucesivamente.""",
                                    """The main diagonal of a matrix is made up of <bookmark mark='g'/> the components whose two indices are equal: <bookmark mark='a'/> the one in the first row and the first column, <bookmark mark='b'/> the one in the second row and the second column, <bookmark mark='c'/> and so on.""")) as tracker:
            self.play(Write(cab_diag), FadeIn(C), run_time=1)
            self.wait_until_bookmark("g")
            # la diagonal en amarillo y lo de fuera atenuado, a la vez que aparece i|A|i
            self.play(Write(a_ii), *[x.animate.set_color(COLOR_ESCALAR) for x in diag_C],
                      *[x.animate.set_opacity(0.3) for x in fuera_C], run_time=1)
            actual = a_ii
            for k, marca in enumerate(["a", "b", "c"]):
                self.wait_until_bookmark(marca)
                # i|A|i pasa a k|A|k mientras la componente k crece
                self.play(diag_C[k].animate.scale(1.35), *([diag_C[k-1].animate.scale(1/1.35)] if k else []),
                          FadeTransform(actual[0][0], a_kk[k][0][0]), FadeTransform(actual[0][4], a_kk[k][0][4]), run_time=0.4)
                self.remove(actual, *actual[0]); self.add(a_kk[k])
                actual = a_kk[k]
            self.wait(0.6)
            self.play(diag_C[2].animate.scale(1/1.35), FadeTransform(actual[0][0], a_ii_fin[0][0]),
                      FadeTransform(actual[0][4], a_ii_fin[0][4]), run_time=0.5)
            self.remove(actual, *actual[0]); self.add(a_ii_fin)
        
        with self.voiceover(text=tr("""Una matriz es diagonal cuando todas las componentes fuera de su diagonal principal son nulas. <bookmark mark='d'/> Por ejemplo, esta matriz de orden tres.""",
                                    """A matrix is diagonal when all the components outside its main diagonal are zero. <bookmark mark='d'/> For example, this matrix of order three.""")) as tracker:
            self.play(FadeOut(C), FadeOut(a_ii_fin), ReplacementTransform(cab_diag, cabecera), run_time=0.8)
            self.wait_until_bookmark("d")
            self.play(FadeIn(ejemplos[0]), run_time=1)
        
        with self.voiceover(text=tr("""Omega cree que una matriz diagonal tiene que ser cuadrada.""",
                                    """Omega thinks that a diagonal matrix has to be square.""")) as tracker:
            entra(self, om)
            self.play(FadeIn(globo, scale=0.8), run_time=0.6)
        
        with self.voiceover(text=tr("""Pero la definición solo exige ceros fuera de la diagonal principal: <bookmark mark='f'/> estas dos matrices rectangulares también son diagonales.""",
                                    """But the definition only asks for zeros outside the main diagonal: <bookmark mark='f'/> these two rectangular matrices are diagonal too.""")) as tracker:
            self.play(FadeOut(globo), run_time=0.4)
            self.wait_until_bookmark("f")
            cambia(self, om, "sorpresa")
            self.play(FadeIn(ejemplos[1]), FadeIn(ejemplos[2]), run_time=1)
            cambia(self, om, "normal", mira=UL)   # la sorpresa dura un instante; ahora atiende
        
        with self.voiceover(text=tr("""Las componentes de la diagonal principal pueden ser cualquier número, también cero. <bookmark mark='z'/> Por eso la matriz nula, que tiene ceros en todas partes, también es diagonal.""",
                                    """The components of the main diagonal can be any number, zero included. <bookmark mark='z'/> That is why the zero matrix, with zeros everywhere, is diagonal too.""")) as tracker:
            self.play(FadeOut(ejemplos), FadeOut(om), run_time=0.8)
            self.wait_until_bookmark("z")
            self.play(FadeIn(cero), run_time=1)
        
        with self.voiceover(text=tr("""Una matriz diagonal muy importante es la matriz identidad: <bookmark mark='i'/> es cuadrada, <bookmark mark='u'/> y todas las componentes de su diagonal principal son unos. <bookmark mark='e'/> Se escribe con la letra i mayúscula en negrita, con su orden debajo cuando hace falta.""",
                                    """A very important diagonal matrix is the identity matrix: <bookmark mark='i'/> it is square, <bookmark mark='u'/> and all the components of its main diagonal are ones. <bookmark mark='e'/> It is written with a bold capital letter I, with its order below when needed.""")) as tracker:
            self.wait_until_bookmark("i")
            self.play(FadeIn(I2[1]), FadeIn(I3[1]), run_time=1)
            self.wait_until_bookmark("u")
            resalta(self, unos)
            self.wait_until_bookmark("e")
            self.play(Write(I2[0]), Write(I3[0]), run_time=1)
            apaga(self, unos)
        
        self.pausa_media()


class L01_V11_E03_Simetricas(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Matrices simétricas", "Symmetric matrices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        defin = MathTex(r"\Mat{A}", r"=", r"\MatT{A}", tex_template=myTemplate, font_size=56).move_to([0, 2.0, 0])
        o_A = MathTex(r"\Mat{A}\in\R[m\times n]", tex_template=myTemplate, font_size=48)
        o_T = MathTex(r"\MatT{A}\in\R[n\times m]", tex_template=myTemplate, font_size=48)
        o_ig = MathTex(r"\Rightarrow\quad m=n", tex_template=myTemplate, font_size=48)
        ordenes = VGroup(o_A, o_T, o_ig).arrange(RIGHT, buff=0.9).move_to([0, 0.3, 0])
        # ejemplos antes de lo general (Marcos, 2026-11-02): una simétrica y una rectangular que no puede serlo
        S1, S1T = matriz(S_EJ), matriz([list(f) for f in zip(*S_EJ)])
        ej_S = VGroup(con_nombre(r"\Mat{S}=", S1), con_nombre(r"\MatT{S}=", S1T)).arrange(RIGHT, buff=1.2).move_to([0, -0.5, 0])
        R1, R1T = matriz(R_EJ), matriz([list(f) for f in zip(*R_EJ)])
        ej_R = VGroup(con_nombre(r"\Mat{B}=", R1), con_nombre(r"\MatT{B}=", R1T)).arrange(RIGHT, buff=1.2).move_to([0, -0.3, 0])
        ord_R = VGroup(Tex(r"$2\times 3$", font_size=32, color=GRAY_B).next_to(R1, DOWN, buff=0.35),
                       Tex(r"$3\times 2$", font_size=32, color=GRAY_B).next_to(R1T, DOWN, buff=0.35))
        # igualdad de matrices componente a componente (consecuencia de V09; no se había dicho)
        igualdad = MathTex(r"\Mat{A}=\Mat{B}", r"\iff", r"\eleM{A}{i}{j}=\eleM{B}{i}{j}", tex_template=myTemplate, font_size=52).move_to([0, 0.3, 0])
        igualdad_nota = Tex(tr(r"del mismo orden, para todo $i$ y todo $j$", r"of the same order, for all $i$ and $j$"),
                            font_size=30, color=GRAY_B).next_to(igualdad, DOWN, buff=0.4)
        # Glifos: i | A | j  =  i | ( A T ) | j  =  j | A | i
        cadena = MathTex(r"\eleM{A}{i}{j}", r"=", r"\eleMT{A}{i}{j}", r"=", r"\eleM{A}{j}{i}", tex_template=myTemplate, font_size=56).move_to([0, -0.1, 0])
        r1 = Tex(r"$\Mat{A}=\MatT{A}$", tex_template=myTemplate, font_size=28, color=GRAY_B).next_to(cadena[1], UP, buff=0.45)
        r2 = Tex(tr("regla de los índices", "index rule"), font_size=28, color=GRAY_B).next_to(cadena[3], UP, buff=0.45)
        S = matriz(S_EJ).move_to([0, -2.4, 0])
        filas_S = S.get_rows()
        arriba = [filas_S[i][j] for i in range(3) for j in range(3) if i <= j]
        debajo = [(filas_S[j][i], filas_S[i][j]) for i in range(3) for j in range(3) if i > j]   # (origen arriba, destino abajo)
        
        with self.voiceover(text=tr("""Aquí nos sirve la transposición del vídeo anterior: una matriz es simétrica cuando es igual a su transpuesta.""",
                                    """Here the transposition of the previous video comes in: a matrix is symmetric when it is equal to its transpose.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.play(Write(defin), run_time=1.2)
        
        with self.voiceover(text=tr("""Por ejemplo, tomemos esta matriz. <bookmark mark='t'/> Al transponerla, sus filas pasan a ser las columnas de la transpuesta, <bookmark mark='i'/> y obtenemos la misma matriz: es simétrica.""",
                                    """For example, take this matrix. <bookmark mark='t'/> When we transpose it, its rows become the columns of the transpose, <bookmark mark='i'/> and we get the same matrix: it is symmetric.""")) as tracker:
            self.play(FadeIn(ej_S[0]), run_time=0.8)
            self.wait_until_bookmark("t")
            construye_transpuesta(self, S1, S1T, nombreT=ej_S[1][0])
            self.wait_until_bookmark("i")
            self.play(Indicate(S1.get_entries(), color=COLOR_A, scale_factor=1.1), Indicate(S1T.get_entries(), color=COLOR_A, scale_factor=1.1), run_time=1.2)
        
        with self.voiceover(text=tr("""En cambio, esta matriz de orden dos por tres no puede ser simétrica: <bookmark mark='t'/> su transpuesta es de orden tres por dos.""",
                                    """On the other hand, this matrix of order two by three cannot be symmetric: <bookmark mark='t'/> its transpose is of order three by two.""")) as tracker:
            self.play(FadeOut(ej_S), run_time=0.6)
            self.play(FadeIn(ej_R[0]), FadeIn(ord_R[0]), run_time=0.8)
            self.wait_until_bookmark("t")
            construye_transpuesta(self, R1, R1T, nombreT=ej_R[1][0], run_time=0.5)
            self.play(FadeIn(ord_R[1]), run_time=0.5)
        
        with self.voiceover(text=tr("""En general, toda matriz simétrica es cuadrada: <bookmark mark='a'/> si A es de orden 'm' por 'n', <bookmark mark='t'/> su transpuesta es de orden 'n' por 'm', <bookmark mark='i'/> y dos matrices iguales tienen el mismo orden.""",
                                    """In general, every symmetric matrix is square: <bookmark mark='a'/> if A is of order 'm' by 'n', <bookmark mark='t'/> its transpose is of order 'n' by 'm', <bookmark mark='i'/> and two equal matrices have the same order.""")) as tracker:
            self.play(FadeOut(ej_R), FadeOut(ord_R), run_time=0.6)
            self.wait_until_bookmark("a")
            self.play(FadeIn(o_A), run_time=0.8)
            self.wait_until_bookmark("t")
            self.play(FadeIn(o_T), run_time=0.8)
            self.wait_until_bookmark("i")
            self.play(FadeIn(o_ig), run_time=0.8)
        
        with self.voiceover(text=tr("""Dos matrices son iguales cuando lo son sus columnas, <bookmark mark='c'/> y dos columnas lo son cuando tienen las mismas componentes. <bookmark mark='m'/> Así que dos matrices del mismo orden son iguales cuando tienen las mismas componentes.""",
                                    """Two matrices are equal when their columns are, <bookmark mark='c'/> and two columns are equal when they have the same components. <bookmark mark='m'/> So two matrices of the same order are equal when they have the same components.""")) as tracker:
            self.play(FadeOut(ordenes), run_time=0.6)
            self.play(FadeIn(igualdad[0]), run_time=0.8)
            self.wait_until_bookmark("m")
            self.play(FadeIn(igualdad[1]), FadeIn(igualdad[2]), FadeIn(igualdad_nota), run_time=1)
        
        with self.voiceover(text=tr("""Veamos ahora las componentes de A. <bookmark mark='c'/> Como A es igual a su transpuesta, las dos tienen las mismas componentes. <bookmark mark='r'/> Y por la regla de los índices del vídeo anterior, podemos quitar la transposición <bookmark mark='x'/> intercambiando los índices de lado.""",
                                    """Let us now look at the components of A. <bookmark mark='c'/> Since A is equal to its transpose, both have the same components. <bookmark mark='r'/> And by the index rule of the previous video, we can remove the transposition <bookmark mark='x'/> by moving each index to the other side.""")) as tracker:
            self.play(FadeOut(igualdad), FadeOut(igualdad_nota), run_time=0.6)
            self.play(FadeIn(cadena[0]), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(FadeIn(r1), FadeIn(cadena[1]), FadeIn(VGroup(cadena[2][2], cadena[2][4], cadena[2][5])),
                      *[TransformFromCopy(cadena[0][i], cadena[2][j]) for i, j in [(0, 0), (1, 1), (2, 3), (3, 6), (4, 7)]], run_time=1.2)
            self.wait_until_bookmark("r")
            copia = copia_literal(self, cadena[2], cadena[4], cadena[3])
            self.play(FadeIn(r2), run_time=0.5)
            self.wait_until_bookmark("x")
            transforma_copia(self, copia, cadena[4], [(0, 4), (1, 3), (3, 2), (6, 1), (7, 0)], se_van=[2, 4, 5])
        
        with self.voiceover(text=tr("""Así pues, si intercambiamos el índice de la fila y el de la columna, la componente no cambia.""",
                                    """So if we swap the row index and the column index, the component does not change.""")) as tracker:
            ies, jotas = [cadena[0][0], cadena[4][4]], [cadena[0][4], cadena[4][0]]
            resalta(self, ies, factor=1.5)
            resalta(self, jotas, color=COLOR_C, factor=1.5)
            self.wait(1)
            apaga(self, ies, factor=1.5)
            apaga(self, jotas, factor=1.5)
        
        with self.voiceover(text=tr("""Volvamos a la matriz del ejemplo. <bookmark mark='e'/> Basta conocer la diagonal principal y las componentes que hay por encima: <bookmark mark='r'/> las de debajo son su reflejo, como en un espejo.""",
                                    """Back to the matrix of the example. <bookmark mark='e'/> It is enough to know the main diagonal and the components above it: <bookmark mark='r'/> the ones below are their mirror image.""")) as tracker:
            self.play(FadeIn(S.get_brackets()), FadeIn(VGroup(*arriba)), run_time=1)
            self.wait_until_bookmark("e")
            resalta(self, [x for x in arriba if x not in diagonal(S)], color=COLOR_A, factor=1.2)
            self.wait_until_bookmark("r")
            self.play(*[TransformFromCopy(o, d) for o, d in debajo], run_time=1.6)
            self.play(*[d.animate.set_color(COLOR_A) for o, d in debajo], run_time=0.3)
        
        self.pausa_media()


class L01_V11_E04_DiagonalSimetrica(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Diagonal y cuadrada, luego simétrica", "Square diagonal, hence symmetric"), font_size=40).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self, [(tr("Matriz diagonal", "Diagonal matrix"), "diag", [r"\eleM{D}{i}{j}", r"=0\quad (i\neq j)"]),
                             (tr("Vídeo anterior", "Previous video"), "regla", r"\eleMT{A}{i}{j}=\eleM{A}{j}{i}")])
        enunciado = VGroup(Tex(tr(r"$\Mat{D}$ diagonal y cuadrada:", r"$\Mat{D}$ square diagonal:"), tex_template=myTemplate, font_size=40),
                           MathTex(r"\MatT{D}", r"=", r"\Mat{D}", tex_template=myTemplate, font_size=48)).arrange(RIGHT, buff=0.4).move_to([0, 1.2, 0])   # bajo el panel: su recuadro no toca los del panel
        # Glifos: i | ( D T ) | i  =  i | D | i
        l1 = MathTex(r"\eleMT{D}{i}{i}", r"=", r"\eleM{D}{i}{i}", tex_template=myTemplate, font_size=52)
        # Glifos: i | ( D T ) | j  =  j | D | i  =  0  =  i | D | j
        l2 = MathTex(r"\eleMT{D}{i}{j}", r"=", r"\eleM{D}{j}{i}", r"=", r"0", r"=", r"\eleM{D}{i}{j}", tex_template=myTemplate, font_size=52)
        columna_de_lineas([l1, l2], x0=-1.2, y0=-0.2, dy=1.3)
        c1 = Tex(r"$i=j$:", font_size=34, color=GRAY_B).next_to(l1, LEFT, buff=0.6)
        c2 = Tex(r"$i\neq j$:", font_size=34, color=GRAY_B).next_to(l2, LEFT, buff=0.6)
        CAMBIO = [(0, 4), (1, 3), (3, 2), (6, 1), (7, 0)]   # quitar la transposición: los índices cambian de lado
        
        D1, D1T = matriz(D_EJ), matriz([list(f) for f in zip(*D_EJ)])
        ej_D = VGroup(con_nombre(r"\Mat{D}=", D1), con_nombre(r"\MatT{D}=", D1T)).arrange(RIGHT, buff=1.2).move_to([0, 0.2, 0])
        
        with self.voiceover(text=tr("""Para terminar, tomemos esta matriz diagonal. <bookmark mark='t'/> Al transponerla, sus filas pasan a ser columnas <bookmark mark='i'/> y, como fuera de la diagonal solo hay ceros, obtenemos la misma matriz.""",
                                    """To finish, take this diagonal matrix. <bookmark mark='t'/> When we transpose it, its rows become columns <bookmark mark='i'/> and, since there are only zeros outside the diagonal, we get the same matrix.""")) as tracker:
            self.play(Write(cabecera), FadeIn(ej_D[0]), run_time=1)
            self.wait_until_bookmark("t")
            construye_transpuesta(self, D1, D1T, nombreT=ej_D[1][0])
            self.wait_until_bookmark("i")
            self.play(Indicate(D1.get_entries(), color=COLOR_A, scale_factor=1.1), Indicate(D1T.get_entries(), color=COLOR_A, scale_factor=1.1), run_time=1.2)
        
        with self.voiceover(text=tr("""El ejemplo solo lo ilustra. Ahora vamos a demostrar que toda matriz diagonal y cuadrada es simétrica.""",
                                    """The example only illustrates it. Now we are going to prove that every square diagonal matrix is symmetric.""")) as tracker:
            self.play(FadeOut(ej_D), run_time=0.6)
            self.play(FadeIn(panel.todo), Write(enunciado), run_time=1.2)
        
        with self.voiceover(text=tr("""Para demostrarlo necesitará <bookmark mark='p'/> la definición de matriz diagonal <bookmark mark='q'/> y la regla de los índices del vídeo anterior.""",
                                    """To prove it you will need <bookmark mark='p'/> the definition of a diagonal matrix <bookmark mark='q'/> and the index rule of the previous video.""")) as tracker:
            self.wait_until_bookmark("p")
            panel.pista("diag")
            self.wait_until_bookmark("q")
            panel.pista("regla")
        
        self.pausa_para_pensar(invitacion=tr("Demuestre que toda matriz diagonal y cuadrada es simétrica.",
                                             "Prove that every square diagonal matrix is symmetric."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que toda matriz diagonal y cuadrada es igual a su transpuesta.",
                                                 "Pause the video and try to prove that every square diagonal matrix is equal to its transpose."))
        
        with self.voiceover(text=tr("""Como D es cuadrada, su transpuesta tiene el mismo orden, así que podemos comparar las componentes de las dos una a una.""",
                                    """Since D is square, its transpose has the same order, so we can compare their components one by one.""")) as tracker:
            self.play(Indicate(enunciado[0], color=COLOR_ESCALAR, scale_factor=1.08), run_time=1.2)
        
        with self.voiceover(text=tr("""En la diagonal principal, los dos índices son iguales, <bookmark mark='a'/> así que la regla de los índices no cambia nada.""",
                                    """On the main diagonal the two indices are equal, <bookmark mark='a'/> so the index rule changes nothing.""")) as tracker:
            self.play(FadeIn(c1), TransformFromCopy(enunciado[1][0], l1[0]), run_time=1)
            panel.senala("regla")
            self.wait_until_bookmark("a")
            copia = copia_literal(self, l1[0], l1[2], l1[1])
            transforma_copia(self, copia, l1[2], CAMBIO, se_van=[2, 4, 5])
            panel.cuenta("regla")
        
        with self.voiceover(text=tr("""Fuera de la diagonal principal, los índices son distintos. <bookmark mark='a'/> Por la regla de los índices, podemos quitar la transposición <bookmark mark='x'/> intercambiando los índices de lado.""",
                                    """Outside the main diagonal, the indices are different. <bookmark mark='a'/> By the index rule, we can remove the transposition <bookmark mark='x'/> by moving each index to the other side.""")) as tracker:
            self.play(FadeIn(c2), TransformFromCopy(enunciado[1][0], l2[0]), run_time=1)
            panel.senala("regla")
            self.wait_until_bookmark("a")
            copia = copia_literal(self, l2[0], l2[2], l2[1])
            self.wait_until_bookmark("x")
            transforma_copia(self, copia, l2[2], CAMBIO, se_van=[2, 4, 5])
            panel.cuenta("regla")
        
        with self.voiceover(text=tr("""Por la definición de matriz diagonal, <bookmark mark='a'/> la componente que hemos obtenido es cero. <bookmark mark='b'/> Por la misma razón, también es cero la de la fila i y la columna j.""",
                                    """By the definition of a diagonal matrix, <bookmark mark='a'/> the component we have obtained is zero. <bookmark mark='b'/> For the same reason, the one in row i and column j is zero too.""")) as tracker:
            panel.senala("diag")
            self.wait_until_bookmark("a")
            self.play(FadeIn(l2[3]), ReplacementTransform(l2[2].copy(), l2[4]), run_time=1)
            panel.cuenta("diag")
            self.wait_until_bookmark("b")
            self.play(FadeIn(l2[5]), TransformFromCopy(panel.piezas["diag"][0], l2[6]), run_time=1.2)
            panel.cuenta("diag")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Así que D y su transpuesta tienen las mismas componentes, <bookmark mark='ok'/> y por tanto son iguales.""",
                                    """So D and its transpose have the same components, <bookmark mark='ok'/> and therefore they are equal.""")) as tracker:
            self.play(Indicate(VGroup(l1, l2), color=COLOR_ESCALAR, scale_factor=1.04), run_time=1)
            self.wait_until_bookmark("ok")
            marco = SurroundingRectangle(enunciado[1], color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
            self.play(Create(marco), Indicate(enunciado[1], color=COLOR_RESULTADO, scale_factor=1.15), run_time=1.5)
        
        with self.voiceover(text=tr("""Hemos usado dos veces la regla de los índices y dos veces la definición de matriz diagonal. En particular, la matriz identidad, que es diagonal y cuadrada, es simétrica.""",
                                    """We have used the index rule twice and the definition of a diagonal matrix twice. In particular, the identity matrix, which is a square diagonal matrix, is symmetric.""")) as tracker:
            self.play(*[Indicate(panel.contadores[c], color=COLOR_ESCALAR) for c in ("regla", "diag")], run_time=1.2)
        
        self.pausa_media()


class L01_V11_E05_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [r"\Mat{A}\in\R[n\times n]", r"\eleM{D}{i}{j}=0\quad (i\neq j)", r"\eleM{I}{i}{i}=1,\quad \eleM{I}{i}{j}=0\quad (i\neq j)",
                    r"\Mat{A}=\MatT{A}\quad\Rightarrow\quad \eleM{A}{i}{j}=\eleM{A}{j}{i}", r"\MatT{D}=\Mat{D}"]
        rotulos = [tr("cuadrada: tantas filas como columnas (de orden $n$)", "square: as many rows as columns (of order $n$)"),
                   tr("diagonal: ceros fuera de la diagonal principal", "diagonal: zeros outside the main diagonal"),
                   tr("identidad: cuadrada y diagonal, con unos en la diagonal", "identity: square and diagonal, with ones on the diagonal"),
                   tr("simétrica: igual a su transpuesta", "symmetric: equal to its transpose"),
                   tr("si $\\Mat{D}$ es diagonal y cuadrada, es simétrica", "if $\\Mat{D}$ is square and diagonal, it is symmetric")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=40), Tex(r, tex_template=myTemplate, font_size=26, color=GRAY_B)).arrange(DOWN, buff=0.15)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.3).move_to([0, -0.4, 0])
        
        with self.voiceover(text=tr("""Resumamos. Una matriz es cuadrada si tiene tantas filas como columnas, <bookmark mark='d'/> y es diagonal si todas sus componentes fuera de la diagonal principal son nulas. <bookmark mark='i'/> La matriz identidad es cuadrada y diagonal, con unos en la diagonal principal.""",
                                    """Let us sum up. A matrix is square if it has as many rows as columns, <bookmark mark='d'/> and it is diagonal if all its components outside the main diagonal are zero. <bookmark mark='i'/> The identity matrix is square and diagonal, with ones on the main diagonal.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("d")
            self.play(FadeIn(filas[1]), run_time=0.8)
            self.wait_until_bookmark("i")
            self.play(FadeIn(filas[2]), run_time=0.8)
        
        with self.voiceover(text=tr("""Una matriz es simétrica si es igual a su transpuesta. Entonces es cuadrada, y sus componentes no cambian al intercambiar los índices. <bookmark mark='x'/> Y toda matriz diagonal y cuadrada es simétrica.""",
                                    """A matrix is symmetric if it is equal to its transpose. Then it is square, and its components do not change when the indices are swapped. <bookmark mark='x'/> And every square diagonal matrix is symmetric.""")) as tracker:
            self.play(FadeIn(filas[3]), run_time=0.8)
            self.wait_until_bookmark("x")
            self.play(FadeIn(filas[4]), run_time=0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos las operaciones con matrices: la suma y el producto por un escalar.""",
                                    """In the next video we will see the operations with matrices: addition and multiplication by a scalar.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
