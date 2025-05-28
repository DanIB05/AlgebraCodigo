from tkinter import messagebox
import bcrypt
import uuid
import re

class Empresa:
    def __init__(self, nombre_empresa: str, direccion, telefono, dueño_nombre: str, dueño_info, contacto_nombre: str, contacto_info, sector=None, tamaño=None, cultura=None, sitio_web=None, redes_sociales=None):
        self.id = uuid.uuid4()
        self.nombre_empresa = nombre_empresa
        self.direccion = direccion
        self.telefono = telefono
        self.sector = sector
        self.tamaño = tamaño
        self.cultura = cultura
        self.sitio_web = sitio_web
        self.redes_sociales = redes_sociales if redes_sociales else {}
        self.dueño_nombre = self._validar_nombre(dueño_nombre)
        self.dueño_info = dueño_info
        self.contacto_nombre = self._validar_nombre(contacto_nombre)
        self.contacto_info = contacto_info
        self.usuario = self._generar_usuario(nombre_empresa)
        self.contraseña_hash = self._hashear_contraseña("contraseña_inicial_empresa")
        self.porcentaje_completitud_perfil = self._calcular_completitud_perfil()

    def _validar_nombre(self, nombre_empresa):
        if not nombre_empresa or not re.match(r"^[a-zA-Z\s]+$", nombre_empresa):
            raise ValueError("El nombre debe contener solo letras y espacios.")
        return nombre_empresa.strip()

    def _generar_usuario(self, nombre_empresa):
        base_usuario = f"{nombre_empresa.lower().replace(' ', '_')}"
        return base_usuario

    def _hashear_contraseña(self, contraseña):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def verificar_contraseña(self, contraseña):
        return bcrypt.checkpw(contraseña.encode('utf-8'), self.contraseña_hash.encode('utf-8'))

    def _calcular_completitud_perfil(self):
        total_campos = 7
        campos_completos = 7
        if self.sector: total_campos += 1; campos_completos += 1
        if self.tamaño: total_campos += 1; campos_completos += 1
        if self.cultura: total_campos += 1; campos_completos += 1
        if self.sitio_web: total_campos += 1; campos_completos += 1
        if self.redes_sociales: total_campos += len(self.redes_sociales); campos_completos += len(self.redes_sociales)
        return (campos_completos / total_campos) * 100 if total_campos > 0 else 0

    def actualizar_informacion(self, nueva_informacion):
        for key, value in nueva_informacion.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.porcentaje_completitud_perfil = self._calcular_completitud_perfil()

    def obtener_info_perfil(self):
        return {
            "Nombre de la Empresa": self.nombre_empresa,
            "Dirección": self.direccion,
            "Teléfono": self.telefono,
            "Sector": self.sector if self.sector else "No especificado",
            "Tamaño": self.tamaño if self.tamaño else "No especificado",
            "Cultura de la Empresa": self.cultura if self.cultura else "No especificada",
            "Sitio Web": self.sitio_web if self.sitio_web else "No especificado",
            "Redes Sociales": "\n".join([f"{red}: {link}" for red, link in self.redes_sociales.items()]) if self.redes_sociales else "No especificadas",
            "Información del Dueño": f"{self.dueño_nombre} - {self.dueño_info}",
            "Contacto en la App": f"{self.contacto_nombre} - {self.contacto_info}",
            "Usuario": self.usuario
        }