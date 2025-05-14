import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from streamlit_extras.switch_page_button import switch_page
from control_taller import utils as ct


def main():
    st.set_page_config(layout="centered", page_title='Login - Intranet Taller', page_icon="src\\img\\taller_img\\icon_taller.jpg")
    st.session_state['login'] = False
    st.markdown("<h1 style='text-align: center;'>"+"Inicio de Sesión"+"</h1>", unsafe_allow_html=True)
    metodo_login = ct.select_data(tabla='login_metodo', where='deleted = 0')['login_metodo_id'][0]
    metodo_login = int(metodo_login)
    with st.container():
        if metodo_login == 1 or metodo_login == 3:
            user_profile = ct.select_data(tabla='usuarios')
            user = st.selectbox("Selecciona tu Usuario",user_profile['usuario_nombre'].unique(), index=None, placeholder='')
            password = None
        else:
            user = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
        submit_button = st.button(label='Ingresar')

    if submit_button:
        if ct.login_check(user, password, metodo_login):
            st.session_state['login'] = True
            st.session_state['user'] = user
            #st.success("Login correcto")
            ct.switch_page("ots.py")
        else:
            st.error("Usuario o contraseña incorrectos")



if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)
    main()
