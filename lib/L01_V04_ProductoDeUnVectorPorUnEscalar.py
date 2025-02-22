from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService
import nacal as nc
import sympy as sp
# PARA LA TRADUCCIÓN (pero no sé generar los vídeos traducidos)
from manim_voiceover.translate import get_gettext
# It is good practice to get the LOCALE and DOMAIN from environment variables
import os
LOCALE = os.getenv("LOCALE")
DOMAIN = os.getenv("DOMAIN")
# The following function uses LOCALE and DOMAIN to set the language, and
# returns a gettext function that is used to insert translations.
_ = get_gettext()
#from manim import *
#from manim_voiceover import VoiceoverScene
#from manim_voiceover.services.gtts import GTTSService
#import nacal as nc
#import sympy as sp
#
## PARA LA TRADUCCIÓN (pero no sé generar los vídeos traducidos)
#from manim_voiceover.translate import get_gettext
## It is good practice to get the LOCALE and DOMAIN from environment variables
#import os
#LOCALE = os.getenv("LOCALE")
#DOMAIN = os.getenv("DOMAIN")
## The following function uses LOCALE and DOMAIN to set the language, and
## returns a gettext function that is used to insert translations.
#_ = get_gettext()

class MiEscenaConVoz(VoiceoverScene):
    def pausa_muy_corta(self, n=0.3):
        self.wait(n)
    def pausa_corta(self, n=0.5):
        self.wait(n)
    def pausa(self, n=1):
        self.wait(n)
    def pausa_media(self, n=1.5):
        self.wait(n)
    def pausa_larga(self, n=3):
        self.wait(n)
    def pausa_muy_larga(self, n=5):
        self.wait(n)

    def creditos(self, variante=1):
        def analisis_opcion_elegida(tipo):
            'Análisis de las opciones de eliminación elegidas'
            lista = [100,20,10,4,2,1]
            opcion = set()
            for t in lista:
                if (tipo - (tipo % t)) in lista:
                    opcion.add(tipo - (tipo % t))
                    tipo = tipo % t
            return opcion    
        copyright = Tex(r"\textcopyright{\;} 2025\; Marcos Bujosa  ")
        if 1 in analisis_opcion_elegida(variante):
            stampDcha  = VGroup(copyright.copy()).rotate( PI/2).scale(0.5).to_edge(RIGHT, buff=0.1).set_color(GRAY_D)
            self.add(stampDcha)
        if 2 in analisis_opcion_elegida(variante):
            stampIzda  = VGroup(copyright.copy()).rotate(-PI/2).scale(0.5).to_edge(LEFT, buff=0.1).set_color(GRAY_D)
            self.add(stampIzda)
        if 4 in analisis_opcion_elegida(variante):
            stampBottom= VGroup(copyright.copy()).rotate(    0).scale(0.5).to_edge(DOWN, buff=0.1).set_color(GRAY_D)
            self.add(stampBottom)
        if 10 in analisis_opcion_elegida(variante):
            stampTop   = VGroup(copyright.copy()).rotate(    0).scale(0.5).to_edge(  UP, buff=0.1).set_color(GRAY_D)
            self.add(stampTop)
            
         

class VectorR2():
    def __init__(self, lista, rpr='c', color=GRAY_B):
        """Inicializa un Vector con una lista"""
        coords = lista + [0] if len(lista)<3 else lista        
        self.color  = color
        #self.coords = tuple(coords)
        #self.coords = tuple([float(i) for i in coords])
        self.coords = tuple([int(i) if float(i)==int(i) else float(i) for i in coords])
        self.Vector = nc.Vector(self.coords[:2], rpr)
        self.tex    = MathTex(self.Vector.latex(), color=self.color).scale(0.8)

    def dot(self, ejes, radio=0.08):
        return Dot(ejes.c2p(*self.coords), radius=radio, color=self.color)

    def v_line(self, ejes):
        return ejes.get_vertical_line(ejes.c2p(*self.coords), color=self.color)

    def h_line(self, ejes):
        return ejes.get_horizontal_line(ejes.c2p(*self.coords), color=self.color)

    def arrow(self, ejes):
        return ejes.get_vector(self.Vector.lista, stroke_color = self.color, stroke_width=4)
        

class VectorR3():
    def __init__(self, lista, rpr='c', color=GRAY_B):
        """Inicializa un Vector con una lista"""
        coords = lista + [0] if len(lista)<3 else lista
        self.color  = color
        #self.coords = tuple(coords)
        self.coords = tuple([int(i) if float(i)==int(i) else float(i) for i in coords])
        self.Vector = nc.Vector(self.coords, rpr)
        self.tex    = MathTex(self.Vector.latex(), color=self.color).scale(0.8)
        self.proyXY = self.coords[:-1] + (0,)
        self.proyZ  = (0,0,) + (self.coords[-1],)

    def dot(self, ejes, radio=0.08):
        return Dot3D(ejes.c2p(*self.coords), radius=radio, color=self.color)

    def x_line(self, ejes):
        return ejes.get_vertical_line(ejes.c2p(*self.proyXY), color=self.color)
    
    def y_line(self, ejes):
        return ejes.get_horizontal_line(ejes.c2p(*self.proyXY), color=self.color)
    
    def z_line(self, ejes):
        return Line3D(start=ejes.c2p(*self.proyZ), end=ejes.c2p(*self.coords), thickness=0.01)
    
    def v_line(self, ejes):
        return Line3D(start=ejes.c2p(*self.proyXY), end=ejes.c2p(*self.coords), thickness=0.01)
    
    def xy_line(self, ejes):
        return Line3D(start=np.array([0,0,0]), end=ejes.c2p(*self.proyXY), thickness=0.01)
    
    def proy_x_line(self, ejes):
        return ejes.get_horizontal_line(ejes.c2p(*self.proyXY), color=self.color)
    
    def proy_y_line(self, ejes):
        return ejes.get_horizontal_line(ejes.c2p(*self.coords), color=self.color)

    def proy_y_line(self, ejes):
        return Line3D(start=ejes.c2p(*self.proyZ), end=ejes.c2p(*self.coords), thickness=0.01)

    def arrow(self, ejes):
        return Arrow3D(
            start=np.array([0, 0, 0]),
            end=np.array(ejes.c2p(*self.coords)),
            resolution=8,
            color = self.color )

class ZCreditos(Scene):
    def construct(self):
        copyright = Tex(r"\textcopyright{\;} 2025 \; Marcos Bujosa")
        github = Tex(r"\texttt{https://github.com/mbujosab}").next_to(copyright, DOWN)
        CGG  = VGroup(copyright,github).scale(1.1)
        self.add(CGG)
        self.wait(10)

