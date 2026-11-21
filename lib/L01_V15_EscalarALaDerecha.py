from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("El escalar a la derecha", "The scalar on the right")

COLOR_SELECTOR = GREEN     # el selector, en verde; el escalar, en amarillo (COLOR_ESCALAR)

# Las reglas del vídeo: (lado izquierdo, lado derecho)
DER_VEC  = (r"\elemRp{\lambda\Vect{b}}{i}", r"\lambda\eleVRpE{b}{i}")      # ( λ b ) | i  =  λ ( b | i )
IZQ_VEC  = (r"\elemLp{\lambda\Vect{b}}{i}", r"\lambda\eleVLpE{b}{i}")      # i | ( λ b )  =  λ ( i | b )
IZQ_VEC2 = (r"\elemLp{\Vect{b}\lambda}{i}", r"\eleVLpE{b}{i}\lambda")      # i | ( b λ )  =  ( i | b ) λ
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


def rotulo(texto, junto_a, x, font_size=34):
    """Rótulo gris pequeño a la derecha de una línea (lo que justifica el paso)."""
    r = Tex(texto, tex_template=myTemplate, font_size=font_size, color=GRAY_A).next_to(junto_a, RIGHT, buff=0.6)
    return r.shift((x - r.get_left()[0])*RIGHT)


def nace(escena, origen, destino, fijos, moviles=(), aparecen=(), con_igual=True, extra=(), marca=None,
         t_fijos=0.8, t_moviles=0.9, tenue=False):
    """Una expresión nace de la anterior (CLAUDE.md, «Cada expresión nace de la anterior»). Primero, mientras la
    voz nombra la regla, se copia lo que no cambia (fijos: parejas glifo de origen, glifo de destino) y aparece el
    igual; después (en la marca, si se da) viaja lo que el paso mueve (moviles) y surge lo nuevo (aparecen).
    Con tenue=True (como en V14), lo fijo baja atenuado y sin el igual; el igual aparece y lo fijo se enciende
    cuando llega lo móvil: así no se lee una igualdad falsa mientras la voz dice el preámbulo."""
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
        escena.play(*[TransformFromCopy(origen[i], destino[j]) for i, j in moviles],
                    *[FadeIn(destino[j]) for j in aparecen], *al_final, run_time=t_moviles)


def entera(escena, linea):
    """Tras nacer glifo a glifo, la línea vuelve a estar en la escena como un solo objeto."""
    escena.remove(*linea[0]); escena.add(linea)

