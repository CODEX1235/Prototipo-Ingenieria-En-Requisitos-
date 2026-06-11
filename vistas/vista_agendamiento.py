import tkinter as tk
from tkinter import messagebox
import calendar
from datetime import date, datetime
from modelos.usuario import Usuario
from modelos.medico import Medico
from servicios.agendamiento import ServicioAgendamiento
from vistas.estilos import COLORES, FUENTES


class VistaAgendamiento(tk.Frame):
    def __init__(self, padre, servicio: ServicioAgendamiento,
                 usuario: Usuario, al_confirmar):
        super().__init__(padre, bg=COLORES["fondo"])
        self._servicio = servicio
        self._usuario = usuario
        self._al_confirmar = al_confirmar
        self._medico_seleccionado: Medico | None = None
        self._fecha_seleccionada: str = ""
        self._hora_seleccionada: str = ""
        self._anio_actual = date.today().year
        self._mes_actual = date.today().month
        self._construir_interfaz()

    # ── Construcción ──────────────────────────────────────────

    def _construir_interfaz(self):
        self._crear_barra_superior()
        self._crear_area_directorio()

    def _crear_barra_superior(self):
        barra = tk.Frame(self, bg=COLORES["encabezado"], height=60)
        barra.pack(fill="x")
        barra.pack_propagate(False)

        tk.Label(barra, text="❤  Salud EPS  |  Portal Paciente",
                 font=FUENTES["subtitulo"], bg=COLORES["encabezado"],
                 fg=COLORES["blanco"]).pack(side="left", padx=20, pady=15)

        tk.Label(barra, text=self._usuario.nombre,
                 font=FUENTES["etiqueta"], bg=COLORES["encabezado"],
                 fg="#A5C8FF").pack(side="right", padx=20)

    def _crear_area_directorio(self):
        self._panel_principal = tk.Frame(self, bg=COLORES["fondo"])
        self._panel_principal.pack(fill="both", expand=True, padx=30, pady=20)
        self._mostrar_directorio()

    # ── Pantalla 1: Directorio médico ─────────────────────────

    def _mostrar_directorio(self):
        self._limpiar_panel()

        encabezado = tk.Frame(self._panel_principal, bg=COLORES["fondo"])
        encabezado.pack(fill="x", pady=(0, 16))

        tk.Label(encabezado, text="←  Directorio Médico",
                 font=FUENTES["subtitulo"], bg=COLORES["fondo"],
                 fg=COLORES["texto_principal"]).pack(side="left")

        medicos = self._servicio.obtener_medicos()
        for medico in medicos:
            self._crear_tarjeta_medico(medico)

    def _crear_tarjeta_medico(self, medico: Medico):
        tarjeta = tk.Frame(self._panel_principal, bg=COLORES["tarjeta"],
                            relief="flat", bd=1)
        tarjeta.pack(fill="x", pady=6, ipady=12, ipadx=12)

        info = tk.Frame(tarjeta, bg=COLORES["tarjeta"])
        info.pack(side="left", padx=14, fill="x", expand=True)

        tk.Label(info, text=medico.nombre, font=("Segoe UI", 11, "bold"),
                 bg=COLORES["tarjeta"], fg=COLORES["texto_principal"]
                 ).pack(anchor="w")
        tk.Label(info, text=f"★ {medico.calificacion}  •  {medico.especialidad}",
                 font=FUENTES["pequeño"], bg=COLORES["tarjeta"],
                 fg=COLORES["primario"]).pack(anchor="w", pady=2)
        tk.Label(info, text=f"Sede: {medico.sede}",
                 font=FUENTES["pequeño"], bg=COLORES["tarjeta"],
                 fg=COLORES["texto_secundario"]).pack(anchor="w")

        tk.Button(
            tarjeta, text="Ver Agenda Disponible",
            font=FUENTES["etiqueta"], bg=COLORES["primario"],
            fg=COLORES["blanco"], relief="flat", cursor="hand2",
            padx=12, pady=6,
            command=lambda m=medico: self._mostrar_selector_fecha(m)
        ).pack(side="right", padx=14)

    # ── Pantalla 2: Selección de fecha y hora ─────────────────

    def _mostrar_selector_fecha(self, medico: Medico):
        self._medico_seleccionado = medico
        self._limpiar_panel()

        encabezado = tk.Frame(self._panel_principal, bg=COLORES["fondo"])
        encabezado.pack(fill="x", pady=(0, 16))

        tk.Button(encabezado, text="← Volver",
                  font=FUENTES["etiqueta"], bg=COLORES["fondo"],
                  fg=COLORES["primario"], relief="flat", cursor="hand2",
                  command=self._mostrar_directorio).pack(side="left", padx=(0, 16))

        tk.Label(encabezado,
                 text=f"Fecha y Hora de Cita  —  {medico.nombre}",
                 font=FUENTES["subtitulo"], bg=COLORES["fondo"],
                 fg=COLORES["texto_principal"]).pack(side="left")

        contenedor = tk.Frame(self._panel_principal, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True)

        self._crear_calendario(contenedor)
        self._crear_selector_hora(contenedor, medico.horarios)

        tk.Button(
            self._panel_principal, text="Continuar con la Reserva",
            font=FUENTES["boton"], bg=COLORES["primario"],
            fg=COLORES["blanco"], relief="flat", cursor="hand2",
            pady=10, command=self._ir_a_confirmacion
        ).pack(fill="x", pady=(20, 0))

    def _crear_calendario(self, padre):
        panel_cal = tk.Frame(padre, bg=COLORES["tarjeta"], padx=16, pady=16)
        panel_cal.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(panel_cal, text="1. Selecciona el Día",
                 font=("Segoe UI", 10, "bold"), bg=COLORES["tarjeta"],
                 fg=COLORES["texto_principal"]).pack(anchor="w", pady=(0, 10))

        self._frame_cal = tk.Frame(panel_cal, bg=COLORES["tarjeta"])
        self._frame_cal.pack()
        self._renderizar_mes()

    def _renderizar_mes(self):
        for widget in self._frame_cal.winfo_children():
            widget.destroy()

        nombre_mes = calendar.month_name[self._mes_actual].capitalize()
        nav = tk.Frame(self._frame_cal, bg=COLORES["tarjeta"])
        nav.pack(fill="x")

        tk.Button(nav, text="<", font=FUENTES["etiqueta"],
                  bg=COLORES["tarjeta"], fg=COLORES["primario"],
                  relief="flat", cursor="hand2",
                  command=self._mes_anterior).pack(side="left")
        tk.Label(nav, text=f"{nombre_mes} {self._anio_actual}",
                 font=("Segoe UI", 10, "bold"), bg=COLORES["tarjeta"],
                 fg=COLORES["texto_principal"]).pack(side="left", expand=True)
        tk.Button(nav, text=">", font=FUENTES["etiqueta"],
                  bg=COLORES["tarjeta"], fg=COLORES["primario"],
                  relief="flat", cursor="hand2",
                  command=self._mes_siguiente).pack(side="right")

        dias_semana = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"]
        fila_dias = tk.Frame(self._frame_cal, bg=COLORES["tarjeta"])
        fila_dias.pack(fill="x", pady=(8, 4))
        for dia in dias_semana:
            tk.Label(fila_dias, text=dia, width=3,
                     font=FUENTES["pequeño"], bg=COLORES["tarjeta"],
                     fg=COLORES["texto_secundario"]).pack(side="left")

        semanas = calendar.monthcalendar(self._anio_actual, self._mes_actual)
        for semana in semanas:
            fila = tk.Frame(self._frame_cal, bg=COLORES["tarjeta"])
            fila.pack()
            for numero in semana:
                if numero == 0:
                    tk.Label(fila, text="", width=3,
                             bg=COLORES["tarjeta"]).pack(side="left")
                else:
                    self._crear_boton_dia(fila, numero)

    def _crear_boton_dia(self, padre, numero: int):
        fecha_str = f"{self._anio_actual}-{self._mes_actual:02d}-{numero:02d}"
        seleccionado = fecha_str == self._fecha_seleccionada

        btn = tk.Button(
            padre, text=str(numero), width=3,
            font=FUENTES["pequeño"], relief="flat", cursor="hand2",
            bg=COLORES["primario"] if seleccionado else COLORES["tarjeta"],
            fg=COLORES["blanco"] if seleccionado else COLORES["texto_principal"],
            command=lambda f=fecha_str: self._seleccionar_fecha(f)
        )
        btn.pack(side="left", pady=2)

    def _crear_selector_hora(self, padre, horarios: list):
        panel_hora = tk.Frame(padre, bg=COLORES["tarjeta"], padx=16, pady=16)
        panel_hora.pack(side="left", fill="both", expand=True)

        tk.Label(panel_hora, text="2. Selecciona la Hora",
                 font=("Segoe UI", 10, "bold"), bg=COLORES["tarjeta"],
                 fg=COLORES["texto_principal"]).pack(anchor="w", pady=(0, 10))

        self._frame_horas = tk.Frame(panel_hora, bg=COLORES["tarjeta"])
        self._frame_horas.pack(fill="x")
        self._horarios_disponibles = horarios
        self._renderizar_horas()

    def _renderizar_horas(self):
        for widget in self._frame_horas.winfo_children():
            widget.destroy()
        for hora in self._horarios_disponibles:
            seleccionada = hora == self._hora_seleccionada
            tk.Button(
                self._frame_horas, text=hora, width=6,
                font=FUENTES["etiqueta"], relief="flat", cursor="hand2",
                bg=COLORES["primario"] if seleccionada else "#EEF2FF",
                fg=COLORES["blanco"] if seleccionada else COLORES["primario"],
                command=lambda h=hora: self._seleccionar_hora(h)
            ).pack(side="left", padx=4, pady=4, ipady=6)

    # ── Pantalla 3: Confirmación ──────────────────────────────

    def _mostrar_confirmacion(self):
        self._limpiar_panel()

        tk.Label(self._panel_principal,
                 text="Confirmación de Cita",
                 font=FUENTES["titulo"], bg=COLORES["fondo"],
                 fg=COLORES["texto_principal"]).pack(anchor="w", pady=(0, 4))
        tk.Label(self._panel_principal,
                 text="Por favor verifica los datos antes de finalizar",
                 font=FUENTES["pequeño"], bg=COLORES["fondo"],
                 fg=COLORES["texto_secundario"]).pack(anchor="w", pady=(0, 16))

        resumen = tk.Frame(self._panel_principal, bg=COLORES["primario"],
                            padx=20, pady=16)
        resumen.pack(fill="x", pady=(0, 12))

        tk.Label(resumen, text="Resumen de la Atención",
                 font=("Segoe UI", 10, "bold"), bg=COLORES["primario"],
                 fg=COLORES["blanco"]).pack(anchor="w", pady=(0, 12))

        columnas = tk.Frame(resumen, bg=COLORES["primario"])
        columnas.pack(fill="x")

        col_paciente = tk.Frame(columnas, bg=COLORES["primario"])
        col_paciente.pack(side="left", expand=True, anchor="w")
        tk.Label(col_paciente, text="DATOS DEL PACIENTE",
                 font=FUENTES["pequeño"], bg=COLORES["primario"],
                 fg="#A5C8FF").pack(anchor="w")
        tk.Label(col_paciente, text=self._usuario.nombre,
                 font=("Segoe UI", 11, "bold"), bg=COLORES["primario"],
                 fg=COLORES["blanco"]).pack(anchor="w")
        tk.Label(col_paciente,
                 text=f"{self._usuario.tipo_documento}: {self._usuario.numero_documento}",
                 font=FUENTES["pequeño"], bg=COLORES["primario"],
                 fg="#A5C8FF").pack(anchor="w")
        tk.Label(col_paciente, text=self._usuario.plan,
                 font=FUENTES["pequeño"], bg="#1544B8",
                 fg=COLORES["blanco"], padx=6, pady=2).pack(anchor="w", pady=(4, 0))

        col_medico = tk.Frame(columnas, bg=COLORES["primario"])
        col_medico.pack(side="left", expand=True, anchor="w")
        tk.Label(col_medico, text="PROFESIONAL DE LA SALUD",
                 font=FUENTES["pequeño"], bg=COLORES["primario"],
                 fg="#A5C8FF").pack(anchor="w")
        tk.Label(col_medico, text=self._medico_seleccionado.nombre,
                 font=("Segoe UI", 11, "bold"), bg=COLORES["primario"],
                 fg=COLORES["blanco"]).pack(anchor="w")
        tk.Label(col_medico, text=self._medico_seleccionado.especialidad,
                 font=FUENTES["pequeño"], bg=COLORES["primario"],
                 fg="#A5C8FF").pack(anchor="w")

        detalle = tk.Frame(self._panel_principal, bg=COLORES["tarjeta"],
                            padx=20, pady=16)
        detalle.pack(fill="x", pady=(0, 12))

        tk.Label(detalle, text="Detalles del Agendamiento",
                 font=("Segoe UI", 10, "bold"), bg=COLORES["tarjeta"],
                 fg=COLORES["texto_principal"]).pack(anchor="w", pady=(0, 10))

        fila_detalles = tk.Frame(detalle, bg=COLORES["tarjeta"])
        fila_detalles.pack(fill="x")

        self._dato_icono(fila_detalles, "📅", "FECHA", self._fecha_seleccionada)
        self._dato_icono(fila_detalles, "🕐", "HORA", self._hora_seleccionada)
        self._dato_icono(fila_detalles, "📍", "LUGAR",
                         self._medico_seleccionado.sede)

        aviso = tk.Frame(self._panel_principal, bg=COLORES["fondo"])
        aviso.pack(fill="x", pady=(0, 8))
        tk.Label(aviso,
                 text="✅ Al confirmar, aceptas los términos del servicio. "
                      "Recuerda llegar 15 minutos antes.",
                 font=FUENTES["pequeño"], bg=COLORES["fondo"],
                 fg=COLORES["texto_secundario"], wraplength=420,
                 justify="left").pack(side="left", fill="x", expand=True)

        tk.Button(
            self._panel_principal, text="Confirmar y Agendar",
            font=FUENTES["boton"], bg=COLORES["primario"],
            fg=COLORES["blanco"], relief="flat", cursor="hand2",
            pady=10, command=self._confirmar_cita
        ).pack(fill="x")

    def _dato_icono(self, padre, icono: str, etiqueta: str, valor: str):
        bloque = tk.Frame(padre, bg=COLORES["tarjeta"])
        bloque.pack(side="left", expand=True)
        tk.Label(bloque, text=icono, font=FUENTES["subtitulo"],
                 bg=COLORES["tarjeta"]).pack()
        tk.Label(bloque, text=etiqueta, font=FUENTES["pequeño"],
                 bg=COLORES["tarjeta"], fg=COLORES["texto_secundario"]).pack()
        tk.Label(bloque, text=valor, font=("Segoe UI", 10, "bold"),
                 bg=COLORES["tarjeta"], fg=COLORES["texto_principal"]).pack()

    # ── Acciones ──────────────────────────────────────────────

    def _seleccionar_fecha(self, fecha: str):
        self._fecha_seleccionada = fecha
        self._renderizar_mes()

    def _seleccionar_hora(self, hora: str):
        self._hora_seleccionada = hora
        self._renderizar_horas()

    def _mes_anterior(self):
        if self._mes_actual == 1:
            self._mes_actual = 12
            self._anio_actual -= 1
        else:
            self._mes_actual -= 1
        self._renderizar_mes()

    def _mes_siguiente(self):
        if self._mes_actual == 12:
            self._mes_actual = 1
            self._anio_actual += 1
        else:
            self._mes_actual += 1
        self._renderizar_mes()

    def _ir_a_confirmacion(self):
        if not self._fecha_seleccionada:
            messagebox.showwarning("Falta información", "Selecciona una fecha.")
            return
        if not self._hora_seleccionada:
            messagebox.showwarning("Falta información", "Selecciona una hora.")
            return
        self._mostrar_confirmacion()

    def _confirmar_cita(self):
        exito, mensaje, cita = self._servicio.agendar_cita(
            self._usuario,
            self._medico_seleccionado,
            self._fecha_seleccionada,
            self._hora_seleccionada
        )
        if exito:
            messagebox.showinfo("Cita confirmada", mensaje)
            self._al_confirmar()
        else:
            messagebox.showerror("Error", mensaje)

    def _limpiar_panel(self):
        for widget in self._panel_principal.winfo_children():
            widget.destroy()
