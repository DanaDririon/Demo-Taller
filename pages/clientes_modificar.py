import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os

import re


def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Modificar Cliente', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Modificar Cliente"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    #set_png_as_page_bg('src\\img\\taller.png')

    col1, col2, col3, col4 = st.columns((3,1,1,1))

    if col1.button(label="⬅Volver"):
        st.switch_page("pages\\clientes.py")