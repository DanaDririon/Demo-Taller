import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os

import re

def extract_digits_rut(x) -> str:
    digits = re.findall(r'\d+', x)
    return digits[0]

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Modificar Cliente', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Modificar Cliente"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    if 'rut_selected' not in st.session_state:
        st.session_state.rut_selected = '0'

    col1, col2, col3, col4 = st.columns((3,1,1,1))

    if col1.button(label="⬅Volver"):
        st.session_state.rut_selected = None
        ct.switch_page("clientes.py")

    clean_rut = extract_digits_rut(st.session_state.rut_selected)

    df_clientes = ct.select_data("clientes", where="cliente_rut = '{}'".format(st.session_state.rut_selected))
    df_clientes = df_clientes[df_clientes['cliente_rut'] == st.session_state.rut_selected]


    with col1.container(height=570):
        rut_1, rut_3, rut_2 = st.columns((9, 0.8, 1.8))
        rut = None
        dig_ver = None
        x = rut_1.text_input("RUT", max_chars=8, value=clean_rut, disabled=True)
        check_rut = ct.check_int(x)
        if check_rut:
            rut_clean = int(x)
            dig_ver = ct.digito_verificador(x)
            rut_clean = str(rut_clean)+'-'+str(dig_ver)
        rut_2.text_input(label="Digito Verificador",disabled=True,value=dig_ver)
        nombre = st.text_input("Nombre cliente",value=df_clientes['cliente_nombre'][0].upper()).upper()     # Puede que el upper/lower 
        check_nombre = nombre.isupper()                                                                     # de afuera no sea necesario 
        correo = st.text_input("Correo Electronico",value=df_clientes['cliente_correo'][0].lower()).lower() # pero no quiero probar xd - Dana
        check_correo = ct.validate_email_syntax(correo)
        telefono = st.text_input("Telefóno",max_chars=9,value=df_clientes['cliente_telefono'][0])
        tel_ini = "+56"
        telefono = telefono.split(tel_ini,1)[1]
        check_telefono = ct.check_int(telefono)
        direccion = st.text_input("Dirección", value=df_clientes['cliente_direccion'][0].upper()).upper()
        check_direccion = direccion.isupper()
        if check_rut and check_nombre and check_correo and check_telefono and check_direccion:
            modificar = st.button(label='Modificar',type="primary")
            if modificar:
                if ct.update_data('clientes',
                                campos_modificar = ['cliente_nombre','cliente_correo','cliente_telefono','cliente_direccion','mod_by'],
                                valores_modificar = [nombre, correo, tel_ini+telefono, direccion, 'dana'],
                                campos_id=['cliente_rut'],
                                valores_id=[rut_clean]):
                    st.success("Registro modificado exitosamente.")
                    sleep(1.2)
                    ct.switch_page("clientes.py")
                else:
                    st.error("Ya existe un registro con el RUT ingresado.")
                ct.switch_page("clientes.py")
        else:
            modificar = st.button(label='Modificar',type="primary", disabled=True)



if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()
