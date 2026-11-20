"""Ventana principal: coordina las pantallas y conecta la interfaz con la lógica."""
from tkinter import messagebox, ttk
import tkinter as tk

from interfaz.dialogo_pregunta import DialogoPregunta
from interfaz.pantalla_inicio import PantallaInicio
from interfaz.pantalla_juego import PantallaJuego
from interfaz.pantalla_resultados import PantallaResultados
from interfaz.temporizador import Temporizador
from servicios.gestor_preguntas import SinPreguntasError
from servicios.partida import Partida

PAUSA_RETROALIMENTACION_MS = 1500


class VentanaPrincipal(tk.Tk):
    def __init__(self, gestor):
        super().__init__()
        self.title("Juego de Preguntas")
        self.geometry("680x560")
        self.minsize(620, 520)
        ttk.Style(self).theme_use("clam")

        self._gestor = gestor        # asociación: la ventana usa al gestor
        self._partida = None         # se crea al iniciar cada juego
        self._esperando = False      # evita responder dos veces la misma pregunta

        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        # Composición: la ventana crea y es dueña de sus pantallas.
        self._inicio = PantallaInicio(
            contenedor, gestor.categorias(), self._iniciar_partida, self._abrir_dialogo)
        self._juego = PantallaJuego(contenedor, self._responder)
        self._resultados = PantallaResultados(contenedor, self._volver_al_inicio)
        for pantalla in (self._inicio, self._juego, self._resultados):
            pantalla.grid(row=0, column=0, sticky="nsew")

        self._temporizador = Temporizador(self, self._juego.actualizar_tiempo, self._tiempo_agotado)
        self.protocol("WM_DELETE_WINDOW", self._cerrar)
        self._inicio.tkraise()

    # ---------- Callbacks de la interfaz ----------
    def _abrir_dialogo(self):
        DialogoPregunta(self, self._gestor,
                        lambda: self._inicio.actualizar_categorias(self._gestor.categorias()))

    def _iniciar_partida(self, nombre, categoria, dificultad, cantidad):
        try:
            preguntas = self._gestor.seleccionar(categoria, dificultad, cantidad)
            self._partida = Partida(nombre, preguntas)
        except (SinPreguntasError, ValueError) as error:
            messagebox.showerror("No se puede iniciar", str(error))
            return
        self._juego.tkraise()
        self._mostrar_pregunta()

    def _mostrar_pregunta(self):
        p = self._partida
        self._esperando = False
        self._juego.mostrar_pregunta(
            p.jugador, p.pregunta_actual, p.numero_actual, p.total_preguntas,
            p.puntaje, p.tiempo_por_pregunta)
        self._temporizador.iniciar(p.tiempo_por_pregunta)

    def _responder(self, respuesta):
        if self._esperando:
            return
        self._esperando = True
        self._temporizador.detener()
        resultado = self._partida.responder(respuesta, self._temporizador.restante)
        self._juego.mostrar_retroalimentacion(resultado)
        self.after(PAUSA_RETROALIMENTACION_MS, self._avanzar)

    def _tiempo_agotado(self):
        if self._esperando:
            return
        self._esperando = True
        self._juego.bloquear_opciones()
        resultado = self._partida.responder(None, 0)
        self._juego.mostrar_retroalimentacion(resultado)
        self.after(PAUSA_RETROALIMENTACION_MS, self._avanzar)

    def _avanzar(self):
        if self._partida.terminada:
            self._resultados.mostrar(self._partida)
            self._resultados.tkraise()
        else:
            self._mostrar_pregunta()

    def _volver_al_inicio(self):
        self._inicio.tkraise()

    def _cerrar(self):
        self._temporizador.detener()
        self.destroy()