class L01_V04_E01_ProductoPorEscalares(MiEscenaConVoz):    
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))       
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)

        self.creditos()
        
        # Portada
        titulo = Title(_("Producto de vectores de ") + r"\R[n]" + _("por escalares"),
                     tex_template = myTemplate,
                     font_size=70).set_color(BLUE)
        self.play(Write(titulo))
        self.pausa_media()
        self.play(FadeOut(titulo))
	
        operacionProducto = Tex(_("Producto por escalares"),
                         tex_template = myTemplate, font_size=70
                         ).to_edge(UP).set_color(BLUE)

        operacionDescripcion = Tex(_("El producto se define componente a componente."),
                         tex_template = myTemplate,
                         ).move_to([0,2.5,0]).to_edge(LEFT)
        # Ejemplos
        EjR3 = Tex(r"\textbf{" + _("Ejemplo en ") + r"\R[3]:}",
                 tex_template = myTemplate,
                 font_size=50).set_color(GREEN).next_to(operacionDescripcion, DOWN, aligned_edge=LEFT)

        EjR4 = Tex(r"\textbf{" + _("Ejemplo en ") + r"\R[4]:}",
                 tex_template = myTemplate,
                 font_size=50).set_color(GREEN).next_to(operacionDescripcion, DOWN, aligned_edge=LEFT)
        
        a    = 3
        b    = nc.Vector( [0, 1, 2])        
        s1 = MathTex(a,                tex_template = myTemplate,)
        por= MathTex(r"\cdot",         tex_template = myTemplate,)
        s3 = MathTex(b.latex(),        tex_template = myTemplate,)
        igual = MathTex(r"=",          tex_template = myTemplate,)
        s5 = MathTex((a*b).latex(),    tex_template = myTemplate,)
        grp1 = VGroup(s1,por,s3,igual,s5).arrange(RIGHT)
       
        with self.voiceover(text=_("""Además de sumar vectores,""")) as tracker:
            self.pausa_corta(tracker.duration)
            
        self.add(operacionProducto)
        self.add(operacionDescripcion)

        with self.voiceover(text=_("""también podemos reescalarlos, es decir, podemos multiplicarlos
        por algún escalar para obtener un múltiplo del vector original.""")) as tracker:
            self.add(EjR3)
            self.play(FadeIn(grp1[2]), run_time=tracker.duration/4)
            self.play(FadeIn(grp1[:2]), run_time=tracker.duration*3/4)

        with self.voiceover(text=_("""El resultado es otro vector que se define componente a
        componente.""")) as tracker:
            self.pausa_media()
            self.add(grp1[3])
            self.add(grp1[4][0][:2])
            self.add(grp1[4][0][-2:])

        with self.voiceover(text=_("""La primera componente del múltiplo es el producto del escalar
        por la primera componente del vector.""")) as tracker:
            self.play(FadeIn(grp1[4][0][2]), run_time=tracker.duration/3)
            self.play(Circumscribe(grp1[0]),
                      Circumscribe(grp1[2][0][2]),
                      Indicate(grp1[4][0][2]),                      
                      run_time=tracker.duration*2/3)
            self.pausa_corta()
            
        with self.voiceover(text=_("""De manera similar se calculan tanto la segunda
        componente, como las restantes componentes del múltiplo del vector.""")) as tracker:
            self.play(FadeIn(grp1[4][0][3]), run_time=tracker.duration/3)
            self.play(Circumscribe(grp1[0]),
                      Circumscribe(grp1[2][0][3]),
                      Indicate(grp1[4][0][3]),
                      run_time=tracker.duration/3)
            self.play(FadeIn(grp1[4][0][4]),
                      run_time=tracker.duration/6)
            self.play(Circumscribe(grp1[0]),
                      Circumscribe(grp1[2][0][4]),
                      Indicate(grp1[4][0][4]),
                      run_time=tracker.duration/3 )
            self.pausa_muy_corta()
            self.play(FadeOut(grp1))

        escalar = sp.symbols('\lambda')
        vga = MathTex(escalar, tex_template = myTemplate)
        
        v_generico_b  = nc.Vector(sp.symbols('b:5')[1:])
        vgb = MathTex(v_generico_b.latex(), tex_template = myTemplate)

        vgab = MathTex((escalar * v_generico_b).latex(), tex_template = myTemplate)

        grp2 = VGroup(vga,por,vgb,igual,vgab).arrange(RIGHT)
        with self.voiceover(text=_("""Así, la siguiente expresión describe
        el producto de un vector de R 4 por un escalar.""")) as tracker:
            self.play(FadeTransform(EjR3,EjR4))
            self.play(FadeIn(grp2))
            self.pausa()

        with self.voiceover(text=_("""Lo habitual es simplificar la notación,
        omitiendo el punto que denota la operación producto""")) as tracker:
            self.pausa(tracker.duration/3)
            self.play(FadeOut(grp2[1]),
                      grp2[0].animate.move_to(grp2[1]),
                      run_time=2*tracker.duration/3)
            self.pausa_muy_corta()
            
        with self.voiceover(text=_("""Como en el caso de la suma,""")) as tracker:
            self.pausa(tracker.duration)

        with self.voiceover(text=_("""para definir la operación en R n necesitamos una
        estrategia que no requiera escribir la lista de componentes. Recuerde que n puede
        ser muy grande.""")) as tracker:
            self.wait(tracker.duration/6)
            self.play(Indicate(vga[0][4:-4]),
                      Indicate(vgb[0][4:-4]),
                      Indicate(vgab[0][4:-4]),
                      run_time=2*tracker.duration/3)
            self.wait(1.5*tracker.duration/6)

        Defn = Tex(r"\textbf{" + _("Definición") + ":}",
                 tex_template = myTemplate,
                 font_size=50).set_color(RED).next_to(operacionDescripcion,
                                                      DOWN,
                                                      aligned_edge=LEFT)
        
        with self.voiceover(text=_("""Una alternativa es definir el producto usando el operador
        selector. Con ella podemos expresar""")) as tracker:
            self.play(FadeOut(grp2),
                      FadeOut(EjR4),
                      run_time=tracker.duration/3)
            self.add(Defn)

        cvab = MathTex(r"\elemRp{\lambda\Vect{a}}{i}", tex_template = myTemplate)
        cvb  = MathTex(r"\lambda\eleVRpE{a}{i}", tex_template = myTemplate)
        eq_suma = VGroup(cvab,igual,cvb).arrange(RIGHT).scale(1.5)
        
        donde = Tex(_("donde"))
        indices = MathTex(r"i=1:n", tex_template = myTemplate)
        pc_indices = VGroup(donde,indices).arrange(RIGHT, buff=1)
        grp3 = VGroup(eq_suma, pc_indices).arrange(RIGHT, buff=1)

        with self.voiceover(text=_("""que la i-ésima componente del
        múltiplo del vector es igual""")) as tracker:
            
            self.play(FadeIn(grp3[0][0],
                             scale=1.5,
                             rate_func=rate_functions.exponential_decay),
                      run_time=tracker.duration-1.5)            
            self.play(FadeIn(grp3[0][1],
                             scale=1.5,
                             rate_func=rate_functions.exponential_decay))

        with self.voiceover(text=_("""al escalar por la i-ésima
        componente del vector.""")) as tracker:

            self.play(FadeIn(grp3[0][2:],
                             scale=0.5,
                             rate_func=rate_functions.exponential_decay),
                      run_time=tracker.duration+0.2)

        with self.voiceover(text=_(r"""(donde el índice recorre los números naturales entre uno
        y n)""")) as tracker:
            self.play(FadeIn(grp3[1]))
            self.pausa_corta()

        with self.voiceover(text=_(r"""Esta definición abstracta  arroja una segunda regla de
        cálculo simbólico:""")) as tracker:
            self.pausa(tracker.duration*2/3)
            self.play(Indicate(eq_suma[0][0][0]),
                      Indicate(eq_suma[0][0][3]),
                      Indicate(eq_suma[2][0][1]),
                      Indicate(eq_suma[2][0][5]),
                      run_time=tracker.duration/3)
            self.pausa_muy_corta()

        with self.voiceover(text=_(r"""que la i-ésima componente del producto se puede sustituir por
        el producto del escalar por la i-ésima componente.""")) as tracker:            
            source0 = MathTex(r"\elemRp{\lambda\Vect{a}}{i}",
                              tex_template = myTemplate).next_to(grp3, DOWN, buff=1.2).scale(2)[0]
            target0 = MathTex(r"\lambda\eleVRpE{a}{i}",
                              tex_template = myTemplate).next_to(grp3, DOWN, buff=1.2).scale(2)[0]
            source1 = target0.copy()
            target1 = source0.copy()

            source2 = source0.copy()
            target2 = target0.copy()

            VG0 = VGroup(source0,target0)
            self.add(source0)
            transform_index0 = [[0,1,2,3,4,5],
                                [1,0,2,5,3,4]]
            self.play(
                *[
                    ReplacementTransform(source0[i],target0[j], rate_func=rate_functions.smooth)
                    for i,j in zip(*transform_index0)
                ],
                run_time=tracker.duration)
            
        with self.voiceover(text=_("""Y que el escalar por la i-ésima componente se puede
        sustituir por la i-ésima componente del producto.""")) as tracker:            
            self.play(ReplacementTransform(target0,source1))
            
            VG1 = VGroup(source1,target1)
            transform_index1 = [[0,1,2,3,4,5],
                                [1,0,2,4,5,3]]
            self.play(
                *[
                    ReplacementTransform(source1[i],target1[j], rate_func=rate_functions.smooth)
                    for i,j in zip(*transform_index1)
                ],
                run_time=tracker.duration)
            
        with self.voiceover(text=_("""Es decir, que los paréntesis pueden desplazarse para dejar
        fuera al escalar y dentro el operador selector, y viceversa.""")) as tracker:
            self.play(ReplacementTransform(target1,source2))
            VG2 = VGroup(source2,target2)
            self.play(
                *[
                    ReplacementTransform(source2[i],target2[j], rate_func=rate_functions.there_and_back_with_pause)
                    for i,j in zip(*transform_index0)
                ],
                run_time=tracker.duration)
	    
        with self.voiceover(text=_("""Esta regla se denomina propiedad asociativa del operador selector
        respecto del producto.""")) as tracker:            
            self.remove(target1,source2,target2)
            self.play(Indicate(eq_suma[0][0][0]),
                      Indicate(eq_suma[0][0][3]),
                      Indicate(eq_suma[2][0][1]),
                      Indicate(eq_suma[2][0][5]),
                      run_time=tracker.duration)
            self.play(FadeOut(grp3), run_time=0.3)
            self.pausa_muy_corta()

        with self.voiceover(text=_("""Por tanto, los paréntesis no son
        necesarios, pues la expresión sin ellos tiene pleno sentido;
        tal y como ocurre con el producto entre números.""")) as tracker:
            
            target3 = MathTex(r"\lambda\eleVR{a}{i}",
                              tex_template = myTemplate).next_to(grp3, DOWN, buff=0).scale(1.5)[0]
            grp4 = VGroup(cvab,igual,cvb,igual.copy(),target3).arrange(RIGHT, buff=1)

            producto = MathTex(r"(ab)c\;=\;a(bc)\;=\;abc",
                               tex_template = myTemplate).next_to(grp4, DOWN, buff=1.2).scale(1.5)[0]

            self.play(FadeIn(grp4),
                      run_time=tracker.duration/3)
            
            self.play(Indicate(target3), run_time=tracker.duration/3)

            self.play(FadeIn(producto))
            
            self.pausa(tracker.duration/3+1)

