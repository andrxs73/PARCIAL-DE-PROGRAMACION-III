import pytest

from modelos import Dificultad, PreguntaMultiple, PreguntaVerdaderoFalso
from servicios.partida import Partida, PartidaTerminadaError


def preguntas():
    return [
        PreguntaMultiple("¿2 + 2?", "Mates", Dificultad.FACIL, ["3", "4"], 1),
        PreguntaVerdaderoFalso("El sol es una estrella.", "Ciencia", Dificultad.DIFICIL, True),
    ]


def test_respuesta_correcta_suma_puntos_base_mas_bono_de_tiempo():
    partida = Partida("Ana", preguntas())
    resultado = partida.responder("4", 15)   # 10 base + 15 // 3 = 5
    assert resultado.correcta
    assert resultado.puntos == 15
    assert partida.puntaje == 15


def test_respuesta_incorrecta_no_suma_puntos():
    partida = Partida("Ana", preguntas())
    assert partida.responder("3", 10).puntos == 0
    assert partida.puntaje == 0


def test_tiempo_agotado_cuenta_como_fallo():
    partida = Partida("Ana", preguntas())
    resultado = partida.responder(None, 0)
    assert not resultado.correcta
    assert resultado.respuesta_texto == "(sin respuesta)"


def test_flujo_completo_y_estadisticas():
    partida = Partida("Ana", preguntas())
    partida.responder("4", 0)
    partida.responder("Falso", 5)
    assert partida.terminada
    assert partida.aciertos == 1
    assert partida.precision == 50.0
    assert len(partida.resultados) == 2


def test_responder_con_partida_terminada_lanza_error():
    partida = Partida("Ana", preguntas()[:1])
    partida.responder("4", 5)
    with pytest.raises(PartidaTerminadaError):
        partida.responder("4", 5)


def test_partida_exige_jugador_y_preguntas():
    with pytest.raises(ValueError):
        Partida("   ", preguntas())
    with pytest.raises(ValueError):
        Partida("Ana", [])


def test_resultados_devuelve_copia_inmutable():
    partida = Partida("Ana", preguntas())
    partida.responder("4", 5)
    assert isinstance(partida.resultados, tuple)
