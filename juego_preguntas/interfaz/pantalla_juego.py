"""Pantalla donde se muestran las preguntas y se responde."""
from tkinter import ttk


class PantallaJuego(ttk.Frame):
    def __init__(self, master, al_responder):
        super().__init__(master, padding=20)
        self._al_responder = al_responder
        self._botones = []

        self._lbl_estado = ttk.Label(self, font=("Helvetica", 11, "bold"))
        self._lbl_estado.pack(anchor="w")
        self._lbl_info = ttk.Label(self, foreground="#666666")
        self._lbl_info.pack(anchor="w", pady=(0, 8))

        self._lbl_tiempo = ttk.Label(self, font=("Helvetica", 11))
        self._lbl_tiempo.pack(anchor="e")
        self._barra = ttk.Progressbar(self, mode="determinate")
        self._barra.pack(fill="x", pady=(2, 18))

        self._lbl_enunciado = ttk.Label(
            self, font=("Helvetica", 16, "bold"), wraplength=540, justify="center")
        self._lbl_enunciado.pack(pady=(0, 18))

        self._marco_opciones = ttk.Frame(self)
        self._marco_opciones.pack(fill="x", padx=40)

        self._lbl_retro = ttk.Label(self, font=("Helvetica", 12, "bold"), wraplength=540,
                                    justify="center")
        self._lbl_retro.pack(pady=18)

    def mostrar_pregunta(self, jugador, pregunta, numero, total, puntaje, segundos):
        self._lbl_estado.config(
            text=f"{jugador}   |   Pregunta {numero}/{total}   |   Puntaje: {puntaje}")
        self._lbl_info.config(
            text=f"{pregunta.categoria} · {pregunta.dificultad.etiqueta} · {pregunta.tipo}")
        self._lbl_enunciado.config(text=pregunta.enunciado)
        self._lbl_retro.config(text="")
        self._barra.config(maximum=segundos)
        self.actualizar_tiempo(segundos)

        for boton in self._botones:
            boton.destroy()
        self._botones.clear()
        # Polimorfismo: cada tipo de pregunta decide cómo presentar sus opciones.
        for opcion in pregunta.opciones_para_mostrar():
            boton = ttk.Button(
                self._marco_opciones, text=opcion,
                command=lambda texto=opcion: self._elegir(texto))
            boton.pack(fill="x", pady=4, ipady=6)
            self._botones.append(boton)

    def actualizar_tiempo(self, restante):
        self._lbl_tiempo.config(text=f"Tiempo: {restante} s")
        self._barra["value"] = restante

    def bloquear_opciones(self):
        for boton in self._botones:
            boton.state(["disabled"])

    def mostrar_retroalimentacion(self, resultado):
        correcta = resultado.pregunta.respuesta_correcta()
        if resultado.respuesta is None:
            texto, color = f"⏰ ¡Se acabó el tiempo! La respuesta era: {correcta}", "#b26a00"
        elif resultado.correcta:
            texto, color = f"✔ ¡Correcto!  +{resultado.puntos} puntos", "#1b7f3b"
        else:
            texto, color = f"✘ Incorrecto. La respuesta era: {correcta}", "#b3261e"
        self._lbl_retro.config(text=texto, foreground=color)

    def _elegir(self, opcion):
        self.bloquear_opciones()
        self._al_responder(opcion)
