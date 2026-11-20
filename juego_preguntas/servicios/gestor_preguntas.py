"""Administra el banco de preguntas en memoria."""
import random

from modelos import Pregunta


class SinPreguntasError(Exception):
    """No hay preguntas que cumplan el filtro solicitado."""


class GestorPreguntas:
    """Guarda las preguntas (agregación) y selecciona subconjuntos para jugar."""

    def __init__(self, preguntas=None):
        self._preguntas = []
        for pregunta in preguntas or []:
            self.agregar(pregunta)

    @property
    def total(self):
        return len(self._preguntas)

    def agregar(self, pregunta):
        if not isinstance(pregunta, Pregunta):
            raise TypeError("Solo se pueden agregar objetos de tipo Pregunta.")
        nuevo = pregunta.enunciado.lower()
        if any(p.enunciado.lower() == nuevo for p in self._preguntas):
            raise ValueError("Ya existe una pregunta con ese enunciado.")
        self._preguntas.append(pregunta)

    def categorias(self):
        return sorted({p.categoria for p in self._preguntas})

    def seleccionar(self, categoria=None, dificultad=None, cantidad=5):
        """Devuelve hasta `cantidad` preguntas al azar que cumplan los filtros."""
        if cantidad <= 0:
            raise ValueError("La cantidad de preguntas debe ser mayor que cero.")
        candidatas = [
            p for p in self._preguntas
            if (categoria is None or p.categoria == categoria)
            and (dificultad is None or p.dificultad == dificultad)
        ]
        if not candidatas:
            raise SinPreguntasError(
                "No hay preguntas con esa combinación de categoría y dificultad."
            )
        return random.sample(candidatas, min(cantidad, len(candidatas)))
