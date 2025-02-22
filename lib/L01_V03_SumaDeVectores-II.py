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
            
         

class VectorR2():
    def __init__(self, lista, rpr='c', color=GRAY_B):
        """Inicializa un Vector con una lista"""
        coords = lista + [0] if len(lista)<3 else lista
        self.color  = color
        self.coords = tuple(coords)
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
        self.coords = tuple(coords)
        self.Vector = nc.Vector(self.coords, rpr)
        self.tex    = MathTex(self.Vector.latex(), color=self.color).scale(0.8)

    def dot(self, ejes, radio=0.08):
        return Dot3D(ejes.c2p(*self.coords), radius=radio, color=self.color)

    def v_line(self, ejes):
        return ejes.get_vertical_line(ejes.c2p(*self.coords), color=self.color)

    def h_line(self, ejes):
        return ejes.get_horizontal_line(ejes.c2p(*self.coords), color=self.color)

    def arrow(self, ejes):
        return Arrow3D(
            start=np.array([0, 0, 0]),
            end=np.array(ejes.c2p(*self.coords)),
            resolution=8,
            color = self.color )

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


class L01_V03_E01_SumaEnR2(MiEscenaConVoz):
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))        
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)
        
        self.creditos()

        # Portada
        titulo = Title(_("Interpretación geométrica de la suma"),
                     tex_template = myTemplate,
                     font_size=70).set_color(BLUE)
        self.play(Write(titulo))
        self.pausa_media()
        self.play(FadeOut(titulo))
        
        axes = NumberPlane(x_range=(-4.5, 6.5, 1),
                           y_range=(-1.5, 6.5, 1),
                           background_line_style={
                               "stroke_width":  3,
                               "stroke_opacity": 0.4 }
                           ).add_coordinates()

        item0 = MathTex(r"\elemRp*{\Vect{a}+\Vect{b}}{i} = \eleVR{a}{i} + \eleVR{b}{i}",
                        tex_template = myTemplate)
        item1 = MathTex(r"\Vect{a}+\Vect{x} = \Vect{x}+\Vect{a}",
                        tex_template = myTemplate).next_to(item0, DOWN, buff=0.5)
        props_suma = VGroup(item0,item1).scale(1.5)

        cabecera = Tex(_("Base de la interpretación"),
                         tex_template = myTemplate, font_size=70
                         ).to_edge(UP).set_color(BLUE)
        
        self.add(cabecera)
        
        with self.voiceover(text=_("""Que la operación suma sea una operación componente a
        componente""")) as tracker:
            self.play(FadeIn(props_suma[0]),
                      run_time=tracker.duration)

        with self.voiceover(text=_("""y que sea conmutativa""")) as tracker:
            self.play(Write(props_suma[1], run_time=tracker.duration/5))
            
        with self.voiceover(text=_("""dota a la suma de interpretación geométrica tanto en R 2 como
        en R 3.""")) as tracker:
            self.pausa(tracker.duration)
            self.play(FadeOut(props_suma),
                      FadeOut(cabecera))
            
        x     = VectorR2([4,5], color=GREEN_B)
        x_dot = x.dot(axes, radio=0.12)
        x_tex = x.tex.scale(1.4)
        vgr_x = VGroup(x.tex).next_to(x_dot, RIGHT).shift(RIGHT*.1)
        x_v_line = x.v_line(axes)
        x_h_line = x.h_line(axes)       
        with self.voiceover(text=_(""" Para verlo debemos interpretar los vectores como puntos en
        el espacio, de manera que las componentes de cada vector sean las coordenadas de un
        punto.""")) as tracker:
            self.play(Create(axes), run_time=tracker.duration/2)

        with self.voiceover(text=_("""En R 2, el convenio es considerar que la primera componente
        es la coordenada respecto al eje horizontal""")) as tracker:
            self.add(vgr_x)
            self.pausa(tracker.duration/3)
            self.play(Circumscribe(x_tex[0][1]),
                      Indicate(x_v_line),
                      run_time=tracker.duration*2/3)
            
        with self.voiceover(text=_("""y la segunda como la coordenada respecto al eje vertical.
        """)) as tracker:
            self.play(Circumscribe(x_tex[0][2]),
                      Indicate(x_h_line),
                      run_time=tracker.duration/2)
            self.add(x_dot)
            self.play(Indicate(x_dot),
                      run_time=tracker.duration/2)
            
        with self.voiceover(text=_("""Consecuentemente, vectores con distintas componentes corresponden
        a puntos distintos.""")) as tracker: 
            self.pausa(tracker.duration)
            self.play(FadeOut(vgr_x, x_dot, x_h_line, x_v_line))
            
        a = VectorR2([0,0], rpr='colum', color=YELLOW)
        a_dot = a.dot(axes, radio=0.12)
        a_tex = a.tex
        vgr_a = VGroup(a.tex).next_to(a_dot, DOWN).shift(LEFT*.5)
        with self.voiceover(text=_("""El vector cero corresponde con el origen del sistema de
        coordenadas""")) as tracker:
            self.play(Indicate(a_dot), Indicate(a_tex), run_time=tracker.duration)
            self.pausa

        #añado punto en el eje horizontal quitando el anterior
        b1 = VectorR2([3,0], rpr='colum')
        b1_dot = b1.dot(axes, radio=0.12)
        b1_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                            fill_color=ORANGE).rotate(45*DEGREES).move_to(b1_dot)
        b1_tex = b1.tex
        vgr_b1= VGroup(b1_tex).next_to(b1_dot, DOWN)
        
        with self.voiceover(text=_("""La primera componente de un vector indica su coordenada respecto
        al eje horizontal. Los valores positivos corresponden a posiciones a la derecha del origen de
        coordenadas.""")) as tracker:
            self.play(FadeOut(a_dot, a_tex), FadeIn(b1_diamond))

        #lo muevo y le pongo etiqueta
        b1n    = VectorR2([-2.5,0])
        vgr_b1n= VGroup(b1n.tex).next_to(b1n.dot(axes, radio=0.12), DOWN)
        b1n_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                             fill_color=ORANGE).rotate(45*DEGREES).move_to(b1n.dot(axes))
        with self.voiceover(text=_("""Y valores negativos a posiciones a la izquierda. Así, el vector
        3 0 corresponde al punto del eje horizontal que está 3 unidades a la derecha del origen.""")) as tracker:
            self.play(ReplacementTransform(b1_diamond, b1n_diamond),
                      rate_function=exponential_decay,
                      run_time=tracker.duration/3)
            self.play(ReplacementTransform(b1n_diamond, b1_dot),
                      FadeIn(b1.tex),
                      rate_function=smooth,
                      run_time=2*tracker.duration/3)

        #añado punto inicial en el eje vertical
        b2i    = VectorR2([0,4])
        vgr_b2i= VGroup(b2i.tex).next_to(b2i.dot(axes, radio=0.12), LEFT)
        #b2i_dot = b2i.dot(axes, radio=0.12)
        b2i_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                             fill_color=ORANGE).rotate(45*DEGREES).move_to(b2i.dot(axes))
        with self.voiceover(text=_("""La segunda componente indica la coordenada respecto al eje vertical.
        Valores positivos corresponden a posiciones por encima del origen de coordenadas.""")) as tracker:
            self.add(b2i_diamond)
            self.pausa
        
        # punto con oordenada negativa
        b2n    = VectorR2([0,-1])
        vgr_b2n= VGroup(b2n.tex).next_to(b2n.dot(axes, radio=0.12), DOWN)
        #b2n_dot = b2n.dot(axes, radio=0.12)
        b2n_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                             fill_color=ORANGE).rotate(45*DEGREES).move_to(b2n.dot(axes))
        
        #lo muevo y pongo etiqueta
        b2    = VectorR2([0,2], rpr='colum')
        b2_dot = b2.dot(axes, radio=0.12)
        b2_tex = b2.tex
        vgr_b2= VGroup(b2_tex).next_to(b2_dot, LEFT)
        with self.voiceover(text=_("""Y valores negativos a posiciones por debajo. Por tanto el vector
        0 2 corresponde al punto del eje vertical que está 2 unidades por encima del origen.""")) as tracker:
            self.play(ReplacementTransform(b2i_diamond,
                                           b2n_diamond,
                                           rate_function=exponential_decay,
                                           run_time= tracker.duration/4))
            self.play(ReplacementTransform(b2n_diamond,
                                           b2_dot,
                                           rate_function=smooth,
                                           run_time=2*tracker.duration/3))
            self.add(b2_tex)
            self.pausa(n=3)
        
        b     = VectorR2([3,2], color=TEAL_A)
        b_dot = b.dot(axes, radio=0.12)
        b_tex = b.tex
        vgr_b = VGroup(b_tex).next_to(b_dot, RIGHT)
        
        # arriba añadir (0,3)+(1,0) = (3,1)
        suma1_gr = VGroup(VectorR2([3,0]).tex,
                          MathTex(r"+"),
                          VectorR2([0,2]).tex,
                          MathTex(r"="),
                          b.tex.copy(),
                          ).arrange(RIGHT).to_corner(UL)
        
        with self.voiceover(text=_("""Ahora consideremos la suma de estos dos vectores.
        Se realiza componente a componente."""))  as tracker:
            self.add(suma1_gr[:3])
            #self.pausa(3*tracker.duration/4)
            #self.play(FadeIn(suma1_gr[3:]), run_time=tracker.duration/4)
            #self.pausa_larga

        with self.voiceover(text=_("""Por una parte se suman las coordenadas respecto al
        eje horizontal, y por otra las coordenadas correspondientes al eje vertical. Así,
        el vector suma es el vector 3 2."""))  as tracker:
            self.play(Circumscribe(suma1_gr[0][0][1]),
                      Circumscribe(suma1_gr[2][0][1]),
                      run_time=tracker.duration/3)
            self.play(Circumscribe(suma1_gr[0][0][2]),
                      Circumscribe(suma1_gr[2][0][2]),
                      run_time=tracker.duration/3)
            self.play(FadeIn(suma1_gr[3:]), run_time=tracker.duration/3)
            self.pausa_larga
            
        # pintar b con un punto y ejes y etiqueta
        b_v_line = b.v_line(axes)
        b_h_line = b.h_line(axes)
        with self.voiceover(text=_("""Sus componentes nos indican que el punto está tres unidades a
        la derecha del origen y dos unidades por encima."""))  as tracker:
            self.play(FadeIn(b_dot, b_tex, b_v_line, b_h_line))
            self.pausa

        # Añadir flechas ejes (quitando puntos) y desplazar para mostrar suma
        flechab1 = b1.arrow(axes)
        flechab2 = b2.arrow(axes)
        with self.voiceover(text=_("""Señalando la posición de cada sumando con una flecha,
        podemos interpretar dicha flecha como una indicación para llegar al punto.""")) as tracker:
            self.play(GrowArrow(flechab1),
                      FadeOut(b1_dot),
                      GrowArrow(flechab2),
                      FadeOut(b2_dot),
                      FadeOut(b_dot) )
            
        with self.voiceover(text=_("""Por ejemplo, al primer sumando se llega desplazandose desde el
        origen tres unidades a la derecha. De este modo dotamos a la suma de interpretación geométrica.
        """)) as tracker:
            self.play(Indicate(b1_tex),
                      run_time=tracker.duration/2)

        # SUMA b1 + b2
        a_dot_copy  = a_dot.copy()
        b1_dot_copy = b1_dot.copy()
        b_dot_copy  = b_dot.copy()
        with self.voiceover(text=_("""Sumar el primer vector con el segundo corresponde a seguir las
        indicaciones del primer vector""")) as tracker:
            self.play(#Indicate(flechab1),
                      Indicate(b1_tex),
                      Indicate(suma1_gr[0]),
                      ReplacementTransform(a_dot_copy, b1_dot_copy),
                      run_time=tracker.duration)
        
        with self.voiceover(text=_("""y luego seguir las indicaciones del segundo.""")) as tracker:
            self.play(Indicate(b2_tex),
                      Indicate(suma1_gr[2]),
                      #Wiggle(flechab2),
                      ReplacementTransform(b1_dot_copy, b_dot_copy),
                      run_time=tracker.duration)
        
        self.play(FadeOut(b_dot_copy))
        
        # SUMA b2 + b1
        a_dot_copy  = a_dot.copy()
        b2_dot_copy = b2_dot.copy()
        b_dot_copy  = b_dot.copy()        
        with self.voiceover(text=_("""Pero invertir el orden y seguir primero las indicaciones del
        segundo vector""")) as tracker:
            self.play(#Wiggle(flechab2),
                      Indicate(b2_tex),
                      Indicate(suma1_gr[2]),
                      ReplacementTransform(a_dot_copy, b2_dot_copy),
                      run_time=tracker.duration)
        
        flechab = b.arrow(axes)
        with self.voiceover(text=_("""y después las indicaciones del primero, nos conduce al mismo
        vector suma.""")) as tracker:
            self.play(Indicate(b1_tex),
                      Indicate(suma1_gr[0]),
                      ReplacementTransform(b2_dot_copy, b_dot_copy),
                      run_time=tracker.duration/2)
            self.play(GrowArrow(flechab),
                      FadeOut(b_dot_copy),
                      FadeOut(flechab1, b1_tex),
                      FadeOut(flechab2, b2_tex),
                      run_time=tracker.duration/2)
            
        self.pausa
        self.play(FadeOut(flechab), FadeIn(b_dot))
        self.pausa_media

        # arriba añadir (3,2)+(-2,1) = (1,3)
        c     = VectorR2([-2,1], color=PURPLE_A)
        c_dot = c.dot(axes, radio=0.12)
        c_tex = c.tex
        c_v_line = c.v_line(axes)
        c_h_line = c.h_line(axes)
        vgr_c = VGroup(c.tex).next_to(c.dot(axes, radio=0.12), LEFT)

        d     = VectorR2([1,3], color=YELLOW_A)
        d_dot = d.dot(axes, radio=0.12)
        d_tex = d.tex
        d_v_line = d.v_line(axes)
        d_h_line = d.h_line(axes)
        vgr_d = VGroup(d.tex).next_to(d.dot(axes, radio=0.12), UP)

        suma2_gr = VGroup(b.tex.copy(),
                          MathTex(r"+"),
                          c.tex.copy(),
                          MathTex(r"="),
                          d.tex.copy(),
                          ).arrange(RIGHT).to_corner(UL)
        
        with self.voiceover(text=_("""Veamos otro ejemplo.""")) as tracker:
            self.play(FadeOut(suma1_gr),
                      run_time=tracker.duration )
            self.pausa_corta

        with self.voiceover(text=_("""Sumemos el último vector con el
        vector -2 1.""")) as tracker:
            self.play(FadeIn(c_dot, c_tex, c_v_line, c_h_line))
            
        with self.voiceover(text=_("""La suma de ambos es el vector 1 3.""")) as tracker:
            self.add(suma2_gr)
            self.pausa
            self.play(FadeOut(b_h_line, b_v_line, c_h_line, c_v_line))
            self.add(d_dot, d.tex, d_v_line, d_h_line)
            self.pausa_larga                

        # Añadir flechas ejes (quitando puntos) y desplazar para mostrar suma
        flechab = b.arrow(axes)
        flechac = c.arrow(axes)
        flechad = d.arrow(axes)
        
        with self.voiceover(text=_("""Una vez más, señalemos los vectores con flechas.""")) as tracker:
            self.play(FadeOut(d_dot), #d_h_line, d_v_line),
                      GrowArrow(flechab),
                      FadeOut(b_dot),
                      GrowArrow(flechac),
                      FadeOut(c_dot))
            self.pausa_corta

        line_graph_b = axes.plot_line_graph(
            x_values = [-2, 1],
            y_values = [1, 3],
            line_color=TEAL_E,
            add_vertex_dots=False,
            stroke_width = 3,
        )

        line_graph_c = axes.plot_line_graph(
            x_values = [3, 1],
            y_values = [2, 3],
            line_color=PURPLE_E,
            add_vertex_dots=False,
            stroke_width = 3,
        )

        self.add(line_graph_b,line_graph_c)
        a_dot_copy  = a_dot.copy()
        b_dot_copy  = b_dot.copy()
        d_dot_copy  = d_dot.copy()

        a1_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                            fill_color=ORANGE).rotate(45*DEGREES).move_to(a_dot)
        a2_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                            fill_color=ORANGE).rotate(45*DEGREES).move_to(a_dot)
        a1_diamond_copy = a1_diamond.copy()
        a2_diamond_copy = a2_diamond.copy()
        b1_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                            fill_color=ORANGE).rotate(45*DEGREES).move_to(b1_dot)
        b2_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                            fill_color=ORANGE).rotate(45*DEGREES).move_to(b2_dot)
        c1_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                            fill_color=ORANGE).rotate(45*DEGREES).move_to(Dot(axes.c2p(-2,0)))
        c2_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                            fill_color=ORANGE).rotate(45*DEGREES).move_to(Dot(axes.c2p(0,1)))
        d1_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                            fill_color=ORANGE).rotate(45*DEGREES).move_to(Dot(axes.c2p(1,0)))
        d2_diamond = Square(color=BLUE, fill_opacity=1, side_length=.12,
                            fill_color=ORANGE).rotate(45*DEGREES).move_to(Dot(axes.c2p(0,3)))

        
        with self.voiceover(text=_("""De nuevo, sumar el primer vector con el segundo corresponde
        a seguir las indicaciones del primer vector""")) as tracker:
            self.play(Indicate(suma2_gr[0]),
                      ReplacementTransform(a_dot_copy, b_dot_copy),
                      ReplacementTransform(a1_diamond, b1_diamond),
                      ReplacementTransform(a2_diamond, b2_diamond),
                      GrowArrow(flechab1),
                      GrowArrow(flechab2),
                      run_time=3)
            self.play(FadeOut(flechab1,
                              flechab2))

        c1 = VectorR2([-2,0])
        c2 = VectorR2([0,1])
        flechac1 = c1.arrow(axes)
        flechac2 = c2.arrow(axes)
        flechac1d = flechac1.copy().move_to(axes.c2p(2,2,0))
        flechac2d = flechac2.copy().move_to(axes.c2p(3,2.5,0))

        with self.voiceover(text=_("""y luego seguir las indicaciones del segundo.""")) as tracker:
            self.play(Indicate(suma2_gr[2]),
                      ReplacementTransform(b_dot_copy, d_dot_copy),
                      ReplacementTransform(b1_diamond, d1_diamond),
                      ReplacementTransform(b2_diamond, d2_diamond),
                      GrowArrow(flechac1d),
                      GrowArrow(flechac2d),
                      run_time=3)
            self.play(FadeOut(d_dot_copy,
                              d1_diamond,
                              d2_diamond,
                              flechac1d,
                              flechac2d))

        a_dot_copy  = a_dot.copy()
        c_dot_copy  = c_dot.copy()
        d_dot_copy  = d_dot.copy()
        flechab1d = flechab1.copy().move_to(axes.c2p(-0.5,1,0))
        flechab2d = flechab2.copy().move_to(axes.c2p(- 2,2,0))
        with self.voiceover(text=_("""Pero invertir el orden y seguir primero las indicaciones
        del segundo vector""")) as tracker:
            self.play(Indicate(suma2_gr[2]),
                      ReplacementTransform(a_dot_copy, c_dot_copy),
                      ReplacementTransform(a1_diamond_copy, c1_diamond),
                      ReplacementTransform(a2_diamond_copy, c2_diamond),
                      GrowArrow(flechac1),
                      GrowArrow(flechac2),
                      run_time=3)
            self.play(FadeOut(flechac1,
                              flechac2))
            
        with self.voiceover(text=_("""y después las indicaciones del primero, nos conduce al mismo punto.
        """)) as tracker:
            self.play(Indicate(suma2_gr[0]),
                      ReplacementTransform(c_dot_copy, d_dot_copy),
                      ReplacementTransform(c1_diamond, d1_diamond),
                      ReplacementTransform(c2_diamond, d2_diamond),
                      GrowArrow(flechab1d),
                      GrowArrow(flechab2d),
                      run_time=2*tracker.duration/3)
            self.play(FadeOut(d_dot_copy),                     
                      FadeOut(d1_diamond),
                      FadeOut(d2_diamond),
                      FadeOut(d_v_line),
                      FadeOut(d_h_line),
                      FadeOut(flechab1d,
                              flechab2d))
            self.play(GrowArrow(flechad),
                      run_time=tracker.duration/3)
            self.pausa_larga                

        
        with self.voiceover(text=_("""Esta descripción geométrica de la suma, donde los sumandos
        forman un vértice de un paralelogramo, y su suma es la diagonal que parte de dicho vértice
        se denomina regla del paralelogramo.""")) as tracker:
            self.play(Indicate(flechab),
                      Indicate(flechac),
                      run_time=tracker.duration/2 )
            self.play(Indicate(flechad),
                      run_time=tracker.duration/2 )

        with self.voiceover(text=_("""A pesar de la utilidad de las flechas, recuerde que un vector
        es una lista de números, y que podemos hacer corresponder dichos números con las coordenadas
        de un punto en el espacio. Por ello, la representación geométrica del vector es el punto.
        La flecha tan solo lo señala.""")) as tracker:
            self.play(Indicate(b_tex),
                      Indicate(c_tex),
                      Indicate(d_tex),
                      run_time=tracker.duration/2 )
            self.play(FadeOut(flechab,
                              flechac,
                              flechad,
                              line_graph_b,
                              line_graph_c),
                      FadeIn(b_dot, c_dot, d_dot),
                      run_time=tracker.duration/2 ) 

        b_dot_copia=Dot(axes.c2p(*b.coords), radius=0.01)
        c_dot_copia=Dot(axes.c2p(*c.coords), radius=0.01)
        d_dot_copia=Dot(axes.c2p(*d.coords), radius=0.01)
        with self.voiceover(text=_("""Una de las dificultades para representar los puntos es que su
        dimensión es cero.""")) as tracker:
            self.play(
                Transform(b_dot, b_dot_copia),
                Transform(c_dot, c_dot_copia),
                Transform(d_dot, d_dot_copia),
                run_time = 6*tracker.duration/5 )
            
        with self.voiceover(text=_("""Una solución es indicar para cada punto su coordenada en el eje
        horizontal (es decir, el primer número de la lista).""")) as tracker:
            self.play(FadeIn(b_v_line),
                      FadeIn(c_v_line),
                      FadeIn(d_v_line),
                      run_time = tracker.duration/2)
            self.play(Circumscribe(b_tex[0][1]),
                      Circumscribe(c_tex[0][1:3]),
                      Circumscribe(d_tex[0][1]),
                      run_time = tracker.duration/2)
            
        with self.voiceover(text=_("""y su coordenada en el eje vertical (es decir, el segundo número
        de la lista).""")) as tracker:
            self.play(FadeIn(b_h_line),
                      FadeIn(c_h_line),
                      FadeIn(d_h_line),
                      run_time = tracker.duration/2)
            self.play(Circumscribe(b_tex[0][2]),
                      Circumscribe(c_tex[0][3]),
                      Circumscribe(d_tex[0][2]),
                      run_time = tracker.duration/2)
            
        with self.voiceover(text=_("""Sin embargo, la representación más frecuente son las flechas.
        Se ven bien y arrojan una interpretación intuitiva de la suma de
        vectores.""")) as tracker:
            self.play(FadeIn(flechab,flechac,flechad),
                      FadeOut(b_h_line, b_v_line),
                      FadeOut(c_h_line, c_v_line),
                      FadeOut(d_h_line, d_v_line),
                      run_time = tracker.duration/2 )
            self.play(FadeIn(line_graph_b, line_graph_c),
                      run_time = tracker.duration/2 )
            
        with self.voiceover(text=_("""Pero no debe olvidar que nuestra definición de vector de Rn
        es que es una lista de números. Y que su representación geométrica hace corresponder dichos
        números con las coordenadas de puntos en el espacio. Por tanto, cuando veamos un vector 
        representado con una flecha, debemos recordar que el vector no es la flecha. El vector es
        el punto señalado por la flecha.""")) as tracker:
            self.play(FadeOut(line_graph_b, line_graph_c),
                      Indicate(b_tex),
                      Indicate(c_tex),
                      Indicate(d_tex),
                      run_time=tracker.duration/2 )
            self.play(FadeOut(flechab, flechac, flechad,),
                      FadeIn(b.dot(axes)),
                      FadeIn(c.dot(axes)),
                      FadeIn(d.dot(axes)),
                      run_time=tracker.duration/2)

            self.pausa_larga()

