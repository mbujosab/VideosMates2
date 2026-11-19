from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Operaciones fila a fila y transposición", "Row-by-row operations and transposition")

A_EJ    = [[1, 1, 9], [2, 0, 2]]       # las dos matrices de orden 2 por 3 del ejemplo del libro (Sección 1.5)
B_EJ    = [[1, 2, 3], [0, -1, 7]]
S_EJ    = [[2, 3, 12], [2, -1, 9]]     # A + B
DOSB_EJ = [[2, 4, 6], [0, -2, 14]]     # 2B
COLOR_FILA = YELLOW                    # las filas, en amarillo; las columnas, en verde (como en V10)
COLOR_COLUMNA = GREEN
CAMPANITA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos", "campanita.wav")   # suena al subir un contador

# Las cuatro reglas del vídeo y las dos definiciones de V13
FILAS_SUMA = r"\elemLp{\Mat{A}+\Mat{B}}{i}=\VectF{A}{i}+\VectF{B}{i}"
FILAS_PROD = r"\elemLp{\lambda\Mat{A}}{i}=\lambda\VectFpE{A}{i}"
COLS_SUMA  = r"\elemRp{\Mat{A}+\Mat{B}}{j}=\VectC{A}{j}+\VectC{B}{j}"
COLS_PROD  = r"\elemRp{\lambda\Mat{A}}{j}=\lambda\VectCpE{A}{j}"
TRANS_SUMA = r"\Transp{\Mat{A}+\Mat{B}}=\MatT{A}+\MatT{B}"
TRANS_PROD = r"\Transp{\lambda\Mat{A}}=\lambda\MatTpE{A}"
DEF_TRANS  = r"\VectTC{A}{j}=\VectF{A}{j}"


def transpuesta(filas):
    return [list(c) for c in zip(*filas)]


def matriz(filas, color=WHITE, escala=0.8, h_buff=1.0):
    m = IntegerMatrix(filas, v_buff=0.62, h_buff=h_buff)
    m.get_entries().set_color(color)
    return m.scale(escala)


def fila_vec(fila):
    """Un vector numérico escrito en horizontal, entre paréntesis y con la coma final del libro."""
    return "(" + r",\;".join(str(x) for x in fila) + ",)"


def marco(mob, color=COLOR_FILA):
    return SurroundingRectangle(mob, color=color, buff=0.1, corner_radius=0.1, stroke_width=3)


def resalta(escena, mobs, color=COLOR_ESCALAR, factor=1.3, run_time=0.3):
    """Resaltado inmediato y sostenido (color y tamaño), sin la subida lenta de Indicate."""
    escena.play(*[x.animate.set_color(color).scale(factor) for x in mobs], run_time=run_time)


def apaga(escena, mobs, color=WHITE, factor=1.3, run_time=0.3):
    escena.play(*[x.animate.set_color(color).scale(1/factor) for x in mobs], run_time=run_time)


class Panel:
    """Panel de herramientas (V06, V11): piezas [(cabecera, clave, fórmula), ...] a la izquierda y a la
    derecha. Pista (amarillo y recuadro), parpadeo antes de cada paso y contador de usos con campanita."""
    def __init__(self, escena, izquierda, derecha, y_sup=2.95, font_size=30):
        self.escena, self.piezas, self.usos, self.contadores = escena, {}, {}, {}
        self.marcos = VGroup()
        lados = []
        for piezas in (izquierda, derecha):
            grupo = VGroup()
            for cab, clave, formula in piezas:
                m = MathTex(formula, tex_template=myTemplate, font_size=font_size)
                self.piezas[clave] = m
                grupo.add(VGroup(Tex(cab, font_size=22).set_color(GRAY_B), m).arrange(DOWN, aligned_edge=LEFT, buff=0.12))
            lados.append(grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.42))
        lados[0].to_edge(LEFT, buff=0.4)
        lados[1].to_edge(RIGHT, buff=1.5)   # deja sitio al contador sin tocar la firma del margen
        for g in lados:
            g.align_to([0, y_sup, 0], UP)
        self.todo = VGroup(*lados)

    def pista(self, *claves, run_time=0.8):
        marcos = VGroup(*[SurroundingRectangle(self.piezas[c], color=COLOR_ESCALAR, buff=0.1,
                                               corner_radius=0.1, stroke_width=2) for c in claves])
        self.marcos.add(*marcos)
        self.escena.play(*[self.piezas[c].animate.set_color(COLOR_ESCALAR) for c in claves],
                         Create(marcos), run_time=run_time)

    def senala(self, clave):
        return Indicate(self.piezas[clave], color=COLOR_RESULTADO, scale_factor=1.12)

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


def linea(formula, font_size=40):
    return MathTex(formula, tex_template=myTemplate, font_size=font_size)


def coloca_cadena(cadena, y_sup=0.45, salto=0.78, x_izq=-2.9, sangria=0.6):
    """La primera línea en x_izq y las siguientes (que empiezan por '=') sangradas."""
    for k, l in enumerate(cadena):
        l.move_to([0, y_sup - k*salto, 0]).align_to([x_izq + (sangria if k else 0), 0, 0], LEFT)
    return cadena


