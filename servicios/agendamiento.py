from modelos.cita import Cita
from modelos.medico import Medico
from modelos.usuario import Usuario
from datos.repositorio import Repositorio


class ServicioAgendamiento:
    def __init__(self, repositorio: Repositorio):
        self._repositorio = repositorio

    def obtener_medicos(self) -> list[Medico]:
        return self._repositorio.obtener_medicos()

    def agendar_cita(self, paciente: Usuario, medico: Medico,
                     fecha: str, hora: str) -> tuple[bool, str, Cita | None]:
        if not fecha or not hora:
            return False, "Selecciona una fecha y hora.", None

        nueva_cita = Cita(paciente, medico, fecha, hora)
        self._repositorio.guardar_cita(nueva_cita)
        return True, "Cita agendada correctamente.", nueva_cita
