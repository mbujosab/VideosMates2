from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Operaciones fila a fila y transposición", "Row-by-row operations and transposition")

A_EJ    = [[1, 1, 9], [2, 0, 2]]       # las dos matrices de orden 2 por 3 del ejemplo del libro (Sección 1.5)
B_EJ    = [[1, 2, 3], [0, -1, 7]]
S_EJ    = [[2, 3, 12], [2, -1, 9]]     # A + B
DOSB_EJ = [[2, 4, 6], [0, -2, 14]]     # 2B
COLOR_FILA = YELLOW                    # las filas, en amarillo; las columnas, en verde (como en V10)
COLOR_COLUMNA = GREEN
COLOR_TRANSP = PURPLE_B                # la transposición, al señalarla en la cantinela
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


def cantinela(escena, pasos, factor=1.5):
    """La cantinela de la linealidad (Marcos, 2026-11-20): «da igual sumar primero y seleccionar después, que
    seleccionar primero y sumar después». pasos = [(marca, [glifos], color), ...]: en cada marca se agranda y
    colorea la operación que la voz nombra, y la anterior vuelve a blanco."""
    antes = []
    for marca, glifos, color in pasos:
        escena.wait_until_bookmark(marca)
        colores = color if isinstance(color, list) else [color]*len(glifos)
        anims = [g.animate.set_color(WHITE).scale(1/factor) for g in antes]
        anims += [g.animate.set_color(c).scale(factor) for g, c in zip(glifos, colores)]
        escena.play(*anims, run_time=0.25)
        antes = glifos
    escena.wait(0.6)
    escena.play(*[g.animate.set_color(WHITE).scale(1/factor) for g in antes], run_time=0.25)


def resalta(escena, mobs, color=COLOR_ESCALAR, factor=1.3, run_time=0.3):
    """Resaltado inmediato y sostenido (color y tamaño), sin la subida lenta de Indicate."""
    escena.play(*[x.animate.set_color(color).scale(factor) for x in mobs], run_time=run_time)


def apaga(escena, mobs, color=WHITE, factor=1.3, run_time=0.3):
    escena.play(*[x.animate.set_color(color).scale(1/factor) for x in mobs], run_time=run_time)