def nace(escena, origen, destino, fijos, moviles=(), aparecen=(), con_igual=True, extra=(), marca=None,
         t_fijos=0.8, t_moviles=0.9):
    """Una expresión nace de la anterior (CLAUDE.md, «Cada expresión nace de la anterior»). origen y destino son
    listas de glifos. Primero, mientras la voz nombra la regla, se copia lo que no cambia (fijos: parejas glifo de
    origen, glifo de destino) y aparece el igual; después (en la marca, si se da) viaja lo que el paso mueve
    (moviles) y surge lo nuevo (aparecen). Lo que se quita no aparece. Un glifo de origen puede ir a dos sitios."""
    cubiertos = sorted({j for _, j in fijos} | {j for _, j in moviles} | set(aparecen) | ({0} if con_igual else set()))
    assert cubiertos == list(range(len(destino))), (cubiertos, len(destino))
    escena.play(*extra, *([FadeIn(destino[0])] if con_igual else []),
                *[TransformFromCopy(origen[i], destino[j]) for i, j in fijos], run_time=t_fijos)
    if marca is not None:
        escena.wait_until_bookmark(marca)
    if moviles or aparecen:
        # si dos glifos de origen se reúnen en uno de destino (factor común), el segundo viaja como copia y se retira
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


def paso(escena, panel, clave, origen, destino, fijos, moviles=(), aparecen=(), marca=None, t_fijos=0.8, t_moviles=0.9, t_cuenta=0.5):
    """Un paso de una demostración con panel, en el orden de V06: la pieza parpadea en el panel mientras se copia
    lo que no cambia, la línea se completa (en la marca, si se da) y entonces sube el contador con la campanita.
    Con clave None el paso no usa ninguna pieza del panel (poner o quitar paréntesis)."""
    nace(escena, origen[0], destino[0], fijos, moviles, aparecen, extra=[panel.senala(clave)] if clave else [], marca=marca,
         t_fijos=t_fijos, t_moviles=t_moviles)
    entera(escena, destino)
    if clave:
        panel.cuenta(clave, run_time=t_cuenta)


