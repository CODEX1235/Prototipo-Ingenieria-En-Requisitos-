from modelos.medico import Medico
from modelos.usuario import Usuario


class Cita:
    ESTADO_PROGRAMADA = "Programada"
    ESTADO_CANCELADA = "Cancelada"

    def __init__(self, paciente: Usuario, medico: Medico,
                 fecha: str, hora: str, consultorio: str = "Consultorio 401"):
        self.paciente = paciente
        self.medico = medico
        self.fecha = fecha
        self.hora = hora
        self.consultorio = consultorio
        self.estado = self.ESTADO_PROGRAMADA

    def cancelar(self):
        self.estado = self.ESTADO_CANCELADA

    def __str__(self) -> str:
        return (f"Cita con {self.medico.nombre} | {self.fecha} {self.hora} "
                f"| {self.estado}")
