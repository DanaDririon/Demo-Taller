import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os


def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Clientes', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Repuestos"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    c,d = st.columns((1,1))

    df_repuestos_ot = pd.DataFrame({
        "Item":[""],
        "Descripción":[""]
    })

    with c.container(height=700):
        st.dataframe(df_repuestos_ot, hide_index=True, height=200)
        st.button(label="Agregar repuesto", key="new_rep")

    with d.container(height=700):
        with st.form('repuestos_form'):
            rut = st.text_input("ID Repuesto")
            nombre = st.text_input("Proovedor")
            correo = st.text_input("Descripción")
            telefono = st.text_input("Cantidad")
            direccion = st.text_input("Precio Compra")
            venta = st.text_input("Precio Venta")
            margen = st.text_input("Margen")
            submit_button = st.form_submit_button(label='Finalizar',type="primary")
            if submit_button:
                st.switch_page("pages//ots.py")


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()

