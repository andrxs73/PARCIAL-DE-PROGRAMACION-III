"""Preguntas de ejemplo con las que arranca la aplicación."""
from modelos import Dificultad, PreguntaMultiple, PreguntaVerdaderoFalso

F, M, D = Dificultad.FACIL, Dificultad.MEDIA, Dificultad.DIFICIL


def crear_banco_inicial():
    return [
        # ---------------- Ciencia ----------------
        PreguntaMultiple("¿Qué planeta es conocido como el planeta rojo?", "Ciencia", F,
                         ["Mercurio", "Venus", "Marte", "Júpiter"], 2),
        PreguntaVerdaderoFalso("El agua hierve a 100 °C al nivel del mar.", "Ciencia", F, True),
        PreguntaMultiple("¿Cuál es el símbolo químico del sodio?", "Ciencia", M,
                         ["Na", "So", "Sd", "Sn"], 0),
        PreguntaMultiple("¿Qué gas absorben las plantas durante la fotosíntesis?", "Ciencia", M,
                         ["Oxígeno", "Dióxido de carbono", "Nitrógeno", "Hidrógeno"], 1),
        PreguntaMultiple("¿Cuántos huesos tiene el cuerpo humano adulto?", "Ciencia", D,
                         ["186", "206", "226", "256"], 1),
        PreguntaVerdaderoFalso(
            "La luz del Sol tarda aproximadamente 8 minutos en llegar a la Tierra.",
            "Ciencia", D, True),
        # ---------------- Historia ----------------
        PreguntaMultiple("¿En qué año llegó Cristóbal Colón a América?", "Historia", F,
                         ["1492", "1502", "1453", "1520"], 0),
        PreguntaVerdaderoFalso(
            "La independencia de Colombia se proclamó el 20 de julio de 1810.",
            "Historia", F, True),
        PreguntaMultiple("¿Quién fue el primer presidente de Estados Unidos?", "Historia", M,
                         ["George Washington", "Abraham Lincoln", "Thomas Jefferson", "John Adams"], 0),
        PreguntaMultiple("¿En qué año terminó la Segunda Guerra Mundial?", "Historia", M,
                         ["1918", "1939", "1945", "1950"], 2),
        PreguntaMultiple("¿Qué imperio construyó Machu Picchu?", "Historia", D,
                         ["Azteca", "Maya", "Inca", "Romano"], 2),
        PreguntaVerdaderoFalso("La Revolución Francesa comenzó en 1789.", "Historia", D, True),
        # ---------------- Geografía ----------------
        PreguntaMultiple("¿Cuál es la capital de Colombia?", "Geografía", F,
                         ["Medellín", "Bogotá", "Cali", "Barranquilla"], 1),
        PreguntaVerdaderoFalso("El océano Atlántico es el más grande del mundo.", "Geografía", F, False),
        PreguntaMultiple("¿Cuál es el río más largo de Sudamérica?", "Geografía", M,
                         ["Orinoco", "Amazonas", "Magdalena", "Paraná"], 1),
        PreguntaVerdaderoFalso("El desierto del Sahara se encuentra en África.", "Geografía", M, True),
        PreguntaMultiple("¿Cuál es la capital de Australia?", "Geografía", D,
                         ["Sídney", "Melbourne", "Canberra", "Perth"], 2),
        PreguntaMultiple("¿Qué país de Sudamérica tiene más habitantes?", "Geografía", D,
                         ["Brasil", "Argentina", "Colombia", "Perú"], 0),
        # ---------------- Tecnología ----------------
        PreguntaMultiple("¿Qué significa CPU?", "Tecnología", F,
                         ["Unidad Central de Procesamiento", "Unidad Cuántica Programable",
                          "Controlador Principal Universal", "Central de Procesos Unificada"], 0),
        PreguntaVerdaderoFalso("Python es un lenguaje de programación.", "Tecnología", F, True),
        PreguntaMultiple("¿Qué lenguaje se usa para dar estilo a las páginas web?", "Tecnología", M,
                         ["HTML", "CSS", "SQL", "Java"], 1),
        PreguntaVerdaderoFalso("El ESP32 incluye conectividad Wi-Fi integrada.", "Tecnología", M, True),
        PreguntaMultiple(
            "¿Qué principio de la POO permite que objetos distintos respondan de forma "
            "diferente al mismo método?", "Tecnología", D,
            ["Encapsulamiento", "Herencia", "Polimorfismo", "Abstracción"], 2),
        PreguntaMultiple("¿Qué módulo de Python permite definir clases abstractas?", "Tecnología", D,
                         ["abc", "os", "sys", "math"], 0),
    ]
