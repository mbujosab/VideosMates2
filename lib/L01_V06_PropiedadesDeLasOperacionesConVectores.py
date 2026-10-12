import os
import re
from manim import *
from contextlib import contextmanager
from manim_voiceover import VoiceoverScene
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.azure import AzureService
from manim_voiceover.services.gtts import GTTSService
import nacal as nc
import sympy as sp

LANG = "es"

def tr(es, en):
    """Cadena en el idioma del vídeo."""
    return es if LANG == "es" else en

VOCES_AZURE  = {"es": "es-ES-AlvaroNeural", "en": "en-GB-RyanNeural"}
SERVICIO_VOZ = os.environ.get("VOZ", "azure")

COLOR_A         = BLUE      # primer objeto (número a, vector a)
COLOR_B         = ORANGE    # segundo objeto (contrasta con el azul)
COLOR_C         = GREEN     # tercer objeto
COLOR_ESCALAR   = YELLOW    # escalares, preguntas al espectador, tarjeta de pausa
COLOR_RESULTADO = WHITE     # resultado de una operación
COLOR_REGLA     = TEAL      # pasos que usan una propiedad de los números reales
COLOR_TITULO    = BLUE      # títulos y cabeceras

TITULO = tr("Propiedades de las operaciones con vectores de  ", "Properties of the operations with vectors in  ") + r"\R[n]"

myTemplate = TexTemplate()
myTemplate.add_to_preamble(r"""\usepackage{nacal} """)

class MiEscenaConVoz(VoiceoverScene):
    def setup(self):
        """Manim lo ejecuta antes de construct(): fija la voz del idioma."""
        self.voz()

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

    @contextmanager
    def voiceover(self, text=None, **kwargs):
        """Como VoiceoverScene.voiceover, con tres añadidos: los dos puntos producen
        una pausa en la voz (Azure no la hace por sí sola); el subtítulo conserva el
        texto original (sin las marcas <bookmark mark='x'/>); y con gTTS, que no da
        los tiempos de cada palabra, las marcas se estiman repartiendo la duración
        proporcionalmente al texto, de modo que self.wait_until_bookmark("x")
        funciona con los dos servicios (con Azure, con precisión)."""
        if text is not None:
            # el subtítulo no lleva ni marcas ni pausas SSML escritas a mano (<break time="200ms"/>)
            kwargs.setdefault("subcaption", re.sub(r"\s*<break[^>]*/>\s*", " ", remove_bookmarks(text)))
            if SERVICIO_VOZ == "gtts":
                text = re.sub(r"\s*<break[^>]*/>\s*", ", ", text).replace(":", ".")
            else:
                text = text.replace(": ", ': <break time="500ms"/> ')
        with super().voiceover(text=text, **kwargs) as tracker:
            if text is not None and "<bookmark" in text and not getattr(tracker, "bookmark_times", None):
                # gTTS guarda en la caché el texto sin marcas: se reponen y se estiman los tiempos
                tracker.data["input_text"] = text
                tracker.data["word_boundaries"] = tracker._get_fallback_word_boundaries()
                tracker._process_bookmarks()
            yield tracker

    def anuncia_regla(self, nueva, anterior=None, run_time=1):
        """Muestra, atenuada, la fórmula que se va a ilustrar (en lugar de la anterior, si la hay).
        Queda a la vista durante la construcción; al terminar, destaca_regla() la enciende."""
        nueva.set_opacity(0.45)
        if anterior is None:
            self.play(FadeIn(nueva), run_time=run_time)
        else:
            self.play(ReplacementTransform(anterior, nueva), run_time=run_time)
        return nueva

    def destaca_regla(self, regla, run_time=1.5):
        """La ilustración ha terminado: la fórmula pasa a opacidad plena y parpadea."""
        self.play(regla.animate.set_opacity(1), run_time=run_time/3)
        self.play(Indicate(regla, color=COLOR_RESULTADO, scale_factor=1.15), run_time=2*run_time/3)

    def voz(self, servicio=SERVICIO_VOZ):
        """Fija el servicio de voz según el idioma del vídeo."""
        if servicio == "gtts":
            self.set_speech_service(GTTSService(lang=LANG, tld="com"))
        else:
            self.set_speech_service(AzureService(voice=VOCES_AZURE[LANG]))

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
    
        copyright = Tex(r"\textcopyright{\;} 2026\; Marcos Bujosa  ")
    
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

    def pausa_para_pensar(self, pista=None, pista_voz=None, segundos=4):
        """Tarjeta que invita a pausar el vídeo; opcionalmente da una pista y vuelve a invitar."""
        def tarjeta(texto):
            barra = lambda: RoundedRectangle(corner_radius=0.06, width=0.2, height=0.6,
                                             fill_color=COLOR_ESCALAR, fill_opacity=1, stroke_width=0)
            icono = VGroup(barra(), barra()).arrange(RIGHT, buff=0.12)
            rotulo = Tex(texto, tex_template=myTemplate, font_size=38)
            rotulo.scale_to_fit_width(min(rotulo.width, config.frame_width*0.75))
            contenido = VGroup(icono, rotulo).arrange(RIGHT, buff=0.4)
            marco = RoundedRectangle(corner_radius=0.25, width=contenido.width+0.8, height=contenido.height+0.6,
                                     stroke_color=COLOR_ESCALAR, fill_color=BLACK, fill_opacity=0.85)
            return VGroup(marco, contenido).to_edge(DOWN, buff=0.4)
    
        invitacion = tr("Pause el vídeo e inténtelo.", "Pause the video and give it a try.")
        tarjeta1 = tarjeta(invitacion)
        with self.voiceover(text=invitacion) as tracker:
            self.play(FadeIn(tarjeta1), run_time=min(0.8, tracker.duration))
        self.wait(segundos)
        if pista is not None:
            tarjeta2 = tarjeta(tr("Pista: ", "Hint: ") + pista)
            with self.voiceover(text=tr("Una pista: ", "A hint: ") + (pista_voz or pista)) as tracker:
                self.play(ReplacementTransform(tarjeta1, tarjeta2), run_time=min(0.8, tracker.duration))
            tarjeta3 = tarjeta(tr("Pause de nuevo e inténtelo.", "Pause again and try once more."))
            with self.voiceover(text=tr("Pause de nuevo e inténtelo.", "Pause again and try once more.")) as tracker:
                self.play(ReplacementTransform(tarjeta2, tarjeta3), run_time=min(0.8, tracker.duration))
            self.wait(segundos)
            tarjeta1 = tarjeta3
        self.play(FadeOut(tarjeta1), run_time=0.6)