FACTOR_SENALA = 1.2


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
                grupo.add(VGroup(Tex(cab, font_size=22).set_color(GRAY_B), m).arrange(DOWN, aligned_edge=LEFT, buff=0.2))
            lados.append(grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.42))
        lados[0].to_edge(LEFT, buff=0.4)
        lados[1].to_edge(RIGHT, buff=1.8)   # deja sitio al contador sin tocar la firma del margen (1.5 lo dejaba al ras del borde)
        for g in lados:
            g.align_to([0, y_sup, 0], UP)
        self.todo = VGroup(*lados)
        # la pieza activa crece desde su borde izquierdo (FACTOR_SENALA): el contador se ancla donde acaba entonces,
        # para que no lo pise ni se mueva al volver la pieza a su tamaño
        self.anclas = {c: m.get_left() + m.width*FACTOR_SENALA*RIGHT for c, m in self.piezas.items()}
        self.activa = None   # (glifos, colores originales, factor, recuadro de la pista o None) de la pieza señalada ahora
        self.recuadros = {}  # clave -> recuadro de la pista

    def pista(self, *claves, run_time=0.8):
        marcos = VGroup(*[SurroundingRectangle(self.piezas[c], color=COLOR_ESCALAR, buff=0.06,
                                               corner_radius=0.1, stroke_width=2) for c in claves])
        self.marcos.add(*marcos)
        self.recuadros.update(zip(claves, marcos))
        self.escena.play(*[self.piezas[c].animate.set_color(COLOR_ESCALAR) for c in claves],
                         Create(marcos), run_time=run_time)

    def senala(self, clave, parte=None, factor=None):
        """La pieza que usa el paso (con parte, slice de glifos, solo esa fórmula) crece y pasa a amarillo, y así
        se queda hasta que otro paso señala la suya (Marcos, 2026-11-20: el parpadeo era demasiado corto para ver
        cuál de las dos sumas se aplica). Devuelve las animaciones: soltar la anterior y señalar esta."""
        pieza = self.piezas[clave] if parte is None else self.piezas[clave][0][parte]
        if self.activa is not None and set(map(id, self.activa[0].family_members_with_points())) == set(map(id, pieza.family_members_with_points())):
            return []   # el paso usa la misma pieza que el anterior: sigue señalada
        anims = self.suelta_anims()
        factor = factor or FACTOR_SENALA
        recuadro = self.recuadros.get(clave) if parte is None else None
        self.activa = (pieza, [g.get_color() for g in pieza.family_members_with_points()], factor, recuadro)
        anims.append(pieza.animate.scale(factor, about_edge=LEFT).set_color(COLOR_ESCALAR))
        if recuadro is not None:   # el recuadro de la pista crece con la pieza
            anims.append(recuadro.animate.stretch_to_fit_width(recuadro.width + pieza.width*(factor - 1))
                         .stretch_to_fit_height(recuadro.height + pieza.height*(factor - 1)).align_to(recuadro, LEFT))
        return anims

    def suelta_anims(self):
        if self.activa is None:
            return []
        pieza, colores, factor, recuadro = self.activa
        self.activa = None
        copia = pieza.copy().scale(1/factor, about_edge=LEFT)
        for g, c in zip(copia.family_members_with_points(), colores):
            g.set_color(c)
        anims = [Transform(pieza, copia)]
        if recuadro is not None:
            w0, h0 = pieza.width/factor, pieza.height/factor
            anims.append(recuadro.animate.stretch_to_fit_width(recuadro.width - pieza.width + w0)
                         .stretch_to_fit_height(recuadro.height - pieza.height + h0).align_to(recuadro, LEFT))
        return anims

    def suelta(self, run_time=0.3):
        """Al terminar la cadena, la última pieza señalada vuelve a su tamaño y color."""
        anims = self.suelta_anims()
        if anims:
            self.escena.play(*anims, run_time=run_time)

    def cuenta(self, clave, run_time=0.5):
        self.usos[clave] = self.usos.get(clave, 0) + 1
        disco = Circle(radius=0.17, fill_color=COLOR_TITULO, fill_opacity=1, stroke_width=0)
        numero = Tex(f"\\textbf{{{self.usos[clave]}}}", font_size=24).set_color(WHITE).move_to(disco)
        nuevo = VGroup(disco, numero).move_to(self.anclas[clave] + (0.3 + 0.17)*RIGHT + 0.1*UP)
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
         t_fijos=0.8, t_moviles=0.9, tenue=False):
    """Una expresión nace de la anterior (CLAUDE.md, «Cada expresión nace de la anterior»). origen y destino son
    listas de glifos. Primero, mientras la voz nombra la regla, se copia lo que no cambia (fijos: parejas glifo de
    origen, glifo de destino) y aparece el igual; después (en la marca, si se da) viaja lo que el paso mueve
    (moviles) y surge lo nuevo (aparecen). Lo que se quita no aparece. Un glifo de origen puede ir a dos sitios.
    Con tenue=True (cuando lo fijo, solo, se leería como una igualdad falsa durante un preámbulo largo), lo fijo
    baja atenuado y sin el igual; el igual aparece y lo fijo se enciende cuando llega lo móvil."""
    cubiertos = sorted({j for _, j in fijos} | {j for _, j in moviles} | set(aparecen) | ({0} if con_igual else set()))
    assert cubiertos == list(range(len(destino))), (cubiertos, len(destino))
    al_final = []
    if tenue:
        for _, j in fijos:
            destino[j].set_opacity(0.35)
        al_final = [destino[j].animate.set_opacity(1) for _, j in fijos] + ([FadeIn(destino[0])] if con_igual else [])
    escena.play(*extra, *([FadeIn(destino[0])] if con_igual and not tenue else []),
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
        escena.play(*anims, *[FadeIn(destino[j]) for j in aparecen], *al_final, run_time=t_moviles)
        escena.remove(*sobran)


def entera(escena, linea):
    """Tras nacer glifo a glifo, la línea vuelve a estar en la escena como un solo objeto."""
    escena.remove(*linea[0]); escena.add(linea)


def paso(escena, panel, clave, origen, destino, fijos, moviles=(), aparecen=(), marca=None, t_fijos=0.8, t_moviles=0.9, t_cuenta=0.5,
         parte=None, tenue=False):
    """Un paso de una demostración con panel, en el orden de V06: la pieza parpadea en el panel mientras se copia
    lo que no cambia, la línea se completa (en la marca, si se da) y entonces sube el contador con la campanita.
    Con clave None el paso no usa ninguna pieza del panel (poner o quitar paréntesis)."""
    nace(escena, origen[0], destino[0], fijos, moviles, aparecen, extra=panel.senala(clave, parte) if clave else [], marca=marca,
         t_fijos=t_fijos, t_moviles=t_moviles, tenue=tenue)
    entera(escena, destino)
    if clave:
        panel.cuenta(clave, run_time=t_cuenta)


def recuadra(escena, enunciado, run_time=1.5):
    """Lo demostrado: recuadro amarillo y parpadeo del enunciado."""
    caja = SurroundingRectangle(enunciado, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
    escena.play(Create(caja), Indicate(enunciado, color=COLOR_RESULTADO, scale_factor=1.15), run_time=run_time)
    return caja

class L01_V14_FilasYTransposicion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

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
        
        self.wait(1.0)
        
        with self.voiceover(text=tr("""La suma de matrices se define columna a columna: <bookmark mark='c'/> cada columna de la suma es la suma de las columnas correspondientes.""",
                                    """Matrix addition is defined column by column: <bookmark mark='c'/> each column of the sum is the sum of the corresponding columns.""")) as tracker:
            self.play(FadeIn(A), FadeIn(mas), FadeIn(B), FadeIn(igual), FadeIn(S.get_brackets()), run_time=1)
            self.wait_until_bookmark("c")
            for k in range(3):
                marcos = VGroup(*[marco(m.get_columns()[k], COLOR_COLUMNA) for m in (A, B)])
                self.play(Create(marcos), run_time=0.3)
                self.play(FadeIn(S.get_columns()[k]), run_time=0.4)
                self.play(FadeOut(marcos), run_time=0.2)
        
        self.wait(0.8)
        
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
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Estos ejemplos solo lo ilustran. Ahora vamos a demostrar que ocurre con cualquier matriz.""",
                                    """These examples only illustrate it. Now we are going to prove that it happens with any matrix.""")) as tracker:
            self.play(FadeIn(ilustra, scale=0.9), run_time=0.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("La suma, fila a fila", "Addition, row by row"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self, [(tr("Definición de suma de matrices", "Definition of matrix addition"), "mat", COLS_SUMA)],
                            [(tr("Definición de suma de vectores", "Definition of vector addition"), "vec",   # con el selector a la derecha y a la izquierda: la cadena usa las dos formas
                              r"\elemRp{\Vect{a}+\Vect{b}}{j}&=\eleVR{a}{j}+\eleVR{b}{j}\\ \elemLp{\Vect{a}+\Vect{b}}{i}&=\eleVL{a}{i}+\eleVL{b}{i}")])
        enunciado = MathTex(FILAS_SUMA, tex_template=myTemplate, font_size=44).move_to([-0.9, 1.55, 0])   # a la izquierda: a su derecha, a la misma altura, está la segunda fórmula del panel
        # Glifos: ( i | ( A + B ) ) | j (0-10);  = i | ( ( A + B ) | j ) (0-11);  = i | ( A | j + B | j ) (0-11);
        #         = i | A | j + i | B | j (0-11);  = ( i | A + i | B ) | j (0-11)
        cadena = coloca_cadena([linea(r"\elemR{\Big(\elemLp{\Mat{A}+\Mat{B}}{i}\Big)}{j}"),
                                linea(r"=\elemL{\Big(\elemRp{\Mat{A}+\Mat{B}}{j}\Big)}{i}"),
                                linea(r"=\elemLp{\VectC{A}{j}+\VectC{B}{j}}{i}"),
                                linea(r"=\eleM{A}{i}{j}+\eleM{B}{i}{j}"),
                                linea(r"=\elemR{\Big(\VectF{A}{i}+\VectF{B}{i}\Big)}{j}")])
        res_prod = MathTex(FILAS_PROD, tex_template=myTemplate, font_size=44).move_to([0, -0.6, 0])
        nota_cc = Tex(tr("iguales componente a componente", "equal component by component"), font_size=34, color=GRAY_A).next_to(enunciado, DOWN, buff=0.4)
        lados = [enunciado[0][0:7], enunciado[0][8:]]   # los dos lados del enunciado: dos filas (vectores)
        
        with self.voiceover(text=tr("""Queremos demostrar que <bookmark mark='e'/> cada fila de la suma es la suma de las filas correspondientes.""",
                                    """We want to prove that <bookmark mark='e'/> each row of the sum is the sum of the corresponding rows.""")) as tracker:
            self.play(Write(cabecera), run_time=0.8)
            self.wait_until_bookmark("e")
            self.play(Write(enunciado), run_time=1.2)
        
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Las filas son vectores, y dos vectores son iguales si lo son <bookmark mark='k'/> componente a componente. Usaremos <bookmark mark='p'/> la definición de suma de matrices <bookmark mark='q'/> y la definición de suma de vectores.""",
                                    """Rows are vectors, and two vectors are equal if they are equal <bookmark mark='k'/> component by component. We will use <bookmark mark='p'/> the definition of matrix addition <bookmark mark='q'/> and the definition of vector addition.""")) as tracker:
            self.play(*[x.animate.set_color(COLOR_FILA) for x in lados], run_time=0.3)
            self.wait_until_bookmark("k")
            self.play(FadeIn(nota_cc), run_time=0.5)
            self.wait_until_bookmark("p")
            self.play(FadeOut(nota_cc), *[x.animate.set_color(WHITE) for x in lados], FadeIn(panel.todo[0]), run_time=0.8)
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
        self.wait(0.4)
        
        with self.voiceover(text=tr("""Como da igual seleccionar primero la fila o la columna, <bookmark mark='x'/> podemos desplazar los paréntesis.""",
                                    """Since it does not matter whether we select the row or the column first, <bookmark mark='x'/> we can move the parentheses.""")) as tracker:
            # los paréntesis grandes pasan a rodear la suma con el selector de columnas
            paso(self, panel, None, cadena[0], cadena[1], [(1, 1), (2, 2), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (9, 9), (10, 10)],
                 [(0, 3), (8, 11)], marca="x", t_fijos=0.5)
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Por la definición de suma de matrices <bookmark mark='x'/> podemos distribuir el selector de columnas.""",
                                    """By the definition of matrix addition <bookmark mark='x'/> we can distribute the column selector.""")) as tracker:
            # el selector de columnas va a cada sumando; los paréntesis de la suma de matrices no aparecen
            paso(self, panel, "mat", cadena[1], cadena[2], [(1, 1), (2, 2), (3, 3), (5, 4), (6, 7), (7, 8), (11, 11)],
                 [(9, 5), (10, 6), (9, 9), (10, 10)], marca="x")
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Dentro de los paréntesis hay ahora una suma de dos vectores. <bookmark mark='r'/> Por la definición de suma de vectores <bookmark mark='x'/> podemos distribuir el selector de la izquierda.""",
                                    """Inside the parentheses there is now a sum of two vectors. <bookmark mark='r'/> By the definition of vector addition <bookmark mark='x'/> we can distribute the selector on the left.""")) as tracker:
            # la suma de las dos columnas, señalada en «una suma de dos vectores»; en «Por la definición» parpadea la fórmula
            # del selector de la izquierda y se copia lo fijo; en «podemos distribuir», el selector va a cada sumando
            suma_cols = cadena[2][0][4:11]
            self.play(suma_cols.animate.set_color(COLOR_COLUMNA), run_time=0.3)
            self.wait_until_bookmark("r")
            paso(self, panel, "vec", cadena[2], cadena[3], [(4, 3), (5, 4), (6, 5), (7, 6), (8, 9), (9, 10), (10, 11)],
                 [(1, 1), (2, 2), (1, 7), (2, 8)], marca="x", parte=slice(15, 30))
            self.play(suma_cols.animate.set_color(WHITE), run_time=0.3)
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Cada sumando es una componente de una fila. <bookmark mark='r'/> De nuevo por la definición de suma de vectores, <bookmark mark='x'/> podemos sacar el selector de la derecha como factor común.""",
                                    """Each term is a component of a row. <bookmark mark='r'/> Again by the definition of vector addition, <bookmark mark='x'/> we can factor out the selector on the right.""")) as tracker:
            # las dos filas (i|A, i|B), en amarillo en «una componente de una fila»; los dos selectores de la derecha se
            # reúnen en uno y aparecen los paréntesis alrededor de la suma de las dos filas
            filas_sum = VGroup(cadena[3][0][1:4], cadena[3][0][7:10])
            self.play(filas_sum.animate.set_color(COLOR_FILA), run_time=0.3)
            self.wait_until_bookmark("r")
            paso(self, panel, "vec", cadena[3], cadena[4], [(1, 2), (2, 3), (3, 4), (6, 5), (7, 6), (8, 7), (9, 8)],
                 [(4, 10), (5, 11), (10, 10), (11, 11)], aparecen=[1, 9], marca="x", parte=slice(0, 15))
            self.play(filas_sum.animate.set_color(WHITE), *panel.suelta_anims(), run_time=0.3)
        
        self.wait(0.3)
        # la conclusión dice el criterio de igualdad (Marcos, 2026-11-20): son iguales porque lo son componente a componente
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> los dos vectores son iguales, porque lo son <bookmark mark='c'/> componente a componente. Las matrices también se suman fila a fila.""",
                                    """So <bookmark mark='ok'/> the two vectors are equal, because they are equal <bookmark mark='c'/> component by component. Matrices are also added row by row.""")) as tracker:
            self.wait_until_bookmark("ok")
            caja = recuadra(self, enunciado)
            self.wait_until_bookmark("c")
            indices = [cadena[0][0][10], cadena[4][0][11]]   # el índice de la componente, a los dos extremos
            self.play(*[x.animate.set_color(COLOR_COLUMNA).scale(1.5) for x in indices], run_time=0.3)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in indices], run_time=0.3)
        
        self.wait(1.0)
        
        # partida en dos (auditoría 2026-11-21): la primera frase conserva su toma, recortada (tmp/parte_toma.py); la segunda es
        # nueva: decía «el producto de la fila por el escalar» con el escalar delante en pantalla
        with self.voiceover(text=tr("""Con el producto por un escalar ocurre lo mismo, y se demuestra con los mismos pasos.""",
                                    """The same happens with scalar multiplication, and it is proved with the same steps.""")) as tracker:
            # al retirar el panel, el enunciado vuelve al centro
            self.play(FadeOut(VGroup(*cadena)), FadeOut(panel.todo), FadeOut(VGroup(*panel.contadores.values())), FadeOut(caja),
                      enunciado.animate.set_x(0), run_time=0.8)
        
        with self.voiceover(text=tr("""Cada fila del producto es el producto <bookmark mark='e'/> del escalar por <bookmark mark='g'/> la fila correspondiente.""",
                                    """Each row of the product is <bookmark mark='e'/> the scalar times <bookmark mark='g'/> the corresponding row.""")) as tracker:
            # cada pieza se señala cuando la voz la nombra (Marcos, 2026-11-21): la fila del producto (lado izquierdo), el
            # escalar y la fila de la matriz. glifos: i | ( λ A ) (0-5)  =  λ ( i | A ) (7-12)
            fila_prod, escalar, fila_mat = res_prod[0][0:6], res_prod[0][7], res_prod[0][9:12]
            fila_prod.set_color(COLOR_FILA)
            self.play(FadeIn(res_prod), run_time=0.5)
            self.wait_until_bookmark("e")
            self.play(fila_prod.animate.set_color(WHITE), escalar.animate.set_color(COLOR_ESCALAR).scale(1.4), run_time=0.25)
            self.wait_until_bookmark("g")
            self.play(escalar.animate.set_color(WHITE).scale(1/1.4), fila_mat.animate.set_color(COLOR_FILA).scale(1.15), run_time=0.25)
            self.wait(1.2)
            apaga(self, [fila_mat], factor=1.15, run_time=0.25)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Operadores lineales", "Linear operators"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        
        def columna(formulas, x):
            filas = VGroup(*[MathTex(f, tex_template=myTemplate, font_size=40) for f in formulas]).arrange(DOWN, buff=0.7)
            return filas.move_to([x, 0.1, 0])
        
        cols, fils = columna([COLS_SUMA, COLS_PROD], -3.4), columna([FILAS_SUMA, FILAS_PROD], 3.4)
        r_cols = Tex(tr("Selector de columnas", "Column selector"), font_size=34).set_color(COLOR_COLUMNA).move_to([-3.4, 2.0, 0])
        r_fils = Tex(tr("Selector de filas", "Row selector"), font_size=34).set_color(COLOR_FILA).move_to([3.4, 2.0, 0])
        idea = aviso("idea", tr(r"Operador lineal: se distribuye en las sumas\\ y es asociativo con el producto por un escalar",   # en dos líneas y con las palabras de la voz
                                r"Linear operator: it distributes over sums\\ and is associative with scalar multiplication"), font_size=34).to_edge(DOWN, buff=0.4)
        
        def distribuye(formula, origen, destinos, color):
            """«Se distribuye» (V13): copias del selector de la izquierda viajan a cada sumando de la derecha."""
            sel = VGroup(*[formula[0][k] for k in origen])
            dest = [VGroup(*[formula[0][k] for k in d]) for d in destinos]
            llegadas = [d.copy().set_color(color) for d in dest]
            return sel, dest, llegadas
        
        def viaja(formula, n_izq, mapa, run_time=2.0):
            """Los glifos del lado izquierdo viajan a la colocación del derecho y vuelven (V10, V13, V15);
            mapa[i] es el glifo del lado derecho (contado desde su primer glifo) al que va el glifo i."""
            izq = formula[0][:n_izq]
            der = VGroup(*formula[0][n_izq + 1:]).copy().move_to(izq)
            return [Transform(izq[i], der[j], rate_func=rate_functions.there_and_back_with_pause, run_time=run_time)
                    for i, j in enumerate(mapa)]
        
        with self.voiceover(text=tr("""El selector de columnas y <bookmark mark='f'/> el selector de filas cumplen las mismas reglas.""",
                                    """The column selector and <bookmark mark='f'/> the row selector obey the same rules.""")) as tracker:
            self.play(Write(cabecera), FadeIn(r_cols), FadeIn(cols), run_time=1)
            self.wait_until_bookmark("f")
            self.play(FadeIn(r_fils), FadeIn(fils), run_time=0.8)
        
        self.wait(0.4)
        
        with self.voiceover(text=tr("""Los dos <bookmark mark='s'/> se distribuyen en las sumas. <bookmark mark='p'/> Y los dos son asociativos con el producto por un escalar.""",
                                    """Both <bookmark mark='s'/> distribute over sums. <bookmark mark='p'/> And both are associative with scalar multiplication.""")) as tracker:
            # «se distribuyen»: en las dos reglas de la suma, copias del selector viajan a los dos sumandos (V13)
            self.wait_until_bookmark("s")
            piezas = [distribuye(cols[0], [5, 6], [[9, 10], [13, 14]], COLOR_COLUMNA),
                      distribuye(fils[0], [0, 1], [[8, 9], [12, 13]], COLOR_FILA)]
            self.play(*[sel.animate.set_color(c) for (sel, _, _), c in zip(piezas, (COLOR_COLUMNA, COLOR_FILA))], run_time=0.3)
            self.play(*[d.animate.set_opacity(0.15) for _, dest, _ in piezas for d in dest], run_time=0.25)
            self.play(*[TransformFromCopy(sel, y) for sel, _, lleg in piezas for y in lleg], run_time=1.0)
            for _, dest, lleg in piezas:
                self.remove(*lleg)
            for (_, dest, _), c in zip(piezas, (COLOR_COLUMNA, COLOR_FILA)):
                for d in dest:
                    d.set_opacity(1).set_color(c)
            # «asociativos con el producto por un escalar»: las dos reglas del producto se encienden
            self.wait_until_bookmark("p")
            self.play(*[x.animate.set_color(WHITE) for x in (cols[0], fils[0])], cols[0].animate.set_opacity(0.4),
                      fils[0].animate.set_opacity(0.4), run_time=0.3)
            self.play(cols[1][0][1].animate.set_color(COLOR_ESCALAR), cols[1][0][7].animate.set_color(COLOR_ESCALAR),
                      fils[1][0][3].animate.set_color(COLOR_ESCALAR), fils[1][0][7].animate.set_color(COLOR_ESCALAR),
                      VGroup(*cols[1][0][4:6], *cols[1][0][10:12]).animate.set_color(COLOR_COLUMNA),
                      VGroup(*fils[1][0][0:2], *fils[1][0][9:11]).animate.set_color(COLOR_FILA), run_time=0.3)
        
        self.wait(0.4)
        
        with self.voiceover(text=tr("""Con el de columnas <bookmark mark='c'/> basta desplazar los paréntesis. Con el de filas, <bookmark mark='f'/> el escalar pasa delante del selector.""",
                                    """With the column selector <bookmark mark='c'/> it is enough to move the parentheses. With the row selector, <bookmark mark='f'/> the scalar moves in front of the selector.""")) as tracker:
            # «basta desplazar los paréntesis»: nada cambia de orden, solo viajan los paréntesis
            self.wait_until_bookmark("c")
            self.play(*viaja(cols[1], 6, [1, 0, 2, 5, 3, 4]))
            # «el escalar pasa delante del selector»: el escalar y el selector se cruzan (como en V15, escena 1)
            self.wait_until_bookmark("f")
            self.play(*viaja(fils[1], 6, [2, 3, 1, 0, 4, 5]))
        
        self.wait(0.8)
        
        # la cantinela, justo antes del nombre: en cada verbo se señala la operación (la suma, el escalar) o el selector
        c0, f0, c1, f1 = cols[0][0], fils[0][0], cols[1][0], fils[1][0]
        with self.voiceover(text=tr("""Dicho de otro modo: da igual <bookmark mark='a1'/> sumar primero y <bookmark mark='a2'/> seleccionar después, que <bookmark mark='a3'/> seleccionar primero y <bookmark mark='a4'/> sumar después. Y da igual <bookmark mark='b1'/> multiplicar primero y <bookmark mark='b2'/> seleccionar después, que <bookmark mark='b3'/> seleccionar primero y <bookmark mark='b4'/> multiplicar después.""",
                                    """In other words: it makes no difference whether we <bookmark mark='a1'/> add first and <bookmark mark='a2'/> select afterwards, or <bookmark mark='a3'/> select first and <bookmark mark='a4'/> add afterwards. And it makes no difference whether we <bookmark mark='b1'/> multiply first and <bookmark mark='b2'/> select afterwards, or <bookmark mark='b3'/> select first and <bookmark mark='b4'/> multiply afterwards.""")) as tracker:
            # las reglas de la suma en blanco y a la vista; las del producto, atenuadas
            self.play(cols[0].animate.set_color(WHITE).set_opacity(1), fils[0].animate.set_color(WHITE).set_opacity(1),
                      cols[1].animate.set_color(WHITE).set_opacity(0.4), fils[1].animate.set_color(WHITE).set_opacity(0.4), run_time=0.3)
            cantinela(self, [("a1", [c0[2], f0[4]], COLOR_ESCALAR),
                             ("a2", [c0[5], c0[6], f0[0], f0[1]], [COLOR_COLUMNA]*2 + [COLOR_FILA]*2),
                             ("a3", [c0[9], c0[10], c0[13], c0[14], f0[8], f0[9], f0[12], f0[13]], [COLOR_COLUMNA]*4 + [COLOR_FILA]*4),
                             ("a4", [c0[11], f0[11]], COLOR_ESCALAR)])
            self.play(cols[0].animate.set_opacity(0.4), fils[0].animate.set_opacity(0.4),
                      cols[1].animate.set_opacity(1), fils[1].animate.set_opacity(1), run_time=0.3)
            cantinela(self, [("b1", [c1[1], f1[3]], COLOR_ESCALAR),
                             ("b2", [c1[4], c1[5], f1[0], f1[1]], [COLOR_COLUMNA]*2 + [COLOR_FILA]*2),
                             ("b3", [c1[10], c1[11], f1[9], f1[10]], [COLOR_COLUMNA]*2 + [COLOR_FILA]*2),
                             ("b4", [c1[7], f1[7]], COLOR_ESCALAR)])
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""De un operador que cumple estas dos reglas <bookmark mark='l'/> se dice que es lineal. <bookmark mark='t'/> Veamos que la transposición también lo es.""",
                                    """An operator that obeys these two rules <bookmark mark='l'/> is said to be linear. <bookmark mark='t'/> Let us see that transposition is linear too.""")) as tracker:
            self.play(*[x.animate.set_color(WHITE).set_opacity(1) for x in (cols[0], cols[1], fils[0], fils[1])], run_time=0.3)
            self.wait_until_bookmark("l")
            self.play(FadeIn(idea, scale=0.9), run_time=0.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("La transpuesta de una suma", "The transpose of a sum"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        # el ejemplo, solo con números (Marcos, 2026-11-20): A + B = S arriba, a la vista todo el ejemplo, y debajo
        # cada transpuesta bajo su matriz, A^T + B^T = S^T; al anunciar la demostración, la fila de abajo pasa a letras
        A4, B4, S4 = matriz(A_EJ, COLOR_A, escala=0.72), matriz(B_EJ, COLOR_B, escala=0.72), matriz(S_EJ, escala=0.72)
        mas4, igual4 = MathTex("+", font_size=40), MathTex("=", font_size=40)
        arriba = VGroup(A4, mas4, B4, igual4, S4).arrange(RIGHT, buff=0.4).move_to([0, 1.55, 0])
        At, Bt, St = (matriz(transpuesta(m), c, escala=0.72) for m, c in ((A_EJ, COLOR_A), (B_EJ, COLOR_B), (S_EJ, WHITE)))
        mas, igual = MathTex("+", font_size=40), MathTex("=", font_size=40)
        abajo = VGroup(At, mas, Bt, igual, St)
        for t, o in zip(abajo, arriba):
            t.move_to([o.get_x(), -1.35, 0])
        letras = MathTex(r"\MatT{A}", "+", r"\MatT{B}", "=", r"\Transp{\Mat{A}+\Mat{B}}", tex_template=myTemplate, font_size=44)
        for t, o in zip(letras, abajo):
            t.move_to([o.get_x(), -1.35, 0])
        
        panel = Panel(self, [(tr("Definición de transpuesta", "Definition of the transpose"), "def", DEF_TRANS),
                             (tr("Definición de suma de matrices", "Definition of matrix addition"), "suma", COLS_SUMA)],
                            [(tr("El selector de filas es lineal", "The row selector is linear"), "filas", FILAS_SUMA)])
        enunciado = MathTex(TRANS_SUMA, tex_template=myTemplate, font_size=44).move_to([0.6, 1.1, 0])
        # Glifos: ( ( A + B ) T ) | j (0-9);  = j | ( A + B ) (0-7);  = j | A + j | B (0-7);
        #         = ( A T ) | j + ( B T ) | j (0-13);  = ( A T + B T ) | j (0-9)
        cadena = coloca_cadena([linea(r"\elemRp{\Transp*{\Mat{A}+\Mat{B}}}{j}"),
                                linea(r"=\elemLp{\Mat{A}+\Mat{B}}{j}"),
                                linea(r"=\VectF{A}{j}+\VectF{B}{j}"),
                                linea(r"=\VectTC{A}{j}+\VectTC{B}{j}"),
                                linea(r"=\elemRp{\MatT{A}+\MatT{B}}{j}")], y_sup=0.1, salto=0.72, x_izq=-2.2)
        
        with self.voiceover(text=tr("""Tomemos de nuevo las dos matrices del ejemplo. <bookmark mark='t'/> Si las sumamos y transponemos la suma, <bookmark mark='f'/> sus filas pasan a ser columnas.""",
                                    """Let us take the two matrices of the example again. <bookmark mark='t'/> If we add them and transpose the sum, <bookmark mark='f'/> its rows become columns.""")) as tracker:
            self.play(Write(cabecera), FadeIn(A4), FadeIn(mas4), FadeIn(B4), run_time=1)
            self.wait_until_bookmark("t")
            self.play(FadeIn(igual4), FadeIn(S4), run_time=0.8)
            self.wait_until_bookmark("f")
            # la suma se transpone debajo de ella: su primera fila (recuadrada) pasa a ser la primera columna
            m_fila = marco(S4.get_rows()[0])
            self.play(Create(m_fila), run_time=0.4)
            self.play(TransformFromCopy(S4, St), ReplacementTransform(m_fila, marco(St.get_columns()[0])), run_time=1.2)
            self.wait(0.6)
            self.play(FadeOut(*[m for m in self.mobjects if isinstance(m, SurroundingRectangle)]), run_time=0.3)
        
        with self.voiceover(text=tr("""Y si transponemos primero cada matriz <bookmark mark='s'/> y sumamos después, obtenemos la misma matriz.""",
                                    """And if we first transpose each matrix <bookmark mark='s'/> and then add, we obtain the same matrix.""")) as tracker:
            marcos_f = [marco(A4.get_rows()[0]), marco(B4.get_rows()[0])]
            self.play(*[Create(m) for m in marcos_f], run_time=0.4)
            self.play(TransformFromCopy(A4, At), TransformFromCopy(B4, Bt),
                      ReplacementTransform(marcos_f[0], marco(At.get_columns()[0])),
                      ReplacementTransform(marcos_f[1], marco(Bt.get_columns()[0])), run_time=1.2)
            self.play(FadeOut(*[m for m in self.mobjects if isinstance(m, SurroundingRectangle)]), run_time=0.3)
            self.wait_until_bookmark("s")
            self.play(FadeIn(mas), run_time=0.4)
            self.play(FadeIn(igual), Indicate(St, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.2)
        
        self.pausa_corta()
        
        with self.voiceover(text=tr("""Este ejemplo solo lo ilustra. <bookmark mark='v'/> Vamos a demostrar que siempre da igual <bookmark mark='e1'/> sumar primero y <bookmark mark='e2'/> transponer después, que <bookmark mark='e3'/> transponer primero y <bookmark mark='e4'/> sumar después.""",
                                    """This example only illustrates it. <bookmark mark='v'/> We are going to prove that it always makes no difference whether we <bookmark mark='e1'/> add first and <bookmark mark='e2'/> transpose afterwards, or <bookmark mark='e3'/> transpose first and <bookmark mark='e4'/> add afterwards.""")) as tracker:
            # transición a letras: cada matriz de la fila de abajo se funde con su nombre (fundido cruzado: FadeTransform
            # agrandaba las letras al tamaño de las matrices) y, tras reposar un segundo, la fila pasa a ser el enunciado
            self.play(FadeOut(arriba), *[FadeOut(n) for n in abajo], *[FadeIn(l) for l in letras], run_time=1.0)
            self.wait_until_bookmark("v")
            # cada trozo viaja a su lado del enunciado: (A+B)^T a la izquierda, A^T + B^T a la derecha
            e = enunciado[0]
            destinos = [VGroup(*e[7:9]), e[9], VGroup(*e[10:12]), e[6], VGroup(*e[0:6])]
            llegadas = [d.copy() for d in destinos]
            self.play(*[ReplacementTransform(l, d, path_arc=PI/2) for l, d in zip(letras, llegadas)], run_time=1.4)   # los lados se cruzan por arriba y por abajo
            self.remove(*llegadas); self.add(enunciado)
            # la cantinela sobre el enunciado: la suma y la transposición, cada una en su verbo
            cantinela(self, [("e1", [e[2]], COLOR_ESCALAR), ("e2", [e[5]], COLOR_TRANSP),
                             ("e3", [e[8], e[11]], COLOR_TRANSP), ("e4", [e[9]], COLOR_ESCALAR)])
        
        with self.voiceover(text=tr("""Para demostrarlo necesitará <bookmark mark='p'/> la definición de transpuesta, <bookmark mark='q'/> que el selector de filas es lineal, <bookmark mark='r'/> y la definición de suma de matrices.""",
                                    """To prove it you will need <bookmark mark='p'/> the definition of the transpose, <bookmark mark='q'/> the fact that the row selector is linear, <bookmark mark='r'/> and the definition of matrix addition.""")) as tracker:
            self.play(FadeIn(panel.todo), run_time=0.6)   # el panel aparece cuando la voz lo nombra (auditoría 2026-11-21)
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
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Como el selector de filas es lineal, <bookmark mark='x'/> podemos distribuirlo entre los sumandos.""",
                                    """Since the row selector is linear, <bookmark mark='x'/> we can distribute it over the terms.""")) as tracker:
            paso(self, panel, "filas", cadena[1], cadena[2], [(4, 3), (5, 4), (6, 7)], [(1, 1), (2, 2), (1, 5), (2, 6)], marca="x")
        self.wait(0.5)
        
        with self.voiceover(text=tr("""De nuevo por la definición de transpuesta, <bookmark mark='x'/> cada fila es una columna de la transpuesta, y el índice vuelve a la derecha.""",
                                    """Again by the definition of the transpose, <bookmark mark='x'/> each row is a column of the transpose, and the index goes back to the right.""")) as tracker:
            paso(self, panel, "def", cadena[2], cadena[3], [(3, 2), (4, 7), (7, 9)], [(1, 6), (2, 5), (5, 13), (6, 12)],
                 aparecen=[1, 3, 4, 8, 10, 11], marca="x")
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Y por la definición de suma de matrices <bookmark mark='x'/> podemos sacar el selector como factor común.""",
                                    """And by the definition of matrix addition <bookmark mark='x'/> we can factor out the selector.""")) as tracker:
            paso(self, panel, "suma", cadena[3], cadena[4], [(2, 2), (3, 3), (7, 4), (9, 5), (10, 6)],
                 [(5, 8), (6, 9), (12, 8), (13, 9), (1, 1), (11, 7)], marca="x")
            panel.suelta()
        
        self.wait(0.5)
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> las dos matrices son iguales, porque lo son <bookmark mark='c'/> columna a columna.""",
                                    """So <bookmark mark='ok'/> the two matrices are equal, because they are equal <bookmark mark='c'/> column by column.""")) as tracker:
            self.wait_until_bookmark("ok")
            recuadra(self, enunciado)
            self.wait_until_bookmark("c")
            indices = [cadena[0][0][9], cadena[4][0][9]]   # el índice de la columna, a los dos extremos
            self.play(*[x.animate.set_color(COLOR_COLUMNA).scale(1.5) for x in indices], run_time=0.3)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in indices], run_time=0.3)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("La transpuesta de un producto por un escalar", "The transpose of a product by a scalar"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self, [(tr("Definición de transpuesta", "Definition of the transpose"), "def", DEF_TRANS),
                             (tr("Definición de producto por un escalar", "Definition of the product by a scalar"), "prod", COLS_PROD)],
                            [(tr("El selector de filas es lineal", "The row selector is linear"), "filas", FILAS_PROD)])
        enunciado = MathTex(TRANS_PROD, tex_template=myTemplate, font_size=44).move_to([0.6, 1.1, 0])
        # Glifos: ( ( λ A ) T ) | j (0-8);  = j | ( λ A ) (0-6);  = λ ( j | A ) (0-6);
        #         = λ ( ( A T ) | j ) (0-9);  = ( λ ( A T ) ) | j (0-9)
        cadena = coloca_cadena([linea(r"\elemRp{\Transp*{\lambda\Mat{A}}}{j}"),
                                linea(r"=\elemLp{\lambda\Mat{A}}{j}"),
                                linea(r"=\lambda\VectFpE{A}{j}"),
                                linea(r"=\lambda\VectTCpE{A}{j}"),
                                linea(r"=\elemRp{\lambda\MatTpE{A}}{j}")], y_sup=0.2, salto=0.66, x_izq=-1.8)
        idea = aviso("idea", tr("La transposición es un operador lineal", "Transposition is a linear operator"), font_size=32).to_edge(DOWN, buff=0.15)
        # las dos reglas demostradas, juntas, para la frase que cierra la escena. Glifos: ( A + B ) T = A T + B T (0-11);
        # ( λ A ) T = λ ( A T ) (0-10)
        regla_suma, regla_prod = [MathTex(f, tex_template=myTemplate, font_size=52) for f in (TRANS_SUMA, TRANS_PROD)]
        VGroup(regla_suma, regla_prod).arrange(DOWN, buff=1.0).move_to([0, 0.5, 0])
        de_fondo = list(self.mobjects)   # lo que no es de la escena (la firma del margen)
        
        with self.voiceover(text=tr("""Con el producto por un escalar ocurre lo mismo: <bookmark mark='e'/> da igual <bookmark mark='e1'/> multiplicar primero y <bookmark mark='e2'/> transponer después, <bookmark mark='d'/> que <bookmark mark='e3'/> transponer primero y <bookmark mark='e4'/> multiplicar después.""",
                                    """The same happens with scalar multiplication: <bookmark mark='e'/> it makes no difference whether we <bookmark mark='e1'/> multiply first and <bookmark mark='e2'/> transpose afterwards, <bookmark mark='d'/> or <bookmark mark='e3'/> transpose first and <bookmark mark='e4'/> multiply afterwards.""")) as tracker:
            self.play(Write(cabecera), FadeIn(panel.todo), run_time=1)
            # cada lado del enunciado se escribe en su frase, y en cada verbo se señala el escalar o la transposición
            e = enunciado[0]
            self.wait_until_bookmark("e")
            self.play(Write(VGroup(*e[0:5])), run_time=0.5)
            cantinela(self, [("e1", [e[1]], COLOR_ESCALAR), ("e2", [e[4]], COLOR_TRANSP)])
            self.wait_until_bookmark("d")
            self.play(Write(VGroup(*e[5:11])), run_time=0.5)
            cantinela(self, [("e3", [e[9]], COLOR_TRANSP), ("e4", [e[6]], COLOR_ESCALAR)])
        
        self.pausa_para_pensar(invitacion=tr("Demuéstrelo con los mismos pasos.", "Prove it with the same steps."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrarlo con los mismos pasos que en la suma.",
                                                 "Pause the video and try to prove it with the same steps as for the sum."))
        
        with self.voiceover(text=tr("""Los pasos son los mismos. <bookmark mark='l0'/> Seleccionamos una columna cualquiera <bookmark mark='l1'/> y quitamos la transposición cambiando de lado el índice.""",
                                    """The steps are the same. <bookmark mark='l0'/> We select any column <bookmark mark='l1'/> and remove the transposition by moving the index to the other side.""")) as tracker:
            # «una columna cualquiera», como en las escenas 2 y 4 (Marcos, 2026-11-21): la locución se partió tras «...el índice.»
            # (toma nueva de la primera parte; la segunda conserva la suya) y entre las dos va la pausa que tenía la toma entera
            rapido = dict(t_fijos=0.5, t_moviles=0.6, t_cuenta=0.35)
            self.wait_until_bookmark("l0")
            self.play(TransformFromCopy(enunciado[0][0:5], cadena[0][0][1:6]), FadeIn(cadena[0][0][0]), FadeIn(cadena[0][0][6:]), run_time=0.8)
            entera(self, cadena[0])
            self.wait_until_bookmark("l1")   # el selector cruza a la izquierda; la T y los paréntesis de fuera no aparecen
            paso(self, panel, "def", cadena[0], cadena[1], [(1, 3), (2, 4), (3, 5), (4, 6)], [(7, 2), (8, 1)], **rapido)
        
        self.wait(0.45)
        with self.voiceover(text=tr("""Como el selector de filas es lineal, <bookmark mark='m2'/> podemos sacar el escalar. <bookmark mark='l3'/> La fila es una columna de la transpuesta. <bookmark mark='l4'/> Y por la definición de producto por un escalar <bookmark mark='m4'/> podemos desplazar los paréntesis.""",
                                    """Since the row selector is linear, <bookmark mark='m2'/> we can take the scalar out. <bookmark mark='l3'/> The row is a column of the transpose. <bookmark mark='l4'/> And by the definition of the product by a scalar <bookmark mark='m4'/> we can move the parentheses.""")) as tracker:
            # primero baja «( A )»; en «sacar el escalar» el escalar sale delante y el selector entra
            # en los paréntesis (Marcos, 2026-11-20: antes viajaban los paréntesis, que no son lo que el paso mueve). «( A )»
            # baja atenuado y sin el igual, para que no se lea «= ( A )» mientras la voz dice el preámbulo (2026-11-21)
            paso(self, panel, "filas", cadena[1], cadena[2], [(3, 2), (5, 5), (6, 6)], [(4, 1), (1, 3), (2, 4)], marca="m2", tenue=True, **rapido)
            self.wait_until_bookmark("l3")   # el índice vuelve a la derecha, con la T y sus paréntesis
            paso(self, panel, "def", cadena[2], cadena[3], [(1, 1), (2, 2), (6, 9), (5, 4)], [(3, 8), (4, 7)], aparecen=[3, 5, 6], **rapido)
            self.wait_until_bookmark("l4")   # los paréntesis pasan a rodear el producto y dejan fuera el selector
            paso(self, panel, "prod", cadena[3], cadena[4], [(1, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 8), (8, 9)], [(2, 1), (9, 7)], marca="m4", **rapido)
            panel.suelta()
        
        self.wait(0.4)
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> las dos matrices son iguales, porque lo son <bookmark mark='c'/> columna a columna.""",
                                    """So <bookmark mark='ok'/> the two matrices are equal, because they are equal <bookmark mark='c'/> column by column.""")) as tracker:
            self.wait_until_bookmark("ok")
            recuadra(self, enunciado)
            self.wait_until_bookmark("c")
            indices = [cadena[0][0][-1], cadena[4][0][-1]]   # el índice de la columna, a los dos extremos
            self.play(*[x.animate.set_color(COLOR_COLUMNA).scale(1.5) for x in indices], run_time=0.3)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in indices], run_time=0.3)
        
        self.wait(0.8)
        
        # El cierre nombra las dos reglas, así que el espectador las tiene delante (Marcos, 2026-11-21): la demostración se
        # retira y quedan la regla de la suma (escena 4) y la del producto, cada una señalada en su frase: la transposición
        # (morado) y la operación (amarillo). Marcas s y p injertadas en la toma que ya había.
        self.play(FadeOut(*[m for m in self.mobjects if m not in de_fondo]), run_time=0.6)
        with self.voiceover(text=tr("""La transposición <bookmark mark='s'/> se distribuye en las sumas y <bookmark mark='p'/> es asociativa con el producto por un escalar: <bookmark mark='i'/> también es un operador lineal.""",
                                    """Transposition <bookmark mark='s'/> distributes over sums and <bookmark mark='p'/> is associative with scalar multiplication: <bookmark mark='i'/> it is a linear operator too.""")) as tracker:
            rs, rp = regla_suma[0], regla_prod[0]
            de_suma = [(rs[5], COLOR_TRANSP), (rs[8], COLOR_TRANSP), (rs[11], COLOR_TRANSP), (rs[2], COLOR_ESCALAR), (rs[9], COLOR_ESCALAR)]
            de_prod = [(rp[4], COLOR_TRANSP), (rp[9], COLOR_TRANSP), (rp[1], COLOR_ESCALAR), (rp[6], COLOR_ESCALAR)]
            self.play(FadeIn(regla_suma), run_time=0.5)
            self.wait_until_bookmark("s")
            self.play(*[g.animate.set_color(c).scale(1.3) for g, c in de_suma], run_time=0.25)
            self.wait_until_bookmark("p")
            self.play(*[g.animate.set_color(WHITE).scale(1/1.3) for g, c in de_suma], FadeIn(regla_prod), run_time=0.3)
            self.play(*[g.animate.set_color(c).scale(1.3) for g, c in de_prod], run_time=0.25)
            self.wait_until_bookmark("i")
            self.play(*[g.animate.set_color(WHITE).scale(1/1.3) for g, c in de_prod], FadeIn(idea, scale=0.9), run_time=0.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [FILAS_SUMA + r"\qquad\quad " + FILAS_PROD, TRANS_SUMA + r"\qquad\quad " + TRANS_PROD]
        rotulos = [tr("las matrices también se suman y se multiplican por un escalar fila a fila",
                      "matrices are also added and multiplied by a scalar row by row"),
                   tr("la transposición es lineal, como los selectores de filas y de columnas",
                      "transposition is linear, like the row and column selectors")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=40), Tex(r, font_size=34, color=GRAY_A)).arrange(DOWN, buff=0.25)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.9).move_to([0, -0.2, 0])
        
        with self.voiceover(text=tr("""Resumamos. Las matrices también se suman y se multiplican por un escalar fila a fila: el selector de filas es lineal, como el de columnas. <bookmark mark='t'/> La transposición también es lineal.""",
                                    """Let us sum up. Matrices are also added and multiplied by a scalar row by row: the row selector is linear, like the column selector. <bookmark mark='t'/> Transposition is linear too.""")) as tracker:
            # la descripción de las dos reglas se quitó (Marcos, 2026-11-21): la escena 5 ya las enseña juntas al cerrar; la
            # toma es la que había, cortada tras «...también es lineal.»
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("t")
            self.play(FadeIn(filas[1]), run_time=0.8)
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos una última extensión de la notación: escribir a la derecha el escalar de un producto.""",
                                    """In the next video we will see one last extension of the notation: writing the scalar of a product on the right.""")) as tracker:
            pass
        
        self.pausa_media()


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
        
        self.wait(1.0)
        
        with self.voiceover(text=tr("""La suma de matrices se define columna a columna: <bookmark mark='c'/> cada columna de la suma es la suma de las columnas correspondientes.""",
                                    """Matrix addition is defined column by column: <bookmark mark='c'/> each column of the sum is the sum of the corresponding columns.""")) as tracker:
            self.play(FadeIn(A), FadeIn(mas), FadeIn(B), FadeIn(igual), FadeIn(S.get_brackets()), run_time=1)
            self.wait_until_bookmark("c")
            for k in range(3):
                marcos = VGroup(*[marco(m.get_columns()[k], COLOR_COLUMNA) for m in (A, B)])
                self.play(Create(marcos), run_time=0.3)
                self.play(FadeIn(S.get_columns()[k]), run_time=0.4)
                self.play(FadeOut(marcos), run_time=0.2)
        
        self.wait(0.8)
        
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
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Estos ejemplos solo lo ilustran. Ahora vamos a demostrar que ocurre con cualquier matriz.""",
                                    """These examples only illustrate it. Now we are going to prove that it happens with any matrix.""")) as tracker:
            self.play(FadeIn(ilustra, scale=0.9), run_time=0.8)
        
        self.pausa_media()


class L01_V14_E02_SumaPorFilas(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La suma, fila a fila", "Addition, row by row"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self, [(tr("Definición de suma de matrices", "Definition of matrix addition"), "mat", COLS_SUMA)],
                            [(tr("Definición de suma de vectores", "Definition of vector addition"), "vec",   # con el selector a la derecha y a la izquierda: la cadena usa las dos formas
                              r"\elemRp{\Vect{a}+\Vect{b}}{j}&=\eleVR{a}{j}+\eleVR{b}{j}\\ \elemLp{\Vect{a}+\Vect{b}}{i}&=\eleVL{a}{i}+\eleVL{b}{i}")])
        enunciado = MathTex(FILAS_SUMA, tex_template=myTemplate, font_size=44).move_to([-0.9, 1.55, 0])   # a la izquierda: a su derecha, a la misma altura, está la segunda fórmula del panel
        # Glifos: ( i | ( A + B ) ) | j (0-10);  = i | ( ( A + B ) | j ) (0-11);  = i | ( A | j + B | j ) (0-11);
        #         = i | A | j + i | B | j (0-11);  = ( i | A + i | B ) | j (0-11)
        cadena = coloca_cadena([linea(r"\elemR{\Big(\elemLp{\Mat{A}+\Mat{B}}{i}\Big)}{j}"),
                                linea(r"=\elemL{\Big(\elemRp{\Mat{A}+\Mat{B}}{j}\Big)}{i}"),
                                linea(r"=\elemLp{\VectC{A}{j}+\VectC{B}{j}}{i}"),
                                linea(r"=\eleM{A}{i}{j}+\eleM{B}{i}{j}"),
                                linea(r"=\elemR{\Big(\VectF{A}{i}+\VectF{B}{i}\Big)}{j}")])
        res_prod = MathTex(FILAS_PROD, tex_template=myTemplate, font_size=44).move_to([0, -0.6, 0])
        nota_cc = Tex(tr("iguales componente a componente", "equal component by component"), font_size=34, color=GRAY_A).next_to(enunciado, DOWN, buff=0.4)
        lados = [enunciado[0][0:7], enunciado[0][8:]]   # los dos lados del enunciado: dos filas (vectores)
        
        with self.voiceover(text=tr("""Queremos demostrar que <bookmark mark='e'/> cada fila de la suma es la suma de las filas correspondientes.""",
                                    """We want to prove that <bookmark mark='e'/> each row of the sum is the sum of the corresponding rows.""")) as tracker:
            self.play(Write(cabecera), run_time=0.8)
            self.wait_until_bookmark("e")
            self.play(Write(enunciado), run_time=1.2)
        
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Las filas son vectores, y dos vectores son iguales si lo son <bookmark mark='k'/> componente a componente. Usaremos <bookmark mark='p'/> la definición de suma de matrices <bookmark mark='q'/> y la definición de suma de vectores.""",
                                    """Rows are vectors, and two vectors are equal if they are equal <bookmark mark='k'/> component by component. We will use <bookmark mark='p'/> the definition of matrix addition <bookmark mark='q'/> and the definition of vector addition.""")) as tracker:
            self.play(*[x.animate.set_color(COLOR_FILA) for x in lados], run_time=0.3)
            self.wait_until_bookmark("k")
            self.play(FadeIn(nota_cc), run_time=0.5)
            self.wait_until_bookmark("p")
            self.play(FadeOut(nota_cc), *[x.animate.set_color(WHITE) for x in lados], FadeIn(panel.todo[0]), run_time=0.8)
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
        self.wait(0.4)
        
        with self.voiceover(text=tr("""Como da igual seleccionar primero la fila o la columna, <bookmark mark='x'/> podemos desplazar los paréntesis.""",
                                    """Since it does not matter whether we select the row or the column first, <bookmark mark='x'/> we can move the parentheses.""")) as tracker:
            # los paréntesis grandes pasan a rodear la suma con el selector de columnas
            paso(self, panel, None, cadena[0], cadena[1], [(1, 1), (2, 2), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (9, 9), (10, 10)],
                 [(0, 3), (8, 11)], marca="x", t_fijos=0.5)
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Por la definición de suma de matrices <bookmark mark='x'/> podemos distribuir el selector de columnas.""",
                                    """By the definition of matrix addition <bookmark mark='x'/> we can distribute the column selector.""")) as tracker:
            # el selector de columnas va a cada sumando; los paréntesis de la suma de matrices no aparecen
            paso(self, panel, "mat", cadena[1], cadena[2], [(1, 1), (2, 2), (3, 3), (5, 4), (6, 7), (7, 8), (11, 11)],
                 [(9, 5), (10, 6), (9, 9), (10, 10)], marca="x")
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Dentro de los paréntesis hay ahora una suma de dos vectores. <bookmark mark='r'/> Por la definición de suma de vectores <bookmark mark='x'/> podemos distribuir el selector de la izquierda.""",
                                    """Inside the parentheses there is now a sum of two vectors. <bookmark mark='r'/> By the definition of vector addition <bookmark mark='x'/> we can distribute the selector on the left.""")) as tracker:
            # la suma de las dos columnas, señalada en «una suma de dos vectores»; en «Por la definición» parpadea la fórmula
            # del selector de la izquierda y se copia lo fijo; en «podemos distribuir», el selector va a cada sumando
            suma_cols = cadena[2][0][4:11]
            self.play(suma_cols.animate.set_color(COLOR_COLUMNA), run_time=0.3)
            self.wait_until_bookmark("r")
            paso(self, panel, "vec", cadena[2], cadena[3], [(4, 3), (5, 4), (6, 5), (7, 6), (8, 9), (9, 10), (10, 11)],
                 [(1, 1), (2, 2), (1, 7), (2, 8)], marca="x", parte=slice(15, 30))
            self.play(suma_cols.animate.set_color(WHITE), run_time=0.3)
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Cada sumando es una componente de una fila. <bookmark mark='r'/> De nuevo por la definición de suma de vectores, <bookmark mark='x'/> podemos sacar el selector de la derecha como factor común.""",
                                    """Each term is a component of a row. <bookmark mark='r'/> Again by the definition of vector addition, <bookmark mark='x'/> we can factor out the selector on the right.""")) as tracker:
            # las dos filas (i|A, i|B), en amarillo en «una componente de una fila»; los dos selectores de la derecha se
            # reúnen en uno y aparecen los paréntesis alrededor de la suma de las dos filas
            filas_sum = VGroup(cadena[3][0][1:4], cadena[3][0][7:10])
            self.play(filas_sum.animate.set_color(COLOR_FILA), run_time=0.3)
            self.wait_until_bookmark("r")
            paso(self, panel, "vec", cadena[3], cadena[4], [(1, 2), (2, 3), (3, 4), (6, 5), (7, 6), (8, 7), (9, 8)],
                 [(4, 10), (5, 11), (10, 10), (11, 11)], aparecen=[1, 9], marca="x", parte=slice(0, 15))
            self.play(filas_sum.animate.set_color(WHITE), *panel.suelta_anims(), run_time=0.3)
        
        self.wait(0.3)
        # la conclusión dice el criterio de igualdad (Marcos, 2026-11-20): son iguales porque lo son componente a componente
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> los dos vectores son iguales, porque lo son <bookmark mark='c'/> componente a componente. Las matrices también se suman fila a fila.""",
                                    """So <bookmark mark='ok'/> the two vectors are equal, because they are equal <bookmark mark='c'/> component by component. Matrices are also added row by row.""")) as tracker:
            self.wait_until_bookmark("ok")
            caja = recuadra(self, enunciado)
            self.wait_until_bookmark("c")
            indices = [cadena[0][0][10], cadena[4][0][11]]   # el índice de la componente, a los dos extremos
            self.play(*[x.animate.set_color(COLOR_COLUMNA).scale(1.5) for x in indices], run_time=0.3)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in indices], run_time=0.3)
        
        self.wait(1.0)
        
        # partida en dos (auditoría 2026-11-21): la primera frase conserva su toma, recortada (tmp/parte_toma.py); la segunda es
        # nueva: decía «el producto de la fila por el escalar» con el escalar delante en pantalla
        with self.voiceover(text=tr("""Con el producto por un escalar ocurre lo mismo, y se demuestra con los mismos pasos.""",
                                    """The same happens with scalar multiplication, and it is proved with the same steps.""")) as tracker:
            # al retirar el panel, el enunciado vuelve al centro
            self.play(FadeOut(VGroup(*cadena)), FadeOut(panel.todo), FadeOut(VGroup(*panel.contadores.values())), FadeOut(caja),
                      enunciado.animate.set_x(0), run_time=0.8)
        
        with self.voiceover(text=tr("""Cada fila del producto es el producto <bookmark mark='e'/> del escalar por <bookmark mark='g'/> la fila correspondiente.""",
                                    """Each row of the product is <bookmark mark='e'/> the scalar times <bookmark mark='g'/> the corresponding row.""")) as tracker:
            # cada pieza se señala cuando la voz la nombra (Marcos, 2026-11-21): la fila del producto (lado izquierdo), el
            # escalar y la fila de la matriz. glifos: i | ( λ A ) (0-5)  =  λ ( i | A ) (7-12)
            fila_prod, escalar, fila_mat = res_prod[0][0:6], res_prod[0][7], res_prod[0][9:12]
            fila_prod.set_color(COLOR_FILA)
            self.play(FadeIn(res_prod), run_time=0.5)
            self.wait_until_bookmark("e")
            self.play(fila_prod.animate.set_color(WHITE), escalar.animate.set_color(COLOR_ESCALAR).scale(1.4), run_time=0.25)
            self.wait_until_bookmark("g")
            self.play(escalar.animate.set_color(WHITE).scale(1/1.4), fila_mat.animate.set_color(COLOR_FILA).scale(1.15), run_time=0.25)
            self.wait(1.2)
            apaga(self, [fila_mat], factor=1.15, run_time=0.25)
        
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
        idea = aviso("idea", tr(r"Operador lineal: se distribuye en las sumas\\ y es asociativo con el producto por un escalar",   # en dos líneas y con las palabras de la voz
                                r"Linear operator: it distributes over sums\\ and is associative with scalar multiplication"), font_size=34).to_edge(DOWN, buff=0.4)
        
        def distribuye(formula, origen, destinos, color):
            """«Se distribuye» (V13): copias del selector de la izquierda viajan a cada sumando de la derecha."""
            sel = VGroup(*[formula[0][k] for k in origen])
            dest = [VGroup(*[formula[0][k] for k in d]) for d in destinos]
            llegadas = [d.copy().set_color(color) for d in dest]
            return sel, dest, llegadas
        
        def viaja(formula, n_izq, mapa, run_time=2.0):
            """Los glifos del lado izquierdo viajan a la colocación del derecho y vuelven (V10, V13, V15);
            mapa[i] es el glifo del lado derecho (contado desde su primer glifo) al que va el glifo i."""
            izq = formula[0][:n_izq]
            der = VGroup(*formula[0][n_izq + 1:]).copy().move_to(izq)
            return [Transform(izq[i], der[j], rate_func=rate_functions.there_and_back_with_pause, run_time=run_time)
                    for i, j in enumerate(mapa)]
        
        with self.voiceover(text=tr("""El selector de columnas y <bookmark mark='f'/> el selector de filas cumplen las mismas reglas.""",
                                    """The column selector and <bookmark mark='f'/> the row selector obey the same rules.""")) as tracker:
            self.play(Write(cabecera), FadeIn(r_cols), FadeIn(cols), run_time=1)
            self.wait_until_bookmark("f")
            self.play(FadeIn(r_fils), FadeIn(fils), run_time=0.8)
        
        self.wait(0.4)
        
        with self.voiceover(text=tr("""Los dos <bookmark mark='s'/> se distribuyen en las sumas. <bookmark mark='p'/> Y los dos son asociativos con el producto por un escalar.""",
                                    """Both <bookmark mark='s'/> distribute over sums. <bookmark mark='p'/> And both are associative with scalar multiplication.""")) as tracker:
            # «se distribuyen»: en las dos reglas de la suma, copias del selector viajan a los dos sumandos (V13)
            self.wait_until_bookmark("s")
            piezas = [distribuye(cols[0], [5, 6], [[9, 10], [13, 14]], COLOR_COLUMNA),
                      distribuye(fils[0], [0, 1], [[8, 9], [12, 13]], COLOR_FILA)]
            self.play(*[sel.animate.set_color(c) for (sel, _, _), c in zip(piezas, (COLOR_COLUMNA, COLOR_FILA))], run_time=0.3)
            self.play(*[d.animate.set_opacity(0.15) for _, dest, _ in piezas for d in dest], run_time=0.25)
            self.play(*[TransformFromCopy(sel, y) for sel, _, lleg in piezas for y in lleg], run_time=1.0)
            for _, dest, lleg in piezas:
                self.remove(*lleg)
            for (_, dest, _), c in zip(piezas, (COLOR_COLUMNA, COLOR_FILA)):
                for d in dest:
                    d.set_opacity(1).set_color(c)
            # «asociativos con el producto por un escalar»: las dos reglas del producto se encienden
            self.wait_until_bookmark("p")
            self.play(*[x.animate.set_color(WHITE) for x in (cols[0], fils[0])], cols[0].animate.set_opacity(0.4),
                      fils[0].animate.set_opacity(0.4), run_time=0.3)
            self.play(cols[1][0][1].animate.set_color(COLOR_ESCALAR), cols[1][0][7].animate.set_color(COLOR_ESCALAR),
                      fils[1][0][3].animate.set_color(COLOR_ESCALAR), fils[1][0][7].animate.set_color(COLOR_ESCALAR),
                      VGroup(*cols[1][0][4:6], *cols[1][0][10:12]).animate.set_color(COLOR_COLUMNA),
                      VGroup(*fils[1][0][0:2], *fils[1][0][9:11]).animate.set_color(COLOR_FILA), run_time=0.3)
        
        self.wait(0.4)
        
        with self.voiceover(text=tr("""Con el de columnas <bookmark mark='c'/> basta desplazar los paréntesis. Con el de filas, <bookmark mark='f'/> el escalar pasa delante del selector.""",
                                    """With the column selector <bookmark mark='c'/> it is enough to move the parentheses. With the row selector, <bookmark mark='f'/> the scalar moves in front of the selector.""")) as tracker:
            # «basta desplazar los paréntesis»: nada cambia de orden, solo viajan los paréntesis
            self.wait_until_bookmark("c")
            self.play(*viaja(cols[1], 6, [1, 0, 2, 5, 3, 4]))
            # «el escalar pasa delante del selector»: el escalar y el selector se cruzan (como en V15, escena 1)
            self.wait_until_bookmark("f")
            self.play(*viaja(fils[1], 6, [2, 3, 1, 0, 4, 5]))
        
        self.wait(0.8)
        
        # la cantinela, justo antes del nombre: en cada verbo se señala la operación (la suma, el escalar) o el selector
        c0, f0, c1, f1 = cols[0][0], fils[0][0], cols[1][0], fils[1][0]
        with self.voiceover(text=tr("""Dicho de otro modo: da igual <bookmark mark='a1'/> sumar primero y <bookmark mark='a2'/> seleccionar después, que <bookmark mark='a3'/> seleccionar primero y <bookmark mark='a4'/> sumar después. Y da igual <bookmark mark='b1'/> multiplicar primero y <bookmark mark='b2'/> seleccionar después, que <bookmark mark='b3'/> seleccionar primero y <bookmark mark='b4'/> multiplicar después.""",
                                    """In other words: it makes no difference whether we <bookmark mark='a1'/> add first and <bookmark mark='a2'/> select afterwards, or <bookmark mark='a3'/> select first and <bookmark mark='a4'/> add afterwards. And it makes no difference whether we <bookmark mark='b1'/> multiply first and <bookmark mark='b2'/> select afterwards, or <bookmark mark='b3'/> select first and <bookmark mark='b4'/> multiply afterwards.""")) as tracker:
            # las reglas de la suma en blanco y a la vista; las del producto, atenuadas
            self.play(cols[0].animate.set_color(WHITE).set_opacity(1), fils[0].animate.set_color(WHITE).set_opacity(1),
                      cols[1].animate.set_color(WHITE).set_opacity(0.4), fils[1].animate.set_color(WHITE).set_opacity(0.4), run_time=0.3)
            cantinela(self, [("a1", [c0[2], f0[4]], COLOR_ESCALAR),
                             ("a2", [c0[5], c0[6], f0[0], f0[1]], [COLOR_COLUMNA]*2 + [COLOR_FILA]*2),
                             ("a3", [c0[9], c0[10], c0[13], c0[14], f0[8], f0[9], f0[12], f0[13]], [COLOR_COLUMNA]*4 + [COLOR_FILA]*4),
                             ("a4", [c0[11], f0[11]], COLOR_ESCALAR)])
            self.play(cols[0].animate.set_opacity(0.4), fils[0].animate.set_opacity(0.4),
                      cols[1].animate.set_opacity(1), fils[1].animate.set_opacity(1), run_time=0.3)
            cantinela(self, [("b1", [c1[1], f1[3]], COLOR_ESCALAR),
                             ("b2", [c1[4], c1[5], f1[0], f1[1]], [COLOR_COLUMNA]*2 + [COLOR_FILA]*2),
                             ("b3", [c1[10], c1[11], f1[9], f1[10]], [COLOR_COLUMNA]*2 + [COLOR_FILA]*2),
                             ("b4", [c1[7], f1[7]], COLOR_ESCALAR)])
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""De un operador que cumple estas dos reglas <bookmark mark='l'/> se dice que es lineal. <bookmark mark='t'/> Veamos que la transposición también lo es.""",
                                    """An operator that obeys these two rules <bookmark mark='l'/> is said to be linear. <bookmark mark='t'/> Let us see that transposition is linear too.""")) as tracker:
            self.play(*[x.animate.set_color(WHITE).set_opacity(1) for x in (cols[0], cols[1], fils[0], fils[1])], run_time=0.3)
            self.wait_until_bookmark("l")
            self.play(FadeIn(idea, scale=0.9), run_time=0.8)
        
        self.pausa_media()


class L01_V14_E04_TranspuestaDeLaSuma(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La transpuesta de una suma", "The transpose of a sum"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        # el ejemplo, solo con números (Marcos, 2026-11-20): A + B = S arriba, a la vista todo el ejemplo, y debajo
        # cada transpuesta bajo su matriz, A^T + B^T = S^T; al anunciar la demostración, la fila de abajo pasa a letras
        A4, B4, S4 = matriz(A_EJ, COLOR_A, escala=0.72), matriz(B_EJ, COLOR_B, escala=0.72), matriz(S_EJ, escala=0.72)
        mas4, igual4 = MathTex("+", font_size=40), MathTex("=", font_size=40)
        arriba = VGroup(A4, mas4, B4, igual4, S4).arrange(RIGHT, buff=0.4).move_to([0, 1.55, 0])
        At, Bt, St = (matriz(transpuesta(m), c, escala=0.72) for m, c in ((A_EJ, COLOR_A), (B_EJ, COLOR_B), (S_EJ, WHITE)))
        mas, igual = MathTex("+", font_size=40), MathTex("=", font_size=40)
        abajo = VGroup(At, mas, Bt, igual, St)
        for t, o in zip(abajo, arriba):
            t.move_to([o.get_x(), -1.35, 0])
        letras = MathTex(r"\MatT{A}", "+", r"\MatT{B}", "=", r"\Transp{\Mat{A}+\Mat{B}}", tex_template=myTemplate, font_size=44)
        for t, o in zip(letras, abajo):
            t.move_to([o.get_x(), -1.35, 0])
        
        panel = Panel(self, [(tr("Definición de transpuesta", "Definition of the transpose"), "def", DEF_TRANS),
                             (tr("Definición de suma de matrices", "Definition of matrix addition"), "suma", COLS_SUMA)],
                            [(tr("El selector de filas es lineal", "The row selector is linear"), "filas", FILAS_SUMA)])
        enunciado = MathTex(TRANS_SUMA, tex_template=myTemplate, font_size=44).move_to([0.6, 1.1, 0])
        # Glifos: ( ( A + B ) T ) | j (0-9);  = j | ( A + B ) (0-7);  = j | A + j | B (0-7);
        #         = ( A T ) | j + ( B T ) | j (0-13);  = ( A T + B T ) | j (0-9)
        cadena = coloca_cadena([linea(r"\elemRp{\Transp*{\Mat{A}+\Mat{B}}}{j}"),
                                linea(r"=\elemLp{\Mat{A}+\Mat{B}}{j}"),
                                linea(r"=\VectF{A}{j}+\VectF{B}{j}"),
                                linea(r"=\VectTC{A}{j}+\VectTC{B}{j}"),
                                linea(r"=\elemRp{\MatT{A}+\MatT{B}}{j}")], y_sup=0.1, salto=0.72, x_izq=-2.2)
        
        with self.voiceover(text=tr("""Tomemos de nuevo las dos matrices del ejemplo. <bookmark mark='t'/> Si las sumamos y transponemos la suma, <bookmark mark='f'/> sus filas pasan a ser columnas.""",
                                    """Let us take the two matrices of the example again. <bookmark mark='t'/> If we add them and transpose the sum, <bookmark mark='f'/> its rows become columns.""")) as tracker:
            self.play(Write(cabecera), FadeIn(A4), FadeIn(mas4), FadeIn(B4), run_time=1)
            self.wait_until_bookmark("t")
            self.play(FadeIn(igual4), FadeIn(S4), run_time=0.8)
            self.wait_until_bookmark("f")
            # la suma se transpone debajo de ella: su primera fila (recuadrada) pasa a ser la primera columna
            m_fila = marco(S4.get_rows()[0])
            self.play(Create(m_fila), run_time=0.4)
            self.play(TransformFromCopy(S4, St), ReplacementTransform(m_fila, marco(St.get_columns()[0])), run_time=1.2)
            self.wait(0.6)
            self.play(FadeOut(*[m for m in self.mobjects if isinstance(m, SurroundingRectangle)]), run_time=0.3)
        
        with self.voiceover(text=tr("""Y si transponemos primero cada matriz <bookmark mark='s'/> y sumamos después, obtenemos la misma matriz.""",
                                    """And if we first transpose each matrix <bookmark mark='s'/> and then add, we obtain the same matrix.""")) as tracker:
            marcos_f = [marco(A4.get_rows()[0]), marco(B4.get_rows()[0])]
            self.play(*[Create(m) for m in marcos_f], run_time=0.4)
            self.play(TransformFromCopy(A4, At), TransformFromCopy(B4, Bt),
                      ReplacementTransform(marcos_f[0], marco(At.get_columns()[0])),
                      ReplacementTransform(marcos_f[1], marco(Bt.get_columns()[0])), run_time=1.2)
            self.play(FadeOut(*[m for m in self.mobjects if isinstance(m, SurroundingRectangle)]), run_time=0.3)
            self.wait_until_bookmark("s")
            self.play(FadeIn(mas), run_time=0.4)
            self.play(FadeIn(igual), Indicate(St, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.2)
        
        self.pausa_corta()
        
        with self.voiceover(text=tr("""Este ejemplo solo lo ilustra. <bookmark mark='v'/> Vamos a demostrar que siempre da igual <bookmark mark='e1'/> sumar primero y <bookmark mark='e2'/> transponer después, que <bookmark mark='e3'/> transponer primero y <bookmark mark='e4'/> sumar después.""",
                                    """This example only illustrates it. <bookmark mark='v'/> We are going to prove that it always makes no difference whether we <bookmark mark='e1'/> add first and <bookmark mark='e2'/> transpose afterwards, or <bookmark mark='e3'/> transpose first and <bookmark mark='e4'/> add afterwards.""")) as tracker:
            # transición a letras: cada matriz de la fila de abajo se funde con su nombre (fundido cruzado: FadeTransform
            # agrandaba las letras al tamaño de las matrices) y, tras reposar un segundo, la fila pasa a ser el enunciado
            self.play(FadeOut(arriba), *[FadeOut(n) for n in abajo], *[FadeIn(l) for l in letras], run_time=1.0)
            self.wait_until_bookmark("v")
            # cada trozo viaja a su lado del enunciado: (A+B)^T a la izquierda, A^T + B^T a la derecha
            e = enunciado[0]
            destinos = [VGroup(*e[7:9]), e[9], VGroup(*e[10:12]), e[6], VGroup(*e[0:6])]
            llegadas = [d.copy() for d in destinos]
            self.play(*[ReplacementTransform(l, d, path_arc=PI/2) for l, d in zip(letras, llegadas)], run_time=1.4)   # los lados se cruzan por arriba y por abajo
            self.remove(*llegadas); self.add(enunciado)
            # la cantinela sobre el enunciado: la suma y la transposición, cada una en su verbo
            cantinela(self, [("e1", [e[2]], COLOR_ESCALAR), ("e2", [e[5]], COLOR_TRANSP),
                             ("e3", [e[8], e[11]], COLOR_TRANSP), ("e4", [e[9]], COLOR_ESCALAR)])
        
        with self.voiceover(text=tr("""Para demostrarlo necesitará <bookmark mark='p'/> la definición de transpuesta, <bookmark mark='q'/> que el selector de filas es lineal, <bookmark mark='r'/> y la definición de suma de matrices.""",
                                    """To prove it you will need <bookmark mark='p'/> the definition of the transpose, <bookmark mark='q'/> the fact that the row selector is linear, <bookmark mark='r'/> and the definition of matrix addition.""")) as tracker:
            self.play(FadeIn(panel.todo), run_time=0.6)   # el panel aparece cuando la voz lo nombra (auditoría 2026-11-21)
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
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Como el selector de filas es lineal, <bookmark mark='x'/> podemos distribuirlo entre los sumandos.""",
                                    """Since the row selector is linear, <bookmark mark='x'/> we can distribute it over the terms.""")) as tracker:
            paso(self, panel, "filas", cadena[1], cadena[2], [(4, 3), (5, 4), (6, 7)], [(1, 1), (2, 2), (1, 5), (2, 6)], marca="x")
        self.wait(0.5)
        
        with self.voiceover(text=tr("""De nuevo por la definición de transpuesta, <bookmark mark='x'/> cada fila es una columna de la transpuesta, y el índice vuelve a la derecha.""",
                                    """Again by the definition of the transpose, <bookmark mark='x'/> each row is a column of the transpose, and the index goes back to the right.""")) as tracker:
            paso(self, panel, "def", cadena[2], cadena[3], [(3, 2), (4, 7), (7, 9)], [(1, 6), (2, 5), (5, 13), (6, 12)],
                 aparecen=[1, 3, 4, 8, 10, 11], marca="x")
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Y por la definición de suma de matrices <bookmark mark='x'/> podemos sacar el selector como factor común.""",
                                    """And by the definition of matrix addition <bookmark mark='x'/> we can factor out the selector.""")) as tracker:
            paso(self, panel, "suma", cadena[3], cadena[4], [(2, 2), (3, 3), (7, 4), (9, 5), (10, 6)],
                 [(5, 8), (6, 9), (12, 8), (13, 9), (1, 1), (11, 7)], marca="x")
            panel.suelta()
        
        self.wait(0.5)
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> las dos matrices son iguales, porque lo son <bookmark mark='c'/> columna a columna.""",
                                    """So <bookmark mark='ok'/> the two matrices are equal, because they are equal <bookmark mark='c'/> column by column.""")) as tracker:
            self.wait_until_bookmark("ok")
            recuadra(self, enunciado)
            self.wait_until_bookmark("c")
            indices = [cadena[0][0][9], cadena[4][0][9]]   # el índice de la columna, a los dos extremos
            self.play(*[x.animate.set_color(COLOR_COLUMNA).scale(1.5) for x in indices], run_time=0.3)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in indices], run_time=0.3)
        
        self.pausa_media()


