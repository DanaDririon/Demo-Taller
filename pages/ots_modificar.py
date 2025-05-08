import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os

def main():
    
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Modificar OT', page_icon="src\\img\\taller_img\\icon_taller.jpg")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Modificar OT"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()