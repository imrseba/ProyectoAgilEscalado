import streamlit as st
from firebase_utils import initialize_firebase
from crear_grupo import crear_grupo
from crear_avanze_grupo import crear_avance_grupo
from eliminar_grupo import eliminar_grupo_app

# Inicializar Firebase al inicio de la aplicación
initialize_firebase()

def main():
    st.title("Aplicación Desarrollo Ágil Escalado")

    st.sidebar.header("Opciones")
    opcion = st.sidebar.selectbox("Seleccione una opción", ["Crear Grupo", "Eliminar Grupo"])

    if opcion == "Crear Grupo":
        st.sidebar.header("Crear Grupo")
        crear_grupo()
    elif opcion == "Eliminar Grupo":
        st.sidebar.header("Eliminar Grupo")
        eliminar_grupo_app()

    st.header("Crear Nuevo Reporte de Avance de Grupo")
    crear_avance_grupo()

if __name__ == "__main__":
    main()

