import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os


def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Nuevo Clientes', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Nuevo Cliente"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    col1, col2, col3, col4, col5 = st.columns((0.5,1,0.5,1,0.5))

    with col2.container(height=525):
        rut = st.text_input("RUT")
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo")
        telefono = st.text_input("Telefóno")
        direccion = st.text_input("Dirección")
        if st.button(label='Agregar',type="primary"):
            st.switch_page("pages\\clientes.py")
            

    st.image("src\\img\\taller.png",use_container_width=True)


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()

