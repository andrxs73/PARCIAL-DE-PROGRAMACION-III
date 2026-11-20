"""Ventana emergente para agregar preguntas nuevas al banco."""
from tkinter import messagebox, ttk
import tkinter as tk

from modelos import Dificultad, PreguntaMultiple, PreguntaVerdaderoFalso

TIPO_MULTIPLE = "Selección múltiple"
TIPO_VF = "Verdadero o falso"


class DialogoPregunta(tk.Toplevel):
    def __init__(self, master, gestor, al_guardar):
        super().__init__(master)
        self.title("Agregar pregunta")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._gestor = gestor
        self._al_guardar = al_guardar
        self._tipo = tk.StringVar(value=TIPO_MULTIPLE)
        self._enunciado = tk.StringVar()
        self._categoria = tk.StringVar()
        self._dificultad = tk.StringVar(value=Dificultad.FACIL.etiqueta)
        self._correcta = tk.IntVar(value=0)
        self._verdadera = tk.StringVar(value=PreguntaVerdaderoFalso.VERDADERO)
        self._entradas = []

        marco = ttk.Frame(self, padding=18)
        marco.pack()

        ttk.Label(marco, text="Tipo:").grid(row=0, column=0, sticky="e", pady=5, padx=6)
        combo_tipo = ttk.Combobox(marco, textvariable=self._tipo, state="readonly", width=30,
                                  values=[TIPO_MULTIPLE, TIPO_VF])
        combo_tipo.grid(row=0, column=1, sticky="w")
        combo_tipo.bind("<<ComboboxSelected>>", self._al_cambiar_tipo)

        ttk.Label(marco, text="Pregunta:").grid(row=1, column=0, sticky="e", pady=5, padx=6)
        ttk.Entry(marco, textvariable=self._enunciado, width=52).grid(row=1, column=1, sticky="w")

        ttk.Label(marco, text="Categoría:").grid(row=2, column=0, sticky="e", pady=5, padx=6)
        ttk.Combobox(marco, textvariable=self._categoria, width=30,
                     values=gestor.categorias()).grid(row=2, column=1, sticky="w")

        ttk.Label(marco, text="Dificultad:").grid(row=3, column=0, sticky="e", pady=5, padx=6)
        ttk.Combobox(marco, textvariable=self._dificultad, state="readonly", width=30,
                     values=[d.etiqueta for d in Dificultad]).grid(row=3, column=1, sticky="w")

        self._marco_multiple = ttk.LabelFrame(marco, text="Opciones (marca la correcta)", padding=8)
        for i in range(4):
            entrada = tk.StringVar()
            self._entradas.append(entrada)
            ttk.Radiobutton(self._marco_multiple, variable=self._correcta, value=i).grid(
                row=i, column=0, padx=(0, 6))
            ttk.Entry(self._marco_multiple, textvariable=entrada, width=48).grid(
                row=i, column=1, pady=2)

        self._marco_vf = ttk.LabelFrame(marco, text="La afirmación es...", padding=8)
        for valor in (PreguntaVerdaderoFalso.VERDADERO, PreguntaVerdaderoFalso.FALSO):
            ttk.Radiobutton(self._marco_vf, text=valor, variable=self._verdadera,
                            value=valor).pack(side="left", padx=12)

        self._marco_multiple.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        self._marco_vf.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        self._marco_vf.grid_remove()

        botones = ttk.Frame(marco)
        botones.grid(row=5, column=0, columnspan=2, pady=(6, 0))
        ttk.Button(botones, text="Guardar", command=self._guardar).pack(side="left", padx=6)
        ttk.Button(botones, text="Cancelar", command=self.destroy).pack(side="left", padx=6)

    def _al_cambiar_tipo(self, _evento=None):
        if self._tipo.get() == TIPO_MULTIPLE:
            self._marco_vf.grid_remove()
            self._marco_multiple.grid()
        else:
            self._marco_multiple.grid_remove()
            self._marco_vf.grid()

    def _construir_pregunta(self):
        enunciado = self._enunciado.get()
        categoria = self._categoria.get()
        dificultad = Dificultad.desde_etiqueta(self._dificultad.get())
        if self._tipo.get() == TIPO_MULTIPLE:
            opciones = [e.get() for e in self._entradas]
            return PreguntaMultiple(enunciado, categoria, dificultad, opciones, self._correcta.get())
        es_verdadera = self._verdadera.get() == PreguntaVerdaderoFalso.VERDADERO
        return PreguntaVerdaderoFalso(enunciado, categoria, dificultad, es_verdadera)

    def _guardar(self):
        try:
            self._gestor.agregar(self._construir_pregunta())
        except ValueError as error:
            messagebox.showerror("No se pudo guardar", str(error), parent=self)
            return
        self._al_guardar()
        messagebox.showinfo("Listo", "La pregunta se agregó al banco.", parent=self)
        self.destroy()