def recuadra(escena, enunciado, run_time=1.5):
    """Lo demostrado: recuadro amarillo y parpadeo del enunciado."""
    caja = SurroundingRectangle(enunciado, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
    escena.play(Create(caja), Indicate(enunciado, color=COLOR_RESULTADO, scale_factor=1.15), run_time=run_time)
    return caja

class L01_V14_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class L01_V14_E01_Ejemplo(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        A, B, S = matriz(A_EJ, COLOR_A), matriz(B_EJ, COLOR_B), matriz(S_EJ)
        mas, igual = MathTex("+", font_size=48), MathTex("=", font_size=48)
        suma = VGroup(A, mas, B, igual, S).arrange(RIGHT, buff=0.3).move_to([0, 1.1, 0])
        sumas = [MathTex(fila_vec(a), "+", fila_vec(b), "=", fila_vec(s), tex_template=myTemplate, font_size=44).move_to([0, -1.2, 0])
                 for a, b, s in zip(A_EJ, B_EJ, S_EJ)]
        for s in sumas:
            s[0].set_color(COLOR_A); s[2].set_color(COLOR_B)
        dos = MathTex("2", font_size=56).set_color(COLOR_ESCALAR)
        B2, P = matriz(B_EJ, COLOR_B), matriz(DOSB_EJ)
        igual2 = MathTex("=", font_size=48)
        prod = VGroup(dos, B2, igual2, P).arrange(RIGHT, buff=0.3).move_to([0, 1.1, 0])
        prods = [MathTex("2", fila_vec(b), "=", fila_vec(p), tex_template=myTemplate, font_size=44).move_to([0, -1.2, 0])
                 for b, p in zip(B_EJ, DOSB_EJ)]
        for p in prods:
            p[0].set_color(COLOR_ESCALAR); p[1].set_color(COLOR_B)
        ilustra = aviso("ilustra").to_edge(DOWN, buff=0.4)
        
        with self.voiceover(text=tr("""En este vídeo veremos que las matrices también se pueden sumar y multiplicar por un escalar fila a fila. Y veremos lo que ocurre al transponer una suma, o un producto por un escalar.""",
                                    """In this video we will see that matrices can also be added and multiplied by a scalar row by row. And we will see what happens when we transpose a sum, or a product by a scalar.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        with self.voiceover(text=tr("""La suma de matrices se define columna a columna: <bookmark mark='c'/> cada columna de la suma es la suma de las columnas correspondientes.""",
                                    """Matrix addition is defined column by column: <bookmark mark='c'/> each column of the sum is the sum of the corresponding columns.""")) as tracker:
            self.play(FadeIn(A), FadeIn(mas), FadeIn(B), FadeIn(igual), FadeIn(S.get_brackets()), run_time=1)
            self.wait_until_bookmark("c")
            for k in range(3):
                marcos = VGroup(*[marco(m.get_columns()[k], COLOR_COLUMNA) for m in (A, B)])
                self.play(Create(marcos), run_time=0.3)
                self.play(FadeIn(S.get_columns()[k]), run_time=0.4)
                self.play(FadeOut(marcos), run_time=0.2)
        
        with self.voiceover(text=tr("""Observe ahora las filas de este ejemplo. <bookmark mark='f1'/> La primera fila de la suma es la suma de las primeras filas, <bookmark mark='f2'/> y la segunda, la suma de las segundas.""",
                                    """Now look at the rows in this example. <bookmark mark='f1'/> The first row of the sum is the sum of the first rows, <bookmark mark='f2'/> and the second, the sum of the second rows.""")) as tracker:
            for k, marca in enumerate(["f1", "f2"]):
                self.wait_until_bookmark(marca)
                nuevos = VGroup(*[marco(m.get_rows()[k]) for m in (A, B, S)])
                if k == 0:
                    marcos = nuevos
                    self.play(Create(marcos), FadeIn(sumas[0]), run_time=0.6)
                else:
                    self.play(Transform(marcos, nuevos), FadeOut(sumas[0]), FadeIn(sumas[1]), run_time=0.6)
        
        self.pausa_corta()
        
        with self.voiceover(text=tr("""Con el producto por un escalar ocurre lo mismo: <bookmark mark='p'/> cada fila del resultado es el doble de la fila correspondiente de la matriz.""",
                                    """The same happens with scalar multiplication: <bookmark mark='p'/> each row of the result is twice the corresponding row of the matrix.""")) as tracker:
            self.play(FadeOut(suma), FadeOut(marcos), FadeOut(sumas[1]), run_time=0.6)
            self.play(FadeIn(prod), run_time=0.8)
            self.wait_until_bookmark("p")
            for k in range(2):
                nuevos = VGroup(*[marco(m.get_rows()[k]) for m in (B2, P)])
                if k == 0:
                    marcos = nuevos
                    self.play(Create(marcos), FadeIn(prods[0]), run_time=0.6)
                    self.wait(0.9)
                else:
                    self.play(Transform(marcos, nuevos), FadeOut(prods[0]), FadeIn(prods[1]), run_time=0.6)
        
        with self.voiceover(text=tr("""Estos ejemplos solo lo ilustran. Ahora vamos a demostrar que ocurre con cualquier matriz.""",
                                    """These examples only illustrate it. Now we are going to prove that it happens with any matrix.""")) as tracker:
            self.play(FadeIn(ilustra, scale=0.9), run_time=0.8)
        
        self.pausa_media()


class L01_V14_E02_SumaPorFilas(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La suma, fila a fila", "Addition, row by row"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self, [(tr("Suma de matrices", "Matrix addition"), "mat", COLS_SUMA)],
                            [(tr("Suma de vectores", "Vector addition"), "vec",   # con el selector a la derecha y a la izquierda: la cadena usa las dos formas
                              r"\elemRp{\Vect{a}+\Vect{b}}{j}&=\eleVR{a}{j}+\eleVR{b}{j}\\ \elemLp{\Vect{a}+\Vect{b}}{i}&=\eleVL{a}{i}+\eleVL{b}{i}")])
        enunciado = MathTex(FILAS_SUMA, tex_template=myTemplate, font_size=44).move_to([0, 1.55, 0])
        # Glifos: ( i | ( A + B ) ) | j (0-10);  = i | ( ( A + B ) | j ) (0-11);  = i | ( A | j + B | j ) (0-11);
        #         = i | A | j + i | B | j (0-11);  = ( i | A + i | B ) | j (0-11)
        cadena = coloca_cadena([linea(r"\elemR{\Big(\elemLp{\Mat{A}+\Mat{B}}{i}\Big)}{j}"),
                                linea(r"=\elemL{\Big(\elemRp{\Mat{A}+\Mat{B}}{j}\Big)}{i}"),
                                linea(r"=\elemLp{\VectC{A}{j}+\VectC{B}{j}}{i}"),
                                linea(r"=\eleM{A}{i}{j}+\eleM{B}{i}{j}"),
                                linea(r"=\elemR{\Big(\VectF{A}{i}+\VectF{B}{i}\Big)}{j}")])
        res_prod = MathTex(FILAS_PROD, tex_template=myTemplate, font_size=44).move_to([0, -0.6, 0])
        
        with self.voiceover(text=tr("""Queremos demostrar que <bookmark mark='e'/> cada fila de la suma es la suma de las filas correspondientes.""",
                                    """We want to prove that <bookmark mark='e'/> each row of the sum is the sum of the corresponding rows.""")) as tracker:
            self.play(Write(cabecera), run_time=0.8)
            self.wait_until_bookmark("e")
            self.play(Write(enunciado), run_time=1.2)
        
        with self.voiceover(text=tr("""Las filas son vectores, y dos vectores son iguales si lo son componente a componente. Usaremos <bookmark mark='p'/> la definición de suma de matrices <bookmark mark='q'/> y la definición de suma de vectores.""",
                                    """Rows are vectors, and two vectors are equal if they are equal component by component. We will use <bookmark mark='p'/> the definition of matrix addition <bookmark mark='q'/> and the definition of vector addition.""")) as tracker:
            self.wait_until_bookmark("p")
            self.play(FadeIn(panel.todo[0]), run_time=0.8)
            self.wait_until_bookmark("q")
            self.play(FadeIn(panel.todo[1]), run_time=0.8)
        
        with self.voiceover(text=tr("""Empezamos por <bookmark mark='c'/> una componente cualquiera de una fila de la suma.""",
                                    """We start with <bookmark mark='c'/> any component of a row of the sum.""")) as tracker:
            # el lado izquierdo del enunciado baja a la cadena y, al decir «componente», aparecen los paréntesis y el selector
            self.play(TransformFromCopy(enunciado[0][0:7], cadena[0][0][1:8]), run_time=0.8)
            self.wait_until_bookmark("c")
            sel = cadena[0][0][9:11]
            sel.set_color(COLOR_COLUMNA).scale(1.3)
            self.play(FadeIn(cadena[0][0][0]), FadeIn(cadena[0][0][8:]), run_time=0.5)
            self.wait(0.8)
            self.play(sel.animate.set_color(WHITE).scale(1/1.3), run_time=0.4)
            entera(self, cadena[0])
        
        with self.voiceover(text=tr("""Como da igual seleccionar primero la fila o la columna, <bookmark mark='x'/> podemos desplazar los paréntesis.""",
                                    """Since it does not matter whether we select the row or the column first, <bookmark mark='x'/> we can move the parentheses.""")) as tracker:
            # los paréntesis grandes pasan a rodear la suma con el selector de columnas
            paso(self, panel, None, cadena[0], cadena[1], [(1, 1), (2, 2), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (9, 9), (10, 10)],
                 [(0, 3), (8, 11)], marca="x", t_fijos=0.5)
        
        with self.voiceover(text=tr("""Por la definición de suma de matrices <bookmark mark='x'/> podemos distribuir el selector de columnas.""",
                                    """By the definition of matrix addition <bookmark mark='x'/> we can distribute the column selector.""")) as tracker:
            # el selector de columnas va a cada sumando; los paréntesis de la suma de matrices no aparecen
            paso(self, panel, "mat", cadena[1], cadena[2], [(1, 1), (2, 2), (3, 3), (5, 4), (6, 7), (7, 8), (11, 11)],
                 [(9, 5), (10, 6), (9, 9), (10, 10)], marca="x")
        
        with self.voiceover(text=tr("""Dentro de los paréntesis hay ahora una suma de dos vectores. Por la definición de suma de vectores <bookmark mark='x'/> podemos distribuir el selector de la izquierda.""",
                                    """Inside the parentheses there is now a sum of two vectors. By the definition of vector addition <bookmark mark='x'/> we can distribute the selector on the left.""")) as tracker:
            # el selector de la izquierda va a cada sumando; los paréntesis no aparecen
            paso(self, panel, "vec", cadena[2], cadena[3], [(4, 3), (5, 4), (6, 5), (7, 6), (8, 9), (9, 10), (10, 11)],
                 [(1, 1), (2, 2), (1, 7), (2, 8)], marca="x")
        
        with self.voiceover(text=tr("""Cada sumando es una componente de una fila. De nuevo por la definición de suma de vectores, <bookmark mark='x'/> podemos sacar el selector de la derecha como factor común.""",
                                    """Each term is a component of a row. Again by the definition of vector addition, <bookmark mark='x'/> we can factor out the selector on the right.""")) as tracker:
            # los dos selectores de la derecha se reúnen en uno; aparecen los paréntesis alrededor de la suma de las dos filas
            paso(self, panel, "vec", cadena[3], cadena[4], [(1, 2), (2, 3), (3, 4), (6, 5), (7, 6), (8, 7), (9, 8)],
                 [(4, 10), (5, 11), (10, 10), (11, 11)], aparecen=[1, 9], marca="x")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Como esto es cierto para <bookmark mark='c'/> cualquier componente, <bookmark mark='ok'/> los dos vectores son iguales: las matrices también se suman fila a fila.""",
                                    """Since this holds for <bookmark mark='c'/> any component, <bookmark mark='ok'/> the two vectors are equal: matrices are also added row by row.""")) as tracker:
            self.wait_until_bookmark("c")
            indices = [cadena[0][0][10], cadena[4][0][11]]   # el índice de la componente, a los dos extremos
            self.play(*[x.animate.set_color(COLOR_COLUMNA).scale(1.5) for x in indices], run_time=0.3)
            self.wait_until_bookmark("ok")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in indices], run_time=0.3)
            caja = recuadra(self, enunciado)
        
        with self.voiceover(text=tr("""Hemos usado <bookmark mark='a'/> una vez la definición de suma de matrices <bookmark mark='b'/> y dos veces la definición de suma de vectores.""",
                                    """We have used <bookmark mark='a'/> the definition of matrix addition once, <bookmark mark='b'/> and the definition of vector addition twice.""")) as tracker:
            self.wait_until_bookmark("a")
            self.play(Indicate(panel.contadores["mat"], color=COLOR_ESCALAR), run_time=1.0)
            self.wait_until_bookmark("b")
            self.play(Indicate(panel.contadores["vec"], color=COLOR_ESCALAR), run_time=1.0)
        
        with self.voiceover(text=tr("""Con el producto por un escalar ocurre lo mismo, y se demuestra con los mismos pasos: <bookmark mark='r'/> cada fila del producto es el producto de la fila por el escalar.""",
                                    """The same happens with scalar multiplication, and it is proved with the same steps: <bookmark mark='r'/> each row of the product is the product of the row by the scalar.""")) as tracker:
            self.play(FadeOut(VGroup(*cadena)), FadeOut(panel.todo), FadeOut(VGroup(*panel.contadores.values())), FadeOut(caja), run_time=0.8)
            self.wait_until_bookmark("r")
            self.play(Write(res_prod), run_time=1.2)
        
        self.pausa_media()