class L01_V03_E02_SumaEnR3(MiEscenaConVoz):
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))        
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)
        
        titulo = Tex(_("Interpretación de la suma en ") + r"$\R[3]$",
                       tex_template = myTemplate,
                       font_size=60).set_color(BLUE).to_edge(UP)

        video1 = VideoMobject(
            filename=r"./media/videos/L01_V03_SumaDeVectores-II/1080p60/aux_movie_files/L01_V03_E02_SumaEnR3_3D.mp4",
            #filename=r"./media/videos/L01_V03_SumaDeVectores-II/1080p60/L01_V03_E02_SumaEnR3_3D.mp4",
            #filename=r"./media/videos/L01_V03_SumaDeVectores-II/480p15/L01_V03_E02_SumaEnR3_3D.mp4",
            speed=1.0
        ).scale_to_fit_width(6.5).next_to(titulo, DOWN, buff=0)
        #v1 = Group(video1, SurroundingRectangle(video1))

        a    = nc.Vector(sp.symbols('a:4')[1:])
        b    = nc.Vector(sp.symbols('b:4')[1:])
        s1 = MathTex(a.latex(),        tex_template = myTemplate,)
        mas= MathTex(r"+",             tex_template = myTemplate,)
        s3 = MathTex(b.latex(),        tex_template = myTemplate,)
        igual = MathTex(r"=",          tex_template = myTemplate,)
        s5 = MathTex((a+b).latex(),    tex_template = myTemplate,)
        grp1 = VGroup(s1,
                      mas,
                      s3,
                      igual,
                      s5,
                      igual.copy(),
                      s3.copy(),
                      mas.copy(),
                      s1.copy()).arrange(RIGHT).next_to(video1, DOWN).scale(.9)
       
        self.creditos(17)
      
        with self.voiceover(text=_("""La representación geométrica en R3 es similar. """)) as tracker:
            self.add(titulo)
            self.add(video1)
            self.play(FadeIn(grp1[0]))

        with self.voiceover(text=_("""El convenio es interpretar las dos primeras componentes como
        coordenadas respecto a un plano horizontal""")) as tracker:
            self.play(Indicate(grp1[0][0][2:6], scale_factor=2),
                      run_time=tracker.duration)

        with self.voiceover(text=_("""y la tercera como la coordenada respecto a un eje perpendicular 
        al plano.""")) as tracker:
            self.play(Indicate(grp1[0][0][6:8], scale_factor=2),
                      run_time=tracker.duration)
            
        with self.voiceover(text=_("""De nuevo, como la suma se realiza componente a componente y
        es conmutativa""")) as tracker:
            self.play(FadeIn(grp1[1:5]),
                      run_time=tracker.duration/2)
            self.play(FadeIn(grp1[5:]),
                      run_time=tracker.duration/2)
            
        with self.voiceover(text=_("""su representación geométrica en R3 también verifica la regla
        del paralelogramo.""")) as tracker:
            self.pausa(tracker.duration+2)

            self.pausa_media()

