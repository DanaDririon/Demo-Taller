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

    df_ejemplo = pd.DataFrame({
        "Id": ["AAAAA", "BBBBB", "CCCCC", "DDDDD", "EEEEE", "FFFFF", "GGGGG"],
        "Item": ["Pastillas","Amortiguadores","Uno","Fish","Cincuenta","Error","Botella"],
        "Cantidad": [74,82,1,5,50,11,2],
        "Precio Total": ["$1.555","222.444","$1","$666.666","$50","$321.123","$500"]
    })

    st.button(label="Nueva Cotizacion", key="new_cotiz")

    with st.container(height=500):
        st.dataframe(df_ejemplo, hide_index=True, height=200)
    st.image("src\\img\\taller.png",use_container_width=True)


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()