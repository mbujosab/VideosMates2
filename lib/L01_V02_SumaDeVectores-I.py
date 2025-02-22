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
        copyright = Tex(r"\textcopyright{\;} 2024\; Marcos Bujosa  ")
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
            
         

class L01_V02_E01_SumaDeVectores(MiEscenaConVoz):    
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))       
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)

        self.creditos()
        
        # Portada
        titulo = Title(_("Suma de vectores en ") + r"\R[n]",
                     tex_template = myTemplate,
                     font_size=70).set_color(BLUE)
        self.play(Write(titulo))
        self.pausa_media()
        self.play(FadeOut(titulo))
	
        # Definición de vector suma
        operacionSuma = Tex(_("Suma de vectores"),
                         tex_template = myTemplate, font_size=70
                         ).to_edge(UP).set_color(BLUE)

        operacionDescripcion = Tex(_("La suma se define componente a componente."),
                         tex_template = myTemplate,
                         ).move_to([0,2.5,0]).to_edge(LEFT)
        # Ejemplos
        EjR3 = Tex(r"\textbf{" + _("Ejemplo en ") + r"\R[3]:}",
                 tex_template = myTemplate,
                 font_size=50).set_color(GREEN).next_to(operacionDescripcion, DOWN, aligned_edge=LEFT)

        EjR4 = Tex(r"\textbf{" + _("Ejemplo en ") + r"\R[4]:}",
                 tex_template = myTemplate,
                 font_size=50).set_color(GREEN).next_to(operacionDescripcion, DOWN, aligned_edge=LEFT)
        
        a    = nc.Vector( [0, 3, 6])        
        b    = nc.Vector( [5, 1, 2])        
        s1 = MathTex(a.latex(),        tex_template = myTemplate,)
        mas= MathTex(r"+",             tex_template = myTemplate,)
        s3 = MathTex(b.latex(),        tex_template = myTemplate,)
        igual = MathTex(r"=",             tex_template = myTemplate,)
        s5 = MathTex((a+b).latex(),    tex_template = myTemplate,)
        grp1 = VGroup(s1,mas,s3,igual,s5).arrange(RIGHT)
       
        self.add(operacionSuma)
        self.add(operacionDescripcion)
        
        with self.voiceover(text=_("""Podemos sumar dos vectores si ambos poseen el mismo número de
        componentes.""")) as tracker:
            self.add(EjR3)
            self.add(grp1[0])
            self.add(grp1[2])

        with self.voiceover(text=_("""El resultado es otro vector que se define componente a
        componente.""")) as tracker:
            self.add(grp1[1])
            self.pausa_media()
            self.add(grp1[3])
            self.add(grp1[4][0][:2])
            self.add(grp1[4][0][-2:])

        with self.voiceover(text=_("""La primera es la suma de las primeras componentes de ambos
        vectores.""")) as tracker:
            self.play(FadeIn(grp1[4][0][2]), run_time=tracker.duration/3)
            self.play(Circumscribe(grp1[0][0][2]), Circumscribe(grp1[2][0][2]), run_time=tracker.duration*2/3)
            self.pausa_corta()
            
        with self.voiceover(text=_("""La segunda es la suma de las segundas.""")) as tracker:
            self.play(FadeIn(grp1[4][0][3]), run_time=tracker.duration/3)
            self.play(Circumscribe(grp1[0][0][3]), Circumscribe(grp1[2][0][3]), run_time=tracker.duration*2/3)
            self.pausa_corta()
            
        with self.voiceover(text=_("""Y así con todas las componentes del vector suma.""")) as tracker:            
            self.play(FadeIn(grp1[4][0][4]))
            self.pausa_corta()
            self.play(Circumscribe(grp1[0][0][4]), Circumscribe(grp1[2][0][4]) )
            self.pausa_corta(.3)
            self.play(FadeOut(grp1))

        self.pausa()

        v_generico_a  = nc.Vector(sp.symbols('a:5')[1:])
        vga = MathTex(v_generico_a.latex(), tex_template = myTemplate)
        
        v_generico_b  = nc.Vector(sp.symbols('b:5')[1:])
        vgb = MathTex(v_generico_b.latex(), tex_template = myTemplate)

        vgab = MathTex((v_generico_a + v_generico_b).latex(), tex_template = myTemplate)

        grp2 = VGroup(vga,mas,vgb,igual,vgab).arrange(RIGHT)
        with self.voiceover(text=_("""Por tanto, la siguiente expresión describe
        la suma de vectores en R 4.""")) as tracker:
            self.play(FadeTransform(EjR3,EjR4))
            self.play(FadeIn(grp2))
            self.pausa()

        with self.voiceover(text=_("""Definir la suma en R n requiere una estrategia distinta; una que no
        necesite escribir la lista completa de componentes. Piense que
        la lista puede ser muy larga cuando n es grande.""")) as tracker:
            self.wait(tracker.duration/3)
            self.play(Indicate(vga[0][4:-4]), Indicate(vgb[0][4:-4]), Indicate(vgab[0][4:-4]), run_time=2)
            self.pausa_corta()

        Defn = Tex(r"\textbf{" + _("Definición") + ":}",
                 tex_template = myTemplate,
                 font_size=50).set_color(RED).next_to(operacionDescripcion, DOWN, aligned_edge=LEFT)
        
        with self.voiceover(text=_("""Una alternativa es definir la suma usando la notación
        descrita en el vídeo anterior. Con ella podemos expresar""")) as tracker:
            self.play(FadeOut(grp2), FadeOut(EjR4), run_time=tracker.duration/3)
            self.add(Defn)

        cvab = MathTex(r"\elemRp{\Vect{a}+\Vect{b}}{i}", tex_template = myTemplate)
        cva  = MathTex(r"\eleVR{a}{i}", tex_template = myTemplate)
        cvb  = MathTex(r"\eleVR{b}{i}", tex_template = myTemplate)
        eq_suma = VGroup(cvab,igual,cva,mas,cvb).arrange(RIGHT).scale(1.5)
        
        donde = Tex(_("donde"))
        indices = MathTex(r"i=1:n", tex_template = myTemplate)
        pc_indices = VGroup(donde,indices).arrange(RIGHT, buff=1)
        grp3 = VGroup(eq_suma, pc_indices).arrange(RIGHT, buff=1)

        with self.voiceover(text=_("""que la componente i-ésima del vector suma es igual a la suma
        de las i-ésimas componentes de los vectores.""")) as tracker:
            self.play(FadeIn(grp3[0][:2],
                             scale=1.5,
                             rate_func=rate_functions.exponential_decay),
                      run_time=2*tracker.duration/5)
            self.play(FadeIn(grp3[0][2:],
                             scale=0.5,
                             rate_func=rate_functions.exponential_decay),
                      run_time=3*tracker.duration/5)
        with self.voiceover(text=_(r"""(donde el índice recorre los números naturales entre uno
        y n)""")) as tracker:
            self.play(FadeIn(grp3[1]))
            self.pausa_corta()

        with self.voiceover(text=_(r"""Esta definición abstracta será muy util para demostrar algunas
        propiedades de las operaciones con vectores, pues arroja una
        primera regla de cálculo simbólico:""")) as tracker:
            self.pausa(tracker.duration*2/3)
            self.play(Indicate(eq_suma[0][0][0]),
                      Indicate(eq_suma[0][0][-3:]),
                      Indicate(eq_suma[2][0][-2:]),
                      Indicate(eq_suma[4][0][-2:]),
                      run_time=tracker.duration/3)
            self.pausa_muy_corta()

        with self.voiceover(text=_(r"""que la suma de las i-ésimas componentes se puede sustituir por
        la i-ésima componente del vector suma.""")) as tracker:            
            source0 = MathTex(r"\eleVR{a}{i}+\eleVR{b}{i}",
                              tex_template = myTemplate).next_to(grp3, DOWN, buff=1.2).scale(2)[0]
            target0 = MathTex(r"\elemRp{\Vect{a}+\Vect{b}}{i}",
                              tex_template = myTemplate).next_to(grp3, DOWN, buff=1.2).scale(2)[0]
            source1 = target0.copy()
            target1 = source0.copy()
            
            VGroup(source0,target0)
            self.add(source0)
            transform_index0 = [[0,1,2,3,4,5,6],
                                [1,0,4,2,3,5,6]]
            self.play(
                *[
                    ReplacementTransform(source0[i],target0[j], rate_func=rate_functions.smooth)
                    for i,j in zip(*transform_index0)
                ],
                run_time=tracker.duration)
            
        with self.voiceover(text=_("""Y la i-ésima componente de una suma se puede sustituir por la
        suma de las i-ésimas componentes.""")) as tracker:            
            self.play(ReplacementTransform(target0,source1))
            
            VGroup(source1,target1)
            transform_index1 = [[0,1,2,3,4,5,6],
                                [1,0,3,4,2,5,6]]
            self.play(
                *[
                    ReplacementTransform(source1[i],target1[j], rate_func=rate_functions.smooth)
                    for i,j in zip(*transform_index1)
                ],
                run_time=tracker.duration)
	    
        with self.voiceover(text=_("""Esta regla se denomina propiedad distributiva del operador selector
        respecto de la suma.""")) as tracker:            
            self.play(FadeOut(target1))
            self.play(Indicate(eq_suma[0][0][0]),
                      Indicate(eq_suma[0][0][-3:]),
                      Indicate(eq_suma[2][0][-2:]),
                      Indicate(eq_suma[4][0][-2:]),
                      run_time=tracker.duration)
            self.pausa()

