from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("El escalar a la derecha", "The scalar on the right")

COLOR_SELECTOR = GREEN     # el selector, en verde; el escalar, en amarillo (COLOR_ESCALAR)

# Las reglas del vídeo: (lado izquierdo, lado derecho)
DER_VEC  = (r"\elemRp{\lambda\Vect{b}}{i}", r"\lambda\eleVRpE{b}{i}")      # ( λ b ) | i  =  λ ( b | i )
IZQ_VEC  = (r"\elemLp{\lambda\Vect{b}}{i}", r"\lambda\eleVLPE{b}{i}")      # i | ( λ b )  =  λ ( i | b )
IZQ_VEC2 = (r"\elemLp{\Vect{b}\lambda}{i}", r"\eleVLPE{b}{i}\lambda")      # i | ( b λ )  =  ( i | b ) λ
FIL_MAT  = (r"\elemLp{\Mat{A}\lambda}{i}", r"\VectFpE{A}{i}\lambda")       # i | ( A λ )  =  ( i | A ) λ
COL_MAT  = (r"\elemRp{\lambda\Mat{A}}{j}", r"\lambda\VectCpE{A}{j}")       # ( λ A ) | j  =  λ ( A | j )
TRA_MAT  = (r"\Transp{\Mat{A}\lambda}", r"\MatTpE{A}\lambda")              # ( A λ ) T  =  ( A T ) λ


def regla(par, font_size=48):
    return MathTex(par[0], "=", par[1], tex_template=myTemplate, font_size=font_size)


def fila_vec(fila):
    """Un vector numérico escrito en horizontal, entre paréntesis y con la coma final del libro."""
    return "(" + r",\;".join(str(x) for x in fila) + ",)"


def resalta(escena, mobs, color=COLOR_ESCALAR, factor=1.3, run_time=0.3):
    """Resaltado inmediato y sostenido (color y tamaño), sin la subida lenta de Indicate."""
    escena.play(*[x.animate.set_color(color).scale(factor) for x in mobs], run_time=run_time)


def apaga(escena, mobs, color=WHITE, factor=1.3, run_time=0.3):
    escena.play(*[x.animate.set_color(color).scale(1/factor) for x in mobs], run_time=run_time)


def viaje(escena, formula, mapa, run_time=2.4):
    """Los glifos del lado izquierdo de la regla viajan a la colocación del derecho y vuelven (V10, V13):
    mapa[i] es el glifo del lado derecho al que va el glifo i del izquierdo."""
    destino = formula[2].copy().move_to(formula[0])
    escena.play(*[Transform(formula[0][i], destino[j], rate_func=rate_functions.there_and_back_with_pause)
                  for i, j in enumerate(mapa)], run_time=run_time)


def rotulo(texto, junto_a, x, font_size=28):
    """Rótulo gris pequeño a la derecha de una línea (lo que justifica el paso)."""
    r = Tex(texto, tex_template=myTemplate, font_size=font_size, color=GRAY_B).next_to(junto_a, RIGHT, buff=0.6)
    return r.shift((x - r.get_left()[0])*RIGHT)


def nace(escena, origen, destino, fijos, moviles=(), aparecen=(), con_igual=True, extra=(), marca=None,
         t_fijos=0.8, t_moviles=0.9):
    """Una expresión nace de la anterior (CLAUDE.md, «Cada expresión nace de la anterior»). Primero, mientras la
    voz nombra la regla, se copia lo que no cambia (fijos: parejas glifo de origen, glifo de destino) y aparece el
    igual; después (en la marca, si se da) viaja lo que el paso mueve (moviles) y surge lo nuevo (aparecen)."""
    cubiertos = sorted({j for _, j in fijos} | {j for _, j in moviles} | set(aparecen) | ({0} if con_igual else set()))
    assert cubiertos == list(range(len(destino))), (cubiertos, len(destino))
    escena.play(*extra, *([FadeIn(destino[0])] if con_igual else []),
                *[TransformFromCopy(origen[i], destino[j]) for i, j in fijos], run_time=t_fijos)
    if marca is not None:
        escena.wait_until_bookmark(marca)
    if moviles or aparecen:
        escena.play(*[TransformFromCopy(origen[i], destino[j]) for i, j in moviles],
                    *[FadeIn(destino[j]) for j in aparecen], run_time=t_moviles)


