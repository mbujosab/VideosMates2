from vm2comun import *   # módulo común generado desde Comunes.org (LANG = "es")

TITULO = tr("Selección de filas, columnas y componentes", "Selecting rows, columns and components")

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


def columna_de_lineas(lineas, x0, y0, dy):
    """Fórmulas de varias partes una debajo de otra, con la parte 1 (el "=") alineada en x0."""
    for k, l in enumerate(lineas):
        l.shift([x0 - l[1].get_left()[0], y0 - k*dy - l.get_y(), 0])
    return VGroup(*lineas)

class L01_V10_Seleccion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        A = matriz(A_SEL, decimales=0, h_buff=1.0)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([0, 2.0, 0])
        x0 = -4.6
        col = MathTex(r"\VectC{A}{1}", r"\;=\;\begin{pmatrix}1\\ 7\end{pmatrix}", tex_template=myTemplate, font_size=48)
        fila = MathTex(r"\VectF{A}{1}", r"\;=\;(1,\ 2,\ 1,)", tex_template=myTemplate, font_size=48)
        for linea, y in [(col, 0.5), (fila, -1.5)]:   # hueco para la fila en vertical
            linea.move_to([x0 + linea.width/2, y, 0])
        fila.shift((col[1].get_left()[0] - fila[1].get_left()[0])*RIGHT)   # los dos "=" alineados
        # la columna y la fila, primero con un índice genérico (j, i) que pasa a ser 1 en el ejemplo
        col_g = MathTex(r"\VectC{A}{j}", tex_template=myTemplate, font_size=48)
        col_g.shift(col[0][0].get_center() - col_g[0][0].get_center())       # glifos: A, |, j
        fila_g = MathTex(r"\VectF{A}{i}", tex_template=myTemplate, font_size=48)
        fila_g.shift(fila[0][2].get_center() - fila_g[0][2].get_center())   # glifos: i, |, A
        # la otra forma de escribir la columna y la fila, detrás de un "=" (Marcos, 2026-10-27)
        col_h = MathTex(r"=(1,\ 7,)", font_size=48).next_to(col, RIGHT, buff=0.25)
        fila_v = MathTex(r"=\begin{pmatrix}1\\ 2\\ 1\end{pmatrix}", font_size=48).next_to(fila, RIGHT, buff=0.25)
        
        # al decir «el elemento de la lista», la matriz de números se transforma en la lista de sus tres columnas (la
        # notación de la escena 5) y al decir «una columna» la franja recorre los tres vectores; vuelve a los números al
        # empezar la frase siguiente (Marcos, 2026-11-03). Glifos de A_lista: [ ( 1 7 ) ; ( 2 0 ) ; ( 1 3 ) ; ]
        A_lista = MathTex(r"\left[\begin{pmatrix}1\\ 7\end{pmatrix};\ \begin{pmatrix}2\\ 0\end{pmatrix};\ \begin{pmatrix}1\\ 3\end{pmatrix};\right]",
                          tex_template=myTemplate, font_size=44).move_to(A).align_to(A, LEFT)
        vectores_lista = [A_lista[0][1:5], A_lista[0][6:10], A_lista[0][11:15]]
        A_num = A.copy()   # copia hecha antes de cualquier animación: A no vuelve a ser destino (CLAUDE.md)
        with self.voiceover(text=tr("""En este vídeo veremos la selección de filas, columnas y componentes de una matriz.""",
                                    """In this video we will see the selection of rows, columns and components of a matrix.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        with self.voiceover(text=tr("""El operador selector también actúa sobre matrices. <bookmark mark='s'/> Con el índice a la derecha selecciona, como en los vectores, <bookmark mark='l'/> el elemento de la lista que ocupa esa posición: <bookmark mark='c'/> una columna.""",
                                    """The selector operator also acts on matrices. <bookmark mark='s'/> With the index on the right it selects, as with vectors, <bookmark mark='l'/> the element of the list in that position: <bookmark mark='c'/> a column.""")) as tracker:
            self.play(FadeIn(f_A), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(col_g), run_time=0.6)
            self.play(Indicate(col_g[0][1:3], color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("l")
            A_tmp = A.copy()
            self.remove(A); self.add(A_tmp)
            self.play(FadeTransform(A_tmp, A_lista), run_time=0.8)   # los números se convierten en la lista de vectores
            self.wait_until_bookmark("c")
            franja = None
            for v in vectores_lista:   # cada elemento de la lista es una columna
                nueva = SurroundingRectangle(v, color=COLOR_ESCALAR, fill_color=COLOR_ESCALAR, fill_opacity=0.22, stroke_width=0, buff=0.08)
                self.play(FadeIn(nueva) if franja is None else ReplacementTransform(franja, nueva), run_time=0.4)
                franja = nueva
            self.play(FadeOut(franja), run_time=0.3)
        
        with self.voiceover(text=tr("""Por ejemplo, con el índice uno, <bookmark mark='c'/> selecciona la primera columna.""",   # sin «de A»: solo hay una matriz (Marcos, 2026-11-03)
                                    """For example, with index one, <bookmark mark='c'/> it selects the first column.""")) as tracker:
            self.play(FadeTransform(A_lista, A_num), ReplacementTransform(col_g, col[0]), run_time=0.8)   # vuelven los números; j pasa a ser 1
            self.remove(A_num); self.add(A)   # el objeto original, intacto, para las franjas que vienen
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0)
            self.play(FadeIn(fc), FadeIn(col[1]), run_time=0.8)
        
        # el símbolo aparece un instante antes de que la voz lo describa (Marcos, 2026-10-18)
        self.play(FadeIn(fila_g), run_time=0.6)
        with self.voiceover(text=tr("""Y con el índice a la izquierda selecciona una fila. <bookmark mark='e'/> Por ejemplo, con el índice uno, <bookmark mark='f'/> selecciona la primera fila.""",
                                    """And with the index on the left it selects a row. <bookmark mark='e'/> For example, with index one, <bookmark mark='f'/> it selects the first row.""")) as tracker:
            self.play(Indicate(fila_g[0][0:2], color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("e")
            self.play(ReplacementTransform(fila_g, fila[0]), run_time=0.8)   # i pasa a ser 1
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 0)
            self.play(FadeIn(ff), FadeIn(fila[1]), run_time=0.8)
        
        with self.voiceover(text=tr("""Cada fila y cada columna es una lista ordenada de números, es decir, un vector.""",
                                    """Each row and each column is an ordered list of numbers, that is, a vector.""")) as tracker:
            self.play(Indicate(ff, color=COLOR_ESCALAR, scale_factor=1.05), run_time=1)
            self.play(Indicate(fc, color=COLOR_ESCALAR, scale_factor=1.05), run_time=1)
        
        self.wait(0.6)   # una pausa antes de la conclusión (Marcos, 2026-10-27)
        with self.voiceover(text=tr("""Por eso, una vez seleccionada, una fila o una columna <bookmark mark='h'/> se puede escribir tanto en horizontal como en vertical, <bookmark mark='p'/> siempre entre paréntesis.""",
                                    """So, once selected, a row or a column <bookmark mark='h'/> can be written either horizontally or vertically, <bookmark mark='p'/> always in parentheses.""")) as tracker:
            self.play(FadeOut(ff), FadeOut(fc), run_time=0.5)
            self.wait_until_bookmark("h")
            self.play(FadeIn(fila_v), FadeIn(col_h), run_time=1)
            self.wait_until_bookmark("p")
            # solo los vectores, sin los signos de igual (glifo 0 de cada parte; Marcos, 2026-11-02)
            self.play(*[Indicate(m, color=COLOR_ESCALAR, scale_factor=1.1) for m in (fila[1][1:], col[1][1:], fila_v[0][1:], col_h[0][1:])], run_time=1.2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Componentes", "Components"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A = matriz(A_SEL, decimales=0, h_buff=1.0)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([0, 2.0, 0])
        por_fila = MathTex(r"\elemRp{\VectF{A}{2}}{1}", r"=", r"\elemR{(7,\ 0,\ 3,)}{1}", r"=", r"7", tex_template=myTemplate, font_size=48)
        por_col = MathTex(r"\elemLp{\VectC{A}{1}}{2}", r"=", r"\elemL{\begin{pmatrix}1\\ 7\end{pmatrix}}{2}", r"=", r"7", tex_template=myTemplate, font_size=48)
        lineas = columna_de_lineas([por_fila, por_col], x0=-1.6, y0=0.3, dy=1.45)
        # Glifos de cada línea: primero la fila (o la columna) seleccionada, después lo que la completa
        fila = VGroup(por_fila[0][1:4], por_fila[1], por_fila[2][:8])                       # 2|A = (7, 0, 3,)
        fila_resto = VGroup(por_fila[0][0], por_fila[0][4:], por_fila[2][8:], por_fila[3:])  # ( )|1, |1, = 7
        col = VGroup(por_col[0][3:6], por_col[1], por_col[2][2:])                            # A|1 = (1; 7)
        col_resto = VGroup(por_col[0][:3], por_col[0][6], por_col[2][:2], por_col[3:])       # 2|( ), 2|, = 7
        convenio = MathTex(r"\eleVL{a}{i}", r"=", r"\eleVR{a}{i}", r"=", r"a_i", tex_template=myTemplate, font_size=52).move_to([0.8, -2.7, 0])
        idea = aviso("idea").next_to(convenio, LEFT, buff=0.8)
        conclusion = MathTex(r"\elemRp{\VectF{A}{2}}{1}", r"=", r"\elemLp{\VectC{A}{1}}{2}", r"=", r"\eleM{A}{2}{1}",
                             tex_template=myTemplate, font_size=52).move_to([0, 0.2, 0])
        general = MathTex(r"\elemRp{\VectF{A}{i}}{j}", r"=", r"\elemLp{\VectC{A}{j}}{i}", r"=", r"\eleM{A}{i}{j}",
                          tex_template=myTemplate, font_size=52).move_to(conclusion)   # mismos glifos: el 2 pasa a i y el 1 a j
        # lo habitual en los libros (a_21) frente al selector, en el ejemplo (como en la escena 3 de V01)
        comp = MathTex(r"\eleM{A}{2}{1}", r"\;=\;", r"a_{21}", r"\;=\;7", tex_template=myTemplate, font_size=48).move_to([0, -1.7, 0])
        r_hab = Tex(tr("lo habitual", "the usual way"), font_size=28, color=GRAY_B).next_to(comp[2], UP, buff=0.2)
        r_sel = Tex(tr("selector", "selector"), font_size=28, color=GRAY_B).next_to(comp[0], UP, buff=0.2)
        # glifos: a_{21} = a, 2, 1; 2|A|1 = 2, |, A, |, 1
        sub_f, sub_c = comp[2][1], comp[2][2]
        sel_i, sel_d = comp[0][0:2], comp[0][3:5]
        
        with self.voiceover(text=tr("""Cada componente de una matriz está a la vez <bookmark mark='f'/> en una fila y <bookmark mark='c'/> en una columna.""",
                                    """Each component of a matrix lies both <bookmark mark='f'/> in a row and <bookmark mark='c'/> in a column.""")) as tracker:
            self.play(Write(cabecera), FadeIn(f_A), run_time=1)
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 1)
            self.play(FadeIn(ff), run_time=0.5)
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0, color=COLOR_C)
            self.play(FadeIn(fc), run_time=0.5)
            self.play(Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
        
        with self.voiceover(text=tr("""El siete, por ejemplo, es componente de dos vectores distintos: <bookmark mark='f'/> es la primera componente de la segunda fila, <bookmark mark='c'/> y la segunda componente de la primera columna.""",
                                    """The seven, for example, is a component of two different vectors: <bookmark mark='f'/> it is the first component of the second row, <bookmark mark='c'/> and the second component of the first column.""")) as tracker:
            self.play(Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
            self.wait_until_bookmark("f")
            self.play(ff.animate.set_fill(opacity=0.55), fc.animate.set_fill(opacity=0.06), run_time=0.5)
            self.wait_until_bookmark("c")
            self.play(ff.animate.set_fill(opacity=0.06), fc.animate.set_fill(opacity=0.55), run_time=0.5)
        self.play(FadeOut(ff), FadeOut(fc), run_time=0.5)
        
        with self.voiceover(text=tr("""Obtengamos el siete de las dos maneras. Seleccionemos primero <bookmark mark='f'/> la fila, <bookmark mark='c'/> y después su primera componente.""",
                                    """Let us get the seven in both ways. First, let us select <bookmark mark='f'/> the row, <bookmark mark='c'/> and then its first component.""")) as tracker:
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 1)
            self.play(FadeIn(ff), FadeIn(fila), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(FadeIn(fila_resto), Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=1)
        
        with self.voiceover(text=tr("""Ahora seleccionemos primero <bookmark mark='c'/> la columna, <bookmark mark='s'/> y después su segunda componente: <bookmark mark='v'/> también obtenemos el siete.""",
                                    """Now let us first select <bookmark mark='c'/> the column, <bookmark mark='s'/> and then its second component: <bookmark mark='v'/> we get the seven again.""")) as tracker:
            self.play(FadeOut(ff), run_time=0.8)
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0, color=COLOR_C)
            self.play(FadeIn(fc), FadeIn(col), run_time=0.8)
            self.wait_until_bookmark("s")
            self.play(FadeIn(col_resto), Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=1)
            self.wait_until_bookmark("v")   # los dos caminos acaban en el mismo siete (Marcos, 2026-11-01)
            self.play(*[Indicate(x, color=COLOR_ESCALAR, scale_factor=1.4) for x in (por_fila[4], por_col[4], A.get_rows()[1][0])], run_time=1.2)
        
        with self.voiceover(text=tr("""Aquí el selector actúa por la izquierda de un vector. <bookmark mark='a'/> Ya en el primer vídeo del curso admitimos que el selector puede actuar por cualquier lado de un vector, <bookmark mark='d'/> con el mismo resultado.""",
                                    """Here the selector acts on the left of a vector. <bookmark mark='a'/> Back in the first video of the course, we agreed that the selector can act on either side of a vector, <bookmark mark='d'/> with the same result.""")) as tracker:
            sel_izq = VGroup(por_col[0][:2], por_col[2][:2])  # los dos selectores por la izquierda, resaltados toda la frase
            self.play(FadeOut(fc), *[s.animate.set_color(COLOR_ESCALAR).scale(1.25) for s in sel_izq], run_time=0.6)
            self.wait_until_bookmark("a")
            self.play(*[s.animate.set_color(WHITE).scale(1/1.25) for s in sel_izq], FadeIn(idea), FadeIn(convenio[0]), run_time=0.8)
            self.wait_until_bookmark("d")
            self.play(FadeIn(convenio[1:]), run_time=0.8)
        
        # la asociatividad del selector justifica la notación sin paréntesis (Marcos, 2026-10-31)
        # glifos: conclusion[0] = ( 2 | A ) | 1 (paréntesis 0 y 4); conclusion[2] = 2 | ( A | 1 ) (paréntesis 2 y 6)
        parentesis = [conclusion[0][0], conclusion[0][4], conclusion[2][2], conclusion[2][6]]
        with self.voiceover(text=tr("""Con este convenio, da igual seleccionar primero la fila o la columna: <bookmark mark='p'/> podemos desplazar los paréntesis sin cambiar el resultado.""",
                                    """With this convention, it makes no difference whether we select the row or the column first: <bookmark mark='p'/> we can move the parentheses without changing the result.""")) as tracker:
            self.play(ReplacementTransform(por_fila[0], conclusion[0]), ReplacementTransform(por_col[0], conclusion[2]), FadeIn(conclusion[1]),
                      FadeOut(VGroup(por_fila[1:], por_col[1:])), run_time=1.2)
            self.wait_until_bookmark("p")
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.3) for x in parentesis], run_time=0.3)
            # como en V04: los glifos de la izquierda van a las posiciones de la derecha y vuelven
            destino = conclusion[2].copy().move_to(conclusion[0])
            self.play(*[Transform(conclusion[0][i], destino[j], rate_func=rate_functions.there_and_back_with_pause)
                        for i, j in zip(range(7), [2, 0, 1, 3, 6, 4, 5])], run_time=2.2)
        
        with self.voiceover(text=tr("""Es una propiedad asociativa, como la del producto por un escalar. <bookmark mark='q'/> Por eso podemos escribir el selector a ambos lados de la matriz, sin paréntesis.""",
                                    """It is an associative property, like that of scalar multiplication. <bookmark mark='q'/> That is why we can write the selector on both sides of the matrix, with no parentheses.""")) as tracker:
            self.wait_until_bookmark("q")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.3) for x in parentesis], run_time=0.3)
            self.play(FadeIn(conclusion[3:]), run_time=1)
        
        with self.voiceover(text=tr("""Lo hemos visto en un ejemplo, pero <bookmark mark='g'/> vale para cualquier componente de cualquier matriz, porque toda componente está a la vez en su <bookmark mark='f'/> fila y en su <bookmark mark='c'/> columna, que son vectores.""",
                                    """We have seen it in an example, but <bookmark mark='g'/> it holds for any component of any matrix, because every component lies both in its <bookmark mark='f'/> row and in its <bookmark mark='c'/> column, which are vectors.""")) as tracker:
            self.wait_until_bookmark("g")
            self.play(*[ReplacementTransform(conclusion[p][g], general[p][g]) for p in range(5) for g in range(len(conclusion[p]))], run_time=1.5)
            # las tres i (fila) y después las tres j (columna), con los colores de las franjas; el resaltado
            # empieza en cuanto la voz dice la palabra (sin la subida lenta de Indicate) y dura hasta la siguiente
            ies = [general[p][g] for p, g in [(0, 1), (2, 0), (4, 0)]]
            jotas = [general[p][g] for p, g in [(0, 6), (2, 5), (4, 4)]]
            self.wait_until_bookmark("f")
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.5) for x in ies], run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in ies], *[x.animate.set_color(COLOR_C).scale(1.5) for x in jotas], run_time=0.25)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in jotas], run_time=0.4)
        
        self.wait(0.4)
        with self.voiceover(text=tr("""Lo habitual es escribir la componente con la letra de la matriz en minúscula y dos subíndices: <bookmark mark='i'/> primero el de la fila <bookmark mark='j'/> y después el de la columna.""",
                                    """The usual way is to write the component with the letter of the matrix in lower case and two subscripts: <bookmark mark='i'/> first the row <bookmark mark='j'/> and then the column.""")) as tracker:
            self.play(FadeOut(convenio), FadeOut(idea), FadeIn(comp[2:]), FadeIn(r_hab), run_time=1)
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
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        encabezados = [tr("fila $i$", "row $i$"), tr("componente $ij$", "component $ij$"), tr("columna $j$", "column $j$")]
        formulas = [r"\VectF{A}{i}\in\R[n]", r"\eleM{A}{i}{j}=a_{ij}", r"\VectC{A}{j}\in\R[m]"]
        tabla = VGroup(*[VGroup(Tex(e, tex_template=myTemplate, font_size=32, color=GRAY_B), MathTex(f, tex_template=myTemplate, font_size=44)).arrange(DOWN, buff=0.3)
                         for e, f in zip(encabezados, formulas)]).arrange(RIGHT, buff=1.2)
        asoc = VGroup(MathTex(r"\elemRp{\VectF{A}{i}}{j}=\elemLp{\VectC{A}{j}}{i}=\eleM{A}{i}{j}", tex_template=myTemplate, font_size=40),
                      Tex(tr("da igual el orden de selección", "the order of selection does not matter"), font_size=28, color=GRAY_B)).arrange(DOWN, buff=0.2)
        bloque = VGroup(tabla, asoc).arrange(DOWN, buff=0.6).move_to([0, 0.3, 0])
        
        # el operador se destaca cuando la voz dice por qué lado actúa (Marcos, 2026-10-27)
        # glifos: tabla[0][1] = i, |, A, ...;  tabla[1][1] = i, |, A, |, j, ...;  tabla[2][1] = A, |, j, ...
        sel_fila, sel_col = tabla[0][1][0][0:2], tabla[2][1][0][1:3]
        sel_comp = [tabla[1][1][0][0:2], tabla[1][1][0][3:5]]
        # «operador selector» una sola vez (antes, tres veces «Con el operador selector actuando»; Marcos, 2026-10-31)
        with self.voiceover(text=tr("""Resumamos. Con el operador selector actuando <bookmark mark='i'/> por la izquierda, seleccionamos una fila; <bookmark mark='d'/> por la derecha, una columna; <bookmark mark='a'/> y por ambos lados, una componente.""",
                                    """Let us sum up. With the selector operator acting <bookmark mark='i'/> on the left, we select a row; <bookmark mark='d'/> on the right, a column; <bookmark mark='a'/> and on both sides, a component.""")) as tracker:
            self.play(Write(cabecera), FadeIn(tabla[0]), run_time=1)
            self.wait_until_bookmark("i")
            self.play(Indicate(sel_fila, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("d")
            self.play(FadeIn(tabla[2]), run_time=0.4)   # FadeIn e Indicate a la vez dejaban el selector invisible
            self.play(Indicate(sel_col, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("a")
            self.play(FadeIn(tabla[1]), run_time=0.4)
            self.play(*[Indicate(g, color=COLOR_ESCALAR, scale_factor=1.6) for g in sel_comp], run_time=0.9)
        
        # Solo se mueve la expresión del medio (Marcos, 2026-11-03): la de la izquierda ya enseña «fila primero» y no debe
        # cambiar mientras la voz dice «la fila»; la del medio pasa a «fila primero» al decir «la fila» y vuelve a «columna
        # primero» al decir «o la columna». Para volver se transforma hacia una copia hecha al crearla (CLAUDE.md).
        # glifos de asoc[0][0]: ( i | A ) | j = i | ( A | j ) = i | A | j  (0-6, 7, 8-14, 15, 16-20)
        med = asoc[0][0][8:15]
        med_orig = med.copy()
        otra_med = MathTex(r"\elemRp{\VectF{A}{i}}{j}", tex_template=myTemplate, font_size=40).move_to(med)   # ( i | A ) | j
        parentesis = [med[2], med[6]]
        with self.voiceover(text=tr("""Y <bookmark mark='p'/> da igual seleccionar primero <bookmark mark='f'/> la fila <bookmark mark='c'/> o la columna.""",
                                    """And it makes no difference <bookmark mark='p'/> whether we select <bookmark mark='f'/> the row <bookmark mark='c'/> or the column first.""")) as tracker:
            self.play(FadeIn(asoc), run_time=0.6)
            self.wait_until_bookmark("p")
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.3) for x in parentesis], run_time=0.3)
            self.wait_until_bookmark("f")
            self.play(*[Transform(med[i], otra_med[0][j]) for i, j in zip(range(7), [1, 2, 0, 3, 5, 6, 4])], run_time=0.6)   # a «fila primero»
            self.wait_until_bookmark("c")
            self.play(*[Transform(med[i], med_orig[i]) for i in range(7)], run_time=0.6)   # de vuelta a «columna primero»
            self.play(*[x.animate.set_color(WHITE).scale(1/1.3) for x in parentesis], run_time=0.3)
        
        self.wait(0.5)   # una pausa antes de anunciar el próximo vídeo, como en V08
        # el anuncio solo anticipa: explicar el resultado lo dejaba incompleto o pisaba el vídeo siguiente (Marcos, 2026-10-31)
        # sin «como hicimos al formar la matriz B»: B no aparece en este vídeo (2026-11-03)
        with self.voiceover(text=tr("""En el próximo vídeo veremos la transposición, que convierte las filas de una matriz en las columnas de otra.""",
                                    """In the next video we will meet transposition, which turns the rows of a matrix into the columns of another.""")) as tracker:
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


class L01_V10_E01_FilasYColumnas(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=46).set_color(COLOR_TITULO)
        A = matriz(A_SEL, decimales=0, h_buff=1.0)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([0, 2.0, 0])
        x0 = -4.6
        col = MathTex(r"\VectC{A}{1}", r"\;=\;\begin{pmatrix}1\\ 7\end{pmatrix}", tex_template=myTemplate, font_size=48)
        fila = MathTex(r"\VectF{A}{1}", r"\;=\;(1,\ 2,\ 1,)", tex_template=myTemplate, font_size=48)
        for linea, y in [(col, 0.5), (fila, -1.5)]:   # hueco para la fila en vertical
            linea.move_to([x0 + linea.width/2, y, 0])
        fila.shift((col[1].get_left()[0] - fila[1].get_left()[0])*RIGHT)   # los dos "=" alineados
        # la columna y la fila, primero con un índice genérico (j, i) que pasa a ser 1 en el ejemplo
        col_g = MathTex(r"\VectC{A}{j}", tex_template=myTemplate, font_size=48)
        col_g.shift(col[0][0].get_center() - col_g[0][0].get_center())       # glifos: A, |, j
        fila_g = MathTex(r"\VectF{A}{i}", tex_template=myTemplate, font_size=48)
        fila_g.shift(fila[0][2].get_center() - fila_g[0][2].get_center())   # glifos: i, |, A
        # la otra forma de escribir la columna y la fila, detrás de un "=" (Marcos, 2026-10-27)
        col_h = MathTex(r"=(1,\ 7,)", font_size=48).next_to(col, RIGHT, buff=0.25)
        fila_v = MathTex(r"=\begin{pmatrix}1\\ 2\\ 1\end{pmatrix}", font_size=48).next_to(fila, RIGHT, buff=0.25)
        
        # al decir «el elemento de la lista», la matriz de números se transforma en la lista de sus tres columnas (la
        # notación de la escena 5) y al decir «una columna» la franja recorre los tres vectores; vuelve a los números al
        # empezar la frase siguiente (Marcos, 2026-11-03). Glifos de A_lista: [ ( 1 7 ) ; ( 2 0 ) ; ( 1 3 ) ; ]
        A_lista = MathTex(r"\left[\begin{pmatrix}1\\ 7\end{pmatrix};\ \begin{pmatrix}2\\ 0\end{pmatrix};\ \begin{pmatrix}1\\ 3\end{pmatrix};\right]",
                          tex_template=myTemplate, font_size=44).move_to(A).align_to(A, LEFT)
        vectores_lista = [A_lista[0][1:5], A_lista[0][6:10], A_lista[0][11:15]]
        A_num = A.copy()   # copia hecha antes de cualquier animación: A no vuelve a ser destino (CLAUDE.md)
        with self.voiceover(text=tr("""En este vídeo veremos la selección de filas, columnas y componentes de una matriz.""",
                                    """In this video we will see the selection of rows, columns and components of a matrix.""")) as tracker:
            self.play(Write(titulo), run_time=1.2)
        
        with self.voiceover(text=tr("""El operador selector también actúa sobre matrices. <bookmark mark='s'/> Con el índice a la derecha selecciona, como en los vectores, <bookmark mark='l'/> el elemento de la lista que ocupa esa posición: <bookmark mark='c'/> una columna.""",
                                    """The selector operator also acts on matrices. <bookmark mark='s'/> With the index on the right it selects, as with vectors, <bookmark mark='l'/> the element of the list in that position: <bookmark mark='c'/> a column.""")) as tracker:
            self.play(FadeIn(f_A), run_time=1)
            self.wait_until_bookmark("s")
            self.play(FadeIn(col_g), run_time=0.6)
            self.play(Indicate(col_g[0][1:3], color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("l")
            A_tmp = A.copy()
            self.remove(A); self.add(A_tmp)
            self.play(FadeTransform(A_tmp, A_lista), run_time=0.8)   # los números se convierten en la lista de vectores
            self.wait_until_bookmark("c")
            franja = None
            for v in vectores_lista:   # cada elemento de la lista es una columna
                nueva = SurroundingRectangle(v, color=COLOR_ESCALAR, fill_color=COLOR_ESCALAR, fill_opacity=0.22, stroke_width=0, buff=0.08)
                self.play(FadeIn(nueva) if franja is None else ReplacementTransform(franja, nueva), run_time=0.4)
                franja = nueva
            self.play(FadeOut(franja), run_time=0.3)
        
        with self.voiceover(text=tr("""Por ejemplo, con el índice uno, <bookmark mark='c'/> selecciona la primera columna.""",   # sin «de A»: solo hay una matriz (Marcos, 2026-11-03)
                                    """For example, with index one, <bookmark mark='c'/> it selects the first column.""")) as tracker:
            self.play(FadeTransform(A_lista, A_num), ReplacementTransform(col_g, col[0]), run_time=0.8)   # vuelven los números; j pasa a ser 1
            self.remove(A_num); self.add(A)   # el objeto original, intacto, para las franjas que vienen
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0)
            self.play(FadeIn(fc), FadeIn(col[1]), run_time=0.8)
        
        # el símbolo aparece un instante antes de que la voz lo describa (Marcos, 2026-10-18)
        self.play(FadeIn(fila_g), run_time=0.6)
        with self.voiceover(text=tr("""Y con el índice a la izquierda selecciona una fila. <bookmark mark='e'/> Por ejemplo, con el índice uno, <bookmark mark='f'/> selecciona la primera fila.""",
                                    """And with the index on the left it selects a row. <bookmark mark='e'/> For example, with index one, <bookmark mark='f'/> it selects the first row.""")) as tracker:
            self.play(Indicate(fila_g[0][0:2], color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("e")
            self.play(ReplacementTransform(fila_g, fila[0]), run_time=0.8)   # i pasa a ser 1
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 0)
            self.play(FadeIn(ff), FadeIn(fila[1]), run_time=0.8)
        
        with self.voiceover(text=tr("""Cada fila y cada columna es una lista ordenada de números, es decir, un vector.""",
                                    """Each row and each column is an ordered list of numbers, that is, a vector.""")) as tracker:
            self.play(Indicate(ff, color=COLOR_ESCALAR, scale_factor=1.05), run_time=1)
            self.play(Indicate(fc, color=COLOR_ESCALAR, scale_factor=1.05), run_time=1)
        
        self.wait(0.6)   # una pausa antes de la conclusión (Marcos, 2026-10-27)
        with self.voiceover(text=tr("""Por eso, una vez seleccionada, una fila o una columna <bookmark mark='h'/> se puede escribir tanto en horizontal como en vertical, <bookmark mark='p'/> siempre entre paréntesis.""",
                                    """So, once selected, a row or a column <bookmark mark='h'/> can be written either horizontally or vertically, <bookmark mark='p'/> always in parentheses.""")) as tracker:
            self.play(FadeOut(ff), FadeOut(fc), run_time=0.5)
            self.wait_until_bookmark("h")
            self.play(FadeIn(fila_v), FadeIn(col_h), run_time=1)
            self.wait_until_bookmark("p")
            # solo los vectores, sin los signos de igual (glifo 0 de cada parte; Marcos, 2026-11-02)
            self.play(*[Indicate(m, color=COLOR_ESCALAR, scale_factor=1.1) for m in (fila[1][1:], col[1][1:], fila_v[0][1:], col_h[0][1:])], run_time=1.2)
        
        self.pausa_media()


class L01_V10_E02_Componentes(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Componentes", "Components"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        A = matriz(A_SEL, decimales=0, h_buff=1.0)
        f_A = con_nombre(r"\Mat{A}=", A).move_to([0, 2.0, 0])
        por_fila = MathTex(r"\elemRp{\VectF{A}{2}}{1}", r"=", r"\elemR{(7,\ 0,\ 3,)}{1}", r"=", r"7", tex_template=myTemplate, font_size=48)
        por_col = MathTex(r"\elemLp{\VectC{A}{1}}{2}", r"=", r"\elemL{\begin{pmatrix}1\\ 7\end{pmatrix}}{2}", r"=", r"7", tex_template=myTemplate, font_size=48)
        lineas = columna_de_lineas([por_fila, por_col], x0=-1.6, y0=0.3, dy=1.45)
        # Glifos de cada línea: primero la fila (o la columna) seleccionada, después lo que la completa
        fila = VGroup(por_fila[0][1:4], por_fila[1], por_fila[2][:8])                       # 2|A = (7, 0, 3,)
        fila_resto = VGroup(por_fila[0][0], por_fila[0][4:], por_fila[2][8:], por_fila[3:])  # ( )|1, |1, = 7
        col = VGroup(por_col[0][3:6], por_col[1], por_col[2][2:])                            # A|1 = (1; 7)
        col_resto = VGroup(por_col[0][:3], por_col[0][6], por_col[2][:2], por_col[3:])       # 2|( ), 2|, = 7
        convenio = MathTex(r"\eleVL{a}{i}", r"=", r"\eleVR{a}{i}", r"=", r"a_i", tex_template=myTemplate, font_size=52).move_to([0.8, -2.7, 0])
        idea = aviso("idea").next_to(convenio, LEFT, buff=0.8)
        conclusion = MathTex(r"\elemRp{\VectF{A}{2}}{1}", r"=", r"\elemLp{\VectC{A}{1}}{2}", r"=", r"\eleM{A}{2}{1}",
                             tex_template=myTemplate, font_size=52).move_to([0, 0.2, 0])
        general = MathTex(r"\elemRp{\VectF{A}{i}}{j}", r"=", r"\elemLp{\VectC{A}{j}}{i}", r"=", r"\eleM{A}{i}{j}",
                          tex_template=myTemplate, font_size=52).move_to(conclusion)   # mismos glifos: el 2 pasa a i y el 1 a j
        # lo habitual en los libros (a_21) frente al selector, en el ejemplo (como en la escena 3 de V01)
        comp = MathTex(r"\eleM{A}{2}{1}", r"\;=\;", r"a_{21}", r"\;=\;7", tex_template=myTemplate, font_size=48).move_to([0, -1.7, 0])
        r_hab = Tex(tr("lo habitual", "the usual way"), font_size=28, color=GRAY_B).next_to(comp[2], UP, buff=0.2)
        r_sel = Tex(tr("selector", "selector"), font_size=28, color=GRAY_B).next_to(comp[0], UP, buff=0.2)
        # glifos: a_{21} = a, 2, 1; 2|A|1 = 2, |, A, |, 1
        sub_f, sub_c = comp[2][1], comp[2][2]
        sel_i, sel_d = comp[0][0:2], comp[0][3:5]
        
        with self.voiceover(text=tr("""Cada componente de una matriz está a la vez <bookmark mark='f'/> en una fila y <bookmark mark='c'/> en una columna.""",
                                    """Each component of a matrix lies both <bookmark mark='f'/> in a row and <bookmark mark='c'/> in a column.""")) as tracker:
            self.play(Write(cabecera), FadeIn(f_A), run_time=1)
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 1)
            self.play(FadeIn(ff), run_time=0.5)
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0, color=COLOR_C)
            self.play(FadeIn(fc), run_time=0.5)
            self.play(Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
        
        with self.voiceover(text=tr("""El siete, por ejemplo, es componente de dos vectores distintos: <bookmark mark='f'/> es la primera componente de la segunda fila, <bookmark mark='c'/> y la segunda componente de la primera columna.""",
                                    """The seven, for example, is a component of two different vectors: <bookmark mark='f'/> it is the first component of the second row, <bookmark mark='c'/> and the second component of the first column.""")) as tracker:
            self.play(Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=0.8)
            self.wait_until_bookmark("f")
            self.play(ff.animate.set_fill(opacity=0.55), fc.animate.set_fill(opacity=0.06), run_time=0.5)
            self.wait_until_bookmark("c")
            self.play(ff.animate.set_fill(opacity=0.06), fc.animate.set_fill(opacity=0.55), run_time=0.5)
        self.play(FadeOut(ff), FadeOut(fc), run_time=0.5)
        
        with self.voiceover(text=tr("""Obtengamos el siete de las dos maneras. Seleccionemos primero <bookmark mark='f'/> la fila, <bookmark mark='c'/> y después su primera componente.""",
                                    """Let us get the seven in both ways. First, let us select <bookmark mark='f'/> the row, <bookmark mark='c'/> and then its first component.""")) as tracker:
            self.wait_until_bookmark("f")
            ff = franja_fila(A, 1)
            self.play(FadeIn(ff), FadeIn(fila), run_time=0.8)
            self.wait_until_bookmark("c")
            self.play(FadeIn(fila_resto), Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=1)
        
        with self.voiceover(text=tr("""Ahora seleccionemos primero <bookmark mark='c'/> la columna, <bookmark mark='s'/> y después su segunda componente: <bookmark mark='v'/> también obtenemos el siete.""",
                                    """Now let us first select <bookmark mark='c'/> the column, <bookmark mark='s'/> and then its second component: <bookmark mark='v'/> we get the seven again.""")) as tracker:
            self.play(FadeOut(ff), run_time=0.8)
            self.wait_until_bookmark("c")
            fc = franja_columna(A, 0, color=COLOR_C)
            self.play(FadeIn(fc), FadeIn(col), run_time=0.8)
            self.wait_until_bookmark("s")
            self.play(FadeIn(col_resto), Indicate(A.get_rows()[1][0], color=COLOR_ESCALAR, scale_factor=1.4), run_time=1)
            self.wait_until_bookmark("v")   # los dos caminos acaban en el mismo siete (Marcos, 2026-11-01)
            self.play(*[Indicate(x, color=COLOR_ESCALAR, scale_factor=1.4) for x in (por_fila[4], por_col[4], A.get_rows()[1][0])], run_time=1.2)
        
        with self.voiceover(text=tr("""Aquí el selector actúa por la izquierda de un vector. <bookmark mark='a'/> Ya en el primer vídeo del curso admitimos que el selector puede actuar por cualquier lado de un vector, <bookmark mark='d'/> con el mismo resultado.""",
                                    """Here the selector acts on the left of a vector. <bookmark mark='a'/> Back in the first video of the course, we agreed that the selector can act on either side of a vector, <bookmark mark='d'/> with the same result.""")) as tracker:
            sel_izq = VGroup(por_col[0][:2], por_col[2][:2])  # los dos selectores por la izquierda, resaltados toda la frase
            self.play(FadeOut(fc), *[s.animate.set_color(COLOR_ESCALAR).scale(1.25) for s in sel_izq], run_time=0.6)
            self.wait_until_bookmark("a")
            self.play(*[s.animate.set_color(WHITE).scale(1/1.25) for s in sel_izq], FadeIn(idea), FadeIn(convenio[0]), run_time=0.8)
            self.wait_until_bookmark("d")
            self.play(FadeIn(convenio[1:]), run_time=0.8)
        
        # la asociatividad del selector justifica la notación sin paréntesis (Marcos, 2026-10-31)
        # glifos: conclusion[0] = ( 2 | A ) | 1 (paréntesis 0 y 4); conclusion[2] = 2 | ( A | 1 ) (paréntesis 2 y 6)
        parentesis = [conclusion[0][0], conclusion[0][4], conclusion[2][2], conclusion[2][6]]
        with self.voiceover(text=tr("""Con este convenio, da igual seleccionar primero la fila o la columna: <bookmark mark='p'/> podemos desplazar los paréntesis sin cambiar el resultado.""",
                                    """With this convention, it makes no difference whether we select the row or the column first: <bookmark mark='p'/> we can move the parentheses without changing the result.""")) as tracker:
            self.play(ReplacementTransform(por_fila[0], conclusion[0]), ReplacementTransform(por_col[0], conclusion[2]), FadeIn(conclusion[1]),
                      FadeOut(VGroup(por_fila[1:], por_col[1:])), run_time=1.2)
            self.wait_until_bookmark("p")
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.3) for x in parentesis], run_time=0.3)
            # como en V04: los glifos de la izquierda van a las posiciones de la derecha y vuelven
            destino = conclusion[2].copy().move_to(conclusion[0])
            self.play(*[Transform(conclusion[0][i], destino[j], rate_func=rate_functions.there_and_back_with_pause)
                        for i, j in zip(range(7), [2, 0, 1, 3, 6, 4, 5])], run_time=2.2)
        
        with self.voiceover(text=tr("""Es una propiedad asociativa, como la del producto por un escalar. <bookmark mark='q'/> Por eso podemos escribir el selector a ambos lados de la matriz, sin paréntesis.""",
                                    """It is an associative property, like that of scalar multiplication. <bookmark mark='q'/> That is why we can write the selector on both sides of the matrix, with no parentheses.""")) as tracker:
            self.wait_until_bookmark("q")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.3) for x in parentesis], run_time=0.3)
            self.play(FadeIn(conclusion[3:]), run_time=1)
        
        with self.voiceover(text=tr("""Lo hemos visto en un ejemplo, pero <bookmark mark='g'/> vale para cualquier componente de cualquier matriz, porque toda componente está a la vez en su <bookmark mark='f'/> fila y en su <bookmark mark='c'/> columna, que son vectores.""",
                                    """We have seen it in an example, but <bookmark mark='g'/> it holds for any component of any matrix, because every component lies both in its <bookmark mark='f'/> row and in its <bookmark mark='c'/> column, which are vectors.""")) as tracker:
            self.wait_until_bookmark("g")
            self.play(*[ReplacementTransform(conclusion[p][g], general[p][g]) for p in range(5) for g in range(len(conclusion[p]))], run_time=1.5)
            # las tres i (fila) y después las tres j (columna), con los colores de las franjas; el resaltado
            # empieza en cuanto la voz dice la palabra (sin la subida lenta de Indicate) y dura hasta la siguiente
            ies = [general[p][g] for p, g in [(0, 1), (2, 0), (4, 0)]]
            jotas = [general[p][g] for p, g in [(0, 6), (2, 5), (4, 4)]]
            self.wait_until_bookmark("f")
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.5) for x in ies], run_time=0.25)
            self.wait_until_bookmark("c")
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in ies], *[x.animate.set_color(COLOR_C).scale(1.5) for x in jotas], run_time=0.25)
            self.wait(0.8)
            self.play(*[x.animate.set_color(WHITE).scale(1/1.5) for x in jotas], run_time=0.4)
        
        self.wait(0.4)
        with self.voiceover(text=tr("""Lo habitual es escribir la componente con la letra de la matriz en minúscula y dos subíndices: <bookmark mark='i'/> primero el de la fila <bookmark mark='j'/> y después el de la columna.""",
                                    """The usual way is to write the component with the letter of the matrix in lower case and two subscripts: <bookmark mark='i'/> first the row <bookmark mark='j'/> and then the column.""")) as tracker:
            self.play(FadeOut(convenio), FadeOut(idea), FadeIn(comp[2:]), FadeIn(r_hab), run_time=1)
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
        
        self.pausa_media()


class L01_V10_E03_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Resumen", "Key Takeaways"), font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        encabezados = [tr("fila $i$", "row $i$"), tr("componente $ij$", "component $ij$"), tr("columna $j$", "column $j$")]
        formulas = [r"\VectF{A}{i}\in\R[n]", r"\eleM{A}{i}{j}=a_{ij}", r"\VectC{A}{j}\in\R[m]"]
        tabla = VGroup(*[VGroup(Tex(e, tex_template=myTemplate, font_size=32, color=GRAY_B), MathTex(f, tex_template=myTemplate, font_size=44)).arrange(DOWN, buff=0.3)
                         for e, f in zip(encabezados, formulas)]).arrange(RIGHT, buff=1.2)
        asoc = VGroup(MathTex(r"\elemRp{\VectF{A}{i}}{j}=\elemLp{\VectC{A}{j}}{i}=\eleM{A}{i}{j}", tex_template=myTemplate, font_size=40),
                      Tex(tr("da igual el orden de selección", "the order of selection does not matter"), font_size=28, color=GRAY_B)).arrange(DOWN, buff=0.2)
        bloque = VGroup(tabla, asoc).arrange(DOWN, buff=0.6).move_to([0, 0.3, 0])
        
        # el operador se destaca cuando la voz dice por qué lado actúa (Marcos, 2026-10-27)
        # glifos: tabla[0][1] = i, |, A, ...;  tabla[1][1] = i, |, A, |, j, ...;  tabla[2][1] = A, |, j, ...
        sel_fila, sel_col = tabla[0][1][0][0:2], tabla[2][1][0][1:3]
        sel_comp = [tabla[1][1][0][0:2], tabla[1][1][0][3:5]]
        # «operador selector» una sola vez (antes, tres veces «Con el operador selector actuando»; Marcos, 2026-10-31)
        with self.voiceover(text=tr("""Resumamos. Con el operador selector actuando <bookmark mark='i'/> por la izquierda, seleccionamos una fila; <bookmark mark='d'/> por la derecha, una columna; <bookmark mark='a'/> y por ambos lados, una componente.""",
                                    """Let us sum up. With the selector operator acting <bookmark mark='i'/> on the left, we select a row; <bookmark mark='d'/> on the right, a column; <bookmark mark='a'/> and on both sides, a component.""")) as tracker:
            self.play(Write(cabecera), FadeIn(tabla[0]), run_time=1)
            self.wait_until_bookmark("i")
            self.play(Indicate(sel_fila, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("d")
            self.play(FadeIn(tabla[2]), run_time=0.4)   # FadeIn e Indicate a la vez dejaban el selector invisible
            self.play(Indicate(sel_col, color=COLOR_ESCALAR, scale_factor=1.6), run_time=0.9)
            self.wait_until_bookmark("a")
            self.play(FadeIn(tabla[1]), run_time=0.4)
            self.play(*[Indicate(g, color=COLOR_ESCALAR, scale_factor=1.6) for g in sel_comp], run_time=0.9)
        
        # Solo se mueve la expresión del medio (Marcos, 2026-11-03): la de la izquierda ya enseña «fila primero» y no debe
        # cambiar mientras la voz dice «la fila»; la del medio pasa a «fila primero» al decir «la fila» y vuelve a «columna
        # primero» al decir «o la columna». Para volver se transforma hacia una copia hecha al crearla (CLAUDE.md).
        # glifos de asoc[0][0]: ( i | A ) | j = i | ( A | j ) = i | A | j  (0-6, 7, 8-14, 15, 16-20)
        med = asoc[0][0][8:15]
        med_orig = med.copy()
        otra_med = MathTex(r"\elemRp{\VectF{A}{i}}{j}", tex_template=myTemplate, font_size=40).move_to(med)   # ( i | A ) | j
        parentesis = [med[2], med[6]]
        with self.voiceover(text=tr("""Y <bookmark mark='p'/> da igual seleccionar primero <bookmark mark='f'/> la fila <bookmark mark='c'/> o la columna.""",
                                    """And it makes no difference <bookmark mark='p'/> whether we select <bookmark mark='f'/> the row <bookmark mark='c'/> or the column first.""")) as tracker:
            self.play(FadeIn(asoc), run_time=0.6)
            self.wait_until_bookmark("p")
            self.play(*[x.animate.set_color(COLOR_ESCALAR).scale(1.3) for x in parentesis], run_time=0.3)
            self.wait_until_bookmark("f")
            self.play(*[Transform(med[i], otra_med[0][j]) for i, j in zip(range(7), [1, 2, 0, 3, 5, 6, 4])], run_time=0.6)   # a «fila primero»
            self.wait_until_bookmark("c")
            self.play(*[Transform(med[i], med_orig[i]) for i in range(7)], run_time=0.6)   # de vuelta a «columna primero»
            self.play(*[x.animate.set_color(WHITE).scale(1/1.3) for x in parentesis], run_time=0.3)
        
        self.wait(0.5)   # una pausa antes de anunciar el próximo vídeo, como en V08
        # el anuncio solo anticipa: explicar el resultado lo dejaba incompleto o pisaba el vídeo siguiente (Marcos, 2026-10-31)
        # sin «como hicimos al formar la matriz B»: B no aparece en este vídeo (2026-11-03)
        with self.voiceover(text=tr("""En el próximo vídeo veremos la transposición, que convierte las filas de una matriz en las columnas de otra.""",
                                    """In the next video we will meet transposition, which turns the rows of a matrix into the columns of another.""")) as tracker:
            pass
        
        self.pausa_media()


class ZCreditosFinales(CreditosFinales):   # manim solo renderiza clases definidas en este fichero
    pass
