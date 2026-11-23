from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Suma de matrices y producto por escalares", "Matrix addition and scalar multiplication")

A_EJ      = [[1, 1, 9], [2, 0, 2]]       # las dos matrices de orden 2 por 3 del ejemplo del libro (Sección 1.5)
B_EJ      = [[1, 2, 3], [0, -1, 7]]
S_EJ      = [[2, 3, 12], [2, -1, 9]]     # A + B
DOSB_EJ   = [[2, 4, 6], [0, -2, 14]]     # 2B
MENOSB_EJ = [[-1, -2, -3], [0, 1, -7]]   # -B
COLOR_COLUMNA = GREEN                    # las columnas, en verde (como en V10)
CAMPANITA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos", "campanita.wav")   # suena al subir un contador

PROPIEDADES_REALES = [r"a+b=b+a", r"a+(b+c)=(a+b)+c", r"a+0=a", r"a+(-a)=0",
                      r"ab=ba", r"a(b+c)=ab+ac", r"a(bc)=(ab)c", r"1a=a"]

PROPIEDADES_VECTORES = [r"\Vect{a}+\Vect{b}=\Vect{b}+\Vect{a}",
                        r"\Vect{a}+(\Vect{b}+\Vect{c})=(\Vect{a}+\Vect{b})+\Vect{c}",
                        r"\Vect{a}+\Vect{0}=\Vect{a}",
                        r"\Vect{a}+(-\Vect{a})=\Vect{0}",
                        r"\lambda(\Vect{a}+\Vect{b})=\lambda\Vect{a}+\lambda\Vect{b}",
                        r"(\lambda+\varphi)\Vect{a}=\lambda\Vect{a}+\varphi\Vect{a}",
                        r"\lambda(\varphi\Vect{a})=(\lambda\varphi)\Vect{a}",
                        r"1\Vect{a}=\Vect{a}"]

# Las cuatro definiciones de los vectores: (clave, lado izquierdo, lado derecho, lado derecho final).
# El lado derecho final solo se da cuando el cambio de símbolos no basta: el número cero pasa a vector nulo.
DEFINICIONES = [("suma",     r"\elemRp{\Vect{a}+\Vect{b}}{i}", r"\eleVR{a}{i}+\eleVR{b}{i}", None),
                ("producto", r"\elemRp{\lambda\Vect{a}}{i}",   r"\lambda\eleVRpE{a}{i}",     None),
                ("nulo",     r"\eleVR{0}{i}",                  r"0",                         r"\Vect{0}"),
                ("opuesto",  r"\elemRp{-\Vect{a}}{i}",         r"-\eleVRpE{a}{i}",           None)]


def a_matrices(s):
    """El cambio de símbolos del vídeo: cada vector pasa a ser la matriz de la misma letra en mayúscula."""
    s = re.sub(r"\\eleVRpE\{(\w)\}", lambda m: r"\VectCpE{" + m.group(1).upper() + "}", s)
    s = re.sub(r"\\eleVR\{(\w)\}",   lambda m: r"\VectC{" + m.group(1).upper() + "}", s)
    s = re.sub(r"\\Vect\{(\w)\}",    lambda m: r"\Mat{" + m.group(1).upper() + "}", s)
    return s


def a_columnas(s):
    return s.replace("{i}", "{j}")


def versiones(s, final=None):
    """Las cuatro versiones de una fórmula escrita para vectores: [vectores, matrices, matrices con j, final]."""
    s2 = a_columnas(a_matrices(s))
    return [s, a_matrices(s), s2, final or s2]


def definicion_matrices(clave):
    """(lado izquierdo, lado derecho) de la definición para matrices."""
    _, izq, der, fin = next(d for d in DEFINICIONES if d[0] == clave)
    return a_columnas(a_matrices(izq)), fin or a_columnas(a_matrices(der))


DEF_MAT = {clave: "=".join(definicion_matrices(clave)) for clave, *_ in DEFINICIONES}
PROPIEDADES_MATRICES = [a_matrices(p) for p in PROPIEDADES_VECTORES]


def traducible(vers, font_size=36, color=WHITE):
    """Fórmula en su primera versión; en .etapas guarda las demás (se colocan con coloca_etapas).
    Cada versión es una cadena o una tupla de cadenas (las partes de MathTex)."""
    partes = [v if isinstance(v, (tuple, list)) else (v,) for v in vers]
    ms = [MathTex(*p, tex_template=myTemplate, font_size=font_size).set_color(color) for p in partes]
    for m in ms[1:]:   # mismo número de glifos en todas las versiones: cada glifo tiene su pareja
        assert [len(x) for x in m] == [len(x) for x in ms[0]], (partes[0], [len(x) for x in m], [len(x) for x in ms[0]])
    m = ms[0]
    m.versiones, m.etapas, m.color_base = partes, ms, color
    return m


def coloca_etapas(m, alinea=LEFT):
    """Las versiones siguientes, en el sitio de la primera (alineadas por la izquierda, o centradas)."""
    for t in m.etapas[1:]:
        t.scale(m.height/m.etapas[0].height if m is not m.etapas[0] else 1)
        t.move_to(m)
        if alinea is not None:
            t.align_to(m, alinea)
    return m


def etapa(k, mobs):
    """Animaciones del cambio de símbolos número k (solo las fórmulas que cambian en esa etapa)."""
    return [Transform(m, m.etapas[k]) for m in mobs if m.versiones[k] != m.versiones[k-1]]


def matriz(filas, color=WHITE, escala=0.8, h_buff=1.0):
    m = IntegerMatrix(filas, v_buff=0.62, h_buff=h_buff)
    m.get_entries().set_color(color)
    return m.scale(escala)


def columnas(filas):
    return [list(c) for c in zip(*filas)]


def vec(col):
    """Un vector numérico, en vertical y entre paréntesis."""
    return r"\begin{pmatrix}" + r"\\".join(str(x) for x in col) + r"\end{pmatrix}"


def marco(mob, color=COLOR_COLUMNA):
    return SurroundingRectangle(mob, color=color, buff=0.12, corner_radius=0.1, stroke_width=3)


def resalta(escena, mobs, color=COLOR_ESCALAR, factor=1.3, run_time=0.3):
    """Resaltado inmediato y sostenido (color y tamaño), sin la subida lenta de Indicate."""
    escena.play(*[x.animate.set_color(color).scale(factor) for x in mobs], run_time=run_time)


def apaga(escena, mobs, color=WHITE, factor=1.3, run_time=0.3):
    escena.play(*[x.animate.set_color(color).scale(1/factor) for x in mobs], run_time=run_time)


def ilumina(escena, nueva=None, anterior=None, run_time=0.25):
    """Señala una línea de la cadena mientras la voz la lee (amarillo y algo mayor); la anterior vuelve a su color."""
    anims = []
    if nueva is not None:
        anims.append(nueva.animate.set_color(COLOR_ESCALAR).scale(1.08, about_edge=LEFT))
    if anterior is not None:
        anims.append(anterior.animate.set_color(anterior.color_base).scale(1/1.08, about_edge=LEFT))
    escena.play(*anims, run_time=run_time)


class Panel:
    """Panel de herramientas de V06: definiciones a la izquierda y las cuatro propiedades de la suma de
    números reales a la derecha. Todas sus piezas son traducibles: con el cambio de símbolos las
    definiciones pasan a ser las de las matrices y las propiedades, las de los vectores."""
    def __init__(self, escena, y_sup=2.95, font_size=28):
        self.escena, self.piezas, self.usos, self.contadores = escena, {}, {}, {}
        izq = VGroup(*[traducible(versiones(i + "=" + d, a_columnas(a_matrices(i)) + "=" + f if f else None), font_size)
                       for _, i, d, f in DEFINICIONES]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for (clave, *_), m in zip(DEFINICIONES, izq):
            self.piezas[clave] = m
        der = VGroup(*[traducible([(f"{k+1}.\\;", PROPIEDADES_REALES[k])]*3 + [(f"{k+1}.\\;", PROPIEDADES_VECTORES[k])], font_size)
                       for k in range(4)]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for k, m in enumerate(der):
            self.piezas[k+1] = m
        cab_izq = Tex(tr("Definiciones", "Definitions"), font_size=24).set_color(GRAY_B)
        self.cab_der = Tex(tr("Números reales", "Real numbers"), font_size=24).set_color(GRAY_B)
        self.izq = VGroup(cab_izq, izq).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=0.35)
        self.der = VGroup(self.cab_der, der).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=1.0)
        for g in (self.izq, self.der):
            g.align_to([0, y_sup, 0], UP)
        self.cab_der_fin = Tex(tr("Vectores", "Vectors"), font_size=24).set_color(GRAY_B).move_to(self.cab_der).align_to(self.cab_der, LEFT)
        self.traducibles = [*izq, *der]
        for m in self.traducibles:
            coloca_etapas(m)
        self.todo = VGroup(self.izq, self.der)

    def senala(self, clave):
        return Indicate(self.piezas[clave], color=COLOR_RESULTADO, scale_factor=1.12)

    def cuenta(self, clave, run_time=0.5):
        """Después del paso: sube el contador de usos de la pieza, con la campanita (insignia de V06). La insignia
        se coloca a la derecha de la versión más ancha de la pieza, para que el cambio de símbolos no la pise."""
        pieza = self.piezas[clave]
        self.usos[clave] = self.usos.get(clave, 0) + 1
        disco = Circle(radius=0.17, fill_color=COLOR_TITULO, fill_opacity=1, stroke_width=0)
        numero = Tex(f"\\textbf{{{self.usos[clave]}}}", font_size=24).set_color(WHITE).move_to(disco)
        x = max(t.get_right()[0] for t in pieza.etapas)
        nuevo = VGroup(disco, numero).move_to([x + 0.3 + 0.17, pieza.get_y() + 0.1, 0])
        self.escena.add_sound(CAMPANITA)
        if clave in self.contadores:
            self.escena.play(ReplacementTransform(self.contadores[clave], nuevo), run_time=run_time)
        else:
            self.escena.play(FadeIn(nuevo, scale=0.5), run_time=run_time)
        self.contadores[clave] = nuevo

    def reinicia(self, run_time=0.6):
        """Los contadores vuelven a cero (desaparecen): la demostración se va a contar otra vez, ya para matrices."""
        self.escena.play(*[FadeOut(c) for c in self.contadores.values()], run_time=run_time)
        self.usos, self.contadores = {}, {}


def linea(formula, de_abajo=False, final=None):
    """Una línea de la cadena, traducible. En teal los pasos que usan una propiedad del nivel de abajo
    (de los números en la demostración para vectores; de los vectores en la de las matrices)."""
    return traducible(versiones(formula, final), 36, COLOR_REGLA if de_abajo else WHITE)


