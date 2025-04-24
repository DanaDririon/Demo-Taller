import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
#from control_servicena import utils as cs
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

def sidebar():
    st.sidebar.title("Menú")
    if st.sidebar.button("Órdenes de Trabajo"):
        st.switch_page("pages\\ots.py")
    if st.sidebar.button("Cotizaciones"):
        st.switch_page("pages\\cotiz.py")
    #if st.sidebar.button("Inicio"):
        #st.switch_page("pages\\home.py")
    if st.sidebar.button("Clientes"):
        st.switch_page("pages\\clientes.py")
    if st.sidebar.button("Cobranza"):
        st.switch_page("pages\\cobranza.py")
    if st.sidebar.button("Negocio"):
        st.switch_page("pages\\negocio.py")

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Clientes', page_icon="src\\img\\logo-servicena.png")
    #cs.increase_page()
    st.markdown("""
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            #MainMenu {visibility: hidden;}
            .stAppDeployButton {display:none;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
        """, unsafe_allow_html=True)
    st.markdown("""
        <style>
                .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
    st.markdown("<h1>"+"Clientes"+"</h1>", unsafe_allow_html=True)
    sidebar()

    with st.popover("Nuevo Cliente"):
        with st.form('cliente_form'):
            rut = st.text_input("RUT")
            nombre = st.text_input("Nombre")
            correo = st.text_input("Correo")
            telefono = st.text_input("Telefóno")
            direccion = st.text_input("Dirección")
            submit_button = st.form_submit_button(label='Agregar',type="primary")



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

    st.dataframe(df_clientes, hide_index=True)
    #left_co, cent_co,last_co = st.columns([0.5,1,0.5])
    cent_co = st.image("src\\img\\taller.png",use_container_width=True)
    #cent_co

#if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

main()