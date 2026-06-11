class Usuario:
    def __init__(self, nombre: str, tipo_documento: str, numero_documento: str,
                 correo: str, contrasena: str, plan: str = "Plan Básico"):
        self.nombre = nombre
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.correo = correo
        self.contrasena = contrasena
        self.plan = plan

    def verificar_contrasena(self, contrasena: str) -> bool:
        return self.contrasena == contrasena

    def __str__(self) -> str:
        return f"{self.nombre} | {self.tipo_documento}: {self.numero_documento}"
