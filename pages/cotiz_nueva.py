import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os

def main():
    
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Nueva Cotización', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Nueva Cotización"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    col1, col2, col3, col99 = st.columns((3,1,2,0.3))

    
    df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
    df_ids_cotiz = ct.select_data(tabla='cotiz_cab', columns='cotiz_id')

    if col1.button(label="⬅Volver"):
        ct.switch_page("cotiz.py")

    with col1.container(height=570):
        rut_cliente = st.selectbox("RUT Cliente", df_clientes['cliente_rut'], placeholder="Seleccionar RUT Cliente", index=None)
        
        rut_1, rut_3, rut_2 = st.columns((9, 0.8, 1.8))
        rut = None
        dig_ver = None
        x = rut_1.text_input("RUT Facturación", max_chars=8, placeholder="Ingresar RUT sin puntos ni dígito verificador")
        check_rut = ct.check_int(x)
        rut_clean = ""
        if check_rut:
            rut_clean = int(x)
            dig_ver = ct.digito_verificador(x)
            rut_clean = str(rut_clean)+'-'+str(dig_ver)
        rut_2.text_input(label="Digito Verificador", disabled=True, value=dig_ver)

        fact_nomb = st.text_input("Nombre Facturación", placeholder="Ingresar Nombre facturación")

    col3.markdown("<h4>"+"Preview"+"</h4>", unsafe_allow_html=True)
    with col3.container(height=570):
        # tel_ini = ""
        # if check_telefono: tel_ini = "+56"
        resumen = pd.DataFrame({
            "Preview": ["RUT Cliente","RUT Facturación","Nombre Facturación"],
            " ": [rut_cliente,rut_clean,fact_nomb],
        })

        st.dataframe(resumen,hide_index=True)
        if check_rut:
            agregar = st.button(label='Agregar',type="primary")
            if agregar:
                #max_id = 1+int(ct.get_data('select MAX(cotiz_id) AS max_id FROM cotiz_cab')['max_id'])
                
                if ct.insert_data('cotiz_cab',
                                campos_insertar = ['cotiz_rut_cliente','cotiz_rut_facturacion','cotiz_nombre_facturacion','created_by','mod_by'],
                                valores_insertar = [rut_cliente, rut_clean, fact_nomb, 'dana', 'dana']):
                    st.success("Registro creado exitosamente.")
                    sleep(1.2)
                    ct.switch_page("cotiz.py")
                else:
                    st.error("Ya existe un registro con el RUT ingresado.")
        else:
            agregar = st.button(label='Agregar',type="primary", disabled=True)


if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()