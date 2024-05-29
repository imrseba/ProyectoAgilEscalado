import streamlit as st
from firebase_utils import crear_hito_grupo, obtener_grupos, obtener_hitos_sprint

def crear_hito_app():
    st.title("Crear Nuevo Hito")

    grupos = obtener_grupos()
    grupo_names = [grupo['nombreGrupo'] for grupo in grupos.values()] if grupos else []

    # Generar una clave única para el selectbox usando el hash de los nombres de grupo
    grupo_selectbox_key = "grupo_selectbox_" + str(hash("".join(grupo_names)))

    st.subheader("Seleccione el grupo al que desea agregar un hito:")
    selected_grupo = st.selectbox("Selecciona un Grupo:", grupo_names, key=grupo_selectbox_key)

    if selected_grupo:
        grupo_id = next((key for key, value in grupos.items() if value['nombreGrupo'] == selected_grupo), None)
        sprints = obtener_hitos_sprint(grupo_id)
        sprint_list = [sprint['sprint'] for sprint in sprints.values()] if sprints else []

        # Generar una clave única para el segundo selectbox usando el hash de los nombres de los sprints
        sprint_selectbox_key = "sprint_selectbox_" + str(hash("".join(sprint_list)))

        st.subheader("Seleccione el sprint al que desea agregar un hito:")
        selected_sprint = st.selectbox("Selecciona un Sprint:", sprint_list, key=sprint_selectbox_key)

        if selected_sprint:
            grupo_id_sprint = next((key for key, value in sprints.items() if value['sprint'] == selected_sprint), None)
            nuevo_hito = st.text_input("Nuevo Hito:", key="hito_input")

            if st.button("Agregar Hito", key="agregar_hito_button"):
                if nuevo_hito:
                    crear_hito_grupo(nuevo_hito, grupo_id, grupo_id_sprint)
                    st.success("¡Hito agregado exitosamente!")
                else:
                    st.error("Por favor, ingrese el nombre del hito.")

