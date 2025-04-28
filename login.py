import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from streamlit_extras.switch_page_button import switch_page
from control_taller import utils as ct


def main():
    st.set_page_config(layout="centered", page_title='Login - Intranet Servicena', page_icon="src\\img\\logo-servicena.png")
    st.session_state['login'] = False
    st.markdown("<h1 style='text-align: center;'>"+"Inicio de Sesión"+"</h1>", unsafe_allow_html=True)
    with st.form('login_form'):
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit_button = st.form_submit_button(label='Ingresar')

    if submit_button:
        st.switch_page("pages\\ots.py")
    
    st.image("src\\img\\taller.png",use_container_width=True)


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)
    main()
