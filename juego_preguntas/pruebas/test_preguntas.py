import pytest

from modelos import Dificultad, Pregunta, PreguntaMultiple, PreguntaVerdaderoFalso


def crear_multiple():
    return PreguntaMultiple("¿2 + 2?", "Mates", Dificultad.FACIL, ["3", "4", "5", "6"], 1)


def test_multiple_evalua_respuesta_correcta():
    assert crear_multiple().evaluar("4") is True


def test_multiple_rechaza_incorrecta_y_none():
    pregunta = crear_multiple()
    assert pregunta.evaluar("3") is False
    assert pregunta.evaluar(None) is False


def test_verdadero_falso_evalua():
    pregunta = PreguntaVerdaderoFalso("El cielo es azul.", "Ciencia", Dificultad.FACIL, True)
    assert pregunta.evaluar("Verdadero") is True
    assert pregunta.evaluar("Falso") is False
    assert pregunta.opciones() == ["Verdadero", "Falso"]


def test_no_se_puede_instanciar_la_clase_abstracta():
    with pytest.raises(TypeError):
        Pregunta("x", "y", Dificultad.FACIL)


def test_enunciado_vacio_lanza_error():
    with pytest.raises(ValueError):
        PreguntaMultiple("   ", "Mates", Dificultad.FACIL, ["a", "b"], 0)


def test_opciones_repetidas_lanzan_error():
    with pytest.raises(ValueError):
        PreguntaMultiple("¿?", "Mates", Dificultad.FACIL, ["a", "A", "b"], 0)


def test_indice_correcto_fuera_de_rango():
    with pytest.raises(ValueError):
        PreguntaMultiple("¿?", "Mates", Dificultad.FACIL, ["a", "b"], 5)


def test_opciones_devuelve_copia_protegida():
    pregunta = crear_multiple()
    pregunta.opciones().append("intruso")
    assert "intruso" not in pregunta.opciones()


def test_opciones_para_mostrar_conserva_las_mismas_opciones():
    pregunta = crear_multiple()
    assert sorted(pregunta.opciones_para_mostrar()) == sorted(pregunta.opciones())
