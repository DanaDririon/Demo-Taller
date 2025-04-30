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

    st.image("src\\img\\taller.png",use_container_width=True)
    #cent_co


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    ct.control_login(page,allow=True)

    main()