class L01_V03_E02_SumaEnR3_3D(ThreeDScene):
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
            
    
    def construct(self):
        axes = ThreeDAxes()
        x_label = axes.get_x_axis_label(Tex("1ª comp."))
        y_label = axes.get_y_axis_label(Tex("2ª comp.")).shift(UP * 2.4).shift(LEFT * 0.6)
       
        self.creditos(17)       
        # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.5)
        
        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label))
        self.wait(1)

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=60 * DEGREES, zoom=1, run_time=1.5)

        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(2)

        b     = VectorR3([3,2,3], color=TEAL_A)
        c     = VectorR3([-2,1,1], color=PURPLE_A)
        d     = VectorR3([1,3,4], color=YELLOW_A)

        b_dot = b.dot(axes)
        c_dot = c.dot(axes)
        d_dot = d.dot(axes)
        
        line_x = Line3D(start=np.array(axes.c2p(3,0,0,)), end=np.array(axes.c2p(3,2,0)), thickness=0.01)
        line_y = Line3D(start=np.array(axes.c2p(0,2,0,)), end=np.array(axes.c2p(3,2,0)), thickness=0.01)
        line_z = Line3D(start=np.array(axes.c2p(3,2,0,)), end=np.array(axes.c2p(3,2,3)), thickness=0.01)
        
        flechab = b.arrow(axes)        
        flechac = c.arrow(axes)
        flechad = d.arrow(axes)
        
        linebd = Line3D(start=np.array(axes.c2p(*b.coords)), end=np.array(axes.c2p(*d.coords)), thickness=0.01)
        linecd = Line3D(start=np.array(axes.c2p(*c.coords)), end=np.array(axes.c2p(*d.coords)), thickness=0.01)

        self.play(FadeIn(line_x))
        self.play(FadeIn(line_y))
        self.wait(4)
        
        self.play(FadeIn(line_z))
        self.add(b_dot)       
        self.wait(1.5)

        self.play(FadeIn(flechab),
                  FadeOut(b_dot),)
        self.wait(1.5)

        self.play(FadeIn(flechac))
        self.play(FadeOut(line_x, line_y, line_z))
        self.wait(1.5)

        self.play(FadeIn(linebd),
                  FadeIn(linecd),)
        self.wait(1.5)
        
        self.play(FadeIn(flechad))
        self.wait(4)

