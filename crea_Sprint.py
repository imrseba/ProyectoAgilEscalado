import streamlit as st
from firebase_utils import crear_sprint_grupo, obtener_grupos

def crear_sprint_app():
    st.title("Crear Nuevo Sprint")

    grupos = obtener_grupos()
    grupo_names = [grupo['nombreGrupo'] for grupo in grupos.values()] if grupos else []

    st.subheader("Seleccione el grupo al que desea agregar un Sprint:")
    selected_grupo = st.selectbox("Selecciona un Grupo:", grupo_names)

    if selected_grupo:
        grupo_id = next((key for key, value in grupos.items() if value['nombreGrupo'] == selected_grupo), None)
        
        # Generar una clave única para el input de texto del sprint
        sprint_input_key = f"sprint_input_{grupo_id}"

        nuevo_Sprint = st.text_input("Nuevo Sprint:", key=sprint_input_key)

        # Generar una clave única para el botón de agregar sprint
        agregar_sprint_button_key = f"agregar_sprint_button_{grupo_id}"

        if st.button("Agregar Sprint", key=agregar_sprint_button_key):
            if nuevo_Sprint:
                crear_sprint_grupo(nuevo_Sprint, grupo_id)
                st.success("¡Sprint agregado exitosamente!")
            else:
                st.error("Por favor, ingrese el nombre del Sprint.")