class L01_V14_E03_Lineales(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Operadores lineales", "Linear operators"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        
        def columna(formulas, x):
            filas = VGroup(*[MathTex(f, tex_template=myTemplate, font_size=40) for f in formulas]).arrange(DOWN, buff=0.7)
            return filas.move_to([x, 0.1, 0])
        
        cols, fils = columna([COLS_SUMA, COLS_PROD], -3.4), columna([FILAS_SUMA, FILAS_PROD], 3.4)
        r_cols = Tex(tr("Selector de columnas", "Column selector"), font_size=34).set_color(COLOR_COLUMNA).move_to([-3.4, 2.0, 0])
        r_fils = Tex(tr("Selector de filas", "Row selector"), font_size=34).set_color(COLOR_FILA).move_to([3.4, 2.0, 0])
        idea = aviso("idea", tr("Operador lineal: se distribuye en las sumas y deja fuera a los escalares",
                                "Linear operator: it distributes over sums and leaves scalars outside"), font_size=30).to_edge(DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""El selector de columnas y <bookmark mark='f'/> el selector de filas cumplen las mismas reglas.""",
                                    """The column selector and <bookmark mark='f'/> the row selector obey the same rules.""")) as tracker:
            self.play(Write(cabecera), FadeIn(r_cols), FadeIn(cols), run_time=1)
            self.wait_until_bookmark("f")
            self.play(FadeIn(r_fils), FadeIn(fils), run_time=0.8)
        
        with self.voiceover(text=tr("""Los dos <bookmark mark='s'/> se distribuyen entre los sumandos. <bookmark mark='p'/> Y con los dos podemos desplazar los paréntesis para dejar fuera al escalar.""",
                                    """Both <bookmark mark='s'/> distribute over the terms of a sum. <bookmark mark='p'/> And with both we can move the parentheses to leave the scalar outside.""")) as tracker:
            self.wait_until_bookmark("s")
            resalta(self, [cols[0], fils[0]], factor=1.1)
            self.wait_until_bookmark("p")
            apaga(self, [cols[0], fils[0]], factor=1.1)
            resalta(self, [cols[1], fils[1]], factor=1.1)
        
        with self.voiceover(text=tr("""De un operador que cumple estas dos reglas se dice que es lineal. <bookmark mark='t'/> Veamos que la transposición también lo es.""",
                                    """An operator that obeys these two rules is said to be linear. <bookmark mark='t'/> Let us see that transposition is linear too.""")) as tracker:
            apaga(self, [cols[1], fils[1]], factor=1.1)
            self.play(FadeIn(idea, scale=0.9), run_time=0.8)
        
        self.pausa_media()


class L01_V14_E04_TranspuestaDeLaSuma(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La transpuesta de una suma", "The transpose of a sum"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        # el ejemplo: (A+B)^T arriba y A^T + B^T abajo, con el mismo resultado
        St1, At, Bt, St2 = (matriz(transpuesta(m), c, escala=0.62) for m, c in ((S_EJ, WHITE), (A_EJ, COLOR_A), (B_EJ, COLOR_B), (S_EJ, WHITE)))
        n1 = MathTex(r"\Transp{\Mat{A}+\Mat{B}}", "=", tex_template=myTemplate, font_size=40)
        fila1 = VGroup(n1, St1).arrange(RIGHT, buff=0.25).move_to([0, 1.3, 0])
        n2 = MathTex(r"\MatT{A}+\MatT{B}", "=", tex_template=myTemplate, font_size=40)
        mas, igual = MathTex("+", font_size=40), MathTex("=", font_size=40)
        fila2 = VGroup(n2, At, mas, Bt, igual, St2).arrange(RIGHT, buff=0.25).move_to([0, -1.5, 0])
        ejemplo = VGroup(fila1, fila2)
        
        panel = Panel(self, [(tr("Definición de transpuesta", "Definition of the transpose"), "def", DEF_TRANS),
                             (tr("Suma de matrices", "Matrix addition"), "suma", COLS_SUMA)],
                            [(tr("El selector de filas es lineal", "The row selector is linear"), "filas", FILAS_SUMA)])
        enunciado = MathTex(TRANS_SUMA, tex_template=myTemplate, font_size=44).move_to([0.6, 1.1, 0])
        # Glifos: ( ( A + B ) T ) | j (0-9);  = j | ( A + B ) (0-7);  = j | A + j | B (0-7);
        #         = ( A T ) | j + ( B T ) | j (0-13);  = ( A T + B T ) | j (0-9)
        cadena = coloca_cadena([linea(r"\elemRp{\Transp*{\Mat{A}+\Mat{B}}}{j}"),
                                linea(r"=\elemLp{\Mat{A}+\Mat{B}}{j}"),
                                linea(r"=\VectF{A}{j}+\VectF{B}{j}"),
                                linea(r"=\VectTC{A}{j}+\VectTC{B}{j}"),
                                linea(r"=\elemRp{\MatT{A}+\MatT{B}}{j}")], y_sup=0.1, salto=0.72, x_izq=-2.2)
        
        with self.voiceover(text=tr("""Tomemos de nuevo las dos matrices del ejemplo. <bookmark mark='t'/> Si las sumamos y transponemos la suma, sus filas pasan a ser columnas.""",
                                    """Let us take the two matrices of the example again. <bookmark mark='t'/> If we add them and transpose the sum, its rows become columns.""")) as tracker:
            self.play(Write(cabecera), run_time=0.8)
            self.wait_until_bookmark("t")
            self.play(FadeIn(fila1), run_time=1)
        
        with self.voiceover(text=tr("""Y si transponemos primero cada matriz <bookmark mark='s'/> y sumamos después, obtenemos la misma matriz.""",
                                    """And if we first transpose each matrix <bookmark mark='s'/> and then add, we obtain the same matrix.""")) as tracker:
            self.play(FadeIn(n2[0]), FadeIn(At), FadeIn(mas), FadeIn(Bt), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(n2[1]), FadeIn(igual), FadeIn(St2), run_time=0.8)
            self.play(Indicate(St1, color=COLOR_ESCALAR, scale_factor=1.1), Indicate(St2, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.2)
        
        self.pausa_corta()
        
        with self.voiceover(text=tr("""Este ejemplo solo lo ilustra. Vamos a demostrar que <bookmark mark='e'/> la transpuesta de una suma es siempre la suma de las transpuestas.""",
                                    """This example only illustrates it. We are going to prove that <bookmark mark='e'/> the transpose of a sum is always the sum of the transposes.""")) as tracker:
            self.play(FadeOut(ejemplo), run_time=0.6)
            self.play(FadeIn(panel.todo), run_time=0.8)
            self.wait_until_bookmark("e")
            self.play(Write(enunciado), run_time=1.2)
        
        with self.voiceover(text=tr("""Para demostrarlo necesitará <bookmark mark='p'/> la definición de transpuesta, <bookmark mark='q'/> que el selector de filas es lineal, <bookmark mark='r'/> y la definición de suma de matrices.""",
                                    """To prove it you will need <bookmark mark='p'/> the definition of the transpose, <bookmark mark='q'/> the fact that the row selector is linear, <bookmark mark='r'/> and the definition of matrix addition.""")) as tracker:
            for marca, clave in (("p", "def"), ("q", "filas"), ("r", "suma")):
                self.wait_until_bookmark(marca)
                panel.pista(clave)
        
        self.pausa_para_pensar(invitacion=tr("Demuestre que la transpuesta de una suma es la suma de las transpuestas.",
                                             "Prove that the transpose of a sum is the sum of the transposes."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrar que la transpuesta de una suma es la suma de las transpuestas.",
                                                 "Pause the video and try to prove that the transpose of a sum is the sum of the transposes."))
        
        with self.voiceover(text=tr("""Empezamos por <bookmark mark='c'/> una columna cualquiera del lado izquierdo.""",
                                    """We start with <bookmark mark='c'/> any column of the left-hand side.""")) as tracker:
            self.play(TransformFromCopy(enunciado[0][0:6], cadena[0][0][1:7]), run_time=0.8)
            self.wait_until_bookmark("c")
            sel = cadena[0][0][8:10]
            sel.set_color(COLOR_COLUMNA).scale(1.3)
            self.play(FadeIn(cadena[0][0][0]), FadeIn(cadena[0][0][7:]), run_time=0.5)
            self.wait(0.8)
            self.play(sel.animate.set_color(WHITE).scale(1/1.3), run_time=0.4)
            entera(self, cadena[0])
        
        with self.voiceover(text=tr("""Por la definición de transpuesta, <bookmark mark='x'/> podemos quitar la transposición cambiando de lado el índice.""",
                                    """By the definition of the transpose, <bookmark mark='x'/> we can remove the transposition by moving the index to the other side.""")) as tracker:
            # la suma entre paréntesis baja tal cual; el selector cruza a la izquierda; la T y los paréntesis de fuera no aparecen
            paso(self, panel, "def", cadena[0], cadena[1], [(1, 3), (2, 4), (3, 5), (4, 6), (5, 7)], [(8, 2), (9, 1)], marca="x")
        
        with self.voiceover(text=tr("""Como el selector de filas es lineal, <bookmark mark='x'/> podemos distribuirlo entre los sumandos.""",
                                    """Since the row selector is linear, <bookmark mark='x'/> we can distribute it over the terms.""")) as tracker:
            paso(self, panel, "filas", cadena[1], cadena[2], [(4, 3), (5, 4), (6, 7)], [(1, 1), (2, 2), (1, 5), (2, 6)], marca="x")
        
        with self.voiceover(text=tr("""De nuevo por la definición de transpuesta, <bookmark mark='x'/> cada fila es una columna de la transpuesta, y el índice vuelve a la derecha.""",
                                    """Again by the definition of the transpose, <bookmark mark='x'/> each row is a column of the transpose, and the index goes back to the right.""")) as tracker:
            paso(self, panel, "def", cadena[2], cadena[3], [(3, 2), (4, 7), (7, 9)], [(1, 6), (2, 5), (5, 13), (6, 12)],
                 aparecen=[1, 3, 4, 8, 10, 11], marca="x")
        
        with self.voiceover(text=tr("""Y por la definición de suma de matrices <bookmark mark='x'/> podemos sacar el selector como factor común.""",
                                    """And by the definition of matrix addition <bookmark mark='x'/> we can factor out the selector.""")) as tracker:
            paso(self, panel, "suma", cadena[3], cadena[4], [(2, 2), (3, 3), (7, 4), (9, 5), (10, 6)],
                 [(5, 8), (6, 9), (12, 8), (13, 9), (1, 1), (11, 7)], marca="x")
        
        self.wait(0.3)
        with self.voiceover(text=tr("""Como esto es cierto para <bookmark mark='c'/> cualquier columna, <bookmark mark='ok'/> las dos matrices son iguales.""",
                                    """Since this holds for <bookmark mark='c'/> any column, <bookmark mark='ok'/> the two matrices are equal.""")) as tracker:
            self.wait_until_bookmark("c")
            indices = [cadena[0][0][9], cadena[4][0][9]]
            self.play(*[x.animate.set_color(COLOR_COLUMNA).scale(1.5) for x in indices], run_time=0.3)
            self.wait_until_bookmark("ok")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in indices], run_time=0.3)
            recuadra(self, enunciado)
        
        with self.voiceover(text=tr("""Hemos usado <bookmark mark='a'/> dos veces la definición de transpuesta, <bookmark mark='b'/> una vez la linealidad del selector de filas <bookmark mark='c'/> y una vez la definición de suma de matrices.""",
                                    """We have used <bookmark mark='a'/> the definition of the transpose twice, <bookmark mark='b'/> the linearity of the row selector once, <bookmark mark='c'/> and the definition of matrix addition once.""")) as tracker:
            for marca, clave in (("a", "def"), ("b", "filas"), ("c", "suma")):
                self.wait_until_bookmark(marca)
                self.play(Indicate(panel.contadores[clave], color=COLOR_ESCALAR), run_time=0.9)
        
        self.pausa_media()


class L01_V14_E05_TranspuestaDelProducto(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La transpuesta de un producto por un escalar", "The transpose of a product by a scalar"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self, [(tr("Definición de transpuesta", "Definition of the transpose"), "def", DEF_TRANS),
                             (tr("Producto por un escalar", "Product by a scalar"), "prod", COLS_PROD)],
                            [(tr("El selector de filas es lineal", "The row selector is linear"), "filas", FILAS_PROD)])
        enunciado = MathTex(TRANS_PROD, tex_template=myTemplate, font_size=44).move_to([0.6, 1.1, 0])
        # Glifos: ( ( λ A ) T ) | j (0-8);  = j | ( λ A ) (0-6);  = λ ( j | A ) (0-6);
        #         = λ ( ( A T ) | j ) (0-9);  = ( λ ( A T ) ) | j (0-9)
        cadena = coloca_cadena([linea(r"\elemRp{\Transp*{\lambda\Mat{A}}}{j}"),
                                linea(r"=\elemLp{\lambda\Mat{A}}{j}"),
                                linea(r"=\lambda\VectFpE{A}{j}"),
                                linea(r"=\lambda\VectTCpE{A}{j}"),
                                linea(r"=\elemRp{\lambda\MatTpE{A}}{j}")], y_sup=0.3, salto=0.66, x_izq=-1.8)
        idea = aviso("idea", tr("La transposición es un operador lineal", "Transposition is a linear operator"), font_size=32).to_edge(DOWN, buff=0.15)
        
        with self.voiceover(text=tr("""Con el producto por un escalar ocurre lo mismo: <bookmark mark='e'/> al transponer un producto por un escalar, podemos dejar fuera al escalar.""",
                                    """The same happens with scalar multiplication: <bookmark mark='e'/> when we transpose a product by a scalar, we can leave the scalar outside.""")) as tracker:
            self.play(Write(cabecera), FadeIn(panel.todo), run_time=1)
            self.wait_until_bookmark("e")
            self.play(Write(enunciado), run_time=1.2)
        
        self.pausa_para_pensar(invitacion=tr("Demuéstrelo con los mismos pasos.", "Prove it with the same steps."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrarlo con los mismos pasos que en la suma.",
                                                 "Pause the video and try to prove it with the same steps as for the sum."))
        
        with self.voiceover(text=tr("""Los pasos son los mismos. <bookmark mark='l0'/> Seleccionamos una columna <bookmark mark='l1'/> y quitamos la transposición cambiando de lado el índice. <bookmark mark='l2'/> Como el selector de filas es lineal, podemos desplazar los paréntesis. <bookmark mark='l3'/> La fila es una columna de la transpuesta. <bookmark mark='l4'/> Y por la definición de producto por un escalar podemos desplazar de nuevo los paréntesis.""",
                                    """The steps are the same. <bookmark mark='l0'/> We select a column <bookmark mark='l1'/> and remove the transposition by moving the index to the other side. <bookmark mark='l2'/> Since the row selector is linear, we can move the parentheses. <bookmark mark='l3'/> The row is a column of the transpose. <bookmark mark='l4'/> And by the definition of the product by a scalar we can move the parentheses again.""")) as tracker:
            rapido = dict(t_fijos=0.5, t_moviles=0.6, t_cuenta=0.35)
            self.wait_until_bookmark("l0")
            self.play(TransformFromCopy(enunciado[0][0:5], cadena[0][0][1:6]), FadeIn(cadena[0][0][0]), FadeIn(cadena[0][0][6:]), run_time=0.8)
            entera(self, cadena[0])
            self.wait_until_bookmark("l1")   # el selector cruza a la izquierda; la T y los paréntesis de fuera no aparecen
            paso(self, panel, "def", cadena[0], cadena[1], [(1, 3), (2, 4), (3, 5), (4, 6)], [(7, 2), (8, 1)], **rapido)
            self.wait_until_bookmark("l2")   # los paréntesis dejan fuera al escalar y rodean la fila
            paso(self, panel, "filas", cadena[1], cadena[2], [(4, 1), (5, 5), (1, 3), (2, 4)], [(3, 2), (6, 6)], **rapido)
            self.wait_until_bookmark("l3")   # el índice vuelve a la derecha, con la T y sus paréntesis
            paso(self, panel, "def", cadena[2], cadena[3], [(1, 1), (2, 2), (6, 9), (5, 4)], [(3, 8), (4, 7)], aparecen=[3, 5, 6], **rapido)
            self.wait_until_bookmark("l4")   # los paréntesis pasan a rodear el producto y dejan fuera el selector
            paso(self, panel, "prod", cadena[3], cadena[4], [(1, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 8), (8, 9)], [(2, 1), (9, 7)], **rapido)
        
        with self.voiceover(text=tr("""Como esto es cierto para cualquier columna, <bookmark mark='ok'/> las dos matrices son iguales.""",
                                    """Since this holds for any column, <bookmark mark='ok'/> the two matrices are equal.""")) as tracker:
            self.wait_until_bookmark("ok")
            recuadra(self, enunciado)
        
        with self.voiceover(text=tr("""Así pues, la transposición se distribuye en las sumas y deja fuera a los escalares: <bookmark mark='i'/> también es un operador lineal.""",
                                    """So transposition distributes over sums and leaves scalars outside: <bookmark mark='i'/> it is a linear operator too.""")) as tracker:
            self.wait_until_bookmark("i")
            self.play(FadeIn(idea, scale=0.9), run_time=0.8)
        
        self.pausa_media()


class L01_V14_E06_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [FILAS_SUMA + r"\qquad\quad " + FILAS_PROD, TRANS_SUMA + r"\qquad\quad " + TRANS_PROD]
        rotulos = [tr("las matrices también se suman y se multiplican por un escalar fila a fila",
                      "matrices are also added and multiplied by a scalar row by row"),
                   tr("la transposición es lineal, como los selectores de filas y de columnas",
                      "transposition is linear, like the row and column selectors")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=40), Tex(r, font_size=28, color=GRAY_B)).arrange(DOWN, buff=0.25)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.9).move_to([0, -0.2, 0])
        
        with self.voiceover(text=tr("""Resumamos. Las matrices también se suman y se multiplican por un escalar fila a fila: el selector de filas es lineal, como el de columnas. <bookmark mark='t'/> La transposición también es lineal: la transpuesta de una suma es la suma de las transpuestas, y al transponer un producto por un escalar, el escalar queda fuera.""",
                                    """Let us sum up. Matrices are also added and multiplied by a scalar row by row: the row selector is linear, like the column selector. <bookmark mark='t'/> Transposition is linear too: the transpose of a sum is the sum of the transposes, and when we transpose a product by a scalar, the scalar stays outside.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("t")
            self.play(FadeIn(filas[1]), run_time=0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos una última extensión de la notación: escribir el escalar a la derecha.""",
                                    """In the next video we will see one last extension of the notation: writing the scalar on the right.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
