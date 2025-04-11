import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-sena'
    MONGODB_SETTINGS = {
        'db': 'SenaApp',
        'host': 'mongodb+srv://saritabenavides880:UVPtNKRxzK2NhFOb@cluster0.0aodz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',
        'port': 27017
    }