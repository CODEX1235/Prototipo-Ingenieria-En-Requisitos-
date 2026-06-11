from modelos.usuario import Usuario
from datos.repositorio import Repositorio


class ServicioAutenticacion:
    def __init__(self, repositorio: Repositorio):
        self._repositorio = repositorio

    def registrar(self, nombre: str, tipo_doc: str, numero_doc: str,
                  correo: str, contrasena: str) -> tuple[bool, str]:
        if not self._campos_completos(nombre, tipo_doc, numero_doc, correo, contrasena):
            return False, "Todos los campos son obligatorios."

        if len(contrasena) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."

        if "@" not in correo or "." not in correo.split("@")[-1]:
            return False, "El correo electrónico no es válido."

        if not numero_doc.isdigit():
            return False, "El número de documento solo debe contener dígitos."

        if self._repositorio.existe_documento(numero_doc):
            return False, "Ya existe una cuenta con ese número de documento."

        nuevo_usuario = Usuario(nombre, tipo_doc, numero_doc, correo, contrasena)
        self._repositorio.guardar_usuario(nuevo_usuario)
        return True, "Cuenta creada exitosamente."

    def iniciar_sesion(self, tipo_doc: str, numero_doc: str,
                       contrasena: str) -> tuple[bool, str, Usuario | None]:
        if not tipo_doc or not numero_doc or not contrasena:
            return False, "Completa todos los campos.", None

        usuario = self._repositorio.buscar_usuario(tipo_doc, numero_doc)
        if usuario is None:
            return False, "No se encontró una cuenta con ese documento.", None

        if not usuario.verificar_contrasena(contrasena):
            return False, "Contraseña incorrecta.", None

        return True, "Bienvenido.", usuario

    def _campos_completos(self, *campos) -> bool:
        return self._validar_campos_recursivo(campos, 0)

    def _validar_campos_recursivo(self, campos: tuple, indice: int) -> bool:
        if indice >= len(campos):
            return True
        if not campos[indice] or not str(campos[indice]).strip():
            return False
        return self._validar_campos_recursivo(campos, indice + 1)
