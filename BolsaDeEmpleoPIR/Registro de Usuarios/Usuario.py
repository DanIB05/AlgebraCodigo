from tkinter import messagebox
import bcrypt
import uuid
import re

class Usuario:
    def __init__(self, nombre, apellido, direccion, contraseña, habilidades=None, experiencia=None, educacion=None, portafolio=None, disponibilidad=None, salario_esperado=None, informacion_relevante=None, redes_sociales=None):
        self.id = uuid.uuid4()
        self.nombre = self._validar_nombre(nombre)
        self.apellido = self._validar_nombre(apellido)
        self.direccion = direccion
        self.usuario = self._generar_usuario(nombre, apellido)
        self.contraseña_hash = self._hashear_contraseña(contraseña)
        self.habilidades = habilidades if habilidades else []
        self.experiencia = experiencia if experiencia else []
        self.educacion = educacion if educacion else []
        self.portafolio = portafolio
        self.disponibilidad = disponibilidad
        self.salario_esperado = salario_esperado
        self.informacion_relevante = informacion_relevante
        self.redes_sociales = redes_sociales if redes_sociales else {}
        self.porcentaje_completitud_perfil = self._calcular_completitud_perfil()

    def _validar_nombre(self, nombre):
        if not nombre or not re.match(r"^[a-zA-Z\s]+$", nombre):
            raise ValueError("El nombre debe contener solo letras y espacios.")
        return nombre.strip()

    def _generar_usuario(self, nombre, apellido):
        base_usuario = f"{nombre.lower()}.{apellido.lower()}"
        return base_usuario

    def _hashear_contraseña(self, contraseña):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def verificar_contraseña(self, contraseña):
        return bcrypt.checkpw(contraseña.encode('utf-8'), self.contraseña_hash.encode('utf-8'))

    def _calcular_completitud_perfil(self):
        total_campos = 7
        campos_completos = 5
        if self.habilidades: campos_completos += 1
        if self.experiencia: campos_completos += 1
        if self.educacion: total_campos += 1; campos_completos += 1
        if self.portafolio: total_campos += 1; campos_completos += 1
        if self.disponibilidad: total_campos += 1; campos_completos += 1
        if self.salario_esperado: total_campos += 1; campos_completos += 1
        if self.informacion_relevante: total_campos += 1; campos_completos += 1
        if self.redes_sociales: total_campos += len(self.redes_sociales); campos_completos += len(self.redes_sociales)
        return (campos_completos / total_campos) * 100 if total_campos > 0 else 0

    def actualizar_informacion(self, nueva_informacion):
        for key, value in nueva_informacion.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.porcentaje_completitud_perfil = self._calcular_completitud_perfil()

    def obtener_info_perfil(self):
        return {
            "Nombre": f"{self.nombre} {self.apellido}",
            "Dirección": self.direccion,
            "Usuario": self.usuario,
            "Habilidades": ", ".join(self.habilidades) if self.habilidades else "No especificado",
            "Experiencia": "\n".join(self.experiencia) if self.experiencia else "No especificada",
            "Educación": ", ".join(self.educacion) if self.educacion else "No especificada",
            "Portafolio": self.portafolio if self.portafolio else "No especificado",
            "Disponibilidad": self.disponibilidad if self.disponibilidad else "No especificada",
            "Salario Esperado": self.salario_esperado if self.salario_esperado else "No especificado",
            "Información Relevante": self.informacion_relevante if self.informacion_relevante else "No especificada",
            "Redes Sociales": "\n".join([f"{red}: {link}" for red, link in self.redes_sociales.items()]) if self.redes_sociales else "No especificadas"
        }