class L01_V04_E02_InterpretacionGeometricaDelProductoDeDosNumeros(MiEscenaConVoz):   
    
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))        
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)
       
        cabecera = Tex(_("Interpretación geométrica del producto"),
                            tex_template = myTemplate,
                            font_size=70).to_edge(UP).set_color(BLUE)

        cabecera2 = Tex(_("Interpretación geométrica del producto de números"),
                       tex_template = myTemplate,
                       font_size=70).to_edge(UP).set_color(BLUE).scale(0.6).shift(0.1*UP)
        
        def coordenada_x(x,ax, label='', pos=0):
            if x==int(x):
                xlabel = (ax[0][2][int(x)-1]).copy()
            else:
                label = label if label else f"{x}"
                xlabel = Tex(label, font_size=30)
                pos_label = UP if pos else DOWN
                xlabel.next_to(ax.c2p(x,0), pos_label, buff=0.6)
            return xlabel

        def coordenada_y(y,ax, label='', pos=0):
            if y==int(y):
                ylabel = (ax[1][2][int(y)-1]).copy()
            else:
                label = label if label else f"{y}"
                ylabel = Tex(label, font_size=30)
                pos_label = RIGHT if pos else LEFT
                ylabel.next_to(ax.c2p(0,y), pos_label, buff=0.5)
            return ylabel
                
        coordenadas_xy = lambda x,y,ax,labelx='',labely='',posx=0,posy=0: (coordenada_x(x,ax,labelx,posx),
                                                                           coordenada_y(y,ax,labely,posy))
        
        def retículaProducto(a, b: int, ax: Axes) -> VGroup:
            def cuadricula(a: int, b: int, ax: Axes):
                base = VGroup(*[Square().scale(0.5) for s in range(0,int(a*b))])
                base.arrange_in_grid(rows=b,
                                     flow_order="ru",
                                     buff=0).next_to(ax.coords_to_point(0, 0),
                                                     UR,
                                                     buff=0)
                return Group(*[base[c[0]:c[1]] for c in [(a*i,a*(i+1)) for i in range(b)]])
            
            def rectangulo(a, b: int, ax: Axes):
                base  = VGroup(*[Rectangle(height=2.0, width=2.0*a).scale(0.5) for s in range(0,b)])
                posicion = UR if a>0 else UL
                tabla = base.arrange_in_grid(rows=b,
                                             flow_order="ru",
                                             buff=0).next_to(ax.coords_to_point(0, 0),
                                                             posicion,
                                                             buff=0)
                return tabla
            return cuadricula(a, b, ax) if isinstance(a, int) else rectangulo(a, b, ax)

        def productoEnteros(a,b,ax,tabla,duración=2):
            self.play([fila.animate.shift(i*a*RIGHT) for i,fila in enumerate(tabla)], run_time=duración/2)
            self.play([fila.animate.shift(i*DOWN) for i,fila in enumerate(tabla)], run_time=duración/2)
        
        def producto(a,b,ax,tabla,duración=3):
            self.play([fila.animate.shift(i*a*RIGHT) for i,fila in enumerate(tabla)], run_time=duración/3)
            self.play([fila.animate.shift(i*DOWN) for i,fila in enumerate(tabla)], run_time=duración/3)
            self.play([fila.animate.shift(i*UP) for i,fila in enumerate(tabla)], run_time=duración/3)

        def multiplicación(a, b: int, ax: Axes, tabla: VGroup, xtext='', ytext='', duración_de_las_rectas=1):
            h_line =ax.get_horizontal_line(ax.c2p(a*b,b), color=YELLOW)
            v_line =ax.get_vertical_line(ax.c2p(a*b,b), color=YELLOW)
            xlabel = Tex(xtext, font_size=32, color=YELLOW)
            pos_x  = DOWN if a*b >0 else UP
            xlabel.next_to(ax.c2p(a,0), pos_x, buff=0.5)
            ylabel = Tex(ytext, font_size=32, color=YELLOW)
            pos_y  = LEFT if a*b >0 else RIGHT
            ylabel.next_to(ax.c2p(0,b), pos_y, buff=0.5)
            prod_label = Tex(f"{b}"+xtext, font_size=32, color=YELLOW) if xtext else Tex('')
            prod_label.next_to(ax.c2p(a*b,0), DOWN, buff=0.5)
            self.add(xlabel)
            self.add(ylabel)
            self.add(prod_label)            
            self.play(Indicate(xlabel,
                               run_time=1),
                      Indicate(tabla[0],
                               run_time=1))
            
            self.play(Indicate(h_line, scale_factor=2),
                      run_time=1)
            self.play(Indicate(v_line, scale_factor=2),
                      run_time=2)
            self.wait(duración_de_las_rectas)
            self.play(FadeOut(v_line),
                      FadeOut(h_line))
            

        self.creditos(1)
        
        ax = Axes(
            x_length=12,
            y_length=6,
            x_range=[0, 12, 1],
            y_range=[0, 6, 1],
            tips=False,
            axis_config={"include_numbers": True}
        )        
        

        resumen1 = Tex(_(r"""Para interpretar geométricamente el producto por escalares en \R[2],"""),
                       tex_template = myTemplate).scale_to_fit_width(config.frame_width*.9)
        
        resumen2 = Tex(_(r"""antes interpretaremos geométricamente el producto de dos números."""),
                       tex_template = myTemplate).next_to(resumen1, DOWN).scale_to_fit_width(config.frame_width*.9)
        
        with self.voiceover(text=_("""Antes de ver la interpretación
        geométrica del reescalado de vectores en R2,""")) as tracker:
            
            self.add(cabecera)            
            self.play(Write(resumen1), run_time=tracker.duration+0.2)
            
        with self.voiceover(text=_("""debemos dar una interpretación
        geométrica al producto entre números reales.""")) as tracker:
            
            self.play(Write(resumen2), run_time=tracker.duration)
            self.play(FadeOut(resumen1),
                      FadeOut(resumen2))
            
            
        with self.voiceover(text=_("""Cuando los números son naturales
        es habitual asociar sus magnitudes con longitudes, y los
        productos con superficies""")) as tracker:

            self.play(FadeIn(ax),
                      FadeTransform(cabecera, cabecera2),
                      run_time=tracker.duration/3)

        with self.voiceover(text=_("""Así, el producto de uno por uno
        se asocia con un cuadrado de lado 1""")) as tracker:
            
            a=1
            b=1
            tabla = retículaProducto(a,b,ax)
            self.pausa(tracker.duration/6)
            xlabel,ylabel=coordenadas_xy(a,b,ax)
            self.play(Indicate(xlabel,scale_factor=2.5))
            self.play(Indicate(ylabel,scale_factor=2.5))
            self.remove(xlabel,
                        ylabel)
            [self.play(FadeIn(base), run_time=.5) for base in tabla]
            self.play(Indicate(tabla), run_time=tracker.duration/3)

        with self.voiceover(text=_("""Evidentemente el área del
        cuadrado coincide con la longitud de la base.""")) as tracker:            
            self.pausa(tracker.duration/2)
            self.play(tabla.animate.fade(0.8), run_time=tracker.duration/2)

            
        with self.voiceover(text=_("""Podemos asociar el producto tres
        por uno con un rectángulo de base tres y altura uno.""")) as tracker:
            
            a=3.
            b=1
            tabla2 = retículaProducto(a,b,ax)
            xlabel,ylabel=coordenadas_xy(a,b,ax)
            self.play(Indicate(xlabel,scale_factor=2.5))
            self.play(Indicate(ylabel,scale_factor=2.5))
            self.remove(xlabel,
                        ylabel)
            [self.play(FadeIn(base), run_time=.5) for base in tabla2]
            self.play(Indicate(tabla2), run_time=tracker.duration/3)
            self.pausa(tracker.duration/4)

        with self.voiceover(text=_("""Y de nuevo el área coincide con
        la longitud de la base, pues la altura es uno.""")) as tracker:
            self.play(FadeOut(tabla), run_time=tracker.duration/2)
            self.play(tabla2.animate.set_opacity(0.15), run_time=tracker.duration/2)
            
        with self.voiceover(text=_("""Multiplicar uno por tres
        corresponde a apilar tres cuadrados de base uno. Si los
        alineamos en una fila de altura uno, podemos comprobar que el
        área total (así como la longitud) es igual a la del rectángulo
        tres por uno.""")) as tracker:
            
            a=1
            b=3
            tabla = retículaProducto(a,b,ax)
            xlabel,ylabel=coordenadas_xy(a,b,ax)
            self.play(Indicate(xlabel,scale_factor=2.5))
            self.play(Indicate(ylabel,scale_factor=2.5))
            self.remove(xlabel,
                        ylabel)
            self.play([FadeIn(base) for base in tabla],
                      run_time=tracker.duration/3)
            productoEnteros(a,b,ax,tabla)
            self.pausa(tracker.duration/3)
            self.play(FadeOut(tabla),
                      FadeOut(tabla2))
                                        
        with self.voiceover(text=_("""Para multiplicar tres por cuatro
        apilamos cuatro rectángulos de base tres y altura uno. De
        nuevo, si los alineamos en una fila de altura 1, su longitud
        total es el valor del producto.""")) as tracker:
            
            a=3.
            b=4
            tabla = retículaProducto(a,b,ax)
            xlabel,ylabel=coordenadas_xy(a,b,ax)
            self.play(Indicate(xlabel,scale_factor=2.5))
            self.play(Indicate(ylabel,scale_factor=2.5))
            self.remove(xlabel,
                        ylabel)
            self.play([FadeIn(base) for base in tabla], run_time=tracker.duration/3)
            productoEnteros(a,b,ax,tabla,duración=tracker.duration/2)
            self.pausa(tracker.duration/6)
            self.play(FadeOut(tabla))

        with self.voiceover(text=_("""Esta forma de multiplicar, donde
        apilamos cierta cantidad de rectángulos con altura uno y base
        un número natural, para luego disponerlos horizontalmente y
        medir la longitud total, se puede generalizar a rectángulos
        cuya base es un número real, pero solo si lo hacemos con
        rectángulos de altura uno.""")) as tracker:
            
            a=2.
            b=3
            tabla = retículaProducto(a,b,ax)
            xlabel,ylabel=coordenadas_xy(a,b,ax)
            self.play(Indicate(xlabel,scale_factor=2.5))
            self.play(Indicate(ylabel,scale_factor=2.5))
            self.remove(xlabel,
                        ylabel)
            self.play([FadeIn(base) for base in tabla], run_time=tracker.duration/3)
            productoEnteros(a,b,ax,tabla,duración=tracker.duration/4)
            self.play(FadeOut(tabla),
                      run_time=tracker.duration*4/12)
            
        with self.voiceover(text=_("""Por ejemplo, podemos multiplicar
        raíz de dos por cinco.""")) as tracker:
            a=np.sqrt(2)
            a_label=r"$\sqrt{2}$"
            b=5
            tabla = retículaProducto(a,b,ax)
            self.pausa(tracker.duration/3)           
            xlabel,ylabel=coordenadas_xy(a, b, ax, labelx=a_label)
            self.play(Indicate(xlabel,scale_factor=2.5))
            self.play(Indicate(ylabel,scale_factor=2.5))
            self.remove(ylabel)
            self.play([FadeIn(base) for base in tabla], run_time=tracker.duration/3)
            productoEnteros(a,b,ax,tabla)
            
        with self.voiceover(text=_("""El resultado es algo mayor que
        siete.""")) as tracker:
            
            self.pausa(tracker.duration)           

        with self.voiceover(text=_("""Pero ¿cómo podemos multiplicar
        dos numeros reales?""")) as tracker:
            
            self.pausa(tracker.duration)           
            
        with self.voiceover(text=_("""Para hacerlo debemos dar una
        nueva interpretación del producto. Fijémonos en lo que pasa si
        nos quedamos a mitad de camino entre la pila inicial y la fila
        final.""")) as tracker:
            
            self.pausa(tracker.duration/3)
            self.play([fila.animate.shift(i*UP) for i,fila in enumerate(tabla)],
                      run_time=tracker.duration/3)

        with self.voiceover(text=_("""En esta posición los rectángulos
        también están alineados.""")) as tracker:
            
            recta =  Line(start = tabla.get_corner(DL),
                          end   = tabla.get_corner(UR),
                          color = RED_B)
            self.play(FadeIn(recta))
            self.pausa(tracker.duration)           
            self.play(FadeOut(tabla,
                              recta,
                              xlabel)) 
            
        with self.voiceover(text=_("""Usaremos este hecho para dar una
        nueva interpretación geométrica del producto entre números.""")) as tracker:
            self.pausa(tracker.duration)
            
        with self.voiceover(text=_("""Para verlo, volvamos primero a
        un ejemplo con números enteros.""")) as tracker:

            a=3.
            b=4
            tabla = retículaProducto(a,b,ax)
            xlabel,ylabel=coordenadas_xy(a, b, ax, labelx=a_label)
            self.play(Indicate(xlabel,scale_factor=2.5))
            self.play(Indicate(ylabel,scale_factor=2.5))
            self.remove(xlabel,
                        ylabel)
            self.add(tabla)
            producto(a,b,ax,tabla,duración=tracker.duration)
            
            recta =  Line(start = tabla.get_corner(DL),
                          end   = tabla.get_corner(UR),
                          color = RED_B)
            
            self.play(FadeIn(recta)) 
            self.play(FadeOut(tabla[1:]))
           
        with self.voiceover(text=_("""tres por cuatro es doce, y se puede
        calcular directamente en la recta roja, pues la recta a la
        altura 4 está sobre 12.""")) as tracker:
            
            multiplicación(a, b, ax, tabla, duración_de_las_rectas=4)
            
        with self.voiceover(text=_("""Pero también se puede ver que
        tres por dos es seis""")) as tracker:
            
            a=3.
            b=2
            multiplicación(a, b, ax, tabla)

        with self.voiceover(text=_("""O que tres por cuatro tercios es
        cuatro""")) as tracker:           
            a=3.
            b=4/3            
            b_label=r"$\frac{4}{3}$"
            xlabel,ylabel=coordenadas_xy(a, b, ax, labely=b_label)
            self.add(ylabel)
            multiplicación(a, b, ax, tabla, duración_de_las_rectas=0.4)
            self.play(FadeOut(tabla[0],
                              recta,
                              ylabel))
            
        with self.voiceover(text=_("""De este modo podemos multiplicar
        dos numeros reales cualesquiera. Por ejemplo, dos veces raíz
        de dos por raíz de diez.""")) as tracker:
            
            a=2*np.sqrt(2)
            a_label=r"$2\sqrt{2}$"
            b=1
            tabla = retículaProducto(a,b,ax)
            c=np.sqrt(10)
            c_label=r"$\sqrt{10}$"
            xlabel,ylabel=coordenadas_xy(a, c, ax, labelx=a_label, labely=c_label)
            self.pausa(tracker.duration/2)
            self.play(Indicate(xlabel,scale_factor=2.5))
            self.play(Indicate(ylabel,scale_factor=2.5))
            self.add(tabla)

        with self.voiceover(text=_("""El resultado es algo menor que
        9.""")) as tracker:
     
            recta =  Line(start = tabla.get_corner(DL),
                          end   = ax.c2p(12,12/a),
                          color = RED_B)
            self.play(FadeIn(recta))
            multiplicación(a, c, ax, tabla, duración_de_las_rectas=1)
            self.play(FadeOut(tabla,
                              recta,
                              xlabel,
                              ylabel,
                              ax,
                              cabecera2))
            
        ax = Axes(
            x_length=12,
            y_length=6,
            x_range=[-6, 6, 1],
            y_range=[-3, 3, 1],
            tips=False,
            axis_config={"include_numbers": True}
        )        
        self.add(ax)
            
        a=-2.5
        a_label=r"$\alpha$"
        b=1
        tabla = retículaProducto(a,b,ax)
        c=-1.5
        c_label=r"$\beta$"
        xlabel,ylabel=coordenadas_xy(a, c, ax, labelx=a_label, labely=c_label)
        xlabel.scale(1.5)
        ylabel.scale(1.5)
        
        with self.voiceover(text=_("""Por tanto, para multiplicar
        gráficamente un número alfa;""")) as tracker:
            
            self.pausa(tracker.duration*2/3)
            self.play(Indicate(xlabel,scale_factor=1.5))
            
        with self.voiceover(text=_("""por un número beta:""")) as tracker:
            self.play(Indicate(ylabel,scale_factor=1.5))
            
        with self.voiceover(text=_("""Pintamos un rectángulo cuya base
        va desde cero hasta alfa, y con altura uno.""")) as tracker:
            
            self.play(Indicate(tabla))

            
        with self.voiceover(text=_("""Extendemos la diagonal que pasa
        por el origen para obtener una recta infinita.""")) as tracker:
            
            recta =  Line(start = ax.c2p(-6,-6/a),
                          end   = ax.c2p( 6, 6/a),
                          color = RED_B)
            self.play(FadeIn(recta),
                      run_time=tracker.duration/3)

        with self.voiceover(text=_("""El punto de la recta cuya
        coordenada vertical es beta""")) as tracker:
            
            prod_label = Tex(r"$\alpha\beta$", font_size=30).scale(1.5)
            prod_label.next_to(ax.c2p(a*c,0), UP, buff=0.3)

            h_line =ax.get_horizontal_line(ax.c2p(a*c,c), color=BLUE)
            v_line =ax.get_vertical_line(ax.c2p(a*c,c), color=BLUE)
            self.play(FadeIn(h_line),
                      Indicate(ylabel))
                      
        with self.voiceover(text=_("""tiene como coordenada horizontal
        el valor alfa por beta""")) as tracker:
            
            self.play(FadeIn(v_line),
                      Indicate(prod_label,
                               scale_factor=1.5))
            self.pausa_larga()

        with self.voiceover(text=_("""Esta nueva interpretación de
        producto implica que, los puntos de una recta que pasa por el
        origen son aquellos que mantienen una proporción constante
        entre sus cordenadas vertical y horizontal.""")) as tracker:
            
            c=2.2
            c_label=r"$y$"
            xlabel2,ylabel2=coordenadas_xy(a, c, ax, labelx=a_label, labely=c_label,posy=1)
            xlabel2.scale(1.5)
            ylabel2.scale(1.5)
            prod_label2 = Tex(r"$x=\alpha y$", font_size=30).scale(1.5)
            prod_label2.next_to(ax.c2p(a*c,0), DOWN, buff=0.6)
            h_line2 =ax.get_horizontal_line(ax.c2p(a*c,c), color=GREEN)
            v_line2 =ax.get_vertical_line(ax.c2p(a*c,c), color=GREEN)

            eq_recta = Tex(r"$\frac{\beta}{\alpha\beta}\;=\;\frac{1}{\alpha}$",
                       tex_template = myTemplate,
                       font_size=30).scale(2.5).set_color(BLUE_A).to_corner(UR)

            self.play(FadeIn(eq_recta))
            self.pausa(tracker.duration/3)
            self.play(Circumscribe(eq_recta[0][-3:]),
                      Circumscribe(eq_recta[0][:3]),
                      run_time=tracker.duration/2)

        with self.voiceover(text=_("""Fíjese que esta representación
        respeta los signos del producto:""")) as tracker:            
            self.pausa(tracker.duration)
            
        with self.voiceover(text=_("""menos por más es menos.""")) as tracker:
            self.pausa(tracker.duration)
            
        with self.voiceover(text=_("""Y menos por menos es más. Por
        eso alpha por beta es positivo en la figura.""")) as tracker:
            self.play(Indicate(xlabel,scale_factor=2),
                      Indicate(ylabel,scale_factor=2),
                      Indicate(prod_label,scale_factor=2),
                      run_time=tracker.duration*2/3)
            self.play(FadeOut(tabla,
                              recta,
                              h_line,
                              v_line,
                              xlabel,
                              ylabel,
                              prod_label,
                              eq_recta),
                      run_time=tracker.duration/2)
                
        eje_y =  Line(start = ax.c2p(0,3),
                      end   = ax.c2p(0,-3),
                      color = RED_B)
        cerolabel = Tex('$0$', font_size=32, color=YELLOW).scale(1.3)
        cerolabel.next_to(ax.c2p(0,0), DOWN)
        
        with self.voiceover(text=_("""Nótese que en el caso en que
        alfa es cero, empleamos como recta el eje vertical.""")) as tracker:
            
            self.play(FadeIn(eje_y),
                      Indicate(cerolabel),
                      run_time=tracker.duration/2)
            self.play(Indicate(eje_y),
                      run_time=tracker.duration/2)
            self.play(FadeOut(eje_y),
                      FadeOut(cerolabel))
            
        with self.voiceover(text=_("""Esta interpretación del producto
        entre números reales, que caracteriza las rectas en función de
        la proporción entre las coordenadas de sus puntos, nos va a
        permitir interpretar el producto de un vector por un
        escalar. Veámoslo""")) as tracker:
            
            self.play(FadeIn(recta,
                             h_line,
                             v_line,
                             xlabel,
                             ylabel,
                             prod_label,
                             eq_recta))

