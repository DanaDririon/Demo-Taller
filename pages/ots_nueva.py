import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os
import uuid

def del_keys():
    # del st.session_state['selected_id_cotiz']
    del st.session_state['form_keyTipo']
    del st.session_state['form_keyCliente']
    del st.session_state['form_keyRUT']
    del st.session_state['form_valueNomb']
    del st.session_state['form_valuePatente']
    del st.session_state['form_valueMarca']
    del st.session_state['form_valueModelo']
    del st.session_state['form_valueYear']

def main():
    
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Nueva OT', page_icon="src\\img\\taller_img\\icon_taller.jpg")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Nueva OT"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()
    
    df_cat = ct.select_data(tabla="categorias_ots", columns='cat_id, cat_nombre', where="deleted = 0")
    
    # if 'selected_id_cotiz' not in st.session_state:
    #     st.session_state['selected_id_cotiz'] = 0
    #     st.session_state['form_keyTipo'] = None
    #     st.session_state['form_keyCliente'] = None
    #     st.session_state['form_keyRUT'] = None

    #     st.session_state['form_valueNomb'] = ""
    #     st.session_state['form_valuePatente'] = ""
    #     st.session_state['form_valueMarca'] = ""
    #     st.session_state['form_valueModelo'] = ""
    #     st.session_state['form_valueYear'] = ""

    if 'selected_id_cotiz' in st.session_state and st.session_state['selected_id_cotiz']:
        df_cotiz_cab = ct.select_data(tabla="cotiz_cab",
                                            columns='cotiz_id, cotiz_cat_id, cotiz_ots_id, cotiz_rut_cliente, cotiz_rut_facturacion, ' \
                                            'cotiz_nombre_facturacion, cotiz_patente, cotiz_marca, cotiz_modelo, cotiz_year, date_created',
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
        del st.session_state['selected_id_cotiz']

    col1, col2, col3, col99 = st.columns((2.8,1,2,0.3))

    # if st.session_state['selected_id_cotiz']:
    if col1.button(label="Volver",icon=":material/arrow_back:"):
        del_keys()
        ct.switch_page("cotiz.py")
    # else:
    #     if col1.button(label="Volver",icon=":material/arrow_back:"):
    #         del_keys()
    #         ct.switch_page("ots.py")

    with col1.container(height=735):
        df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
        # df_clientes_1 = df_clientes
        # df_clientes_1 = df_clientes_1.drop(columns=['cliente_rut'])        
        # df_clientes_1['rut_name'] = df_clientes_1['cliente_rut'] +' | '+df_clientes_1['cliente_nombre']

        categoria = st.selectbox("Tipo OT", df_cat['cat_nombre'], placeholder="Tipo de trabajo",index=None, key="form_keyTipo")
        if categoria:
            categoria_id = df_cat['cat_id'][df_cat['cat_nombre']==categoria].astype(int) #Error si no exite categoria

        rut_cliente = st.selectbox("Cliente", df_clientes['cliente_rut'], placeholder="RUT Cliente", index=None, key="form_keyCliente")

        fact_rut = st.text_input("RUT Facturación",max_chars=8, placeholder="RUT factura",value=st.session_state['form_keyRUT'])
        # check_int_fact_rut = ct.check_int(fact_rut)
        fact_nomb = st.text_input("Nombre Facturación", placeholder="Nombre factura", value=st.session_state['form_valueNomb']).upper()
        fact_dir = st.text_input("Dirección Facturación", placeholder="Dirección factura").upper()
        check_dir_fact = fact_dir.isupper()

        fact_telf = st.text_input("Teléfono Facturación",max_chars=9, placeholder="Sólo los últimos 9 dígitos")
        check_telefono = ct.check_int(fact_telf)

        patente = st.text_input("Patente", placeholder="Patente", value=st.session_state['form_valuePatente']).upper()
        check_patente = patente.isupper()
        marca = st.text_input("Marca", placeholder="Marca", value=st.session_state['form_valueMarca']).upper()
        modelo = st.text_input("Modelo", placeholder="Modelo", value=st.session_state['form_valueModelo']).upper()
        año = st.text_input("Año", max_chars=4, placeholder="Año", value=st.session_state['form_valueYear'])
        check_año = ct.check_int(año)
        vin = st.text_input("VIN", placeholder="VIN Vehículo")
        descripcion = st.text_input("Descripción", placeholder="Descripción").upper()

        # telefono = st.text_input("Telefóno",max_chars=9,placeholder="Sólo los últimos 9 dígitos")
        # check_telefono = ct.check_int(telefono)
        # direccion = st.text_input("Dirección", placeholder="Ingresar dirección").upper()
        # check_direccion = direccion.isupper()
    
    col3.markdown("<h4>"+"Preview"+"</h4>", unsafe_allow_html=True)
    with col3.container(height=735):
        tel_ini = ""
        if check_telefono: tel_ini = "+56"
        resumen = pd.DataFrame({
            "Preview": ["Tipo OT","RUT Cliente","RUT Factura","Nombre Factura","Teléfono Factura","Dirección Factura",
                        "Patente","Marca","Modelo","Año","VIN","Descripcion"],
                    " ": [categoria,rut_cliente,fact_rut,fact_nomb,tel_ini+fact_telf,fact_dir,
                        patente,marca,modelo,año,vin,descripcion],
        })

        st.dataframe(resumen,hide_index=True,height=458)
        if check_telefono and check_dir_fact and check_año and vin and categoria and patente and modelo and marca:
            agregar = st.button(label='Finalizar',type="primary")
            if agregar:
                if ct.insert_data('ots',
                                campos_insertar = ['ots_cat_id', 'ots_rut_cliente','ots_rut_facturacion','ots_nombre_facturacion',
                                                   'ots_telefono_facturacion','ots_dir_facturacion',
                                                   'ots_v_patente','ots_v_marca', 'ots_v_modelo', 'ots_v_año', 'ots_v_vin', 'ots_descripcion',
                                                   'created_by','mod_by'],
                                valores_insertar = [categoria_id, rut_cliente,fact_rut, fact_nomb,
                                                    tel_ini+fact_telf, fact_dir,
                                                    patente, marca, modelo, año, vin, descripcion,
                                                    'dana', 'dana']):
                    ct.update_data('cotiz_cab')
                    st.success("Registro creado exitosamente.")
                    sleep(1.2)
                    ct.switch_page("ots.py")
        else:
            agregar = st.button(label='Finalizar',type="primary", disabled=True)

    col1.write(st.session_state)

if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()