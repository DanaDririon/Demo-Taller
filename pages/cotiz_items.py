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
    st.set_page_config(layout="wide", page_title='Agregar Item', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Agregar Item"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    col1, col2, col3, col99 = st.columns((1,1,2,0.3))

    # Tabla temporal de nuevos items
    if 'tabla_nuevos' not in st.session_state:
        st.session_state.tabla_nuevos =  pd.DataFrame({'Tipo Producto':[],
                                     'Descripcion Producto':[],
                                     'Cantidad':[],
                                     'Precio Venta':[],
                                     'Precio Costo':[]
                                     })
    # Llaves para resetear los valores del formulario
    if 'form_key1' not in st.session_state:
        st.session_state.form_key1 = str(uuid.uuid4())
    if 'form_key2' not in st.session_state:
        st.session_state.form_key2 = str(uuid.uuid4())
    if 'form_key3' not in st.session_state:
        st.session_state.form_key3 = str(uuid.uuid4())
    if 'form_key4' not in st.session_state:
        st.session_state.form_key4 = str(uuid.uuid4())
    if 'form_key5' not in st.session_state:
        st.session_state.form_key5 = str(uuid.uuid4())

    
    df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
    df_ids_cotiz = ct.select_data(tabla='cotiz_cab', columns='cotiz_id')
    df_tipos_prod = ct.select_data(tabla='tipo_prod', columns='tipo_prod_id, tipo_prod_descripcion', where='deleted = 0')


    
    df_cotizaciones_det = ct.select_data(tabla="cotiz_det",
                                        columns='cotiz_cab_id, cotiz_tipo_prod, cotiz_item, cotiz_cantidad, cotiz_costo, cotiz_precio_venta',
                                        where="deleted = 0 and cotiz_cab_id = {}".format(st.session_state.selected_id_cotiz))
    df_cotizaciones_det['cotiz_cab_id'] = df_cotizaciones_det['cotiz_cab_id'].astype(int)
    df_cotizaciones_det['cotiz_tipo_prod'] = df_cotizaciones_det['cotiz_tipo_prod'].astype(int)
    df_tipo_prod = ct.select_data(tabla="tipo_prod",
                                  columns='tipo_prod_id, tipo_prod_descripcion',
                                  where="deleted = 0")
    df_tipo_prod['tipo_prod_id'] = df_tipo_prod['tipo_prod_id'].astype(int)
    df_cotiz_det = pd.merge(df_cotizaciones_det, df_tipo_prod, how='left', left_on='cotiz_tipo_prod', right_on='tipo_prod_id')
    df_cotiz_det = df_cotiz_det.drop(columns=['cotiz_tipo_prod', 'tipo_prod_id', 'cotiz_cab_id'])
    df_cotiz_det = df_cotiz_det[['tipo_prod_descripcion', 'cotiz_item', 'cotiz_cantidad', 'cotiz_costo', 'cotiz_precio_venta']]

   

    if col1.button(label="⬅Volver"):
        st.switch_page("pages\\cotiz.py")
    
    with col1.container(height=600):
        tipo_item = st.selectbox("Tipo Producto",df_tipos_prod['tipo_prod_descripcion'],placeholder="Seleccionar tipo de producto",index=None,key=st.session_state.form_key1)
        desc_item = st.text_input("Descripción Producto", placeholder="Añadir descripción del producto",key=st.session_state.form_key2).upper()
        cant_item = st.number_input("Cantidad Producto",value=1,key=st.session_state.form_key3)
        venta_item = st.text_input("Precio Venta Producto",placeholder="0",key=st.session_state.form_key4)
        check_venta = ct.check_int(venta_item)
        costo_item = st.text_input("Precio Costo Producto",placeholder="0",key=st.session_state.form_key5)
        check_costo = ct.check_int(costo_item)

        if tipo_item and desc_item and cant_item and check_venta and check_costo:
            agregar = st.button(label="Agregar",type="primary")
            nueva_fila = pd.DataFrame({'Tipo Producto':[tipo_item],
                                     'Descripcion Producto':[desc_item],
                                     'Cantidad':[cant_item],
                                     'Precio Venta':[venta_item],
                                     'Precio Costo':[costo_item]})
            if agregar:
                st.session_state.tabla_nuevos = pd.concat([st.session_state.tabla_nuevos, nueva_fila], ignore_index=True)
                #st.session_state.form_key1 = str(uuid.uuid4()) # Aquí se resetea el tipo. Puede que sea más cómodo no resetearlo -> Preguntar - Dana
                st.session_state.form_key2 = str(uuid.uuid4())
                st.session_state.form_key3 = str(uuid.uuid4())
                st.session_state.form_key4 = str(uuid.uuid4())
                st.session_state.form_key5 = str(uuid.uuid4())
                st.rerun()
        else:
            agregar = st.button(label="Agregar",type="primary",disabled=True)



    col3.markdown("<h4>"+" "+"</h4>", unsafe_allow_html=True)

    with col3.container(height=300):
        st.dataframe(df_cotiz_det,hide_index=True)
    

    col3.markdown("<h4>"+" "+"</h4>", unsafe_allow_html=True)

    with col3.container(height=300):
        st.dataframe(st.session_state.tabla_nuevos,hide_index=True,use_container_width=True,on_select=nuevo_prod_select,selection_mode="single-row")
        
    if col1.button(label="Finalizar",type='primary'):
        st.session_state.tabla_nuevos.reset_index()


if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()