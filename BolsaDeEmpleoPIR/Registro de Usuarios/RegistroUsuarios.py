from tkinter import Tk, Label, Entry, Button, Frame, messagebox, Text, DISABLED, END
from tkinter import ttk
import bcrypt
import uuid
import re
from Usuario import Usuario
from Empresa import Empresa

# --- Definición de Estilos ---
BG_COLOR = "#2c3e50"
FG_COLOR = "#ecf0f1"
FONT = ("Arial", 12)
TITLE_FONT = ("Arial", 16, "bold")

# --- Almacenamiento de Datos (Simulación en Memoria) ---
usuarios = {}
empresas = {}
usuario_actual = None
empresa_actual = None

class Registro_usuarios:
    def __init__(self, root):
        self.root = root
        root.title("App de Conexión Laboral")
        root.geometry("400x350")
        root.configure(bg=BG_COLOR)
        self.mostrar_inicio()

    def registrar_usuario(self, nombre_entry: str, apellido_entry: str, direccion_entry, contraseña_entry):
        nombre = nombre_entry.get()
        apellido = apellido_entry.get()
        direccion = direccion_entry.get()
        contraseña = contraseña_entry.get()

        if not nombre.isalpha():
            messagebox.showerror("Error de Nombre", "El nombre debe contener solo letras.")
            return None
        if not apellido.isalpha():
            messagebox.showerror("Error de Apellido", "El apellido debe contener solo letras.")
            return None

        try:
            nuevo_usuario = Usuario(nombre, apellido, direccion, contraseña)
            if nuevo_usuario.usuario in usuarios:
                messagebox.showerror("Error", "El nombre de usuario ya existe.")
                return None
            usuarios[nuevo_usuario.usuario] = nuevo_usuario
            messagebox.showinfo("Registro Exitoso", f"Usuario '{nuevo_usuario.usuario}' registrado exitosamente.")
            self.mostrar_perfil_usuario(nuevo_usuario)
            return nuevo_usuario
        except ValueError as e:
            messagebox.showerror("Error de Registro", str(e))
            return None

    def registrar_empresa(self, nombre_empresa_entry: str, direccion_entry, telefono_entry, dueño_nombre_entry: str, dueño_info_entry, contacto_nombre_entry: str, contacto_info_entry):
        nombre_empresa = nombre_empresa_entry.get()
        direccion = direccion_entry.get()
        telefono = telefono_entry.get()
        dueño_nombre = dueño_nombre_entry.get()
        dueño_info = dueño_info_entry.get()
        contacto_nombre = contacto_nombre_entry.get()
        contacto_info = contacto_info_entry.get()
        # Usar el nombre de la empresa como nombre de usuario único (puedes modificar esto según tu lógica)
        usuario_empresa = nombre_empresa.replace(" ", "_").lower()
        try:
            nueva_empresa = Empresa(usuario_empresa, nombre_empresa, direccion, telefono, dueño_nombre, dueño_info, contacto_nombre, contacto_info)
            if nueva_empresa.usuario in empresas:
                messagebox.showerror("Error", "El nombre de usuario de la empresa ya existe.")
                return None
            empresas[nueva_empresa.usuario] = nueva_empresa
            messagebox.showinfo("Registro Exitoso", f"Empresa '{nueva_empresa.usuario}' registrada exitosamente.")
            self.mostrar_perfil_empresa(nueva_empresa)
            return nueva_empresa
        except ValueError as e:
            messagebox.showerror("Error de Registro", str(e))
            return None 

    def iniciar_sesion(self, usuario_entry, contraseña_entry):
        usuario = usuario_entry.get()
        contraseña = contraseña_entry.get()
        if usuario in usuarios:
            if usuarios[usuario].verificar_contraseña(contraseña):
                messagebox.showinfo("Inicio de Sesión", f"Inicio de sesión exitoso para el usuario: {usuario}")
                global usuario_actual
                usuario_actual = usuarios[usuario]
                self.mostrar_perfil_usuario(usuario_actual)
                return usuario_actual
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return None
        elif usuario in empresas:
            if empresas[usuario].verificar_contraseña(contraseña):
                messagebox.showinfo("Inicio de Sesión", f"Inicio de sesión exitoso para la empresa: {usuario}")
                global empresa_actual
                empresa_actual = empresas[usuario]
                self.mostrar_perfil_empresa(empresa_actual)
                return empresa_actual
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return None
        else:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return None

    def mostrar_perfil_usuario(self, usuario):
        self.limpiar_pantalla()
        perfil_frame = ttk.Frame(self.root, padding=20)
        perfil_frame.grid(row=0, column=0, sticky="nsew") # Usamos grid aquí
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        ttk.Label(perfil_frame, text="Perfil de Usuario", font=TITLE_FONT, background=BG_COLOR, foreground=FG_COLOR).grid(row=0, column=0, columnspan=2, pady=10)
        info = usuario.obtener_info_perfil()
        row = 1
        for key, value in info.items():
            ttk.Label(perfil_frame, text=f"{key}:", background=BG_COLOR, foreground=FG_COLOR, font=FONT).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            text_widget = Text(perfil_frame, height=1 if "\n" not in value else value.count("\n") + 1, width=40, font=FONT)
            text_widget.insert(END, value)
            text_widget.config(state=DISABLED)
            text_widget.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
            row += 1
        editar_button = ttk.Button(perfil_frame, text="Editar Perfil", command=lambda: self.mostrar_editar_perfil("usuario", usuario))
        editar_button.grid(row=row, column=0, columnspan=2, pady=10)
        volver_button = ttk.Button(perfil_frame, text="Volver al Inicio", command=self.mostrar_inicio)
        volver_button.grid(row=row + 1, column=0, columnspan=2, pady=5)

    def mostrar_perfil_empresa(self, empresa):
        self.limpiar_pantalla()
        perfil_frame = ttk.Frame(self.root, padding=20)
        perfil_frame.grid(row=0, column=0, sticky="nsew") # Usamos grid aquí
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        ttk.Label(perfil_frame, text="Perfil de Empresa", font=TITLE_FONT, background=BG_COLOR, foreground=FG_COLOR).grid(row=0, column=0, columnspan=2, pady=10)
        info = empresa.obtener_info_perfil()
        row = 1
        for key, value in info.items():
            ttk.Label(perfil_frame, text=f"{key}:", background=BG_COLOR, foreground=FG_COLOR, font=FONT).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            text_widget = Text(perfil_frame, height=1 if "\n" not in value else value.count("\n") + 1, width=40, font=FONT)
            text_widget.insert(END, value)
            text_widget.config(state=DISABLED)
            text_widget.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
            row += 1
        editar_button = ttk.Button(perfil_frame, text="Editar Perfil", command=lambda: self.mostrar_editar_perfil("empresa", empresa))
        editar_button.grid(row=row, column=0, columnspan=2, pady=10)
        volver_button = ttk.Button(perfil_frame, text="Volver al Inicio", command=self.mostrar_inicio)
        volver_button.grid(row=row + 1, column=0, columnspan=2, pady=5)

    def mostrar_editar_perfil(self, tipo, entidad):
        self.limpiar_pantalla()
        editar_frame = ttk.Frame(self.root, padding=20)
        editar_frame.grid(row=0, column=0, sticky="nsew") # Usamos grid aquí
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        ttk.Label(editar_frame, text=f"Editar Perfil de {tipo.capitalize()}", font=TITLE_FONT, background=BG_COLOR, foreground=FG_COLOR).grid(row=0, column=0, columnspan=2, pady=10)

        if tipo == "usuario":
            info_actual = entidad.obtener_info_perfil()
            campos_editables = ["Dirección", "Habilidades", "Experiencia", "Educación", "Portafolio", "Disponibilidad", "Salario Esperado", "Información Relevante", "Redes Sociales"]
            labels_map = {
                "Habilidades": "Habilidades (separadas por coma):",
                "Experiencia": "Experiencia (cada entrada en una nueva línea):",
                "Educación": "Educación (separada por coma):",
                "Redes Sociales": "Redes Sociales (formato: Nombre:Link, Nombre:Link):"
            }
        elif tipo == "empresa":
            info_actual = entidad.obtener_info_perfil()
            campos_editables = ["Dirección", "Teléfono", "Sector", "Tamaño", "Cultura de la Empresa", "Sitio Web", "Redes Sociales", "Información del Dueño", "Contacto en la App"]
            labels_map = {
                "Redes Sociales": "Redes Sociales (formato: Nombre:Link, Nombre:Link):",
                "Información del Dueño": "Información del Dueño (Nombre - Info):",
                "Contacto en la App": "Contacto en la App (Nombre - Info):"
            }
        else:
            return

        row = 1 # Empezamos en la fila 1 después del título
        entry_widgets = {}
        for key in campos_editables:
            label_text = labels_map.get(key, f"{key}:")
            ttk.Label(editar_frame, text=label_text, background=BG_COLOR, foreground=FG_COLOR, font=FONT).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            entry = Text(editar_frame, height=1 if "\n" not in info_actual.get(key, "") and ":" not in info_actual.get(key, "") else info_actual.get(key, "").count("\n") + 1, width=40, font=FONT)
            entry.insert(END, info_actual.get(key, ""))
            entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
            entry_widgets[key] = entry
            row += 1

        guardar_button = ttk.Button(editar_frame, text="Guardar Cambios", command=lambda: self.guardar_cambios_perfil(tipo, entidad, entry_widgets))
        guardar_button.grid(row=row, column=0, columnspan=2, pady=10)
        volver_button = ttk.Button(editar_frame, text="Volver al Perfil", command=lambda: self.mostrar_perfil(tipo, entidad))
        volver_button.grid(row=row + 1, column=0, columnspan=2, pady=10)

    def guardar_cambios_perfil(self, tipo, entidad, entry_widgets):
        nuevos_datos = {}
        for key, widget in entry_widgets.items():
            nuevos_datos[key.lower().replace(' ', '_')] = widget.get("1.0", END).strip()

        if tipo == "usuario":
            if "habilidades" in nuevos_datos:
                nuevos_datos["habilidades"] = [h.strip() for h in nuevos_datos["habilidades"].split(',')]
            if "experiencia" in nuevos_datos:
                nuevos_datos["experiencia"] = [exp.strip() for exp in nuevos_datos["experiencia"].split('\n')]
            if "educación" in nuevos_datos:
                nuevos_datos["educacion"] = [edu.strip() for edu in nuevos_datos["educacion"].split(',')]
            if "redes_sociales" in nuevos_datos:
                redes = {}
                for item in nuevos_datos["redes_sociales"].split(','):
                    parts = item.strip().split(':')
                    if len(parts) == 2:
                        redes[parts[0].strip()] = parts[1].strip()
                nuevos_datos["redes_sociales"] = redes
            entidad.actualizar_informacion(nuevos_datos)
            self.mostrar_perfil_usuario(entidad)
        elif tipo == "empresa":
            if "redes_sociales" in nuevos_datos:
                redes = {}
                for item in nuevos_datos["redes_sociales"].split(','):
                    parts = item.strip().split(':')
                    if len(parts) == 2:
                        redes[parts[0].strip()] = parts[1].strip()
                nuevos_datos["redes_sociales"] = redes
            if "información_del_dueño" in nuevos_datos:
                parts = nuevos_datos["información_del_dueño"].split('-')
                if len(parts) == 2:
                    nuevos_datos["dueño_nombre"] = parts[0].strip()
                    nuevos_datos["dueño_info"] = parts[1].strip()
            if "contacto_en_la_app" in nuevos_datos:
                parts = nuevos_datos["contacto_en_la_app"].split('-')
                if len(parts) == 2:
                    nuevos_datos["contacto_nombre"] = parts[0].strip()
                    nuevos_datos["contacto_info"] = parts[1].strip()
                    print(f"Nuevos datos empresa: {nuevos_datos}")
            entidad.actualizar_informacion(nuevos_datos)
            print(f"Información del perfil después de guardar: {entidad.obtener_info_perfil()}")
            self.mostrar_perfil_empresa(entidad)

    def mostrar_perfil(self, tipo, entidad):
        if tipo == "usuario":
            self.mostrar_perfil_usuario(entidad)
        elif tipo == "empresa":
            self.mostrar_perfil_empresa(entidad)

    def mostrar_registro_usuario(self):
        self.limpiar_pantalla()
        registro_frame = ttk.Frame(self.root, padding=20)
        registro_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        ttk.Label(registro_frame, text="Registro de Usuario", font=TITLE_FONT, background=BG_COLOR, foreground=FG_COLOR).grid(row=0, column=0, columnspan=2, pady=10)
        labels = ["Nombre:", "Apellido:", "Dirección:", "Contraseña:"]
        entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(registro_frame, text=label_text, background=BG_COLOR, foreground=FG_COLOR, font=FONT).grid(row=i + 1, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(registro_frame, font=FONT)
            entry.grid(row=i + 1, column=1, sticky="ew", padx=10, pady=5)
            entries[label_text[:-1].lower()] = entry
        registrar_button = ttk.Button(registro_frame, text="Registrar", command=lambda: self.registrar_usuario(entries['nombre'], entries['apellido'], entries['dirección'], entries['contraseña']))
        registrar_button.grid(row=len(labels) + 1 + 1, column=0, columnspan=2, pady=10)
        volver_button = ttk.Button(registro_frame, text="Volver al Inicio", command=self.mostrar_inicio)
        volver_button.grid(row=len(labels) + 2 + 1, column=0, columnspan=2, pady=10)

    def mostrar_registro_empresa(self):
        self.limpiar_pantalla()
        registro_frame = ttk.Frame(self.root, padding=20)
        registro_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        ttk.Label(registro_frame, text="Registro de Empresa", font=TITLE_FONT, background=BG_COLOR, foreground=FG_COLOR).grid(row=0, column=0, columnspan=2, pady=10)
        labels = ["Nombre de la Empresa:", "Dirección:", "Teléfono:", "Nombre del Dueño:", "Información del Dueño:", "Nombre del Contacto:", "Información del Contacto:"]
        entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(registro_frame, text=label_text, background=BG_COLOR, foreground=FG_COLOR, font=FONT).grid(row=i + 1, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(registro_frame, font=FONT)
            entry.grid(row=i + 1, column=1, sticky="ew", padx=10, pady=5)
            entries[label_text[:-1].lower().replace(' ', '_')] = entry
        registrar_button = ttk.Button(registro_frame, text="Registrar", command=lambda: self.registrar_empresa(entries['nombre_de_la_empresa'], entries['dirección'], entries['teléfono'], entries['nombre_del_dueño'], entries['información_del_dueño'], entries['nombre_del_contacto'], entries['información_del_contacto']))
        registrar_button.grid(row=len(labels) + 1 + 1, column=0, columnspan=2, pady=10)
        volver_button = ttk.Button(registro_frame, text="Volver al Inicio", command=self.mostrar_inicio)
        volver_button.grid(row=len(labels) + 2 + 1, column=0, columnspan=2, pady=10)

    def mostrar_inicio_sesion(self):
        self.limpiar_pantalla()
        login_frame = ttk.Frame(self.root, padding=20)
        login_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        ttk.Label(login_frame, text="Inicio de Sesión", font=TITLE_FONT, background=BG_COLOR, foreground=FG_COLOR).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(login_frame, text="Usuario:", background=BG_COLOR, foreground=FG_COLOR, font=FONT).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        usuario_entry = ttk.Entry(login_frame, font=FONT)
        usuario_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        ttk.Label(login_frame, text="Contraseña:", background=BG_COLOR, foreground=FG_COLOR, font=FONT).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        contraseña_entry = ttk.Entry(login_frame, show="*", font=FONT)
        contraseña_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        inicio_sesion_button = ttk.Button(login_frame, text="Iniciar Sesión", command=lambda: self.iniciar_sesion(usuario_entry, contraseña_entry))
        inicio_sesion_button.grid(row=3, column=0, columnspan=2, pady=10)
        volver_button = ttk.Button(login_frame, text="Volver al Inicio", command=self.mostrar_inicio)
        volver_button.grid(row=4, column=0, columnspan=2, pady=10)

    def mostrar_inicio(self):
        self.limpiar_pantalla()
        inicio_frame = ttk.Frame(self.root, padding=20)
        inicio_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        ttk.Label(inicio_frame, text="Bienvenido", font=TITLE_FONT, background=BG_COLOR, foreground=FG_COLOR).grid(row=0, column=0, pady=20)
        registro_usuario_button = ttk.Button(inicio_frame, text="Registrarse como Usuario", command=self.mostrar_registro_usuario)
        registro_usuario_button.grid(row=1, column=0, pady=5, padx=20, sticky="ew")
        registro_empresa_button = ttk.Button(inicio_frame, text="Registrarse como Empresa", command=self.mostrar_registro_empresa)
        registro_empresa_button.grid(row=2, column=0, pady=5, padx=20, sticky="ew")
        inicio_sesion_button = ttk.Button(inicio_frame, text="Iniciar Sesión", command=self.mostrar_inicio_sesion)
        inicio_sesion_button.grid(row=3, column=0, pady=5, padx=20, sticky="ew")

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    app = Registro_usuarios(root)
    root.mainloop()