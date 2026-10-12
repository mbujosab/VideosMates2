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

VOCES_AZURE  = {"es": "es-ES-Tristan:DragonHDLatestNeural", "en": "en-GB-Ollie:DragonHDLatestNeural"}   # voces HD desde 2026-10-12
# Las voces "DragonHD" ya hacen una pausa larga en los dos puntos (medido: 0,7 s); a las demás se les añade un <break>
BREAK_DOS_PUNTOS = "" if "DragonHD" in VOCES_AZURE[LANG] else '<break time="500ms"/> '
SERVICIO_VOZ = os.environ.get("VOZ", "azure")

COLOR_A         = BLUE      # primer objeto (número a, vector a)
COLOR_B         = ORANGE    # segundo objeto (contrasta con el azul)
COLOR_C         = GREEN     # tercer objeto
COLOR_ESCALAR   = YELLOW    # escalares, preguntas al espectador, tarjeta de pausa
COLOR_RESULTADO = WHITE     # resultado de una operación
COLOR_REGLA     = TEAL      # pasos que usan una propiedad de los números reales
COLOR_TITULO    = BLUE      # títulos y cabeceras

TITULO = tr("Las propiedades de los números reales, con regla y compás",
            "The properties of the real numbers, with ruler and compass")

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
            # el subtítulo no lleva ni marcas, ni pausas SSML escritas a mano (<break time="600ms"/>),
            # ni las comillas simples que guían la entonación de Azure ('a', 'b más c'); los apóstrofos
            # ingleses (Euclid's) no se tocan porque van pegados a una letra
            subtitulo = re.sub(r"\s*<break[^>]*/>\s*", " ", remove_bookmarks(text))
            subtitulo = re.sub(r"(?<!\w)'([^']{1,15})'(?!\w)", r"\1", subtitulo)
            kwargs.setdefault("subcaption", subtitulo)
            if SERVICIO_VOZ == "gtts":
                text = re.sub(r"\s*<break[^>]*/>\s*", ", ", text).replace(":", ".")
            elif BREAK_DOS_PUNTOS:
                text = text.replace(": ", ": " + BREAK_DOS_PUNTOS)
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

