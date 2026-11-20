"""Modelos del dominio: dificultades y tipos de pregunta."""
import random
from abc import ABC, abstractmethod
from enum import Enum


class Dificultad(Enum):
    """Nivel de dificultad. Cada nivel define los puntos base que otorga."""

    FACIL = ("Fácil", 10)
    MEDIA = ("Media", 20)
    DIFICIL = ("Difícil", 30)

    def __init__(self, etiqueta, puntos):
        self.etiqueta = etiqueta
        self.puntos = puntos

    @classmethod
    def desde_etiqueta(cls, etiqueta):
        for dificultad in cls:
            if dificultad.etiqueta == etiqueta:
                return dificultad
        raise ValueError(f"Dificultad desconocida: {etiqueta!r}")


def _texto_valido(valor, campo):
    """Valida que un valor sea un texto no vacío y lo devuelve sin espacios sobrantes."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    return valor.strip()


class Pregunta(ABC):
    """Clase abstracta: define el contrato que cumple todo tipo de pregunta."""

    def __init__(self, enunciado, categoria, dificultad):
        self.enunciado = enunciado      # pasa por el setter con validación
        self.categoria = categoria      # pasa por el setter con validación
        if not isinstance(dificultad, Dificultad):
            raise ValueError("La dificultad debe ser un valor de Dificultad.")
        self._dificultad = dificultad

    # --- Encapsulamiento: atributos protegidos con validación ---
    @property
    def enunciado(self):
        return self._enunciado

    @enunciado.setter
    def enunciado(self, valor):
        self._enunciado = _texto_valido(valor, "enunciado")

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._categoria = _texto_valido(valor, "categoría")

    @property
    def dificultad(self):
        return self._dificultad

    @property
    def puntos_base(self):
        return self._dificultad.puntos

    # --- Contrato abstracto: cada subclase lo implementa a su manera ---
    @property
    @abstractmethod
    def tipo(self):
        """Nombre legible del tipo de pregunta."""

    @abstractmethod
    def opciones(self):
        """Lista de opciones de respuesta posibles."""

    @abstractmethod
    def respuesta_correcta(self):
        """Texto de la respuesta correcta."""

    @abstractmethod
    def evaluar(self, respuesta):
        """Devuelve True si la respuesta recibida es correcta."""

    def opciones_para_mostrar(self):
        """Orden en que se presentan las opciones. Las subclases pueden cambiarlo."""
        return self.opciones()


class PreguntaMultiple(Pregunta):
    """Pregunta con varias opciones y una sola correcta."""

    def __init__(self, enunciado, categoria, dificultad, opciones, indice_correcto):
        super().__init__(enunciado, categoria, dificultad)
        limpias = [_texto_valido(o, "opción") for o in opciones]
        if len(limpias) < 2:
            raise ValueError("Se necesitan al menos 2 opciones.")
        if len({o.lower() for o in limpias}) != len(limpias):
            raise ValueError("Las opciones no pueden repetirse.")
        if not 0 <= indice_correcto < len(limpias):
            raise ValueError("El índice de la respuesta correcta está fuera de rango.")
        self._opciones = limpias
        self._indice_correcto = indice_correcto

    @property
    def tipo(self):
        return "Selección múltiple"

    def opciones(self):
        return list(self._opciones)  # copia: protege el estado interno

    def respuesta_correcta(self):
        return self._opciones[self._indice_correcto]

    def evaluar(self, respuesta):
        return respuesta == self.respuesta_correcta()

    def opciones_para_mostrar(self):
        # Polimorfismo: esta clase mezcla las opciones, la otra mantiene el orden.
        return random.sample(self._opciones, len(self._opciones))


class PreguntaVerdaderoFalso(Pregunta):
    """Afirmación que el jugador debe calificar como verdadera o falsa."""

    VERDADERO = "Verdadero"
    FALSO = "Falso"

    def __init__(self, enunciado, categoria, dificultad, es_verdadera):
        super().__init__(enunciado, categoria, dificultad)
        self._es_verdadera = bool(es_verdadera)

    @property
    def tipo(self):
        return "Verdadero o falso"

    def opciones(self):
        return [self.VERDADERO, self.FALSO]

    def respuesta_correcta(self):
        return self.VERDADERO if self._es_verdadera else self.FALSO

    def evaluar(self, respuesta):
        return respuesta == self.respuesta_correcta()
