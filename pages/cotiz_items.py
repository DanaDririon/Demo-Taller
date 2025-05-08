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
    st.set_page_config(layout="wide", page_title='Modificar Detalle', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Modificar Detalle Cotización"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    col1, col2, col3, col99 = st.columns((1,1,2.5,0.3))

    # Este valor viene de la cotizacion. Si es que se recarga la página, no tira error 
    if 'selected_id_cotiz' not in st.session_state:
        st.session_state.selected_id_cotiz = 0

    # Tabla temporal de nuevos items
    if 'tabla_nuevos' not in st.session_state:
        st.session_state.tabla_nuevos = pd.DataFrame({'Tipo Producto':[],
                                     'Descripción':[],
                                     'Proovedor':[],
                                     'Cantidad':[],
                                     'Costo':[],
                                     'Venta':[],
                                     'TipoProductoId':[]
                                     })
        st.session_state.tabla_nuevos['TipoProductoId'] = st.session_state.tabla_nuevos['TipoProductoId'].astype(int)
        st.session_state.tabla_nuevos['Cantidad'] = st.session_state.tabla_nuevos['Cantidad'].astype(int)
        st.session_state.tabla_nuevos['Costo'] = st.session_state.tabla_nuevos['Costo'].astype(int)
        st.session_state.tabla_nuevos['Venta'] = st.session_state.tabla_nuevos['Venta'].astype(int)
    
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
    if 'form_key6' not in st.session_state:
        st.session_state.form_key6 = str(uuid.uuid4())

    
    df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
    df_ids_cotiz = ct.select_data(tabla='cotiz_cab', columns='cotiz_id')
    df_tipos_prod = ct.select_data(tabla='tipo_prod', columns='tipo_prod_id, tipo_prod_descripcion', where='deleted = 0')


    
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

    if col1.button(label="⬅Volver"):
        del st.session_state.form_key1
        del st.session_state.form_key2
        del st.session_state.form_key3
        del st.session_state.form_key4
        del st.session_state.form_key5
        del st.session_state.form_key6
        del st.session_state.tabla_nuevos
        st.switch_page("pages\\cotiz.py")
    
    with col1.container(height=650):
        tipo_item = st.selectbox("Tipo Producto",df_tipos_prod['tipo_prod_descripcion'],placeholder="Seleccionar tipo de producto",index=None,key=st.session_state.form_key1)
        tipo_item_id = None
        if tipo_item:
            tipo_item_id = int(df_tipo_prod[df_tipo_prod['tipo_prod_descripcion']==tipo_item]['tipo_prod_id'].iloc[0]) #Error si no exite tipo_item
        desc_item = st.text_input("Descripción", placeholder="Añadir descripción del producto",key=st.session_state.form_key2).upper()
        prov_item = st.text_input("Proovedor", placeholder="Proovedor producto",key=st.session_state.form_key6).upper()
        cant_item = st.number_input("Cantidad Producto",value=1,key=st.session_state.form_key3)
        check_cant = ct.check_int(cant_item)
        costo_item = st.text_input("Costo Producto",placeholder="0",key=st.session_state.form_key5)
        check_costo = ct.check_int(costo_item)
        venta_item = st.text_input("Venta Producto",placeholder="0",key=st.session_state.form_key4)
        check_venta = ct.check_int(venta_item)

        if tipo_item and desc_item and check_cant and check_venta and check_costo:
            agregar = st.button(label="Agregar",type="primary")
            nueva_fila = pd.DataFrame({'Tipo Producto':[tipo_item],
                                     'Descripción':[desc_item],
                                     'Proovedor':[prov_item],
                                     'Cantidad':[cant_item],
                                     'Costo':[costo_item],
                                     'Venta':[venta_item],
                                     'TipoProductoId':[tipo_item_id]})
            nueva_fila['TipoProductoId'] = nueva_fila['TipoProductoId'].astype(int)
            nueva_fila['Cantidad'] = nueva_fila['Cantidad'].astype(int)
            nueva_fila['Costo'] = nueva_fila['Costo'].astype(int)
            nueva_fila['Venta'] = nueva_fila['Venta'].astype(int)
            if agregar:
                st.session_state.tabla_nuevos = pd.concat([st.session_state.tabla_nuevos, nueva_fila], ignore_index=True)
                #st.session_state.form_key1 = str(uuid.uuid4()) # Aquí se resetea el tipo. Puede que sea más cómodo no resetearlo -> Preguntar
                st.session_state.form_key2 = str(uuid.uuid4())
                st.session_state.form_key3 = str(uuid.uuid4())
                st.session_state.form_key4 = str(uuid.uuid4())
                st.session_state.form_key5 = str(uuid.uuid4())
                st.session_state.form_key6 = str(uuid.uuid4())
                st.rerun()
        else:
            agregar = st.button(label="Agregar",type="primary",disabled=True)



    col3.markdown("<h4>"+"Items cargados"+"</h4>", unsafe_allow_html=True)
    with col3.container(height=275):
        st.dataframe(df_cotiz_det,hide_index=True,use_container_width=True,height=250)
    

    col3.markdown("<h4>"+"Items a agregar"+"</h4>", unsafe_allow_html=True)
    with col3.container(height=275):
        st.dataframe(st.session_state.tabla_nuevos,hide_index=True,use_container_width=True,
                     on_select=nuevo_prod_select,selection_mode="single-row",height=175,
                     column_config={"TipoProductoId":None})
        if st.button(label="Finalizar",type='primary'):
            for i in range(len(st.session_state.tabla_nuevos)): 
                if ct.insert_data('cotiz_det',
                                    campos_insertar=['cotiz_cab_id',
                                                     'cotiz_item',
                                                     'cotiz_tipo_prod',
                                                     'cotiz_prov_prod',
                                                     'cotiz_costo',
                                                     'cotiz_precio_venta',
                                                     'cotiz_cantidad',
                                                     'created_by','mod_by'],
                                    valores_insertar=[st.session_state.selected_id_cotiz,
                                                      st.session_state.tabla_nuevos['Descripción'][i],
                                                      st.session_state.tabla_nuevos['TipoProductoId'][i],
                                                      st.session_state.tabla_nuevos['Proovedor'][i],
                                                      st.session_state.tabla_nuevos['Costo'][i],
                                                      st.session_state.tabla_nuevos['Venta'][i],
                                                      st.session_state.tabla_nuevos['Cantidad'][i],
                                                    'dana','dana']):
                    pass
                
            st.success("Campos agregados exitosamente.")
            sleep(1)

            st.session_state.tabla_nuevos = pd.DataFrame({'Tipo Producto':[],
                                    'Descripción':[],
                                    'Proovedor':[],
                                    'Cantidad':[],
                                    'Costo':[],
                                    'Venta':[],
                                    'TipoProductoId':[]
                                    })
            st.session_state.tabla_nuevos['TipoProductoId'] = st.session_state.tabla_nuevos['TipoProductoId'].astype(int)
            st.session_state.tabla_nuevos['Cantidad'] = st.session_state.tabla_nuevos['Cantidad'].astype(int)
            st.session_state.tabla_nuevos['Costo'] = st.session_state.tabla_nuevos['Costo'].astype(int)
            st.session_state.tabla_nuevos['Venta'] = st.session_state.tabla_nuevos['Venta'].astype(int)

            st.rerun()


if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()