class L01_V04_E03_InterpretacionGeometricaDelProductoPorEscalaresR2(MiEscenaConVoz):    
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))        
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)

        self.creditos(7)
        	
        cabecera = Tex(_("Interpretación geométrica del producto de vectores en $\R[2]$"),
                            tex_template = myTemplate,
                            font_size=60).scale_to_fit_width(config.frame_width*.9).to_edge(UP).set_color(BLUE)        
        self.add(cabecera)
        self.pausa_corta()

        axes = NumberPlane(x_range=(-8, 8, 1),
                           y_range=(-7, 7, 1),
                           background_line_style={
                               "stroke_width":  3,
                               "stroke_opacity": 0.4 }
                           ).add_coordinates()

        with self.voiceover(text=_("""Ahora ya podemos dar una
        sencilla interpretación geométrica del reescalado de
        vectores""")) as tracker: self.pausa(tracker.duration)

        with self.voiceover(text=_("""Comencemos por el producto de un vector no nulo de
        R 2. Consideremos dos casos.""")) as tracker:
            self.play(FadeIn(axes),
                      FadeOut(cabecera),
                      run_time=tracker.duration)

        eje_y =  Line(start = [0, -5, 0.],
                      end   = [0,  5, 0.],
                      color = RED_B)
        
        b  = nc.Vector([0,sp.symbols('a_2')])
        escalar = sp.symbols('\lambda')
        w  = b*escalar
        lv = MathTex(r"\lambda\,\Vect{a} = ",  tex_template = myTemplate)
        s4 = MathTex(w.latex(),  tex_template = myTemplate)
        s5 = MathTex(r";\qquad a_2\ne0",  tex_template = myTemplate)
        grp2 = VGroup(lv, s4, s5).arrange(RIGHT).to_corner(UL)
        
        c       = VectorR2([0,2.5], color=RED_A)
        dotc = c.dot(axes)
        dotc2 = dotc.copy()
        flechac = c.arrow(axes)
        flechac2 = flechac.copy()
        d       = VectorR2([0,4.5], color=RED_A)
        dotd = d.dot(axes)
        flechad = d.arrow(axes)
        e       = VectorR2([0,-4.5], color=RED_A)
        dote = e.dot(axes)
        flechae = e.arrow(axes)

        with self.voiceover(text=_("""Por una parte, si la primera componente de un vector no nulo es
        cero,  el conjunto de sus múltiplos constituye el eje vertical.""")) as tracker:
            self.play(FadeIn(grp2),
                      FadeIn(dotc),
                      run_time=tracker.duration/2)
            self.play(Transform(dotc,
                                dotd),
                      run_time=tracker.duration/7)
            self.play(Transform(dotc,
                                dote),
                      run_time=tracker.duration/7)
            self.play(Transform(dotc,
                                dotc2),
                      run_time=tracker.duration/7)
            self.remove(dotc),
            self.play(Wiggle(eje_y),
                      run_time=1.5)
            self.pausa()
            self.play(FadeOut(grp2,eje_y))

        Vect1 = nc.Vector([4,2])
        vect1 = VectorR2(Vect1.lista, rpr='colum', color=BLUE_B)
        vect1_dot = vect1.dot(axes, radio=0.05)
        vect1_tex = vect1.tex
        vgr_vect1 = VGroup(vect1.tex).next_to(vect1_dot, RIGHT, buff=0.25)
        vect1_v_line = vect1.v_line(axes)
        vect1_h_line = vect1.h_line(axes)
        vect1_flecha = vect1.arrow(axes)

        a = nc.Vector(sp.symbols('a:3')[1:])
        escalar = sp.symbols('\lambda')
        v  = a*escalar
        lv = MathTex(r"\lambda\,\Vect{a} = ",  tex_template = myTemplate)
        s1 = MathTex(v.latex(),  tex_template = myTemplate)
        s2 = MathTex(r";\qquad",  tex_template = myTemplate)
        s3 = MathTex(r"a_1\ne0",  tex_template = myTemplate)
        grp1 = VGroup(lv, s1, s2, s3).arrange(RIGHT).to_corner(UL)
        
        with self.voiceover(text=_("""Y ahora consideremos cualquier otro vector no nulo de
        R 2.""")) as tracker:
            self.play(FadeIn(grp1))
            self.pausa()

        with self.voiceover(text=_("""Por ejemplo el 4 2""")) as tracker:
            self.play(FadeIn(vect1_dot, vect1_tex, vect1_v_line, vect1_h_line))
            self.pausa()
    
        with self.voiceover(text=_("""Al reescalarlo, aplicamos el mismo factor a todas sus
        componentes""")) as tracker:
            self.play(Indicate(grp1[1][0][1]),
                      Indicate(grp1[1][0][4]),
                      run_time=tracker.duration)
            self.pausa()

        Vect2 = Vect1*(nc.fracc(1,2))
        vect2 = VectorR2(Vect2.lista, rpr='colum', color=BLUE_B)
        vect2_dot = vect2.dot(axes, radio=0.05)
        vect2_tex = vect2.tex
        vgr_vect2 = VGroup(vect2.tex).next_to(vect2_dot, RIGHT, buff=0.25)
        vect2_v_line = vect2.v_line(axes)
        vect2_h_line = vect2.h_line(axes)
        vect2_flecha = vect2.arrow(axes)

        with self.voiceover(text=_("""Así, si multiplicamos el vector por un medio, reducimos sus
        componentes a la mitad.""")) as tracker:
            self.play(TransformFromCopy(vect1_dot,
                                        vect2_dot),
                      TransformFromCopy(vect1_tex,
                                        vect2_tex),
                      TransformFromCopy(vect1_v_line,
                                        vect2_v_line),
                      TransformFromCopy(vect1_h_line,
                                        vect2_h_line),
                      run_time=tracker.duration/2)            

        Vect3 = Vect2*3
        vect3 = VectorR2(Vect3.lista, rpr='colum', color=BLUE_B)
        vect3_dot = vect3.dot(axes, radio=0.05)
        vect3_tex = vect3.tex
        vgr_vect3 = VGroup(vect3.tex).next_to(vect3_dot, RIGHT, buff=0.25)
        vect3_v_line = vect3.v_line(axes)
        vect3_h_line = vect3.h_line(axes)
        vect3_flecha = vect3.arrow(axes)

        with self.voiceover(text=_("""Si ahora lo multiplicamos por tres, triplicamos sus
        componentes.""")) as tracker:
            self.play(TransformFromCopy(vect2_dot,
                                        vect3_dot),
                      TransformFromCopy(vect2_tex,
                                        vect3_tex),
                      TransformFromCopy(vect2_v_line,
                                        vect3_v_line),
                      TransformFromCopy(vect2_h_line,
                                        vect3_h_line),
                      run_time=tracker.duration/2)

        Vect4 = Vect3*nc.fracc(-2,3)
        vect4 = VectorR2(Vect4.lista, rpr='colum', color=BLUE_B)
        vect4_dot = vect4.dot(axes, radio=0.05)
        vect4_tex = vect4.tex
        vgr_vect4 = VGroup(vect4.tex).next_to(vect4_dot, LEFT, buff=0.25)
        vect4_v_line = vect4.v_line(axes)
        vect4_h_line = vect4.h_line(axes)
        vect4_flecha = vect4.arrow(axes)

        Vect5 = Vect3*nc.fracc(-1,3)
        vect5 = VectorR2(Vect5.lista, rpr='colum', color=BLUE_B)
        vect5_dot = vect5.dot(axes, radio=0.05)
        vect5_tex = vect5.tex
        vgr_vect5 = VGroup(vect5.tex).next_to(vect5_dot, LEFT, buff=0.25)
        vect5_v_line = vect5.v_line(axes)
        vect5_h_line = vect5.h_line(axes)
        vect5_flecha = vect5.arrow(axes)

        Vect6 = Vect3*(-1)
        vect6 = VectorR2(Vect6.lista, rpr='colum', color=BLUE_B)
        vect6_dot = vect6.dot(axes, radio=0.06)
        vect6_tex = vect6.tex
        vgr_vect6 = VGroup(vect6.tex).next_to(vect6_dot, LEFT, buff=0.26)
        vect6_v_line = vect6.v_line(axes)
        vect6_h_line = vect6.h_line(axes)
        vect6_flecha = vect6.arrow(axes)

        with self.voiceover(text=_("""Y si lo multiplicamos por algún número negativo, cambiamos el
        signo de sus componentes.""")) as tracker:
            self.play(TransformFromCopy(vect3_dot,
                                        vect4_dot),
                      TransformFromCopy(vect3_tex,
                                        vect4_tex),
                      TransformFromCopy(vect3_v_line,
                                        vect4_v_line),
                      TransformFromCopy(vect3_h_line,
                                        vect4_h_line),
                      TransformFromCopy(vect3_dot,
                                        vect5_dot),
                      TransformFromCopy(vect3_tex,
                                        vect5_tex),
                      TransformFromCopy(vect3_v_line,
                                        vect5_v_line),
                      TransformFromCopy(vect3_h_line,
                                        vect5_h_line),
                      TransformFromCopy(vect3_dot,
                                        vect6_dot),
                      TransformFromCopy(vect3_tex,
                                        vect6_tex),
                      TransformFromCopy(vect3_v_line,
                                        vect6_v_line),
                      TransformFromCopy(vect3_h_line,
                                        vect6_h_line),
                      run_time=tracker.duration/2)
            
        Vect0 = Vect3*0
        vect0 = VectorR2(Vect0.lista, rpr='colum', color=BLUE_B)
        vect0_dot = vect0.dot(axes, radio=0.05)
        vect0_tex = vect0.tex
        vgr_vect0 = VGroup(vect0.tex).next_to(vect0_dot, RIGHT, buff=0.25)
        
        with self.voiceover(text=_("""Además, cualquier vector
        multiplicado por cero es un vector nulo.""")) as tracker:            
            self.play(TransformFromCopy(vect1_dot,
                                vect0_dot),
                      TransformFromCopy(vect1_tex,
                                vect0_tex),
                      run_time=tracker.duration/2)
            
        p1 = MathTex(r"\frac{\lambda a_2}{\lambda a_1}=",
                     tex_template = myTemplate)
        p2 = MathTex(r"\frac{a_2}{a_1};\qquad ",
                     tex_template = myTemplate)
        p3 = MathTex(r"\lambda\ne0",
                     tex_template = myTemplate)
        pendiente = VGroup(p1,
                           p2,
                           p3).arrange(RIGHT).next_to(grp1,
                                                      DOWN,
                                                      buff=0.7).scale(.9)
        
        with self.voiceover(text=_("""Nótese que si el escalar es distinto de cero, la
        proporcionalidad entre ambas componentes se mantiene, pues ambas componentes se
        multiplican por el mismo número.""")) as tracker:
            self.add(pendiente[-1])
            self.wait(tracker.duration/2)
            self.pausa(tracker.duration/6)
            self.play(Flash(grp1[1][0][1]),
                      Flash(grp1[1][0][4]),
                      run_time=tracker.duration/3)
                    
        with self.voiceover(text=_("""En el ejemplo, las primeras componentes son el doble de las
        segundas.""")) as tracker:
            self.wait(tracker.duration/2)
            
        with self.voiceover(text=_("""Atendiendo a la interpretación
        geométrica del producto entre números reales que vimos
        anteriormente,""")) as tracker:
            
            self.wait(tracker.duration)
            
        with self.voiceover(text=_("""sabemos que, los puntos que comparten
        idéntica proporción entre sus coordenadas vertical y
        horizontal, constituyen una recta que pasa por el origen.""")) as tracker:
            
            self.play(FadeIn(pendiente[0:-1]),
                      run_time=tracker.duration/6)
            self.wait(tracker.duration/6)
            self.play(Indicate(vect1_h_line),
                      Indicate(vect2_h_line),
                      Indicate(vect3_h_line),
                      Indicate(vect4_h_line),
                      Indicate(vect5_h_line),
                      Indicate(vect6_h_line),
                      Circumscribe(pendiente[0][0][:3]),
                      run_time=tracker.duration/6)
            self.play(Indicate(vect1_v_line),
                      Indicate(vect2_v_line),
                      Indicate(vect3_v_line),
                      Indicate(vect4_v_line),
                      Indicate(vect5_v_line),
                      Indicate(vect6_v_line),
                      Circumscribe(pendiente[0][0][4:-1]),
                      run_time=tracker.duration/6)
            self.play(FadeOut(vect1_v_line,
                              vect2_v_line,
                              vect3_v_line,
                              vect4_v_line,
                              vect5_v_line,
                              vect6_v_line,
                              vect1_h_line,
                              vect2_h_line,
                              vect3_h_line,
                              vect4_h_line,
                              vect5_h_line,
                              vect6_h_line,
                              vect0_tex,
                              vect1_tex,
                              vect2_tex,
                              vect3_tex,
                              vect4_tex,
                              vect5_tex,
                              vect6_tex),
                      run_time=tracker.duration*1/6)
                

            a = nc.Vector(sp.symbols('a:3')[1:])
            escalar = sp.symbols('\lambda')
            v  = a*escalar
            lv = MathTex(r"\lambda\,\Vect{a} = ",  tex_template = myTemplate)
            s1 = MathTex(v.latex(),  tex_template = myTemplate)
            s2 = MathTex(r";\qquad",  tex_template = myTemplate)
            s3 = MathTex(r"a_1\ne0",  tex_template = myTemplate)
            grp1 = VGroup(lv, s1, s2, s3).arrange(RIGHT).to_corner(UL).scale(.9)
            
            b  = nc.Vector([0,sp.symbols('a_2')])
            w  = b*escalar
            s4 = MathTex(w.latex(),  tex_template = myTemplate)
            s5 = MathTex(r"a_1=0",  tex_template = myTemplate)
            grp2 = VGroup(lv, s4).arrange(RIGHT).to_corner(UL).scale(.9)
            
            recta =  Line(start = [-8, -4, 0.],
                          end   = [8, 4, 0.],
                          color = BLUE_B)
        
            self.play(FadeOut(vect1_dot,
                              vect2_dot,
                              vect3_dot,
                              vect4_dot,
                              vect5_dot,
                              vect6_dot),
                      Indicate(recta, scale_factor=5))

        self.pausa()

        resumen1 = Tex(_(r"""El conjunto de múltiplos de un vector no nulo de \R[2]"""),
                       tex_template = myTemplate)
        resumen2 = Tex(_(r"""se corresponde con una recta que pasa por el origen."""),
                       tex_template = myTemplate).next_to(resumen1, DOWN)
            
        with self.voiceover(text=_("""Por tanto, el conjunto de
        múltiplos de cualquier vector no nulo de R 2 corresponde a
        una recta que pasa por el origen.""")) as tracker:
            
            self.play(*[FadeOut(mob)for mob in self.mobjects] )            
            self.play(Write(resumen1))
            self.play(Write(resumen2))
            
        self.pausa(3)

