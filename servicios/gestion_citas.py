from modelos.cita import Cita
from modelos.usuario import Usuario
from datos.repositorio import Repositorio


class ServicioGestionCitas:
    def __init__(self, repositorio: Repositorio):
        self._repositorio = repositorio

    def obtener_mis_citas(self, usuario: Usuario) -> list[Cita]:
        return self._repositorio.obtener_citas_de_usuario(usuario.numero_documento)
