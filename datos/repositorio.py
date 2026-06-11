from modelos.usuario import Usuario
from modelos.medico import Medico
from modelos.cita import Cita


class Repositorio:
    def __init__(self):
        self._usuarios: list[Usuario] = []
        self._medicos: list[Medico] = self._cargar_medicos_iniciales()
        self._citas: list[Cita] = []

    def _cargar_medicos_iniciales(self) -> list[Medico]:
        return [
            Medico("Dra. Ana Martínez", "Odontología", 4.7,
                   ["10:00", "12:00", "15:00"]),
            Medico("Dr. Carlos Ramírez", "Medicina General", 4.5,
                   ["09:00", "11:00", "14:00"]),
            Medico("Dra. Laura Gómez", "Pediatría", 4.8,
                   ["08:00", "10:00", "16:00"]),
            Medico("Dr. Andrés Torres", "Cardiología", 4.6,
                   ["09:00", "13:00", "15:00"]),
        ]

    # ── Usuarios ──────────────────────────────────────────────

    def guardar_usuario(self, usuario: Usuario):
        self._usuarios.append(usuario)

    def buscar_usuario(self, tipo_doc: str, numero_doc: str) -> Usuario | None:
        return self._buscar_usuario_recursivo(
            self._usuarios, tipo_doc, numero_doc, 0
        )

    def _buscar_usuario_recursivo(self, usuarios: list, tipo_doc: str,
                                   numero_doc: str, indice: int) -> Usuario | None:
        if indice >= len(usuarios):
            return None
        usuario = usuarios[indice]
        if usuario.tipo_documento == tipo_doc and usuario.numero_documento == numero_doc:
            return usuario
        return self._buscar_usuario_recursivo(
            usuarios, tipo_doc, numero_doc, indice + 1
        )

    def existe_documento(self, numero_doc: str) -> bool:
        return self._verificar_documento_recursivo(self._usuarios, numero_doc, 0)

    def _verificar_documento_recursivo(self, usuarios: list,
                                        numero_doc: str, indice: int) -> bool:
        if indice >= len(usuarios):
            return False
        if usuarios[indice].numero_documento == numero_doc:
            return True
        return self._verificar_documento_recursivo(usuarios, numero_doc, indice + 1)

    # ── Médicos ───────────────────────────────────────────────

    def obtener_medicos(self) -> list[Medico]:
        return self._medicos

    def obtener_medicos_por_especialidad(self, especialidad: str) -> list[Medico]:
        return self._filtrar_medicos_recursivo(self._medicos, especialidad, 0, [])

    def _filtrar_medicos_recursivo(self, medicos: list, especialidad: str,
                                    indice: int, resultado: list) -> list:
        if indice >= len(medicos):
            return resultado
        if medicos[indice].especialidad.lower() == especialidad.lower():
            resultado.append(medicos[indice])
        return self._filtrar_medicos_recursivo(
            medicos, especialidad, indice + 1, resultado
        )

    # ── Citas ─────────────────────────────────────────────────

    def guardar_cita(self, cita: Cita):
        self._citas.append(cita)

    def obtener_citas_de_usuario(self, numero_doc: str) -> list[Cita]:
        return self._filtrar_citas_recursivo(self._citas, numero_doc, 0, [])

    def _filtrar_citas_recursivo(self, citas: list, numero_doc: str,
                                  indice: int, resultado: list) -> list:
        if indice >= len(citas):
            return resultado
        if citas[indice].paciente.numero_documento == numero_doc:
            resultado.append(citas[indice])
        return self._filtrar_citas_recursivo(
            citas, numero_doc, indice + 1, resultado
        )