class L01_V06_PropiedadesDeLasOperacionesConVectores(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        
        # Portada
        titulo = Title(TITULO, tex_template=myTemplate, font_size=50).set_color(COLOR_TITULO)
        self.play(Write(titulo))
        self.pausa_media()
        
        igual = MathTex(r"=", tex_template=myTemplate)
        mas   = MathTex(r"+", tex_template=myTemplate)
        
        # suma
        cvab = MathTex(r"\elemRp{\Vect{a}+\Vect{b}}{i}", tex_template=myTemplate)
        cva  = MathTex(r"\eleVR{a}{i}",                  tex_template=myTemplate)
        cvb  = MathTex(r"\eleVR{b}{i}",                  tex_template=myTemplate)
        
        eq_suma = VGroup(cvab.copy(),
                         igual.copy(),
                         cva.copy(),
                         mas.copy(),
                         cvb.copy()).arrange(RIGHT).scale(1.5)
        
        # producto
        cvla = MathTex(r"\elemRp{\lambda\Vect{a}}{i}", tex_template=myTemplate)
        lca  = MathTex(r"\lambda\eleVRpE{a}{i}",       tex_template=myTemplate)
        
        eq_producto = VGroup(cvla.copy(),
                             igual.copy(),
                             lca.copy()).arrange(RIGHT).scale(1.5).next_to(eq_suma,
                                                                           DOWN,
                                                                           aligned_edge=LEFT,
                                                                           buff=1.2)
        
        with self.voiceover(text=tr("""En los vídeos anteriores hemos visto dos operaciones con vectores de Rn:""",
                                    """In the previous videos we saw two operations with vectors in R n:""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        with self.voiceover(text=tr("""La suma,""",
                                    """The sum,""")) as tracker:
            self.play(FadeIn(eq_suma[0][0][1:4],
                             rate_func=rate_functions.exponential_decay),
                      run_time=2*tracker.duration/3)
        
        with self.voiceover(text=tr("""y el reescalado""",
                                    """and scaling.""")) as tracker:
            self.play(FadeIn(eq_producto[0][0][1:3],
                             rate_func=rate_functions.exponential_decay),
                      run_time=2*tracker.duration/3)
        
        with self.voiceover(text=tr("""Ambas operaciones se definen componente a componente.""",
                                    """Both operations are defined component-wise.""")) as tracker:
            self.play(FadeIn(eq_suma[0][0][0],      # paréntesis inicial
                             eq_suma[0][0][4:],     # cierre de paréntesis y selector
                             eq_producto[0][0][0],  # paréntesis inicial
                             eq_producto[0][0][3:], # cierre de paréntesis y selector
                             scale=.5,
                             rate_func=rate_functions.exponential_decay),
                      run_time=tracker.duration)
        
        with self.voiceover(text=tr("""Las componentes del 'vector suma' son la suma de las componentes,""",
                                    """The components of the 'sum vector' are the sums of the components,""")) as tracker:
            self.play(FadeIn(eq_suma[1:],           # resto de la ecuación
                             scale=.1,
                             rate_func=rate_functions.exponential_decay),
                      run_time=3*tracker.duration/5)
            self.play(Indicate(eq_suma[2][0]),
                      Indicate(eq_suma[4][0]))
        
        with self.voiceover(text=tr("""y las componentes del 'vector reescalado' son las componentes reescaladas.""",
                                    """and the components of the 'scaled vector' are the scaled components.""")) as tracker:
            self.play(FadeIn(eq_producto[1:],       # resto de la ecuación
                             scale=.1,
                             rate_func=rate_functions.exponential_decay),
                      run_time=3*tracker.duration/5)
            self.play(Indicate(eq_producto[2][0][0]),
                      Indicate(eq_producto[2][0][2:5]))
        
        with self.voiceover(text=tr("""Aunque vimos la interpretación geométrica, en R2 y en R3, de ambas operaciones, señalamos que lo importante no es la interpretación geométrica. Lo más importante es que son operaciones definidas componente a componente que se traducen en reglas simples de manipulación simbólica. En este caso se traducen en operaciones entre números reales; sumas de números en el primer caso y productos en el segundo.""",
                                    """Although we saw the geometric interpretation of both operations in R2 and R3, we pointed out that the geometric interpretation is not what matters most. What matters most is that these operations are defined component-wise, and that translates into simple rules of symbolic manipulation. In this case, they translate into operations between real numbers: sums of numbers in the first case, and products in the second.""")) as tracker:
            self.pausa_corta(tracker.duration)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        
        subtitulo = Title(tr("Recordatorio: propiedades de los números reales",
                             "Reminder: properties of the real numbers"),
                          tex_template=myTemplate,
                          font_size=44).set_color(BLUE)
        self.play(Write(subtitulo))
        
        sean = Tex(tr(r"Sean $a$, $b$ y $c$ números reales. Entonces:",
                      r"Let $a$, $b$ and $c$ be real numbers. Then:"),
                   tex_template=myTemplate,
                   font_size=40).next_to(subtitulo, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        
        propiedades = [r"a+b=b+a",
                       r"a+(b+c)=(a+b)+c",
                       r"a+0=a",
                       r"a+(-a)=0",
                       r"ab=ba",
                       r"a(b+c)=ab+ac",
                       r"a(bc)=(ab)c",
                       r"1a=a"]
        
        lista = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=44)
                         for k, p in enumerate(propiedades)])
        
        columna_suma     = VGroup(*lista[:4]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        columna_producto = VGroup(*lista[4:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        cuadro = VGroup(columna_suma, columna_producto).arrange(RIGHT, buff=1.8, aligned_edge=UP)
        cuadro.next_to(sean, DOWN, buff=0.6).set_x(0)
        for k in range(4):   # alinea cada fila de la segunda columna con la primera
            lista[4+k].set_y(lista[k].get_y())
        
        with self.voiceover(text=tr("""Para estudiar las propiedades de las operaciones con vectores, recordemos primero algunas propiedades de los números reales que seguro conoce desde la escuela.""",
                                    """To study the properties of the operations with vectors, let us first recall some properties of the real numbers that you surely know from school.""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        with self.voiceover(text=tr("""Sean a, b y c tres números reales.""",
                                    """Let a, b and c be three real numbers.""")) as tracker:
            self.play(FadeIn(sean), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""La suma es conmutativa,""",
                                    """Addition is commutative,""")) as tracker:
            self.play(FadeIn(lista[0]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""y asociativa.""",
                                    """and associative.""")) as tracker:
            self.play(FadeIn(lista[1]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""El cero es el elemento neutro de la suma,""",
                                    """Zero is the identity element for addition,""")) as tracker:
            self.play(FadeIn(lista[2]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""y todo número tiene un opuesto: sumados dan cero.""",
                                    """and every number has an opposite: their sum is zero.""")) as tracker:
            self.play(FadeIn(lista[3]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""El producto es conmutativo,""",
                                    """Multiplication is commutative,""")) as tracker:
            self.play(FadeIn(lista[4]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""y distributivo respecto de la suma.""",
                                    """and distributive over addition.""")) as tracker:
            self.play(FadeIn(lista[5]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""También es asociativo,""",
                                    """It is also associative,""")) as tracker:
            self.play(FadeIn(lista[6]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""y el uno es el elemento neutro del producto.""",
                                    """and one is the identity element for multiplication.""")) as tracker:
            self.play(FadeIn(lista[7]), run_time=tracker.duration/2)
        
        pregunta = Tex(tr(r"¿Se verifican también estas propiedades al operar con \emph{vectores}?",
                          r"Do these properties also hold when operating with \emph{vectors}?"),
                       tex_template=myTemplate,
                       font_size=44).set_color(YELLOW).next_to(cuadro, DOWN, buff=0.8)
        
        with self.voiceover(text=tr("""Estas ocho propiedades son tan familiares que las usamos sin pensar. La cuestión que queremos abordar ahora es la siguiente:""",
                                    """These eight properties are so familiar that we use them without thinking. The question we want to address now is the following:""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        with self.voiceover(text=tr("""¿Se verifican también estas propiedades cuando operamos con vectores?""",
                                    """Do these properties also hold when we operate with vectors?""")) as tracker:
            self.play(Write(pregunta), run_time=tracker.duration)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        pass

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        pass

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        pass

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        pass

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        copyright = Tex(r"\textcopyright{\;} 2026 \; Marcos Bujosa")
        github = Tex(r"\texttt{https://github.com/mbujosab}").next_to(copyright, DOWN)
        CGG  = VGroup(copyright, github).scale(1.1)
        self.add(CGG)
        self.wait(10)


class L01_V06_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

class L01_V06_E01_Introduccion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        
        # Portada
        titulo = Title(TITULO, tex_template=myTemplate, font_size=50).set_color(COLOR_TITULO)
        self.play(Write(titulo))
        self.pausa_media()
        
        igual = MathTex(r"=", tex_template=myTemplate)
        mas   = MathTex(r"+", tex_template=myTemplate)
        
        # suma
        cvab = MathTex(r"\elemRp{\Vect{a}+\Vect{b}}{i}", tex_template=myTemplate)
        cva  = MathTex(r"\eleVR{a}{i}",                  tex_template=myTemplate)
        cvb  = MathTex(r"\eleVR{b}{i}",                  tex_template=myTemplate)
        
        eq_suma = VGroup(cvab.copy(),
                         igual.copy(),
                         cva.copy(),
                         mas.copy(),
                         cvb.copy()).arrange(RIGHT).scale(1.5)
        
        # producto
        cvla = MathTex(r"\elemRp{\lambda\Vect{a}}{i}", tex_template=myTemplate)
        lca  = MathTex(r"\lambda\eleVRpE{a}{i}",       tex_template=myTemplate)
        
        eq_producto = VGroup(cvla.copy(),
                             igual.copy(),
                             lca.copy()).arrange(RIGHT).scale(1.5).next_to(eq_suma,
                                                                           DOWN,
                                                                           aligned_edge=LEFT,
                                                                           buff=1.2)
        
        with self.voiceover(text=tr("""En los vídeos anteriores hemos visto dos operaciones con vectores de Rn:""",
                                    """In the previous videos we saw two operations with vectors in R n:""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        with self.voiceover(text=tr("""La suma,""",
                                    """The sum,""")) as tracker:
            self.play(FadeIn(eq_suma[0][0][1:4],
                             rate_func=rate_functions.exponential_decay),
                      run_time=2*tracker.duration/3)
        
        with self.voiceover(text=tr("""y el reescalado""",
                                    """and scaling.""")) as tracker:
            self.play(FadeIn(eq_producto[0][0][1:3],
                             rate_func=rate_functions.exponential_decay),
                      run_time=2*tracker.duration/3)
        
        with self.voiceover(text=tr("""Ambas operaciones se definen componente a componente.""",
                                    """Both operations are defined component-wise.""")) as tracker:
            self.play(FadeIn(eq_suma[0][0][0],      # paréntesis inicial
                             eq_suma[0][0][4:],     # cierre de paréntesis y selector
                             eq_producto[0][0][0],  # paréntesis inicial
                             eq_producto[0][0][3:], # cierre de paréntesis y selector
                             scale=.5,
                             rate_func=rate_functions.exponential_decay),
                      run_time=tracker.duration)
        
        with self.voiceover(text=tr("""Las componentes del 'vector suma' son la suma de las componentes,""",
                                    """The components of the 'sum vector' are the sums of the components,""")) as tracker:
            self.play(FadeIn(eq_suma[1:],           # resto de la ecuación
                             scale=.1,
                             rate_func=rate_functions.exponential_decay),
                      run_time=3*tracker.duration/5)
            self.play(Indicate(eq_suma[2][0]),
                      Indicate(eq_suma[4][0]))
        
        with self.voiceover(text=tr("""y las componentes del 'vector reescalado' son las componentes reescaladas.""",
                                    """and the components of the 'scaled vector' are the scaled components.""")) as tracker:
            self.play(FadeIn(eq_producto[1:],       # resto de la ecuación
                             scale=.1,
                             rate_func=rate_functions.exponential_decay),
                      run_time=3*tracker.duration/5)
            self.play(Indicate(eq_producto[2][0][0]),
                      Indicate(eq_producto[2][0][2:5]))
        
        with self.voiceover(text=tr("""Aunque vimos la interpretación geométrica, en R2 y en R3, de ambas operaciones, señalamos que lo importante no es la interpretación geométrica. Lo más importante es que son operaciones definidas componente a componente que se traducen en reglas simples de manipulación simbólica. En este caso se traducen en operaciones entre números reales; sumas de números en el primer caso y productos en el segundo.""",
                                    """Although we saw the geometric interpretation of both operations in R2 and R3, we pointed out that the geometric interpretation is not what matters most. What matters most is that these operations are defined component-wise, and that translates into simple rules of symbolic manipulation. In this case, they translate into operations between real numbers: sums of numbers in the first case, and products in the second.""")) as tracker:
            self.pausa_corta(tracker.duration)


class L01_V06_E02_PropiedadesDeLosReales(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        
        subtitulo = Title(tr("Recordatorio: propiedades de los números reales",
                             "Reminder: properties of the real numbers"),
                          tex_template=myTemplate,
                          font_size=44).set_color(BLUE)
        self.play(Write(subtitulo))
        
        sean = Tex(tr(r"Sean $a$, $b$ y $c$ números reales. Entonces:",
                      r"Let $a$, $b$ and $c$ be real numbers. Then:"),
                   tex_template=myTemplate,
                   font_size=40).next_to(subtitulo, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        
        propiedades = [r"a+b=b+a",
                       r"a+(b+c)=(a+b)+c",
                       r"a+0=a",
                       r"a+(-a)=0",
                       r"ab=ba",
                       r"a(b+c)=ab+ac",
                       r"a(bc)=(ab)c",
                       r"1a=a"]
        
        lista = VGroup(*[MathTex(f"{k+1}.\\;\\;", p, tex_template=myTemplate, font_size=44)
                         for k, p in enumerate(propiedades)])
        
        columna_suma     = VGroup(*lista[:4]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        columna_producto = VGroup(*lista[4:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        cuadro = VGroup(columna_suma, columna_producto).arrange(RIGHT, buff=1.8, aligned_edge=UP)
        cuadro.next_to(sean, DOWN, buff=0.6).set_x(0)
        for k in range(4):   # alinea cada fila de la segunda columna con la primera
            lista[4+k].set_y(lista[k].get_y())
        
        with self.voiceover(text=tr("""Para estudiar las propiedades de las operaciones con vectores, recordemos primero algunas propiedades de los números reales que seguro conoce desde la escuela.""",
                                    """To study the properties of the operations with vectors, let us first recall some properties of the real numbers that you surely know from school.""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        with self.voiceover(text=tr("""Sean a, b y c tres números reales.""",
                                    """Let a, b and c be three real numbers.""")) as tracker:
            self.play(FadeIn(sean), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""La suma es conmutativa,""",
                                    """Addition is commutative,""")) as tracker:
            self.play(FadeIn(lista[0]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""y asociativa.""",
                                    """and associative.""")) as tracker:
            self.play(FadeIn(lista[1]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""El cero es el elemento neutro de la suma,""",
                                    """Zero is the identity element for addition,""")) as tracker:
            self.play(FadeIn(lista[2]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""y todo número tiene un opuesto: sumados dan cero.""",
                                    """and every number has an opposite: their sum is zero.""")) as tracker:
            self.play(FadeIn(lista[3]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""El producto es conmutativo,""",
                                    """Multiplication is commutative,""")) as tracker:
            self.play(FadeIn(lista[4]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""y distributivo respecto de la suma.""",
                                    """and distributive over addition.""")) as tracker:
            self.play(FadeIn(lista[5]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""También es asociativo,""",
                                    """It is also associative,""")) as tracker:
            self.play(FadeIn(lista[6]), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""y el uno es el elemento neutro del producto.""",
                                    """and one is the identity element for multiplication.""")) as tracker:
            self.play(FadeIn(lista[7]), run_time=tracker.duration/2)
        
        pregunta = Tex(tr(r"¿Se verifican también estas propiedades al operar con \emph{vectores}?",
                          r"Do these properties also hold when operating with \emph{vectors}?"),
                       tex_template=myTemplate,
                       font_size=44).set_color(YELLOW).next_to(cuadro, DOWN, buff=0.8)
        
        with self.voiceover(text=tr("""Estas ocho propiedades son tan familiares que las usamos sin pensar. La cuestión que queremos abordar ahora es la siguiente:""",
                                    """These eight properties are so familiar that we use them without thinking. The question we want to address now is the following:""")) as tracker:
            self.pausa_corta(tracker.duration)
        
        with self.voiceover(text=tr("""¿Se verifican también estas propiedades cuando operamos con vectores?""",
                                    """Do these properties also hold when we operate with vectors?""")) as tracker:
            self.play(Write(pregunta), run_time=tracker.duration)
        
        self.pausa_media()


class L01_V06_E03_EjemploNumerico(MiEscenaConVoz):
    def construct(self):
        pass


class L01_V06_E04_Estrategia1(MiEscenaConVoz):
    def construct(self):
        pass


class L01_V06_E05_Estrategia2(MiEscenaConVoz):
    def construct(self):
        pass


class L01_V06_E06_Resumen(MiEscenaConVoz):
    def construct(self):
        pass


class ZCreditosFinales(Scene):
    def construct(self):
        copyright = Tex(r"\textcopyright{\;} 2026 \; Marcos Bujosa")
        github = Tex(r"\texttt{https://github.com/mbujosab}").next_to(copyright, DOWN)
        CGG  = VGroup(copyright, github).scale(1.1)
        self.add(CGG)
        self.wait(10)
