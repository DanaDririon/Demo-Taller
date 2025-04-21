import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
#from control_servicena import utils as cs
import os


def sidebar():
    st.sidebar.title("Menú")
    if st.sidebar.button("Clientes"):
        st.switch_page("pages\\clientes.py")
    if st.sidebar.button("Cotizaciones"):
        st.switch_page("pages\\cotiz.py")
    if st.sidebar.button("Órdenes de Trabajo"):
        st.switch_page("pages\\ots.py")
    if st.sidebar.button("Negocio"):
        st.switch_page("pages\\negocio.py")

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Inicio - Taller', page_icon="src\\img\\logo-servicena.png")
    #cs.increase_page()
    if st.button("⬅︎Volver"):
        st.switch_page("pages\\home.py")
    st.markdown("<h1>"+"Cotizaciones"+"</h1>", unsafe_allow_html=True)
    sidebar()

    left_co, cent_co,last_co = st.columns([0.5,1,0.5])
    cent_co.image("src\\img\\intranet_img.jpg", width=550)


#if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

main()