def coloca_cadena(cadena, y_sup=0.55, salto=0.66, x_izq=-3.3, sangria=0.6):
    """Como en V06: la primera línea en x_izq y las siguientes (que empiezan por '=') sangradas."""
    for k, l in enumerate(cadena):
        l.move_to([0, y_sup - k*salto, 0]).align_to([x_izq + (sangria if k else 0), 0, 0], LEFT)
        coloca_etapas(l)
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
    lo que no cambia, la línea se completa y entonces sube el contador con la campanita."""
    nace(escena, origen[0], destino[0], fijos, moviles, aparecen, extra=[panel.senala(clave)], marca=marca,
         t_fijos=t_fijos, t_moviles=t_moviles)
    entera(escena, destino)
    panel.cuenta(clave, run_time=t_cuenta)


def relee(escena, panel, clave, nueva, anterior=None, run_time=0.8):
    """Relectura de un paso ya traducido: la línea se ilumina, la pieza parpadea y su contador vuelve a subir."""
    ilumina(escena, nueva, anterior)
    escena.play(panel.senala(clave), run_time=run_time)
    panel.cuenta(clave)


def senala_selector(escena, lineas, color=COLOR_COLUMNA, factor=1.8, espera=1.6):
    """«Componente a componente», «columna a columna»: el selector de los dos extremos de la cadena (la barra y el
    índice, sus dos últimos glifos) crece y cambia de color mientras la voz lo dice (auditoría 2026-11-21: el índice
    solo, 1,5 veces, casi no se veía)."""
    sels = [l[0][-2:] for l in lineas]
    escena.play(*[x.animate.set_color(color).scale(factor, about_edge=LEFT) for x in sels], run_time=0.3)
    escena.wait(espera)
    escena.play(*[x.animate.set_color(WHITE).scale(1/factor, about_edge=LEFT) for x in sels], run_time=0.3)


def enunciado_traducible(numero):
    """El enunciado de la propiedad, en el hueco entre los dos lados del panel (como en V06)."""
    e = traducible(versiones(PROPIEDADES_VECTORES[numero-1]), 40)
    for t in e.etapas:
        t.move_to([-0.3, 2.2, 0])
    return e


def cambio_de_simbolos(k, panel, enunciado, cadena):
    """Todas las animaciones de la etapa k del cambio de símbolos (panel, enunciado y cadena)."""
    anims = etapa(k, [*panel.traducibles, enunciado, *cadena])
    if k == 3:
        anims.append(Transform(panel.cab_der, panel.cab_der_fin))
    return anims

class L01_V13_OperacionesConMatrices(MiEscenaConVoz):
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
        VGroup(A, mas, B, igual, S).arrange(RIGHT, buff=0.3).move_to([0, 1.25, 0])
        nombres = VGroup(*[MathTex(t, tex_template=myTemplate, font_size=40).next_to(m, DOWN, buff=0.25)
                           for t, m in ((r"\Mat{A}", A), (r"\Mat{B}", B), (r"\Mat{A}+\Mat{B}", S))])
        nombres[0].set_color(COLOR_A); nombres[1].set_color(COLOR_B)
        sumas = [MathTex(vec(a), "+", vec(b), "=", vec(s), tex_template=myTemplate, font_size=44).move_to([0, -1.15, 0])
                 for a, b, s in zip(columnas(A_EJ), columnas(B_EJ), columnas(S_EJ))]
        for s in sumas:
            s[0].set_color(COLOR_A); s[2].set_color(COLOR_B)
        def_suma = MathTex(DEF_MAT["suma"], tex_template=myTemplate, font_size=52).move_to([0, -2.75, 0])
        selectores = [def_suma[0][5:7], def_suma[0][9:11], def_suma[0][13:15]]   # los tres «|j»
        
        with self.voiceover(text=tr("""En este vídeo veremos la suma de matrices y el producto de una matriz por un escalar. Y descubriremos que sus propiedades ya están demostradas.""",
                                    """In this video we will look at the addition of matrices and the multiplication of a matrix by a scalar. And we will find that their properties have already been proved.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        self.wait(1.0)   # respiro tras el arranque (auditoría 2026-11-21)
        
        with self.voiceover(text=tr("""Las columnas de una matriz <bookmark mark='k'/> son vectores, <break time="200ms"/> que ya sabemos sumar. Por eso definimos la suma de <bookmark mark='m'/> dos matrices del mismo orden columna a columna.""",
                                    """The columns of a matrix <bookmark mark='k'/> are vectors, and we already know how to add vectors. That is why we define the sum of <bookmark mark='m'/> two matrices of the same order column by column.""")) as tracker:
            # las dos matrices del ejemplo se ven desde que la voz habla de columnas; el signo de sumar, al decir «sumar»
            self.play(FadeIn(A), FadeIn(B), FadeIn(nombres[0]), FadeIn(nombres[1]), run_time=1)
            self.wait_until_bookmark("k")   # una columna enmarcada, la misma que después (auditoría 2026-11-19)
            col_k = marco(A.get_columns()[0])
            self.play(Create(col_k), run_time=0.4)
            self.wait(0.8)
            self.play(FadeOut(col_k), run_time=0.3)
            self.wait_until_bookmark("m")
            self.play(FadeIn(mas), run_time=0.6)
        
        # el propósito, dicho (Marcos, 2026-11-21: el «por eso» lo dejaba implícito); locución aparte para conservar la toma
        # anterior. Las columnas de las dos matrices se enmarcan mientras la voz lo dice: son los vectores que se aprovechan
        with self.voiceover(text=tr("""Así aprovechamos todo lo que ya hemos aprendido sobre los vectores.""",
                                    """This way we reuse everything we have learned about vectors.""")) as tracker:
            cols = VGroup(*[marco(c) for M in (A, B) for c in M.get_columns()])
            self.play(Create(cols, lag_ratio=0.15), run_time=1.2)
            self.wait(max(tracker.duration - 1.6, 0.1))
            self.play(FadeOut(cols), run_time=0.4)
        
        self.wait(0.6)
        
        with self.voiceover(text=tr("""La primera columna de la suma es la suma de las primeras columnas, <bookmark mark='c2'/> la segunda es la suma de las segundas, <bookmark mark='c3'/> y la tercera, la suma de las terceras.""",
                                    """The first column of the sum is the sum of the first columns, <bookmark mark='c2'/> the second is the sum of the second columns, <bookmark mark='c3'/> and the third, the sum of the third columns.""")) as tracker:
            self.play(FadeIn(igual), FadeIn(S.get_brackets()), FadeIn(nombres[2]), run_time=0.6)
            # sin «En este ejemplo» (Marcos, 2026-11-20: sonaba a que en otro ejemplo podría no ser así); la toma es la
            # nueva (el recorte se notaba) y la primera columna se señala al empezar la frase
            for k, marca in enumerate([None, "c2", "c3"]):
                if marca:
                    self.wait_until_bookmark(marca)
                nuevos = VGroup(marco(A.get_columns()[k]), marco(B.get_columns()[k]))
                if k == 0:
                    marcos = nuevos
                    self.play(Create(marcos), FadeIn(sumas[0]), run_time=0.6)
                else:
                    self.play(Transform(marcos, nuevos), FadeOut(sumas[k-1]), FadeIn(sumas[k]), run_time=0.6)
                self.play(FadeIn(S.get_columns()[k]), run_time=0.5)
        
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Esta es la definición de suma de matrices: <bookmark mark='d'/> cada columna de la suma es la suma de <bookmark mark='c'/> las columnas correspondientes. Con nuestra notación, <bookmark mark='s'/> el selector de columnas <bookmark mark='v'/> se distribuye entre los sumandos.""",
                                    """This is the definition of matrix addition: <bookmark mark='d'/> each column of the sum is the sum of <bookmark mark='c'/> the corresponding columns. In our notation, <bookmark mark='s'/> the column selector <bookmark mark='v'/> distributes over the terms.""")) as tracker:
            # la definición se escribe con «Esta es» (Marcos, 2026-11-20: si no, la voz señala algo que no está)
            self.play(FadeOut(marcos), Write(def_suma), run_time=1.2)
            # cada pieza se señala cuando la voz la nombra, como en la definición del producto (Marcos, 2026-11-21): la columna
            # de la suma (lado izquierdo) y las columnas de los sumandos. glifos: ( A + B ) | j (0-6)  =  A | j (8-10)  +  B | j (12-14)
            col_suma, cols = def_suma[0][0:7], [def_suma[0][8:11], def_suma[0][12:15]]
            self.wait_until_bookmark("d")
            resalta(self, [col_suma], color=COLOR_COLUMNA, factor=1.12)
            self.wait_until_bookmark("c")
            self.play(col_suma.animate.set_color(WHITE).scale(1/1.12), *[x.animate.set_color(COLOR_COLUMNA).scale(1.15) for x in cols], run_time=0.25)
            self.wait(1.3)
            apaga(self, cols, factor=1.15, run_time=0.25)
            # «el selector de columnas»: el |j de la izquierda; «se distribuye»: dos copias suyas viajan a los dos sumandos
            # (Marcos, 2026-11-18); los |j de la derecha se atenúan un instante para que se vea llegar cada copia
            self.wait_until_bookmark("s")
            resalta(self, selectores[:1], color=COLOR_COLUMNA, factor=1.25)
            self.wait_until_bookmark("v")
            llegadas = [x.copy().set_color(COLOR_COLUMNA).scale(1.25) for x in selectores[1:]]
            self.play(*[x.animate.set_opacity(0.15) for x in selectores[1:]], run_time=0.25)
            self.play(*[TransformFromCopy(selectores[0], y) for y in llegadas], run_time=1.0)
            self.remove(*llegadas)
            for x in selectores[1:]:
                x.set_opacity(1).set_color(COLOR_COLUMNA).scale(1.25)
            self.wait(1.2)
            apaga(self, selectores, factor=1.25)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Producto de una matriz por un escalar", "Product of a matrix by a scalar"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        dos = MathTex("2", font_size=56).set_color(COLOR_ESCALAR)
        B, P = matriz(B_EJ, COLOR_B), matriz(DOSB_EJ)
        igual = MathTex("=", font_size=48)
        VGroup(dos, B, igual, P).arrange(RIGHT, buff=0.3).move_to([0, 1.25, 0])
        nombres = VGroup(*[MathTex(t, tex_template=myTemplate, font_size=40).next_to(m, DOWN, buff=0.25)
                           for t, m in ((r"\Mat{B}", B), (r"2\Mat{B}", P))])
        nombres[0].set_color(COLOR_B)
        prods = [MathTex("2", vec(b), "=", vec(p), tex_template=myTemplate, font_size=44).move_to([0, -1.15, 0])
                 for b, p in zip(columnas(B_EJ), columnas(DOSB_EJ))]
        for p in prods:
            p[0].set_color(COLOR_ESCALAR); p[1].set_color(COLOR_B)
        def_prod = MathTex(DEF_MAT["producto"], tex_template=myTemplate, font_size=52).move_to([0, -2.75, 0])
        parentesis = [def_prod[0][0], def_prod[0][3], def_prod[0][8], def_prod[0][12]]
        
        with self.voiceover(text=tr("""Con el producto por un escalar hacemos lo mismo: para multiplicar una matriz por un número, multiplicamos <bookmark mark='c0'/> cada una de sus columnas por ese número.""",
                                    """With scalar multiplication we do the same: to multiply a matrix by a number, we multiply <bookmark mark='c0'/> each of its columns by that number.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.play(FadeIn(dos), FadeIn(B), FadeIn(nombres[0]), run_time=1)
            self.wait_until_bookmark("c0")
            marcos = marco(B.get_columns()[0])
            self.play(Create(marcos), run_time=0.4)
        
        with self.voiceover(text=tr("""Cada columna del resultado es el doble de la columna correspondiente de la matriz.""",
                                    """Each column of the result is twice the corresponding column of the matrix.""")) as tracker:
            self.play(FadeIn(igual), FadeIn(P.get_brackets()), FadeIn(nombres[1]), run_time=0.6)
            for k in range(3):   # unos 1,5 s por columna (auditoría 2026-11-19)
                if k == 0:
                    self.play(FadeIn(prods[0]), run_time=0.5)
                else:
                    self.play(Transform(marcos, marco(B.get_columns()[k])), FadeOut(prods[k-1]), FadeIn(prods[k]), run_time=0.5)
                self.play(FadeIn(P.get_columns()[k]), run_time=0.4)
                self.wait(0.9)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Esta es la definición de producto de una matriz por un escalar: <bookmark mark='d'/> cada columna del producto es el producto <bookmark mark='b'/> del escalar por <bookmark mark='c'/> la columna correspondiente. Con nuestra notación, <bookmark mark='p'/> la definición permite desplazar los paréntesis.""",
                                    """This is the definition of the product of a matrix by a scalar: <bookmark mark='d'/> each column of the product is <bookmark mark='b'/> the scalar times <bookmark mark='c'/> the corresponding column. In our notation, <bookmark mark='p'/> the definition lets us move the parentheses.""")) as tracker:
            # la definición se lee, como la de la suma, y se escribe con «Esta es» (Marcos, 2026-11-20)
            self.play(FadeOut(marcos), Write(def_prod), run_time=1.2)
            # cada pieza se señala cuando la voz la nombra (Marcos, 2026-11-21): la columna del producto (lado izquierdo),
            # el escalar y la columna de la matriz. glifos: ( λ A ) | j (0-5)  =  λ ( A | j ) (7-12)
            col_prod, escalar, col_mat = def_prod[0][0:6], def_prod[0][7], def_prod[0][9:12]
            self.wait_until_bookmark("d")
            resalta(self, [col_prod], color=COLOR_COLUMNA, factor=1.12)
            self.wait_until_bookmark("b")
            self.play(col_prod.animate.set_color(WHITE).scale(1/1.12), escalar.animate.set_color(COLOR_ESCALAR).scale(1.4), run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(escalar.animate.set_color(WHITE).scale(1/1.4), col_mat.animate.set_color(COLOR_COLUMNA).scale(1.15), run_time=0.25)
            self.wait(1.3)
            apaga(self, [col_mat], factor=1.15, run_time=0.25)
            self.wait_until_bookmark("p")
            resalta(self, parentesis, factor=1.25)
            # como en V10 (escena 2): los glifos de la izquierda viajan a la colocación de la derecha y vuelven, para que se
            # vea moverse la pareja de paréntesis, que deja fuera primero el selector y después el escalar (Marcos, 2026-11-10)
            # glifos: ( λ A ) | j  (0-5)  =  λ ( A | j )  (7-12)
            destino = def_prod[0][7:13].copy().move_to(def_prod[0][0:6])
            self.play(*[Transform(def_prod[0][i], destino[j], rate_func=rate_functions.there_and_back_with_pause)
                        for i, j in zip(range(6), [1, 0, 2, 5, 3, 4])], run_time=2.4)
            apaga(self, parentesis, factor=1.25)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Componente a componente", "Component-wise"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A, B, S = matriz(A_EJ, COLOR_A, escala=0.72), matriz(B_EJ, COLOR_B, escala=0.72), matriz(S_EJ, escala=0.72)
        mas, igual = MathTex("+", font_size=40), MathTex("=", font_size=40)
        VGroup(A, mas, B, igual, S).arrange(RIGHT, buff=0.25).move_to([0, 2.0, 0])
        trio = [m.get_rows()[0][2] for m in (A, B, S)]   # el nueve, el tres y el doce
        
        l0 = MathTex(r"\elemLR{(\Mat{A}+\Mat{B})}{i}{j}", tex_template=myTemplate, font_size=40)
        pasos = [MathTex("=", f, tex_template=myTemplate, font_size=40)
                 for f in (r"\elemL{\Big(\elemRp{\Mat{A}+\Mat{B}}{j}\Big)}{i}",
                           r"\elemL{\Big(\VectC{A}{j}+\VectC{B}{j}\Big)}{i}",
                           r"\elemLp{\VectC{A}{j}}{i}+\elemLp{\VectC{B}{j}}{i}",
                           r"\eleM{A}{i}{j}+\eleM{B}{i}{j}")]
        for k, p in enumerate(pasos):   # los «=», en columna
            p.move_to([0, 0.75 - 0.82*k, 0])
            p.shift((-1.6 - p[0].get_left()[0])*RIGHT)
        l0.next_to(pasos[0][0], LEFT, buff=0.2)
        res_suma = MathTex(r"\elemLR{(\Mat{A}+\Mat{B})}{i}{j}", "=", r"\eleM{A}{i}{j}+\eleM{B}{i}{j}", tex_template=myTemplate, font_size=44).move_to([0, 0.2, 0])
        res_prod = MathTex(r"\elemLR{(\lambda\Mat{A})}{i}{j}", "=", r"\lambda\big(\eleM{A}{i}{j}\big)", tex_template=myTemplate, font_size=44).move_to([0, -1.0, 0])
        res_prod.shift((res_suma[1].get_left()[0] - res_prod[1].get_left()[0])*RIGHT)
        conclusion = Tex(tr("también componente a componente", "also component-wise"), font_size=36).set_color(COLOR_REGLA).move_to([0, -2.3, 0])
        
        with self.voiceover(text=tr("""En el ejemplo de la suma, cada componente del resultado es la suma de las componentes que ocupan la misma posición. <bookmark mark='x'/> El doce, por ejemplo, es la suma <bookmark mark='n'/> del nueve y <bookmark mark='t'/> el tres.""",
                                    """In the addition example, each component of the result is the sum of the components in the same position. <bookmark mark='x'/> The twelve, for example, is the sum <bookmark mark='n'/> of the nine and <bookmark mark='t'/> the three.""")) as tracker:
            self.play(Write(cabecera), FadeIn(A), FadeIn(mas), FadeIn(B), FadeIn(igual), FadeIn(S), run_time=1)
            self.wait_until_bookmark("x")
            resalta(self, [trio[2]], factor=1.4)
            self.wait_until_bookmark("n")
            resalta(self, trio[:1], factor=1.4)
            self.wait_until_bookmark("t")
            resalta(self, trio[1:2], factor=1.4)
        
        with self.voiceover(text=tr("""No es una casualidad: se deduce de la definición. Para demostrarlo, <bookmark mark='l0'/> seleccionemos una componente cualquiera de la suma.""",
                                    """This is no coincidence: it follows from the definition. To prove it, <bookmark mark='l0'/> let us select any component of the sum.""")) as tracker:
            self.play(trio[0].animate.set_color(COLOR_A).scale(1/1.4), trio[1].animate.set_color(COLOR_B).scale(1/1.4),
                      trio[2].animate.set_color(WHITE).scale(1/1.4), run_time=0.4)
            self.wait_until_bookmark("l0")
            self.play(Write(l0), run_time=1)
        
        # v2: tirada A2 elegida por Marcos de oído (2026-11-18); la primera acababa en suspenso (F0 final ~126 Hz)
        with self.voiceover(text=tr("""Como da igual seleccionar primero la fila o la columna, <bookmark mark='l1'/> seleccionamos primero la columna.<bookmark mark='v2'/>""",
                                    """Since it does not matter whether we select the row or the column first, <bookmark mark='l1'/> we select the column first.""")) as tracker:
            # glifos: i | ( A + B ) | j (0-8)  ->  i | ( ( A + B ) | j ) (0-10): al seleccionar aparecen los paréntesis grandes
            nace(self, l0[0], pasos[0][1], [(0, 0), (1, 1), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)], aparecen=[2, 10],
                 con_igual=False, extra=[FadeIn(pasos[0][0])], marca="l1")
        self.wait(1.0)   # descanso tras la frase (Marcos, 2026-11-18)
        
        with self.voiceover(text=tr("""Por la definición de suma de matrices <bookmark mark='l2'/> podemos distribuir el selector de columnas.""",
                                    """By the definition of matrix addition <bookmark mark='l2'/> we can distribute the column selector.""")) as tracker:
            # -> i | ( A | j + B | j ) (0-10): el selector de columnas va a cada sumando; los paréntesis de la suma no aparecen
            nace(self, pasos[0][1], pasos[1][1], [(0, 0), (1, 1), (2, 2), (10, 10), (4, 3), (5, 6), (6, 7)],
                 [(8, 4), (9, 5), (8, 8), (9, 9)], con_igual=False, extra=[FadeIn(pasos[1][0])], marca="l2")
        
        with self.voiceover(text=tr("""Dentro de los paréntesis <bookmark mark='d'/> queda una suma de vectores, así que <bookmark mark='l3'/> por la definición de suma de vectores también podemos distribuir el selector de componentes.""",
                                    """Inside the parentheses <bookmark mark='d'/> there is now a sum of vectors, so <bookmark mark='l3'/> by the definition of vector addition we can distribute the component selector too.""")) as tracker:
            # «una suma de vectores»: A|j + B|j (glifos 3-9) se resalta en la línea de arriba; el paso entero (copia y viaje)
            # espera a la marca, para que la línea nueva no se lea a medias (auditoría 2026-11-19)
            suma_vec = pasos[1][1][3:10]
            self.wait_until_bookmark("d")
            resalta(self, [suma_vec], factor=1.08)
            self.wait_until_bookmark("l3")
            # -> i | ( A | j ) + i | ( B | j ) (0-14): el selector de componentes y los paréntesis van a cada sumando
            nace(self, pasos[1][1], pasos[2][1], [(3, 3), (4, 4), (5, 5), (6, 7), (7, 11), (8, 12), (9, 13)],
                 [(0, 0), (1, 1), (0, 8), (1, 9), (2, 2), (2, 10), (10, 6), (10, 14)], con_igual=False, extra=[FadeIn(pasos[2][0])])
            apaga(self, [suma_vec], factor=1.08)
        
        with self.voiceover(text=tr("""Y al quitar los paréntesis <bookmark mark='l4'/> queda la suma de las dos componentes.""",
                                    """And dropping the parentheses <bookmark mark='l4'/> leaves the sum of the two components.""")) as tracker:
            # -> i | A | j + i | B | j (0-10): todo baja a su sitio menos los paréntesis, que no aparecen
            nace(self, pasos[2][1], pasos[3][1], [(0, 0), (1, 1), (3, 2), (4, 3), (5, 4), (7, 5), (8, 6), (9, 7), (11, 8), (12, 9), (13, 10)],
                 con_igual=False, extra=[FadeIn(pasos[3][0])], t_fijos=1.2)
            self.remove(*pasos[3][1]); self.add(pasos[3])
        
        self.pausa()
        
        with self.voiceover(text=tr("""Con el producto por un escalar ocurre lo mismo, y se deduce del mismo modo. <bookmark mark='r'/> Así pues, las matrices también se suman y se multiplican por un escalar componente a componente.""",
                                    """The same happens with scalar multiplication, and it is deduced in the same way. <bookmark mark='r'/> So matrices are also added and multiplied by a scalar component-wise.""")) as tracker:
            # la cadena se recoge en su resultado (primer y último miembro) y debajo aparece el del producto
            self.remove(*[g for p in pasos[:3] for g in p[1]]); self.add(*pasos[:3])   # nacieron glifo a glifo
            self.play(*[FadeOut(p) for p in pasos[:3]], ReplacementTransform(l0, res_suma[0]),
                      ReplacementTransform(pasos[3][0], res_suma[1]), ReplacementTransform(pasos[3][1], res_suma[2]), run_time=1)
            self.play(Write(res_prod), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(conclusion), run_time=0.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Matrices nulas y matriz opuesta", "Zero matrices and the opposite matrix"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        N = matriz([[0, 0, 0], [0, 0, 0]])
        nN = MathTex(r"\Mat{0}=", tex_template=myTemplate, font_size=48)
        VGroup(nN, N).arrange(RIGHT, buff=0.2).move_to([-3.6, 0.9, 0])
        def_nula = MathTex(DEF_MAT["nulo"], tex_template=myTemplate, font_size=48).move_to([-3.6, -1.9, 0])
        B, mB = matriz(B_EJ, COLOR_B), matriz(MENOSB_EJ)
        nB = MathTex(r"\Mat{B}=", tex_template=myTemplate, font_size=48).set_color(COLOR_B)
        nmB = MathTex(r"-\Mat{B}=", tex_template=myTemplate, font_size=48)
        VGroup(B, mB).arrange(DOWN, buff=0.45).move_to([3.7, 0.9, 0])
        nB.next_to(B, LEFT, buff=0.2); nmB.next_to(mB, LEFT, buff=0.2)
        def_opuesta = MathTex(DEF_MAT["opuesto"], tex_template=myTemplate, font_size=48).move_to([3.3, -1.9, 0])
        
        with self.voiceover(text=tr("""Nos faltan dos definiciones para enunciar las propiedades de la suma. <bookmark mark='n'/> Todas las componentes de las matrices nulas son cero, <bookmark mark='c'/> así que cada una de sus columnas es un vector nulo.""",
                                    """We still need two definitions to state the properties of addition. <bookmark mark='n'/> All the components of zero matrices are zero, <bookmark mark='c'/> so each of their columns is a zero vector.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("n")
            self.play(FadeIn(nN), FadeIn(N), run_time=0.8)
            self.wait_until_bookmark("c")
            marcos = marco(N.get_columns()[0])
            self.play(Create(marcos), Write(def_nula), run_time=0.8)
            for k in (1, 2):
                self.play(Transform(marcos, marco(N.get_columns()[k])), run_time=0.4)
            self.play(FadeOut(marcos), run_time=0.3)
        self.wait(0.8)   # respiro entre las dos definiciones (auditoría 2026-11-19)
        
        with self.voiceover(text=tr("""La matriz opuesta de una matriz se obtiene <bookmark mark='o'/> cambiando cada columna por su vector opuesto. <bookmark mark='e'/> La escribimos con un signo menos delante.""",
                                    """The opposite of a matrix is obtained <bookmark mark='o'/> by replacing each column with its opposite vector. <bookmark mark='e'/> We write it with a minus sign in front.""")) as tracker:
            self.play(FadeIn(nB), FadeIn(B), run_time=0.8)
            self.wait_until_bookmark("o")   # la fórmula se escribe con la frase que la describe (auditoría 2026-11-19)
            self.play(FadeIn(mB.get_brackets()), Write(def_opuesta), run_time=0.8)
            for k in range(3):
                self.play(TransformFromCopy(B.get_columns()[k], mB.get_columns()[k]), run_time=0.5)
            self.wait_until_bookmark("e")
            self.play(Write(nmB), run_time=0.8)
        self.wait(0.6)
        
        with self.voiceover(text=tr("""Con nuestra notación, <bookmark mark='p'/> la definición permite desplazar los paréntesis.""",
                                    """In our notation, <bookmark mark='p'/> the definition lets us move the parentheses.""")) as tracker:
            # como en la escena 2: los paréntesis viajan a la colocación de la derecha y vuelven; la escena 7 usa la definición
            # justo por eso. glifos: ( − A ) | j (0-5) = − ( A | j ) (7-12)
            par_op = [def_opuesta[0][0], def_opuesta[0][3], def_opuesta[0][8], def_opuesta[0][12]]
            self.wait_until_bookmark("p")
            resalta(self, par_op, factor=1.25)
            destino = def_opuesta[0][7:13].copy().move_to(def_opuesta[0][0:6])
            self.play(*[Transform(def_opuesta[0][i], destino[j], rate_func=rate_functions.there_and_back_with_pause)
                        for i, j in zip(range(6), [1, 0, 2, 5, 3, 4])], run_time=2.4)
            apaga(self, par_op, factor=1.25)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Las mismas definiciones", "The same definitions"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        
        def columna(pares, x_igual):
            filas = VGroup(*[MathTex(i, "=", d, tex_template=myTemplate, font_size=42) for i, d in pares])
            for k, f in enumerate(filas):
                f.move_to([0, 1.2 - 1.05*k, 0])
                f.shift((x_igual - f[1].get_left()[0])*RIGHT)
            return filas
        
        vectores = columna([(i, d) for _, i, d, _ in DEFINICIONES], -4.4)
        matrices = columna([definicion_matrices(clave) for clave, *_ in DEFINICIONES], 2.2)
        r_vec = Tex(tr("Vectores", "Vectors"), font_size=38).set_color(GRAY_B).move_to([vectores.get_x(), 2.3, 0])
        r_mat = Tex("Matrices", font_size=38).set_color(GRAY_B).move_to([matrices.get_x(), 2.3, 0])
        
        with self.voiceover(text=tr("""Ya tenemos cuatro definiciones para las matrices: <bookmark mark='s'/> la suma, <bookmark mark='p'/> el producto por un escalar, <bookmark mark='n'/> las matrices nulas <bookmark mark='o'/> y la matriz opuesta.""",
                                    """We now have four definitions for matrices: <bookmark mark='s'/> addition, <bookmark mark='p'/> scalar multiplication, <bookmark mark='n'/> the zero matrices <bookmark mark='o'/> and the opposite matrix.""")) as tracker:
            self.play(Write(cabecera), FadeIn(r_mat), run_time=1)
            for k, marca in enumerate(["s", "p", "n", "o"]):
                self.wait_until_bookmark(marca)
                self.play(FadeIn(matrices[k]), run_time=0.5)
        
        with self.voiceover(text=tr("""Pongamos al lado las cuatro definiciones correspondientes para los vectores.""",
                                    """Let us put next to them the four corresponding definitions for vectors.""")) as tracker:
            self.play(FadeIn(r_vec), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(v) for v in vectores], lag_ratio=0.4), run_time=2)
        
        with self.voiceover(text=tr("""Son las mismas reglas. <bookmark mark='m'/> Donde había vectores, en minúscula, ahora hay matrices, en mayúscula. <bookmark mark='s'/> Y donde antes obteníamos un número, ahora obtenemos una columna.<bookmark mark='v3'/>""",   # «columna» (Marcos, 2026-11-18): es lo que da el selector; v3: tirada X1 elegida de oído (las otras dejaban «columna» en suspenso)
                                    """They are the same rules. <bookmark mark='m'/> Where there were vectors, in lower case, there are now matrices, in upper case. <bookmark mark='s'/> And where we obtained a number, we now obtain a column.""")) as tracker:
            izquierdos = [f[0] for f in vectores] + [f[0] for f in matrices]
            derechos = [f[2] for f in vectores] + [f[2] for f in matrices]
            self.wait_until_bookmark("m")
            resalta(self, izquierdos[:4], factor=1.12)
            self.wait(1.0)
            resalta(self, izquierdos[4:], factor=1.12)
            self.wait_until_bookmark("s")
            apaga(self, izquierdos, factor=1.12)
            resalta(self, derechos[:4], factor=1.12)
            self.wait(0.9)
            resalta(self, derechos[4:], factor=1.12)
            self.wait(1.2)
            apaga(self, derechos, factor=1.12)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("La misma demostración", "The same proof"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self)
        enunciado = enunciado_traducible(1)
        cadena = coloca_cadena([linea(r"\elemRp{\Vect{a}+\Vect{b}}{i}"),
                                linea(r"=\eleVR{a}{i}+\eleVR{b}{i}"),
                                linea(r"=\eleVR{b}{i}+\eleVR{a}{i}", de_abajo=True),
                                linea(r"=\elemRp{\Vect{b}+\Vect{a}}{i}")])
        claves = [None, "suma", 1, "suma"]
        
        with self.voiceover(text=tr("""Con las cuatro definiciones de los vectores y con <bookmark mark='r'/> las propiedades de los números reales demostramos las propiedades de los vectores. <bookmark mark='e'/> Recordemos una de ellas: la propiedad conmutativa de la suma.<bookmark mark='v4'/>""",   # tirada C3 elegida por Marcos de oído (2026-11-18): «...es conmutativa» quedaba en suspenso
                                    """With the four definitions for vectors and <bookmark mark='r'/> the properties of the real numbers we proved the properties of vectors. <bookmark mark='e'/> Let us recall one of them: the commutative property of addition.""")) as tracker:
            self.play(Write(cabecera), FadeIn(panel.izq), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(panel.der), run_time=1)
            self.wait_until_bookmark("e")
            self.play(Write(enunciado), run_time=1.2)
        
        # «demostrarla» (Marcos, 2026-11-18): el antecedente es «la propiedad conmutativa». Partida en dos: la primera frase es
        # una toma nueva; el resto sale recortado de la toma anterior (tmp/parte_toma.py). La marca l1 estaba al principio del
        # resto: el paso se anima al empezar la segunda locución, sin esperar (una marca en la posición 0 se dispara al final).
        with self.voiceover(text=tr("""Para demostrarla, <bookmark mark='l0'/> seleccionamos una componente cualquiera.""",   # «cualquiera» (auditoría 2026-11-21): la conclusión ya no lo dice
                                    """To prove it, <bookmark mark='l0'/> we select any component.""")) as tracker:
            # glifos: ( a + b ) | i (0-6);  = a | i + b | i (0-7);  = ( b + a ) | i (0-7)
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=0.9)
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l2'/> Los sumandos son números, así que <bookmark mark='c2'/> por la conmutativa podemos intercambiarlos. <bookmark mark='l3'/> Y por la definición de suma podemos sacar el selector como factor común.""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l2'/> The terms are numbers, so <bookmark mark='c2'/> by the commutative property we can swap them. <bookmark mark='l3'/> And by the definition of addition we can factor out the selector.""")) as tracker:
            # cada línea nace de la anterior y cada uso se cuenta con la campanita, como en V06 (Marcos, 2026-11-10)
            # «Por la definición de suma...»: el selector va a cada sumando; los paréntesis no aparecen
            paso(self, panel, "suma", cadena[0], cadena[1], [(1, 1), (2, 4), (3, 5)], [(5, 2), (6, 3), (5, 6), (6, 7)])
            self.wait_until_bookmark("l2")   # «los sumandos son números»
            sumandos = [cadena[1][0][1:4], cadena[1][0][5:8]]
            self.play(*[Indicate(g, color=COLOR_REGLA, scale_factor=1.2) for g in sumandos], run_time=0.9)
            self.wait_until_bookmark("c2")   # los dos sumandos se cruzan
            paso(self, panel, 1, cadena[1], cadena[2], [(4, 4)], [(1, 5), (2, 6), (3, 7), (5, 1), (6, 2), (7, 3)])
            self.wait_until_bookmark("l3")   # los dos selectores se reúnen en uno, fuera de los paréntesis nuevos
            paso(self, panel, "suma", cadena[2], cadena[3], [(1, 2), (4, 3), (5, 4)], [(2, 6), (3, 7), (6, 6), (7, 7)], aparecen=[1, 5])
        
        # la conclusión dice el criterio de igualdad (Marcos, 2026-11-20, como en V14): son iguales porque lo son componente a
        # componente; la locución anterior conserva su toma, recortada antes de la conclusión (tmp/parte_toma.py)
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> los dos vectores son iguales, porque lo son <bookmark mark='c'/> componente a componente.""",
                                    """So <bookmark mark='ok'/> the two vectors are equal, because they are equal <bookmark mark='c'/> component by component.""")) as tracker:
            self.wait_until_bookmark("ok")
            self.play(Indicate(cadena[0], color=COLOR_ESCALAR, scale_factor=1.1), Indicate(cadena[3], color=COLOR_ESCALAR, scale_factor=1.1),
                      Indicate(enunciado, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.5)
            self.wait_until_bookmark("c")
            senala_selector(self, [cadena[0], cadena[3]], color=COLOR_ESCALAR)   # el selector de componentes, a los dos extremos
        
        self.pausa()
        
        with self.voiceover(text=tr("""Ahora cambiemos los símbolos. <bookmark mark='m'/> Donde había vectores, ponemos matrices. <bookmark mark='c'/> Donde se seleccionaba una componente, se selecciona una columna. <bookmark mark='v'/> Y a la derecha, en lugar de las propiedades de los números, <bookmark mark='w'/> ponemos las de los vectores, que ya están demostradas: son las mismas, <bookmark mark='b'/> con las letras en negrita.""",
                                    """Now let us change the symbols. <bookmark mark='m'/> Where there were vectors, we put matrices. <bookmark mark='c'/> Where a component was selected, a column is selected. <bookmark mark='v'/> And on the right, instead of the properties of numbers, <bookmark mark='w'/> we put those of vectors, which are already proved: they are the same, <bookmark mark='b'/> with the letters in bold.""")) as tracker:
            for k, marca in enumerate(["m", "c"], start=1):
                self.wait_until_bookmark(marca)
                self.play(*cambio_de_simbolos(k, panel, enunciado, cadena), run_time=1.5)
            # tercera etapa (auditoría 2026-11-19): en «Y a la derecha» se señalan las propiedades de los números; el cambio
            # llega en «ponemos las de los vectores», y las letras en negrita se señalan al nombrarlas
            lado_der = [panel.piezas[k] for k in (1, 2, 3, 4)]
            self.wait_until_bookmark("v")
            self.play(*[Indicate(x, color=COLOR_ESCALAR, scale_factor=1.08) for x in lado_der], run_time=1.0)
            self.wait_until_bookmark("w")
            self.play(*cambio_de_simbolos(3, panel, enunciado, cadena), run_time=1.5)
            self.wait_until_bookmark("b")
            self.play(*[Indicate(x[1] if len(x) > 1 else x, color=COLOR_ESCALAR, scale_factor=1.12) for x in lado_der], run_time=1.2)
        
        self.pausa()
        panel.reinicia()   # los usos se cuentan de nuevo al releer la demostración, ya para matrices
        
        with self.voiceover(text=tr("""Leamos de nuevo la demostración. <bookmark mark='l0'/> Seleccionamos una columna. <bookmark mark='l1'/> Por la definición de suma de matrices podemos distribuir el selector. <bookmark mark='l2'/> Los sumandos son vectores, así que <bookmark mark='c2'/> por la conmutativa de los vectores podemos intercambiarlos. <bookmark mark='l3'/> Y por la definición de suma podemos sacar el selector como factor común.""",
                                    """Let us read the proof again. <bookmark mark='l0'/> We select a column. <bookmark mark='l1'/> By the definition of matrix addition we can distribute the selector. <bookmark mark='l2'/> The terms are vectors, so <bookmark mark='c2'/> by the commutative property of vectors we can swap them. <bookmark mark='l3'/> And by the definition of addition we can factor out the selector.""")) as tracker:
            # en la relectura cada paso se vuelve a animar como en la primera lectura (Marcos, 2026-11-18): las líneas 1-3
            # se retiran y vuelven a nacer de la anterior, ya con matrices (los glifos son los mismos en todas las versiones)
            fantasmas = [c.copy() for c in cadena[1:]]
            self.remove(*cadena[1:]); self.add(*fantasmas)
            self.play(*[FadeOut(f) for f in fantasmas], run_time=0.6)
            self.wait_until_bookmark("l0")
            self.play(Indicate(cadena[0], color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.0)
            self.wait_until_bookmark("l1")   # el selector va a cada sumando
            paso(self, panel, "suma", cadena[0], cadena[1], [(1, 1), (2, 4), (3, 5)], [(5, 2), (6, 3), (5, 6), (6, 7)])
            self.wait_until_bookmark("l2")   # «los sumandos son vectores», como en la primera lectura (auditoría 2026-11-19)
            sumandos = [cadena[1][0][1:4], cadena[1][0][5:8]]
            self.play(*[Indicate(g, color=COLOR_REGLA, scale_factor=1.2) for g in sumandos], run_time=0.9)
            self.wait_until_bookmark("c2")   # los dos sumandos (vectores) se cruzan
            paso(self, panel, 1, cadena[1], cadena[2], [(4, 4)], [(1, 5), (2, 6), (3, 7), (5, 1), (6, 2), (7, 3)])
            self.wait_until_bookmark("l3")   # los dos selectores se reúnen en uno
            paso(self, panel, "suma", cadena[2], cadena[3], [(1, 2), (4, 3), (5, 4)], [(2, 6), (3, 7), (6, 6), (7, 7)], aparecen=[1, 5])
        
        self.wait(0.4)   # el punto entre el último paso y la conclusión (auditoría 2026-11-21)
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> las dos matrices son iguales, porque lo son <bookmark mark='c'/> columna a columna. La suma de matrices es conmutativa. No hemos tenido que cambiar ningún paso.""",
                                    """So <bookmark mark='ok'/> the two matrices are equal, because they are equal <bookmark mark='c'/> column by column. Matrix addition is commutative. We did not have to change a single step.""")) as tracker:
            self.wait_until_bookmark("ok")
            caja = SurroundingRectangle(enunciado, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
            self.play(Create(caja), Indicate(enunciado, color=COLOR_RESULTADO, scale_factor=1.15), run_time=1.5)
            self.wait_until_bookmark("c")
            senala_selector(self, [cadena[0], cadena[3]])   # el selector de columnas, a los dos extremos
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Otra demostración que ya está hecha", "Another proof that is already done"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self)
        enunciado = enunciado_traducible(4)
        cadena = coloca_cadena([linea(r"\elemR{\big(\Vect{a}+(-\Vect{a})\big)}{i}"),
                                linea(r"=\eleVR{a}{i}+\elemRp{-\Vect{a}}{i}"),
                                linea(r"=\eleVR{a}{i}+\big(-\eleVRpE{a}{i}\big)"),
                                linea(r"=0", de_abajo=True, final=r"=\Vect{0}"),
                                linea(r"=\eleVR{0}{i}")])
        claves = [None, "suma", "opuesto", 4, "nulo"]
        idea = aviso("idea", tr("Mismas reglas, mismas demostraciones", "Same rules, same proofs"), font_size=34).to_edge(DOWN, buff=0.3)
        
        with self.voiceover(text=tr("""Hagamos lo mismo con otra propiedad de los vectores: sumar un vector y su opuesto da un vector nulo.""",
                                    """Let us do the same with another property of vectors: adding a vector and its opposite gives a zero vector.""")) as tracker:
            self.play(Write(cabecera), FadeIn(panel.todo), run_time=1)
            self.play(Write(enunciado), FadeIn(cadena[0]), run_time=1.2)
        
        with self.voiceover(text=tr("""En su demostración <bookmark mark='l1'/> distribuimos el selector y <bookmark mark='l2'/> desplazamos los paréntesis por la definición de opuesto. <bookmark mark='l3'/> Sumar un número y su opuesto da cero, <bookmark mark='l4'/> y el cero es una componente de un vector nulo.""",
                                    """In its proof <bookmark mark='l1'/> we distribute the selector and <bookmark mark='l2'/> move the parentheses by the definition of opposite. <bookmark mark='l3'/> Adding a number and its opposite gives zero, <bookmark mark='l4'/> and zero is a component of a zero vector.""")) as tracker:
            # glifos: ( a + ( - a ) ) | i (0-9);  = a | i + ( - a ) | i (0-10);  = a | i + ( - ( a | i ) ) (0-12);  = 0;  = 0 | i
            rapido = dict(t_fijos=0.5, t_moviles=0.6, t_cuenta=0.35)
            self.wait_until_bookmark("l1")   # el selector va a cada sumando; los paréntesis grandes no aparecen
            paso(self, panel, "suma", cadena[0], cadena[1], [(1, 1), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8)],
                 [(8, 2), (9, 3), (8, 9), (9, 10)], **rapido)
            self.wait_until_bookmark("l2")   # los paréntesis pasan a rodear la componente; el sumando entero, entre paréntesis nuevos
            paso(self, panel, "opuesto", cadena[1], cadena[2], [(1, 1), (2, 2), (3, 3), (4, 4), (6, 6), (7, 8), (9, 9), (10, 10)],
                 [(5, 7), (8, 11)], aparecen=[5, 12], **rapido)
            self.wait_until_bookmark("l3")   # toda la suma se convierte en el cero
            paso(self, panel, 4, cadena[2], cadena[3], [], [(slice(1, 13), 1)], t_fijos=0.4, t_moviles=0.7, t_cuenta=0.35)
            self.wait_until_bookmark("l4")   # al cero le sale el selector
            paso(self, panel, "nulo", cadena[3], cadena[4], [(1, 1)], aparecen=[2, 3], **rapido)
        
        self.pausa()
        
        with self.voiceover(text=tr("""Hacemos el mismo cambio de símbolos.""",
                                    """We make the same change of symbols.""")) as tracker:
            for k in (1, 2, 3):
                self.play(*cambio_de_simbolos(k, panel, enunciado, cadena), run_time=0.9)
            panel.reinicia(run_time=0.4)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Ahora la demostración dice que <bookmark mark='l1'/> distribuimos el selector y <bookmark mark='l2'/> desplazamos los paréntesis por la definición de matriz opuesta. <bookmark mark='l3'/> Sumar un vector y su opuesto da un vector nulo, <bookmark mark='l4'/> y ese vector nulo es una columna de una matriz nula.""",
                                    """Now the proof says that <bookmark mark='l1'/> we distribute the selector and <bookmark mark='l2'/> move the parentheses by the definition of the opposite matrix. <bookmark mark='l3'/> Adding a vector and its opposite gives a zero vector, <bookmark mark='l4'/> and that zero vector is a column of a zero matrix.""")) as tracker:
            # cada paso se vuelve a animar, ya con matrices (como la relectura de la escena 6; auditoría 2026-11-19): se ve
            # qué se convierte en qué, también el vector nulo que pasa a ser columna de una matriz nula
            fantasmas = [c.copy() for c in cadena[1:]]
            self.remove(*cadena[1:]); self.add(*fantasmas)
            self.play(*[FadeOut(f) for f in fantasmas], run_time=0.5)
            self.wait_until_bookmark("l1")
            paso(self, panel, "suma", cadena[0], cadena[1], [(1, 1), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8)],
                 [(8, 2), (9, 3), (8, 9), (9, 10)], **rapido)
            self.wait_until_bookmark("l2")
            paso(self, panel, "opuesto", cadena[1], cadena[2], [(1, 1), (2, 2), (3, 3), (4, 4), (6, 6), (7, 8), (9, 9), (10, 10)],
                 [(5, 7), (8, 11)], aparecen=[5, 12], **rapido)
            self.wait_until_bookmark("l3")
            paso(self, panel, 4, cadena[2], cadena[3], [], [(slice(1, 13), 1)], t_fijos=0.4, t_moviles=0.7, t_cuenta=0.35)
            self.wait_until_bookmark("l4")
            paso(self, panel, "nulo", cadena[3], cadena[4], [(1, 1)], aparecen=[2, 3], **rapido)
        
        self.wait(0.4)   # el punto entre el último paso y la conclusión (auditoría 2026-11-21)
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> las dos matrices son iguales, porque lo son <bookmark mark='c'/> columna a columna. Sumar una matriz y su opuesta da una matriz nula.""",
                                    """So <bookmark mark='ok'/> the two matrices are equal, because they are equal <bookmark mark='c'/> column by column. Adding a matrix and its opposite gives a zero matrix.""")) as tracker:
            self.wait_until_bookmark("ok")
            caja = SurroundingRectangle(enunciado, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
            self.play(Create(caja), Indicate(enunciado, color=COLOR_RESULTADO, scale_factor=1.15), run_time=1.5)
            self.wait_until_bookmark("c")
            senala_selector(self, [cadena[0], cadena[4]])   # el selector de columnas, a los dos extremos
        
        self.pausa()
        
        with self.voiceover(text=tr("""Esta es la gran ventaja del álgebra. <bookmark mark='i'/> Las demostraciones solo han usado reglas para manipular símbolos, así que no importa si los símbolos representan vectores o matrices. Si unos objetos nuevos cumplen las mismas reglas, las demostraciones de sus propiedades ya están hechas.""",
                                    """This is the great advantage of algebra. <bookmark mark='i'/> The proofs have only used rules for manipulating symbols, so it does not matter whether the symbols stand for vectors or matrices. If new objects obey the same rules, the proofs of their properties are already done.""")) as tracker:
            self.wait_until_bookmark("i")
            self.play(FadeIn(idea, scale=0.9), run_time=0.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Las ocho propiedades", "The eight properties"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        
        def tabla(props, x):
            filas = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=34) for k, p in enumerate(props)])
            filas.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
            return filas.move_to([x, 0.05, 0])
        
        vectores, matrices = tabla(PROPIEDADES_VECTORES, -3.4), tabla(PROPIEDADES_MATRICES, 3.4)
        for v, m in zip(vectores, matrices):
            m.set_y(v.get_y())
        r_vec = Tex(tr("Vectores", "Vectors"), font_size=36).set_color(GRAY_B).next_to(vectores, UP, buff=0.3)
        r_mat = Tex("Matrices", font_size=36).set_color(GRAY_B).next_to(matrices, UP, buff=0.3)
        r_mat.set_y(r_vec.get_y())
        nota = Tex(tr("(demostradas en los vídeos 1.6 y 1.7)", "(proved in videos 1.6 and 1.7)"), font_size=28).set_color(GRAY_A).next_to(vectores, DOWN, buff=0.25).align_to(vectores, LEFT)
        
        with self.voiceover(text=tr("""Las operaciones con vectores cumplen ocho propiedades: <bookmark mark='s'/> cuatro de la suma <bookmark mark='p'/> y cuatro del producto por escalares.""",
                                    """Vector operations satisfy eight properties: <bookmark mark='s'/> four for addition <bookmark mark='p'/> and four for scalar multiplication.""")) as tracker:
            self.play(Write(cabecera), FadeIn(r_vec), FadeIn(nota), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(vectores[:4]), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(FadeIn(vectores[4:]), run_time=0.8)
        
        with self.voiceover(text=tr("""Con el mismo cambio de símbolos, <bookmark mark='m'/> las operaciones con matrices cumplen las mismas ocho.""",
                                    """With the same change of symbols, <bookmark mark='m'/> matrix operations satisfy the same eight.""")) as tracker:
            self.wait_until_bookmark("m")
            self.play(FadeIn(r_mat), *[TransformFromCopy(v, m) for v, m in zip(vectores, matrices)], run_time=2)
        
        self.pausa_para_pensar(invitacion=tr("Pause el vídeo y demuestre otra propiedad de la suma.", "Pause the video and prove another property of addition."),
                               invitacion_voz=tr("Para convencerse, pause el vídeo e intente demostrar otra de las propiedades de la suma: escriba la demostración para vectores y cambie los símbolos.",
                                                 "To convince yourself, pause the video and try to prove another of the properties of addition: write down the proof for vectors and change the symbols."),
                               al_invitar=lambda: self.play(   # las que quedan son la 2 y la 3; la 1 y la 4 ya están hechas (auditoría 2026-11-19)
                                   FadeOut(nota),   # la tarjeta la tapaba a medias (auditoría 2026-11-21)
                                   *[Create(marco(t[k], COLOR_ESCALAR)) for t in (vectores, matrices) for k in (1, 2)],
                                   *[t[k].animate.set_opacity(0.35) for t in (vectores, matrices) for k in (0, 3)], run_time=0.8))
        
        self.pausa()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [DEF_MAT["suma"] + r"\qquad\quad " + DEF_MAT["producto"],
                    r"\elemLR{(\Mat{A}+\Mat{B})}{i}{j}=\eleM{A}{i}{j}+\eleM{B}{i}{j}\qquad\quad \elemLR{(\lambda\Mat{A})}{i}{j}=\lambda\big(\eleM{A}{i}{j}\big)",
                    r"\Mat{A}+\Mat{B}=\Mat{B}+\Mat{A},\quad\ldots,\quad 1\Mat{A}=\Mat{A}"]
        rotulos = [tr("suma y producto por un escalar: columna a columna", "addition and scalar multiplication: column by column"),
                   tr("y por tanto, componente a componente", "and therefore, component-wise"),
                   tr(r"las mismas ocho propiedades que los vectores,\\ y se demuestran del mismo modo", "the same eight properties as vectors, proved in the same way")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=40), Tex(r, tex_template=myTemplate, font_size=32, color=GRAY_A)).arrange(DOWN, buff=0.18)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.45).move_to([0, 0.35, 0])
        idea = aviso("idea", tr("Las demostraciones solo usan reglas para manipular símbolos", "Proofs only use rules for manipulating symbols"), font_size=32).to_edge(DOWN, buff=0.45)
        
        with self.voiceover(text=tr("""Resumamos. Las matrices se suman y se multiplican por un escalar columna a columna, <bookmark mark='c'/> y por tanto también componente a componente.""",
                                    """Let us sum up. Matrices are added and multiplied by a scalar column by column, <bookmark mark='c'/> and therefore also component-wise.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("c")
            self.play(FadeIn(filas[1]), run_time=0.8)
        
        with self.voiceover(text=tr("""Estas operaciones cumplen las mismas ocho propiedades que las operaciones con vectores.""",
                                    """These operations satisfy the same eight properties as vector operations.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.8)
        
        with self.voiceover(text=tr("""En vídeos anteriores usamos dibujos para entender las operaciones con números y con vectores. Aquí no ha hecho falta ninguno: <bookmark mark='i'/> las demostraciones solo usan reglas para manipular símbolos, y las matrices cumplen las mismas reglas que los vectores.""",
                                    """In earlier videos we used drawings to understand the operations with numbers and with vectors. Here we have not needed any: <bookmark mark='i'/> the proofs only use rules for manipulating symbols, and matrices obey the same rules as vectors.""")) as tracker:
            self.wait_until_bookmark("i")
            self.play(FadeIn(idea, scale=0.9), run_time=0.8)
        
        self.wait(1.0)
        with self.voiceover(text=tr("""En este vídeo hemos visto que con las matrices podemos operar <bookmark mark='c'/> columna a columna, <bookmark mark='k'/> o componente a componente.""",
                                    """In this video we have seen that we can operate with matrices <bookmark mark='c'/> column by column, <bookmark mark='k'/> or component by component.""")) as tracker:
            self.wait_until_bookmark("c")
            self.play(Indicate(filas[0][1], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1.0)
            self.wait_until_bookmark("k")
            self.play(Indicate(filas[1][1], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1.0)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos que las mismas operaciones, la suma y el producto por un escalar, también se pueden hacer fila a fila. Y veremos lo que ocurre al transponer una suma o un producto por un escalar.""",
                                    """In the next video we will see that the same operations, addition and scalar multiplication, can also be done row by row. And we will see what happens when we transpose a sum or a product by a scalar.""")) as tracker:
            pass
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos_finales()


