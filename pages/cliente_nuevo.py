import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os

import re


def check_int(x):
    if x == "" or x == None:
        return False
    else:
        try:
            int(x)
            return True
        except:
            st.warning("No es un número entero")
            return False

def validate_email_syntax(email):
    if email == "" or email == None:
        return False
    else:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if re.match(pattern, email) is not None:
            return True
        else:
            st.warning("Correo Electronico invalido")
            return False


def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Nuevo Clientes', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Nuevo Cliente"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    set_png_as_page_bg('src\\img\\taller.png')

    col1, col2, col3, col4 = st.columns((3,1,1,1))

    if col1.button(label="⬅Volver"):
        st.switch_page("pages\\clientes.py")

    with col1.container(height=570):
        rut_1, rut_3, rut_2 = st.columns((9, 0.1, 1.8))
        rut = None
        dig_ver = None
        x = rut_1.text_input("RUT", max_chars=10, placeholder="Ingresar RUT sin punto ni digito verificador")
        check_rut = check_int(x)
        if check_rut:
            rut_clean = int(x)
            dig_ver = ct.digito_verificador(x)
            rut_clean = str(rut_clean)+'-'+str(dig_ver)
        rut_2.text_input(label="Digito Verificador", disabled=True, value=dig_ver)
        nombre = st.text_input("Nombre cliente", placeholder="Ingresar nombre de cliente")
        correo = st.text_input("Correo Electronico", placeholder="Formato de correo es xxxx@xxxx.xx")
        check_correo = validate_email_syntax(correo)
        telefono = st.text_input("Telefóno",max_chars=9,placeholder="Ingresar solo los últimos 9 números")
        check_telefono = check_int(telefono)
        if check_telefono:
            telefono_clean = int(x)
        direccion = st.text_input("Dirección", placeholder="Ingresar Direccion")
        if check_correo and check_rut and check_telefono:
            agregar = st.button(label='Agregar',type="primary")
            if agregar:
                if ct.insert_data('clientes',
                                campos_insertar = ['cliente_rut','cliente_nombre','cliente_correo','cliente_telefono','cliente_direccion','created_by','mod_by'],
                                valores_insertar = [rut_clean, nombre, correo, telefono_clean, direccion, 'dana', 'dana'],
                                check_duplicado=True,
                                campo_contar='cliente_id',
                                campos_check_duplicado=['cliente_rut'],
                                valores_check_duplicado=[rut]):
                    st.success("Registro Creado Exitosamente")
                    sleep(1.5)
                    st.switch_page("pages\\clientes.py")
                else:
                    st.error("Ya existe un registro con el RUT ingresado.")
        else:
            agregar = st.button(label='Agregar',type="primary", disabled=True)


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()