class L01_V04_E04_3D_InterpretacionGeometricaDelProductoDeTresNumeros(ThreeDScene):
    
    def creditos(self, variante=1):
        def analisis_opcion_elegida(tipo):
            'Análisis de las opciones de eliminación elegidas'
            lista = [100,20,10,4,2,1]
            opcion = set()
            for t in lista:
                if (tipo - (tipo % t)) in lista:
                    opcion.add(tipo - (tipo % t))
                    tipo = tipo % t
            return opcion    
        copyright = Tex(r"\textcopyright{\;} 2025\; Marcos Bujosa  ")
        if 1 in analisis_opcion_elegida(variante):
            stampDcha  = VGroup(copyright.copy()).rotate( PI/2).scale(0.5).to_edge(RIGHT, buff=0.1).set_color(GRAY_D)
            self.add(stampDcha)
        if 2 in analisis_opcion_elegida(variante):
            stampIzda  = VGroup(copyright.copy()).rotate(-PI/2).scale(0.5).to_edge(LEFT, buff=0.1).set_color(GRAY_D)
            self.add(stampIzda)
        if 4 in analisis_opcion_elegida(variante):
            stampBottom= VGroup(copyright.copy()).rotate(    0).scale(0.5).to_edge(DOWN, buff=0.1).set_color(GRAY_D)
            self.add(stampBottom)
        if 10 in analisis_opcion_elegida(variante):
            stampTop   = VGroup(copyright.copy()).rotate(    0).scale(0.5).to_edge(  UP, buff=0.1).set_color(GRAY_D)
            self.add(stampTop)
            
    
    def construct(self):
        lado = 0.25
        ejes = ThreeDAxes(
            x_range=(-28, 28, 1),
            y_range=(-15, 15, 1),
            z_range=(-10, 10, 1),
            z_length=5,
            x_length=lado*28*2,
            y_length=lado*15*2,
            tips=False,
            axis_config={"include_numbers": True,
                         "font_size": 12},
        )

        def coordenada_x(x, ax, label='', pos=0):
            label = label if label else f"{x}"
            xlabel = Tex(label, font_size=30)
            pos_label = UP if pos else DOWN
            xlabel.next_to(ax.c2p(x,0,0), pos_label, buff=0.35)
            return xlabel

        def coordenada_y(y, ax, label='', pos=0):
            label = label if label else f"{y}"
            ylabel = Tex(label, font_size=30)
            pos_label = RIGHT if pos else LEFT
            ylabel.next_to(ax.c2p(0,y,0), pos_label, buff=0.35)
            return ylabel

        def coordenada_z(z, ax, label='', pos=0):
            label = label if label else f"{z}"
            zlabel = Tex(label, font_size=30)
            pos_label = RIGHT if pos else LEFT
            zlabel.rotate(PI/2, axis=RIGHT).next_to(ax.c2p(0,0,z), pos_label, buff=0.35)
            return zlabel
        
        coordenadas_xy = lambda x,y,ax,labelx='',labely='',posx=0,posy=0: (coordenada_x(x,ax,labelx,posx),
                                                                           coordenada_y(y,ax,labely,posy))

        def ladrillo(a, b, ax: Axes) -> VGroup:
            prisma = Prism(dimensions=[float(a*b*lado), float(b*lado), float(1*lado)],
                         fill_opacity=0.6,
                         stroke_width=1).next_to(ax.coords_to_point(0, 0),
                                                 UR,
                                                 buff=0)
            return Group(*[prisma.copy()])
        
        def pila(a, b, c: int, ax: Axes) -> VGroup:
            columna = Group(*[ladrillo(a, b, ax).shift(s*lado*OUT) for s in range(0,c)]).shift([0, 0, lado/2])
            columna.a = a
            columna.b = b
            columna.c = c
            return columna 
                
        def producto(pila,ritmo=0.6, pausa=8):
            a = float(pila.a)
            b = float(pila.b)
            c = pila.c
            [self.play(piso.animate.shift([0, p*b*lado, 0]), run_time=ritmo) for p,piso in enumerate(pila)]
            for p,piso in enumerate(pila):
                self.play([fila.animate.shift([f*a*lado+p*a*b*lado, 0, 0]) for f,fila in enumerate(piso)], run_time=ritmo) # alineados
            for p,piso in enumerate(pila):
                self.play(piso.animate.shift([0, 0, -p*lado]), run_time=ritmo)
            for p,piso in enumerate(pila):
                self.play([fila.animate.shift([0, -(p*b+f)*lado, 0]) for f,fila in enumerate(piso)], run_time=ritmo)
            self.wait(pausa)
            for p,piso in enumerate(pila):
                self.play(piso.animate.shift([0, 0, p*lado]), run_time=ritmo)
            for p,piso in enumerate(pila):
                self.play([fila.animate.shift([0, (p*b+f)*lado, 0]) for f,fila in enumerate(piso)], run_time=ritmo)
                
        def multiplicación(a, b, c, ax: Axes, pila: VGroup):
            v_line =ax.get_vertical_line(ax.c2p(float(a*b*c),float(b*c),float(c)), color=YELLOW)
            recta =  Line(start = ax.c2p(0,0,float(c)),
                          end   = ax.c2p(float(a*b*c),float(b*c),float(c)))

            self.play(Indicate(recta, scale_factor=2),
                      run_time=2)
            self.play(Indicate(v_line, scale_factor=2),
                      run_time=2)
            self.wait()
            self.play(FadeOut(v_line))

        def multiplicacion3Num(a, b, c, ax: Axes, pila: VGroup):
                Vect = nc.Vector([a*b*c,b*c,c])
                v = VectorR3(Vect.lista, rpr='colum', color=TEAL_A)
                line_x = v.x_line(ejes)
                line_y = v.y_line(ejes)
                line_z = v.z_line(ejes)
                line_xy = v.xy_line(ejes)
                line_v = v.v_line(ejes)
                return line_x,line_y,line_z,line_xy,line_v
        
        self.add(ejes)
        a=2
        b=3
        c=4
        columna = pila(a, b, c, ejes)

        # Set the camera orientation for a better view
        self.set_camera_orientation(theta=-90 * DEGREES,
                                    zoom=3)

        rectangulo = Rectangle(height=lado,
                               width=lado*a).next_to(ejes.coords_to_point(0, 0, 0),
                                                     UR,
                                                     buff=0)
        self.play(FadeIn(rectangulo))

        xlabel=coordenada_x(a, ejes, label=r"$\alpha$")        
        self.play(Indicate(xlabel,scale_factor=1.5),
                  run_time=.5)

        ylabel=coordenada_y(b, ejes, label=r"$\beta$")
        self.play(Indicate(ylabel,scale_factor=1.5),
                  run_time=.5)

        recta0 =  Line(start = ejes.c2p(-10,-5,0),
                      end   = ejes.c2p( 10, 5,0),
                      color = RED_B,).set_opacity(0.5)

        self.wait(2)
        self.play(Indicate(rectangulo),
                  run_time=2)
        
        self.wait(1)
        self.play(FadeIn(recta0))
        self.wait(6)

        pila = columna.copy()

        prodxylabel=coordenada_x(a*b, ejes, label=r"$\alpha\beta$")
        self.play(FadeIn(pila[0][0][0]))
        self.play(Indicate(ylabel,scale_factor=1.5),
                  run_time=1.5)
        self.play(Indicate(prodxylabel,scale_factor=1.5),
                  run_time=1.5)

        self.wait(5) 
        self.move_camera(phi=65 * DEGREES, theta=-65 * DEGREES, zoom=2.5, run_time=2)
        #self.set_camera_orientation(phi=65 * DEGREES, theta=-65 * DEGREES, zoom=2.5)
        
        self.play(Indicate(pila[0][0][0], run_time=1.8),
                  FadeOut(recta0),
                  FadeOut(xlabel),
                  FadeOut(rectangulo))

        self.wait(1)
        self.play(Indicate(prodxylabel,scale_factor=1.5),
                  run_time=1.5)
                
        self.wait(1.5)
        self.play(Indicate(ylabel,scale_factor=1.5),
                  run_time=1.5)
        
        self.wait(1.5)

        # mostramos el prisma
        self.play(FadeIn(pila[0][0][1:]),
                  run_time=1)                

        self.wait(2)
        self.move_camera(zoom=1, run_time=2)
        #self.set_camera_orientation(phi=65 * DEGREES, theta=-65 * DEGREES, zoom=1)
                        
        # mostramos una pila de prismas
        [self.play(FadeIn(piso)) for piso in columna[0:]]
        
        prodZlabel=coordenada_z(c, ejes, label=r"$\gamma$").set_color(YELLOW)
        prodXYZlabel=coordenada_x(a*b*c, ejes, label=r"$\alpha\beta\gamma$").set_color(YELLOW)
        prodYZlabel=coordenada_y(b*c, ejes, label=r"$\beta\gamma$").set_color(YELLOW)
        self.add(prodXYZlabel)
        
        producto(columna, pausa=7)
        self.wait(3)
        
        recta =  Line(start = [float(-a*b*c*lado),float(-b*c*lado),float(-c*lado)],
                      end   = [float(a*b*c*lado),float(b*c*lado),float(c*lado)],
                      color = RED_B)
        self.add(recta)
        
        self.wait(6)
        
        self.play(FadeOut(columna))

        self.wait(3)

        line_x,line_y,line_z,line_xy,line_v = multiplicacion3Num(a, b, c, ejes, columna)        
        self.add(line_x)
        self.add(line_z)
        self.add(line_v)
        self.add(prodZlabel)

        self.wait(3)
        self.play(Indicate(line_z,
                           scale_factor=1.5),
                  Indicate(prodZlabel,
                           scale_factor=2.5))
        self.wait(1.5)        
        self.play(Indicate(line_x,
                           scale_factor=1.5,
                           run_time=2),
                  Indicate(prodXYZlabel,
                           scale_factor=2.5,
                           run_time=2))
        self.wait(12.5)

        self.play(Indicate(line_x,scale_factor=2),
                  Indicate(line_v,scale_factor=2),
                  Indicate(prodXYZlabel,scale_factor=2.5),
                  Indicate(prodZlabel,scale_factor=3),
                  run_time=4)

        self.play(Indicate(line_y,scale_factor=2),
                  Indicate(prodYZlabel,scale_factor=3),
                  Indicate(prodZlabel,scale_factor=3),
                  Indicate(line_v,scale_factor=2),
                  run_time=3.5)
        
        rectaPlanoXY =  Line(start = ejes.c2p(     0,   0, 0),
                             end   = ejes.c2p( a*b*c, b*c, 0),
                             color = BLUE_B).set_opacity(0.5)
        self.add(rectaPlanoXY)
        self.play(Indicate(line_y,scale_factor=2),
                  Indicate(prodXYZlabel,scale_factor=2.5),
                  Indicate(prodYZlabel,scale_factor=3),
                  Indicate(line_x,scale_factor=2),
                  run_time=4)
        
        self.wait(7)

        self.play(Indicate(recta,
                           scale_factor=2.5,
                           run_time=2))

        self.wait(3)