class L01_V15_EscalarALaDerecha(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        der = regla(DER_VEC).move_to([0, 1.2, 0])
        izq = regla(IZQ_VEC).move_to([0, -1.2, 0])
        r_der = Tex(tr("selector a la derecha: basta desplazar los paréntesis", "selector on the right: moving the parentheses is enough"),
                    font_size=32, color=GRAY_A).next_to(der, DOWN, buff=0.35)
        r_izq = Tex(tr("selector a la izquierda: el escalar y el selector intercambian sus posiciones", "selector on the left: the scalar and the selector swap their positions"),
                    font_size=32, color=GRAY_A).next_to(izq, DOWN, buff=0.35)
        # glifos de izq: i | ( λ b ) (0-5)  =  λ ( i | b ) (0-5)
        sel = [izq[0][0:2], izq[2][2:4]]
        esc = [izq[0][3], izq[2][0]]
        # glifos de der: ( λ b ) | i (0-5)  =  λ ( b | i ) (0-5)
        sel_d = [der[0][4:6], der[2][3:5]]
        esc_d = [der[0][1], der[2][0]]
        sin_par = MathTex(r"=\lambda\eleVR{b}{i}", tex_template=myTemplate, font_size=48).next_to(der, RIGHT, buff=0.2)
        
        with self.voiceover(text=tr("""En este vídeo veremos una última extensión de la notación: escribir el escalar a la derecha de un vector o de una matriz.""",
                                    """In this video we will see one last extension of the notation: writing the scalar on the right of a vector or a matrix.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Seleccionemos una componente del producto de un escalar por un vector. Con el selector a la derecha, <bookmark mark='q'/> la definición de producto por un escalar permite <bookmark mark='p'/> desplazar los paréntesis. <bookmark mark='n'/> Ningún símbolo cambia de sitio: solo se mueven los paréntesis.""",
                                    """Let us select a component of the product of a scalar and a vector. With the selector on the right, <bookmark mark='q'/> the definition of the product by a scalar lets us <bookmark mark='p'/> move the parentheses. <bookmark mark='n'/> No symbol changes place: only the parentheses move.""")) as tracker:
            # en dos tiempos (auditoría 2026-11-21): primero la componente del producto; el otro lado, cuando la voz llega a la definición
            self.play(FadeIn(der[0]), run_time=0.8)
            self.wait_until_bookmark("q")
            self.play(FadeIn(der[1]), FadeIn(der[2]), run_time=0.8)
            self.wait_until_bookmark("p")
            parentesis = [der[0][0], der[0][3], der[2][1], der[2][5]]
            resalta(self, parentesis, factor=1.25)
            viaje(self, der, [1, 0, 2, 5, 3, 4])
            apaga(self, parentesis, factor=1.25)
            self.wait_until_bookmark("n")
            self.play(*[x.animate.set_color(COLOR_SELECTOR) for x in sel_d], *[x.animate.set_color(COLOR_ESCALAR) for x in esc_d],
                      FadeIn(r_der), run_time=0.5)
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""El selector también puede actuar por la izquierda, con el mismo resultado. <bookmark mark='x'/> Pero entonces, al sacar el escalar, <bookmark mark='c'/> el escalar y el selector intercambian sus posiciones. La igualdad es cierta, pero ya no basta con desplazar los paréntesis.""",
                                    """The selector can also act on the left, with the same result. <bookmark mark='x'/> But then, when we take the scalar out, <bookmark mark='c'/> the scalar and the selector swap their positions. The equality holds, but moving the parentheses is no longer enough.""")) as tracker:
            self.play(FadeIn(izq[0]), run_time=0.8)
            self.wait_until_bookmark("x")
            self.play(FadeIn(izq[1]), FadeIn(izq[2]), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(*[x.animate.set_color(COLOR_SELECTOR) for x in sel], *[x.animate.set_color(COLOR_ESCALAR) for x in esc], run_time=0.4)
            viaje(self, izq, [2, 3, 1, 0, 4, 5], run_time=2.2)   # el selector y el escalar se cruzan, ida y vuelta
            self.play(FadeIn(r_izq), run_time=0.5)
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Cuando basta con desplazar los paréntesis, <bookmark mark='o'/> podemos escribir sin ellos.""",
                                    """When moving the parentheses is enough, <bookmark mark='o'/> we can write without them.""")) as tracker:
            self.wait_until_bookmark("o")
            self.play(FadeIn(sin_par), run_time=0.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Un convenio de notación", "A notational convention"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        convenio = MathTex(r"\Vect{b}\lambda", "=", r"\lambda\Vect{b}", tex_template=myTemplate, font_size=60).move_to([0, 1.3, 0])
        caja = SurroundingRectangle(convenio, color=COLOR_ESCALAR, buff=0.25, corner_radius=0.15, stroke_width=3)
        # ejemplo con todas las componentes iguales: menos cifras distintas y se ve de un vistazo (Marcos, 2026-11-21)
        ejemplo = MathTex(fila_vec([1, 1, 1]), "2", "=", "2", fila_vec([1, 1, 1]), "=", fila_vec([2, 2, 2]), tex_template=myTemplate, font_size=44).move_to([0, -0.7, 0])
        ejemplo[1].set_color(COLOR_ESCALAR); ejemplo[3].set_color(COLOR_ESCALAR)
        problema = regla(IZQ_VEC, 60).move_to([0, 1.3, 0]).set_opacity(0.35)   # la regla del problema (escena 1), atenuada: el antecedente de «cuando el selector actúa por la izquierda»
        habitual = Tex(tr(r"Lo habitual es escribir el escalar primero: $2\Vect{b}$", r"The usual way is to write the scalar first: $2\Vect{b}$"),
                       tex_template=myTemplate, font_size=34, color=GRAY_A).move_to([0, -2.3, 0])
        
        with self.voiceover(text=tr("""Para que también baste con desplazar los paréntesis cuando el selector actúa por la izquierda, adoptamos un convenio: <bookmark mark='c'/> aceptamos escribir el escalar a la derecha del vector. Por definición, significa lo mismo que con el escalar a la izquierda.""",
                                    """So that moving the parentheses is also enough when the selector acts on the left, we adopt a convention: <bookmark mark='c'/> we accept writing the scalar on the right of the vector. By definition, it means the same as with the scalar on the left.""")) as tracker:
            self.play(Write(cabecera), FadeIn(problema), run_time=1)
            self.wait_until_bookmark("c")
            self.play(FadeOut(problema), FadeIn(convenio[0]), run_time=0.8)   # el convenio ocupa el sitio del problema
            self.wait(1.5)
            self.play(FadeIn(convenio[1]), FadeIn(convenio[2]), Create(caja), run_time=1)
        
        self.wait(0.6)
        
        with self.voiceover(text=tr("""El vector por dos <bookmark mark='m'/> es lo mismo que dos por el vector.""",
                                    """The vector times two <bookmark mark='m'/> is the same as two times the vector.""")) as tracker:
            # sin «En este ejemplo» (Marcos, 2026-11-20: el convenio vale siempre); toma nueva (el recorte se notaba).
            # En tres tiempos (auditoría 2026-11-21): cada forma en su frase y el resultado al acabar
            self.play(FadeIn(ejemplo[0:2]), run_time=0.6)
            self.wait_until_bookmark("m")
            self.play(FadeIn(ejemplo[2:5]), run_time=0.6)
        self.play(FadeIn(ejemplo[5:]), run_time=0.6)
        self.wait(0.5)
        
        with self.voiceover(text=tr("""No es una operación nueva, sino otra manera de escribir el mismo producto. <bookmark mark='h'/> Lo habitual es escribir el escalar primero. En este curso lo escribiremos a la derecha solo cuando convenga a la notación.""",
                                    """It is not a new operation, but another way of writing the same product. <bookmark mark='h'/> The usual way is to write the scalar first. In this course we will write it on the right only when it suits the notation.""")) as tracker:
            self.wait_until_bookmark("h")
            self.play(FadeIn(habitual), run_time=0.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Con el escalar a la derecha", "With the scalar on the right"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        # Glifos: i | ( b λ ) (0-5);  = i | ( λ b ) (0-6);  = λ ( i | b ) (0-6);  = ( i | b ) λ (0-6)
        cadena = [MathTex(f, tex_template=myTemplate, font_size=48) for f in
                  (IZQ_VEC2[0], "=" + IZQ_VEC[0], "=" + IZQ_VEC[1], "=" + IZQ_VEC2[1])]
        for k, l in enumerate(cadena):
            l.move_to([0, 1.7 - 0.95*k, 0]).align_to([-4.2 + (0.7 if k else 0), 0, 0], LEFT)   # 0,6 más a la izquierda: el tercer rótulo tocaba la firma del margen
        rotulos = [rotulo(t, l, 0.0) for t, l in zip([tr("el convenio", "the convention"),
                                                      tr("el escalar pasa delante del selector", "the scalar moves in front of the selector"),
                                                      tr("la conmutativa del producto de números", "commutativity of the product of numbers")], cadena[1:])]
        final = regla(IZQ_VEC2, 52).move_to([0, -2.6, 0])
        objetivo = final.copy().set_opacity(0.35)   # lo que se va a demostrar, atenuado hasta reunir los extremos
        
        with self.voiceover(text=tr("""Vamos a demostrar que, con el escalar a la derecha, vuelve a bastar con desplazar los paréntesis. <bookmark mark='l0'/> Seleccionamos por la izquierda una componente del producto, escrito con el escalar a la derecha.""",
                                    """Let us prove that, with the scalar on the right, moving the parentheses is enough again. <bookmark mark='l0'/> We select, on the left, a component of the product, written with the scalar on the right.""")) as tracker:
            self.play(Write(cabecera), FadeIn(objetivo), run_time=1)
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        self.wait(0.4)
        
        with self.voiceover(text=tr("""Por el convenio, <bookmark mark='x'/> podemos escribir el escalar a la izquierda.""",
                                    """By the convention, <bookmark mark='x'/> we can write the scalar on the left.""")) as tracker:
            # el vector y el escalar se cruzan dentro de los paréntesis
            nace(self, cadena[0][0], cadena[1][0], [(0, 1), (1, 2), (2, 3), (5, 6)], [(3, 5), (4, 4)], extra=[FadeIn(rotulos[0])], marca="x")
            entera(self, cadena[1])
        self.wait(0.5)
        
        with self.voiceover(text=tr("""El selector actúa igual por los dos lados del vector, así que <bookmark mark='x'/> también podemos sacar el escalar.""",   # «sacar el escalar», como V14 y la escena 1 (auditoría 2026-11-21)
                                    """The selector acts in the same way on both sides of the vector, so <bookmark mark='x'/> we can also take the scalar out.""")) as tracker:
            # primero baja «( b )», atenuado y sin el igual; en «podemos sacar el escalar» el escalar y el selector bajan
            # intercambiando sus posiciones (Marcos, 2026-11-21, como en V14: antes viajaban los paréntesis)
            nace(self, cadena[1][0], cadena[2][0], [(3, 2), (5, 5), (6, 6)], [(4, 1), (1, 3), (2, 4)], extra=[FadeIn(rotulos[1])], marca="x", tenue=True)
            entera(self, cadena[2])
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Lo que queda es un producto de dos números, así que por la conmutativa <bookmark mark='x'/> podemos intercambiarlos.""",
                                    """What remains is a product of two numbers, so by the commutative property <bookmark mark='x'/> we can swap them.""")) as tracker:
            # los dos números (λ e i|b), señalados en «un producto de dos números»; el cruce, entero en «podemos intercambiarlos»
            numeros = VGroup(cadena[2][0][1], cadena[2][0][3:6])
            self.play(numeros.animate.set_color(COLOR_ESCALAR), run_time=0.3)
            self.wait_until_bookmark("x")
            nace(self, cadena[2][0], cadena[3][0], [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)], [(1, 6)], extra=[FadeIn(rotulos[2])])
            entera(self, cadena[3])
            self.play(numeros.animate.set_color(WHITE), run_time=0.3)
        
        self.pausa_corta()
        
        with self.voiceover(text=tr("""Reunamos los dos extremos de la cadena. <bookmark mark='p'/> Con el escalar a la derecha, vuelve a bastar con desplazar los paréntesis.""",
                                    """Let us put the two ends of the chain together. <bookmark mark='p'/> With the scalar on the right, moving the parentheses is enough again.""")) as tracker:
            self.play(FadeOut(objetivo), TransformFromCopy(cadena[0][0], final[0]), FadeIn(final[1]), TransformFromCopy(cadena[3][0][1:], final[2]), run_time=1.2)
            caja = SurroundingRectangle(final, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)   # lo demostrado, recuadrado
            self.play(Create(caja), run_time=0.8)
            self.wait_until_bookmark("p")
            # glifos: i | ( b λ ) (0-5)  ->  ( i | b ) λ (0-5)
            parentesis = [final[0][2], final[0][5], final[2][0], final[2][4]]
            resalta(self, parentesis, factor=1.25)
            viaje(self, final, [1, 2, 0, 3, 5, 4])
            apaga(self, parentesis, factor=1.25)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Lo mismo con matrices", "The same with matrices"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        convenio = MathTex(r"\Mat{A}\lambda", "=", r"\lambda\Mat{A}", tex_template=myTemplate, font_size=56).move_to([0, 1.9, 0])
        caja = SurroundingRectangle(convenio, color=COLOR_ESCALAR, buff=0.22, corner_radius=0.15, stroke_width=3)
        filas = regla(FIL_MAT).move_to([0, 0.2, 0])
        # la regla de la transposición con su deducción (libro, 1.6): convenio, transpuesta de un producto por un escalar, convenio
        tras = MathTex(r"\Transp{\Mat{A}\lambda}", "=", r"\Transp{\lambda\Mat{A}}", "=", r"\lambda\MatTpE{A}", "=", r"\MatTpE{A}\lambda",
                       tex_template=myTemplate, font_size=48).move_to([0, -1.5, 0])
        intermedios = VGroup(*tras[1:5])
        r_filas = Tex(tr("filas: basta desplazar los paréntesis", "rows: moving the parentheses is enough"), font_size=34, color=GRAY_A).next_to(filas, DOWN, buff=0.3)
        r_tras = Tex(tr("transposición: el escalar se queda a la derecha", "transposition: the scalar stays on the right"), font_size=34, color=GRAY_A).next_to(tras, DOWN, buff=0.3)
        
        with self.voiceover(text=tr("""Con las matrices adoptamos el mismo convenio: <bookmark mark='c'/> una matriz con el escalar a la derecha significa, por definición, lo mismo que con el escalar a la izquierda.""",
                                    """With matrices we adopt the same convention: <bookmark mark='c'/> a matrix with the scalar on the right means, by definition, the same as with the scalar on the left.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("c")
            self.play(FadeIn(convenio), Create(caja), run_time=1)
        
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Así, con el selector de filas, que actúa por la izquierda, <bookmark mark='p'/> también basta con desplazar los paréntesis. Se demuestra del mismo modo.""",
                                    """So with the row selector, which acts on the left, <bookmark mark='p'/> moving the parentheses is enough too. It is proved in the same way.""")) as tracker:
            self.play(FadeIn(filas), run_time=0.8)
            self.wait_until_bookmark("p")
            # glifos: i | ( A λ ) (0-5)  ->  ( i | A ) λ (0-5)
            parentesis = [filas[0][2], filas[0][5], filas[2][0], filas[2][4]]
            resalta(self, parentesis, factor=1.25)
            viaje(self, filas, [1, 2, 0, 3, 5, 4])
            apaga(self, parentesis, factor=1.25)
            self.play(FadeIn(r_filas), run_time=0.5)
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Y al transponer, <bookmark mark='t'/> el escalar puede quedarse a la derecha. <bookmark mark='d'/> Se deduce del convenio y de la transpuesta de un producto por un escalar.""",
                                    """And when we transpose, <bookmark mark='t'/> the scalar can stay on the right. <bookmark mark='d'/> It follows from the convention and from the transpose of a product by a scalar.""")) as tracker:
            self.wait_until_bookmark("t")
            intermedios.set_opacity(0.25)
            self.play(FadeIn(tras), FadeIn(r_tras), run_time=1)
            self.wait_until_bookmark("d")
            self.play(intermedios.animate.set_opacity(1), run_time=0.8)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        convenios = MathTex(r"\Vect{b}\lambda=\lambda\Vect{b}\qquad\quad \Mat{A}\lambda=\lambda\Mat{A}", tex_template=myTemplate, font_size=44).move_to([0, 1.7, 0])
        col_r, fil_r = regla(COL_MAT, 44), regla(FIL_MAT, 44)
        reglas = VGroup(col_r, fil_r).arrange(RIGHT, buff=1.2).move_to([0, 0.2, 0])
        r_reglas = Tex(tr("por los dos lados, basta desplazar los paréntesis", "on both sides, moving the parentheses is enough"), font_size=34, color=GRAY_A).next_to(reglas, DOWN, buff=0.3)
        sin = MathTex(r"\lambda\VectC{A}{j}\qquad\quad \VectF{A}{i}\lambda", tex_template=myTemplate, font_size=44).move_to([0, -1.6, 0])
        r_sin = Tex(tr("los paréntesis se pueden omitir", "the parentheses can be omitted"), font_size=34, color=GRAY_A).next_to(sin, DOWN, buff=0.3)
        
        with self.voiceover(text=tr("""Resumamos. Aceptamos escribir el escalar a la derecha de un vector o de una matriz, con el mismo significado. <bookmark mark='r'/> Así, tanto si el selector actúa <bookmark mark='d'/> por la derecha como <bookmark mark='i'/> por la izquierda, basta con desplazar los paréntesis.""",
                                    """Let us sum up. We accept writing the scalar on the right of a vector or a matrix, with the same meaning. <bookmark mark='r'/> So whether the selector acts <bookmark mark='d'/> on the right or <bookmark mark='i'/> on the left, moving the parentheses is enough.""")) as tracker:
            self.play(Write(cabecera), FadeIn(convenios), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(reglas), FadeIn(r_reglas), run_time=0.8)
            self.wait_until_bookmark("d")
            viaje(self, col_r, [1, 0, 2, 5, 3, 4], run_time=1.6)
            self.wait_until_bookmark("i")
            viaje(self, fil_r, [1, 2, 0, 3, 5, 4], run_time=1.6)
        
        self.wait(0.5)
        
        # el nombre que V14 dio a esta propiedad (auditoría 2026-11-21): aquí se ve, porque basta desplazar los paréntesis
        with self.voiceover(text=tr("""Por eso decimos que el selector es asociativo con el producto por un escalar.""",
                                    """That is why we say that the selector is associative with scalar multiplication.""")) as tracker:
            self.play(Indicate(col_r, color=COLOR_ESCALAR, scale_factor=1.08), Indicate(fil_r, color=COLOR_ESCALAR, scale_factor=1.08), run_time=1.5)
        
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Como el resultado no depende de la colocación de los paréntesis, <bookmark mark='o'/> muchas veces podremos omitirlos. En las demostraciones los seguiremos escribiendo, porque muestran la regla que se aplica en cada paso.""",
                                    """Since the result does not depend on where the parentheses are, <bookmark mark='o'/> we will often be able to omit them. In proofs we will keep writing them, because they show the rule applied at each step.""")) as tracker:
            self.wait_until_bookmark("o")
            self.play(FadeIn(sin), FadeIn(r_sin), run_time=0.8)
        
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Con este vídeo termina la primera lección del curso. En el próximo empieza la segunda, con el producto punto.""",
                                    """This video ends the first lesson of the course. The next one starts the second lesson, with the dot product.""")) as tracker:
            pass
        
        self.pausa_media()


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
                    font_size=32, color=GRAY_A).next_to(der, DOWN, buff=0.35)
        r_izq = Tex(tr("selector a la izquierda: el escalar y el selector intercambian sus posiciones", "selector on the left: the scalar and the selector swap their positions"),
                    font_size=32, color=GRAY_A).next_to(izq, DOWN, buff=0.35)
        # glifos de izq: i | ( λ b ) (0-5)  =  λ ( i | b ) (0-5)
        sel = [izq[0][0:2], izq[2][2:4]]
        esc = [izq[0][3], izq[2][0]]
        # glifos de der: ( λ b ) | i (0-5)  =  λ ( b | i ) (0-5)
        sel_d = [der[0][4:6], der[2][3:5]]
        esc_d = [der[0][1], der[2][0]]
        sin_par = MathTex(r"=\lambda\eleVR{b}{i}", tex_template=myTemplate, font_size=48).next_to(der, RIGHT, buff=0.2)
        
        with self.voiceover(text=tr("""En este vídeo veremos una última extensión de la notación: escribir el escalar a la derecha de un vector o de una matriz.""",
                                    """In this video we will see one last extension of the notation: writing the scalar on the right of a vector or a matrix.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Seleccionemos una componente del producto de un escalar por un vector. Con el selector a la derecha, <bookmark mark='q'/> la definición de producto por un escalar permite <bookmark mark='p'/> desplazar los paréntesis. <bookmark mark='n'/> Ningún símbolo cambia de sitio: solo se mueven los paréntesis.""",
                                    """Let us select a component of the product of a scalar and a vector. With the selector on the right, <bookmark mark='q'/> the definition of the product by a scalar lets us <bookmark mark='p'/> move the parentheses. <bookmark mark='n'/> No symbol changes place: only the parentheses move.""")) as tracker:
            # en dos tiempos (auditoría 2026-11-21): primero la componente del producto; el otro lado, cuando la voz llega a la definición
            self.play(FadeIn(der[0]), run_time=0.8)
            self.wait_until_bookmark("q")
            self.play(FadeIn(der[1]), FadeIn(der[2]), run_time=0.8)
            self.wait_until_bookmark("p")
            parentesis = [der[0][0], der[0][3], der[2][1], der[2][5]]
            resalta(self, parentesis, factor=1.25)
            viaje(self, der, [1, 0, 2, 5, 3, 4])
            apaga(self, parentesis, factor=1.25)
            self.wait_until_bookmark("n")
            self.play(*[x.animate.set_color(COLOR_SELECTOR) for x in sel_d], *[x.animate.set_color(COLOR_ESCALAR) for x in esc_d],
                      FadeIn(r_der), run_time=0.5)
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""El selector también puede actuar por la izquierda, con el mismo resultado. <bookmark mark='x'/> Pero entonces, al sacar el escalar, <bookmark mark='c'/> el escalar y el selector intercambian sus posiciones. La igualdad es cierta, pero ya no basta con desplazar los paréntesis.""",
                                    """The selector can also act on the left, with the same result. <bookmark mark='x'/> But then, when we take the scalar out, <bookmark mark='c'/> the scalar and the selector swap their positions. The equality holds, but moving the parentheses is no longer enough.""")) as tracker:
            self.play(FadeIn(izq[0]), run_time=0.8)
            self.wait_until_bookmark("x")
            self.play(FadeIn(izq[1]), FadeIn(izq[2]), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(*[x.animate.set_color(COLOR_SELECTOR) for x in sel], *[x.animate.set_color(COLOR_ESCALAR) for x in esc], run_time=0.4)
            viaje(self, izq, [2, 3, 1, 0, 4, 5], run_time=2.2)   # el selector y el escalar se cruzan, ida y vuelta
            self.play(FadeIn(r_izq), run_time=0.5)
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Cuando basta con desplazar los paréntesis, <bookmark mark='o'/> podemos escribir sin ellos.""",
                                    """When moving the parentheses is enough, <bookmark mark='o'/> we can write without them.""")) as tracker:
            self.wait_until_bookmark("o")
            self.play(FadeIn(sin_par), run_time=0.8)
        
        self.pausa_media()


