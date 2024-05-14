import firebase_admin
from firebase_admin import credentials, db

def initialize_firebase():
    if not firebase_admin._apps:
        # Ruta al archivo JSON de credenciales de servicio
        firebase_sdk = credentials.Certificate('proyectoagilescalado-firebase-adminsdk-7rd33-f5e91e8997.json')

        # Inicializar la aplicación Firebase solo si no está inicializada
        firebase_admin.initialize_app(firebase_sdk, {'databaseURL': 'https://proyectoagilescalado-default-rtdb.firebaseio.com/'})


def crear_Grupos(nombreGrupo, descripcion, miembros, correo):
    ref = db.reference('Grupos')
    ref.push({
        'nombreGrupo': nombreGrupo,
        'descripcion': descripcion,
        'miembros': miembros,
        'correo': correo
    })

def crear_avanze_grupos(avance,fecha,grupo_id):
    ref_avances = db.reference(f'Grupos/{grupo_id}/avances')
    ref_avances.push({
        'avance': avance,
        'fecha': fecha.isoformat()
    })