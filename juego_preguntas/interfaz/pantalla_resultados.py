"""Pantalla final con el resumen de la partida."""
from tkinter import ttk


class PantallaResultados(ttk.Frame):
    def __init__(self, master, al_jugar_de_nuevo):
        super().__init__(master, padding=20)
        self._lbl_titulo = ttk.Label(self, font=("Helvetica", 20, "bold"))
        self._lbl_titulo.pack(pady=(5, 8))
        self._lbl_resumen = ttk.Label(self, font=("Helvetica", 12))
        self._lbl_resumen.pack(pady=(0, 12))

        columnas = ("pregunta", "tu_respuesta", "correcta", "puntos")
        self._tabla = ttk.Treeview(self, columns=columnas, show="headings", height=8)
        for columna, titulo, ancho in (
            ("pregunta", "Pregunta", 280), ("tu_respuesta", "Tu respuesta", 120),
            ("correcta", "Correcta", 120), ("puntos", "Puntos", 60),
        ):
            self._tabla.heading(columna, text=titulo)
            self._tabla.column(columna, width=ancho, anchor="w" if columna != "puntos" else "center")
        self._tabla.pack(fill="both", expand=True)

        ttk.Button(self, text="Jugar de nuevo", command=al_jugar_de_nuevo).pack(
            pady=14, ipadx=20, ipady=4)

    def mostrar(self, partida):
        self._lbl_titulo.config(text=f"¡Fin de la partida, {partida.jugador}!")
        self._lbl_resumen.config(
            text=(f"Puntaje: {partida.puntaje}   |   "
                  f"Aciertos: {partida.aciertos}/{partida.total_preguntas}   |   "
                  f"Precisión: {partida.precision:.0f}%"))
        self._tabla.delete(*self._tabla.get_children())
        for r in partida.resultados:
            self._tabla.insert("", "end", values=(
                r.pregunta.enunciado, r.respuesta_texto,
                r.pregunta.respuesta_correcta(), r.puntos))
