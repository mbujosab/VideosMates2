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

    def pausa_para_pensar(self, pista=None, pista_voz=None, segundos=4, invitacion=None, invitacion_voz=None,
                          al_dar_la_pista=None):
        """Tarjeta que invita a pausar el vídeo; opcionalmente da una pista y vuelve a invitar.
        `invitacion` cambia el texto de la primera tarjeta (e `invitacion_voz` lo que dice la voz);
        `al_dar_la_pista` es una función que se ejecuta mientras la voz da la pista (por ejemplo,
        iluminar en amarillo las piezas que hacen falta)."""
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
    
        invitacion = invitacion or tr("Pause el vídeo e inténtelo.", "Pause the video and give it a try.")
        tarjeta1 = tarjeta(invitacion)
        with self.voiceover(text=invitacion_voz or invitacion) as tracker:
            self.play(FadeIn(tarjeta1), run_time=min(0.8, tracker.duration))
        self.wait(segundos)
        if pista is not None:
            tarjeta2 = tarjeta(tr("Pista: ", "Hint: ") + pista)
            with self.voiceover(text=tr("Una pista: ", "A hint: ") + (pista_voz or pista)) as tracker:
                self.play(ReplacementTransform(tarjeta1, tarjeta2), run_time=min(0.8, tracker.duration))
                if al_dar_la_pista is not None:
                    al_dar_la_pista()
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

OMEGA_COLOR  = PURPLE_B     # fuera del código de colores de la serie


def _cara(estado, alto, mira=ORIGIN):
    """Ojos, cejas y boca de Omega (se colocan dentro del arco). Estados: normal (sonriente),
    neutral (sin sonrisa), duda, sorpresa, alegria y meditacion."""
    u, blanco, r = alto/2, dict(color=WHITE, stroke_width=3), 0.11*alto/2
    def ojo(rr=r, pupila=0.5, m=mira):
        b = Circle(radius=rr, color=WHITE, fill_opacity=1, stroke_width=1.2).set_stroke(BLACK)
        p = Dot(radius=rr*pupila, color=BLACK).move_to(m*rr*0.4)
        return VGroup(b, p, Dot(radius=rr*0.13, color=WHITE).move_to(p.get_center() + rr*0.18*(UP + LEFT)))
    if estado == "alegria":
        ojos = VGroup(*[Arc(radius=0.8*r, start_angle=0, angle=PI, **blanco) for _ in range(2)])
    elif estado == "meditacion":
        ojos = VGroup(*[Arc(radius=0.8*r, start_angle=PI, angle=PI, **blanco) for _ in range(2)])
    elif estado == "sorpresa":
        ojos = VGroup(ojo(1.25*r, 0.3, ORIGIN), ojo(1.25*r, 0.3, ORIGIN))
    elif estado == "duda":
        ojos = VGroup(ojo(m=UR), ojo(m=UR))
    else:
        ojos = VGroup(ojo(), ojo())
    ojos.arrange(RIGHT, buff=0.9*r)
    i, d, w = ojos[0].get_top(), ojos[1].get_top(), 2.2*r
    ceja = lambda c, ang, dy: Line(c + 0.5*w*LEFT, c + 0.5*w*RIGHT, **blanco).rotate(ang).shift((0.12*u + dy)*UP)
    if estado == "duda":          # una ceja alta, con la punta interior levantada
        cejas = VGroup(ceja(i, 0, -0.02*u), ceja(d, -18*DEGREES, 0.1*u))
    elif estado == "sorpresa":
        cejas = VGroup(*[ArcBetweenPoints(c + 0.5*w*LEFT + 0.2*u*UP, c + 0.5*w*RIGHT + 0.2*u*UP, angle=-PI/3, **blanco) for c in (i, d)])
    elif estado in ("meditacion", "neutral"):
        cejas = VGroup(ceja(i, 0, -0.02*u), ceja(d, 0, -0.02*u))
    else:                         # normal y alegría: cejas relajadas
        cejas = VGroup(ceja(i, 10*DEGREES, 0), ceja(d, -10*DEGREES, 0))
    base = ojos.get_bottom() + 0.16*u*DOWN
    if estado == "alegria":
        boca = Arc(radius=0.17*u, start_angle=PI, angle=PI, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=2).move_to(base + 0.04*u*DOWN)
    elif estado == "sorpresa":
        boca = Ellipse(width=0.12*u, height=0.17*u, color=WHITE, stroke_width=3).move_to(base + 0.04*u*DOWN)
    elif estado == "duda":
        boca = Line(base + 0.12*u*LEFT, base + 0.12*u*RIGHT, **blanco).rotate(-12*DEGREES)
    elif estado in ("meditacion", "neutral"):
        boca = Line(base + (0.06 if estado == "meditacion" else 0.1)*u*LEFT, base + (0.06 if estado == "meditacion" else 0.1)*u*RIGHT, **blanco)
    else:
        boca = Arc(radius=0.14*u, start_angle=-PI*0.8, angle=PI*0.6, **blanco).move_to(base)
    return VGroup(ojos, cejas, boca)


