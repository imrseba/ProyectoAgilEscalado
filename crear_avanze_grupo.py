from EmailSender import EmailSender
from firebase_admin import db
import streamlit as st
from firebase_utils import crear_avanze_grupos

email_sender = EmailSender(smtp_server='smtp.gmail.com',
                           smtp_port=587,
                           sender_email='mauricie.seba@gmail.com',
                           sender_password='yctj sdjx qols rbdf')


def crear_avanze_grupo():
    ref_grupos = db.reference('Grupos')
    grupos = ref_grupos.get()
    grupo_names = [grupo['nombreGrupo'] for grupo in grupos.values()] if grupos else []

    st.subheader("seleccione grupo a reportar avance:")
    # Crear un widget de selección para elegir un grupo
    selected_grupo = st.selectbox("Selecciona un Grupo:", grupo_names)

    if(selected_grupo):
        # Obtener la referencia del grupo seleccionado
        grupo_id = list(grupos.keys())[grupo_names.index(selected_grupo)]

        with st.form("crear_avance_form"):
            # Campos de entrada dentro del formulario
            avance = st.text_area("Avance del Grupo:")
            fecha = st.date_input("Fecha del Avance:")
            # Botón para enviar el formulario (crear avance)
            submit_button = st.form_submit_button("crear Avance")

            # Manejar la lógica cuando se envía el formulario
            if submit_button and avance and fecha:
                crear_avanze_grupos(avance, fecha, grupo_id)
                # Obtener el correo del grupo (aquí sustituye por la lógica para obtener el correo del grupo)
                correo_grupo = grupos[grupo_id]['correo']

                # Enviar correo con el avance creado
                email_sender.send_email(recipient_email=correo_grupo,
                                subject="Avance de Grupo",
                                body=f"Se ha reportado un nuevo avance: {avance}\nFecha: {fecha}")
                st.success(f"¡Avance del Grupo '{selected_grupo}' creado correctamente!")