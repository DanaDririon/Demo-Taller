import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os

def main():
    
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Nueva OT', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Nueva OT"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    col1, col2, col3, col99 = st.columns((3,1,2,0.3))

    if col1.button(label="⬅Volver"):
        st.switch_page("pages\\ots.py")

    with col1.container(height=570):
        df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
        df_clientes_1 = df_clientes
        df_clientes_1 = df_clientes_1.drop(columns=['cliente_rut'])        
        df_clientes_1['rut_name'] = df_clientes_1['cliente_rut'] +' | '+df_clientes_1['cliente_nombre']

        cliente, rut_3, rut_2 = st.columns((9, 0.8, 1.8))

        rut_nombre = cliente.selectbox("Cliente", df_clientes_1['rut_name'], placeholder="Buscar Cliente")
        patente = st.text_input("Nombre cliente", placeholder="Ingresar Patente").upper()
        check_patente = patente.isupper()
        marca = st.text_input("Marca", placeholder="Marca")
        modelo = st.text_input("Modelo", placeholder="Modelo")
        año = st.text_input("Año", max_chars=4, placeholder="Año")
        check_año = ct.check_int(año)
        vin = st.text_input("VIN", placeholder="VIN Vehículo")
        descripcion = st.text_input("Descripción", placeholder="Descripción")

        telefono = st.text_input("Telefóno",max_chars=9,placeholder="Ingresar sólo los últimos 9 dígitos")
        check_telefono = ct.check_int(telefono)
        direccion = st.text_input("Dirección", placeholder="Ingresar dirección").upper()
        check_direccion = direccion.isupper()
    
    col3.markdown("<h4>"+"Preview"+"</h4>", unsafe_allow_html=True)
    with col3.container(height=570):
        tel_ini = ""
        if check_telefono: tel_ini = "+56"
        resumen = pd.DataFrame({
            "Preview": ["RUT Nombre","Patente","Correo","Teléfono","Dirección"],
            " ": [rut_clean,nombre,correo,tel_ini+telefono,direccion],
        })

        st.dataframe(resumen,hide_index=True)
        if check_rut and check_nombre and check_correo and check_telefono and check_direccion:
            agregar = st.button(label='Agregar',type="primary")
            if agregar:
                if ct.insert_data('clientes',
                                campos_insertar = ['cliente_rut','cliente_nombre','cliente_correo','cliente_telefono','cliente_direccion','created_by','mod_by'],
                                valores_insertar = [rut_clean, nombre, correo, tel_ini+telefono, direccion, 'dana', 'dana'],
                                check_duplicado=True,
                                campo_contar='cliente_id',
                                campos_check_duplicado=['cliente_rut'],
                                valores_check_duplicado=[rut]):
                    st.success("Registro creado exitosamente.")
                    sleep(1.2)
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