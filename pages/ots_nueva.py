import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os
import uuid

def del_keys():
    pass

def main():
    
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Nueva OT', page_icon="src\\img\\taller_img\\icon_taller.jpg")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Nueva OT"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()
    
    df_cat = ct.select_data(tabla="categorias_ots", columns='cat_id, cat_nombre', where="deleted = 0")

    if 'selected_id_cotiz' in st.session_state:
        df_cotiz_cab = ct.select_data(tabla="cotiz_cab",
                                            columns='cotiz_id, cotiz_cat_id, cotiz_ots_id, cotiz_rut_cliente, cotiz_rut_facturacion, cotiz_nombre_facturacion, cotiz_patente, cotiz_marca, cotiz_modelo, cotiz_year, date_created',
                                            where="deleted = 0 AND cotiz_id = {}".format(st.session_state['selected_id_cotiz']))
        df_cotiz_cab['cotiz_ots_id'] = df_cotiz_cab['cotiz_ots_id'].astype(int)
        df_cotiz_cab = df_cotiz_cab.fillna('')


        st.session_state['form_keyCliente'] = df_cotiz_cab['cotiz_rut_cliente'].array[0]
        st.session_state['form_keyRUT'] = df_cotiz_cab['cotiz_rut_facturacion'].array[0]
        st.session_state['form_valueNomb'] = df_cotiz_cab['cotiz_nombre_facturacion'].array[0]
        # st.session_state['form_valueDir']
        # st.session_state['form_valueTel']
        st.session_state['form_valuePatente'] = df_cotiz_cab['cotiz_patente'].array[0]
        st.session_state['form_valueMarca'] = df_cotiz_cab['cotiz_marca'].array[0]
        st.session_state['form_valueModelo'] = df_cotiz_cab['cotiz_modelo'].array[0]
        st.session_state['form_valueYear'] = df_cotiz_cab['cotiz_year'].array[0]
        
        val_cat_id = int(df_cotiz_cab['cotiz_cat_id'][0])
        st.session_state['form_keyTipo'] = df_cat['cat_nombre'][df_cat['cat_id']==val_cat_id].array[0]

    
    if 'selected_id_cotiz' not in st.session_state:
        st.session_state['selected_id_cotiz'] = 0
        st.session_state['form_keyTipo'] = None
        st.session_state['form_keyRUT'] = None
        st.session_state['form_valueNomb'] = None
        
        st.session_state['form_valuePatente'] = None
        st.session_state['form_valueMarca'] = None
        st.session_state['form_valueModelo'] = None
        st.session_state['form_valueYear'] = None

    col1, col2, col3, col99 = st.columns((2.8,1,2,0.3))

    if col1.button(label="Volver",icon=":material/arrow_back:"):
        ct.switch_page("ots.py")
        del st.session_state['selected_id_cotiz']
        del st.session_state['form_keyTipo']
        del st.session_state['form_keyCliente']

    with col1.container(height=570):
        df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
        # df_clientes_1 = df_clientes
        # df_clientes_1 = df_clientes_1.drop(columns=['cliente_rut'])        
        # df_clientes_1['rut_name'] = df_clientes_1['cliente_rut'] +' | '+df_clientes_1['cliente_nombre']

        categoria = st.selectbox("Tipo OT", df_cat['cat_nombre'], placeholder="Tipo de trabajo",index=None, key="form_keyTipo")
        if categoria:
            categoria_id = int(df_cat['cat_id'][df_cat['cat_nombre']==categoria]) #Error si no exite categoria

        rut_cliente = st.selectbox("Cliente", df_clientes['cliente_rut'], placeholder="RUT Cliente", index=None, key="form_keyCliente")

        fact_rut = st.text_input("RUT Facturación", placeholder="RUT factura")
        fact_nomb = st.text_input("Nombre Facturación", placeholder="Nombre factura", value=st.session_state['form_valueNomb'])
        fact_dir = st.text_input("Dirección Facturación", placeholder="Dirección factura").upper()
        check_dir_fact = fact_dir.isupper()

        fact_telf = st.text_input("Teléfono Facturación", placeholder="Teféfono factura")

        patente = st.text_input("Patente", placeholder="Patente", value=st.session_state['form_valuePatente']).upper()
        check_patente = patente.isupper()
        marca = st.text_input("Marca", placeholder="Marca", value=st.session_state['form_valueMarca'])
        modelo = st.text_input("Modelo", placeholder="Modelo", value=st.session_state['form_valueModelo'])
        año = st.text_input("Año", max_chars=4, placeholder="Año", value=st.session_state['form_valueYear'])
        check_año = ct.check_int(año)
        vin = st.text_input("VIN", placeholder="VIN Vehículo")
        descripcion = st.text_input("Descripción", placeholder="Descripción")

        telefono = st.text_input("Telefóno",max_chars=9,placeholder="Sólo los últimos 9 dígitos")
        check_telefono = ct.check_int(telefono)
        # direccion = st.text_input("Dirección", placeholder="Ingresar dirección").upper()
        # check_direccion = direccion.isupper()
    
    col3.markdown("<h4>"+"Preview"+"</h4>", unsafe_allow_html=True)
    with col3.container(height=570):
        tel_ini = ""
        if check_telefono: tel_ini = "+56"
        resumen = pd.DataFrame({
            "Preview": ["Tipo OT","RUT Nombre","Patente","Correo","Teléfono","Dirección"],
            " ": [categoria,rut_cliente,fact_nomb,fact_dir,tel_ini+telefono,fact_dir],
        })

        st.dataframe(resumen,hide_index=True)
        if check_telefono and check_dir_fact and categoria:
            agregar = st.button(label='Finalizar',type="primary")
            if agregar:
                if ct.insert_data('ots',
                                campos_insertar = ['cliente_rut','cliente_nombre','cliente_correo','cliente_telefono','cliente_direccion','created_by','mod_by'],
                                valores_insertar = [rut_cliente, fact_nomb, fact_dir, tel_ini+telefono, fact_dir, 'dana', 'dana']):
                    st.success("Registro creado exitosamente.")
                    sleep(1.2)
                    ct.switch_page("ots.py")
                else:
                    st.error("Ya existe un registro con el RUT ingresado.")
        else:
            agregar = st.button(label='Finalizar',type="primary", disabled=True)

    col1.write(st.session_state)

if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()