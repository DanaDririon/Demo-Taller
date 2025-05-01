import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import altair as alt
from babel.numbers import format_currency 
from time import sleep
from control_taller import utils as ct
import os

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Reportes - Taller', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Reportes"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    #cent_co
    col1, col2, col3, col4 = st.columns((1,1,1,1)) 

    df_ventas = pd.DataFrame({
        "Meses": ["Enero", "Febrero", "Marzo", "Abril","Mayo","Junio", "Julio"],
        #"Ventas":["$9.685.415", "$8.754.361", "16.487.591", "13.548.794","$0","$0","$0"]
        "Ventas":[9685415, 8754361, 16487591, 13548794,0,0,0]
    })
    col1.markdown("**Ventas Mensuales**")
    col1.dataframe(df_ventas,hide_index=True, use_container_width=True)

    df_proovedores = pd.DataFrame({
        "Proovedor": ["Imperial", "3M", "Mobil", "Otros"],
        #"Compras": ["$6.789.012", "$4.456.789", "$1.862.486", "$765.432"]
        "Compras": [6789012, 4456789, 1862486, 765432]
    })
    col3.markdown("**Compras por proovedor mensuales**")
    col3.dataframe(df_proovedores,hide_index=True,use_container_width=True)

    df_ots =  pd.DataFrame({
        "Mes": ["Enero","Enero","Febrero","Febrero","Marzo","Marzo","Abril","Abril","Mayo","Mayo","Junio","Junio"],
        "Tipos de OTs": ["Mantención","Específica","Mantención","Específica","Mantención","Específica","Mantención","Específica","Mantención","Específica","Mantención","Específica"],
        "# Órdenes de Trabajo": [23,12,19,7,38,22,33,15,25,15,21,9]
        })
    col1.markdown("**Órdenes de trabajo por tipo por mes**")
    col1.dataframe(df_ots,hide_index=True,use_container_width=True)


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    ct.control_login(page,allow=True)

    main()