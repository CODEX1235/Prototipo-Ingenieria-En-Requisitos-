# Salud EPS — Portal Paciente

Aplicativo de escritorio desarrollado en Python con interfaz gráfica (tkinter), orientado a la gestión de citas médicas para pacientes de una EPS.

---

## Prototipos implementados

| # | Prototipo | Descripción |
|---|-----------|-------------|
| 1 | **Acceso y Registro** | Inicio de sesión y creación de cuenta de paciente |
| 2 | **Agendamiento** | Directorio médico, selección de fecha/hora y confirmación de cita |
| 3 | **Gestión de Citas** | Vista de citas programadas y acceso rápido a nueva cita |

---

## Tecnologías y conceptos aplicados

- **Python 3.11+**
- **Tkinter** — interfaz gráfica nativa
- **Programación Orientada a Objetos** — clases con responsabilidad única
- **Recursividad** — búsqueda de usuarios, filtrado de citas y validación de campos
- **Manejo de excepciones** — control de errores en flujos de usuario
- **Código Limpio** — nombres descriptivos, métodos cortos, módulos separados por responsabilidad

---

## Estructura del proyecto

```
salud_eps/
├── main.py                  # Punto de entrada y navegación principal
├── README.md
│
├── modelos/                 # Entidades del dominio
│   ├── usuario.py
│   ├── medico.py
│   └── cita.py
│
├── servicios/               # Lógica de negocio
│   ├── autenticacion.py
│   ├── agendamiento.py
│   └── gestion_citas.py
│
├── vistas/                  # Pantallas de la aplicación
│   ├── estilos.py
│   ├── vista_acceso.py
│   ├── vista_agendamiento.py
│   └── vista_mis_citas.py
│
└── datos/                   # Capa de datos en memoria
    └── repositorio.py
```

---

## Cómo ejecutar

### Requisitos
- Python 3.11 o superior
- Tkinter (incluido por defecto en Python)

### Pasos

```bash
# Clonar o descargar el proyecto
cd salud_eps

# Ejecutar
python main.py
```

---

## Cuenta de prueba

Para probar el inicio de sesión, primero **regístrate** desde la pantalla de acceso.  
Luego ingresa con el mismo tipo de documento, número y contraseña que usaste.

---

## Uso de recursividad

La recursividad se aplica en tres puntos del proyecto:

1. **`repositorio.py`** — `_buscar_usuario_recursivo`: recorre la lista de usuarios para encontrar uno por documento.
2. **`repositorio.py`** — `_filtrar_citas_recursivo`: filtra las citas que pertenecen al usuario activo.
3. **`autenticacion.py`** — `_validar_campos_recursivo`: verifica que todos los campos del formulario estén completos.

---

## Principios de Código Limpio aplicados

- **SRP** (Single Responsibility Principle): cada clase tiene una sola razón para cambiar.
- **DRY** (Don't Repeat Yourself): los estilos y colores están centralizados en `estilos.py`.
- **Nombres descriptivos**: métodos y variables se explican por sí solos.
- **Métodos cortos**: cada método realiza una sola acción.
- **Sin comentarios innecesarios**: el código es autoexplicativo.
