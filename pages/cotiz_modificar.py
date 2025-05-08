import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os
import uuid

def nuevo_prod_select():
    pass
 

def main():
    
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Modificar Cotización', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Modificar Cotización"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    # Este valor viene de la cotizacion. Si es que se recarga la página, no tira error 
    if 'selected_id_cotiz' not in st.session_state:
        st.session_state.selected_id_cotiz = 0
    
    col1, col2, col3, col99 = st.columns((2.5,1,2.5,0.3))

    if col1.button(label="Volver",icon=":material/arrow_back:"):
        ct.switch_page("cotiz.py")
    
    df_cotiz_cab = ct.select_data(tabla='cotiz_cab', columns="cotiz_rut_cliente, cotiz_rut_facturacion, cotiz_nombre_facturacion, cotiz_marca, cotiz_modelo, cotiz_year, cotiz_patente", where="cotiz_id = '{}'".format(st.session_state.selected_id_cotiz))
    df_cotizaciones_det = ct.select_data(tabla="cotiz_det",
                                        columns='cotiz_cab_id, cotiz_tipo_prod, cotiz_item, cotiz_prov_prod, cotiz_cantidad, cotiz_costo, cotiz_precio_venta',
                                        where="deleted = 0 and cotiz_cab_id = {}".format(st.session_state.selected_id_cotiz))
    df_cotizaciones_det['cotiz_cab_id'] = df_cotizaciones_det['cotiz_cab_id'].astype(int)
    df_cotizaciones_det['cotiz_tipo_prod'] = df_cotizaciones_det['cotiz_tipo_prod'].astype(int)
    df_tipo_prod = ct.select_data(tabla="tipo_prod",
                                  columns='tipo_prod_id, tipo_prod_descripcion',
                                  where="deleted = 0")
    df_tipo_prod['tipo_prod_id'] = df_tipo_prod['tipo_prod_id'].astype(int)
    df_cotiz_det = pd.merge(df_cotizaciones_det, df_tipo_prod, how='left', left_on='cotiz_tipo_prod', right_on='tipo_prod_id')
    #df_cotiz_det = df_cotiz_det.drop(columns=['cotiz_tipo_prod', 'tipo_prod_id', 'cotiz_cab_id'])
    df_cotiz_det = df_cotiz_det[['tipo_prod_descripcion', 'cotiz_item','cotiz_prov_prod', 'cotiz_cantidad', 'cotiz_costo', 'cotiz_precio_venta']]
    df_cotiz_det = df_cotiz_det.rename(columns={'tipo_prod_descripcion': 'Tipo Producto', 'cotiz_item': 'Descripción',
                                                'cotiz_prov_prod': 'Proovedor', 'cotiz_cantidad': 'Cantidad', 'cotiz_costo': 'Costo',
                                                'cotiz_precio_venta': 'Venta'})


    with col1.container(height=750):
        rut_cliente = st.text_input("RUT Cliente", value=df_cotiz_cab['cotiz_rut_cliente'][0], disabled=True)

        clean_rut = ct.extract_digits_rut(df_cotiz_cab['cotiz_rut_facturacion'][0])
        rut_1, rut_3, rut_2 = st.columns((6, 1, 1.8))
        rut = None
        dig_ver = None
        x = rut_1.text_input("RUT Facturación", max_chars=8, value=clean_rut, disabled=True)
        check_rut = ct.check_int(x)
        if check_rut:
            rut_clean = int(x)
            dig_ver = ct.digito_verificador(x)
            rut_clean = str(rut_clean)+'-'+str(dig_ver)
        rut_2.text_input(label="Digito Verificador",disabled=True,value=dig_ver)
        
        fact_nomb = st.text_input("Nombre Facturación", value=df_cotiz_cab['cotiz_nombre_facturacion'][0].upper()).upper()

        marca = st.text_input("Marca",value=df_cotiz_cab['cotiz_marca'][0].upper()).upper()
        modelo = st.text_input("Modelo",value=df_cotiz_cab['cotiz_modelo'][0].upper()).upper()
        año = st.text_input("Año",value=df_cotiz_cab['cotiz_year'][0],max_chars=4)
        check_año = ct.check_int(año)
        patente = st.text_input("Patente",value=df_cotiz_cab['cotiz_patente'][0].upper()).upper()

        if rut_cliente and check_rut and check_año and fact_nomb and marca and modelo and patente:
            modificar = st.button(label='Guardar',type="primary")
            if modificar:
                if ct.update_data('cotiz_cab',
                                campos_modificar=['cotiz_rut_cliente',' cotiz_rut_facturacion',' cotiz_nombre_facturacion',
                                                    ' cotiz_marca',' cotiz_modelo',' cotiz_year',' cotiz_patente','mod_by'],
                                valores_modificar=[rut_cliente, rut_clean, fact_nomb,
                                                    marca,modelo,año,patente,'dana'],
                                campos_id=['cotiz_id'],
                                valores_id=[st.session_state.selected_id_cotiz]):
                    st.success("Registro modificado exitosamente.")
                else:
                    st.error("Error de Query. Contactar desarrollador.")

        else:
            modificar = st.button(label='Guardar',type="primary", disabled=True)

    col3.markdown("<h4>"+"Preview"+"</h4>", unsafe_allow_html=True)
    with col3.container(height=400):
        #st.dataframe(df_cotiz_det,hide_index=True,use_container_width=True,height=250)
        resumen = pd.DataFrame({
            "Preview": ["RUT Cliente","RUT Facturación","Nombre Facturación","Marca","Modelo","Año","Patente"],
            " ": [rut_cliente,rut_clean,fact_nomb,marca,modelo,año,patente],
        })

        st.dataframe(resumen,hide_index=True)
        

if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()