def entera(escena, linea):
    """Tras nacer glifo a glifo, la línea vuelve a estar en la escena como un solo objeto."""
    escena.remove(*linea[0]); escena.add(linea)

class L01_V15_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class L01_V15_E01_Problema(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        der = regla(DER_VEC).move_to([0, 1.2, 0])
        izq = regla(IZQ_VEC).move_to([0, -1.2, 0])
        r_der = Tex(tr("selector a la derecha: basta desplazar los paréntesis", "selector on the right: moving the parentheses is enough"),
                    font_size=30, color=GRAY_B).next_to(der, DOWN, buff=0.35)
        r_izq = Tex(tr("selector a la izquierda: el escalar y el selector se cruzan", "selector on the left: the scalar and the selector cross"),
                    font_size=30, color=GRAY_B).next_to(izq, DOWN, buff=0.35)
        # glifos de izq: i | ( λ b ) (0-5)  =  λ ( i | b ) (0-5)
        sel = [izq[0][0:2], izq[2][2:4]]
        esc = [izq[0][3], izq[2][0]]
        
        with self.voiceover(text=tr("""En este vídeo veremos una última extensión de la notación: escribir el escalar a la derecha de un vector o de una matriz.""",
                                    """In this video we will see one last extension of the notation: writing the scalar on the right of a vector or a matrix.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        with self.voiceover(text=tr("""Cuando el selector actúa por la derecha de un vector, la definición de producto por un escalar permite <bookmark mark='p'/> desplazar los paréntesis. Los símbolos no cambian de orden.""",
                                    """When the selector acts on the right of a vector, the definition of the product by a scalar lets us <bookmark mark='p'/> move the parentheses. The symbols do not change their order.""")) as tracker:
            self.play(FadeIn(der), run_time=0.8)
            self.wait_until_bookmark("p")
            parentesis = [der[0][0], der[0][3], der[2][1], der[2][5]]
            resalta(self, parentesis, factor=1.25)
            viaje(self, der, [1, 0, 2, 5, 3, 4])
            apaga(self, parentesis, factor=1.25)
            self.play(FadeIn(r_der), run_time=0.5)
        
        with self.voiceover(text=tr("""El selector también puede actuar por la izquierda, con el mismo resultado. <bookmark mark='x'/> Pero entonces, al sacar el escalar, <bookmark mark='c'/> el escalar y el selector intercambian sus posiciones. Ya no basta con desplazar los paréntesis.""",
                                    """The selector can also act on the left, with the same result. <bookmark mark='x'/> But then, when we take the scalar out, <bookmark mark='c'/> the scalar and the selector swap their positions. Moving the parentheses is no longer enough.""")) as tracker:
            self.play(FadeIn(izq[0]), run_time=0.8)
            self.wait_until_bookmark("x")
            self.play(FadeIn(izq[1]), FadeIn(izq[2]), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(*[x.animate.set_color(COLOR_SELECTOR).scale(1.2) for x in sel], *[x.animate.set_color(COLOR_ESCALAR).scale(1.2) for x in esc], run_time=0.4)
            self.play(FadeIn(r_izq), run_time=0.5)
        
        self.pausa_media()


class L01_V15_E02_Convenio(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Un convenio de notación", "A notational convention"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        convenio = MathTex(r"\Vect{b}\lambda", "=", r"\lambda\Vect{b}", tex_template=myTemplate, font_size=60).move_to([0, 1.3, 0])
        caja = SurroundingRectangle(convenio, color=COLOR_ESCALAR, buff=0.25, corner_radius=0.15, stroke_width=3)
        ejemplo = MathTex(fila_vec([1, 2, 3]), "2", "=", "2", fila_vec([1, 2, 3]), "=", fila_vec([2, 4, 6]), tex_template=myTemplate, font_size=44).move_to([0, -0.7, 0])
        ejemplo[1].set_color(COLOR_ESCALAR); ejemplo[3].set_color(COLOR_ESCALAR)
        habitual = Tex(tr(r"Lo habitual es escribir el escalar primero: $2\Vect{b}$", r"The usual way is to write the scalar first: $2\Vect{b}$"),
                       tex_template=myTemplate, font_size=32, color=GRAY_B).move_to([0, -2.3, 0])
        
        with self.voiceover(text=tr("""Para recuperar esa regla adoptamos un convenio: <bookmark mark='c'/> aceptamos escribir el escalar a la derecha del vector. Por definición, significa lo mismo que con el escalar a la izquierda.""",
                                    """To recover that rule we adopt a convention: <bookmark mark='c'/> we accept writing the scalar on the right of the vector. By definition, it means the same as with the scalar on the left.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("c")
            self.play(FadeIn(convenio[0]), run_time=0.8)
            self.wait(1.5)
            self.play(FadeIn(convenio[1]), FadeIn(convenio[2]), Create(caja), run_time=1)
        
        with self.voiceover(text=tr("""En este ejemplo, <bookmark mark='e'/> el vector por dos es lo mismo que dos por el vector.""",
                                    """In this example, <bookmark mark='e'/> the vector times two is the same as two times the vector.""")) as tracker:
            self.wait_until_bookmark("e")
            self.play(FadeIn(ejemplo[0:2]), run_time=0.6)
            self.play(FadeIn(ejemplo[2:]), run_time=0.8)
        
        with self.voiceover(text=tr("""No es una operación nueva, sino otra manera de escribir el mismo producto. <bookmark mark='h'/> Lo habitual es escribir el escalar primero. Aquí lo escribiremos a la derecha solo cuando convenga a la notación.""",
                                    """It is not a new operation, but another way of writing the same product. <bookmark mark='h'/> The usual way is to write the scalar first. Here we will write it on the right only when it suits the notation.""")) as tracker:
            self.wait_until_bookmark("h")
            self.play(FadeIn(habitual), run_time=0.8)
        
        self.pausa_media()


class L01_V15_E03_Comprobacion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Con el escalar a la derecha", "With the scalar on the right"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        # Glifos: i | ( b λ ) (0-5);  = i | ( λ b ) (0-6);  = λ ( i | b ) (0-6);  = ( i | b ) λ (0-6)
        cadena = [MathTex(f, tex_template=myTemplate, font_size=48) for f in
                  (IZQ_VEC2[0], "=" + IZQ_VEC[0], "=" + IZQ_VEC[1], "=" + IZQ_VEC2[1])]
        for k, l in enumerate(cadena):
            l.move_to([0, 1.7 - 0.95*k, 0]).align_to([-3.6 + (0.7 if k else 0), 0, 0], LEFT)
        rotulos = [rotulo(t, l, 0.6) for t, l in zip([tr("el convenio", "the convention"),
                                                      tr("el selector deja fuera al escalar", "the selector leaves the scalar outside"),
                                                      tr("producto de dos números", "product of two numbers")], cadena[1:])]
        final = regla(IZQ_VEC2, 52).move_to([0, -2.6, 0])
        
        with self.voiceover(text=tr("""Vamos a demostrar que funciona. <bookmark mark='l0'/> Seleccionamos por la izquierda una componente del producto, escrito con el escalar a la derecha.""",
                                    """Let us prove that it works. <bookmark mark='l0'/> We select, on the left, a component of the product, written with the scalar on the right.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        
        with self.voiceover(text=tr("""Por el convenio, <bookmark mark='x'/> podemos escribir el escalar a la izquierda.""",
                                    """By the convention, <bookmark mark='x'/> we can write the scalar on the left.""")) as tracker:
            # el vector y el escalar se cruzan dentro de los paréntesis
            nace(self, cadena[0][0], cadena[1][0], [(0, 1), (1, 2), (2, 3), (5, 6)], [(3, 5), (4, 4)], extra=[FadeIn(rotulos[0])], marca="x")
            entera(self, cadena[1])
        
        with self.voiceover(text=tr("""El selector actúa igual por los dos lados del vector, así que <bookmark mark='x'/> también deja fuera al escalar.""",
                                    """The selector acts in the same way on both sides of the vector, so <bookmark mark='x'/> it also leaves the scalar outside.""")) as tracker:
            nace(self, cadena[1][0], cadena[2][0], [(5, 5), (6, 6)], [(4, 1), (1, 3), (2, 4), (3, 2)], extra=[FadeIn(rotulos[1])], marca="x")
            entera(self, cadena[2])
        
        with self.voiceover(text=tr("""Lo que queda es un producto de dos números, así que <bookmark mark='x'/> podemos cambiarlos de orden.""",
                                    """What remains is a product of two numbers, so <bookmark mark='x'/> we can change their order.""")) as tracker:
            nace(self, cadena[2][0], cadena[3][0], [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)], [(1, 6)], extra=[FadeIn(rotulos[2])], marca="x")
            entera(self, cadena[3])
        
        self.pausa_corta()
        
        with self.voiceover(text=tr("""Reunamos los dos extremos de la cadena. <bookmark mark='p'/> Con el escalar a la derecha, vuelve a bastar con desplazar los paréntesis.""",
                                    """Let us put the two ends of the chain together. <bookmark mark='p'/> With the scalar on the right, moving the parentheses is enough again.""")) as tracker:
            self.play(TransformFromCopy(cadena[0][0], final[0]), FadeIn(final[1]), TransformFromCopy(cadena[3][0][1:], final[2]), run_time=1.2)
            self.wait_until_bookmark("p")
            # glifos: i | ( b λ ) (0-5)  ->  ( i | b ) λ (0-5)
            parentesis = [final[0][2], final[0][5], final[2][0], final[2][4]]
            resalta(self, parentesis, factor=1.25)
            viaje(self, final, [1, 2, 0, 3, 5, 4])
            apaga(self, parentesis, factor=1.25)
        
        self.pausa_media()


class L01_V15_E04_Matrices(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Lo mismo con matrices", "The same with matrices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        convenio = MathTex(r"\Mat{A}\lambda", "=", r"\lambda\Mat{A}", tex_template=myTemplate, font_size=56).move_to([0, 1.9, 0])
        caja = SurroundingRectangle(convenio, color=COLOR_ESCALAR, buff=0.22, corner_radius=0.15, stroke_width=3)
        filas = regla(FIL_MAT).move_to([0, 0.2, 0])
        tras = regla(TRA_MAT).move_to([0, -1.5, 0])
        r_filas = Tex(tr("filas: basta desplazar los paréntesis", "rows: moving the parentheses is enough"), font_size=28, color=GRAY_B).next_to(filas, DOWN, buff=0.3)
        r_tras = Tex(tr("transposición: el escalar se queda a la derecha", "transposition: the scalar stays on the right"), font_size=28, color=GRAY_B).next_to(tras, DOWN, buff=0.3)
        
        with self.voiceover(text=tr("""Con las matrices adoptamos el mismo convenio: <bookmark mark='c'/> una matriz con el escalar a la derecha significa, por definición, lo mismo que con el escalar a la izquierda.""",
                                    """With matrices we adopt the same convention: <bookmark mark='c'/> a matrix with the scalar on the right means, by definition, the same as with the scalar on the left.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("c")
            self.play(FadeIn(convenio), Create(caja), run_time=1)
        
        with self.voiceover(text=tr("""Así, con el selector de filas, que actúa por la izquierda, <bookmark mark='p'/> también basta con desplazar los paréntesis. Se demuestra con los mismos pasos.""",
                                    """So with the row selector, which acts on the left, <bookmark mark='p'/> moving the parentheses is enough too. It is proved with the same steps.""")) as tracker:
            self.play(FadeIn(filas), run_time=0.8)
            self.wait_until_bookmark("p")
            # glifos: i | ( A λ ) (0-5)  ->  ( i | A ) λ (0-5)
            parentesis = [filas[0][2], filas[0][5], filas[2][0], filas[2][4]]
            resalta(self, parentesis, factor=1.25)
            viaje(self, filas, [1, 2, 0, 3, 5, 4])
            apaga(self, parentesis, factor=1.25)
            self.play(FadeIn(r_filas), run_time=0.5)
        
        with self.voiceover(text=tr("""Y al transponer, <bookmark mark='t'/> el escalar puede quedarse a la derecha.""",
                                    """And when we transpose, <bookmark mark='t'/> the scalar can stay on the right.""")) as tracker:
            self.wait_until_bookmark("t")
            self.play(FadeIn(tras), FadeIn(r_tras), run_time=1)
        
        self.pausa_media()


class L01_V15_E05_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        convenios = MathTex(r"\Vect{b}\lambda=\lambda\Vect{b}\qquad\quad \Mat{A}\lambda=\lambda\Mat{A}", tex_template=myTemplate, font_size=44).move_to([0, 1.7, 0])
        reglas = MathTex(COL_MAT[0] + "=" + COL_MAT[1] + r"\qquad\quad " + FIL_MAT[0] + "=" + FIL_MAT[1], tex_template=myTemplate, font_size=44).move_to([0, 0.2, 0])
        r_reglas = Tex(tr("por los dos lados, basta desplazar los paréntesis", "on both sides, moving the parentheses is enough"), font_size=28, color=GRAY_B).next_to(reglas, DOWN, buff=0.3)
        sin = MathTex(r"\lambda\VectC{A}{j}\qquad\quad \VectF{A}{i}\lambda", tex_template=myTemplate, font_size=44).move_to([0, -1.6, 0])
        r_sin = Tex(tr("notación asociativa: los paréntesis se pueden omitir", "associative notation: the parentheses can be omitted"), font_size=28, color=GRAY_B).next_to(sin, DOWN, buff=0.3)
        
        with self.voiceover(text=tr("""Resumamos. Aceptamos escribir el escalar a la derecha de un vector o de una matriz, con el mismo significado. <bookmark mark='r'/> Así, tanto si el selector actúa por la derecha como por la izquierda, basta con desplazar los paréntesis.""",
                                    """Let us sum up. We accept writing the scalar on the right of a vector or a matrix, with the same meaning. <bookmark mark='r'/> So whether the selector acts on the right or on the left, moving the parentheses is enough.""")) as tracker:
            self.play(Write(cabecera), FadeIn(convenios), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(reglas), FadeIn(r_reglas), run_time=0.8)
        
        with self.voiceover(text=tr("""Como el resultado no depende de la colocación de los paréntesis, <bookmark mark='o'/> muchas veces podremos omitirlos. En las demostraciones los seguiremos escribiendo, para ver qué regla se aplica en cada paso.""",
                                    """Since the result does not depend on where the parentheses are, <bookmark mark='o'/> we will often be able to omit them. In proofs we will keep writing them, to see which rule is applied at each step.""")) as tracker:
            self.wait_until_bookmark("o")
            self.play(FadeIn(sin), FadeIn(r_sin), run_time=0.8)
        
        with self.voiceover(text=tr("""Con este vídeo termina la primera lección del curso.""",
                                    """This video ends the first lesson of the course.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
