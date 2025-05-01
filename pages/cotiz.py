import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os


def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Cotizaciones', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Cotizaciones"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    col1, col2, col3 = st.columns((1,1,7))
    col1.button(label="Nueva Cotizacion ➕", type="primary")
    col2.button(label="Modificar Cotizacion", type="primary",disabled=True)
    col3.button(label="Finalizar Cotizacion", type="primary",disabled=True)

    col11, col22 = st.columns((1,1))

    df_cotiz = ct.select_data('cotiz_cab')

    df_detalles = ct.select_data('cotiz_det')

    with col11.container(height=400):
        st.markdown("Cotizaciones")
        st.dataframe(df_cotiz,
                    hide_index=True, 
                    height=200,
                    use_container_width=True,
                    on_select='rerun',
                    selection_mode='single-row')

    with col22.container(height=400):
        st.markdown("Resumen")
    
    with col11.container(height=350):
        st.markdown("Detalles")
    
    with col22.container(height=350):
        st.markdown("Datos Cliente")

if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()