class L01_V03_E03_SumaEnRn(MiEscenaConVoz):
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))        
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)
        
        titulo = Tex(_("Interpretación de la suma en ") + r"$\R[n]$",
                     tex_template = myTemplate,
                     font_size=70).set_color(BLUE).to_edge(UP)

        video1 = VideoMobject(
            filename=r"./media/videos/L01_V03_SumaDeVectores-II/1080p60/aux_movie_files/L01_V03_E03_SumaEnRn_3D.mp4",
            #filename=r"./media/videos/L01_V03_SumaDeVectores-II/1080p60/L01_V03_E03_SumaEnRn_3D.mp4",
            #filename=r"./media/videos/L01_V03_SumaDeVectores-II/480p15/L01_V03_E03_SumaEnRn_3D.mp4",
            speed=1.0
        ).scale_to_fit_width(6.5).next_to(titulo, DOWN, buff=0)
        #v1 = Group(video1, SurroundingRectangle(video1))

        a    = nc.Vector(sp.symbols('a:6')[1:])
        b    = nc.Vector(sp.symbols('b:6')[1:])
        s1 = MathTex(a.latex(),        tex_template = myTemplate,)
        mas= MathTex(r"+",             tex_template = myTemplate,)
        s3 = MathTex(b.latex(),        tex_template = myTemplate,)
        igual = MathTex(r"=",          tex_template = myTemplate,)
        s5 = MathTex((a+b).latex(),    tex_template = myTemplate,)
        grp1 = VGroup(s1,
                      mas,
                      s3,
                      igual,
                      s5,
                      igual.copy(),
                      s3.copy(),
                      mas.copy(),
                      s1.copy()).arrange(RIGHT).next_to(video1, DOWN).scale(.8).shift(UP*0.7)
        
        self.creditos(3)

        with self.voiceover(text=_("""Los vectores en Rn son puntos en un espacio ene-dimensional. Para
        representarlos sería necesario dibujar tantos ejes de coordenadas como elementos tiene el vector.
        Esto no es posible cuando el número de componentes es mayor a tres. No obstante, sí que podemos
        recurrir a una interpretación geométrica."""))  as tracker:
            self.add(titulo)
            self.add(video1)          
            self.play(FadeIn(grp1[0]),
                      FadeIn(grp1[2]),
                      run_time=tracker.duration)

        with self.voiceover(text=_("""Dicha interpretación no describe literalmente las componentes de
        cada vector. Es tan  solo un ESQUEMA geométrico. En dicho esquema, los vectores son puntos de
        un espacio ene-dimensional.""")) as tracker:
            self.pausa(tracker.duration)

        with self.voiceover(text=_("""Como en los casos anteriores, se suman componente a componente,
        es decir, se suman las coordenadas respecto a cada eje de manera separada,""")) as tracker:
            self.play(FadeIn(grp1[1]),
                      FadeIn(grp1[3:5]),
                      run_time=tracker.duration/2)

        with self.voiceover(text=_("""y su suma es conmutativa.""")) as tracker:
            self.play(FadeIn(grp1[5:]),
                      run_time=tracker.duration)
            
        with self.voiceover(text=_("""Consecuentemente, como esquema geométrico, la regla del
        paralelogramo es válida incluso en espacios de dimension arbitraria. Lo es incluso en
        dimensión infinita.""")) as tracker:
            self.pausa(tracker.duration)
            
            self.pausa_larga()

