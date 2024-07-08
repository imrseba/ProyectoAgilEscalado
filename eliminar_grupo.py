import streamlit as st
from firebase_utils import obtener_grupos, eliminar_grupo

def eliminar_grupo_app():
    st.sidebar.title("Eliminar Grupo")
    
    # Obtener los grupos existentes
    grupos = obtener_grupos()
    grupo_names = [grupo['nombreGrupo'] for grupo in grupos.values()] if grupos else []

    if not grupo_names:
        st.sidebar.warning("No hay grupos disponibles para eliminar.")
        return

    # Mostrar la lista de grupos existentes
    st.sidebar.subheader("Grupos existentes:")
    selected_grupo = st.sidebar.selectbox("Seleccione el grupo que desea eliminar:", grupo_names)

    if selected_grupo:
        # Obtener el ID del grupo seleccionado
        grupo_id = next((key for key, value in grupos.items() if value['nombreGrupo'] == selected_grupo), None)

        if st.sidebar.button("Eliminar Grupo"):
            eliminar_grupo(grupo_id)
            st.sidebar.success("¡Grupo eliminado exitosamente!")
            st.experimental_rerun()
