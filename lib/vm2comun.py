"""Código común a los vídeos de la serie (español). Generado desde Comunes.org: no editar a mano."""
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

    def creditos_finales(self):
        """Pantalla final de créditos al acabar el vídeo completo."""
        pantalla_de_creditos(self)

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

def pantalla_de_creditos(escena, segundos=15):
    """Copyright y enlace a GitHub; `segundos` deja sitio a las tarjetas de enlaces de YouTube."""
    copyright = Tex(r"\textcopyright{\;} 2026 \; Marcos Bujosa")
    github = Tex(r"\texttt{https://github.com/mbujosab}").next_to(copyright, DOWN)
    escena.add(VGroup(copyright, github).scale(1.1))
    escena.wait(segundos)


class CreditosFinales(Scene):
    """Escena suelta de créditos; en cada vídeo: class ZCreditosFinales(CreditosFinales): pass"""
    def construct(self):
        pantalla_de_creditos(self)

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
            start=np.array(ejes.c2p(0, 0, 0)),
            end=np.array(ejes.c2p(*self.coords)),
            resolution=8,
            color = self.color )
