import tkinter as tk
from datos.repositorio import Repositorio
from servicios.autenticacion import ServicioAutenticacion
from servicios.agendamiento import ServicioAgendamiento
from servicios.gestion_citas import ServicioGestionCitas
from vistas.vista_acceso import VistaAcceso
from vistas.vista_agendamiento import VistaAgendamiento
from vistas.vista_mis_citas import VistaMisCitas
from vistas.estilos import COLORES, DIMENSIONES
from modelos.usuario import Usuario


class AplicacionSaludEPS:
    TITULO = "Salud EPS — Portal Paciente"

    def __init__(self):
        self._repositorio = Repositorio()
        self._servicio_auth = ServicioAutenticacion(self._repositorio)
        self._servicio_agendamiento = ServicioAgendamiento(self._repositorio)
        self._servicio_citas = ServicioGestionCitas(self._repositorio)
        self._usuario_activo: Usuario | None = None
        self._ventana = self._crear_ventana()
        self._vista_actual = None
        self._mostrar_acceso()

    def _crear_ventana(self) -> tk.Tk:
        ventana = tk.Tk()
        ventana.title(self.TITULO)
        ventana.configure(bg=COLORES["fondo"])
        ventana.resizable(False, False)
        ancho = DIMENSIONES["ancho_ventana"]
        alto = DIMENSIONES["alto_ventana"]
        ventana.geometry(self._centrar_ventana(ventana, ancho, alto))
        return ventana

    def _centrar_ventana(self, ventana: tk.Tk, ancho: int, alto: int) -> str:
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        return f"{ancho}x{alto}+{x}+{y}"

    # ── Navegación entre pantallas ────────────────────────────

    def _mostrar_acceso(self):
        self._limpiar_vista()
        self._ventana.geometry(self._centrar_ventana(
            self._ventana,
            DIMENSIONES["ancho_ventana"],
            DIMENSIONES["alto_ventana"]
        ))
        self._vista_actual = VistaAcceso(
            self._ventana, self._servicio_auth, self._al_iniciar_sesion
        )
        self._vista_actual.pack(fill="both", expand=True)

    def _mostrar_mis_citas(self):
        self._limpiar_vista()
        self._ventana.geometry(self._centrar_ventana(self._ventana, 780, 520))
        self._vista_actual = VistaMisCitas(
            self._ventana, self._servicio_citas,
            self._usuario_activo, self._mostrar_agendamiento,
            al_inicio=self._mostrar_acceso
        )
        self._vista_actual.pack(fill="both", expand=True)

    def _mostrar_agendamiento(self):
        self._limpiar_vista()
        self._ventana.geometry(self._centrar_ventana(self._ventana, 820, 600))
        self._vista_actual = VistaAgendamiento(
            self._ventana, self._servicio_agendamiento,
            self._usuario_activo, self._al_confirmar_cita
        )
        self._vista_actual.pack(fill="both", expand=True)

    # ── Callbacks ─────────────────────────────────────────────

    def _al_iniciar_sesion(self, usuario: Usuario):
        self._usuario_activo = usuario
        self._mostrar_mis_citas()

    def _al_confirmar_cita(self):
        self._mostrar_mis_citas()

    def _limpiar_vista(self):
        if self._vista_actual is not None:
            self._vista_actual.destroy()
            self._vista_actual = None

    def ejecutar(self):
        self._ventana.mainloop()


if __name__ == "__main__":
    app = AplicacionSaludEPS()
    app.ejecutar()
