import streamlit as st
from firebase_utils import initialize_firebase
from crear_grupo import crear_grupo
from crear_avanze_grupo import crear_avanze_grupo
# Inicializar Firebase al inicio de la aplicación
initialize_firebase()

def main():
    st.title("Aplicacion Desarrollo Agil Escalado")

    st.sidebar.header("Crear Grupo")
    crear_grupo()

    st.header("Crear Nuevo Reporte de Avance de Grupo")
    crear_avanze_grupo()

if __name__ == "__main__":
    main()