class L01_V05_PropiedadesDeLosRealesConReglaYCompas(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=44).set_color(COLOR_TITULO)
        self.play(Write(titulo))
        
        # las dos definiciones (vídeos 3 y 4), con los glifos coloreados según el código de la serie
        f_suma = MathTex(r"\elemRp{\Vect{a}+\Vect{b}}{i}", "=", r"\eleVR{a}{i}+\eleVR{b}{i}",
                         tex_template=myTemplate, font_size=56).shift(0.9*UP)
        f_prod = MathTex(r"\elemRp{\lambda\Vect{a}}{i}", "=", r"\lambda\eleVRpE{a}{i}",
                         tex_template=myTemplate, font_size=56).shift(0.5*DOWN)
        for g in (f_suma[0][1], f_suma[2][0], f_prod[0][2], f_prod[2][2]):
            g.set_color(COLOR_A)
        for g in (f_suma[0][3], f_suma[2][4]):
            g.set_color(COLOR_B)
        for g in (f_prod[0][1], f_prod[2][0]):
            g.set_color(COLOR_ESCALAR)
        indices = [f_suma[0][6], f_suma[2][2], f_suma[2][6], f_prod[0][5], f_prod[2][4]]
        
        with self.voiceover(text=tr("""En los vídeos anteriores definimos dos operaciones con vectores: <bookmark mark='suma'/>la suma, <bookmark mark='producto'/>y el producto de un vector por un escalar. Las dos se calculan <bookmark mark='componentes'/>componente a componente, es decir, <bookmark mark='reales'/>sumando y multiplicando números reales.""",
                                    """In the previous videos we defined two operations with vectors: <bookmark mark='suma'/>the sum, <bookmark mark='producto'/>and the product of a vector by a scalar. Both are computed <bookmark mark='componentes'/>component-wise, that is, <bookmark mark='reales'/>by adding and multiplying real numbers.""")) as tracker:
            self.wait_until_bookmark("suma")
            self.play(FadeIn(f_suma), run_time=1)
            self.wait_until_bookmark("producto")
            self.play(FadeIn(f_prod), run_time=1)
            self.wait_until_bookmark("componentes")
            self.play(*[Indicate(g, color=COLOR_ESCALAR, scale_factor=1.8) for g in indices], run_time=1.5)
            self.wait_until_bookmark("reales")
            self.play(Circumscribe(f_suma[2], color=COLOR_ESCALAR, buff=0.15),
                      Circumscribe(f_prod[2], color=COLOR_ESCALAR, buff=0.15), run_time=2)
        
        with self.voiceover(text=tr("""El siguiente paso es estudiar las propiedades que tienen esas dos operaciones con vectores. Y para eso vamos a necesitar las propiedades algebraicas de los números reales. Seguro que las conoce desde la escuela.""",
                                    """The next step is to study the properties of those two operations with vectors. And for that we will need the algebraic properties of the real numbers. You surely know them from school.""")) as tracker:
            ocho = Tex(tr("Propiedades algebraicas de los números reales", "Algebraic properties of the real numbers"),
                       font_size=48).set_color(COLOR_REGLA)
            self.pausa(tracker.duration/3)
            self.play(FadeOut(f_suma, f_prod), FadeIn(ocho), run_time=tracker.duration/3)
        
        # recta con regla y compás
        recta = NumberLine(x_range=[-1, 7, 1], length=10, include_numbers=False).shift(1.2*DOWN)
        recta.add_numbers([0, 1], font_size=36)
        u = recta.n2p(1)[0] - recta.n2p(0)[0]
        pa = recta.n2p(2.6)
        punto_a = Dot(pa, color=COLOR_A, radius=0.1)
        etq_a = MathTex("a", color=COLOR_A, font_size=46).next_to(punto_a, UP, buff=0.25)
        arco = Arc(radius=2.6*u, start_angle=PI/2, angle=-PI/2, arc_center=recta.n2p(0),
                   color=GRAY_B, stroke_width=2)
        
        with self.voiceover(text=tr("""Pero ¿de dónde salen? En este vídeo vamos a verlas, no a demostrarlas. Y las veremos con regla y compás como hacían los geómetras griegos.""",
                                    """But where do they come from? In this video we are going to see them, not to prove them. And we will see them with ruler and compass as the Greek geometers did.""")) as tracker:
            self.pausa(tracker.duration/2)
            self.play(FadeOut(ocho), run_time=tracker.duration/4)
            self.play(Create(recta), run_time=tracker.duration/4)
        
        with self.voiceover(text=tr("""Para ello, un número real será un punto de una recta en la que hemos fijado el cero y el uno.""",
                                    """For that, a real number will be a point on a line on which we have fixed zero and one.""")) as tracker:
            self.play(Indicate(recta.numbers[0], color=COLOR_RESULTADO), Indicate(recta.numbers[1], color=COLOR_RESULTADO),
                      run_time=tracker.duration/3)
            self.play(Create(arco), run_time=tracker.duration/3)
            self.play(FadeIn(punto_a), FadeIn(etq_a), FadeOut(arco), run_time=tracker.duration/3)
        
        with self.voiceover(text=tr("""Veremos que las sumas y los productos de números reales se pueden construir con la regla y el compás, trasladando segmentos y trazando paralelas. Pero también, que dicha construcción es incómoda en la práctica. De tratar de evitar esa incomodidad nace la manera moderna de hacer matemáticas: operar con símbolos siguiendo unas pocas reglas.""",
                                    """We will see that sums and products of real numbers can be constructed with ruler and compass, by moving segments and drawing parallel lines. But also, that such a construction is cumbersome in practice. The modern way of doing mathematics was born from trying to avoid that inconvenience: operating with symbols by following a few rules.""")) as tracker:
            reglas = Tex(tr("regla y compás $\\;\\longrightarrow\\;$ reglas para manipular símbolos",
                            "ruler and compass $\\;\\longrightarrow\\;$ rules for manipulating symbols"),
                         font_size=40).set_color(COLOR_ESCALAR).next_to(recta, DOWN, buff=0.9)
            self.pausa(tracker.duration/2)
            self.play(Write(reglas), run_time=tracker.duration/2)
        
        self.pausa()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("La suma, con regla y compás", "Addition, with ruler and compass"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        a, b, c = 2, 3, 1.5
        recta = NumberLine(x_range=[-4, 9, 1], length=12.5, include_numbers=False).shift(1.9*DOWN)
        recta.add_numbers([0, 1], font_size=36)
        u = recta.n2p(1)[0] - recta.n2p(0)[0]
        
        def altura(fila):
            return 1.2 + 0.55*fila
        
        def segmento(desde, hasta, color, fila=0):
            return Line(recta.n2p(desde) + altura(fila)*UP, recta.n2p(hasta) + altura(fila)*UP,
                        color=color, stroke_width=10)
        
        def rotulo(seg, texto, color):
            return MathTex(texto, color=color, font_size=42).next_to(seg, UP, buff=0.12)
        
        def compas(seg_origen, valor, desde, fila=0, run_time=1.5, antes=None, abatir=None):
            """Copia el segmento `seg_origen` (de longitud |valor|; su origen es el extremo
            `start`), marca el origen con un punto, levanta la copia en vertical sobre el
            origen, la traslada hasta poner el origen en el punto `desde` y la abate con el
            compás: en el sentido de las agujas del reloj si valor>0, en el contrario si
            valor<0 (el segmento queda orientado como estaba).
            Así se ve desde el principio que el segmento trasladado mide lo mismo y cuál de
            sus extremos es el origen. Devuelve la copia y un grupo con el arco y el punto
            del origen (para borrarlos después).
            Para que el movimiento acompañe a la voz, `antes` y `abatir` son marcas
            (<bookmark mark='x'/>) a las que se espera antes de levantar el segmento y antes
            de abatirlo; deben usarse dentro de un `with self.voiceover(...)`."""
            base = recta.n2p(desde) + altura(fila)*UP
            copia = seg_origen.copy()
            inicio = copia.get_start()
            origen = Dot(inicio, color=copia.get_color(), radius=0.11)
            movil = VGroup(copia, origen)
            hacia_derecha = copia.get_end()[0] > inicio[0]
            if antes is not None:
                self.wait_until_bookmark(antes)
            self.play(FadeIn(origen, scale=2), run_time=run_time/8)
            self.play(Rotate(movil, angle=PI/2 if hacia_derecha else -PI/2, about_point=inicio), run_time=run_time/4)
            self.play(movil.animate.shift(base - inicio), run_time=run_time/4)
            if abatir is not None:
                self.wait_until_bookmark(abatir)
            angulo = -PI/2 if valor > 0 else PI/2
            arco = Arc(radius=abs(valor)*u, start_angle=PI/2, angle=angulo, arc_center=base,
                       color=GRAY_B, stroke_width=1.5)
            self.play(Rotate(movil, angle=angulo, about_point=base), Create(arco), run_time=3*run_time/8)
            return copia, VGroup(arco, origen)
        
        def marca(valor, texto, color=COLOR_RESULTADO):
            punto = Dot(recta.n2p(valor), color=color, radius=0.09)
            etq = MathTex(texto, color=color, font_size=42).next_to(punto, DOWN, buff=0.45)
            return VGroup(punto, etq)
        
        def regla(texto):
            return MathTex(texto, font_size=52, color=COLOR_REGLA).next_to(cabecera, DOWN, buff=0.5)
        
        seg_a = segmento(0, a, COLOR_A)
        etq_a = rotulo(seg_a, "a", COLOR_A)
        origen_a = Dot(seg_a.get_start(), color=COLOR_A, radius=0.11)
        
        with self.voiceover(text=tr("""Empecemos por la suma. Fijados el cero y el uno, tomemos un número a. Es un punto de la recta. Pero también podemos verlo como un segmento: <bookmark mark='origen'/>su origen está siempre en el cero, <bookmark mark='extremo'/>y su otro extremo es el número a.""",
                                    """Let us start with addition. Once zero and one are fixed, a number 'a' is a point on the line. But we can also see it as a segment: <bookmark mark='origen'/>its origin is always at zero, <bookmark mark='extremo'/>and its other end is the number 'a'.""")) as tracker:
            self.play(Create(recta), run_time=1.5)
            self.play(FadeIn(marca(a, "a", COLOR_A)[0]), run_time=0.6)
            self.wait_until_bookmark("origen")
            self.play(FadeIn(origen_a, scale=2), Indicate(recta.numbers[0], color=COLOR_RESULTADO), run_time=1)
            self.wait_until_bookmark("extremo")
            self.play(Create(seg_a), FadeIn(etq_a), run_time=1.2)
            self.play(FadeOut(origen_a), run_time=0.4)
        
        seg_b = segmento(0, b, COLOR_B, fila=1)
        etq_b = rotulo(seg_b, "b", COLOR_B)
        regla1 = regla("a+b=b+a")
        
        with self.voiceover(text=tr("""Y aquí tenemos otro número, b: otro segmento con el origen en el cero.""",
                                    """And here we have another number, b: another segment with its origin at zero.""")) as tracker:
            self.play(Create(seg_b), FadeIn(etq_b), run_time=tracker.duration)
        
        with self.voiceover(text=tr("""Para sumar 'a' y b, <bookmark mark='traslada'/>trasladamos el segmento b, <bookmark mark='origen'/>y ponemos su origen en el extremo de 'a'. Eso es justo lo que hace un compás: toma una longitud y la lleva a otro sitio.""",
                                    """To add the two numbers, <bookmark mark='traslada'/>we move the second segment, 'b', <bookmark mark='origen'/>and place its origin at the end of the first, 'a'. That is exactly what a compass does: it takes a length and carries it somewhere else.<bookmark mark='v1'/>""")) as tracker:
            self.anuncia_regla(regla1, run_time=0.8)
            seg_b_tras, arco1 = compas(seg_b, b, a, fila=0, run_time=2.4, antes="traslada", abatir="origen")
            etq_b_tras = rotulo(seg_b_tras, "b", COLOR_B)
            self.add(etq_b_tras)
        
        # la suma es un nuevo segmento con origen en el cero (en blanco, debajo de los dos sumandos)
        marca_ab = marca(a + b, "a+b")
        seg_ab = segmento(0, a + b, COLOR_RESULTADO, fila=-1).set_stroke(width=6)
        with self.voiceover(text=tr("""El extremo del segmento trasladado es la suma, 'a' más b. <bookmark mark='nuevo'/>Es decir, la suma es un nuevo segmento: con el origen en el cero, como siempre, y con el otro extremo en 'a' más b.""",
                                    """The end of the moved segment is the sum, 'a' plus 'b'. <bookmark mark='nuevo'/>That is, the sum is a new segment: with its origin at zero, as always, and with its other end at the sum.""")) as tracker:
            self.play(FadeIn(marca_ab), run_time=0.8)
            self.wait_until_bookmark("nuevo")
            self.play(Create(seg_ab), run_time=1.5)
        
        with self.voiceover(text=tr("""Hagámoslo ahora en el otro orden: partimos de b <bookmark mark='traslada'/>y ponemos el origen de a en el extremo de b.""",
                                    """Let us now do it in the other order: we start from 'b' <bookmark mark='traslada'/>and place the origin of 'a' at the end of b.""")) as tracker:
            seg_a_tras, arco2 = compas(seg_a, a, b, fila=1, run_time=2.4, antes="traslada")
            etq_a_tras = rotulo(seg_a_tras, "a", COLOR_A)
            self.add(etq_a_tras)
        
        linea = DashedLine(recta.n2p(a + b) + 0.1*UP, recta.n2p(a + b) + altura(1.6)*UP, color=COLOR_RESULTADO)
        with self.voiceover(text=tr("""Llegamos exactamente al mismo punto. Es la propiedad conmutativa de la suma.""",
                                    """We arrive at exactly the same point. This is the commutative property of addition.""")) as tracker:
            self.play(Create(linea), FadeOut(arco1, arco2), run_time=tracker.duration/3)
            self.destaca_regla(regla1)
        
        self.play(FadeOut(seg_b, etq_b, seg_b_tras, etq_b_tras, seg_a_tras, etq_a_tras, linea, marca_ab, seg_ab))
        
        # asociativa: las dos agrupaciones se construyen en el orden en que se enuncian.
        # (a+b)+c en la fila 0; a+(b+c) en la fila 1, con b+c construido antes en la fila 2.
        seg_b2 = segmento(0, b, COLOR_B, fila=2)
        seg_c3 = segmento(0, c, COLOR_C, fila=3)
        etq_b2, etq_c3 = rotulo(seg_b2, "b", COLOR_B), rotulo(seg_c3, "c", COLOR_C)
        regla2 = regla("a+(b+c)=(a+b)+c")
        self.anuncia_regla(regla2, regla1)
        self.play(FadeIn(seg_b2, etq_b2, seg_c3, etq_c3))
        
        with self.voiceover(text=tr("""Con tres números podemos agrupar de dos maneras. <bookmark mark='ab'/>Primero 'a' más b, poniendo el origen de b en el extremo de 'a'. <bookmark mark='c'/>Y después sumar c.""",
                                    """With three numbers we can group in two ways. <bookmark mark='ab'/>First 'a' plus b, placing the origin of b at the end of 'a'. <bookmark mark='c'/>And then add c.""")) as tracker:
            self.wait_until_bookmark("ab")
            seg_b0, arco1 = compas(seg_b2, b, a, fila=0, run_time=1.6)
            etq_b0 = rotulo(seg_b0, "b", COLOR_B)
            self.add(etq_b0)
            llave1 = Brace(VGroup(seg_a, seg_b0), DOWN, buff=0.1, color=GRAY_B)
            etq_llave1 = llave1.get_tex("a+b").set_color(GRAY_B)
            self.play(GrowFromCenter(llave1), FadeIn(etq_llave1), FadeOut(arco1), run_time=0.8)
            self.wait_until_bookmark("c")
            seg_c0, arco2 = compas(seg_c3, c, a + b, fila=0, run_time=1.6)
            etq_c0 = rotulo(seg_c0, "c", COLOR_C)
            self.add(etq_c0)
            self.play(FadeOut(arco2), run_time=0.4)
        
        seg_a1 = segmento(0, a, COLOR_A, fila=1)
        etq_a1 = rotulo(seg_a1, "a", COLOR_A)
        with self.voiceover(text=tr("""O primero b más c, poniendo el origen de c en el extremo de b. <bookmark mark='a'/>Y después sumárselo al número a.""",
                                    """Or first b plus c, placing the origin of c at the end of b. <bookmark mark='a'/>And then add it to the number 'a'.""")) as tracker:
            seg_c2, arco3 = compas(seg_c3, c, b, fila=2, run_time=1.6)
            etq_c2 = rotulo(seg_c2, "c", COLOR_C)
            self.add(etq_c2)
            grupo_bc = VGroup(seg_b2, etq_b2, seg_c2, etq_c2)
            llave2 = Brace(grupo_bc, UP, buff=0.1, color=GRAY_B)
            etq_llave2 = llave2.get_tex("b+c").set_color(GRAY_B)
            self.play(FadeOut(arco3, seg_c3, etq_c3), run_time=0.4)
            self.play(GrowFromCenter(llave2), FadeIn(etq_llave2), run_time=0.8)
            grupo_bc.add(llave2, etq_llave2)
            self.wait_until_bookmark("a")
            self.play(FadeIn(seg_a1, etq_a1), run_time=0.6)
            # el segmento b+c, ya construido, se traslada en bloque hasta el extremo de a
            self.play(grupo_bc.animate.shift(recta.n2p(a) - recta.n2p(0) + (altura(1) - altura(2))*UP), run_time=1.5)
        
        marca_abc = marca(a + b + c, "a+b+c")
        with self.voiceover(text=tr("""El punto final es el mismo. Es la propiedad asociativa.""",
                                    """The end point is the same. This is the associative property.""")) as tracker:
            self.play(FadeIn(marca_abc), run_time=tracker.duration/3)
            self.destaca_regla(regla2)
        
        self.play(FadeOut(seg_b0, etq_b0, seg_c0, etq_c0, seg_a1, etq_a1, grupo_bc, llave1, etq_llave1, marca_abc))
        
        # cero: un segmento de longitud cero (un punto) con el origen en el cero, que se traslada como los demás
        cero = Dot(recta.n2p(0) + altura(1)*UP, color=COLOR_B, radius=0.12)
        regla3 = regla("a+0=a")
        with self.voiceover(text=tr("""Sumar cero es sumar un segmento de longitud cero: <bookmark mark='punto'/>un punto, con el origen en el cero. <bookmark mark='traslada'/>Lo ponemos en el extremo de a, <bookmark mark='quietos'/>y no nos movemos de a. <bookmark mark='neutro'/>El cero es el elemento neutro de la suma.""",
                                    """Adding zero means adding a segment of length zero: <bookmark mark='punto'/>a point, with its origin at zero. <bookmark mark='traslada'/>We place it at the end of a, <bookmark mark='quietos'/>and we do not move away from 'a'. <bookmark mark='neutro'/>Zero is the identity element for addition.""")) as tracker:
            self.anuncia_regla(regla3, regla2, run_time=0.8)
            self.wait_until_bookmark("punto")
            self.play(FadeIn(cero, scale=3), run_time=0.8)
            self.wait_until_bookmark("traslada")
            self.play(cero.animate.move_to(recta.n2p(a) + altura(0)*UP), run_time=1.5)
            self.wait_until_bookmark("quietos")
            self.play(Flash(cero, color=COLOR_RESULTADO), run_time=0.8)
            self.wait_until_bookmark("neutro")
            self.destaca_regla(regla3)
            self.play(FadeOut(cero), run_time=0.5)
        
        self.pausa(1.2)   # respiro antes de cambiar de propiedad (1,5 s resultaba largo)
        
        # opuesto: el mismo segmento abatido al lado contrario del cero (origen en el cero; si a>0 el extremo queda a la izquierda)
        regla4 = regla("a+(-a)=0")
        with self.voiceover(text=tr("""Todo número tiene un opuesto. Para construir el opuesto de a, <bookmark mark='compas'/>ponemos el compás en el cero <bookmark mark='abatimos'/>y abatimos el segmento hacia el lado contrario. <bookmark mark='obtenemos'/>Obtenemos menos a, un segmento con el origen en el cero, como todos, pero que se extiende hacia el otro lado.""",
                                    """Every number has an opposite. To construct the opposite of 'a', <bookmark mark='compas'/>we put the compass at zero <bookmark mark='abatimos'/>and swing the segment to the opposite side. <bookmark mark='obtenemos'/>We get minus a: a segment with its origin at zero, like all of them, but extending to the other side.""")) as tracker:
            self.anuncia_regla(regla4, regla3, run_time=0.8)
            seg_ma, arco1 = compas(seg_a, -a, 0, fila=0, run_time=2.4, antes="compas", abatir="abatimos")
            seg_ma.set_opacity(0.6)
            self.wait_until_bookmark("obtenemos")
            marca_ma = marca(-a, "-a", COLOR_A)
            self.play(FadeIn(marca_ma), FadeOut(arco1[0]), run_time=0.8)   # el punto del origen (arco1[1]) se queda en el cero
        
        with self.voiceover(text=tr("""Sumemos ahora 'a' y su opuesto con la regla de siempre: <bookmark mark='traslada'/>trasladamos el segmento opuesto, y ponemos su origen en el extremo de 'a'. <bookmark mark='cae'/>Su otro extremo cae justo en el cero. <bookmark mark='regla'/>'a', más su opuesto es cero.""",
                                    """Now let us add 'a' and its opposite with the usual rule: <bookmark mark='traslada'/>we move the opposite segment, and place its origin at the end of a. <bookmark mark='cae'/>Its other end lands exactly at zero. <bookmark mark='regla'/>'a' plus its opposite is zero.""")) as tracker:
            seg_ma1, arco2 = compas(seg_ma, -a, a, fila=1, run_time=2.4, antes="traslada", abatir="cae")
            punto_0 = Dot(recta.n2p(0), color=COLOR_RESULTADO, radius=0.09)
            linea0 = DashedLine(recta.n2p(0) + 0.1*UP, recta.n2p(0) + altura(1.6)*UP, color=COLOR_RESULTADO)
            self.play(Create(linea0), FadeIn(punto_0), Indicate(recta.numbers[0], color=COLOR_RESULTADO), FadeOut(arco2), run_time=0.8)
            self.wait_until_bookmark("regla")
            self.destaca_regla(regla4)
        
        with self.voiceover(text=tr("""Acabamos de ver cuatro propiedades de la suma. Y las cuatro se ven en la recta con una sola regla: poner el origen de un segmento en el extremo del otro.""",
                                    """We have just seen four properties of addition. And all four can be seen on the line with a single rule: placing the origin of one segment at the end of the other.""")) as tracker:
            self.pausa(tracker.duration)
        
        self.pausa()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("El producto, con regla y compás", "Multiplication, with ruler and compass"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        a, b, c = 2, 1.5, 2
        ax = Axes(x_range=[-0.5, 8.5, 1], y_range=[-0.5, 4.2, 1], x_length=10, y_length=10*4.7/9,
                  tips=False, axis_config={"include_ticks": True})
        ax.shift(np.array([-4.8, -2.45, 0]) - ax.c2p(0, 0))   # origen abajo a la izquierda
        O = ax.c2p(0, 0)
        ux = ax.c2p(1, 0)[0] - O[0]
        
        def recta_por(p, q, color=GRAY_B, ext=1.25):
            return Line(ax.c2p(*p), ax.c2p(*q), color=color, stroke_width=2.5).scale(ext)
        
        def marca_x(valor, texto, color=COLOR_RESULTADO, buff=0.35):
            punto = Dot(ax.c2p(valor, 0), color=color, radius=0.09)
            etq = MathTex(texto, color=color, font_size=42).next_to(punto, DOWN, buff=buff)
            return VGroup(punto, etq)
        
        def marca_y(valor, texto, color=COLOR_RESULTADO):
            punto = Dot(ax.c2p(0, valor), color=color, radius=0.09)
            etq = MathTex(texto, color=color, font_size=42).next_to(punto, LEFT, buff=0.3)
            return VGroup(punto, etq)
        
        def seg_x(desde, hasta, color, altura=0.0):
            return Line(ax.c2p(desde, 0) + altura*UP, ax.c2p(hasta, 0) + altura*UP, color=color, stroke_width=10)
        
        def seg_y(desde, hasta, color):
            return Line(ax.c2p(0, desde), ax.c2p(0, hasta), color=color, stroke_width=10)
        
        def regla(texto):
            return MathTex(texto, font_size=52, color=COLOR_REGLA).next_to(cabecera, DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""Pasemos al producto. En el vídeo anterior vimos una construcción geométrica que multiplica dos números. Recordémosla.""",
                                    """Let us move on to multiplication. In the previous video we saw a geometric construction that multiplies two numbers. Let us recall it.""")) as tracker:
            self.play(Create(ax), run_time=tracker.duration/2)
        
        m_a, m_b, m_1 = marca_x(a, "a", COLOR_A), marca_y(b, "b", COLOR_B), marca_y(1, "1")
        with self.voiceover(text=tr("""Ponemos 'a' en el eje horizontal y b en el eje vertical.""",
                                    """We place a on the horizontal axis and 'b' on the vertical axis.""")) as tracker:
            self.play(FadeIn(m_a), run_time=tracker.duration/2)
            self.play(FadeIn(m_b), run_time=tracker.duration/2)
        
        diagonal = recta_por((a, 0), (0, 1))
        with self.voiceover(text=tr("""Trazamos la recta que une el punto 'a' del eje horizontal con el punto uno del eje vertical.""",
                                    """We draw the line joining point a on the horizontal axis with point one on the vertical axis.""")) as tracker:
            self.play(FadeIn(m_1), run_time=tracker.duration/4)
            self.play(Create(diagonal), run_time=tracker.duration/2)
        
        paralela_b = recta_por((a*b, 0), (0, b), color=COLOR_B)
        with self.voiceover(text=tr("""Y trazamos la paralela que pasa por b. <break time="600ms"/> Dibujar una paralela es una construcción clásica con regla y compás.""",
                                    """And we draw the parallel line through 'b'. <break time="600ms"/> Drawing a parallel is a classical ruler and compass construction.""")) as tracker:
            self.play(TransformFromCopy(diagonal, paralela_b), run_time=tracker.duration*0.6)
        
        m_ab = marca_x(a*b, "ab")
        with self.voiceover(text=tr("""Donde esa paralela corta al eje horizontal está el producto a por b.""",
                                    """Where that parallel meets the horizontal axis is the product 'a' times 'b'.""")) as tracker:
            self.play(FadeIn(m_ab, scale=2), run_time=tracker.duration/2)
        
        # la construcción como homotecia
        t = ValueTracker(b)
        paralela_t = always_redraw(lambda: recta_por((a*t.get_value(), 0), (0, t.get_value()), color=COLOR_ESCALAR))
        punto_t = always_redraw(lambda: Dot(ax.c2p(a*t.get_value(), 0), color=COLOR_ESCALAR, radius=0.09))
        punto_ty = always_redraw(lambda: Dot(ax.c2p(0, t.get_value()), color=COLOR_ESCALAR, radius=0.09))
        with self.voiceover(text=tr("""Fíjese en lo que hace esta figura: a cada número del eje vertical le asigna un número del eje horizontal, su producto por a. Si subimos por el eje vertical, el resultado se aleja proporcionalmente.""",
                                    """Notice what this figure does: to each number on the vertical axis it assigns a number on the horizontal axis, its product by 'a'. As we go up the vertical axis, the result moves away proportionally.""")) as tracker:
            self.add(paralela_t, punto_t, punto_ty)
            self.play(t.animate.set_value(2.8), run_time=tracker.duration*0.4, rate_func=there_and_back)
            self.play(t.animate.set_value(0.4), run_time=tracker.duration*0.4, rate_func=there_and_back)
        
        regla1 = regla("1a=a")
        with self.voiceover(text=tr("""Si tomamos el uno, la paralela es la propia recta inicial, y el resultado es a. Uno por 'a' es 'a': el uno es el elemento neutro del producto.""",
                                    """If we take one, the parallel line is the initial line itself, and the result is 'a'. One times a is 'a': one is the identity element for multiplication.""")) as tracker:
            self.anuncia_regla(regla1, run_time=0.8)
            self.play(t.animate.set_value(1), run_time=tracker.duration/3)
            self.play(Indicate(m_a, color=COLOR_RESULTADO), run_time=tracker.duration/4)
            self.destaca_regla(regla1)
        
        # inverso: la paralela que corta al eje horizontal en el uno
        regla_inv = regla(r"a\,a^{-1}=1")
        m_1x = marca_x(1, "1")
        m_inv = marca_y(1/a, "a^{-1}", COLOR_A)
        with self.voiceover(text=tr("""Hay otra propiedad del producto: todo número distinto de cero tiene un inverso, un número que multiplicado por él da uno. <bookmark mark='mueve'/>Para construirlo, movemos la paralela hasta que corte al eje horizontal justo en el uno. <bookmark mark='inverso'/>Donde esa paralela corta al eje vertical está el inverso de a.""",
                                    """There is another property of multiplication: every nonzero number has an inverse, a number which multiplied by it gives one. <bookmark mark='mueve'/>To construct it, we move the parallel line until it meets the horizontal axis exactly at one. <bookmark mark='inverso'/>Where that parallel meets the vertical axis is the inverse of 'a'.""")) as tracker:
            self.anuncia_regla(regla_inv, regla1, run_time=0.8)
            self.wait_until_bookmark("mueve")
            self.play(FadeIn(m_1x, scale=2), run_time=0.6)
            self.play(t.animate.set_value(1/a), run_time=2)
            self.wait_until_bookmark("inverso")
            self.play(FadeIn(m_inv, scale=2), run_time=0.8)
            self.destaca_regla(regla_inv)
            self.remove(paralela_t, punto_t, punto_ty)
            self.play(FadeOut(m_1x, m_inv), run_time=0.5)
        
        self.pausa(1.2)   # respiro antes de cambiar de propiedad
        
        # distributiva
        regla2 = regla("a(b+c)=ab+ac")
        seg_b_y = seg_y(0, b, COLOR_B)
        seg_c_y = seg_y(b, b + c, COLOR_C)
        m_bc = marca_y(b + c, "b+c", COLOR_C)
        with self.voiceover(text=tr("""Ahora sumemos otro número c a b, trasladándolo con el compás sobre el eje vertical, encima de b.""",
                                    """Now let us add a third number, c, to b, moving it with the compass along the vertical axis, on top of 'b'.""")) as tracker:
            self.anuncia_regla(regla2, regla_inv, run_time=0.8)
            self.play(Create(seg_b_y), run_time=tracker.duration/4)
            self.play(Create(seg_c_y), FadeIn(m_bc), run_time=tracker.duration/2)
        
        paralela_bc = recta_por((a*(b + c), 0), (0, b + c), color=COLOR_C)
        m_abc = marca_x(a*(b + c), "a(b+c)")
        with self.voiceover(text=tr("""La paralela que pasa por 'b más c' nos da el producto 'a' por 'b más c'.""",
                                    """The parallel through b plus c gives us the product 'a' times b plus c.""")) as tracker:
            self.play(TransformFromCopy(diagonal, paralela_bc), run_time=tracker.duration/2)
            self.play(FadeIn(m_abc, scale=2), run_time=tracker.duration/4)
        
        seg_ab_x = seg_x(0, a*b, COLOR_B, altura=0.18)
        seg_ac_x = seg_x(a*b, a*(b + c), COLOR_C, altura=0.18)
        with self.voiceover(text=tr("""En el eje horizontal, <bookmark mark='s1'/>entre cero y 'a' por 'b', está el segmento 'a' 'b'. <bookmark mark='s2'/>Y entre 'a' por b y 'a' por 'b más c' queda otro segmento.""",
                                    """On the horizontal axis, <bookmark mark='s1'/>between zero and ab lies the segment 'a' times 'b'. <bookmark mark='s2'/>And between 'a' times b and 'a' times b plus c there is another segment.""")) as tracker:
            self.wait_until_bookmark("s1")
            self.play(Create(seg_ab_x), run_time=1)
            self.play(Indicate(seg_ab_x, color=COLOR_RESULTADO, scale_factor=1.05), run_time=1)
            self.wait_until_bookmark("s2")
            self.play(Create(seg_ac_x), run_time=1)
            self.play(Indicate(seg_ac_x, color=COLOR_RESULTADO, scale_factor=1.05), run_time=1)
        
        paralela_c = recta_por((a*c, 0), (0, c), color=COLOR_C).set_opacity(0.6)
        m_c = marca_y(c, "c", COLOR_C)
        m_ac = marca_x(a*c, "ac", COLOR_C, buff=0.8)
        with self.voiceover(text=tr("""¿Cuánto mide ese segmento? <bookmark mark='aparte'/>Construyamos aparte el producto a por c, con la paralela que pasa por c.""",
                                    """How long is that segment? <bookmark mark='aparte'/>Let us construct separately the product 'a' times c, with the parallel through 'c'.""")) as tracker:
            self.play(Indicate(seg_ac_x, color=COLOR_RESULTADO, scale_factor=1.05), run_time=1.2)
            self.wait_until_bookmark("aparte")
            self.play(FadeIn(m_c), run_time=tracker.duration/4)
            self.play(TransformFromCopy(diagonal, paralela_c), run_time=tracker.duration/3)
            self.play(FadeIn(m_ac, scale=2), run_time=tracker.duration/4)
        
        # el compás, como en la escena 2: la copia (en blanco) se levanta sobre su extremo izquierdo,
        # se lleva al origen y se abate hacia la derecha, en el sentido de las agujas del reloj
        copia = seg_ac_x.copy().set_color(COLOR_RESULTADO)
        with self.voiceover(text=tr("""Y traslademos el segmento con el compás hasta el origen. <bookmark mark='coincide'/>Coincide exactamente con a por c.""",
                                    """And let us move the segment with the compass to the origin. <bookmark mark='coincide'/>It coincides exactly with 'a' times c.<bookmark mark='v1'/>""")) as tracker:
            inicio = copia.get_start()
            origen = O + 0.18*UP
            self.play(Rotate(copia, angle=PI/2, about_point=inicio), run_time=0.7)
            self.play(copia.animate.shift(origen - inicio), run_time=0.7)
            arco = Arc(radius=a*c*ux, start_angle=PI/2, angle=-PI/2, arc_center=origen, color=GRAY_B, stroke_width=1.5)
            self.play(Rotate(copia, angle=-PI/2, about_point=origen), Create(arco), run_time=1.2)
            self.wait_until_bookmark("coincide")
            self.play(FadeOut(arco), Indicate(m_ac, color=COLOR_RESULTADO), run_time=1)
        
        # cada segmento vertical "viaja" hasta su imagen en el eje horizontal; después, las dos sumas
        with self.voiceover(text=tr("""No es casualidad: <bookmark mark='traslada'/>la figura traslada los segmentos del eje vertical al horizontal agrandándolos todos en la misma proporción. <bookmark mark='sumav'/>Por eso una suma en el eje vertical <bookmark mark='sumah'/>se convierte en una suma en el horizontal. <bookmark mark='distributiva'/>Es la propiedad distributiva.""",
                                    """This is no coincidence: <bookmark mark='traslada'/>the figure carries the segments from the vertical axis to the horizontal one, enlarging them all in the same proportion. <bookmark mark='sumav'/>That is why a sum on the vertical axis <bookmark mark='sumah'/>becomes a sum on the horizontal axis. <bookmark mark='distributiva'/>This is the distributive property.""")) as tracker:
            self.play(FadeOut(copia), run_time=0.5)
            self.wait_until_bookmark("traslada")
            viaje_b, viaje_c = seg_b_y.copy(), seg_c_y.copy()
            self.play(Transform(viaje_b, seg_ab_x), run_time=1.3)
            self.play(Transform(viaje_c, seg_ac_x), run_time=1.3)
            self.remove(viaje_b, viaje_c)
            # "una suma": los dos sumandos se apartan y se separan un instante, y vuelven a encajar uno a continuación del otro
            self.wait_until_bookmark("sumav")
            cb, cc = seg_b_y.copy(), seg_c_y.copy()
            self.play(cb.animate.shift(0.9*LEFT), cc.animate.shift(0.9*LEFT + 0.5*UP), run_time=0.6)
            self.play(cb.animate.shift(0.9*RIGHT), cc.animate.shift(0.9*RIGHT + 0.5*DOWN), run_time=0.7)
            self.play(Indicate(m_bc, color=COLOR_RESULTADO), run_time=0.6)
            self.remove(cb, cc)
            self.wait_until_bookmark("sumah")
            cab, cac = seg_ab_x.copy(), seg_ac_x.copy()
            self.play(cab.animate.shift(0.8*UP + 0.4*LEFT), cac.animate.shift(0.8*UP + 0.4*RIGHT), run_time=0.6)
            self.play(cab.animate.shift(0.8*DOWN + 0.4*RIGHT), cac.animate.shift(0.8*DOWN + 0.4*LEFT), run_time=0.7)
            self.play(Indicate(m_abc, color=COLOR_RESULTADO), run_time=0.6)
            self.remove(cab, cac)
            self.wait_until_bookmark("distributiva")
            self.destaca_regla(regla2)
        
        self.pausa()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Dos propiedades incómodas", "Two uncomfortable properties"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        a, b, c = 2, 1.5, 2.5
        ax = Axes(x_range=[-0.5, 8.5, 1], y_range=[-0.5, 4.2, 1], x_length=10, y_length=10*4.7/9,
                  tips=False, axis_config={"include_ticks": True})
        ax.shift(np.array([-4.8, -2.45, 0]) - ax.c2p(0, 0))   # origen abajo a la izquierda
        O = ax.c2p(0, 0)
        ux = ax.c2p(1, 0)[0] - O[0]
        
        def recta_por(p, q, color=GRAY_B, ext=1.25):
            return Line(ax.c2p(*p), ax.c2p(*q), color=color, stroke_width=2.5).scale(ext)
        
        def marca_x(valor, texto, color=COLOR_RESULTADO, buff=0.35):
            punto = Dot(ax.c2p(valor, 0), color=color, radius=0.09)
            etq = MathTex(texto, color=color, font_size=42).next_to(punto, DOWN, buff=buff)
            return VGroup(punto, etq)
        
        def marca_y(valor, texto, color=COLOR_RESULTADO):
            punto = Dot(ax.c2p(0, valor), color=color, radius=0.09)
            etq = MathTex(texto, color=color, font_size=42).next_to(punto, LEFT, buff=0.3)
            return VGroup(punto, etq)
        
        def arco_x_a_y(valor, color):
            """Arco de compás, centrado en el origen, que lleva el punto (valor,0) a (0,valor)."""
            return Arc(radius=valor*ux, start_angle=0, angle=PI/2, arc_center=O, color=color, stroke_width=1.5)
        
        def regla(texto):
            return MathTex(texto, font_size=52, color=COLOR_REGLA).next_to(cabecera, DOWN, buff=0.5)
        
        def multiplica(x, y, color, velocidad=1.0):
            """Construye x·y: recta por (x,0),(0,1) y paralela por (0,y). Devuelve los objetos creados."""
            d = recta_por((x, 0), (0, 1))
            p = recta_por((x*y, 0), (0, y), color=color)
            self.play(Create(d), run_time=0.8*velocidad)
            self.play(TransformFromCopy(d, p), run_time=0.8*velocidad)
            return VGroup(d, p)
        
        self.play(Create(ax), run_time=1)
        m_a, m_b, m_1 = marca_x(a, "a", COLOR_A), marca_y(b, "b", COLOR_B), marca_y(1, "1")
        self.play(FadeIn(m_a, m_b, m_1), run_time=0.8)
        regla1 = regla("ab=ba")
        regla2 = regla("a(bc)=(ab)c")
        
        with self.voiceover(text=tr("""¿Y la conmutativa? a por b igual a b por a. Nuestra construcción pone 'a' en el eje horizontal y b en el vertical, y nos da a por b.""",
                                    """What about commutativity? 'a' times b equals b times a. Our construction puts a on the horizontal axis and b on the vertical one, and gives us the product 'a' times b.<bookmark mark='v1'/>""")) as tracker:
            self.anuncia_regla(regla1, run_time=0.8)
            rectas_ab = multiplica(a, b, COLOR_B, velocidad=tracker.duration/4)
            m_ab = marca_x(a*b, "ab")
            self.play(FadeIn(m_ab, scale=2), run_time=tracker.duration/5)
        
        with self.voiceover(text=tr("""Para calcular b por a necesitamos intercambiar los papeles: llevamos b al eje horizontal y a al eje vertical, con dos arcos de compás.""",
                                    """To compute b times 'a' we have to swap the roles: we carry b to the horizontal axis and a to the vertical one, with two compass arcs.<bookmark mark='v1'/>""")) as tracker:
            self.play(rectas_ab.animate.set_stroke(opacity=0.35), run_time=tracker.duration/6)
            arco_b, arco_a = arco_x_a_y(b, COLOR_B), arco_x_a_y(a, COLOR_A)
            m_b_x, m_a_y = marca_x(b, "b", COLOR_B, buff=0.8), marca_y(a, "a", COLOR_A)
            self.play(Create(arco_b), FadeIn(m_b_x), run_time=tracker.duration/3)
            self.play(Create(arco_a), FadeIn(m_a_y), run_time=tracker.duration/3)
        
        with self.voiceover(text=tr("""Y repetimos la construcción: la recta por b y por uno, y su paralela por a.""",
                                    """And we repeat the construction: the line through 'b' and one, and its parallel through the point a.""")) as tracker:
            rectas_ba = multiplica(b, a, COLOR_A, velocidad=tracker.duration/3)
        
        with self.voiceover(text=tr("""Son dos construcciones distintas, <bookmark mark='mismo'/>y acaban en el mismo punto. <bookmark mark='regla'/>Que coincidan no es casualidad, pero tampoco es evidente: para justificarlo hacen falta triángulos semejantes.""",
                                    """They are two different constructions, <bookmark mark='mismo'/>and they end at the same point. <bookmark mark='regla'/>That they coincide is no coincidence, but it is not obvious either: to justify it one needs similar triangles.""")) as tracker:
            self.wait_until_bookmark("mismo")
            self.play(Indicate(m_ab, color=COLOR_RESULTADO, scale_factor=1.6), run_time=1)
            self.wait_until_bookmark("regla")
            self.destaca_regla(regla1)
        
        self.play(FadeOut(rectas_ab, rectas_ba, arco_a, arco_b, m_b_x, m_a_y, m_ab, m_b), run_time=0.8)
        
        # asociativa
        with self.voiceover(text=tr("""La asociativa es peor: a por, b por c, frente a, a por b, por c. Hay que multiplicar dos veces, y entre medias llevar el resultado del eje horizontal al vertical con el compás.""",
                                    """Associativity is worse: the number 'a' times the product b times c, versus the product 'a' times b, times c. We must multiply twice, and in between carry the result from the horizontal axis to the vertical one with the compass.""")) as tracker:
            self.anuncia_regla(regla2, regla1, run_time=0.8)
            m_c, m_b_x = marca_y(c, "c", COLOR_C), marca_x(b, "b", COLOR_B, buff=0.8)
            self.play(FadeIn(m_c, m_b_x), run_time=tracker.duration/5)
            r1 = multiplica(b, c, COLOR_C, velocidad=tracker.duration/8)
            m_bc = marca_x(b*c, "bc", COLOR_C, buff=0.8)
            self.play(FadeIn(m_bc), run_time=tracker.duration/10)
            arco1 = arco_x_a_y(b*c, COLOR_C)
            m_bc_y = marca_y(b*c, "bc", COLOR_C)
            self.play(Create(arco1), FadeIn(m_bc_y), run_time=tracker.duration/5)
            r2 = multiplica(a, b*c, COLOR_C, velocidad=tracker.duration/8)
            m_abc = marca_x(a*b*c, "a(bc)", COLOR_C)
            self.play(FadeIn(m_abc, scale=2), run_time=tracker.duration/10)
        
        with self.voiceover(text=tr("""Y por el otro camino: a por b, lo llevamos al eje vertical, y lo multiplicamos por c.""",
                                    """And the other way round: we compute the product 'a' times 'b', carry it to the vertical axis, and multiply it by c.""")) as tracker:
            self.play(VGroup(r1, r2, arco1).animate.set_stroke(opacity=0.3), run_time=tracker.duration/8)
            r3 = multiplica(a, b, COLOR_B, velocidad=tracker.duration/8)
            m_ab = marca_x(a*b, "ab", COLOR_B)
            self.play(FadeIn(m_ab), run_time=tracker.duration/10)
            arco2 = arco_x_a_y(a*b, COLOR_B)
            m_ab_y = marca_y(a*b, "ab", COLOR_B)
            self.play(Create(arco2), FadeIn(m_ab_y), run_time=tracker.duration/5)
            m_c_x = marca_x(c, "c", COLOR_C, buff=0.8)
            self.play(FadeIn(m_c_x), run_time=tracker.duration/10)
            r4 = multiplica(c, a*b, COLOR_B, velocidad=tracker.duration/8)
            m_abc2 = MathTex("(ab)c", color=COLOR_B, font_size=42).next_to(m_abc, DOWN, buff=0.15)
            self.play(FadeIn(m_abc2), run_time=tracker.duration/10)
        
        with self.voiceover(text=tr("""Mismo punto. Pero cuente: <bookmark mark='rectas'/>cuatro rectas, <bookmark mark='paralelas'/>cuatro paralelas, <bookmark mark='arcos'/>dos arcos... <bookmark mark='tres'/>y solo para multiplicar tres números.""",
                                    """Same point. But count: <bookmark mark='rectas'/>four lines, <bookmark mark='paralelas'/>four parallels, <bookmark mark='arcos'/>two arcs... <bookmark mark='tres'/>and only to multiply three numbers.""")) as tracker:
            self.play(Indicate(m_abc, color=COLOR_RESULTADO, scale_factor=1.5), run_time=1)
            # cada cosa que cuenta la voz parpadea cuando la nombra; la fórmula, al final
            self.wait_until_bookmark("rectas")
            self.play(*[Indicate(r[0], color=COLOR_RESULTADO, scale_factor=1.03) for r in (r1, r2, r3, r4)], run_time=1)
            self.wait_until_bookmark("paralelas")
            self.play(*[Indicate(r[1], color=COLOR_RESULTADO, scale_factor=1.03) for r in (r1, r2, r3, r4)], run_time=1)
            self.wait_until_bookmark("arcos")
            self.play(Indicate(arco1, color=COLOR_RESULTADO, scale_factor=1.03), Indicate(arco2, color=COLOR_RESULTADO, scale_factor=1.03), run_time=1)
            self.wait_until_bookmark("tres")
            self.destaca_regla(regla2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not cabecera], run_time=0.8)
        
        euclides = Tex(tr("Euclides, siglo III a.\\,C.: álgebra con figuras", "Euclid, 3rd century BC: algebra with figures"),
                       font_size=42)
        descartes = Tex(tr("Descartes, 1637: los segmentos son números, y se opera con símbolos",
                           "Descartes, 1637: segments are numbers, and one operates with symbols"),
                        font_size=42).set_color(COLOR_ESCALAR)
        escuela = Tex(tr("La escuela: las reglas se comprueban con ejemplos numéricos, y se usan",
                         "School: the rules are checked on numerical examples, and used"),
                      font_size=42)
        historia = VGroup(euclides, descartes, escuela).arrange(DOWN, buff=0.6).move_to(0.3*DOWN)
        for h in historia:
            h.scale_to_fit_width(min(h.width, config.frame_width*0.9))
        
        with self.voiceover(text=tr("""Todas estas propiedades se pueden ver con regla y compás. Pero es engorroso. Y esta es la cuestión. Los geómetras griegos razonaban así, con figuras: en los Elementos de Euclides la propiedad distributiva es un teorema sobre rectángulos.""",
                                    """All these properties can be seen with ruler and compass. But it is cumbersome. And that is the point. The Greek geometers reasoned this way, with figures: in Euclid's Elements the distributive property is a theorem about rectangles.""")) as tracker:
            self.play(Write(euclides), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""Hubo que esperar casi dos mil años a que Descartes diera el salto: tratar los segmentos como números y operar con símbolos siguiendo unas pocas reglas.""",
                                    """It took almost two thousand years for Descartes to make the leap: to treat segments as numbers and to operate with symbols following a few rules.""")) as tracker:
            self.play(Write(descartes), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""Esa es la tradición que usted recibió en la escuela: allí las reglas no se justifican con figuras, se comprueban con unos cuantos ejemplos numéricos, y se usan.""",
                                    """That is the tradition you received at school: there the rules are not justified with figures, they are checked on a few numerical examples, and used.""")) as tracker:
            self.play(Write(escuela), run_time=tracker.duration/2)
        
        self.pausa()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        self.creditos()
        cabecera = Tex(tr("Las reglas del juego", "The rules of the game"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        sean = Tex(tr(r"Para cualesquiera números reales $a$, $b$ y $c$:", r"For any real numbers $a$, $b$ and $c$:"),
                   tex_template=myTemplate, font_size=40).next_to(cabecera, DOWN, buff=0.4)
        
        propiedades = [r"a+b=b+a",
                       r"a+(b+c)=(a+b)+c",
                       r"a+0=a",
                       r"a+(-a)=0",
                       r"ab=ba",
                       r"a(b+c)=ab+ac",
                       r"a(bc)=(ab)c",
                       r"1a=a",
                       r"a\,a^{-1}=1\;\;(a\neq 0)"]
        
        lista = VGroup(*[MathTex(f"{k+1}.\;\;", p, tex_template=myTemplate, font_size=44)
                         for k, p in enumerate(propiedades)])
        
        # dos columnas (suma: 4 filas; producto: 5 filas) sobre una misma rejilla de filas
        columna_suma     = VGroup(*lista[:4]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        columna_producto = VGroup(*lista[4:]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        cuadro = VGroup(columna_suma, columna_producto).arrange(RIGHT, buff=1.4, aligned_edge=UP)
        cuadro.next_to(sean, DOWN, buff=0.5).set_x(0)
        paso = 0.68
        y0 = lista[0].get_y()
        for k in range(4):
            lista[k].set_y(y0 - k*paso)
        for k in range(5):
            lista[4+k].set_y(y0 - k*paso)
        
        with self.voiceover(text=tr("""Resumamos. Las dos operaciones con números reales se pueden hacer con regla y compás, y cumplen estas propiedades.""",
                                    """Let us sum up. The two operations with real numbers can be carried out with ruler and compass, and they satisfy these properties.""")) as tracker:
            self.play(FadeIn(sean), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""De la suma: es conmutativa, es asociativa, el cero es el elemento neutro, y todo número tiene un opuesto.""",
                                    """For addition: it is commutative, it is associative, zero is the identity element, and every number has an opposite.""")) as tracker:
            for k in range(4):
                self.play(FadeIn(lista[k]), run_time=tracker.duration/4)
        
        with self.voiceover(text=tr("""Del producto: es conmutativo, es distributivo respecto de la suma, es asociativo, el uno es el elemento neutro, y todo número distinto de cero tiene un inverso.""",
                                    """For multiplication: it is commutative, it is distributive over addition, it is associative, one is the identity element, and every nonzero number has an inverse.""")) as tracker:
            for k in range(4, 9):
                self.play(FadeIn(lista[k]), run_time=tracker.duration/5)
        
        cita = VGroup(Tex(r"``Notation is everything''", font_size=46).set_color(COLOR_ESCALAR),
                      Tex("Charles F. Van Loan", font_size=34).set_color(GRAY_B)).arrange(DOWN, buff=0.25)
        cita.next_to(cuadro, DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""A partir de ahora no volveremos a la regla y el compás. Estas nueve reglas son todo lo que necesitamos para operar simbólicamente con números reales. Como dice Charles Van Loan: la notación lo es todo.""",
                                    """From now on we will not go back to ruler and compass. These nine rules are all we need to operate symbolically with real numbers. As Charles Van Loan says: notation is everything.""")) as tracker:
            self.pausa(tracker.duration/2)
            self.play(FadeIn(cita), run_time=tracker.duration/2)
        
        self.pausa(1.2)   # respiro tras la cita
        
        pregunta = Tex(tr(r"¿Cumplen estas propiedades las operaciones con \emph{vectores}?",
                          r"Do the operations with \emph{vectors} satisfy these properties?"),
                       tex_template=myTemplate, font_size=44).set_color(COLOR_ESCALAR).next_to(cuadro, DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""En el próximo vídeo plantearemos la misma cuestión para los vectores. Veremos si la suma de vectores y el producto por escalares cumplen estas mismas propiedades.""",
                                    """In the next video we will raise the same question for vectors. We will see whether the sum of vectors and the product by scalars satisfy these same properties.""")) as tracker:
            self.play(FadeOut(cita), run_time=1)
            self.play(Write(pregunta), run_time=2)
        
        self.pausa_media()

        self.play(*[FadeOut(mob) for mob in self.mobjects])  # borrado de todo

        copyright = Tex(r"\textcopyright{\;} 2026 \; Marcos Bujosa")
        github = Tex(r"\texttt{https://github.com/mbujosab}").next_to(copyright, DOWN)
        CGG  = VGroup(copyright, github).scale(1.1)
        self.add(CGG)
        self.wait(15)   # tiempo para las tarjetas de enlaces de YouTube


class L01_V05_E00_Portada(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        portada = Tex(TITULO, tex_template=myTemplate, font_size=60).set_color(COLOR_TITULO)
        portada.scale_to_fit_width(min(portada.width, config.frame_width*0.9))
        self.play(FadeIn(portada, shift=0.3*UP), run_time=1.5)
        self.wait(4.5)


class L01_V05_E01_Introduccion(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        titulo = Title(TITULO, tex_template=myTemplate, font_size=44).set_color(COLOR_TITULO)
        self.play(Write(titulo))
        
        # las dos definiciones (vídeos 3 y 4), con los glifos coloreados según el código de la serie
        f_suma = MathTex(r"\elemRp{\Vect{a}+\Vect{b}}{i}", "=", r"\eleVR{a}{i}+\eleVR{b}{i}",
                         tex_template=myTemplate, font_size=56).shift(0.9*UP)
        f_prod = MathTex(r"\elemRp{\lambda\Vect{a}}{i}", "=", r"\lambda\eleVRpE{a}{i}",
                         tex_template=myTemplate, font_size=56).shift(0.5*DOWN)
        for g in (f_suma[0][1], f_suma[2][0], f_prod[0][2], f_prod[2][2]):
            g.set_color(COLOR_A)
        for g in (f_suma[0][3], f_suma[2][4]):
            g.set_color(COLOR_B)
        for g in (f_prod[0][1], f_prod[2][0]):
            g.set_color(COLOR_ESCALAR)
        indices = [f_suma[0][6], f_suma[2][2], f_suma[2][6], f_prod[0][5], f_prod[2][4]]
        
        with self.voiceover(text=tr("""En los vídeos anteriores definimos dos operaciones con vectores: <bookmark mark='suma'/>la suma, <bookmark mark='producto'/>y el producto de un vector por un escalar. Las dos se calculan <bookmark mark='componentes'/>componente a componente, es decir, <bookmark mark='reales'/>sumando y multiplicando números reales.""",
                                    """In the previous videos we defined two operations with vectors: <bookmark mark='suma'/>the sum, <bookmark mark='producto'/>and the product of a vector by a scalar. Both are computed <bookmark mark='componentes'/>component-wise, that is, <bookmark mark='reales'/>by adding and multiplying real numbers.""")) as tracker:
            self.wait_until_bookmark("suma")
            self.play(FadeIn(f_suma), run_time=1)
            self.wait_until_bookmark("producto")
            self.play(FadeIn(f_prod), run_time=1)
            self.wait_until_bookmark("componentes")
            self.play(*[Indicate(g, color=COLOR_ESCALAR, scale_factor=1.8) for g in indices], run_time=1.5)
            self.wait_until_bookmark("reales")
            self.play(Circumscribe(f_suma[2], color=COLOR_ESCALAR, buff=0.15),
                      Circumscribe(f_prod[2], color=COLOR_ESCALAR, buff=0.15), run_time=2)
        
        with self.voiceover(text=tr("""El siguiente paso es estudiar las propiedades que tienen esas dos operaciones con vectores. Y para eso vamos a necesitar las propiedades algebraicas de los números reales. Seguro que las conoce desde la escuela.""",
                                    """The next step is to study the properties of those two operations with vectors. And for that we will need the algebraic properties of the real numbers. You surely know them from school.""")) as tracker:
            ocho = Tex(tr("Propiedades algebraicas de los números reales", "Algebraic properties of the real numbers"),
                       font_size=48).set_color(COLOR_REGLA)
            self.pausa(tracker.duration/3)
            self.play(FadeOut(f_suma, f_prod), FadeIn(ocho), run_time=tracker.duration/3)
        
        # recta con regla y compás
        recta = NumberLine(x_range=[-1, 7, 1], length=10, include_numbers=False).shift(1.2*DOWN)
        recta.add_numbers([0, 1], font_size=36)
        u = recta.n2p(1)[0] - recta.n2p(0)[0]
        pa = recta.n2p(2.6)
        punto_a = Dot(pa, color=COLOR_A, radius=0.1)
        etq_a = MathTex("a", color=COLOR_A, font_size=46).next_to(punto_a, UP, buff=0.25)
        arco = Arc(radius=2.6*u, start_angle=PI/2, angle=-PI/2, arc_center=recta.n2p(0),
                   color=GRAY_B, stroke_width=2)
        
        with self.voiceover(text=tr("""Pero ¿de dónde salen? En este vídeo vamos a verlas, no a demostrarlas. Y las veremos con regla y compás como hacían los geómetras griegos.""",
                                    """But where do they come from? In this video we are going to see them, not to prove them. And we will see them with ruler and compass as the Greek geometers did.""")) as tracker:
            self.pausa(tracker.duration/2)
            self.play(FadeOut(ocho), run_time=tracker.duration/4)
            self.play(Create(recta), run_time=tracker.duration/4)
        
        with self.voiceover(text=tr("""Para ello, un número real será un punto de una recta en la que hemos fijado el cero y el uno.""",
                                    """For that, a real number will be a point on a line on which we have fixed zero and one.""")) as tracker:
            self.play(Indicate(recta.numbers[0], color=COLOR_RESULTADO), Indicate(recta.numbers[1], color=COLOR_RESULTADO),
                      run_time=tracker.duration/3)
            self.play(Create(arco), run_time=tracker.duration/3)
            self.play(FadeIn(punto_a), FadeIn(etq_a), FadeOut(arco), run_time=tracker.duration/3)
        
        with self.voiceover(text=tr("""Veremos que las sumas y los productos de números reales se pueden construir con la regla y el compás, trasladando segmentos y trazando paralelas. Pero también, que dicha construcción es incómoda en la práctica. De tratar de evitar esa incomodidad nace la manera moderna de hacer matemáticas: operar con símbolos siguiendo unas pocas reglas.""",
                                    """We will see that sums and products of real numbers can be constructed with ruler and compass, by moving segments and drawing parallel lines. But also, that such a construction is cumbersome in practice. The modern way of doing mathematics was born from trying to avoid that inconvenience: operating with symbols by following a few rules.""")) as tracker:
            reglas = Tex(tr("regla y compás $\\;\\longrightarrow\\;$ reglas para manipular símbolos",
                            "ruler and compass $\\;\\longrightarrow\\;$ rules for manipulating symbols"),
                         font_size=40).set_color(COLOR_ESCALAR).next_to(recta, DOWN, buff=0.9)
            self.pausa(tracker.duration/2)
            self.play(Write(reglas), run_time=tracker.duration/2)
        
        self.pausa()


class L01_V05_E02_Suma(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("La suma, con regla y compás", "Addition, with ruler and compass"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        a, b, c = 2, 3, 1.5
        recta = NumberLine(x_range=[-4, 9, 1], length=12.5, include_numbers=False).shift(1.9*DOWN)
        recta.add_numbers([0, 1], font_size=36)
        u = recta.n2p(1)[0] - recta.n2p(0)[0]
        
        def altura(fila):
            return 1.2 + 0.55*fila
        
        def segmento(desde, hasta, color, fila=0):
            return Line(recta.n2p(desde) + altura(fila)*UP, recta.n2p(hasta) + altura(fila)*UP,
                        color=color, stroke_width=10)
        
        def rotulo(seg, texto, color):
            return MathTex(texto, color=color, font_size=42).next_to(seg, UP, buff=0.12)
        
        def compas(seg_origen, valor, desde, fila=0, run_time=1.5, antes=None, abatir=None):
            """Copia el segmento `seg_origen` (de longitud |valor|; su origen es el extremo
            `start`), marca el origen con un punto, levanta la copia en vertical sobre el
            origen, la traslada hasta poner el origen en el punto `desde` y la abate con el
            compás: en el sentido de las agujas del reloj si valor>0, en el contrario si
            valor<0 (el segmento queda orientado como estaba).
            Así se ve desde el principio que el segmento trasladado mide lo mismo y cuál de
            sus extremos es el origen. Devuelve la copia y un grupo con el arco y el punto
            del origen (para borrarlos después).
            Para que el movimiento acompañe a la voz, `antes` y `abatir` son marcas
            (<bookmark mark='x'/>) a las que se espera antes de levantar el segmento y antes
            de abatirlo; deben usarse dentro de un `with self.voiceover(...)`."""
            base = recta.n2p(desde) + altura(fila)*UP
            copia = seg_origen.copy()
            inicio = copia.get_start()
            origen = Dot(inicio, color=copia.get_color(), radius=0.11)
            movil = VGroup(copia, origen)
            hacia_derecha = copia.get_end()[0] > inicio[0]
            if antes is not None:
                self.wait_until_bookmark(antes)
            self.play(FadeIn(origen, scale=2), run_time=run_time/8)
            self.play(Rotate(movil, angle=PI/2 if hacia_derecha else -PI/2, about_point=inicio), run_time=run_time/4)
            self.play(movil.animate.shift(base - inicio), run_time=run_time/4)
            if abatir is not None:
                self.wait_until_bookmark(abatir)
            angulo = -PI/2 if valor > 0 else PI/2
            arco = Arc(radius=abs(valor)*u, start_angle=PI/2, angle=angulo, arc_center=base,
                       color=GRAY_B, stroke_width=1.5)
            self.play(Rotate(movil, angle=angulo, about_point=base), Create(arco), run_time=3*run_time/8)
            return copia, VGroup(arco, origen)
        
        def marca(valor, texto, color=COLOR_RESULTADO):
            punto = Dot(recta.n2p(valor), color=color, radius=0.09)
            etq = MathTex(texto, color=color, font_size=42).next_to(punto, DOWN, buff=0.45)
            return VGroup(punto, etq)
        
        def regla(texto):
            return MathTex(texto, font_size=52, color=COLOR_REGLA).next_to(cabecera, DOWN, buff=0.5)
        
        seg_a = segmento(0, a, COLOR_A)
        etq_a = rotulo(seg_a, "a", COLOR_A)
        origen_a = Dot(seg_a.get_start(), color=COLOR_A, radius=0.11)
        
        with self.voiceover(text=tr("""Empecemos por la suma. Fijados el cero y el uno, tomemos un número a. Es un punto de la recta. Pero también podemos verlo como un segmento: <bookmark mark='origen'/>su origen está siempre en el cero, <bookmark mark='extremo'/>y su otro extremo es el número a.""",
                                    """Let us start with addition. Once zero and one are fixed, a number 'a' is a point on the line. But we can also see it as a segment: <bookmark mark='origen'/>its origin is always at zero, <bookmark mark='extremo'/>and its other end is the number 'a'.""")) as tracker:
            self.play(Create(recta), run_time=1.5)
            self.play(FadeIn(marca(a, "a", COLOR_A)[0]), run_time=0.6)
            self.wait_until_bookmark("origen")
            self.play(FadeIn(origen_a, scale=2), Indicate(recta.numbers[0], color=COLOR_RESULTADO), run_time=1)
            self.wait_until_bookmark("extremo")
            self.play(Create(seg_a), FadeIn(etq_a), run_time=1.2)
            self.play(FadeOut(origen_a), run_time=0.4)
        
        seg_b = segmento(0, b, COLOR_B, fila=1)
        etq_b = rotulo(seg_b, "b", COLOR_B)
        regla1 = regla("a+b=b+a")
        
        with self.voiceover(text=tr("""Y aquí tenemos otro número, b: otro segmento con el origen en el cero.""",
                                    """And here we have another number, b: another segment with its origin at zero.""")) as tracker:
            self.play(Create(seg_b), FadeIn(etq_b), run_time=tracker.duration)
        
        with self.voiceover(text=tr("""Para sumar 'a' y b, <bookmark mark='traslada'/>trasladamos el segmento b, <bookmark mark='origen'/>y ponemos su origen en el extremo de 'a'. Eso es justo lo que hace un compás: toma una longitud y la lleva a otro sitio.""",
                                    """To add the two numbers, <bookmark mark='traslada'/>we move the second segment, 'b', <bookmark mark='origen'/>and place its origin at the end of the first, 'a'. That is exactly what a compass does: it takes a length and carries it somewhere else.<bookmark mark='v1'/>""")) as tracker:
            self.anuncia_regla(regla1, run_time=0.8)
            seg_b_tras, arco1 = compas(seg_b, b, a, fila=0, run_time=2.4, antes="traslada", abatir="origen")
            etq_b_tras = rotulo(seg_b_tras, "b", COLOR_B)
            self.add(etq_b_tras)
        
        # la suma es un nuevo segmento con origen en el cero (en blanco, debajo de los dos sumandos)
        marca_ab = marca(a + b, "a+b")
        seg_ab = segmento(0, a + b, COLOR_RESULTADO, fila=-1).set_stroke(width=6)
        with self.voiceover(text=tr("""El extremo del segmento trasladado es la suma, 'a' más b. <bookmark mark='nuevo'/>Es decir, la suma es un nuevo segmento: con el origen en el cero, como siempre, y con el otro extremo en 'a' más b.""",
                                    """The end of the moved segment is the sum, 'a' plus 'b'. <bookmark mark='nuevo'/>That is, the sum is a new segment: with its origin at zero, as always, and with its other end at the sum.""")) as tracker:
            self.play(FadeIn(marca_ab), run_time=0.8)
            self.wait_until_bookmark("nuevo")
            self.play(Create(seg_ab), run_time=1.5)
        
        with self.voiceover(text=tr("""Hagámoslo ahora en el otro orden: partimos de b <bookmark mark='traslada'/>y ponemos el origen de a en el extremo de b.""",
                                    """Let us now do it in the other order: we start from 'b' <bookmark mark='traslada'/>and place the origin of 'a' at the end of b.""")) as tracker:
            seg_a_tras, arco2 = compas(seg_a, a, b, fila=1, run_time=2.4, antes="traslada")
            etq_a_tras = rotulo(seg_a_tras, "a", COLOR_A)
            self.add(etq_a_tras)
        
        linea = DashedLine(recta.n2p(a + b) + 0.1*UP, recta.n2p(a + b) + altura(1.6)*UP, color=COLOR_RESULTADO)
        with self.voiceover(text=tr("""Llegamos exactamente al mismo punto. Es la propiedad conmutativa de la suma.""",
                                    """We arrive at exactly the same point. This is the commutative property of addition.""")) as tracker:
            self.play(Create(linea), FadeOut(arco1, arco2), run_time=tracker.duration/3)
            self.destaca_regla(regla1)
        
        self.play(FadeOut(seg_b, etq_b, seg_b_tras, etq_b_tras, seg_a_tras, etq_a_tras, linea, marca_ab, seg_ab))
        
        # asociativa: las dos agrupaciones se construyen en el orden en que se enuncian.
        # (a+b)+c en la fila 0; a+(b+c) en la fila 1, con b+c construido antes en la fila 2.
        seg_b2 = segmento(0, b, COLOR_B, fila=2)
        seg_c3 = segmento(0, c, COLOR_C, fila=3)
        etq_b2, etq_c3 = rotulo(seg_b2, "b", COLOR_B), rotulo(seg_c3, "c", COLOR_C)
        regla2 = regla("a+(b+c)=(a+b)+c")
        self.anuncia_regla(regla2, regla1)
        self.play(FadeIn(seg_b2, etq_b2, seg_c3, etq_c3))
        
        with self.voiceover(text=tr("""Con tres números podemos agrupar de dos maneras. <bookmark mark='ab'/>Primero 'a' más b, poniendo el origen de b en el extremo de 'a'. <bookmark mark='c'/>Y después sumar c.""",
                                    """With three numbers we can group in two ways. <bookmark mark='ab'/>First 'a' plus b, placing the origin of b at the end of 'a'. <bookmark mark='c'/>And then add c.""")) as tracker:
            self.wait_until_bookmark("ab")
            seg_b0, arco1 = compas(seg_b2, b, a, fila=0, run_time=1.6)
            etq_b0 = rotulo(seg_b0, "b", COLOR_B)
            self.add(etq_b0)
            llave1 = Brace(VGroup(seg_a, seg_b0), DOWN, buff=0.1, color=GRAY_B)
            etq_llave1 = llave1.get_tex("a+b").set_color(GRAY_B)
            self.play(GrowFromCenter(llave1), FadeIn(etq_llave1), FadeOut(arco1), run_time=0.8)
            self.wait_until_bookmark("c")
            seg_c0, arco2 = compas(seg_c3, c, a + b, fila=0, run_time=1.6)
            etq_c0 = rotulo(seg_c0, "c", COLOR_C)
            self.add(etq_c0)
            self.play(FadeOut(arco2), run_time=0.4)
        
        seg_a1 = segmento(0, a, COLOR_A, fila=1)
        etq_a1 = rotulo(seg_a1, "a", COLOR_A)
        with self.voiceover(text=tr("""O primero b más c, poniendo el origen de c en el extremo de b. <bookmark mark='a'/>Y después sumárselo al número a.""",
                                    """Or first b plus c, placing the origin of c at the end of b. <bookmark mark='a'/>And then add it to the number 'a'.""")) as tracker:
            seg_c2, arco3 = compas(seg_c3, c, b, fila=2, run_time=1.6)
            etq_c2 = rotulo(seg_c2, "c", COLOR_C)
            self.add(etq_c2)
            grupo_bc = VGroup(seg_b2, etq_b2, seg_c2, etq_c2)
            llave2 = Brace(grupo_bc, UP, buff=0.1, color=GRAY_B)
            etq_llave2 = llave2.get_tex("b+c").set_color(GRAY_B)
            self.play(FadeOut(arco3, seg_c3, etq_c3), run_time=0.4)
            self.play(GrowFromCenter(llave2), FadeIn(etq_llave2), run_time=0.8)
            grupo_bc.add(llave2, etq_llave2)
            self.wait_until_bookmark("a")
            self.play(FadeIn(seg_a1, etq_a1), run_time=0.6)
            # el segmento b+c, ya construido, se traslada en bloque hasta el extremo de a
            self.play(grupo_bc.animate.shift(recta.n2p(a) - recta.n2p(0) + (altura(1) - altura(2))*UP), run_time=1.5)
        
        marca_abc = marca(a + b + c, "a+b+c")
        with self.voiceover(text=tr("""El punto final es el mismo. Es la propiedad asociativa.""",
                                    """The end point is the same. This is the associative property.""")) as tracker:
            self.play(FadeIn(marca_abc), run_time=tracker.duration/3)
            self.destaca_regla(regla2)
        
        self.play(FadeOut(seg_b0, etq_b0, seg_c0, etq_c0, seg_a1, etq_a1, grupo_bc, llave1, etq_llave1, marca_abc))
        
        # cero: un segmento de longitud cero (un punto) con el origen en el cero, que se traslada como los demás
        cero = Dot(recta.n2p(0) + altura(1)*UP, color=COLOR_B, radius=0.12)
        regla3 = regla("a+0=a")
        with self.voiceover(text=tr("""Sumar cero es sumar un segmento de longitud cero: <bookmark mark='punto'/>un punto, con el origen en el cero. <bookmark mark='traslada'/>Lo ponemos en el extremo de a, <bookmark mark='quietos'/>y no nos movemos de a. <bookmark mark='neutro'/>El cero es el elemento neutro de la suma.""",
                                    """Adding zero means adding a segment of length zero: <bookmark mark='punto'/>a point, with its origin at zero. <bookmark mark='traslada'/>We place it at the end of a, <bookmark mark='quietos'/>and we do not move away from 'a'. <bookmark mark='neutro'/>Zero is the identity element for addition.""")) as tracker:
            self.anuncia_regla(regla3, regla2, run_time=0.8)
            self.wait_until_bookmark("punto")
            self.play(FadeIn(cero, scale=3), run_time=0.8)
            self.wait_until_bookmark("traslada")
            self.play(cero.animate.move_to(recta.n2p(a) + altura(0)*UP), run_time=1.5)
            self.wait_until_bookmark("quietos")
            self.play(Flash(cero, color=COLOR_RESULTADO), run_time=0.8)
            self.wait_until_bookmark("neutro")
            self.destaca_regla(regla3)
            self.play(FadeOut(cero), run_time=0.5)
        
        self.pausa(1.2)   # respiro antes de cambiar de propiedad (1,5 s resultaba largo)
        
        # opuesto: el mismo segmento abatido al lado contrario del cero (origen en el cero; si a>0 el extremo queda a la izquierda)
        regla4 = regla("a+(-a)=0")
        with self.voiceover(text=tr("""Todo número tiene un opuesto. Para construir el opuesto de a, <bookmark mark='compas'/>ponemos el compás en el cero <bookmark mark='abatimos'/>y abatimos el segmento hacia el lado contrario. <bookmark mark='obtenemos'/>Obtenemos menos a, un segmento con el origen en el cero, como todos, pero que se extiende hacia el otro lado.""",
                                    """Every number has an opposite. To construct the opposite of 'a', <bookmark mark='compas'/>we put the compass at zero <bookmark mark='abatimos'/>and swing the segment to the opposite side. <bookmark mark='obtenemos'/>We get minus a: a segment with its origin at zero, like all of them, but extending to the other side.""")) as tracker:
            self.anuncia_regla(regla4, regla3, run_time=0.8)
            seg_ma, arco1 = compas(seg_a, -a, 0, fila=0, run_time=2.4, antes="compas", abatir="abatimos")
            seg_ma.set_opacity(0.6)
            self.wait_until_bookmark("obtenemos")
            marca_ma = marca(-a, "-a", COLOR_A)
            self.play(FadeIn(marca_ma), FadeOut(arco1[0]), run_time=0.8)   # el punto del origen (arco1[1]) se queda en el cero
        
        with self.voiceover(text=tr("""Sumemos ahora 'a' y su opuesto con la regla de siempre: <bookmark mark='traslada'/>trasladamos el segmento opuesto, y ponemos su origen en el extremo de 'a'. <bookmark mark='cae'/>Su otro extremo cae justo en el cero. <bookmark mark='regla'/>'a', más su opuesto es cero.""",
                                    """Now let us add 'a' and its opposite with the usual rule: <bookmark mark='traslada'/>we move the opposite segment, and place its origin at the end of a. <bookmark mark='cae'/>Its other end lands exactly at zero. <bookmark mark='regla'/>'a' plus its opposite is zero.""")) as tracker:
            seg_ma1, arco2 = compas(seg_ma, -a, a, fila=1, run_time=2.4, antes="traslada", abatir="cae")
            punto_0 = Dot(recta.n2p(0), color=COLOR_RESULTADO, radius=0.09)
            linea0 = DashedLine(recta.n2p(0) + 0.1*UP, recta.n2p(0) + altura(1.6)*UP, color=COLOR_RESULTADO)
            self.play(Create(linea0), FadeIn(punto_0), Indicate(recta.numbers[0], color=COLOR_RESULTADO), FadeOut(arco2), run_time=0.8)
            self.wait_until_bookmark("regla")
            self.destaca_regla(regla4)
        
        with self.voiceover(text=tr("""Acabamos de ver cuatro propiedades de la suma. Y las cuatro se ven en la recta con una sola regla: poner el origen de un segmento en el extremo del otro.""",
                                    """We have just seen four properties of addition. And all four can be seen on the line with a single rule: placing the origin of one segment at the end of the other.""")) as tracker:
            self.pausa(tracker.duration)
        
        self.pausa()


class L01_V05_E03_Producto(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("El producto, con regla y compás", "Multiplication, with ruler and compass"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        a, b, c = 2, 1.5, 2
        ax = Axes(x_range=[-0.5, 8.5, 1], y_range=[-0.5, 4.2, 1], x_length=10, y_length=10*4.7/9,
                  tips=False, axis_config={"include_ticks": True})
        ax.shift(np.array([-4.8, -2.45, 0]) - ax.c2p(0, 0))   # origen abajo a la izquierda
        O = ax.c2p(0, 0)
        ux = ax.c2p(1, 0)[0] - O[0]
        
        def recta_por(p, q, color=GRAY_B, ext=1.25):
            return Line(ax.c2p(*p), ax.c2p(*q), color=color, stroke_width=2.5).scale(ext)
        
        def marca_x(valor, texto, color=COLOR_RESULTADO, buff=0.35):
            punto = Dot(ax.c2p(valor, 0), color=color, radius=0.09)
            etq = MathTex(texto, color=color, font_size=42).next_to(punto, DOWN, buff=buff)
            return VGroup(punto, etq)
        
        def marca_y(valor, texto, color=COLOR_RESULTADO):
            punto = Dot(ax.c2p(0, valor), color=color, radius=0.09)
            etq = MathTex(texto, color=color, font_size=42).next_to(punto, LEFT, buff=0.3)
            return VGroup(punto, etq)
        
        def seg_x(desde, hasta, color, altura=0.0):
            return Line(ax.c2p(desde, 0) + altura*UP, ax.c2p(hasta, 0) + altura*UP, color=color, stroke_width=10)
        
        def seg_y(desde, hasta, color):
            return Line(ax.c2p(0, desde), ax.c2p(0, hasta), color=color, stroke_width=10)
        
        def regla(texto):
            return MathTex(texto, font_size=52, color=COLOR_REGLA).next_to(cabecera, DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""Pasemos al producto. En el vídeo anterior vimos una construcción geométrica que multiplica dos números. Recordémosla.""",
                                    """Let us move on to multiplication. In the previous video we saw a geometric construction that multiplies two numbers. Let us recall it.""")) as tracker:
            self.play(Create(ax), run_time=tracker.duration/2)
        
        m_a, m_b, m_1 = marca_x(a, "a", COLOR_A), marca_y(b, "b", COLOR_B), marca_y(1, "1")
        with self.voiceover(text=tr("""Ponemos 'a' en el eje horizontal y b en el eje vertical.""",
                                    """We place a on the horizontal axis and 'b' on the vertical axis.""")) as tracker:
            self.play(FadeIn(m_a), run_time=tracker.duration/2)
            self.play(FadeIn(m_b), run_time=tracker.duration/2)
        
        diagonal = recta_por((a, 0), (0, 1))
        with self.voiceover(text=tr("""Trazamos la recta que une el punto 'a' del eje horizontal con el punto uno del eje vertical.""",
                                    """We draw the line joining point a on the horizontal axis with point one on the vertical axis.""")) as tracker:
            self.play(FadeIn(m_1), run_time=tracker.duration/4)
            self.play(Create(diagonal), run_time=tracker.duration/2)
        
        paralela_b = recta_por((a*b, 0), (0, b), color=COLOR_B)
        with self.voiceover(text=tr("""Y trazamos la paralela que pasa por b. <break time="600ms"/> Dibujar una paralela es una construcción clásica con regla y compás.""",
                                    """And we draw the parallel line through 'b'. <break time="600ms"/> Drawing a parallel is a classical ruler and compass construction.""")) as tracker:
            self.play(TransformFromCopy(diagonal, paralela_b), run_time=tracker.duration*0.6)
        
        m_ab = marca_x(a*b, "ab")
        with self.voiceover(text=tr("""Donde esa paralela corta al eje horizontal está el producto a por b.""",
                                    """Where that parallel meets the horizontal axis is the product 'a' times 'b'.""")) as tracker:
            self.play(FadeIn(m_ab, scale=2), run_time=tracker.duration/2)
        
        # la construcción como homotecia
        t = ValueTracker(b)
        paralela_t = always_redraw(lambda: recta_por((a*t.get_value(), 0), (0, t.get_value()), color=COLOR_ESCALAR))
        punto_t = always_redraw(lambda: Dot(ax.c2p(a*t.get_value(), 0), color=COLOR_ESCALAR, radius=0.09))
        punto_ty = always_redraw(lambda: Dot(ax.c2p(0, t.get_value()), color=COLOR_ESCALAR, radius=0.09))
        with self.voiceover(text=tr("""Fíjese en lo que hace esta figura: a cada número del eje vertical le asigna un número del eje horizontal, su producto por a. Si subimos por el eje vertical, el resultado se aleja proporcionalmente.""",
                                    """Notice what this figure does: to each number on the vertical axis it assigns a number on the horizontal axis, its product by 'a'. As we go up the vertical axis, the result moves away proportionally.""")) as tracker:
            self.add(paralela_t, punto_t, punto_ty)
            self.play(t.animate.set_value(2.8), run_time=tracker.duration*0.4, rate_func=there_and_back)
            self.play(t.animate.set_value(0.4), run_time=tracker.duration*0.4, rate_func=there_and_back)
        
        regla1 = regla("1a=a")
        with self.voiceover(text=tr("""Si tomamos el uno, la paralela es la propia recta inicial, y el resultado es a. Uno por 'a' es 'a': el uno es el elemento neutro del producto.""",
                                    """If we take one, the parallel line is the initial line itself, and the result is 'a'. One times a is 'a': one is the identity element for multiplication.""")) as tracker:
            self.anuncia_regla(regla1, run_time=0.8)
            self.play(t.animate.set_value(1), run_time=tracker.duration/3)
            self.play(Indicate(m_a, color=COLOR_RESULTADO), run_time=tracker.duration/4)
            self.destaca_regla(regla1)
        
        # inverso: la paralela que corta al eje horizontal en el uno
        regla_inv = regla(r"a\,a^{-1}=1")
        m_1x = marca_x(1, "1")
        m_inv = marca_y(1/a, "a^{-1}", COLOR_A)
        with self.voiceover(text=tr("""Hay otra propiedad del producto: todo número distinto de cero tiene un inverso, un número que multiplicado por él da uno. <bookmark mark='mueve'/>Para construirlo, movemos la paralela hasta que corte al eje horizontal justo en el uno. <bookmark mark='inverso'/>Donde esa paralela corta al eje vertical está el inverso de a.""",
                                    """There is another property of multiplication: every nonzero number has an inverse, a number which multiplied by it gives one. <bookmark mark='mueve'/>To construct it, we move the parallel line until it meets the horizontal axis exactly at one. <bookmark mark='inverso'/>Where that parallel meets the vertical axis is the inverse of 'a'.""")) as tracker:
            self.anuncia_regla(regla_inv, regla1, run_time=0.8)
            self.wait_until_bookmark("mueve")
            self.play(FadeIn(m_1x, scale=2), run_time=0.6)
            self.play(t.animate.set_value(1/a), run_time=2)
            self.wait_until_bookmark("inverso")
            self.play(FadeIn(m_inv, scale=2), run_time=0.8)
            self.destaca_regla(regla_inv)
            self.remove(paralela_t, punto_t, punto_ty)
            self.play(FadeOut(m_1x, m_inv), run_time=0.5)
        
        self.pausa(1.2)   # respiro antes de cambiar de propiedad
        
        # distributiva
        regla2 = regla("a(b+c)=ab+ac")
        seg_b_y = seg_y(0, b, COLOR_B)
        seg_c_y = seg_y(b, b + c, COLOR_C)
        m_bc = marca_y(b + c, "b+c", COLOR_C)
        with self.voiceover(text=tr("""Ahora sumemos otro número c a b, trasladándolo con el compás sobre el eje vertical, encima de b.""",
                                    """Now let us add a third number, c, to b, moving it with the compass along the vertical axis, on top of 'b'.""")) as tracker:
            self.anuncia_regla(regla2, regla_inv, run_time=0.8)
            self.play(Create(seg_b_y), run_time=tracker.duration/4)
            self.play(Create(seg_c_y), FadeIn(m_bc), run_time=tracker.duration/2)
        
        paralela_bc = recta_por((a*(b + c), 0), (0, b + c), color=COLOR_C)
        m_abc = marca_x(a*(b + c), "a(b+c)")
        with self.voiceover(text=tr("""La paralela que pasa por 'b más c' nos da el producto 'a' por 'b más c'.""",
                                    """The parallel through b plus c gives us the product 'a' times b plus c.""")) as tracker:
            self.play(TransformFromCopy(diagonal, paralela_bc), run_time=tracker.duration/2)
            self.play(FadeIn(m_abc, scale=2), run_time=tracker.duration/4)
        
        seg_ab_x = seg_x(0, a*b, COLOR_B, altura=0.18)
        seg_ac_x = seg_x(a*b, a*(b + c), COLOR_C, altura=0.18)
        with self.voiceover(text=tr("""En el eje horizontal, <bookmark mark='s1'/>entre cero y 'a' por 'b', está el segmento 'a' 'b'. <bookmark mark='s2'/>Y entre 'a' por b y 'a' por 'b más c' queda otro segmento.""",
                                    """On the horizontal axis, <bookmark mark='s1'/>between zero and ab lies the segment 'a' times 'b'. <bookmark mark='s2'/>And between 'a' times b and 'a' times b plus c there is another segment.""")) as tracker:
            self.wait_until_bookmark("s1")
            self.play(Create(seg_ab_x), run_time=1)
            self.play(Indicate(seg_ab_x, color=COLOR_RESULTADO, scale_factor=1.05), run_time=1)
            self.wait_until_bookmark("s2")
            self.play(Create(seg_ac_x), run_time=1)
            self.play(Indicate(seg_ac_x, color=COLOR_RESULTADO, scale_factor=1.05), run_time=1)
        
        paralela_c = recta_por((a*c, 0), (0, c), color=COLOR_C).set_opacity(0.6)
        m_c = marca_y(c, "c", COLOR_C)
        m_ac = marca_x(a*c, "ac", COLOR_C, buff=0.8)
        with self.voiceover(text=tr("""¿Cuánto mide ese segmento? <bookmark mark='aparte'/>Construyamos aparte el producto a por c, con la paralela que pasa por c.""",
                                    """How long is that segment? <bookmark mark='aparte'/>Let us construct separately the product 'a' times c, with the parallel through 'c'.""")) as tracker:
            self.play(Indicate(seg_ac_x, color=COLOR_RESULTADO, scale_factor=1.05), run_time=1.2)
            self.wait_until_bookmark("aparte")
            self.play(FadeIn(m_c), run_time=tracker.duration/4)
            self.play(TransformFromCopy(diagonal, paralela_c), run_time=tracker.duration/3)
            self.play(FadeIn(m_ac, scale=2), run_time=tracker.duration/4)
        
        # el compás, como en la escena 2: la copia (en blanco) se levanta sobre su extremo izquierdo,
        # se lleva al origen y se abate hacia la derecha, en el sentido de las agujas del reloj
        copia = seg_ac_x.copy().set_color(COLOR_RESULTADO)
        with self.voiceover(text=tr("""Y traslademos el segmento con el compás hasta el origen. <bookmark mark='coincide'/>Coincide exactamente con a por c.""",
                                    """And let us move the segment with the compass to the origin. <bookmark mark='coincide'/>It coincides exactly with 'a' times c.<bookmark mark='v1'/>""")) as tracker:
            inicio = copia.get_start()
            origen = O + 0.18*UP
            self.play(Rotate(copia, angle=PI/2, about_point=inicio), run_time=0.7)
            self.play(copia.animate.shift(origen - inicio), run_time=0.7)
            arco = Arc(radius=a*c*ux, start_angle=PI/2, angle=-PI/2, arc_center=origen, color=GRAY_B, stroke_width=1.5)
            self.play(Rotate(copia, angle=-PI/2, about_point=origen), Create(arco), run_time=1.2)
            self.wait_until_bookmark("coincide")
            self.play(FadeOut(arco), Indicate(m_ac, color=COLOR_RESULTADO), run_time=1)
        
        # cada segmento vertical "viaja" hasta su imagen en el eje horizontal; después, las dos sumas
        with self.voiceover(text=tr("""No es casualidad: <bookmark mark='traslada'/>la figura traslada los segmentos del eje vertical al horizontal agrandándolos todos en la misma proporción. <bookmark mark='sumav'/>Por eso una suma en el eje vertical <bookmark mark='sumah'/>se convierte en una suma en el horizontal. <bookmark mark='distributiva'/>Es la propiedad distributiva.""",
                                    """This is no coincidence: <bookmark mark='traslada'/>the figure carries the segments from the vertical axis to the horizontal one, enlarging them all in the same proportion. <bookmark mark='sumav'/>That is why a sum on the vertical axis <bookmark mark='sumah'/>becomes a sum on the horizontal axis. <bookmark mark='distributiva'/>This is the distributive property.""")) as tracker:
            self.play(FadeOut(copia), run_time=0.5)
            self.wait_until_bookmark("traslada")
            viaje_b, viaje_c = seg_b_y.copy(), seg_c_y.copy()
            self.play(Transform(viaje_b, seg_ab_x), run_time=1.3)
            self.play(Transform(viaje_c, seg_ac_x), run_time=1.3)
            self.remove(viaje_b, viaje_c)
            # "una suma": los dos sumandos se apartan y se separan un instante, y vuelven a encajar uno a continuación del otro
            self.wait_until_bookmark("sumav")
            cb, cc = seg_b_y.copy(), seg_c_y.copy()
            self.play(cb.animate.shift(0.9*LEFT), cc.animate.shift(0.9*LEFT + 0.5*UP), run_time=0.6)
            self.play(cb.animate.shift(0.9*RIGHT), cc.animate.shift(0.9*RIGHT + 0.5*DOWN), run_time=0.7)
            self.play(Indicate(m_bc, color=COLOR_RESULTADO), run_time=0.6)
            self.remove(cb, cc)
            self.wait_until_bookmark("sumah")
            cab, cac = seg_ab_x.copy(), seg_ac_x.copy()
            self.play(cab.animate.shift(0.8*UP + 0.4*LEFT), cac.animate.shift(0.8*UP + 0.4*RIGHT), run_time=0.6)
            self.play(cab.animate.shift(0.8*DOWN + 0.4*RIGHT), cac.animate.shift(0.8*DOWN + 0.4*LEFT), run_time=0.7)
            self.play(Indicate(m_abc, color=COLOR_RESULTADO), run_time=0.6)
            self.remove(cab, cac)
            self.wait_until_bookmark("distributiva")
            self.destaca_regla(regla2)
        
        self.pausa()


class L01_V05_E04_ProductoIncomodo(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Dos propiedades incómodas", "Two uncomfortable properties"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        a, b, c = 2, 1.5, 2.5
        ax = Axes(x_range=[-0.5, 8.5, 1], y_range=[-0.5, 4.2, 1], x_length=10, y_length=10*4.7/9,
                  tips=False, axis_config={"include_ticks": True})
        ax.shift(np.array([-4.8, -2.45, 0]) - ax.c2p(0, 0))   # origen abajo a la izquierda
        O = ax.c2p(0, 0)
        ux = ax.c2p(1, 0)[0] - O[0]
        
        def recta_por(p, q, color=GRAY_B, ext=1.25):
            return Line(ax.c2p(*p), ax.c2p(*q), color=color, stroke_width=2.5).scale(ext)
        
        def marca_x(valor, texto, color=COLOR_RESULTADO, buff=0.35):
            punto = Dot(ax.c2p(valor, 0), color=color, radius=0.09)
            etq = MathTex(texto, color=color, font_size=42).next_to(punto, DOWN, buff=buff)
            return VGroup(punto, etq)
        
        def marca_y(valor, texto, color=COLOR_RESULTADO):
            punto = Dot(ax.c2p(0, valor), color=color, radius=0.09)
            etq = MathTex(texto, color=color, font_size=42).next_to(punto, LEFT, buff=0.3)
            return VGroup(punto, etq)
        
        def arco_x_a_y(valor, color):
            """Arco de compás, centrado en el origen, que lleva el punto (valor,0) a (0,valor)."""
            return Arc(radius=valor*ux, start_angle=0, angle=PI/2, arc_center=O, color=color, stroke_width=1.5)
        
        def regla(texto):
            return MathTex(texto, font_size=52, color=COLOR_REGLA).next_to(cabecera, DOWN, buff=0.5)
        
        def multiplica(x, y, color, velocidad=1.0):
            """Construye x·y: recta por (x,0),(0,1) y paralela por (0,y). Devuelve los objetos creados."""
            d = recta_por((x, 0), (0, 1))
            p = recta_por((x*y, 0), (0, y), color=color)
            self.play(Create(d), run_time=0.8*velocidad)
            self.play(TransformFromCopy(d, p), run_time=0.8*velocidad)
            return VGroup(d, p)
        
        self.play(Create(ax), run_time=1)
        m_a, m_b, m_1 = marca_x(a, "a", COLOR_A), marca_y(b, "b", COLOR_B), marca_y(1, "1")
        self.play(FadeIn(m_a, m_b, m_1), run_time=0.8)
        regla1 = regla("ab=ba")
        regla2 = regla("a(bc)=(ab)c")
        
        with self.voiceover(text=tr("""¿Y la conmutativa? a por b igual a b por a. Nuestra construcción pone 'a' en el eje horizontal y b en el vertical, y nos da a por b.""",
                                    """What about commutativity? 'a' times b equals b times a. Our construction puts a on the horizontal axis and b on the vertical one, and gives us the product 'a' times b.<bookmark mark='v1'/>""")) as tracker:
            self.anuncia_regla(regla1, run_time=0.8)
            rectas_ab = multiplica(a, b, COLOR_B, velocidad=tracker.duration/4)
            m_ab = marca_x(a*b, "ab")
            self.play(FadeIn(m_ab, scale=2), run_time=tracker.duration/5)
        
        with self.voiceover(text=tr("""Para calcular b por a necesitamos intercambiar los papeles: llevamos b al eje horizontal y a al eje vertical, con dos arcos de compás.""",
                                    """To compute b times 'a' we have to swap the roles: we carry b to the horizontal axis and a to the vertical one, with two compass arcs.<bookmark mark='v1'/>""")) as tracker:
            self.play(rectas_ab.animate.set_stroke(opacity=0.35), run_time=tracker.duration/6)
            arco_b, arco_a = arco_x_a_y(b, COLOR_B), arco_x_a_y(a, COLOR_A)
            m_b_x, m_a_y = marca_x(b, "b", COLOR_B, buff=0.8), marca_y(a, "a", COLOR_A)
            self.play(Create(arco_b), FadeIn(m_b_x), run_time=tracker.duration/3)
            self.play(Create(arco_a), FadeIn(m_a_y), run_time=tracker.duration/3)
        
        with self.voiceover(text=tr("""Y repetimos la construcción: la recta por b y por uno, y su paralela por a.""",
                                    """And we repeat the construction: the line through 'b' and one, and its parallel through the point a.""")) as tracker:
            rectas_ba = multiplica(b, a, COLOR_A, velocidad=tracker.duration/3)
        
        with self.voiceover(text=tr("""Son dos construcciones distintas, <bookmark mark='mismo'/>y acaban en el mismo punto. <bookmark mark='regla'/>Que coincidan no es casualidad, pero tampoco es evidente: para justificarlo hacen falta triángulos semejantes.""",
                                    """They are two different constructions, <bookmark mark='mismo'/>and they end at the same point. <bookmark mark='regla'/>That they coincide is no coincidence, but it is not obvious either: to justify it one needs similar triangles.""")) as tracker:
            self.wait_until_bookmark("mismo")
            self.play(Indicate(m_ab, color=COLOR_RESULTADO, scale_factor=1.6), run_time=1)
            self.wait_until_bookmark("regla")
            self.destaca_regla(regla1)
        
        self.play(FadeOut(rectas_ab, rectas_ba, arco_a, arco_b, m_b_x, m_a_y, m_ab, m_b), run_time=0.8)
        
        # asociativa
        with self.voiceover(text=tr("""La asociativa es peor: a por, b por c, frente a, a por b, por c. Hay que multiplicar dos veces, y entre medias llevar el resultado del eje horizontal al vertical con el compás.""",
                                    """Associativity is worse: the number 'a' times the product b times c, versus the product 'a' times b, times c. We must multiply twice, and in between carry the result from the horizontal axis to the vertical one with the compass.""")) as tracker:
            self.anuncia_regla(regla2, regla1, run_time=0.8)
            m_c, m_b_x = marca_y(c, "c", COLOR_C), marca_x(b, "b", COLOR_B, buff=0.8)
            self.play(FadeIn(m_c, m_b_x), run_time=tracker.duration/5)
            r1 = multiplica(b, c, COLOR_C, velocidad=tracker.duration/8)
            m_bc = marca_x(b*c, "bc", COLOR_C, buff=0.8)
            self.play(FadeIn(m_bc), run_time=tracker.duration/10)
            arco1 = arco_x_a_y(b*c, COLOR_C)
            m_bc_y = marca_y(b*c, "bc", COLOR_C)
            self.play(Create(arco1), FadeIn(m_bc_y), run_time=tracker.duration/5)
            r2 = multiplica(a, b*c, COLOR_C, velocidad=tracker.duration/8)
            m_abc = marca_x(a*b*c, "a(bc)", COLOR_C)
            self.play(FadeIn(m_abc, scale=2), run_time=tracker.duration/10)
        
        with self.voiceover(text=tr("""Y por el otro camino: a por b, lo llevamos al eje vertical, y lo multiplicamos por c.""",
                                    """And the other way round: we compute the product 'a' times 'b', carry it to the vertical axis, and multiply it by c.""")) as tracker:
            self.play(VGroup(r1, r2, arco1).animate.set_stroke(opacity=0.3), run_time=tracker.duration/8)
            r3 = multiplica(a, b, COLOR_B, velocidad=tracker.duration/8)
            m_ab = marca_x(a*b, "ab", COLOR_B)
            self.play(FadeIn(m_ab), run_time=tracker.duration/10)
            arco2 = arco_x_a_y(a*b, COLOR_B)
            m_ab_y = marca_y(a*b, "ab", COLOR_B)
            self.play(Create(arco2), FadeIn(m_ab_y), run_time=tracker.duration/5)
            m_c_x = marca_x(c, "c", COLOR_C, buff=0.8)
            self.play(FadeIn(m_c_x), run_time=tracker.duration/10)
            r4 = multiplica(c, a*b, COLOR_B, velocidad=tracker.duration/8)
            m_abc2 = MathTex("(ab)c", color=COLOR_B, font_size=42).next_to(m_abc, DOWN, buff=0.15)
            self.play(FadeIn(m_abc2), run_time=tracker.duration/10)
        
        with self.voiceover(text=tr("""Mismo punto. Pero cuente: <bookmark mark='rectas'/>cuatro rectas, <bookmark mark='paralelas'/>cuatro paralelas, <bookmark mark='arcos'/>dos arcos... <bookmark mark='tres'/>y solo para multiplicar tres números.""",
                                    """Same point. But count: <bookmark mark='rectas'/>four lines, <bookmark mark='paralelas'/>four parallels, <bookmark mark='arcos'/>two arcs... <bookmark mark='tres'/>and only to multiply three numbers.""")) as tracker:
            self.play(Indicate(m_abc, color=COLOR_RESULTADO, scale_factor=1.5), run_time=1)
            # cada cosa que cuenta la voz parpadea cuando la nombra; la fórmula, al final
            self.wait_until_bookmark("rectas")
            self.play(*[Indicate(r[0], color=COLOR_RESULTADO, scale_factor=1.03) for r in (r1, r2, r3, r4)], run_time=1)
            self.wait_until_bookmark("paralelas")
            self.play(*[Indicate(r[1], color=COLOR_RESULTADO, scale_factor=1.03) for r in (r1, r2, r3, r4)], run_time=1)
            self.wait_until_bookmark("arcos")
            self.play(Indicate(arco1, color=COLOR_RESULTADO, scale_factor=1.03), Indicate(arco2, color=COLOR_RESULTADO, scale_factor=1.03), run_time=1)
            self.wait_until_bookmark("tres")
            self.destaca_regla(regla2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not cabecera], run_time=0.8)
        
        euclides = Tex(tr("Euclides, siglo III a.\\,C.: álgebra con figuras", "Euclid, 3rd century BC: algebra with figures"),
                       font_size=42)
        descartes = Tex(tr("Descartes, 1637: los segmentos son números, y se opera con símbolos",
                           "Descartes, 1637: segments are numbers, and one operates with symbols"),
                        font_size=42).set_color(COLOR_ESCALAR)
        escuela = Tex(tr("La escuela: las reglas se comprueban con ejemplos numéricos, y se usan",
                         "School: the rules are checked on numerical examples, and used"),
                      font_size=42)
        historia = VGroup(euclides, descartes, escuela).arrange(DOWN, buff=0.6).move_to(0.3*DOWN)
        for h in historia:
            h.scale_to_fit_width(min(h.width, config.frame_width*0.9))
        
        with self.voiceover(text=tr("""Todas estas propiedades se pueden ver con regla y compás. Pero es engorroso. Y esta es la cuestión. Los geómetras griegos razonaban así, con figuras: en los Elementos de Euclides la propiedad distributiva es un teorema sobre rectángulos.""",
                                    """All these properties can be seen with ruler and compass. But it is cumbersome. And that is the point. The Greek geometers reasoned this way, with figures: in Euclid's Elements the distributive property is a theorem about rectangles.""")) as tracker:
            self.play(Write(euclides), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""Hubo que esperar casi dos mil años a que Descartes diera el salto: tratar los segmentos como números y operar con símbolos siguiendo unas pocas reglas.""",
                                    """It took almost two thousand years for Descartes to make the leap: to treat segments as numbers and to operate with symbols following a few rules.""")) as tracker:
            self.play(Write(descartes), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""Esa es la tradición que usted recibió en la escuela: allí las reglas no se justifican con figuras, se comprueban con unos cuantos ejemplos numéricos, y se usan.""",
                                    """That is the tradition you received at school: there the rules are not justified with figures, they are checked on a few numerical examples, and used.""")) as tracker:
            self.play(Write(escuela), run_time=tracker.duration/2)
        
        self.pausa()


class L01_V05_E05_Resumen(MiEscenaConVoz):
    def construct(self):
        self.creditos()
        cabecera = Tex(tr("Las reglas del juego", "The rules of the game"),
                       font_size=44).set_color(COLOR_TITULO).to_edge(UP)
        self.add(cabecera)
        
        sean = Tex(tr(r"Para cualesquiera números reales $a$, $b$ y $c$:", r"For any real numbers $a$, $b$ and $c$:"),
                   tex_template=myTemplate, font_size=40).next_to(cabecera, DOWN, buff=0.4)
        
        propiedades = [r"a+b=b+a",
                       r"a+(b+c)=(a+b)+c",
                       r"a+0=a",
                       r"a+(-a)=0",
                       r"ab=ba",
                       r"a(b+c)=ab+ac",
                       r"a(bc)=(ab)c",
                       r"1a=a",
                       r"a\,a^{-1}=1\;\;(a\neq 0)"]
        
        lista = VGroup(*[MathTex(f"{k+1}.\;\;", p, tex_template=myTemplate, font_size=44)
                         for k, p in enumerate(propiedades)])
        
        # dos columnas (suma: 4 filas; producto: 5 filas) sobre una misma rejilla de filas
        columna_suma     = VGroup(*lista[:4]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        columna_producto = VGroup(*lista[4:]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        cuadro = VGroup(columna_suma, columna_producto).arrange(RIGHT, buff=1.4, aligned_edge=UP)
        cuadro.next_to(sean, DOWN, buff=0.5).set_x(0)
        paso = 0.68
        y0 = lista[0].get_y()
        for k in range(4):
            lista[k].set_y(y0 - k*paso)
        for k in range(5):
            lista[4+k].set_y(y0 - k*paso)
        
        with self.voiceover(text=tr("""Resumamos. Las dos operaciones con números reales se pueden hacer con regla y compás, y cumplen estas propiedades.""",
                                    """Let us sum up. The two operations with real numbers can be carried out with ruler and compass, and they satisfy these properties.""")) as tracker:
            self.play(FadeIn(sean), run_time=tracker.duration/2)
        
        with self.voiceover(text=tr("""De la suma: es conmutativa, es asociativa, el cero es el elemento neutro, y todo número tiene un opuesto.""",
                                    """For addition: it is commutative, it is associative, zero is the identity element, and every number has an opposite.""")) as tracker:
            for k in range(4):
                self.play(FadeIn(lista[k]), run_time=tracker.duration/4)
        
        with self.voiceover(text=tr("""Del producto: es conmutativo, es distributivo respecto de la suma, es asociativo, el uno es el elemento neutro, y todo número distinto de cero tiene un inverso.""",
                                    """For multiplication: it is commutative, it is distributive over addition, it is associative, one is the identity element, and every nonzero number has an inverse.""")) as tracker:
            for k in range(4, 9):
                self.play(FadeIn(lista[k]), run_time=tracker.duration/5)
        
        cita = VGroup(Tex(r"``Notation is everything''", font_size=46).set_color(COLOR_ESCALAR),
                      Tex("Charles F. Van Loan", font_size=34).set_color(GRAY_B)).arrange(DOWN, buff=0.25)
        cita.next_to(cuadro, DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""A partir de ahora no volveremos a la regla y el compás. Estas nueve reglas son todo lo que necesitamos para operar simbólicamente con números reales. Como dice Charles Van Loan: la notación lo es todo.""",
                                    """From now on we will not go back to ruler and compass. These nine rules are all we need to operate symbolically with real numbers. As Charles Van Loan says: notation is everything.""")) as tracker:
            self.pausa(tracker.duration/2)
            self.play(FadeIn(cita), run_time=tracker.duration/2)
        
        self.pausa(1.2)   # respiro tras la cita
        
        pregunta = Tex(tr(r"¿Cumplen estas propiedades las operaciones con \emph{vectores}?",
                          r"Do the operations with \emph{vectors} satisfy these properties?"),
                       tex_template=myTemplate, font_size=44).set_color(COLOR_ESCALAR).next_to(cuadro, DOWN, buff=0.5)
        
        with self.voiceover(text=tr("""En el próximo vídeo plantearemos la misma cuestión para los vectores. Veremos si la suma de vectores y el producto por escalares cumplen estas mismas propiedades.""",
                                    """In the next video we will raise the same question for vectors. We will see whether the sum of vectors and the product by scalars satisfy these same properties.""")) as tracker:
            self.play(FadeOut(cita), run_time=1)
            self.play(Write(pregunta), run_time=2)
        
        self.pausa_media()


class ZCreditosFinales(Scene):
    def construct(self):
        copyright = Tex(r"\textcopyright{\;} 2026 \; Marcos Bujosa")
        github = Tex(r"\texttt{https://github.com/mbujosab}").next_to(copyright, DOWN)
        CGG  = VGroup(copyright, github).scale(1.1)
        self.add(CGG)
        self.wait(15)   # tiempo para las tarjetas de enlaces de YouTube
