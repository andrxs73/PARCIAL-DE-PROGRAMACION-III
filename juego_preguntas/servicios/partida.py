"""Lógica de una partida: avance, puntaje y resultados."""
from dataclasses import dataclass
from typing import Optional

from modelos import Pregunta


class PartidaTerminadaError(Exception):
    """Se intentó operar sobre una partida que ya terminó."""


@dataclass(frozen=True)
class ResultadoRespuesta:
    """Resultado de responder una pregunta (composición dentro de Partida)."""

    pregunta: Pregunta
    respuesta: Optional[str]
    correcta: bool
    puntos: int
    tiempo_restante: int

    @property
    def respuesta_texto(self):
        return self.respuesta if self.respuesta is not None else "(sin respuesta)"


class Partida:
    """Controla el estado del juego. No conoce nada de la interfaz gráfica."""

    TIEMPO_POR_PREGUNTA = 15
    SEGUNDOS_POR_PUNTO_EXTRA = 3

    def __init__(self, jugador, preguntas, tiempo_por_pregunta=TIEMPO_POR_PREGUNTA):
        if not isinstance(jugador, str) or not jugador.strip():
            raise ValueError("El nombre del jugador no puede estar vacío.")
        preguntas = list(preguntas)
        if not preguntas:
            raise ValueError("La partida necesita al menos una pregunta.")
        if tiempo_por_pregunta <= 0:
            raise ValueError("El tiempo por pregunta debe ser mayor que cero.")
        self._jugador = jugador.strip()
        self._preguntas = preguntas
        self._tiempo_por_pregunta = tiempo_por_pregunta
        self._indice = 0
        self._puntaje = 0
        self._resultados = []

    @property
    def jugador(self):
        return self._jugador

    @property
    def puntaje(self):
        return self._puntaje

    @property
    def tiempo_por_pregunta(self):
        return self._tiempo_por_pregunta

    @property
    def total_preguntas(self):
        return len(self._preguntas)

    @property
    def numero_actual(self):
        return min(self._indice + 1, self.total_preguntas)

    @property
    def terminada(self):
        return self._indice >= self.total_preguntas

    @property
    def resultados(self):
        return tuple(self._resultados)

    @property
    def aciertos(self):
        return sum(1 for r in self._resultados if r.correcta)

    @property
    def precision(self):
        if not self._resultados:
            return 0.0
        return 100 * self.aciertos / len(self._resultados)

    @property
    def pregunta_actual(self):
        if self.terminada:
            raise PartidaTerminadaError("La partida ya terminó.")
        return self._preguntas[self._indice]

    def responder(self, respuesta, tiempo_restante):
        """Evalúa la respuesta (None si se agotó el tiempo) y avanza a la siguiente."""
        pregunta = self.pregunta_actual
        tiempo_restante = max(0, int(tiempo_restante))
        correcta = respuesta is not None and pregunta.evaluar(respuesta)
        puntos = 0
        if correcta:
            bono = tiempo_restante // self.SEGUNDOS_POR_PUNTO_EXTRA
            puntos = pregunta.puntos_base + bono
        resultado = ResultadoRespuesta(pregunta, respuesta, correcta, puntos, tiempo_restante)
        self._resultados.append(resultado)
        self._puntaje += puntos
        self._indice += 1
        return resultado