class L01_V02_E02_PropiedadConmutativaDeLaSuma(MiEscenaConVoz):    
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))        
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)

        self.creditos(7)
        	
        operacionSuma = Tex(_("Suma de vectores en ") + r"\R[n]",
                            tex_template = myTemplate,
                            font_size=70).to_edge(UP).set_color(BLUE)        
        self.add(operacionSuma)
        
        source0  = MathTex(r"\elemRp{\Vect{a}+\Vect{b}}{i}", tex_template = myTemplate).scale(2)[0]
        source1  = source0.copy()
        target0  = MathTex(r"\elemRp{\Vect{b}+\Vect{a}}{i}", tex_template = myTemplate).scale(2)[0]
        igual = MathTex(r"=",             tex_template = myTemplate,).scale(2)[0]
        vgr0  = VGroup(source0, igual, source1).arrange(RIGHT, buff=1)
        vgr1  = VGroup(source0, igual, target0).arrange(RIGHT, buff=1)
        transform_index0 = [[1,2,3],
                            [3,2,1]]

        with self.voiceover(text=_("""Usemos la anterior regla de cálculo simbólico para demostrar la
        propiedad conmutativa de la suma. Es decir, que el orden en que se sumen los vectores es
        irrelevante.""")) as tracker:
            self.play(FadeIn(source0[1:-3]), FadeIn(vgr1[1]), FadeIn(source1[1:-3]))
            self.pausa(tracker.duration/2)
            self.play(
                *[
                    ReplacementTransform(vgr0[2][i],vgr1[2][j], rate_func=rate_functions.smooth)
                    for i,j in zip(*transform_index0)
                ],
                run_time=tracker.duration/2)
            self.pausa_corta()
            
        with self.voiceover(text=_("""Sabemos que dos vectores son iguales si lo son sus correspondientes
        listas de componentes. Por tanto, para demostrar la igualdad entre vectores debemos probar
        la igualdad componente a componente.""")) as tracker:           
            self.pausa(tracker.duration*2/5)
            self.play(FadeIn(source0[0]), FadeIn(source0[-3:]), FadeIn(target0[0]), FadeIn(target0[-3:]) )
            self.pausa(tracker.duration/4)
            self.play(Indicate(source0[-2:]), Indicate(target0[-2:]), run_time=tracker.duration/4)
            self.pausa_corta()

        with self.voiceover(text=_("""Para ello comenzaremos escribiendo uno cualquiera de sus lados.
        Después operaremos hasta obtener la expresión del lado opuesto de la igualdad.""")) as tracker:            
            self.pausa(tracker.duration/4)
            self.play(Indicate(vgr0[0]))
            self.play(Indicate(vgr1[2]))

        vgr2=vgr1.copy().scale(1/2).next_to(operacionSuma, DOWN).to_edge(LEFT)
        vgr3=vgr1.copy().scale(1/2).to_edge(LEFT)
        item1 = MathTex(r"\eleVR{x}{i} \in \R",tex_template = myTemplate)
        item2 = MathTex(r"\alpha + \beta = \beta + \alpha\quad (\alpha,\beta\in\R)",
                        tex_template = myTemplate)
        item3 = MathTex(r"\elemRp*{\Vect{x}+\Vect{y}}{i} = \eleVR{x}{i} + \eleVR{y}{i}",
                        tex_template = myTemplate)
        items = VGroup(item1,
                       item2,
                       item3).arrange(DOWN).scale(.8).align_to(vgr2, UP).to_edge(RIGHT).shift(DOWN*0.15)        
        box =  SurroundingRectangle(items, color=YELLOW )

        paso1 = MathTex(r"=\eleVR{a}{i}+\eleVR{b}{i}",
                        tex_template = myTemplate).next_to(vgr3[0], RIGHT)
        paso2 = MathTex(r"=\eleVR{b}{i}+\eleVR{a}{i}",
                        tex_template = myTemplate).next_to(paso1, DOWN, aligned_edge=LEFT)
        paso3 = MathTex(r"=\elemRp{\Vect{b}+\Vect{a}}{i}",
                        tex_template = myTemplate).next_to(paso2, DOWN, aligned_edge=LEFT)
        demo = VGroup(paso1, paso2, paso3)
        
        with self.voiceover(text=_("""Con operar nos referimos a sustituir una expresión por otra que sabemos
        que es equivalente. Para esta demostración solo necesitamos considerar tres cosas""")) as tracker:
            self.play(FadeTransformPieces(vgr1,vgr2),
                      run_time=tracker.duration/2 )
            self.add(box,items)
            self.pausa_muy_larga()

        with self.voiceover(text=_("""que los elementos de un vector son números reales,
        que entre números reales la suma es conmutativa,
        y que el operador selector es distributivo respecto de la suma""")) as tracker:
            self.play(Indicate(items[0]), run_time=tracker.duration/3 )
            self.play(Indicate(items[1]), run_time=tracker.duration/3 )
            self.play(Indicate(items[2]), run_time=tracker.duration/3 )
            
        with self.voiceover(text=_("""Comencemos escribiendo uno de los lados,
        por ejemplo el izquierdo.""")) as tracker:
            self.play( FadeTransformPieces(vgr2[0].copy(),vgr3[0]),
                       FadeToColor(vgr2[0], color=TEAL),
                       run_time=tracker.duration/2 )
            self.pausa_media()
            
        with self.voiceover(text=_("""En primer lugar,
        el operador selector es distributivo respecto de la suma""")) as tracker:
            self.play(Indicate(items[2], run_time=tracker.duration/2) )
            self.play(FadeIn(demo[0],    run_time=tracker.duration/2) )
            
        with self.voiceover(text=_("""En segundo lugar, dado que los componentes son números reales,
        el resultado no cambia si intercambiamos el orden de su suma.""")) as tracker:            
            self.play(Indicate(items[:2], run_time=tracker.duration/2) )
            self.play(FadeIn(demo[1],     run_time=tracker.duration/2) )
            
        with self.voiceover(text=_("""Por último,
        el operador selector es distributivo respecto de la suma""")) as tracker:
            self.play(Indicate(items[2], run_time=tracker.duration/2) )
            self.play(FadeIn(demo[2],    run_time=tracker.duration/2) )

        with self.voiceover(text=_("""Con esto termina la demostración.""")) as tracker:
            self.play(FadeToColor(vgr2[0], color=TEAL))
            self.play(Indicate(vgr3[0]),
                      Indicate(demo[2]),
                      FadeToColor(vgr2[1:], color=TEAL),
                      run_time=tracker.duration)
            self.pausa()

        with self.voiceover(text=_("""En el próximo vídeo daremos una interprtación
        geométrica de la suma de vectores.""")) as tracker:
            self.pausa_muy_larga()