class L01_V04_E04_InterpretacionGeometricaDelProductoDeTresNumeros(MiEscenaConVoz):    
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))        
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)

        self.creditos(1)

        cabecera = Tex(_("Interpretación geométrica del producto por escalares en ") + r"$\R[3]$",
                       tex_template = myTemplate,
                       font_size=60).scale_to_fit_width(config.frame_width*.9).to_edge(UP).set_color(BLUE)

        self.add(cabecera)
        self.pausa_corta()

        video1 = VideoMobject(
            filename=r"./media/videos/L01_V04_ProductoDeUnVectorPorUnEscalar/480p15/aux_movie_files/L01_V04_E04_3D_InterpretacionGeometricaDelProductoDeTresNumeros.mp4",
            #filename=r"./media/videos/L01_V04_ProductoDeUnVectorPorUnEscalar/1080p60/aux_movie_files/L01_V04_E04_3D_InterpretacionGeometricaDelProductoDeTresNumeros.mp4",
            speed=1.0
        ).scale_to_fit_width(config.frame_width*.95)

        resumen1 = Tex(_(r"""Para interpretar geométricamente el producto por escalares en \R[3],"""),
        tex_template = myTemplate).scale_to_fit_width(config.frame_width*.9)
        
        resumen2 = Tex(_(r"""antes interpretaremos geométricamente el producto de tres números."""),
                       tex_template = myTemplate).next_to(resumen1, DOWN).scale_to_fit_width(config.frame_width*.9)

        with self.voiceover(text=_("""Para interpretar geométricamente
        el producto por escalares en R3,""")) as tracker:
            
            self.play(Write(resumen1), run_time=tracker.duration+0.2)

        with self.voiceover(text=_("""antes interpretaremos
        geométricamente el producto de tres números.""")) as tracker:
            
            self.play(Write(resumen2), run_time=tracker.duration+0.2)


        with self.voiceover(text=_("""Recordemos que, para multiplicar
        alfa por beta, comenzamos con un rectángulo con una base que
        va desde cero hasta alfa y altura uno""")) as tracker:
            self.play(*[FadeOut(mob)for mob in self.mobjects])
            self.add(video1)
            
        with self.voiceover(text=_("""Y extendemos la diagonal que
        pasa por el origen de coordenadas para obtener una recta
        infinita.""")) as tracker:

            self.wait(tracker.duration)
            print(tracker.duration)

        with self.voiceover(text=_("""El punto de la recta con
        coordenada beta en el eje y, tiene coordenada alfa por beta en
        el eje x.""")) as tracker:

            self.wait(tracker.duration)

        with self.voiceover(text=_("""Pero para multiplicar tres
        números (alfa, beta y gamma) comenzaremos con un prisma cuya
        base rectangular tiene un lado sobre el eje x, que va desde
        cero hasta alfa por beta, y el otro lado sobre el eje 'y', que
        va desde cero hasta beta.""")) as tracker:

            self.wait(tracker.duration)
            
        with self.voiceover(text=_("""Además, la altura del prisma
        será uno.""")) as tracker:
            
            self.wait(tracker.duration)

        with self.voiceover(text=_("""Así, para multiplicar alfa beta
        por un número natural gamma, apilaremos gamma copias del
        citado prisma.""")) as tracker:

            self.wait(tracker.duration)

        with self.voiceover(text=_("""Y luego alinearemos dichos
        prismas a lo largo del eje x sin cambiar su orientación. La
        longitud de la fila creada a lo largo del eje x es igual al
        producto de los tres números. Pero este procedimiento solo
        vale cuando apilamos un número  natural de prismas.""")) as tracker:

            self.wait(tracker.duration)            

        with self.voiceover(text=_("""De nuevo, generalizaremos el
        procedimiento alineando los prismas en una posición intermedia
        entre la pila inicial y la fila final.""")) as tracker:
            
            self.wait(7)

        with self.voiceover(text=_("""Si extendemos la diagonal del
        primer prisma, obtenemos la recta a lo largo de la cual hemos
        alineado los prismas. Dicha recta nos sirve para describir
        geométricamente el producto. El punto de la recta, cuya
        coordenada en el eje z es gamma, tiene coordenada en el eje x
        igual al producto de los tres números.""")) as tracker:
            
            self.wait(9)

        xz = MathTex(r"\frac{z}{x}=\frac{\gamma}{\alpha\beta\gamma}=\frac{1}{\alpha\beta}",
                     tex_template = myTemplate).to_corner(UL)
        
        yz = MathTex(r"\frac{z}{y}=\frac{\gamma}{\beta\gamma}=\frac{1}{\beta}",
                     tex_template = myTemplate).next_to(xz,
                                                        DOWN,
                                                        aligned_edge=LEFT,
                                                        buff=1.3)
        
        xy = MathTex(r"\frac{y}{x}=\frac{\beta\gamma}{\alpha\beta\gamma}=\frac{1}{\alpha}",
                     tex_template = myTemplate).next_to(yz,
                                                        DOWN,
                                                        aligned_edge=LEFT,
                                                        buff=1.3)
        
        with self.voiceover(text=_("""De manera similar a lo visto con
        el producto de dos números, para cada punto de la recta que
        extiende la diagonal del prisma, la proporcionalidad entre las
        coordenadas se mantiene. Así:""")) as tracker:
            
            self.play(video1.animate.scale(.7).to_corner(UR))
            self.play(Write(xz))
            self.play(Write(yz))
            self.play(Write(xy))

        with self.voiceover(text=_("""los ratios
        entre la coordenada z y la coordenada x;""")) as tracker:            
            
            self.play(Indicate(xz),
                      run_time=tracker.duration)
            
        with self.voiceover(text=_("""la coordenada z y la
        coordenada y;""")) as tracker:
            
            self.play(Indicate(yz),
                  run_time=tracker.duration)
            
        with self.voiceover(text=_("""y la coordenada 'y' y la
        cooordenada x""")) as tracker:
            
            self.play(Indicate(xy),
                  run_time=tracker.duration)
            
        with self.voiceover(text=_("""se mantienen en todos los puntos
        de la recta. Es decir, los puntos que mantienen la misma
        proporción entre sus coordenadas se disponen a lo largo de una
        recta que pasa por el origen.""")) as tracker:

            self.wait(tracker.duration+2)