class L01_V13_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class L01_V13_E01_Suma(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        A, B, S = matriz(A_EJ, COLOR_A), matriz(B_EJ, COLOR_B), matriz(S_EJ)
        mas, igual = MathTex("+", font_size=48), MathTex("=", font_size=48)
        VGroup(A, mas, B, igual, S).arrange(RIGHT, buff=0.3).move_to([0, 1.25, 0])
        nombres = VGroup(*[MathTex(t, tex_template=myTemplate, font_size=40).next_to(m, DOWN, buff=0.25)
                           for t, m in ((r"\Mat{A}", A), (r"\Mat{B}", B), (r"\Mat{A}+\Mat{B}", S))])
        nombres[0].set_color(COLOR_A); nombres[1].set_color(COLOR_B)
        sumas = [MathTex(vec(a), "+", vec(b), "=", vec(s), tex_template=myTemplate, font_size=44).move_to([0, -1.15, 0])
                 for a, b, s in zip(columnas(A_EJ), columnas(B_EJ), columnas(S_EJ))]
        for s in sumas:
            s[0].set_color(COLOR_A); s[2].set_color(COLOR_B)
        def_suma = MathTex(DEF_MAT["suma"], tex_template=myTemplate, font_size=52).move_to([0, -2.75, 0])
        selectores = [def_suma[0][5:7], def_suma[0][9:11], def_suma[0][13:15]]   # los tres «|j»
        
        with self.voiceover(text=tr("""En este vídeo veremos la suma de matrices y el producto de una matriz por un escalar. Y descubriremos que sus propiedades ya están demostradas.""",
                                    """In this video we will look at the addition of matrices and the multiplication of a matrix by a scalar. And we will find that their properties have already been proved.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        self.wait(1.0)   # respiro tras el arranque (auditoría 2026-11-21)
        
        with self.voiceover(text=tr("""Las columnas de una matriz <bookmark mark='k'/> son vectores, <break time="200ms"/> que ya sabemos sumar. Por eso definimos la suma de <bookmark mark='m'/> dos matrices del mismo orden columna a columna.""",
                                    """The columns of a matrix <bookmark mark='k'/> are vectors, and we already know how to add vectors. That is why we define the sum of <bookmark mark='m'/> two matrices of the same order column by column.""")) as tracker:
            # las dos matrices del ejemplo se ven desde que la voz habla de columnas; el signo de sumar, al decir «sumar»
            self.play(FadeIn(A), FadeIn(B), FadeIn(nombres[0]), FadeIn(nombres[1]), run_time=1)
            self.wait_until_bookmark("k")   # una columna enmarcada, la misma que después (auditoría 2026-11-19)
            col_k = marco(A.get_columns()[0])
            self.play(Create(col_k), run_time=0.4)
            self.wait(0.8)
            self.play(FadeOut(col_k), run_time=0.3)
            self.wait_until_bookmark("m")
            self.play(FadeIn(mas), run_time=0.6)
        
        # el propósito, dicho (Marcos, 2026-11-21: el «por eso» lo dejaba implícito); locución aparte para conservar la toma
        # anterior. Las columnas de las dos matrices se enmarcan mientras la voz lo dice: son los vectores que se aprovechan
        with self.voiceover(text=tr("""Así aprovechamos todo lo que ya hemos aprendido sobre los vectores.""",
                                    """This way we reuse everything we have learned about vectors.""")) as tracker:
            cols = VGroup(*[marco(c) for M in (A, B) for c in M.get_columns()])
            self.play(Create(cols, lag_ratio=0.15), run_time=1.2)
            self.wait(max(tracker.duration - 1.6, 0.1))
            self.play(FadeOut(cols), run_time=0.4)
        
        self.wait(0.6)
        
        with self.voiceover(text=tr("""La primera columna de la suma es la suma de las primeras columnas, <bookmark mark='c2'/> la segunda es la suma de las segundas, <bookmark mark='c3'/> y la tercera, la suma de las terceras.""",
                                    """The first column of the sum is the sum of the first columns, <bookmark mark='c2'/> the second is the sum of the second columns, <bookmark mark='c3'/> and the third, the sum of the third columns.""")) as tracker:
            self.play(FadeIn(igual), FadeIn(S.get_brackets()), FadeIn(nombres[2]), run_time=0.6)
            # sin «En este ejemplo» (Marcos, 2026-11-20: sonaba a que en otro ejemplo podría no ser así); la toma es la
            # nueva (el recorte se notaba) y la primera columna se señala al empezar la frase
            for k, marca in enumerate([None, "c2", "c3"]):
                if marca:
                    self.wait_until_bookmark(marca)
                nuevos = VGroup(marco(A.get_columns()[k]), marco(B.get_columns()[k]))
                if k == 0:
                    marcos = nuevos
                    self.play(Create(marcos), FadeIn(sumas[0]), run_time=0.6)
                else:
                    self.play(Transform(marcos, nuevos), FadeOut(sumas[k-1]), FadeIn(sumas[k]), run_time=0.6)
                self.play(FadeIn(S.get_columns()[k]), run_time=0.5)
        
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Esta es la definición de suma de matrices: <bookmark mark='d'/> cada columna de la suma es la suma de <bookmark mark='c'/> las columnas correspondientes. Con nuestra notación, <bookmark mark='s'/> el selector de columnas <bookmark mark='v'/> se distribuye entre los sumandos.""",
                                    """This is the definition of matrix addition: <bookmark mark='d'/> each column of the sum is the sum of <bookmark mark='c'/> the corresponding columns. In our notation, <bookmark mark='s'/> the column selector <bookmark mark='v'/> distributes over the terms.""")) as tracker:
            # la definición se escribe con «Esta es» (Marcos, 2026-11-20: si no, la voz señala algo que no está)
            self.play(FadeOut(marcos), Write(def_suma), run_time=1.2)
            # cada pieza se señala cuando la voz la nombra, como en la definición del producto (Marcos, 2026-11-21): la columna
            # de la suma (lado izquierdo) y las columnas de los sumandos. glifos: ( A + B ) | j (0-6)  =  A | j (8-10)  +  B | j (12-14)
            col_suma, cols = def_suma[0][0:7], [def_suma[0][8:11], def_suma[0][12:15]]
            self.wait_until_bookmark("d")
            resalta(self, [col_suma], color=COLOR_COLUMNA, factor=1.12)
            self.wait_until_bookmark("c")
            self.play(col_suma.animate.set_color(WHITE).scale(1/1.12), *[x.animate.set_color(COLOR_COLUMNA).scale(1.15) for x in cols], run_time=0.25)
            self.wait(1.3)
            apaga(self, cols, factor=1.15, run_time=0.25)
            # «el selector de columnas»: el |j de la izquierda; «se distribuye»: dos copias suyas viajan a los dos sumandos
            # (Marcos, 2026-11-18); los |j de la derecha se atenúan un instante para que se vea llegar cada copia
            self.wait_until_bookmark("s")
            resalta(self, selectores[:1], color=COLOR_COLUMNA, factor=1.25)
            self.wait_until_bookmark("v")
            llegadas = [x.copy().set_color(COLOR_COLUMNA).scale(1.25) for x in selectores[1:]]
            self.play(*[x.animate.set_opacity(0.15) for x in selectores[1:]], run_time=0.25)
            self.play(*[TransformFromCopy(selectores[0], y) for y in llegadas], run_time=1.0)
            self.remove(*llegadas)
            for x in selectores[1:]:
                x.set_opacity(1).set_color(COLOR_COLUMNA).scale(1.25)
            self.wait(1.2)
            apaga(self, selectores, factor=1.25)
        
        self.pausa_media()


class L01_V13_E02_Producto(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Producto de una matriz por un escalar", "Product of a matrix by a scalar"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        dos = MathTex("2", font_size=56).set_color(COLOR_ESCALAR)
        B, P = matriz(B_EJ, COLOR_B), matriz(DOSB_EJ)
        igual = MathTex("=", font_size=48)
        VGroup(dos, B, igual, P).arrange(RIGHT, buff=0.3).move_to([0, 1.25, 0])
        nombres = VGroup(*[MathTex(t, tex_template=myTemplate, font_size=40).next_to(m, DOWN, buff=0.25)
                           for t, m in ((r"\Mat{B}", B), (r"2\Mat{B}", P))])
        nombres[0].set_color(COLOR_B)
        prods = [MathTex("2", vec(b), "=", vec(p), tex_template=myTemplate, font_size=44).move_to([0, -1.15, 0])
                 for b, p in zip(columnas(B_EJ), columnas(DOSB_EJ))]
        for p in prods:
            p[0].set_color(COLOR_ESCALAR); p[1].set_color(COLOR_B)
        def_prod = MathTex(DEF_MAT["producto"], tex_template=myTemplate, font_size=52).move_to([0, -2.75, 0])
        parentesis = [def_prod[0][0], def_prod[0][3], def_prod[0][8], def_prod[0][12]]
        
        with self.voiceover(text=tr("""Con el producto por un escalar hacemos lo mismo: para multiplicar una matriz por un número, multiplicamos <bookmark mark='c0'/> cada una de sus columnas por ese número.""",
                                    """With scalar multiplication we do the same: to multiply a matrix by a number, we multiply <bookmark mark='c0'/> each of its columns by that number.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.play(FadeIn(dos), FadeIn(B), FadeIn(nombres[0]), run_time=1)
            self.wait_until_bookmark("c0")
            marcos = marco(B.get_columns()[0])
            self.play(Create(marcos), run_time=0.4)
        
        with self.voiceover(text=tr("""Cada columna del resultado es el doble de la columna correspondiente de la matriz.""",
                                    """Each column of the result is twice the corresponding column of the matrix.""")) as tracker:
            self.play(FadeIn(igual), FadeIn(P.get_brackets()), FadeIn(nombres[1]), run_time=0.6)
            for k in range(3):   # unos 1,5 s por columna (auditoría 2026-11-19)
                if k == 0:
                    self.play(FadeIn(prods[0]), run_time=0.5)
                else:
                    self.play(Transform(marcos, marco(B.get_columns()[k])), FadeOut(prods[k-1]), FadeIn(prods[k]), run_time=0.5)
                self.play(FadeIn(P.get_columns()[k]), run_time=0.4)
                self.wait(0.9)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Esta es la definición de producto de una matriz por un escalar: <bookmark mark='d'/> cada columna del producto es el producto <bookmark mark='b'/> del escalar por <bookmark mark='c'/> la columna correspondiente. Con nuestra notación, <bookmark mark='p'/> la definición permite desplazar los paréntesis.""",
                                    """This is the definition of the product of a matrix by a scalar: <bookmark mark='d'/> each column of the product is <bookmark mark='b'/> the scalar times <bookmark mark='c'/> the corresponding column. In our notation, <bookmark mark='p'/> the definition lets us move the parentheses.""")) as tracker:
            # la definición se lee, como la de la suma, y se escribe con «Esta es» (Marcos, 2026-11-20)
            self.play(FadeOut(marcos), Write(def_prod), run_time=1.2)
            # cada pieza se señala cuando la voz la nombra (Marcos, 2026-11-21): la columna del producto (lado izquierdo),
            # el escalar y la columna de la matriz. glifos: ( λ A ) | j (0-5)  =  λ ( A | j ) (7-12)
            col_prod, escalar, col_mat = def_prod[0][0:6], def_prod[0][7], def_prod[0][9:12]
            self.wait_until_bookmark("d")
            resalta(self, [col_prod], color=COLOR_COLUMNA, factor=1.12)
            self.wait_until_bookmark("b")
            self.play(col_prod.animate.set_color(WHITE).scale(1/1.12), escalar.animate.set_color(COLOR_ESCALAR).scale(1.4), run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(escalar.animate.set_color(WHITE).scale(1/1.4), col_mat.animate.set_color(COLOR_COLUMNA).scale(1.15), run_time=0.25)
            self.wait(1.3)
            apaga(self, [col_mat], factor=1.15, run_time=0.25)
            self.wait_until_bookmark("p")
            resalta(self, parentesis, factor=1.25)
            # como en V10 (escena 2): los glifos de la izquierda viajan a la colocación de la derecha y vuelven, para que se
            # vea moverse la pareja de paréntesis, que deja fuera primero el selector y después el escalar (Marcos, 2026-11-10)
            # glifos: ( λ A ) | j  (0-5)  =  λ ( A | j )  (7-12)
            destino = def_prod[0][7:13].copy().move_to(def_prod[0][0:6])
            self.play(*[Transform(def_prod[0][i], destino[j], rate_func=rate_functions.there_and_back_with_pause)
                        for i, j in zip(range(6), [1, 0, 2, 5, 3, 4])], run_time=2.4)
            apaga(self, parentesis, factor=1.25)
        
        self.pausa_media()


class L01_V13_E03_Componentes(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Componente a componente", "Component-wise"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A, B, S = matriz(A_EJ, COLOR_A, escala=0.72), matriz(B_EJ, COLOR_B, escala=0.72), matriz(S_EJ, escala=0.72)
        mas, igual = MathTex("+", font_size=40), MathTex("=", font_size=40)
        VGroup(A, mas, B, igual, S).arrange(RIGHT, buff=0.25).move_to([0, 2.0, 0])
        trio = [m.get_rows()[0][2] for m in (A, B, S)]   # el nueve, el tres y el doce
        
        l0 = MathTex(r"\elemLR{(\Mat{A}+\Mat{B})}{i}{j}", tex_template=myTemplate, font_size=40)
        pasos = [MathTex("=", f, tex_template=myTemplate, font_size=40)
                 for f in (r"\elemL{\Big(\elemRp{\Mat{A}+\Mat{B}}{j}\Big)}{i}",
                           r"\elemL{\Big(\VectC{A}{j}+\VectC{B}{j}\Big)}{i}",
                           r"\elemLp{\VectC{A}{j}}{i}+\elemLp{\VectC{B}{j}}{i}",
                           r"\eleM{A}{i}{j}+\eleM{B}{i}{j}")]
        for k, p in enumerate(pasos):   # los «=», en columna
            p.move_to([0, 0.75 - 0.82*k, 0])
            p.shift((-1.6 - p[0].get_left()[0])*RIGHT)
        l0.next_to(pasos[0][0], LEFT, buff=0.2)
        res_suma = MathTex(r"\elemLR{(\Mat{A}+\Mat{B})}{i}{j}", "=", r"\eleM{A}{i}{j}+\eleM{B}{i}{j}", tex_template=myTemplate, font_size=44).move_to([0, 0.2, 0])
        res_prod = MathTex(r"\elemLR{(\lambda\Mat{A})}{i}{j}", "=", r"\lambda\big(\eleM{A}{i}{j}\big)", tex_template=myTemplate, font_size=44).move_to([0, -1.0, 0])
        res_prod.shift((res_suma[1].get_left()[0] - res_prod[1].get_left()[0])*RIGHT)
        conclusion = Tex(tr("también componente a componente", "also component-wise"), font_size=36).set_color(COLOR_REGLA).move_to([0, -2.3, 0])
        
        with self.voiceover(text=tr("""En el ejemplo de la suma, cada componente del resultado es la suma de las componentes que ocupan la misma posición. <bookmark mark='x'/> El doce, por ejemplo, es la suma <bookmark mark='n'/> del nueve y <bookmark mark='t'/> el tres.""",
                                    """In the addition example, each component of the result is the sum of the components in the same position. <bookmark mark='x'/> The twelve, for example, is the sum <bookmark mark='n'/> of the nine and <bookmark mark='t'/> the three.""")) as tracker:
            self.play(Write(cabecera), FadeIn(A), FadeIn(mas), FadeIn(B), FadeIn(igual), FadeIn(S), run_time=1)
            self.wait_until_bookmark("x")
            resalta(self, [trio[2]], factor=1.4)
            self.wait_until_bookmark("n")
            resalta(self, trio[:1], factor=1.4)
            self.wait_until_bookmark("t")
            resalta(self, trio[1:2], factor=1.4)
        
        with self.voiceover(text=tr("""No es una casualidad: se deduce de la definición. Para demostrarlo, <bookmark mark='l0'/> seleccionemos una componente cualquiera de la suma.""",
                                    """This is no coincidence: it follows from the definition. To prove it, <bookmark mark='l0'/> let us select any component of the sum.""")) as tracker:
            self.play(trio[0].animate.set_color(COLOR_A).scale(1/1.4), trio[1].animate.set_color(COLOR_B).scale(1/1.4),
                      trio[2].animate.set_color(WHITE).scale(1/1.4), run_time=0.4)
            self.wait_until_bookmark("l0")
            self.play(Write(l0), run_time=1)
        
        # v2: tirada A2 elegida por Marcos de oído (2026-11-18); la primera acababa en suspenso (F0 final ~126 Hz)
        with self.voiceover(text=tr("""Como da igual seleccionar primero la fila o la columna, <bookmark mark='l1'/> seleccionamos primero la columna.<bookmark mark='v2'/>""",
                                    """Since it does not matter whether we select the row or the column first, <bookmark mark='l1'/> we select the column first.""")) as tracker:
            # glifos: i | ( A + B ) | j (0-8)  ->  i | ( ( A + B ) | j ) (0-10): al seleccionar aparecen los paréntesis grandes
            nace(self, l0[0], pasos[0][1], [(0, 0), (1, 1), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)], aparecen=[2, 10],
                 con_igual=False, extra=[FadeIn(pasos[0][0])], marca="l1")
        self.wait(1.0)   # descanso tras la frase (Marcos, 2026-11-18)
        
        with self.voiceover(text=tr("""Por la definición de suma de matrices <bookmark mark='l2'/> podemos distribuir el selector de columnas.""",
                                    """By the definition of matrix addition <bookmark mark='l2'/> we can distribute the column selector.""")) as tracker:
            # -> i | ( A | j + B | j ) (0-10): el selector de columnas va a cada sumando; los paréntesis de la suma no aparecen
            nace(self, pasos[0][1], pasos[1][1], [(0, 0), (1, 1), (2, 2), (10, 10), (4, 3), (5, 6), (6, 7)],
                 [(8, 4), (9, 5), (8, 8), (9, 9)], con_igual=False, extra=[FadeIn(pasos[1][0])], marca="l2")
        
        with self.voiceover(text=tr("""Dentro de los paréntesis <bookmark mark='d'/> queda una suma de vectores, así que <bookmark mark='l3'/> por la definición de suma de vectores también podemos distribuir el selector de componentes.""",
                                    """Inside the parentheses <bookmark mark='d'/> there is now a sum of vectors, so <bookmark mark='l3'/> by the definition of vector addition we can distribute the component selector too.""")) as tracker:
            # «una suma de vectores»: A|j + B|j (glifos 3-9) se resalta en la línea de arriba; el paso entero (copia y viaje)
            # espera a la marca, para que la línea nueva no se lea a medias (auditoría 2026-11-19)
            suma_vec = pasos[1][1][3:10]
            self.wait_until_bookmark("d")
            resalta(self, [suma_vec], factor=1.08)
            self.wait_until_bookmark("l3")
            # -> i | ( A | j ) + i | ( B | j ) (0-14): el selector de componentes y los paréntesis van a cada sumando
            nace(self, pasos[1][1], pasos[2][1], [(3, 3), (4, 4), (5, 5), (6, 7), (7, 11), (8, 12), (9, 13)],
                 [(0, 0), (1, 1), (0, 8), (1, 9), (2, 2), (2, 10), (10, 6), (10, 14)], con_igual=False, extra=[FadeIn(pasos[2][0])])
            apaga(self, [suma_vec], factor=1.08)
        
        with self.voiceover(text=tr("""Y al quitar los paréntesis <bookmark mark='l4'/> queda la suma de las dos componentes.""",
                                    """And dropping the parentheses <bookmark mark='l4'/> leaves the sum of the two components.""")) as tracker:
            # -> i | A | j + i | B | j (0-10): todo baja a su sitio menos los paréntesis, que no aparecen
            nace(self, pasos[2][1], pasos[3][1], [(0, 0), (1, 1), (3, 2), (4, 3), (5, 4), (7, 5), (8, 6), (9, 7), (11, 8), (12, 9), (13, 10)],
                 con_igual=False, extra=[FadeIn(pasos[3][0])], t_fijos=1.2)
            self.remove(*pasos[3][1]); self.add(pasos[3])
        
        self.pausa()
        
        with self.voiceover(text=tr("""Con el producto por un escalar ocurre lo mismo, y se deduce del mismo modo. <bookmark mark='r'/> Así pues, las matrices también se suman y se multiplican por un escalar componente a componente.""",
                                    """The same happens with scalar multiplication, and it is deduced in the same way. <bookmark mark='r'/> So matrices are also added and multiplied by a scalar component-wise.""")) as tracker:
            # la cadena se recoge en su resultado (primer y último miembro) y debajo aparece el del producto
            self.remove(*[g for p in pasos[:3] for g in p[1]]); self.add(*pasos[:3])   # nacieron glifo a glifo
            self.play(*[FadeOut(p) for p in pasos[:3]], ReplacementTransform(l0, res_suma[0]),
                      ReplacementTransform(pasos[3][0], res_suma[1]), ReplacementTransform(pasos[3][1], res_suma[2]), run_time=1)
            self.play(Write(res_prod), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(conclusion), run_time=0.8)
        
        self.pausa_media()


class L01_V13_E04_NulaYOpuesta(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Matrices nulas y matriz opuesta", "Zero matrices and the opposite matrix"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        N = matriz([[0, 0, 0], [0, 0, 0]])
        nN = MathTex(r"\Mat{0}=", tex_template=myTemplate, font_size=48)
        VGroup(nN, N).arrange(RIGHT, buff=0.2).move_to([-3.6, 0.9, 0])
        def_nula = MathTex(DEF_MAT["nulo"], tex_template=myTemplate, font_size=48).move_to([-3.6, -1.9, 0])
        B, mB = matriz(B_EJ, COLOR_B), matriz(MENOSB_EJ)
        nB = MathTex(r"\Mat{B}=", tex_template=myTemplate, font_size=48).set_color(COLOR_B)
        nmB = MathTex(r"-\Mat{B}=", tex_template=myTemplate, font_size=48)
        VGroup(B, mB).arrange(DOWN, buff=0.45).move_to([3.7, 0.9, 0])
        nB.next_to(B, LEFT, buff=0.2); nmB.next_to(mB, LEFT, buff=0.2)
        def_opuesta = MathTex(DEF_MAT["opuesto"], tex_template=myTemplate, font_size=48).move_to([3.3, -1.9, 0])
        
        with self.voiceover(text=tr("""Nos faltan dos definiciones para enunciar las propiedades de la suma. <bookmark mark='n'/> Todas las componentes de las matrices nulas son cero, <bookmark mark='c'/> así que cada una de sus columnas es un vector nulo.""",
                                    """We still need two definitions to state the properties of addition. <bookmark mark='n'/> All the components of zero matrices are zero, <bookmark mark='c'/> so each of their columns is a zero vector.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("n")
            self.play(FadeIn(nN), FadeIn(N), run_time=0.8)
            self.wait_until_bookmark("c")
            marcos = marco(N.get_columns()[0])
            self.play(Create(marcos), Write(def_nula), run_time=0.8)
            for k in (1, 2):
                self.play(Transform(marcos, marco(N.get_columns()[k])), run_time=0.4)
            self.play(FadeOut(marcos), run_time=0.3)
        self.wait(0.8)   # respiro entre las dos definiciones (auditoría 2026-11-19)
        
        with self.voiceover(text=tr("""La matriz opuesta de una matriz se obtiene <bookmark mark='o'/> cambiando cada columna por su vector opuesto. <bookmark mark='e'/> La escribimos con un signo menos delante.""",
                                    """The opposite of a matrix is obtained <bookmark mark='o'/> by replacing each column with its opposite vector. <bookmark mark='e'/> We write it with a minus sign in front.""")) as tracker:
            self.play(FadeIn(nB), FadeIn(B), run_time=0.8)
            self.wait_until_bookmark("o")   # la fórmula se escribe con la frase que la describe (auditoría 2026-11-19)
            self.play(FadeIn(mB.get_brackets()), Write(def_opuesta), run_time=0.8)
            for k in range(3):
                self.play(TransformFromCopy(B.get_columns()[k], mB.get_columns()[k]), run_time=0.5)
            self.wait_until_bookmark("e")
            self.play(Write(nmB), run_time=0.8)
        self.wait(0.6)
        
        with self.voiceover(text=tr("""Con nuestra notación, <bookmark mark='p'/> la definición permite desplazar los paréntesis.""",
                                    """In our notation, <bookmark mark='p'/> the definition lets us move the parentheses.""")) as tracker:
            # como en la escena 2: los paréntesis viajan a la colocación de la derecha y vuelven; la escena 7 usa la definición
            # justo por eso. glifos: ( − A ) | j (0-5) = − ( A | j ) (7-12)
            par_op = [def_opuesta[0][0], def_opuesta[0][3], def_opuesta[0][8], def_opuesta[0][12]]
            self.wait_until_bookmark("p")
            resalta(self, par_op, factor=1.25)
            destino = def_opuesta[0][7:13].copy().move_to(def_opuesta[0][0:6])
            self.play(*[Transform(def_opuesta[0][i], destino[j], rate_func=rate_functions.there_and_back_with_pause)
                        for i, j in zip(range(6), [1, 0, 2, 5, 3, 4])], run_time=2.4)
            apaga(self, par_op, factor=1.25)
        
        self.pausa_media()


class L01_V13_E05_Definiciones(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Las mismas definiciones", "The same definitions"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        
        def columna(pares, x_igual):
            filas = VGroup(*[MathTex(i, "=", d, tex_template=myTemplate, font_size=42) for i, d in pares])
            for k, f in enumerate(filas):
                f.move_to([0, 1.2 - 1.05*k, 0])
                f.shift((x_igual - f[1].get_left()[0])*RIGHT)
            return filas
        
        vectores = columna([(i, d) for _, i, d, _ in DEFINICIONES], -4.4)
        matrices = columna([definicion_matrices(clave) for clave, *_ in DEFINICIONES], 2.2)
        r_vec = Tex(tr("Vectores", "Vectors"), font_size=38).set_color(GRAY_B).move_to([vectores.get_x(), 2.3, 0])
        r_mat = Tex("Matrices", font_size=38).set_color(GRAY_B).move_to([matrices.get_x(), 2.3, 0])
        
        with self.voiceover(text=tr("""Ya tenemos cuatro definiciones para las matrices: <bookmark mark='s'/> la suma, <bookmark mark='p'/> el producto por un escalar, <bookmark mark='n'/> las matrices nulas <bookmark mark='o'/> y la matriz opuesta.""",
                                    """We now have four definitions for matrices: <bookmark mark='s'/> addition, <bookmark mark='p'/> scalar multiplication, <bookmark mark='n'/> the zero matrices <bookmark mark='o'/> and the opposite matrix.""")) as tracker:
            self.play(Write(cabecera), FadeIn(r_mat), run_time=1)
            for k, marca in enumerate(["s", "p", "n", "o"]):
                self.wait_until_bookmark(marca)
                self.play(FadeIn(matrices[k]), run_time=0.5)
        
        with self.voiceover(text=tr("""Pongamos al lado las cuatro definiciones correspondientes para los vectores.""",
                                    """Let us put next to them the four corresponding definitions for vectors.""")) as tracker:
            self.play(FadeIn(r_vec), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(v) for v in vectores], lag_ratio=0.4), run_time=2)
        
        with self.voiceover(text=tr("""Son las mismas reglas. <bookmark mark='m'/> Donde había vectores, en minúscula, ahora hay matrices, en mayúscula. <bookmark mark='s'/> Y donde antes obteníamos un número, ahora obtenemos una columna.<bookmark mark='v3'/>""",   # «columna» (Marcos, 2026-11-18): es lo que da el selector; v3: tirada X1 elegida de oído (las otras dejaban «columna» en suspenso)
                                    """They are the same rules. <bookmark mark='m'/> Where there were vectors, in lower case, there are now matrices, in upper case. <bookmark mark='s'/> And where we obtained a number, we now obtain a column.""")) as tracker:
            izquierdos = [f[0] for f in vectores] + [f[0] for f in matrices]
            derechos = [f[2] for f in vectores] + [f[2] for f in matrices]
            self.wait_until_bookmark("m")
            resalta(self, izquierdos[:4], factor=1.12)
            self.wait(1.0)
            resalta(self, izquierdos[4:], factor=1.12)
            self.wait_until_bookmark("s")
            apaga(self, izquierdos, factor=1.12)
            resalta(self, derechos[:4], factor=1.12)
            self.wait(0.9)
            resalta(self, derechos[4:], factor=1.12)
            self.wait(1.2)
            apaga(self, derechos, factor=1.12)
        
        self.pausa_media()


class L01_V13_E06_Conmutativa(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La misma demostración", "The same proof"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self)
        enunciado = enunciado_traducible(1)
        cadena = coloca_cadena([linea(r"\elemRp{\Vect{a}+\Vect{b}}{i}"),
                                linea(r"=\eleVR{a}{i}+\eleVR{b}{i}"),
                                linea(r"=\eleVR{b}{i}+\eleVR{a}{i}", de_abajo=True),
                                linea(r"=\elemRp{\Vect{b}+\Vect{a}}{i}")])
        claves = [None, "suma", 1, "suma"]
        
        with self.voiceover(text=tr("""Con las cuatro definiciones de los vectores y con <bookmark mark='r'/> las propiedades de los números reales demostramos las propiedades de los vectores. <bookmark mark='e'/> Recordemos una de ellas: la propiedad conmutativa de la suma.<bookmark mark='v4'/>""",   # tirada C3 elegida por Marcos de oído (2026-11-18): «...es conmutativa» quedaba en suspenso
                                    """With the four definitions for vectors and <bookmark mark='r'/> the properties of the real numbers we proved the properties of vectors. <bookmark mark='e'/> Let us recall one of them: the commutative property of addition.""")) as tracker:
            self.play(Write(cabecera), FadeIn(panel.izq), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(panel.der), run_time=1)
            self.wait_until_bookmark("e")
            self.play(Write(enunciado), run_time=1.2)
        
        # «demostrarla» (Marcos, 2026-11-18): el antecedente es «la propiedad conmutativa». Partida en dos: la primera frase es
        # una toma nueva; el resto sale recortado de la toma anterior (tmp/parte_toma.py). La marca l1 estaba al principio del
        # resto: el paso se anima al empezar la segunda locución, sin esperar (una marca en la posición 0 se dispara al final).
        with self.voiceover(text=tr("""Para demostrarla, <bookmark mark='l0'/> seleccionamos una componente cualquiera.""",   # «cualquiera» (auditoría 2026-11-21): la conclusión ya no lo dice
                                    """To prove it, <bookmark mark='l0'/> we select any component.""")) as tracker:
            # glifos: ( a + b ) | i (0-6);  = a | i + b | i (0-7);  = ( b + a ) | i (0-7)
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=0.9)
        
        with self.voiceover(text=tr("""Por la definición de suma podemos distribuir el selector. <bookmark mark='l2'/> Los sumandos son números, así que <bookmark mark='c2'/> por la conmutativa podemos intercambiarlos. <bookmark mark='l3'/> Y por la definición de suma podemos sacar el selector como factor común.""",
                                    """By the definition of addition we can distribute the selector. <bookmark mark='l2'/> The terms are numbers, so <bookmark mark='c2'/> by the commutative property we can swap them. <bookmark mark='l3'/> And by the definition of addition we can factor out the selector.""")) as tracker:
            # cada línea nace de la anterior y cada uso se cuenta con la campanita, como en V06 (Marcos, 2026-11-10)
            # «Por la definición de suma...»: el selector va a cada sumando; los paréntesis no aparecen
            paso(self, panel, "suma", cadena[0], cadena[1], [(1, 1), (2, 4), (3, 5)], [(5, 2), (6, 3), (5, 6), (6, 7)])
            self.wait_until_bookmark("l2")   # «los sumandos son números»
            sumandos = [cadena[1][0][1:4], cadena[1][0][5:8]]
            self.play(*[Indicate(g, color=COLOR_REGLA, scale_factor=1.2) for g in sumandos], run_time=0.9)
            self.wait_until_bookmark("c2")   # los dos sumandos se cruzan
            paso(self, panel, 1, cadena[1], cadena[2], [(4, 4)], [(1, 5), (2, 6), (3, 7), (5, 1), (6, 2), (7, 3)])
            self.wait_until_bookmark("l3")   # los dos selectores se reúnen en uno, fuera de los paréntesis nuevos
            paso(self, panel, "suma", cadena[2], cadena[3], [(1, 2), (4, 3), (5, 4)], [(2, 6), (3, 7), (6, 6), (7, 7)], aparecen=[1, 5])
        
        # la conclusión dice el criterio de igualdad (Marcos, 2026-11-20, como en V14): son iguales porque lo son componente a
        # componente; la locución anterior conserva su toma, recortada antes de la conclusión (tmp/parte_toma.py)
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> los dos vectores son iguales, porque lo son <bookmark mark='c'/> componente a componente.""",
                                    """So <bookmark mark='ok'/> the two vectors are equal, because they are equal <bookmark mark='c'/> component by component.""")) as tracker:
            self.wait_until_bookmark("ok")
            self.play(Indicate(cadena[0], color=COLOR_ESCALAR, scale_factor=1.1), Indicate(cadena[3], color=COLOR_ESCALAR, scale_factor=1.1),
                      Indicate(enunciado, color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.5)
            self.wait_until_bookmark("c")
            senala_selector(self, [cadena[0], cadena[3]], color=COLOR_ESCALAR)   # el selector de componentes, a los dos extremos
        
        self.pausa()
        
        with self.voiceover(text=tr("""Ahora cambiemos los símbolos. <bookmark mark='m'/> Donde había vectores, ponemos matrices. <bookmark mark='c'/> Donde se seleccionaba una componente, se selecciona una columna. <bookmark mark='v'/> Y a la derecha, en lugar de las propiedades de los números, <bookmark mark='w'/> ponemos las de los vectores, que ya están demostradas: son las mismas, <bookmark mark='b'/> con las letras en negrita.""",
                                    """Now let us change the symbols. <bookmark mark='m'/> Where there were vectors, we put matrices. <bookmark mark='c'/> Where a component was selected, a column is selected. <bookmark mark='v'/> And on the right, instead of the properties of numbers, <bookmark mark='w'/> we put those of vectors, which are already proved: they are the same, <bookmark mark='b'/> with the letters in bold.""")) as tracker:
            for k, marca in enumerate(["m", "c"], start=1):
                self.wait_until_bookmark(marca)
                self.play(*cambio_de_simbolos(k, panel, enunciado, cadena), run_time=1.5)
            # tercera etapa (auditoría 2026-11-19): en «Y a la derecha» se señalan las propiedades de los números; el cambio
            # llega en «ponemos las de los vectores», y las letras en negrita se señalan al nombrarlas
            lado_der = [panel.piezas[k] for k in (1, 2, 3, 4)]
            self.wait_until_bookmark("v")
            self.play(*[Indicate(x, color=COLOR_ESCALAR, scale_factor=1.08) for x in lado_der], run_time=1.0)
            self.wait_until_bookmark("w")
            self.play(*cambio_de_simbolos(3, panel, enunciado, cadena), run_time=1.5)
            self.wait_until_bookmark("b")
            self.play(*[Indicate(x[1] if len(x) > 1 else x, color=COLOR_ESCALAR, scale_factor=1.12) for x in lado_der], run_time=1.2)
        
        self.pausa()
        panel.reinicia()   # los usos se cuentan de nuevo al releer la demostración, ya para matrices
        
        with self.voiceover(text=tr("""Leamos de nuevo la demostración. <bookmark mark='l0'/> Seleccionamos una columna. <bookmark mark='l1'/> Por la definición de suma de matrices podemos distribuir el selector. <bookmark mark='l2'/> Los sumandos son vectores, así que <bookmark mark='c2'/> por la conmutativa de los vectores podemos intercambiarlos. <bookmark mark='l3'/> Y por la definición de suma podemos sacar el selector como factor común.""",
                                    """Let us read the proof again. <bookmark mark='l0'/> We select a column. <bookmark mark='l1'/> By the definition of matrix addition we can distribute the selector. <bookmark mark='l2'/> The terms are vectors, so <bookmark mark='c2'/> by the commutative property of vectors we can swap them. <bookmark mark='l3'/> And by the definition of addition we can factor out the selector.""")) as tracker:
            # en la relectura cada paso se vuelve a animar como en la primera lectura (Marcos, 2026-11-18): las líneas 1-3
            # se retiran y vuelven a nacer de la anterior, ya con matrices (los glifos son los mismos en todas las versiones)
            fantasmas = [c.copy() for c in cadena[1:]]
            self.remove(*cadena[1:]); self.add(*fantasmas)
            self.play(*[FadeOut(f) for f in fantasmas], run_time=0.6)
            self.wait_until_bookmark("l0")
            self.play(Indicate(cadena[0], color=COLOR_ESCALAR, scale_factor=1.1), run_time=1.0)
            self.wait_until_bookmark("l1")   # el selector va a cada sumando
            paso(self, panel, "suma", cadena[0], cadena[1], [(1, 1), (2, 4), (3, 5)], [(5, 2), (6, 3), (5, 6), (6, 7)])
            self.wait_until_bookmark("l2")   # «los sumandos son vectores», como en la primera lectura (auditoría 2026-11-19)
            sumandos = [cadena[1][0][1:4], cadena[1][0][5:8]]
            self.play(*[Indicate(g, color=COLOR_REGLA, scale_factor=1.2) for g in sumandos], run_time=0.9)
            self.wait_until_bookmark("c2")   # los dos sumandos (vectores) se cruzan
            paso(self, panel, 1, cadena[1], cadena[2], [(4, 4)], [(1, 5), (2, 6), (3, 7), (5, 1), (6, 2), (7, 3)])
            self.wait_until_bookmark("l3")   # los dos selectores se reúnen en uno
            paso(self, panel, "suma", cadena[2], cadena[3], [(1, 2), (4, 3), (5, 4)], [(2, 6), (3, 7), (6, 6), (7, 7)], aparecen=[1, 5])
        
        self.wait(0.4)   # el punto entre el último paso y la conclusión (auditoría 2026-11-21)
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> las dos matrices son iguales, porque lo son <bookmark mark='c'/> columna a columna. La suma de matrices es conmutativa. No hemos tenido que cambiar ningún paso.""",
                                    """So <bookmark mark='ok'/> the two matrices are equal, because they are equal <bookmark mark='c'/> column by column. Matrix addition is commutative. We did not have to change a single step.""")) as tracker:
            self.wait_until_bookmark("ok")
            caja = SurroundingRectangle(enunciado, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
            self.play(Create(caja), Indicate(enunciado, color=COLOR_RESULTADO, scale_factor=1.15), run_time=1.5)
            self.wait_until_bookmark("c")
            senala_selector(self, [cadena[0], cadena[3]])   # el selector de columnas, a los dos extremos
        
        self.pausa_media()


class L01_V13_E07_Opuesta(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Otra demostración que ya está hecha", "Another proof that is already done"), font_size=36).set_color(COLOR_TITULO).to_edge(UP, buff=0.25)
        panel = Panel(self)
        enunciado = enunciado_traducible(4)
        cadena = coloca_cadena([linea(r"\elemR{\big(\Vect{a}+(-\Vect{a})\big)}{i}"),
                                linea(r"=\eleVR{a}{i}+\elemRp{-\Vect{a}}{i}"),
                                linea(r"=\eleVR{a}{i}+\big(-\eleVRpE{a}{i}\big)"),
                                linea(r"=0", de_abajo=True, final=r"=\Vect{0}"),
                                linea(r"=\eleVR{0}{i}")])
        claves = [None, "suma", "opuesto", 4, "nulo"]
        idea = aviso("idea", tr("Mismas reglas, mismas demostraciones", "Same rules, same proofs"), font_size=34).to_edge(DOWN, buff=0.3)
        
        with self.voiceover(text=tr("""Hagamos lo mismo con otra propiedad de los vectores: sumar un vector y su opuesto da un vector nulo.""",
                                    """Let us do the same with another property of vectors: adding a vector and its opposite gives a zero vector.""")) as tracker:
            self.play(Write(cabecera), FadeIn(panel.todo), run_time=1)
            self.play(Write(enunciado), FadeIn(cadena[0]), run_time=1.2)
        
        with self.voiceover(text=tr("""En su demostración <bookmark mark='l1'/> distribuimos el selector y <bookmark mark='l2'/> desplazamos los paréntesis por la definición de opuesto. <bookmark mark='l3'/> Sumar un número y su opuesto da cero, <bookmark mark='l4'/> y el cero es una componente de un vector nulo.""",
                                    """In its proof <bookmark mark='l1'/> we distribute the selector and <bookmark mark='l2'/> move the parentheses by the definition of opposite. <bookmark mark='l3'/> Adding a number and its opposite gives zero, <bookmark mark='l4'/> and zero is a component of a zero vector.""")) as tracker:
            # glifos: ( a + ( - a ) ) | i (0-9);  = a | i + ( - a ) | i (0-10);  = a | i + ( - ( a | i ) ) (0-12);  = 0;  = 0 | i
            rapido = dict(t_fijos=0.5, t_moviles=0.6, t_cuenta=0.35)
            self.wait_until_bookmark("l1")   # el selector va a cada sumando; los paréntesis grandes no aparecen
            paso(self, panel, "suma", cadena[0], cadena[1], [(1, 1), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8)],
                 [(8, 2), (9, 3), (8, 9), (9, 10)], **rapido)
            self.wait_until_bookmark("l2")   # los paréntesis pasan a rodear la componente; el sumando entero, entre paréntesis nuevos
            paso(self, panel, "opuesto", cadena[1], cadena[2], [(1, 1), (2, 2), (3, 3), (4, 4), (6, 6), (7, 8), (9, 9), (10, 10)],
                 [(5, 7), (8, 11)], aparecen=[5, 12], **rapido)
            self.wait_until_bookmark("l3")   # toda la suma se convierte en el cero
            paso(self, panel, 4, cadena[2], cadena[3], [], [(slice(1, 13), 1)], t_fijos=0.4, t_moviles=0.7, t_cuenta=0.35)
            self.wait_until_bookmark("l4")   # al cero le sale el selector
            paso(self, panel, "nulo", cadena[3], cadena[4], [(1, 1)], aparecen=[2, 3], **rapido)
        
        self.pausa()
        
        with self.voiceover(text=tr("""Hacemos el mismo cambio de símbolos.""",
                                    """We make the same change of symbols.""")) as tracker:
            for k in (1, 2, 3):
                self.play(*cambio_de_simbolos(k, panel, enunciado, cadena), run_time=0.9)
            panel.reinicia(run_time=0.4)
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Ahora la demostración dice que <bookmark mark='l1'/> distribuimos el selector y <bookmark mark='l2'/> desplazamos los paréntesis por la definición de matriz opuesta. <bookmark mark='l3'/> Sumar un vector y su opuesto da un vector nulo, <bookmark mark='l4'/> y ese vector nulo es una columna de una matriz nula.""",
                                    """Now the proof says that <bookmark mark='l1'/> we distribute the selector and <bookmark mark='l2'/> move the parentheses by the definition of the opposite matrix. <bookmark mark='l3'/> Adding a vector and its opposite gives a zero vector, <bookmark mark='l4'/> and that zero vector is a column of a zero matrix.""")) as tracker:
            # cada paso se vuelve a animar, ya con matrices (como la relectura de la escena 6; auditoría 2026-11-19): se ve
            # qué se convierte en qué, también el vector nulo que pasa a ser columna de una matriz nula
            fantasmas = [c.copy() for c in cadena[1:]]
            self.remove(*cadena[1:]); self.add(*fantasmas)
            self.play(*[FadeOut(f) for f in fantasmas], run_time=0.5)
            self.wait_until_bookmark("l1")
            paso(self, panel, "suma", cadena[0], cadena[1], [(1, 1), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8)],
                 [(8, 2), (9, 3), (8, 9), (9, 10)], **rapido)
            self.wait_until_bookmark("l2")
            paso(self, panel, "opuesto", cadena[1], cadena[2], [(1, 1), (2, 2), (3, 3), (4, 4), (6, 6), (7, 8), (9, 9), (10, 10)],
                 [(5, 7), (8, 11)], aparecen=[5, 12], **rapido)
            self.wait_until_bookmark("l3")
            paso(self, panel, 4, cadena[2], cadena[3], [], [(slice(1, 13), 1)], t_fijos=0.4, t_moviles=0.7, t_cuenta=0.35)
            self.wait_until_bookmark("l4")
            paso(self, panel, "nulo", cadena[3], cadena[4], [(1, 1)], aparecen=[2, 3], **rapido)
        
        self.wait(0.4)   # el punto entre el último paso y la conclusión (auditoría 2026-11-21)
        with self.voiceover(text=tr("""Así pues, <bookmark mark='ok'/> las dos matrices son iguales, porque lo son <bookmark mark='c'/> columna a columna. Sumar una matriz y su opuesta da una matriz nula.""",
                                    """So <bookmark mark='ok'/> the two matrices are equal, because they are equal <bookmark mark='c'/> column by column. Adding a matrix and its opposite gives a zero matrix.""")) as tracker:
            self.wait_until_bookmark("ok")
            caja = SurroundingRectangle(enunciado, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)
            self.play(Create(caja), Indicate(enunciado, color=COLOR_RESULTADO, scale_factor=1.15), run_time=1.5)
            self.wait_until_bookmark("c")
            senala_selector(self, [cadena[0], cadena[4]])   # el selector de columnas, a los dos extremos
        
        self.pausa()
        
        with self.voiceover(text=tr("""Esta es la gran ventaja del álgebra. <bookmark mark='i'/> Las demostraciones solo han usado reglas para manipular símbolos, así que no importa si los símbolos representan vectores o matrices. Si unos objetos nuevos cumplen las mismas reglas, las demostraciones de sus propiedades ya están hechas.""",
                                    """This is the great advantage of algebra. <bookmark mark='i'/> The proofs have only used rules for manipulating symbols, so it does not matter whether the symbols stand for vectors or matrices. If new objects obey the same rules, the proofs of their properties are already done.""")) as tracker:
            self.wait_until_bookmark("i")
            self.play(FadeIn(idea, scale=0.9), run_time=0.8)
        
        self.pausa_media()


class L01_V13_E08_OchoPropiedades(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Las ocho propiedades", "The eight properties"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        
        def tabla(props, x):
            filas = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=34) for k, p in enumerate(props)])
            filas.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
            return filas.move_to([x, 0.05, 0])
        
        vectores, matrices = tabla(PROPIEDADES_VECTORES, -3.4), tabla(PROPIEDADES_MATRICES, 3.4)
        for v, m in zip(vectores, matrices):
            m.set_y(v.get_y())
        r_vec = Tex(tr("Vectores", "Vectors"), font_size=36).set_color(GRAY_B).next_to(vectores, UP, buff=0.3)
        r_mat = Tex("Matrices", font_size=36).set_color(GRAY_B).next_to(matrices, UP, buff=0.3)
        r_mat.set_y(r_vec.get_y())
        nota = Tex(tr("(demostradas en los vídeos 1.6 y 1.7)", "(proved in videos 1.6 and 1.7)"), font_size=28).set_color(GRAY_A).next_to(vectores, DOWN, buff=0.25).align_to(vectores, LEFT)
        
        with self.voiceover(text=tr("""Las operaciones con vectores cumplen ocho propiedades: <bookmark mark='s'/> cuatro de la suma <bookmark mark='p'/> y cuatro del producto por escalares.""",
                                    """Vector operations satisfy eight properties: <bookmark mark='s'/> four for addition <bookmark mark='p'/> and four for scalar multiplication.""")) as tracker:
            self.play(Write(cabecera), FadeIn(r_vec), FadeIn(nota), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(vectores[:4]), run_time=0.8)
            self.wait_until_bookmark("p")
            self.play(FadeIn(vectores[4:]), run_time=0.8)
        
        with self.voiceover(text=tr("""Con el mismo cambio de símbolos, <bookmark mark='m'/> las operaciones con matrices cumplen las mismas ocho.""",
                                    """With the same change of symbols, <bookmark mark='m'/> matrix operations satisfy the same eight.""")) as tracker:
            self.wait_until_bookmark("m")
            self.play(FadeIn(r_mat), *[TransformFromCopy(v, m) for v, m in zip(vectores, matrices)], run_time=2)
        
        self.pausa_para_pensar(invitacion=tr("Pause el vídeo y demuestre otra propiedad de la suma.", "Pause the video and prove another property of addition."),
                               invitacion_voz=tr("Para convencerse, pause el vídeo e intente demostrar otra de las propiedades de la suma: escriba la demostración para vectores y cambie los símbolos.",
                                                 "To convince yourself, pause the video and try to prove another of the properties of addition: write down the proof for vectors and change the symbols."),
                               al_invitar=lambda: self.play(   # las que quedan son la 2 y la 3; la 1 y la 4 ya están hechas (auditoría 2026-11-19)
                                   FadeOut(nota),   # la tarjeta la tapaba a medias (auditoría 2026-11-21)
                                   *[Create(marco(t[k], COLOR_ESCALAR)) for t in (vectores, matrices) for k in (1, 2)],
                                   *[t[k].animate.set_opacity(0.35) for t in (vectores, matrices) for k in (0, 3)], run_time=0.8))
        
        self.pausa()


