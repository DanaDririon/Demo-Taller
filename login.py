import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from streamlit_extras.switch_page_button import switch_page
from control_taller import utils as ct


def main():
    st.set_page_config(layout="centered", page_title='Login - Intranet Taller', page_icon="src\\img\\logo-servicena.png")
    st.session_state['login'] = False
    st.markdown("<h1 style='text-align: center;'>"+"Inicio de Sesión"+"</h1>", unsafe_allow_html=True)
    user_profile = ct.select_data(tabla='usuarios')
    metodo_login = ct.select_data(tabla='login')['login_metodo']
    with st.container():
        if metodo_login == (1 or 3):
            user = st.selectbox("Usuario",user_profile['usuario_nombre'].unique)
        else:
            user = st.text_input("Usuario")

        password = st.text_input("Contraseña", type="password")
        submit_button = st.button(label='Ingresar')

    if submit_button:
        st.switch_page("pages\\ots.py")
    
    st.image("src\\img\\taller.png",use_container_width=True)


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)
    main()