class L01_V04_E05_3D_InterpretacionGeometricaDelProductoPorEscalaresEnR3(ThreeDScene):
    def creditos(self, variante=1):
        def analisis_opcion_elegida(tipo):
            'Análisis de las opciones de eliminación elegidas'
            lista = [100,20,10,4,2,1]
            opcion = set()
            for t in lista:
                if (tipo - (tipo % t)) in lista:
                    opcion.add(tipo - (tipo % t))
                    tipo = tipo % t
            return opcion    
        copyright = Tex(r"\textcopyright{\;} 2025\; Marcos Bujosa  ")
        if 1 in analisis_opcion_elegida(variante):
            stampDcha  = VGroup(copyright.copy()).rotate( PI/2).scale(0.5).to_edge(RIGHT, buff=0.1).set_color(GRAY_D)
            self.add(stampDcha)
        if 2 in analisis_opcion_elegida(variante):
            stampIzda  = VGroup(copyright.copy()).rotate(-PI/2).scale(0.5).to_edge(LEFT, buff=0.1).set_color(GRAY_D)
            self.add(stampIzda)
        if 4 in analisis_opcion_elegida(variante):
            stampBottom= VGroup(copyright.copy()).rotate(    0).scale(0.5).to_edge(DOWN, buff=0.1).set_color(GRAY_D)
            self.add(stampBottom)
        if 10 in analisis_opcion_elegida(variante):
            stampTop   = VGroup(copyright.copy()).rotate(    0).scale(0.5).to_edge(  UP, buff=0.1).set_color(GRAY_D)
            self.add(stampTop)
            
    
    def construct(self):
        axes = ThreeDAxes()
        x_label = axes.get_x_axis_label(Tex("1ª comp."))
        y_label = axes.get_y_axis_label(Tex("2ª comp.")).shift(UP * 2.4).shift(LEFT * 0.6)
       	
        # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.5)
        
        c       = VectorR3([0,0, 2.5], color=RED_B)
        d       = VectorR3([0,0, 4.5], color=RED_B)
        e       = VectorR3([0,0,-4.5], color=RED_B)
        flechac = c.arrow(axes)
        flechad = d.arrow(axes)
        flechae = e.arrow(axes)
        flechac2= flechac.copy()
        c_dot = c.dot(axes)
        d_dot = d.dot(axes)
        e_dot = e.dot(axes)
        c_dot2 = c_dot.copy()
        
        eje_z =  Line(start = [0, 0, -5],
                      end   = [0, 0,  5],
                      color = RED_B)
        
	
        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label))
        self.wait(1)
        self.play(Indicate(c_dot,
                           scale_factor=3,
                           run_time=1.5))
	
        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=60 * DEGREES, zoom=1, run_time=1.5)
	
        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(2)
        
        # caso 1
        self.wait(.5)
	
        self.play(Transform(c_dot,
                            d_dot),
                  run_time=1)
        self.play(Transform(c_dot,
                            e_dot),
                  run_time=1)
        self.play(Transform(c_dot,
                            c_dot2),
                  run_time=1)
        self.play(FadeOut(c_dot)),
		
        self.play(Indicate(eje_z),
                  run_time=1.5)
        self.wait(2)
        self.play(FadeOut(eje_z))
	
        self.wait(2)
        
        Vect = nc.Vector([3,2,3])
        b = VectorR3(Vect.lista, rpr='colum', color=TEAL_A)
        b1 = VectorR3((Vect*nc.fracc(3,2)).lista, rpr='colum', color=TEAL_A)
        b2 = VectorR3((Vect*nc.fracc(1,2)).lista, rpr='colum', color=TEAL_A)
        b3 = VectorR3((Vect*(-1)).lista, rpr='colum', color=TEAL_A)
        b4 = VectorR3((Vect*nc.fracc(-1,2)).lista, rpr='colum', color=TEAL_A)
        b5 = VectorR3((Vect*nc.fracc(-3,2)).lista, rpr='colum', color=TEAL_A)
        b0 = VectorR3((Vect*0).lista, rpr='colum', color=YELLOW)

        b_dot  = b.dot(axes)
        b_dot1 = b1.dot(axes)
        b_dot2 = b2.dot(axes)
        b_dot3 = b3.dot(axes)
        b_dot4 = b4.dot(axes)
        b_dot5 = b5.dot(axes)
        b_dot0 = b0.dot(axes, radio=0.12)

        extremo1 = VectorR3((Vect*5).lista).dot(axes)
        extremo2 = VectorR3((Vect*(-5)).lista).dot(axes)
        recta =  Line(start = extremo1.get_center(),
                      end   = extremo2.get_center(),
                      color = BLUE_B)

        self.play(Indicate(b_dot))
        line_x = b.x_line(axes)
        self.add(line_x)
        line_y = b.y_line(axes)
        self.add(line_y)
        line_z = b.z_line(axes)
        self.add(line_z)
        line_xy = b.xy_line(axes)
        self.add(line_xy)

        line_v = b.v_line(axes)
        self.add(line_v)

        self.wait(2.5)
                
        self.play(TransformFromCopy(b_dot,
                                    b_dot1), run_time=3)
        
        self.play(TransformFromCopy(b_dot,
                                    b_dot2), run_time=3)
 
        self.play(TransformFromCopy(b_dot,
                                    b_dot3),
                  TransformFromCopy(b_dot,
                                    b_dot4),
                  TransformFromCopy(b_dot,
                                    b_dot5), run_time=4.5)

        self.wait(1)

        self.play(TransformFromCopy(b_dot,
                                    b_dot0), run_time=3.5)
       
        self.wait(15)
        
        self.play(FadeOut(b_dot),
                  #FadeOut(b_dot0),
                  FadeOut(b_dot1),
                  FadeOut(b_dot2),
                  FadeOut(b_dot3),
                  FadeOut(b_dot4),
                  FadeOut(b_dot5),
                  FadeIn(recta))

        self.wait(10)