class L01_V15_E02_Convenio(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Un convenio de notación", "A notational convention"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        convenio = MathTex(r"\Vect{b}\lambda", "=", r"\lambda\Vect{b}", tex_template=myTemplate, font_size=60).move_to([0, 1.3, 0])
        caja = SurroundingRectangle(convenio, color=COLOR_ESCALAR, buff=0.25, corner_radius=0.15, stroke_width=3)
        # ejemplo con todas las componentes iguales: menos cifras distintas y se ve de un vistazo (Marcos, 2026-11-21)
        ejemplo = MathTex(fila_vec([1, 1, 1]), "2", "=", "2", fila_vec([1, 1, 1]), "=", fila_vec([2, 2, 2]), tex_template=myTemplate, font_size=44).move_to([0, -0.7, 0])
        ejemplo[1].set_color(COLOR_ESCALAR); ejemplo[3].set_color(COLOR_ESCALAR)
        problema = regla(IZQ_VEC, 60).move_to([0, 1.3, 0]).set_opacity(0.35)   # la regla del problema (escena 1), atenuada: el antecedente de «cuando el selector actúa por la izquierda»
        habitual = Tex(tr(r"Lo habitual es escribir el escalar primero: $2\Vect{b}$", r"The usual way is to write the scalar first: $2\Vect{b}$"),
                       tex_template=myTemplate, font_size=34, color=GRAY_A).move_to([0, -2.3, 0])
        
        with self.voiceover(text=tr("""Para que también baste con desplazar los paréntesis cuando el selector actúa por la izquierda, adoptamos un convenio: <bookmark mark='c'/> aceptamos escribir el escalar a la derecha del vector. Por definición, significa lo mismo que con el escalar a la izquierda.""",
                                    """So that moving the parentheses is also enough when the selector acts on the left, we adopt a convention: <bookmark mark='c'/> we accept writing the scalar on the right of the vector. By definition, it means the same as with the scalar on the left.""")) as tracker:
            self.play(Write(cabecera), FadeIn(problema), run_time=1)
            self.wait_until_bookmark("c")
            self.play(FadeOut(problema), FadeIn(convenio[0]), run_time=0.8)   # el convenio ocupa el sitio del problema
            self.wait(1.5)
            self.play(FadeIn(convenio[1]), FadeIn(convenio[2]), Create(caja), run_time=1)
        
        self.wait(0.6)
        
        with self.voiceover(text=tr("""El vector por dos <bookmark mark='m'/> es lo mismo que dos por el vector.""",
                                    """The vector times two <bookmark mark='m'/> is the same as two times the vector.""")) as tracker:
            # sin «En este ejemplo» (Marcos, 2026-11-20: el convenio vale siempre); toma nueva (el recorte se notaba).
            # En tres tiempos (auditoría 2026-11-21): cada forma en su frase y el resultado al acabar
            self.play(FadeIn(ejemplo[0:2]), run_time=0.6)
            self.wait_until_bookmark("m")
            self.play(FadeIn(ejemplo[2:5]), run_time=0.6)
        self.play(FadeIn(ejemplo[5:]), run_time=0.6)
        self.wait(0.5)
        
        with self.voiceover(text=tr("""No es una operación nueva, sino otra manera de escribir el mismo producto. <bookmark mark='h'/> Lo habitual es escribir el escalar primero. En este curso lo escribiremos a la derecha solo cuando convenga a la notación.""",
                                    """It is not a new operation, but another way of writing the same product. <bookmark mark='h'/> The usual way is to write the scalar first. In this course we will write it on the right only when it suits the notation.""")) as tracker:
            self.wait_until_bookmark("h")
            self.play(FadeIn(habitual), run_time=0.8)
        
        self.pausa_media()


class L01_V15_E03_Demostracion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Con el escalar a la derecha", "With the scalar on the right"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        # Glifos: i | ( b λ ) (0-5);  = i | ( λ b ) (0-6);  = λ ( i | b ) (0-6);  = ( i | b ) λ (0-6)
        cadena = [MathTex(f, tex_template=myTemplate, font_size=48) for f in
                  (IZQ_VEC2[0], "=" + IZQ_VEC[0], "=" + IZQ_VEC[1], "=" + IZQ_VEC2[1])]
        for k, l in enumerate(cadena):
            l.move_to([0, 1.7 - 0.95*k, 0]).align_to([-4.2 + (0.7 if k else 0), 0, 0], LEFT)   # 0,6 más a la izquierda: el tercer rótulo tocaba la firma del margen
        rotulos = [rotulo(t, l, 0.0) for t, l in zip([tr("el convenio", "the convention"),
                                                      tr("el escalar pasa delante del selector", "the scalar moves in front of the selector"),
                                                      tr("la conmutativa del producto de números", "commutativity of the product of numbers")], cadena[1:])]
        final = regla(IZQ_VEC2, 52).move_to([0, -2.6, 0])
        objetivo = final.copy().set_opacity(0.35)   # lo que se va a demostrar, atenuado hasta reunir los extremos
        
        with self.voiceover(text=tr("""Vamos a demostrar que, con el escalar a la derecha, vuelve a bastar con desplazar los paréntesis. <bookmark mark='l0'/> Seleccionamos por la izquierda una componente del producto, escrito con el escalar a la derecha.""",
                                    """Let us prove that, with the scalar on the right, moving the parentheses is enough again. <bookmark mark='l0'/> We select, on the left, a component of the product, written with the scalar on the right.""")) as tracker:
            self.play(Write(cabecera), FadeIn(objetivo), run_time=1)
            self.wait_until_bookmark("l0")
            self.play(Write(cadena[0]), run_time=1)
        self.wait(0.4)
        
        with self.voiceover(text=tr("""Por el convenio, <bookmark mark='x'/> podemos escribir el escalar a la izquierda.""",
                                    """By the convention, <bookmark mark='x'/> we can write the scalar on the left.""")) as tracker:
            # el vector y el escalar se cruzan dentro de los paréntesis
            nace(self, cadena[0][0], cadena[1][0], [(0, 1), (1, 2), (2, 3), (5, 6)], [(3, 5), (4, 4)], extra=[FadeIn(rotulos[0])], marca="x")
            entera(self, cadena[1])
        self.wait(0.5)
        
        with self.voiceover(text=tr("""El selector actúa igual por los dos lados del vector, así que <bookmark mark='x'/> también podemos sacar el escalar.""",   # «sacar el escalar», como V14 y la escena 1 (auditoría 2026-11-21)
                                    """The selector acts in the same way on both sides of the vector, so <bookmark mark='x'/> we can also take the scalar out.""")) as tracker:
            # primero baja «( b )», atenuado y sin el igual; en «podemos sacar el escalar» el escalar y el selector bajan
            # intercambiando sus posiciones (Marcos, 2026-11-21, como en V14: antes viajaban los paréntesis)
            nace(self, cadena[1][0], cadena[2][0], [(3, 2), (5, 5), (6, 6)], [(4, 1), (1, 3), (2, 4)], extra=[FadeIn(rotulos[1])], marca="x", tenue=True)
            entera(self, cadena[2])
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Lo que queda es un producto de dos números, así que por la conmutativa <bookmark mark='x'/> podemos intercambiarlos.""",
                                    """What remains is a product of two numbers, so by the commutative property <bookmark mark='x'/> we can swap them.""")) as tracker:
            # los dos números (λ e i|b), señalados en «un producto de dos números»; el cruce, entero en «podemos intercambiarlos»
            numeros = VGroup(cadena[2][0][1], cadena[2][0][3:6])
            self.play(numeros.animate.set_color(COLOR_ESCALAR), run_time=0.3)
            self.wait_until_bookmark("x")
            nace(self, cadena[2][0], cadena[3][0], [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)], [(1, 6)], extra=[FadeIn(rotulos[2])])
            entera(self, cadena[3])
            self.play(numeros.animate.set_color(WHITE), run_time=0.3)
        
        self.pausa_corta()
        
        with self.voiceover(text=tr("""Reunamos los dos extremos de la cadena. <bookmark mark='p'/> Con el escalar a la derecha, vuelve a bastar con desplazar los paréntesis.""",
                                    """Let us put the two ends of the chain together. <bookmark mark='p'/> With the scalar on the right, moving the parentheses is enough again.""")) as tracker:
            self.play(FadeOut(objetivo), TransformFromCopy(cadena[0][0], final[0]), FadeIn(final[1]), TransformFromCopy(cadena[3][0][1:], final[2]), run_time=1.2)
            caja = SurroundingRectangle(final, color=COLOR_ESCALAR, buff=0.2, corner_radius=0.15, stroke_width=3)   # lo demostrado, recuadrado
            self.play(Create(caja), run_time=0.8)
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
        # la regla de la transposición con su deducción (libro, 1.6): convenio, transpuesta de un producto por un escalar, convenio
        tras = MathTex(r"\Transp{\Mat{A}\lambda}", "=", r"\Transp{\lambda\Mat{A}}", "=", r"\lambda\MatTpE{A}", "=", r"\MatTpE{A}\lambda",
                       tex_template=myTemplate, font_size=48).move_to([0, -1.5, 0])
        intermedios = VGroup(*tras[1:5])
        r_filas = Tex(tr("filas: basta desplazar los paréntesis", "rows: moving the parentheses is enough"), font_size=34, color=GRAY_A).next_to(filas, DOWN, buff=0.3)
        r_tras = Tex(tr("transposición: el escalar se queda a la derecha", "transposition: the scalar stays on the right"), font_size=34, color=GRAY_A).next_to(tras, DOWN, buff=0.3)
        
        with self.voiceover(text=tr("""Con las matrices adoptamos el mismo convenio: <bookmark mark='c'/> una matriz con el escalar a la derecha significa, por definición, lo mismo que con el escalar a la izquierda.""",
                                    """With matrices we adopt the same convention: <bookmark mark='c'/> a matrix with the scalar on the right means, by definition, the same as with the scalar on the left.""")) as tracker:
            self.play(Write(cabecera), run_time=1)
            self.wait_until_bookmark("c")
            self.play(FadeIn(convenio), Create(caja), run_time=1)
        
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Así, con el selector de filas, que actúa por la izquierda, <bookmark mark='p'/> también basta con desplazar los paréntesis. Se demuestra del mismo modo.""",
                                    """So with the row selector, which acts on the left, <bookmark mark='p'/> moving the parentheses is enough too. It is proved in the same way.""")) as tracker:
            self.play(FadeIn(filas), run_time=0.8)
            self.wait_until_bookmark("p")
            # glifos: i | ( A λ ) (0-5)  ->  ( i | A ) λ (0-5)
            parentesis = [filas[0][2], filas[0][5], filas[2][0], filas[2][4]]
            resalta(self, parentesis, factor=1.25)
            viaje(self, filas, [1, 2, 0, 3, 5, 4])
            apaga(self, parentesis, factor=1.25)
            self.play(FadeIn(r_filas), run_time=0.5)
        
        self.wait(0.8)
        
        with self.voiceover(text=tr("""Y al transponer, <bookmark mark='t'/> el escalar puede quedarse a la derecha. <bookmark mark='d'/> Se deduce del convenio y de la transpuesta de un producto por un escalar.""",
                                    """And when we transpose, <bookmark mark='t'/> the scalar can stay on the right. <bookmark mark='d'/> It follows from the convention and from the transpose of a product by a scalar.""")) as tracker:
            self.wait_until_bookmark("t")
            intermedios.set_opacity(0.25)
            self.play(FadeIn(tras), FadeIn(r_tras), run_time=1)
            self.wait_until_bookmark("d")
            self.play(intermedios.animate.set_opacity(1), run_time=0.8)
        
        self.pausa_media()


