from mongoengine import Document, StringField, ReferenceField, DateTimeField, FileField
from datetime import datetime

class Instructor(Document):
    nombre = StringField(required=True)
    correo = StringField(required=True, unique=True)
    regional = StringField(required=True, choices=['Cauca', 'Huila', 'Antioquia', 'Valle', 'Nariño'])
    usuario = StringField(required=True, unique=True)
    contraseña = StringField(required=True)

class GuiaAprendizaje(Document):
    nombre = StringField(required=True)
    descripcion = StringField(required=True)
    programa = StringField(required=True, choices=[
        'Desarrollo de Software', 'Multimedia', 'Inteligencia Artificial', 
        'Analítica de Datos', 'Construcción', 'Contabilidad'
    ])
    archivo_pdf = FileField(required=True)
    fecha_subida = DateTimeField(default=datetime.utcnow)
    instructor = ReferenceField(Instructor, required=True)
