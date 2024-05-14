import streamlit as st
from firebase_utils import crear_Grupos

def crear_grupo():
    with st.sidebar.form("crear_grupo_form"):
        # Campos de entrada dentro del formulario
        nombre_grupo = st.text_input("Nombre del Grupo:")
        descripcion_grupo = st.text_area("Descripción del Grupo:")
        miembros_grupo = st.text_area("Miembros del Grupo:")
        correo_grupo = st.text_area("Correo del Grupo:")
        # Botón para enviar el formulario (crear grupo)
        submit_button = st.form_submit_button("crear Grupo")

        # Manejar la lógica cuando se envía el formulario
        if submit_button and nombre_grupo and descripcion_grupo and miembros_grupo and correo_grupo:
            crear_Grupos(nombre_grupo, descripcion_grupo, miembros_grupo, correo_grupo)
            st.success(f"¡Grupo '{nombre_grupo}' creado correctamente!") 
    