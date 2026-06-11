class Medico:
    def __init__(self, nombre: str, especialidad: str, calificacion: float,
                 horarios: list, sede: str = "Sede Principal"):
        self.nombre = nombre
        self.especialidad = especialidad
        self.calificacion = calificacion
        self.horarios = horarios
        self.sede = sede

    def __str__(self) -> str:
        return f"{self.nombre} - {self.especialidad}"
