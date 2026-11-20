"""Cuenta regresiva no bloqueante basada en Widget.after()."""


class Temporizador:
    """Llama a `al_tick(restante)` cada segundo y a `al_terminar()` al llegar a 0."""

    def __init__(self, widget, al_tick, al_terminar):
        self._widget = widget
        self._al_tick = al_tick
        self._al_terminar = al_terminar
        self._restante = 0
        self._id_after = None

    @property
    def restante(self):
        return self._restante

    def iniciar(self, segundos):
        self.detener()
        self._restante = segundos
        self._tick()

    def detener(self):
        if self._id_after is not None:
            self._widget.after_cancel(self._id_after)
            self._id_after = None

    def _tick(self):
        self._id_after = None
        self._al_tick(self._restante)
        if self._restante <= 0:
            self._al_terminar()
            return
        self._restante -= 1
        self._id_after = self._widget.after(1000, self._tick)