def omega(estado="normal", alto=1.6, mira=ORIGIN, color=None):
    """La criatura de la serie: [0] el cuerpo (una Ω gruesa), [1] la cara (ojos, cejas, boca)
    y [2] el signo del estado (?, !, destellos o la nube de pensamiento)."""
    cuerpo = MathTex(r"\boldsymbol{\Omega}").set_color(color or OMEGA_COLOR).scale_to_fit_height(alto)
    cara = _cara(estado, alto, mira).move_to(cuerpo.get_center() + 0.13*alto*UP)
    figura = VGroup(cuerpo, cara)
    signo = VGroup()
    if estado == "duda":
        figura.rotate(-8*DEGREES)
        signo = MathTex("?", font_size=60, color=COLOR_ESCALAR).next_to(figura, UR, buff=0)
    elif estado == "sorpresa":
        figura.stretch(1.08, 1)
        signo = MathTex("!", font_size=60, color=COLOR_ESCALAR).next_to(figura, UR, buff=0)
    elif estado == "alegria":
        figura.stretch(0.95, 1)
        signo = VGroup(*[Star(n=4, outer_radius=0.12, inner_radius=0.04, color=COLOR_ESCALAR, fill_opacity=1).move_to(figura.get_corner(UR) + v)
                         for v in (0.1*UP, 0.35*DOWN + 0.25*RIGHT, 0.25*UP + 0.45*LEFT)])
    elif estado == "meditacion":
        nube = VGroup(*[Circle(radius=rr, color=WHITE, fill_opacity=1) for rr in (0.06, 0.1, 0.38)])
        nube[0].move_to(figura.get_corner(UR) + 0.05*UP); nube[1].next_to(nube[0], UR, buff=0.05); nube[2].next_to(nube[1], UR, buff=0)
        signo = VGroup(nube, MathTex(r"\dots", color=BLACK, font_size=40).move_to(nube[2]))
    o = VGroup(cuerpo, cara, signo)
    o.estado, o.alto, o.mira = estado, alto, mira
    return o


def cambia(escena, criatura, estado, mira=None, run_time=0.6):
    """Cambia la expresión de la criatura sin moverla (el cuerpo se queda donde estaba)."""
    nueva = omega(estado, criatura.alto, criatura.mira if mira is None else mira)
    nueva.shift(criatura[0].get_bottom() - nueva[0].get_bottom())
    # Un signo que aparece o desaparece (?, !, destellos) lo hace en su sitio: transformado
    # desde o hacia un grupo vacío, volaría desde o hacia el origen.
    if len(nueva[2]) == 0 and len(criatura[2]) > 0:
        nueva.submobjects[2] = criatura[2].copy().set_opacity(0)
    elif len(criatura[2]) == 0 and len(nueva[2]) > 0:
        criatura.submobjects[2] = nueva[2].copy().set_opacity(0)
    escena.play(Transform(criatura, nueva), run_time=run_time)
    criatura.estado, criatura.mira = estado, nueva.mira


def bocadillo(texto, criatura, ancho=4.2, font_size=30):
    t = Tex(texto, font_size=font_size, color=BLACK)
    if t.width > ancho:
        t.scale_to_fit_width(ancho)
    globo = RoundedRectangle(corner_radius=0.25, width=t.width + 0.5, height=t.height + 0.4,
                             fill_color=WHITE, fill_opacity=1, stroke_color=WHITE)
    globo.next_to(criatura[0], UL, buff=0.05).shift(0.4*RIGHT)
    t.move_to(globo)
    pico = Polygon(globo.get_corner(DR) + 0.35*LEFT, globo.get_corner(DR) + 0.8*LEFT,
                   criatura[0].get_corner(UL) + 0.15*RIGHT + 0.05*DOWN, fill_color=WHITE, fill_opacity=1, stroke_width=0)
    return VGroup(pico, globo, t)