class L01_V14_E05_TranspuestaDelProducto(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La transpuesta de un producto por un escalar", "The transpose of a product by a scalar"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self, [(tr("Definición de transpuesta", "Definition of the transpose"), "def", DEF_TRANS),
                             (tr("Definición de producto por un escalar", "Definition of the product by a scalar"), "prod", COLS_PROD)],
                            [(tr("El selector de filas es lineal", "The row selector is linear"), "filas", FILAS_PROD)])
        enunciado = MathTex(TRANS_PROD, tex_template=myTemplate, font_size=44).move_to([0.6, 1.1, 0])
        # Glifos: ( ( λ A ) T ) | j (0-8);  = j | ( λ A ) (0-6);  = λ ( j | A ) (0-6);
        #         = λ ( ( A T ) | j ) (0-9);  = ( λ ( A T ) ) | j (0-9)
        cadena = coloca_cadena([linea(r"\elemRp{\Transp*{\lambda\Mat{A}}}{j}"),
                                linea(r"=\elemLp{\lambda\Mat{A}}{j}"),
                                linea(r"=\lambda\VectFpE{A}{j}"),
                                linea(r"=\lambda\VectTCpE{A}{j}"),
                                linea(r"=\elemRp{\lambda\MatTpE{A}}{j}")], y_sup=0.2, salto=0.66, x_izq=-1.8)
        idea = aviso("idea", tr("La transposición es un operador lineal", "Transposition is a linear operator"), font_size=32).to_edge(DOWN, buff=0.15)
        # las dos reglas demostradas, juntas, para la frase que cierra la escena. Glifos: ( A + B ) T = A T + B T (0-11);
        # ( λ A ) T = λ ( A T ) (0-10)
        regla_suma, regla_prod = [MathTex(f, tex_template=myTemplate, font_size=52) for f in (TRANS_SUMA, TRANS_PROD)]
        VGroup(regla_suma, regla_prod).arrange(DOWN, buff=1.0).move_to([0, 0.5, 0])
        de_fondo = list(self.mobjects)   # lo que no es de la escena (la firma del margen)
        
        with self.voiceover(text=tr("""Con el producto por un escalar ocurre lo mismo: <bookmark mark='e'/> da igual <bookmark mark='e1'/> multiplicar primero y <bookmark mark='e2'/> transponer después, <bookmark mark='d'/> que <bookmark mark='e3'/> transponer primero y <bookmark mark='e4'/> multiplicar después.""",
                                    """The same happens with scalar multiplication: <bookmark mark='e'/> it makes no difference whether we <bookmark mark='e1'/> multiply first and <bookmark mark='e2'/> transpose afterwards, <bookmark mark='d'/> or <bookmark mark='e3'/> transpose first and <bookmark mark='e4'/> multiply afterwards.""")) as tracker:
            self.play(Write(cabecera), FadeIn(panel.todo), run_time=1)
            # cada lado del enunciado se escribe en su frase, y en cada verbo se señala el escalar o la transposición
            e = enunciado[0]
            self.wait_until_bookmark("e")
            self.play(Write(VGroup(*e[0:5])), run_time=0.5)
            cantinela(self, [("e1", [e[1]], COLOR_ESCALAR), ("e2", [e[4]], COLOR_TRANSP)])
            self.wait_until_bookmark("d")
            self.play(Write(VGroup(*e[5:11])), run_time=0.5)
            cantinela(self, [("e3", [e[9]], COLOR_TRANSP), ("e4", [e[6]], COLOR_ESCALAR)])
        
        self.pausa_para_pensar(invitacion=tr("Demuéstrelo con los mismos pasos.", "Prove it with the same steps."),
                               invitacion_voz=tr("Pause el vídeo e intente demostrarlo con los mismos pasos que en la suma.",
                                                 "Pause the video and try to prove it with the same steps as for the sum."))
        
        with self.voiceover(text=tr("""Los pasos son los mismos. <bookmark mark='l0'/> Seleccionamos una columna cualquiera <bookmark mark='l1'/> y quitamos la transposición cambiando de lado el índice.""",
                                    """The steps are the same. <bookmark mark='l0'/> We select any column <bookmark mark='l1'/> and remove the transposition by moving the index to the other side.""")) as tracker:
            # «una columna cualquiera», como en las escenas 2 y 4 (Marcos, 2026-11-21): la locución se partió tras «...el índice.»
            # (toma nueva de la primera parte; la segunda conserva la suya) y entre las dos va la pausa que tenía la toma entera
            rapido = dict(t_fijos=0.5, t_moviles=0.6, t_cuenta=0.35)
            self.wait_until_bookmark("l0")
            self.play(TransformFromCopy(enunciado[0][0:5], cadena[0][0][1:6]), FadeIn(cadena[0][0][0]), FadeIn(cadena[0][0][6:]), run_time=0.8)
            entera(self, cadena[0])
            self.wait_until_bookmark("l1")   # el selector cruza a la izquierda; la T y los paréntesis de fuera no aparecen
            paso(self, panel, "def", cadena[0], cadena[1], [(1, 3), (2, 4), (3, 5), (4, 6)], [(7, 2), (8, 1)], **rapido)
        
        self.wait(0.45)
        with self.voiceover(text=tr("""Como el selector de filas es lineal, <bookmark mark='m2'/> podemos sacar el escalar. <bookmark mark='l3'/> La fila es una columna de la transpuesta. <bookmark mark='l4'/> Y por la definición de producto por un escalar <bookmark mark='m4'/> podemos desplazar los paréntesis.""",
                                    """Since the row selector is linear, <bookmark mark='m2'/> we can take the scalar out. <bookmark mark='l3'/> The row is a column of the transpose. <bookmark mark='l4'/> And by the definition of the product by a scalar <bookmark mark='m4'/> we can move the parentheses.""")) as tracker:
            # primero baja «( A )»; en «sacar el escalar» el escalar sale delante y el selector entra
            # en los paréntesis (Marcos, 2026-11-20: antes viajaban los paréntesis, que no son lo que el paso mueve). «( A )»
            # baja atenuado y sin el igual, para que no se lea «= ( A )» mientras la voz dice el preámbulo (2026-11-21)
            paso(self, panel, "filas", cadena[1], cadena[2], [(3, 2), (5, 5), (6, 6)], [(4, 1), (1, 3), (2, 4)], marca="m2", tenue=True, **rapido)
            self.wait_until_bookmark("l3")   # el índice vuelve a la derecha, con la T y sus paréntesis
            paso(self, panel, "def", cadena[2], cadena[3], [(1, 1), (2, 2), (6, 9), (5, 4)], [(3, 8), (4, 7)], aparecen=[3, 5, 6], **rapido)
            self.wait_until_bookmark("l4")   # los paréntesis pasan a rodear el producto y dejan fuera el selector
            paso(self, panel, "prod", cadena[3], cadena[4], [(1, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 8), (8, 9)], [(2, 1), (9, 7)], marca="m4", **rapido)
            panel.suelta()
        
        self.wait(0.4)
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> las dos matrices son iguales, porque lo son <bookmark mark='c'/> columna a columna.""",
                                    """So <bookmark mark='ok'/> the two matrices are equal, because they are equal <bookmark mark='c'/> column by column.""")) as tracker:
            self.wait_until_bookmark("ok")
            recuadra(self, enunciado)
            self.wait_until_bookmark("c")
            indices = [cadena[0][0][-1], cadena[4][0][-1]]   # el índice de la columna, a los dos extremos
            self.play(*[x.animate.set_color(COLOR_COLUMNA).scale(1.5) for x in indices], run_time=0.3)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in indices], run_time=0.3)
        
        self.wait(0.8)
        
        # El cierre nombra las dos reglas, así que el espectador las tiene delante (Marcos, 2026-11-21): la demostración se
        # retira y quedan la regla de la suma (escena 4) y la del producto, cada una señalada en su frase: la transposición
        # (morado) y la operación (amarillo). Marcas s y p injertadas en la toma que ya había.
        self.play(FadeOut(*[m for m in self.mobjects if m not in de_fondo]), run_time=0.6)
        with self.voiceover(text=tr("""La transposición <bookmark mark='s'/> se distribuye en las sumas y <bookmark mark='p'/> es asociativa con el producto por un escalar: <bookmark mark='i'/> también es un operador lineal.""",
                                    """Transposition <bookmark mark='s'/> distributes over sums and <bookmark mark='p'/> is associative with scalar multiplication: <bookmark mark='i'/> it is a linear operator too.""")) as tracker:
            rs, rp = regla_suma[0], regla_prod[0]
            de_suma = [(rs[5], COLOR_TRANSP), (rs[8], COLOR_TRANSP), (rs[11], COLOR_TRANSP), (rs[2], COLOR_ESCALAR), (rs[9], COLOR_ESCALAR)]
            de_prod = [(rp[4], COLOR_TRANSP), (rp[9], COLOR_TRANSP), (rp[1], COLOR_ESCALAR), (rp[6], COLOR_ESCALAR)]
            self.play(FadeIn(regla_suma), run_time=0.5)
            self.wait_until_bookmark("s")
            self.play(*[g.animate.set_color(c).scale(1.3) for g, c in de_suma], run_time=0.25)
            self.wait_until_bookmark("p")
            self.play(*[g.animate.set_color(WHITE).scale(1/1.3) for g, c in de_suma], FadeIn(regla_prod), run_time=0.3)
            self.play(*[g.animate.set_color(c).scale(1.3) for g, c in de_prod], run_time=0.25)
            self.wait_until_bookmark("i")
            self.play(*[g.animate.set_color(WHITE).scale(1/1.3) for g, c in de_prod], FadeIn(idea, scale=0.9), run_time=0.8)
        
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
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=40), Tex(r, font_size=34, color=GRAY_A)).arrange(DOWN, buff=0.25)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.9).move_to([0, -0.2, 0])
        
        with self.voiceover(text=tr("""Resumamos. Las matrices también se suman y se multiplican por un escalar fila a fila: el selector de filas es lineal, como el de columnas. <bookmark mark='t'/> La transposición también es lineal.""",
                                    """Let us sum up. Matrices are also added and multiplied by a scalar row by row: the row selector is linear, like the column selector. <bookmark mark='t'/> Transposition is linear too.""")) as tracker:
            # la descripción de las dos reglas se quitó (Marcos, 2026-11-21): la escena 5 ya las enseña juntas al cerrar; la
            # toma es la que había, cortada tras «...también es lineal.»
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("t")
            self.play(FadeIn(filas[1]), run_time=0.8)
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos una última extensión de la notación: escribir a la derecha el escalar de un producto.""",
                                    """In the next video we will see one last extension of the notation: writing the scalar of a product on the right.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
