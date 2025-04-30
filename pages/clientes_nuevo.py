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
    st.set_page_config(layout="wide", page_title='Nuevo Cliente', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Nuevo Cliente"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    #set_png_as_page_bg('src\\img\\taller.png')

    col1, col2, col3, col99 = st.columns((3,1,2,0.3))

    if col1.button(label="⬅Volver"):
        st.switch_page("pages\\clientes.py")

    with col1.container(height=570):
        rut_1, rut_3, rut_2 = st.columns((9, 0.8, 1.8))
        rut = None
        dig_ver = None
        x = rut_1.text_input("RUT", max_chars=8, placeholder="Ingresar RUT sin puntos ni dígito verificador")
        check_rut = ct.check_int(x)
        rut_clean = ""
        if check_rut:
            rut_clean = int(x)
            dig_ver = ct.digito_verificador(x)
            rut_clean = str(rut_clean)+'-'+str(dig_ver)
        rut_2.text_input(label="Digito Verificador", disabled=True, value=dig_ver)
        nombre = st.text_input("Nombre cliente", placeholder="Ingresar nombre de cliente").upper()
        check_nombre = nombre.isupper()
        correo = st.text_input("Correo Electronico", placeholder="Formato de correo es 'xxxx@xxxx.xx'")
        check_correo = ct.validate_email_syntax(correo)
        telefono = st.text_input("Telefóno",max_chars=9,placeholder="Ingresar sólo los últimos 9 dígitos")
        check_telefono = ct.check_int(telefono)
        telefono_clean = 0
        if check_telefono:
            telefono_clean = int(x)
        direccion = st.text_input("Dirección", placeholder="Ingresar dirección").upper()
        check_direccion = direccion.isupper()
    
    col3.markdown("<h4>"+"Preview"+"</h4>", unsafe_allow_html=True)
    with col3.container(height=570):
        tel_ini = ""
        if telefono_clean: tel_ini = "+56"
        resumen = pd.DataFrame({
            "Preview": ["RUT","Nombre","Correo","Teléfono","Dirección"],
            " ": [rut_clean,nombre,correo,tel_ini+telefono,direccion],
        },index=None)

        st.dataframe(resumen,hide_index=True)
        if check_rut and check_nombre and check_correo and check_telefono and check_direccion:
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

