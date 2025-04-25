import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
#from control_servicena import utils as cs
import os

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
    st.set_page_config(layout="wide", page_title='Cobranza', page_icon="src\\img\\logo-servicena.png")
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
    st.markdown("<h1>"+"Cobranza"+"</h1>", unsafe_allow_html=True)
    sidebar()

    
    if st.button(label="Nueva Cobranza",key="nuevo_cobro"):
        st.markdown("pog")
    with st.container(height=400):
        df_cobranza = pd.DataFrame({
            "Id": ["AAAAA", "BBBBB", "CCCCC", "DDDDD", "EEEEE", "FFFFF", "GGGGG"],
            "Item": ["Pastillas","Amortiguadores","Uno","Fish","Cincuenta","Error","Botella"],
            "Cantidad": [74,82,1,5,50,11,2],
            "Precio Total": ["$1.555","222.444","$1","$666.666","$50","$321.123","$500"]
        })

    
        st.dataframe(df_cobranza, hide_index=True)  

    #left_co, cent_co,last_co = st.columns([0.5,1,0.5])
    cent_co = st.image("src\\img\\taller.png",use_container_width=True)


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()