import cv2 # needs opencv-python https://pypi.org/project/opencv-python/
from PIL import Image, ImageOps
from dataclasses import dataclass

@dataclass
class VideoStatus:
    time: float = 0
    videoObject: cv2.VideoCapture = None
    def __deepcopy__(self, memo):
        return self

class VideoMobject(ImageMobject):
    '''
    Following a discussion on Discord about animated GIF images.
    Modified for videos

    Parameters
    ----------
    filename
        the filename of the video file

    imageops
        (optional) possibility to include a PIL.ImageOps operation, e.g.
        PIL.ImageOps.mirror

    speed
        (optional) speed-up/slow-down the playback

    loop
        (optional) replay the video from the start in an endless loop

    https://discord.com/channels/581738731934056449/1126245755607339250/1126245755607339250
    2023-07-06 Uwe Zimmermann & Abulafia
    2024-03-09 Uwe Zimmermann
    '''
    def __init__(self, filename=None, imageops=None, speed=1.0, loop=False, **kwargs):
        self.filename = filename
        self.imageops = imageops
        self.speed    = speed
        self.loop     = loop
        self._id = id(self)
        self.status = VideoStatus()
        self.status.videoObject = cv2.VideoCapture(filename)

        self.status.videoObject.set(cv2.CAP_PROP_POS_FRAMES, 1)
        ret, frame = self.status.videoObject.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            
            img = Image.fromarray(frame)

            if imageops != None:
                img = imageops(img)
        else:
            img = Image.fromarray(np.uint8([[63, 0, 0, 0],
                                        [0, 127, 0, 0],
                                        [0, 0, 191, 0],
                                        [0, 0, 0, 255]
                                        ]))
        super().__init__(img, **kwargs)
        if ret:
            self.add_updater(self.videoUpdater)

    def videoUpdater(self, mobj, dt):
        if dt == 0:
            return
        status = self.status
        status.time += 1000*dt*mobj.speed
        self.status.videoObject.set(cv2.CAP_PROP_POS_MSEC, status.time)
        ret, frame = self.status.videoObject.read()
        if (ret == False) and self.loop:
            status.time = 0
            self.status.videoObject.set(cv2.CAP_PROP_POS_MSEC, status.time)
            ret, frame = self.status.videoObject.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # needed here?        
            img = Image.fromarray(frame)

            if mobj.imageops != None:
                img = mobj.imageops(img)
            mobj.pixel_array = change_to_rgba_array(
                np.asarray(img), mobj.pixel_array_dtype
            )


class L01_V04_E05_InterpretacionGeometricaDelProductoPorEscalaresEnR3(MiEscenaConVoz):
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))        
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)

        self.creditos(1)

        titulo = Tex(_("Interpretación geométrica del producto en ") + r"$\R[3]$",
                       tex_template = myTemplate,
                       font_size=60).set_color(BLUE).to_edge(UP)

        video1 = VideoMobject(
            filename=r"./media/videos/L01_V04_ProductoDeUnVectorPorUnEscalar/480p15/aux_movie_files/L01_V04_E05_3D_InterpretacionGeometricaDelProductoPorEscalaresEnR3.mp4",
            #filename=r"./media/videos/L01_V04_ProductoDeUnVectorPorUnEscalar/1080p60/aux_movie_files/L01_V04_E05_3D_InterpretacionGeometricaDelProductoPorEscalaresEnR3.mp4",
           speed=1.0
        ).scale_to_fit_width(6.5).next_to(titulo, DOWN, buff=0)

        escalar = sp.symbols('\lambda')
        c3      = sp.symbols('a_3')
        c       = nc.Vector([0,0,c3])
        s0      = MathTex(r"\lambda " + c.latex(),   tex_template = myTemplate,)
        igual   = MathTex(r"=",        tex_template = myTemplate,)
        s05     = MathTex((escalar*c).latex(), tex_template = myTemplate,)
        grp0 = VGroup(s0,
                      igual,
                      s05).arrange(RIGHT).next_to(video1, DOWN).scale(.9)
       
        escalar = sp.symbols('\lambda')
        a  = nc.Vector(sp.symbols('a:4')[1:])
        s1 = MathTex(r"\lambda " + a.latex(),
                     tex_template = myTemplate,)
        s5 = MathTex((escalar*a).latex(),
                     tex_template = myTemplate,)
        grp1 = VGroup(s1,
                      igual.copy(),
                      s5).arrange(RIGHT).next_to(video1, DOWN).scale(.9)
        
        self.creditos(17)
      
        with self.voiceover(text=_("""La interpretación geométrica del
        producto por escalares en R3 es similar a la de R2.""")) as tracker:
            
            self.add(titulo)
            self.add(video1)
            self.pausa(4)

        with self.voiceover(text=_("""En el caso en el que todas las
        componentes salvo la última son cero.""")) as tracker:
            
            self.play(FadeIn(grp0))
            self.pausa(3)
                        
        with self.voiceover(text=_("""El conjunto de múltiplos
        constituye el eje vertical.""")) as tracker:
            
            self.pausa(7.7)
            self.play(FadeOut(grp0))
            
        with self.voiceover(text=_("""En cuanto a cualquier otro tipo
        de vector no nulo.""")) as tracker:
            
            self.play(FadeIn(grp1))

        with self.voiceover(text=_("""Dependiendo del valor del
        escalar, las componentes del múltiplo serán mayores o
        menores.""")) as tracker:
            
            self.pausa(1)

        with self.voiceover(text=_("""Y si el escalar es negativo,
        cambiará el signo de las componentes del vector.""")) as tracker:

            self.pausa(tracker.duration)

        with self.voiceover(text=_("""Además, cualquier vector
        multiplicado por cero es un vector nulo.""")) as tracker:
            
            self.pausa(tracker.duration)
            self.play(FadeOut(grp1))
            self.pausa(1)

        cvab = MathTex(r"\elemRp{\lambda\Vect{a}}{i}", tex_template = myTemplate)
        cvb  = MathTex(r"\lambda\eleVRpE{a}{i}", tex_template = myTemplate)
        eq_suma = VGroup(cvab,igual,cvb).arrange(RIGHT).scale(1.5)
        
        grp3 = VGroup(eq_suma,).arrange(RIGHT,
                                          buff=1).next_to(video1,
                                                          DOWN).scale(1)

        r1 =  MathTex(r"""\frac{\lambda a_j}{\lambda a_k}=\frac{a_j}{a_k}\qquad
        \text{para todo}\; \lambda, j, k,\;
        \text{ si }\; a_k\ne0""",
                      tex_template = myTemplate).next_to(video1,
                                                         DOWN).scale(1)
        
        with self.voiceover(text=_("""Como las componentes del vector
        son multiplicadas por un mismo valor, las proporciones entre
        las cordenadas no nulas se mantienen entre todos los
        múltiplos.""")) as tracker:
            
            self.play(FadeIn(grp3))
            self.pausa(tracker.duration*2/5)
            self.play(FadeOut(grp3))           
            self.play(FadeIn(r1))
            
        with self.voiceover(text=_("""Así, dada la interpretación del
        producto entre tres números vista anteriormente, los múltiplos
        de un vector no nulo de R3 se corresponden con los puntos de
        una recta que pasa por el origen de coordenadas.""")) as tracker:
            
            self.pausa(tracker.duration)
            self.play(FadeOut(r1),
                      FadeOut(video1))

        resumen1 = Tex(_(r"""El conjunto de múltiplos de un vector no nulo de \R[3]"""),
                       tex_template = myTemplate)
        resumen2 = Tex(_(r"""se corresponde con una recta que pasa por el origen."""),
                       tex_template = myTemplate).next_to(resumen1, DOWN)
            
        with self.voiceover(text=_("""Por tanto, el conjunto de
        múltiplos de cualquier vector no nulo de R 3 es una recta que
        pasa por el origen.""")) as tracker:
            self.play(Write(resumen1),
                      run_time=tracker.duration/2)
            self.play(Write(resumen2),
                      run_time=tracker.duration/2)

            self.pausa_muy_corta()
            self.play(FadeOut(resumen1),
                      FadeOut(resumen2))

        titulo2 = Tex(_("Interpretación geométrica del producto en ") + r"$\R[n]$",
                       tex_template = myTemplate,
                       font_size=60).set_color(BLUE).to_edge(UP)

        resumenRn_1 = Tex(_(r"""El conjunto de múltiplos de un vector no nulo de \R[n]"""),
                          tex_template = myTemplate)
        resumenRn_2 = Tex(_(r"""se corresponde con una recta que pasa por el origen."""),
                          tex_template = myTemplate).next_to(resumenRn_1, DOWN)
                
        with self.voiceover(text=_("""Reescalar un vector en R n
        mantiene la proporción entre sus coordenadas. Aunque no
        podemos visualizar una recta en más de tres dimensiones,
        abusando del lenguaje diremos que: los múltiplos de un vector
        en R n se corresponden con una recta que pasa por el
        origen.""")) as tracker:

            self.play(FadeOut(titulo))
            self.play(FadeIn(titulo2))
            self.pausa(tracker.duration/2)
            self.play(Write(resumenRn_1))
            self.play(Write(resumenRn_2))
            self.pausa(2)
