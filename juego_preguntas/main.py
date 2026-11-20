"""Punto de entrada de la aplicación."""
from interfaz.ventana_principal import VentanaPrincipal
from servicios.banco_inicial import crear_banco_inicial
from servicios.gestor_preguntas import GestorPreguntas


def main():
    gestor = GestorPreguntas(crear_banco_inicial())
    VentanaPrincipal(gestor).mainloop()


if __name__ == "__main__":
    main()
