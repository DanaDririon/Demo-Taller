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
 
def reset_form_keys():
    st.session_state['form_keyDesc'] = str(uuid.uuid4())
    st.session_state['form_keyCant'] = str(uuid.uuid4())
    st.session_state['form_keyVenta'] = str(uuid.uuid4())
    st.session_state['form_keyCosto'] = str(uuid.uuid4())
    st.session_state['form_keyProv'] = str(uuid.uuid4())
    st.session_state['value_keyDesc'] = ""
    st.session_state['value_keyCant'] = 1
    st.session_state['value_keyVenta'] = ""
    st.session_state['value_keyCosto'] = ""
    st.session_state['value_keyProv'] = ""
    st.rerun()

def del_value_keys():
    del st.session_state['value_keyDesc']
    del st.session_state['value_keyCant']
    del st.session_state['value_keyVenta']
    del st.session_state['value_keyCosto']
    del st.session_state['value_keyProv']

def main():

    # Este valor viene de la cotizacion. Si es que se recarga la página, no tira error 
    if 'selected_id_cotiz' not in st.session_state:
        st.session_state.selected_id_cotiz = 0
    
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Modificar Detalle', page_icon="src\\img\\taller_img\\icon_taller.jpg")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Modificar Detalle Cotización # "+ str(st.session_state.selected_id_cotiz) +"</h1>", unsafe_allow_html=True)
    ct.sidebar()
    
    # Llaves para resetear los valores del formulario
    if 'form_cotizId' not in st.session_state:
        st.session_state['form_cotizId'] = None
    if 'form_keyTipo' not in st.session_state:
        st.session_state['form_keyTipo'] = None
    if 'form_keyDesc' not in st.session_state:
        st.session_state['form_keyDesc'] = str(uuid.uuid4())
    if 'form_keyCant' not in st.session_state:
        st.session_state['form_keyCant'] = str(uuid.uuid4())
    if 'form_keyVenta' not in st.session_state:
        st.session_state['form_keyVenta'] = str(uuid.uuid4())
    if 'form_keyCosto' not in st.session_state:
        st.session_state['form_keyCosto'] = str(uuid.uuid4())
    if 'form_keyProv' not in st.session_state:
        st.session_state['form_keyProv'] = str(uuid.uuid4())

    if 'form_cotizId' not in st.session_state:
        st.session_state['form_cotizId'] = None
    if 'value_keyDesc' not in st.session_state:
        st.session_state['value_keyDesc'] = ""
    if 'value_keyCant' not in st.session_state:
        st.session_state['value_keyCant'] = 1
    if 'value_keyVenta' not in st.session_state:
        st.session_state['value_keyVenta'] = ""
    if 'value_keyCosto' not in st.session_state:
        st.session_state['value_keyCosto'] = ""
    if 'value_keyProv' not in st.session_state:
        st.session_state['value_keyProv'] = ""
    
    # df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
    df_cotiz_cab = ct.select_data(tabla='cotiz_cab', columns="cotiz_rut_cliente, cotiz_rut_facturacion, cotiz_nombre_facturacion, cotiz_marca, cotiz_modelo, cotiz_year, cotiz_patente", where="cotiz_id = '{}'".format(st.session_state.selected_id_cotiz))
    df_tipos_prod = ct.select_data(tabla='tipo_prod', columns='tipo_prod_id, tipo_prod_descripcion', where='deleted = 0')
    
    df_cotizaciones_det = ct.select_data(tabla='cotiz_det',
                                        columns='cotiz_det_id, cotiz_cab_id, cotiz_tipo_prod, cotiz_item, cotiz_prov_prod, cotiz_cantidad, cotiz_costo, cotiz_precio_venta',
                                        where='deleted = 0 and cotiz_cab_id = {}'.format(st.session_state.selected_id_cotiz))
    df_cotizaciones_det['cotiz_cab_id'] = df_cotizaciones_det['cotiz_cab_id'].astype(int)
    df_cotizaciones_det['cotiz_tipo_prod'] = df_cotizaciones_det['cotiz_tipo_prod'].astype(int)
    df_tipo_prod = ct.select_data(tabla='tipo_prod',
                                  columns='tipo_prod_id, tipo_prod_descripcion',
                                  where='deleted = 0')
    df_tipo_prod['tipo_prod_id'] = df_tipo_prod['tipo_prod_id'].astype(int)
    df_cotiz_det = pd.merge(df_cotizaciones_det, df_tipo_prod, how='left', left_on='cotiz_tipo_prod', right_on='tipo_prod_id')
    #df_cotiz_det = df_cotiz_det.drop(columns=['cotiz_tipo_prod', 'tipo_prod_id', 'cotiz_cab_id'])
    df_cotiz_det = df_cotiz_det[['cotiz_det_id', 'tipo_prod_descripcion', 'cotiz_item','cotiz_prov_prod', 'cotiz_cantidad', 'cotiz_costo', 'cotiz_precio_venta']]
    df_cotiz_det = df_cotiz_det.rename(columns={'tipo_prod_descripcion': 'Tipo Producto', 'cotiz_item': 'Descripción',
                                                'cotiz_prov_prod': 'Proovedor', 'cotiz_cantidad': 'Cantidad', 'cotiz_costo': 'Costo',
                                                'cotiz_precio_venta': 'Venta'})
    
    # st.write(st.session_state)

    if st.button(label="Volver",icon=":material/arrow_back:"):
        del st.session_state.form_keyTipo
        del st.session_state['form_keyDesc']
        del st.session_state['form_keyCant']
        del st.session_state['form_keyVenta']
        del st.session_state['form_keyCosto']
        del st.session_state['form_keyProv']
        del st.session_state['form_cotizId']
        del_value_keys()
        ct.switch_page("cotiz.py")
    
    ######### Datos Cliente #########
    with st.container(height=115):
        # resumen = pd.DataFrame({
        #     "Información": ["RUT Cliente","RUT Facturación","Nombre Facturación","Marca","Modelo","Año","Patente"],
        #     "Cliente": [df_cotiz_cab['cotiz_rut_cliente'][0],df_cotiz_cab['cotiz_rut_facturacion'][0],df_cotiz_cab['cotiz_nombre_facturacion'][0],
        #           df_cotiz_cab['cotiz_marca'][0],df_cotiz_cab['cotiz_modelo'][0],df_cotiz_cab['cotiz_year'][0],df_cotiz_cab['cotiz_patente'][0]],
        # })

        st.dataframe(df_cotiz_cab,hide_index=True,use_container_width=True,
                     column_config={"cotiz_rut_cliente":"RUT Cliente",
                                    "cotiz_rut_facturacion":"RUT Facturacion",
                                    "cotiz_nombre_facturacion":"Nombre Facturacion",
                                    "cotiz_marca":"Marca",
                                    "cotiz_modelo":"Modelo",
                                    "cotiz_year":"Año",
                                    "cotiz_patente":"Patente"})

    
    col1, col2, col3 = st.columns((1,0.5,3.5))

    ########## Items cargados / Detalle #########
    col3.markdown("<h4>"+"Items cargados"+"</h4>", unsafe_allow_html=True)
    with col3.container(height=650):
        data_detalle = st.dataframe(df_cotiz_det,hide_index=True,use_container_width=True,height=500,on_select='rerun',selection_mode='single-row',
                       column_config={"cotiz_det_id":None})
        col3_1, col3_2, col3_3 = st.columns((1,1,2))

        if len(data_detalle.selection['rows']):
            selected_row_detalle = data_detalle.selection['rows'][0]
            if col3_1.button("Editar",type="primary",icon=":material/edit:"):
                st.session_state['form_cotizId'] = df_cotiz_det.iloc[selected_row_detalle]['cotiz_det_id']
                st.session_state.form_keyTipo = df_cotiz_det.iloc[selected_row_detalle]['Tipo Producto']
                st.session_state['value_keyDesc'] = df_cotiz_det.iloc[selected_row_detalle]['Descripción']
                st.session_state['value_keyProv'] = df_cotiz_det.iloc[selected_row_detalle]['Proovedor']
                st.session_state['value_keyCant'] = df_cotiz_det.iloc[selected_row_detalle]['Cantidad'].astype(int)
                st.session_state['value_keyCosto'] = df_cotiz_det.iloc[selected_row_detalle]['Costo'].astype(int)
                st.session_state['value_keyVenta'] = df_cotiz_det.iloc[selected_row_detalle]['Venta'].astype(int)
                st.rerun()
                # reset_form_keys()

            with col3_2.popover("Eliminar",icon=":material/delete:"):
                st.markdown("¿Eliminar fila?")
                #colyes, colno = st.columns((1,1))
                if st.button("Sí",type="primary",icon=":material/check:"):
                    if ct.update_data('cotiz_det',campos_modificar=['deleted'],valores_modificar=[1],
                                      campos_id=['cotiz_det_id'],valores_id=[df_cotiz_det.iloc[selected_row_detalle]['cotiz_det_id']]):
                        st.rerun()
                if st.button("No",type="primary",icon=":material/close:"):
                    st.rerun()

        else:
            col3_1.button("Editar",disabled=True,icon=":material/edit:")
            col3_2.popover("Eliminar",disabled=True,icon=":material/delete:")
            if st.session_state['form_cotizId']:
                st.session_state['form_cotizId'] = None
                st.session_state.form_keyTipo = None
                reset_form_keys()

            
    ########## Agregar / Editar #########
    col1.markdown("<h4>"+"Editar Item"+"</h4>", unsafe_allow_html=True)
    with col1.container(height=650):
        tipo_item = st.selectbox("Tipo Producto",df_tipos_prod['tipo_prod_descripcion'], placeholder="Seleccionar tipo de producto", index=None, key="form_keyTipo")
        tipo_item_id = None
        if tipo_item:
            tipo_item_id = int(df_tipo_prod[df_tipo_prod['tipo_prod_descripcion']==tipo_item]['tipo_prod_id'].iloc[0]) #Error si no exite tipo_item
        desc_item = st.text_input("Descripción", placeholder="Añadir descripción del producto",key=st.session_state['form_keyDesc'],value=st.session_state['value_keyDesc']).upper()
        prov_item = st.text_input("Proovedor", placeholder="Proovedor producto",key=st.session_state['form_keyProv'], value=st.session_state['value_keyProv']).upper()
        cant_item = st.number_input("Cantidad Producto",key=st.session_state['form_keyCant'], value=st.session_state['value_keyCant'])
        check_cant = ct.check_int(cant_item)
        costo_item = st.text_input("Costo Producto",placeholder="0",key=st.session_state['form_keyCosto'], value=st.session_state['value_keyCosto'])
        check_costo = ct.check_int(costo_item)
        venta_item = st.text_input("Venta Producto",placeholder="0",key=st.session_state['form_keyVenta'], value=st.session_state['value_keyVenta'])
        check_venta = ct.check_int(venta_item)

        if tipo_item and desc_item and check_cant and check_venta and check_costo and not st.session_state['form_cotizId']:
            if st.button(label="Agregar",type="primary",icon=":material/add:"):                
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
                                                    desc_item,
                                                    tipo_item_id,
                                                    prov_item,
                                                    costo_item,
                                                    venta_item,
                                                    cant_item,
                                                    'dana','dana']):
                    st.success("Campos agregados exitosamente.")
                
                    #st.session_state.form_keyTipo = str(uuid.uuid4()) # Aquí se resetea el tipo. Puede que sea más cómodo no resetearlo -> Preguntar
                    del_value_keys()
                    reset_form_keys()
        elif st.session_state['form_cotizId']:
            if st.button(label="Modificar",type="primary",icon=":material/edit:"):
                if ct.update_data('cotiz_det',
                                    campos_modificar=['cotiz_item',
                                                    'cotiz_tipo_prod',
                                                    'cotiz_prov_prod',
                                                    'cotiz_precio_venta',
                                                    'cotiz_costo',
                                                    'cotiz_cantidad',
                                                    'mod_by'],
                                    valores_modificar=[desc_item,
                                                    tipo_item_id,
                                                    prov_item,
                                                    venta_item,
                                                    costo_item,
                                                    cant_item,
                                                    'dana'],
                                  campos_id=['cotiz_det_id'],
                                  valores_id=[st.session_state['form_cotizId']]):
                    st.success("Campos modificados exitosamente.")
                    sleep(1)
                    del st.session_state.form_keyTipo
                    del st.session_state['form_cotizId']
                    del_value_keys()
                    reset_form_keys()
            
        else:
            st.button(label="Agregar",type="primary",disabled=True,icon=":material/add:")

if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()