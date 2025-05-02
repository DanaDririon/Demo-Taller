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
    st.markdown("<h1>"+"Inventario"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    df_inv = ct.select_data('inventario')

    col1, col2, col3 = st.columns((1,1,8))

    col1.button(label="Nuevo Producto", key="new_item",type="primary")
    col2.button(label="Agregar Inventario", key="add",type="primary")

    # with st.container(height=500):
    st.dataframe(df_inv, hide_index=True, use_container_width=True)


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()

