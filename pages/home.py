import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os


def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Inicio - Taller', page_icon="src\\img\\logo-servicena.png")
    #cs.increase_page()
    st.markdown("<h1>"+"Taller - Inicio"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    left_co, cent_co,last_co = st.columns([0.5,1,0.5])
    cent_co.image("src\\img\\intranet_img.jpg", width=550)


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()