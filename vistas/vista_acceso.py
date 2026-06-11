import tkinter as tk
from tkinter import ttk, messagebox
from servicios.autenticacion import ServicioAutenticacion
from vistas.estilos import COLORES, FUENTES, DIMENSIONES


class VistaAcceso(tk.Frame):
    TIPOS_DOCUMENTO = ["CC", "TI", "CE", "Pasaporte"]

    def __init__(self, padre, servicio_auth: ServicioAutenticacion, al_ingresar):
        super().__init__(padre, bg=COLORES["fondo"])
        self._servicio = servicio_auth
        self._al_ingresar = al_ingresar
        self._modo_login = True
        self._construir_interfaz()

    # ── Construcción ──────────────────────────────────────────

    def _construir_interfaz(self):
        self._crear_encabezado()
        self._crear_tarjeta_central()

    def _crear_encabezado(self):
        encabezado = tk.Frame(self, bg=COLORES["encabezado"], height=60)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        tk.Label(encabezado, text="❤  Salud EPS",
                 font=FUENTES["subtitulo"], bg=COLORES["encabezado"],
                 fg=COLORES["blanco"]).pack(side="left", padx=20, pady=15)

        tk.Label(encabezado, text="Portal Paciente",
                 font=FUENTES["pequeño"], bg=COLORES["encabezado"],
                 fg="#A5C8FF").pack(side="left")

    def _crear_tarjeta_central(self):
        contenedor = tk.Frame(self, bg=COLORES["fondo"])
        contenedor.pack(expand=True, fill="both", pady=30)

        self._tarjeta = tk.Frame(contenedor, bg=COLORES["tarjeta"],
                                  relief="flat", bd=0)
        self._tarjeta.place(relx=0.5, rely=0.5, anchor="center",
                             width=360, height=520)

        self._crear_sombra_tarjeta()
        self._crear_contenido_tarjeta()

    def _crear_sombra_tarjeta(self):
        sombra = tk.Frame(self._tarjeta.master, bg="#E2E8F0")
        sombra.place(relx=0.5, rely=0.5, anchor="center", width=364, height=524)
        self._tarjeta.lift()

    def _crear_contenido_tarjeta(self):
        cabecera = tk.Frame(self._tarjeta, bg=COLORES["primario"], height=90)
        cabecera.pack(fill="x")
        cabecera.pack_propagate(False)

        tk.Label(cabecera, text="Portal Paciente",
                 font=FUENTES["titulo"], bg=COLORES["primario"],
                 fg=COLORES["blanco"]).pack(pady=(18, 2))
        tk.Label(cabecera, text="Ingresa a tu cuenta para continuar",
                 font=FUENTES["pequeño"], bg=COLORES["primario"],
                 fg="#A5C8FF").pack()

        self._crear_pestanas()
        self._contenido_formulario = tk.Frame(self._tarjeta, bg=COLORES["tarjeta"])
        self._contenido_formulario.pack(fill="both", expand=True, padx=24, pady=10)
        self._mostrar_login()

    def _crear_pestanas(self):
        pestanas = tk.Frame(self._tarjeta, bg=COLORES["tarjeta"])
        pestanas.pack(fill="x", padx=24, pady=(12, 0))

        self._btn_login = tk.Button(
            pestanas, text="→  Iniciar Sesión",
            font=FUENTES["etiqueta"], relief="flat", cursor="hand2",
            command=self._cambiar_a_login
        )
        self._btn_login.pack(side="left", expand=True, fill="x", pady=6)

        self._btn_registro = tk.Button(
            pestanas, text="☺  Registrarse",
            font=FUENTES["etiqueta"], relief="flat", cursor="hand2",
            command=self._cambiar_a_registro
        )
        self._btn_registro.pack(side="left", expand=True, fill="x", pady=6)

        self._linea_pestana = tk.Frame(pestanas, height=2, bg=COLORES["primario"])
        self._linea_pestana.place(x=0, y=30, relwidth=0.5)
        self._actualizar_pestanas()

    # ── Formularios ───────────────────────────────────────────

    def _mostrar_login(self):
        self._limpiar_formulario()
        self._modo_login = True
        self._actualizar_pestanas()

        self._tipo_doc_var = tk.StringVar(value="CC")
        self._crear_fila_documento(self._contenido_formulario,
                                    self._tipo_doc_var, "numero_doc_login")

        self._crear_campo_contrasena(self._contenido_formulario)

        tk.Button(
            self._contenido_formulario, text="Ingresar al Portal",
            font=FUENTES["boton"], bg=COLORES["primario"], fg=COLORES["blanco"],
            relief="flat", cursor="hand2", pady=10,
            command=self._ejecutar_login
        ).pack(fill="x", pady=(16, 0))

    def _mostrar_registro(self):
        self._limpiar_formulario()
        self._modo_login = False
        self._actualizar_pestanas()

        self._crear_campo_texto(self._contenido_formulario,
                                 "Nombre completo", "nombre_reg", "Ej. Juan Pérez")
        self._tipo_doc_reg_var = tk.StringVar(value="CC")
        self._crear_fila_documento(self._contenido_formulario,
                                    self._tipo_doc_reg_var, "numero_doc_reg")
        self._crear_campo_texto(self._contenido_formulario,
                                 "Correo electrónico", "correo_reg",
                                 "tu@correo.com")
        self._crear_campo_contrasena(self._contenido_formulario, clave="contrasena_reg")

        tk.Button(
            self._contenido_formulario, text="Crear Cuenta",
            font=FUENTES["boton"], bg=COLORES["primario"], fg=COLORES["blanco"],
            relief="flat", cursor="hand2", pady=10,
            command=self._ejecutar_registro
        ).pack(fill="x", pady=(12, 0))

    def _crear_campo_texto(self, padre, etiqueta: str,
                            clave: str, placeholder: str = ""):
        tk.Label(padre, text=etiqueta, font=FUENTES["etiqueta"],
                 bg=COLORES["tarjeta"], fg=COLORES["texto_principal"]
                 ).pack(anchor="w", pady=(8, 2))
        entrada = tk.Entry(padre, font=FUENTES["cuerpo"], relief="flat",
                           bg="#F9FAFB", fg=COLORES["texto_secundario"],
                           insertbackground=COLORES["primario"])
        entrada.insert(0, placeholder)
        entrada.bind("<FocusIn>",
                     lambda e, en=entrada, ph=placeholder: self._limpiar_placeholder(e, en, ph))
        entrada.pack(fill="x", ipady=8,
                     padx=0, pady=0)
        tk.Frame(padre, height=1, bg=COLORES["borde"]).pack(fill="x")
        setattr(self, f"_campo_{clave}", entrada)

    def _crear_fila_documento(self, padre, tipo_var: tk.StringVar, clave_numero: str):
        fila_etiquetas = tk.Frame(padre, bg=COLORES["tarjeta"])
        fila_etiquetas.pack(fill="x", pady=(8, 2))
        tk.Label(fila_etiquetas, text="Tipo doc.", font=FUENTES["etiqueta"],
                 bg=COLORES["tarjeta"], fg=COLORES["texto_principal"]
                 ).pack(side="left", expand=True, anchor="w")
        tk.Label(fila_etiquetas, text="Número de documento",
                 font=FUENTES["etiqueta"],
                 bg=COLORES["tarjeta"], fg=COLORES["texto_principal"]
                 ).pack(side="left", expand=True, anchor="w")

        fila = tk.Frame(padre, bg=COLORES["tarjeta"])
        fila.pack(fill="x")

        combo = ttk.Combobox(fila, textvariable=tipo_var,
                              values=self.TIPOS_DOCUMENTO,
                              width=6, state="readonly",
                              font=FUENTES["cuerpo"])
        combo.pack(side="left", ipady=6, padx=(0, 8))

        entrada = tk.Entry(fila, font=FUENTES["cuerpo"], relief="flat",
                           bg="#F9FAFB", fg=COLORES["texto_secundario"],
                           insertbackground=COLORES["primario"])
        entrada.insert(0, "Ej. 1234567890")
        entrada.bind("<FocusIn>",
                     lambda e, en=entrada: self._limpiar_placeholder(e, en, "Ej. 1234567890"))
        entrada.pack(side="left", fill="x", expand=True, ipady=6)
        tk.Frame(padre, height=1, bg=COLORES["borde"]).pack(fill="x")
        setattr(self, f"_campo_{clave_numero}", entrada)

    def _crear_campo_contrasena(self, padre, clave: str = "contrasena"):
        tk.Label(padre, text="Contraseña", font=FUENTES["etiqueta"],
                 bg=COLORES["tarjeta"], fg=COLORES["texto_principal"]
                 ).pack(anchor="w", pady=(8, 2))
        entrada = tk.Entry(padre, font=FUENTES["cuerpo"], relief="flat",
                           bg="#F9FAFB", fg=COLORES["texto_principal"],
                           show="•", insertbackground=COLORES["primario"])
        entrada.pack(fill="x", ipady=8)
        tk.Frame(padre, height=1, bg=COLORES["borde"]).pack(fill="x")
        setattr(self, f"_campo_{clave}", entrada)

    # ── Acciones ──────────────────────────────────────────────

    def _ejecutar_login(self):
        tipo = self._tipo_doc_var.get()
        numero = self._obtener_valor("numero_doc_login", "Ej. 1234567890")
        contrasena = self._campo_contrasena.get()

        exito, mensaje, usuario = self._servicio.iniciar_sesion(tipo, numero, contrasena)
        if exito:
            self._al_ingresar(usuario)
        else:
            messagebox.showerror("Error de acceso", mensaje)

    def _ejecutar_registro(self):
        nombre = self._obtener_valor("nombre_reg", "Ej. Juan Pérez")
        tipo = self._tipo_doc_reg_var.get()
        numero = self._obtener_valor("numero_doc_reg", "Ej. 1234567890")
        correo = self._obtener_valor("correo_reg", "tu@correo.com")
        contrasena = self._campo_contrasena_reg.get()

        exito, mensaje = self._servicio.registrar(nombre, tipo, numero,
                                                   correo, contrasena)
        if exito:
            messagebox.showinfo("Cuenta creada", mensaje)
            self._cambiar_a_login()
        else:
            messagebox.showerror("Error al registrarse", mensaje)

    # ── Helpers ───────────────────────────────────────────────

    def _obtener_valor(self, clave: str, placeholder: str) -> str:
        campo = getattr(self, f"_campo_{clave}", None)
        if campo is None:
            return ""
        valor = campo.get().strip()
        return "" if valor == placeholder else valor

    def _limpiar_placeholder(self, evento, entrada: tk.Entry, placeholder: str):
        if entrada.get() == placeholder:
            entrada.delete(0, "end")
            entrada.config(fg=COLORES["texto_principal"])

    def _limpiar_formulario(self):
        for widget in self._contenido_formulario.winfo_children():
            widget.destroy()

    def _cambiar_a_login(self):
        self._mostrar_login()

    def _cambiar_a_registro(self):
        self._mostrar_registro()

    def _actualizar_pestanas(self):
        if self._modo_login:
            self._btn_login.config(fg=COLORES["primario"],
                                    bg=COLORES["tarjeta"], font=("Segoe UI", 10, "bold"))
            self._btn_registro.config(fg=COLORES["texto_secundario"],
                                       bg=COLORES["tarjeta"], font=FUENTES["etiqueta"])
        else:
            self._btn_registro.config(fg=COLORES["primario"],
                                       bg=COLORES["tarjeta"], font=("Segoe UI", 10, "bold"))
            self._btn_login.config(fg=COLORES["texto_secundario"],
                                    bg=COLORES["tarjeta"], font=FUENTES["etiqueta"])
