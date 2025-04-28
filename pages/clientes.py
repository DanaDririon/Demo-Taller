import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os


def filtros_detalles(df, rut=None, cod_nubox=None, nombre=None, fecha=None) -> pd.DataFrame:
    if rut != None:
        df = df[df['RUT']==rut]
    #if cod_nubox != None:
    #    df = df[df['Cod Nubox']==cod_nubox]
    if nombre != None:
        df = df[df['Nombre']==nombre]
    if fecha != None:
        if len(fecha) == 2:
            df = df[(pd.to_datetime(df['Fecha'])>=pd.to_datetime(fecha[0])) & (pd.to_datetime(df['Fecha'])<=pd.to_datetime(fecha[1]))]
        elif len(fecha) == 1:
            df = df[(pd.to_datetime(df['Fecha'])==pd.to_datetime(fecha[0]))]
        else:
            df = df
    return df

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Clientes', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Clientes"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    if st.button("Nuevo Cliente ➕"):
        st.switch_page("pages\\cliente_nuevo.py")

    with st.container(height=530):
        df_clientes = ct.select_data("clientes")
    
        col1, col2, col3, col4 = st.columns((0.5,0.5,1,0.5))

        rut_filter = col1.selectbox("Buscar RUT", df_clientes['cliente_rut'].unique() , index=None, placeholder='RUT')
        if rut_filter:
            df_clientes = filtros_detalles(df_clientes, rut=rut_filter)

        nombre_filter = col2.selectbox("Buscar Nombre", df_clientes['cliente_nombre'].unique() , index=None, placeholder='Nombre')
        if nombre_filter:
            df_clientes = filtros_detalles(df_clientes, nombre=nombre_filter)

        st.dataframe(df_clientes, hide_index=True, height=405, 
                    column_order=((
                        "cliente_rut",
                        "cliente_nombre",
                        "cliente_correo",
                        "cliente_telefono",
                        "cliente_direccion")),
                    column_config={
                        'cliente_rut': st.column_config.Column("RUT"),#,width
                        'cliente_nombre':st.column_config.Column("Nombre"),
                        'cliente_correo':st.column_config.Column("Correo"),
                        'cliente_telefono':st.column_config.Column("Teléfono"),
                        'cliente_direccion':st.column_config.Column("Dirección")})

    st.image("src\\img\\taller.png",use_container_width=True)

if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()