def parpadea(escena, criatura, run_time=0.3):
    if criatura.estado in ("alegria", "meditacion"):   # ya tiene los ojos cerrados
        return
    ojos = criatura[1][0]
    escena.play(ojos.animate.stretch(0.1, 1), run_time=run_time/2)
    escena.play(ojos.animate.stretch(10, 1), run_time=run_time/2)


def entra(escena, criatura, desde=RIGHT, run_time=1):
    escena.play(FadeIn(criatura, shift=1.5*(-desde)), run_time=run_time)
    parpadea(escena, criatura)

ICONOS = {   # tipo: (color, texto por defecto)
    "pregunta":   (COLOR_ESCALAR, tr("Pregunta", "Question")),
    "idea":       (GOLD_A,        tr("Idea clave", "Key idea")),
    "engorroso":  (RED_B,         tr("Engorroso", "Tedious")),
    "ilustra":    (GRAY_A,        tr("Ilustra, no demuestra", "Illustrates, does not prove")),
    "ampliacion": (PURPLE_B,      tr("Ampliación", "Extension")),
}

def icono(tipo, alto=0.6):
    """El símbolo del tipo de momento, dibujado con primitivas (sin fuentes especiales)."""
    color = ICONOS[tipo][0]
    if tipo == "pregunta":     # disco con una interrogación
        s = VGroup(Circle(radius=0.5, fill_color=color, fill_opacity=1, stroke_width=0),
                   MathTex(r"\boldsymbol{?}", color=BLACK, font_size=72))
    elif tipo == "idea":       # bombilla con rayos
        bombilla = Circle(radius=0.32, color=color, stroke_width=6).shift(0.12*UP)
        casquillo = VGroup(*[Line(0.14*LEFT, 0.14*RIGHT, color=color, stroke_width=6).shift((0.32 + 0.11*k)*DOWN)
                             for k in range(2)])
        rayos = VGroup(*[Line(0.45*UP, 0.62*UP, color=color, stroke_width=5).rotate(a, about_point=ORIGIN).shift(0.12*UP)
                         for a in (-1.0, -0.5, 0, 0.5, 1.0)])
        s = VGroup(bombilla, casquillo, rayos)
    elif tipo == "engorroso":  # garabato enredado
        s = ParametricFunction(lambda t: np.array([0.4*np.sin(2*t) + 0.15*np.cos(7*t), 0.4*np.cos(3*t) + 0.12*np.sin(5*t), 0]),
                               t_range=[0, TAU], color=color, stroke_width=5)
    elif tipo == "ilustra":    # un ojo
        parpado = VGroup(ArcBetweenPoints(0.55*LEFT, 0.55*RIGHT, angle=-1.6),
                         ArcBetweenPoints(0.55*LEFT, 0.55*RIGHT, angle=1.6)).set_stroke(color, 6)
        s = VGroup(parpado, Circle(radius=0.17, fill_color=color, fill_opacity=1, stroke_width=0))
    elif tipo == "ampliacion":  # señal de curva peligrosa (rombo con una curva en S)
        rombo = Square(side_length=0.75, color=color, stroke_width=6).rotate(PI/4)
        curva = ParametricFunction(lambda t: np.array([0.12*np.sin(PI*t), 0.3*t, 0]), t_range=[-1, 1],
                                   color=color, stroke_width=6)
        s = VGroup(rombo, curva)
    s.scale_to_fit_height(alto)
    for m in s.family_members_with_points():   # trazo diseñado para alto 1: más fino si el icono es pequeño
        m.set_stroke(width=m.get_stroke_width()*min(1, alto))
    return s

def aviso(tipo, texto=None, font_size=30):
    """Rótulo con icono para marcar el tipo de momento del vídeo (ver ICONOS)."""
    color, por_defecto = ICONOS[tipo]
    rotulo = Tex(texto or por_defecto, tex_template=myTemplate, font_size=font_size, color=color)
    contenido = VGroup(icono(tipo, alto=max(0.45, 1.3*rotulo.height)), rotulo).arrange(RIGHT, buff=0.25)
    marco = RoundedRectangle(corner_radius=0.18, width=contenido.width+0.5, height=contenido.height+0.35,
                             stroke_color=color, stroke_width=2, fill_color=BLACK, fill_opacity=0.85)
    return VGroup(marco, contenido.move_to(marco))

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
