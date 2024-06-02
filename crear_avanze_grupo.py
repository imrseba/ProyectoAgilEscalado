from EmailSender import EmailSender
import streamlit as st
from firebase_utils import obtener_grupos, actualizar_hito_grupo, obtener_hitos_grupo, obtener_hitos_sprint, actualizar_sprint
from generarPDF import generar_pdf
from mostrar_hitos import mostrar_hitos_app

email_sender = EmailSender(smtp_server='smtp.gmail.com',
                           smtp_port=587,
                           sender_email='mauricie.seba@gmail.com',
                           sender_password='yctj sdjx qols rbdf')

def crear_avanze_grupo():
    grupos = obtener_grupos()
    grupo_names = [grupo['nombreGrupo'] for grupo in grupos.values()] if grupos else []

    st.subheader("Seleccione grupo a reportar avance:")
    selected_grupo = st.selectbox("Selecciona un Grupo:", grupo_names, key="grupo_selectbox")

    if selected_grupo:
        grupo_id = next((key for key, value in grupos.items() if value['nombreGrupo'] == selected_grupo), None)
        sprints = obtener_hitos_sprint(grupo_id)
        sprint_list = [sprint['sprint'] for sprint in sprints.values()] if sprints else []

        st.subheader("Seleccione el sprint a reportar avance:")
        selected_sprint = st.selectbox("Selecciona un Sprint:", sprint_list, key="sprint_selectbox")

        if selected_sprint:
            grupo_id_sprint = next((key for key, value in sprints.items() if value['sprint'] == selected_sprint), None)
            hitos = obtener_hitos_grupo(grupo_id, grupo_id_sprint)
            hitos_list = [(hito_id, hito['hito'], hito['cumplido']) for hito_id, hito in hitos.items()] if hitos else []

            with st.form("crear_avance_form"):
                avance = st.text_area("Avance del Grupo:")
                fecha = st.date_input("Fecha del Avance:")
                
                st.subheader("Seleccione el estado de los hitos:")
                hitos_cumplidos = []
                
                for hito_id, hito, cumplido in hitos_list:
                    estado = st.checkbox(f"{hito}", value=cumplido, key=hito_id)
                    hitos_cumplidos.append((hito_id, hito, estado))
                submit_button = st.form_submit_button("Crear Avance")
                
                
                if submit_button and avance and fecha:
                    noCumplio = True
                    for hito_id, _, estado in hitos_cumplidos:
                        if(estado == False):
                            noCumplio = False
                        actualizar_hito_grupo(hito_id, grupo_id, estado, grupo_id_sprint)
                    if(noCumplio == True):
                        actualizar_sprint(grupo_id, grupo_id_sprint)

                        
                    correo_grupo = grupos[grupo_id]['correo']
                    pdf_buffer = generar_pdf(selected_grupo, fecha, hitos_cumplidos, avance,selected_sprint,grupo_id)

                    email_sender.send_email(
                        recipient_email=correo_grupo,
                        subject="Avance de Grupo",
                        body=f"Entrega avance grupo {selected_grupo}",
                        attachment=pdf_buffer,
                        attachment_name=f"Avance_{selected_grupo}.pdf"
                    )
                    st.success(f"¡Avance del Grupo '{selected_grupo}' creado correctamente!")
        
        mostrar_hitos_app(grupo_id, grupo_id_sprint,selected_sprint)


