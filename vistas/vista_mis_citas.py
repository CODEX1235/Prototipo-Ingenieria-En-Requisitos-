import tkinter as tk
from tkinter import messagebox
from modelos.usuario import Usuario
from servicios.gestion_citas import ServicioGestionCitas
from vistas.estilos import COLORES, FUENTES

MESES = {
    "01": "ENE", "02": "FEB", "03": "MAR", "04": "ABR",
    "05": "MAY", "06": "JUN", "07": "JUL", "08": "AGO",
    "09": "SEP", "10": "OCT", "11": "NOV", "12": "DIC",
}


class VistaMisCitas(tk.Frame):
    def __init__(self, padre, servicio: ServicioGestionCitas,
                 usuario: Usuario, al_nueva_cita, al_inicio=None):
        super().__init__(padre, bg=COLORES["fondo"])
        self._servicio = servicio
        self._usuario = usuario
        self._al_nueva_cita = al_nueva_cita
        self._al_inicio = al_inicio
        self._solo_activas = tk.BooleanVar(value=True)
        self._construir_interfaz()

    # ── Construcción ──────────────────────────────────────────

    def _construir_interfaz(self):
        self._crear_barra_superior()
        self._crear_cuerpo()

    def _crear_barra_superior(self):
        barra = tk.Frame(self, bg=COLORES["encabezado"], height=60)
        barra.pack(fill="x")
        barra.pack_propagate(False)

        tk.Label(barra, text="❤  Salud EPS",
                 font=FUENTES["subtitulo"], bg=COLORES["encabezado"],
                 fg=COLORES["blanco"]).pack(side="left", padx=20, pady=15)

        nav = tk.Frame(barra, bg=COLORES["encabezado"])
        nav.pack(side="left", padx=20)

        tk.Button(nav, text="Inicio", font=FUENTES["etiqueta"],
                  bg=COLORES["encabezado"], fg="#A5C8FF",
                  relief="flat", bd=0, cursor="hand2",
                  activebackground=COLORES["encabezado"],
                  activeforeground=COLORES["blanco"],
                  command=self._ir_al_inicio).pack(side="left", padx=10)

        tk.Label(nav, text="Mis Citas", font=("Segoe UI", 10, "bold"),
                 bg=COLORES["encabezado"],
                 fg=COLORES["blanco"]).pack(side="left", padx=10)

        tk.Label(barra, text=f"{self._usuario.nombre}  |  {self._usuario.plan}",
                 font=FUENTES["pequeño"], bg=COLORES["encabezado"],
                 fg="#A5C8FF").pack(side="right", padx=20)

    def _crear_cuerpo(self):
        cuerpo = tk.Frame(self, bg=COLORES["fondo"])
        cuerpo.pack(fill="both", expand=True, padx=30, pady=20)

        encabezado = tk.Frame(cuerpo, bg=COLORES["fondo"])
        encabezado.pack(fill="x", pady=(0, 16))

        bloque_titulo = tk.Frame(encabezado, bg=COLORES["fondo"])
        bloque_titulo.pack(side="left")
        tk.Label(bloque_titulo, text="Mis Citas Médicas",
                 font=FUENTES["titulo"], bg=COLORES["fondo"],
                 fg=COLORES["texto_principal"]).pack(anchor="w")
        tk.Label(bloque_titulo,
                 text="Historial y próximas atenciones programadas",
                 font=FUENTES["pequeño"], bg=COLORES["fondo"],
                 fg=COLORES["texto_secundario"]).pack(anchor="w")

        acciones = tk.Frame(encabezado, bg=COLORES["fondo"])
        acciones.pack(side="right")

        tk.Checkbutton(
            acciones, text="Solo activas",
            variable=self._solo_activas,
            font=FUENTES["pequeño"], bg=COLORES["fondo"],
            fg=COLORES["texto_secundario"], activebackground=COLORES["fondo"],
            cursor="hand2", command=self._cargar_citas
        ).pack(side="left", padx=(0, 12))

        tk.Button(
            acciones, text="＋  Nueva Cita",
            font=FUENTES["boton"], bg=COLORES["primario"],
            fg=COLORES["blanco"], relief="flat", cursor="hand2",
            padx=16, pady=8, command=self._al_nueva_cita
        ).pack(side="left")

        self._area_citas = tk.Frame(cuerpo, bg=COLORES["fondo"])
        self._area_citas.pack(fill="both", expand=True)
        self._cargar_citas()

    def _cargar_citas(self):
        for widget in self._area_citas.winfo_children():
            widget.destroy()

        citas = self._servicio.obtener_mis_citas(self._usuario)

        if self._solo_activas.get():
            citas = [c for c in citas if c.estado == "Programada"]

        if not citas:
            self._mostrar_estado_vacio()
            return

        contenedor = tk.Frame(self._area_citas, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True)

        for cita in citas:
            self._crear_tarjeta_cita(contenedor, cita)

    def _mostrar_estado_vacio(self):
        tk.Label(self._area_citas,
                 text="No tienes citas programadas aún.\nHaz clic en '+ Nueva Cita' para agendar.",
                 font=FUENTES["cuerpo"], bg=COLORES["fondo"],
                 fg=COLORES["texto_secundario"], justify="center"
                 ).pack(expand=True, pady=60)

    def _crear_tarjeta_cita(self, padre, cita):
        partes_fecha = cita.fecha.split("-")
        dia = partes_fecha[2] if len(partes_fecha) == 3 else "—"
        mes = MESES.get(partes_fecha[1], "—") if len(partes_fecha) == 3 else "—"
        anio = partes_fecha[0] if len(partes_fecha) == 3 else "—"

        tarjeta = tk.Frame(padre, bg=COLORES["tarjeta"], relief="groove", bd=1)
        tarjeta.pack(side="left", padx=8, pady=4, ipadx=4, ipady=8)

        bloque_fecha = tk.Frame(tarjeta, bg="#EEF2FF")
        bloque_fecha.pack(side="left", fill="y", ipadx=12, ipady=12)

        tk.Label(bloque_fecha, text=mes, font=FUENTES["pequeño"],
                 bg="#EEF2FF", fg=COLORES["primario"]).pack(pady=(8, 0))
        tk.Label(bloque_fecha, text=dia, font=("Segoe UI", 20, "bold"),
                 bg="#EEF2FF", fg=COLORES["texto_principal"]).pack()
        tk.Label(bloque_fecha, text=anio, font=FUENTES["pequeño"],
                 bg="#EEF2FF", fg=COLORES["texto_secundario"]).pack(pady=(0, 8))

        info = tk.Frame(tarjeta, bg=COLORES["tarjeta"])
        info.pack(side="left", padx=12, pady=10)

        fila_nombre = tk.Frame(info, bg=COLORES["tarjeta"])
        fila_nombre.pack(fill="x", pady=(0, 4))
        tk.Label(fila_nombre, text=cita.medico.nombre,
                 font=("Segoe UI", 10, "bold"), bg=COLORES["tarjeta"],
                 fg=COLORES["texto_principal"]).pack(side="left", padx=(0, 10))

        estado_color = COLORES["exito"] if cita.estado == "Programada" else COLORES["error"]
        etiqueta_estado = tk.Label(fila_nombre, text=cita.estado,
                 font=FUENTES["pequeño"], bg=estado_color,
                 fg=COLORES["blanco"], padx=6)
        etiqueta_estado.pack(side="left")

        tk.Label(info, text=cita.medico.especialidad,
                 font=FUENTES["pequeño"], bg=COLORES["tarjeta"],
                 fg=COLORES["primario"]).pack(anchor="w", pady=(0, 6))

        fila_horario = tk.Frame(info, bg=COLORES["tarjeta"])
        fila_horario.pack(anchor="w")
        tk.Label(fila_horario, text=f"🕐 {cita.hora}",
                 font=FUENTES["pequeño"], bg=COLORES["tarjeta"],
                 fg=COLORES["texto_secundario"]).pack(side="left", padx=(0, 12))
        tk.Label(fila_horario, text=f"📍 {cita.medico.sede}",
                 font=FUENTES["pequeño"], bg=COLORES["tarjeta"],
                 fg=COLORES["texto_secundario"]).pack(side="left")

        if cita.estado == "Programada":
            tk.Button(
                info, text="Cancelar cita",
                font=FUENTES["pequeño"], bg=COLORES["error"],
                fg=COLORES["blanco"], relief="flat", cursor="hand2",
                padx=8, pady=4,
                command=lambda c=cita: self._cancelar_cita(c)
            ).pack(anchor="w", pady=(8, 0))

    # ── Acciones ──────────────────────────────────────────────

    def _cancelar_cita(self, cita):
        confirmado = messagebox.askyesno(
            "Cancelar cita",
            f"¿Seguro que deseas cancelar la cita con {cita.medico.nombre} "
            f"el {cita.fecha} a las {cita.hora}?"
        )
        if confirmado:
            cita.cancelar()
            self._cargar_citas()

    def _ir_al_inicio(self):
        if self._al_inicio:
            self._al_inicio()

    def actualizar(self):
        self._cargar_citas()