class L01_V03_E03_SumaEnRn_3D(ThreeDScene):
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
                
    def construct(self):
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)
        
        axes = ThreeDAxes()

        b     = VectorR3([2,2,3], color=PURE_RED)
        c     = VectorR3([-3,1,-1], color=PURE_GREEN)
        d     = VectorR3([-1,3,2], color=PURE_BLUE)
        
        b_dot = b.dot(axes)
        c_dot = c.dot(axes)
        d_dot = d.dot(axes)
        
        flechab = b.arrow(axes)        
        flechac = c.arrow(axes)
        flechad = d.arrow(axes)

        linebd = Line3D(start=np.array(axes.c2p(*b.coords)), end=np.array(axes.c2p(*d.coords)))
        linecd = Line3D(start=np.array(axes.c2p(*c.coords)), end=np.array(axes.c2p(*d.coords)))

        #self.add(axes, plane)

        self.move_camera(phi=75 * DEGREES, theta=60 * DEGREES, zoom=1, run_time=1)
        self.add(b_dot, c_dot)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(23)

        self.play(FadeIn(flechab, flechac),
                  FadeOut(b_dot, c_dot))
        
        self.wait(7)
        self.play(FadeIn(flechad))
        
        self.wait(8)
        self.add(linebd, linecd)

        self.wait(2)
        
        self.begin_ambient_camera_rotation(rate=0.6, about='gamma')
        self.wait(5)

        self.begin_ambient_camera_rotation(rate=0.6, about='theta')
        self.play(FadeIn(b_dot,
                         c_dot,
                         d_dot),
                  FadeOut(flechab,
                          flechac,
                          flechad,
                          linebd,
                          linecd))
        self.wait(5)

