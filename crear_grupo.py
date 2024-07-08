import streamlit as st
from firebase_utils import crear_Grupos, obtener_grupo_id
from EmailSender import EmailSender

email_sender = EmailSender(smtp_server='smtp.gmail.com',
                           smtp_port=587,
                           sender_email='mauricie.seba@gmail.com',
                           sender_password='yctj sdjx qols rbdf')

def crear_grupo():
    with st.sidebar.form("crear_grupo_form"):
        # Campos de entrada dentro del formulario
        nombre_grupo = st.text_input("Nombre del Grupo:")
        descripcion_grupo = st.text_area("Descripción del Grupo:")
        miembros_grupo = st.text_area("Líder del Grupo:")
        correo_grupo = st.text_input("Correo del Grupo:")
        # Botón para enviar el formulario (crear grupo)
        submit_button = st.form_submit_button("Crear Grupo")

        # Manejar la lógica cuando se envía el formulario
        if submit_button and nombre_grupo and descripcion_grupo and miembros_grupo and correo_grupo:
            crear_Grupos(nombre_grupo, descripcion_grupo, miembros_grupo, correo_grupo)
            st.success(f"¡Grupo '{nombre_grupo}' creado correctamente!") 

            codigoSecreto = obtener_grupo_id(nombre_grupo)
            print(obtener_grupo_id(nombre_grupo))
            email_sender.send_email(
                recipient_email=correo_grupo,
                subject="Creación de Grupo",
                body=f"Grupo {nombre_grupo} creado correctamente, su código secreto es {codigoSecreto}",
            )

            
    