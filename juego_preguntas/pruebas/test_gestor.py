import pytest

from modelos import Dificultad, PreguntaMultiple, PreguntaVerdaderoFalso
from servicios.banco_inicial import crear_banco_inicial
from servicios.gestor_preguntas import GestorPreguntas, SinPreguntasError


def test_banco_inicial_cubre_todas_las_combinaciones():
    gestor = GestorPreguntas(crear_banco_inicial())
    for categoria in gestor.categorias():
        for dificultad in Dificultad:
            assert gestor.seleccionar(categoria, dificultad, 1)


def test_seleccionar_respeta_filtros_y_cantidad():
    gestor = GestorPreguntas(crear_banco_inicial())
    elegidas = gestor.seleccionar("Ciencia", Dificultad.FACIL, 10)
    assert len(elegidas) == 2
    assert all(p.categoria == "Ciencia" and p.dificultad == Dificultad.FACIL for p in elegidas)


def test_seleccionar_sin_coincidencias_lanza_error():
    gestor = GestorPreguntas()
    gestor.agregar(PreguntaVerdaderoFalso("Afirmación", "Arte", Dificultad.FACIL, True))
    with pytest.raises(SinPreguntasError):
        gestor.seleccionar("Arte", Dificultad.DIFICIL, 3)


def test_cantidad_invalida_lanza_error():
    with pytest.raises(ValueError):
        GestorPreguntas(crear_banco_inicial()).seleccionar(cantidad=0)


def test_no_permite_enunciados_duplicados():
    gestor = GestorPreguntas()
    gestor.agregar(PreguntaVerdaderoFalso("Repetida", "A", Dificultad.FACIL, True))
    with pytest.raises(ValueError):
        gestor.agregar(PreguntaVerdaderoFalso("repetida", "B", Dificultad.MEDIA, False))


def test_solo_acepta_objetos_pregunta():
    with pytest.raises(TypeError):
        GestorPreguntas().agregar("no soy una pregunta")


def test_categorias_ordenadas_y_sin_repetir():
    gestor = GestorPreguntas([
        PreguntaMultiple("¿1?", "Zeta", Dificultad.FACIL, ["a", "b"], 0),
        PreguntaMultiple("¿2?", "Alfa", Dificultad.FACIL, ["a", "b"], 0),
        PreguntaMultiple("¿3?", "Alfa", Dificultad.MEDIA, ["a", "b"], 0),
    ])
    assert gestor.categorias() == ["Alfa", "Zeta"]
