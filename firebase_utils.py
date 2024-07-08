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

def obtener_grupos():
    ref_grupos = db.reference('Grupos')
    return ref_grupos.get()

def actualizar_hito_grupo(hito_id, grupo_id,cumplido, sprint_id):
    
    ref_hito = db.reference(f'Grupos/{grupo_id}/sprints/{sprint_id}/hitos/{hito_id}')
    ref_hito.update({
        'cumplido': cumplido
    })

def obtener_hitos_grupo(grupo_id,sprint_id):
    ref_hitos = db.reference(f'Grupos/{grupo_id}/sprints/{sprint_id}/hitos')
    return ref_hitos.get()

def obtener_hitos_sprint(grupo_id):
    ref_sprints = db.reference(f'Grupos/{grupo_id}/sprints')
    #Obtener los sprints del grupo,solo los que tengan cumplimento false
    sprints = ref_sprints.get()
    sprints_no_cumplidos = {}
    if sprints:
        for sprint_id, sprint_info in sprints.items():
            if not sprint_info.get('cumplido', False):
                sprints_no_cumplidos[sprint_id] = sprint_info
    return sprints_no_cumplidos
    

def obtener_sprints_con_hitos(grupo_id):
    ref_sprints = db.reference(f'Grupos/{grupo_id}/sprints')
    sprints_con_hitos = []

    sprints_data = ref_sprints.get()
    if sprints_data:
        for sprint_id, sprint_info in sprints_data.items():

            hitos_sprint = []
            ref_hitos = db.reference(f'Grupos/{grupo_id}/sprints/{sprint_id}/hitos')
            hitos_data = ref_hitos.get()
            if hitos_data:
                for hito_id, hito_info in hitos_data.items():
                    hito = hito_info.get('hito')
                    cumplido = hito_info.get('cumplido', False)
                    hitos_sprint.append((hito, cumplido))
            sprints_con_hitos.append((sprint_info.get('sprint'), hitos_sprint))

    return sprints_con_hitos

def actualizar_sprint(grupo_id, sprint_id):
    ref_sprint = db.reference(f'Grupos/{grupo_id}/sprints/{sprint_id}')
    ref_sprint.update({
        'cumplido': True
    })


def obtener_grupo_id(nombreGrupo):
    ref_grupos = db.reference('Grupos')
    grupos = ref_grupos.get()
    if grupos:
        for grupo_id, grupo_info in grupos.items():
            if grupo_info.get('nombreGrupo') == nombreGrupo:
                return grupo_id
    return None

def eliminar_grupo(grupo_id):
    ref_grupo = db.reference(f'Grupos/{grupo_id}')
    ref_grupo.delete()