class L01_V13_E09_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        formulas = [DEF_MAT["suma"] + r"\qquad\quad " + DEF_MAT["producto"],
                    r"\elemLR{(\Mat{A}+\Mat{B})}{i}{j}=\eleM{A}{i}{j}+\eleM{B}{i}{j}\qquad\quad \elemLR{(\lambda\Mat{A})}{i}{j}=\lambda\big(\eleM{A}{i}{j}\big)",
                    r"\Mat{A}+\Mat{B}=\Mat{B}+\Mat{A},\quad\ldots,\quad 1\Mat{A}=\Mat{A}"]
        rotulos = [tr("suma y producto por un escalar: columna a columna", "addition and scalar multiplication: column by column"),
                   tr("y por tanto, componente a componente", "and therefore, component-wise"),
                   tr(r"las mismas ocho propiedades que los vectores,\\ y se demuestran del mismo modo", "the same eight properties as vectors, proved in the same way")]
        filas = VGroup(*[VGroup(MathTex(f, tex_template=myTemplate, font_size=40), Tex(r, tex_template=myTemplate, font_size=32, color=GRAY_A)).arrange(DOWN, buff=0.18)
                         for f, r in zip(formulas, rotulos)]).arrange(DOWN, buff=0.45).move_to([0, 0.35, 0])
        idea = aviso("idea", tr("Las demostraciones solo usan reglas para manipular símbolos", "Proofs only use rules for manipulating symbols"), font_size=32).to_edge(DOWN, buff=0.45)
        
        with self.voiceover(text=tr("""Resumamos. Las matrices se suman y se multiplican por un escalar columna a columna, <bookmark mark='c'/> y por tanto también componente a componente.""",
                                    """Let us sum up. Matrices are added and multiplied by a scalar column by column, <bookmark mark='c'/> and therefore also component-wise.""")) as tracker:
            self.play(Write(cabecera), FadeIn(filas[0]), run_time=1)
            self.wait_until_bookmark("c")
            self.play(FadeIn(filas[1]), run_time=0.8)
        
        with self.voiceover(text=tr("""Estas operaciones cumplen las mismas ocho propiedades que las operaciones con vectores.""",
                                    """These operations satisfy the same eight properties as vector operations.""")) as tracker:
            self.play(FadeIn(filas[2]), run_time=0.8)
        
        with self.voiceover(text=tr("""En vídeos anteriores usamos dibujos para entender las operaciones con números y con vectores. Aquí no ha hecho falta ninguno: <bookmark mark='i'/> las demostraciones solo usan reglas para manipular símbolos, y las matrices cumplen las mismas reglas que los vectores.""",
                                    """In earlier videos we used drawings to understand the operations with numbers and with vectors. Here we have not needed any: <bookmark mark='i'/> the proofs only use rules for manipulating symbols, and matrices obey the same rules as vectors.""")) as tracker:
            self.wait_until_bookmark("i")
            self.play(FadeIn(idea, scale=0.9), run_time=0.8)
        
        self.wait(1.0)
        with self.voiceover(text=tr("""En este vídeo hemos visto que con las matrices podemos operar <bookmark mark='c'/> columna a columna, <bookmark mark='k'/> o componente a componente.""",
                                    """In this video we have seen that we can operate with matrices <bookmark mark='c'/> column by column, <bookmark mark='k'/> or component by component.""")) as tracker:
            self.wait_until_bookmark("c")
            self.play(Indicate(filas[0][1], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1.0)
            self.wait_until_bookmark("k")
            self.play(Indicate(filas[1][1], color=COLOR_ESCALAR, scale_factor=1.15), run_time=1.0)
        
        with self.voiceover(text=tr("""En el próximo vídeo veremos que las mismas operaciones, la suma y el producto por un escalar, también se pueden hacer fila a fila. Y veremos lo que ocurre al transponer una suma o un producto por un escalar.""",
                                    """In the next video we will see that the same operations, addition and scalar multiplication, can also be done row by row. And we will see what happens when we transpose a sum or a product by a scalar.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
