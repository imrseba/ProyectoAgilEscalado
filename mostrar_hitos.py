import streamlit as st
from firebase_utils import obtener_hitos_grupo
import pandas as pd

def mostrar_hitos_app(id, sprint_id, selected_sprint):
    hitos = obtener_hitos_grupo(id, sprint_id)
    hitos_list = [hito['hito'] for hito in hitos.values()] if hitos else []
    descripcion_list = [hito['descripcion'] for hito in hitos.values()] if hitos else []

    # Mostrar ambas listas en una tabla que diga el hito y su descripción
    data = {'Hito': hitos_list, 'Descripción': descripcion_list}
    df = pd.DataFrame(data)

    # Mostrar la tabla en Streamlit
    st.subheader('Hitos ' + selected_sprint)
    st.table(df)

        