class L01_V03_E04_Resumen(MiEscenaConVoz):
    def construct(self):
        self.set_speech_service( AzureService(voice="es-ES-AlvaroNeural" ) )       
        #self.set_speech_service(GTTSService(lang="es", tld="com"))        
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"""\usepackage{nacal} """)
        
        self.creditos()
        
        titulo = Title(_("Suma de vectores de ") + r"$\R[n]$",
                     tex_template = myTemplate,
                     font_size=70).set_color(BLUE)
        self.add(titulo)
        self.pausa()

        # Resumen
        resumen = Tex(_(r"\textbf{Lo más importante:}"),
                 tex_template = myTemplate,
                 font_size=50).set_color(ORANGE).next_to(titulo, DOWN, aligned_edge=LEFT)


        with self.voiceover(text=_("""Por último, quiero subrayar que la interpretación geométrica se
        deriva de la definición de la suma.""")) as tracker:
            self.add(resumen)
            self.pausa(tracker.duration)

        cvab  = MathTex(r"\elemRp{\Vect{a}+\Vect{b}}{i}", tex_template = myTemplate)
        cva   = MathTex(r"\eleVR{a}{i}", tex_template = myTemplate)
        cvb   = MathTex(r"\eleVR{b}{i}", tex_template = myTemplate)
        igual = MathTex(r"=",            tex_template = myTemplate)
        mas   = MathTex(r"+",            tex_template = myTemplate)
        eq_suma = VGroup(cvab,igual,cva,mas,cvb).arrange(RIGHT).scale(1.5)
        cva_copy   = cva.copy().move_to(cvb)
        cvb_copy   = cvb.copy().move_to(cva)

        item1 = MathTex(r"\Vect{a}+\Vect{x} = \Vect{x}+\Vect{a}",
                        tex_template = myTemplate).next_to(eq_suma,
                                                           DOWN,
                                                           buff=1.5).scale(1.5)
        
        props_suma = VGroup(eq_suma, item1)

        with self.voiceover(text=_("""Por tanto, lo fundamental no es la interpretación geométrica; lo
        fundamental es que la suma es una operación componente a componente.""")) as tracker:
            self.play(FadeIn(props_suma[0]),
                      run_time=tracker.duration+0.3)

        with self.voiceover(text=_("""Ello se traduce en la siguiente regla de cálculo
        simbólico:""")) as tracker:
            self.pausa(tracker.duration)
            self.pausa_muy_corta()

        with self.voiceover(text=_("""El operador selector es distributivo respecto de la
        suma.""")) as tracker:
            self.play(Indicate(eq_suma[0][0][0]),
                      Indicate(eq_suma[0][0][-3:]),
                      Indicate(eq_suma[2][0][-2:]),
                      Indicate(eq_suma[4][0][-2:]),
                      run_time = tracker.duration)
            self.pausa_muy_corta()
            
        with self.voiceover(text=_("""Además, como las componentes son números reales, la suma es
        conmutativa""")) as tracker:
            self.play(Transform(cva,cva_copy),
                      Transform(cvb,cvb_copy),
                      run_time = 3*tracker.duration/4)
            self.play(Indicate(item1),
                      run_time = 3*tracker.duration/10)
            
        self.pausa_larga()
