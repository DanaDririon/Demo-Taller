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

    with st.container(height=525):
        df_clientes = pd.DataFrame ({
                    "RUT":["15.898.932-9","6.622.912-0","7.930.134-5","19.334.061-4","18.887.218-K"],
                    "Nombre":["María","José","Daniel","Eladio","Felipe"],
                    "Correo":["María@gmail.com" ,"José@gmail.com","Daniel@gmail.com","Eladio@gmail.com","Felipe@gmail.com"],
                    "Teléfono":["+56954735358","+56930920520","+56937668224","+56915858981","+56959068833"],
                    "Dirección":["Santiago 111", "La Florida 222", "Peñalolén 333", "Maipú 444", "Las Condes 555"]
                    })
    
        col1, col2, col3, col4 = st.columns((0.5,0.5,1,0.5))

        rut_filter = col1.selectbox("Buscar RUT", df_clientes['RUT'].unique() , index=None, placeholder='RUT')
        if rut_filter:
            df_clientes = filtros_detalles(df_clientes, rut=rut_filter)

        nombre_filter = col2.selectbox("Buscar Nombre", df_clientes['Nombre'].unique() , index=None, placeholder='Nombre')
        if nombre_filter:
            df_clientes = filtros_detalles(df_clientes, nombre=nombre_filter)

        st.dataframe(df_clientes, hide_index=True, height=400)

    st.image("src\\img\\taller.png",use_container_width=True)

if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()