class L01_V15_E05_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        convenios = MathTex(r"\Vect{b}\lambda=\lambda\Vect{b}\qquad\quad \Mat{A}\lambda=\lambda\Mat{A}", tex_template=myTemplate, font_size=44).move_to([0, 1.7, 0])
        col_r, fil_r = regla(COL_MAT, 44), regla(FIL_MAT, 44)
        reglas = VGroup(col_r, fil_r).arrange(RIGHT, buff=1.2).move_to([0, 0.2, 0])
        r_reglas = Tex(tr("por los dos lados, basta desplazar los paréntesis", "on both sides, moving the parentheses is enough"), font_size=34, color=GRAY_A).next_to(reglas, DOWN, buff=0.3)
        sin = MathTex(r"\lambda\VectC{A}{j}\qquad\quad \VectF{A}{i}\lambda", tex_template=myTemplate, font_size=44).move_to([0, -1.6, 0])
        r_sin = Tex(tr("los paréntesis se pueden omitir", "the parentheses can be omitted"), font_size=34, color=GRAY_A).next_to(sin, DOWN, buff=0.3)
        
        with self.voiceover(text=tr("""Resumamos. Aceptamos escribir el escalar a la derecha de un vector o de una matriz, con el mismo significado. <bookmark mark='r'/> Así, tanto si el selector actúa <bookmark mark='d'/> por la derecha como <bookmark mark='i'/> por la izquierda, basta con desplazar los paréntesis.""",
                                    """Let us sum up. We accept writing the scalar on the right of a vector or a matrix, with the same meaning. <bookmark mark='r'/> So whether the selector acts <bookmark mark='d'/> on the right or <bookmark mark='i'/> on the left, moving the parentheses is enough.""")) as tracker:
            self.play(Write(cabecera), FadeIn(convenios), run_time=1)
            self.wait_until_bookmark("r")
            self.play(FadeIn(reglas), FadeIn(r_reglas), run_time=0.8)
            self.wait_until_bookmark("d")
            viaje(self, col_r, [1, 0, 2, 5, 3, 4], run_time=1.6)
            self.wait_until_bookmark("i")
            viaje(self, fil_r, [1, 2, 0, 3, 5, 4], run_time=1.6)
        
        self.wait(0.5)
        
        # el nombre que V14 dio a esta propiedad (auditoría 2026-11-21): aquí se ve, porque basta desplazar los paréntesis
        with self.voiceover(text=tr("""Por eso decimos que el selector es asociativo con el producto por un escalar.""",
                                    """That is why we say that the selector is associative with scalar multiplication.""")) as tracker:
            self.play(Indicate(col_r, color=COLOR_ESCALAR, scale_factor=1.08), Indicate(fil_r, color=COLOR_ESCALAR, scale_factor=1.08), run_time=1.5)
        
        self.wait(0.5)
        
        with self.voiceover(text=tr("""Como el resultado no depende de la colocación de los paréntesis, <bookmark mark='o'/> muchas veces podremos omitirlos. En las demostraciones los seguiremos escribiendo, porque muestran la regla que se aplica en cada paso.""",
                                    """Since the result does not depend on where the parentheses are, <bookmark mark='o'/> we will often be able to omit them. In proofs we will keep writing them, because they show the rule applied at each step.""")) as tracker:
            self.wait_until_bookmark("o")
            self.play(FadeIn(sin), FadeIn(r_sin), run_time=0.8)
        
        self.wait(1.0)
        
        with self.voiceover(text=tr("""Con este vídeo termina la primera lección del curso. En el próximo empieza la segunda, con el producto punto.""",
                                    """This video ends the first lesson of the course. The next one starts the second lesson, with the dot product.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
