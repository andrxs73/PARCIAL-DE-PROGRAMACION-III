"""Pantalla de configuración de la partida."""
from tkinter import messagebox, ttk
import tkinter as tk

from modelos import Dificultad

TODAS = "Todas"


class PantallaInicio(ttk.Frame):
    def __init__(self, master, categorias, al_jugar, al_agregar_pregunta):
        super().__init__(master, padding=30)
        self._al_jugar = al_jugar
        self._nombre = tk.StringVar()
        self._categoria = tk.StringVar(value=TODAS)
        self._dificultad = tk.StringVar(value=TODAS)
        self._cantidad = tk.StringVar(value="5")

        ttk.Label(self, text="Juego de Preguntas", font=("Helvetica", 26, "bold")).pack(pady=(10, 25))

        formulario = ttk.Frame(self)
        formulario.pack()

        ttk.Label(formulario, text="Tu nombre:").grid(row=0, column=0, sticky="e", pady=6, padx=6)
        self._entrada_nombre = ttk.Entry(formulario, textvariable=self._nombre, width=24)
        self._entrada_nombre.grid(row=0, column=1, pady=6)

        ttk.Label(formulario, text="Categoría:").grid(row=1, column=0, sticky="e", pady=6, padx=6)
        self._combo_categoria = ttk.Combobox(
            formulario, textvariable=self._categoria, state="readonly", width=21)
        self._combo_categoria.grid(row=1, column=1, pady=6)

        ttk.Label(formulario, text="Dificultad:").grid(row=2, column=0, sticky="e", pady=6, padx=6)
        ttk.Combobox(
            formulario, textvariable=self._dificultad, state="readonly", width=21,
            values=[TODAS] + [d.etiqueta for d in Dificultad],
        ).grid(row=2, column=1, pady=6)

        ttk.Label(formulario, text="Nº de preguntas:").grid(row=3, column=0, sticky="e", pady=6, padx=6)
        ttk.Spinbox(formulario, from_=1, to=20, textvariable=self._cantidad, width=22).grid(
            row=3, column=1, pady=6)

        ttk.Button(self, text="Jugar", command=self._jugar).pack(pady=(25, 6), ipadx=30, ipady=4)
        ttk.Button(self, text="Agregar pregunta", command=al_agregar_pregunta).pack(pady=6)

        self.actualizar_categorias(categorias)
        self._entrada_nombre.focus_set()
        self.bind_all("<Return>", self._al_presionar_enter)

    def actualizar_categorias(self, categorias):
        self._combo_categoria["values"] = [TODAS] + list(categorias)

    def _al_presionar_enter(self, _evento):
        # Solo reacciona cuando esta pantalla es la visible.
        if self.winfo_ismapped():
            self._jugar()

    def _jugar(self):
        nombre = self._nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Datos incompletos", "Escribe tu nombre para jugar.")
            return
        try:
            cantidad = int(self._cantidad.get())
        except ValueError:
            messagebox.showwarning(
                "Cantidad inválida", "La cantidad de preguntas debe ser un número entero.")
            return
        if not 1 <= cantidad <= 20:
            messagebox.showwarning(
                "Cantidad inválida", "La cantidad de preguntas debe estar entre 1 y 20.")
            return
        categoria = None if self._categoria.get() == TODAS else self._categoria.get()
        dificultad = (None if self._dificultad.get() == TODAS
                      else Dificultad.desde_etiqueta(self._dificultad.get()))
        self._al_jugar(nombre, categoria, dificultad, cantidad)
