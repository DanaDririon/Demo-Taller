import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os

def repuestos():
    pass

def servicios_extras():
    pass

def imagenes():
    pass

def cotizaciones():
    pass

def cobranza():
    pass

def registro_estados() -> pd.DataFrame:
    df_1 = pd.DataFrame({
        "Id": ["AAAAA", "BBBBB", "CCCCC", "DDDDD", "EEEEE", "FFFFF", "GGGGG"],
        "Item": ["Pastillas","Amortiguadores","Uno","Fish","Cincuenta","Error","Botella"],
        "Cantidad": [74,82,1,5,50,11,2],
        "Precio Total": ["$1.555","222.444","$1","$666.666","$50","$321.123","$500"]
    })
    df_2 = pd.DataFrame({
        "Id": ["AAAAA", "BBBBB", "CCCCC", "DDDDD", "EEEEE", "FFFFF", "GGGGG"],
        "Item": ["Pastillas","Amortiguadores","Uno","Fish","Cincuenta","Error","Botella"],
        "Cantidad": [74,82,1,5,50,11,2],
        "Precio Total": ["$1.555","222.444","$1","$666.666","$50","$321.123","$500"]
    })

    return df_1, df_2

col1, col2 = registro_estados()


def clientes(df: pd.DataFrame) -> pd.DataFrame:
    df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
    df_ots_clientes_1 = pd.merge(df, df_clientes, how='left', left_on='ots_rut_cliente', right_on='cliente_rut')
    df_ots_clientes_1 = df_ots_clientes_1.drop(columns=['cliente_rut'])
    df_ots_clientes_1['rut_name'] = df_ots_clientes_1['ots_rut_cliente'] +' | '+df_ots_clientes_1['cliente_nombre']
    return df_ots_clientes_1

def vehiculos():
    pass

def ots() -> pd.DataFrame:
    df_ots = ct.select_data(tabla="ots", where="deleted = 0", order="date_created DESC")
    return df_ots


def filtros_detalles(df: pd.DataFrame, rut_name=None, patente=None, estado=None) -> pd.DataFrame:
    if rut_name != None:
        df = df[df['rut_name']==rut_name]
    if patente != None:
        df = df[df['ots_v_patente']==patente]
    if estado != None:
        if estado=="Finalizadas":
            df = df[df['estado_tipo_nombre']=="Finalizada"]
        else:
            df = df[df['estado_tipo_nombre']!="Finalizada"]
    return df

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Ordenes de Trabajo', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Órdenes de Trabajo"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    if 'selected_id_ot' not in st.session_state:
        st.session_state['selected_id_ot'] = None

    col1, col2, col3, col4, col5, col6, col7 = st.columns((1,1,1,1,1.5,2,2))
    agregar = col1.button("Nueva OT ➕", type="primary")
    modificar = col2.button("Modificar OT 🖊️", type="primary")

    df_ots = ct.select_data(tabla="ots", where="deleted = 0", order="date_created DESC")

    df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
    df_ots_clientes_1 = pd.merge(df_ots, df_clientes, how='left', left_on='ots_rut_cliente', right_on='cliente_rut')
    df_ots_clientes_1 = df_ots_clientes_1.drop(columns=['cliente_rut'])
    df_ots_clientes_1['rut_name'] = df_ots_clientes_1['ots_rut_cliente'] +' | '+df_ots_clientes_1['cliente_nombre']

    df_log_ots = ct.select_data(tabla="log_ots", columns='log_ots_id, log_estado_ots_id, date_created, created_by', where="deleted = 0", order="date_created DESC")
    df_nombres_estados_ots = ct.select_data(tabla="estado_tipo", columns='estado_tipo_id, estado_tipo_nombre', where="deleted = 0")

    df_log_ots_2 = pd.merge(df_log_ots, df_nombres_estados_ots, how='left', left_on='log_estado_ots_id', right_on='estado_tipo_id')
    df_log_ots_2 = df_log_ots_2.drop(columns=['log_estado_ots_id', 'estado_tipo_id'])
    df_log_ots_3 = df_log_ots_2[['log_ots_id', 'estado_tipo_nombre', 'date_created', 'created_by']]

    max_log_ots = df_log_ots_3.groupby('log_ots_id').agg({'date_created': 'max'}).reset_index()
    max_log_ots = max_log_ots[['log_ots_id', 'date_created']]
    df_max_log_ots = pd.merge(df_log_ots_3, max_log_ots, how='inner', left_on=['log_ots_id', 'date_created'], right_on=['log_ots_id', 'date_created'])
    df_max_log_ots = df_max_log_ots.drop(columns=['date_created', 'created_by'])

    df_ots_clientes_2= pd.merge(df_ots_clientes_1, df_max_log_ots, how='left', left_on='ots_id', right_on='log_ots_id')
    df_ots_clientes_2 = df_ots_clientes_2.drop(columns=['log_ots_id'])

    df_cat_ots = ct.select_data(tabla="categorias_ots", columns='cat_id, cat_nombre', where="deleted = 0")

    df_ots_clientes_final = pd.merge(df_ots_clientes_2, df_cat_ots, how='left', left_on='ots_cat_id', right_on='cat_id')
    df_ots_clientes_final = df_ots_clientes_final.drop(columns=['cat_id', 'ots_cat_id'])

    df_ots_cabecera = df_ots_clientes_final[['ots_id', 
                                        'rut_name',
                                       'ots_rut_cliente', 
                                       'cliente_nombre', 
                                       'ots_v_patente', 
                                       "ots_v_marca", 
                                       "ots_v_modelo",
                                        'cat_nombre',
                                       'estado_tipo_nombre',
                                       'date_created',
                                       'created_by']]

    df_ots_detalle = df_ots_clientes_final[['ots_id', 
                                           'ots_rut_cliente', 
                                           'cliente_nombre', 
                                           'cliente_correo', 
                                           'cliente_telefono', 
                                           'cliente_direccion',
                                           'ots_v_patente', 
                                           'ots_v_marca',
                                           'ots_v_modelo', 
                                           'ots_v_año', 
                                           'ots_v_vin', 
                                           'ots_descripcion',
                                           'cat_nombre',
                                           'date_created', 
                                           'estado_tipo_nombre',
                                           'date_mod', 
                                           'created_by', 
                                           'mod_por']]


    with st.container(height=320): # Cabecera OT
        # df_ots['rut_name'] = df_ots['RUT Cliente'] +' | '+df_ots['Nombre Cliente']
        col1, col2 , col3 , col4= st.columns((1,0.5,0.5,1))
        #rut_filter = col1.selectbox("Buscar RUT", df_ots['RUT Cliente'].unique() , index=None, placeholder='RUT')
        rut_name_filter = col1.selectbox("Buscar Cliente", df_ots_cabecera['rut_name'].sort_values().unique() , index=None, placeholder='Cliente',label_visibility="collapsed")
        if rut_name_filter is not None:
            #df_ots = filtros_detalles(df_ots, rut=rut_filter)
            df_ots_cabecera = filtros_detalles(df_ots_cabecera, rut_name=rut_name_filter)

        patente_filter = col2.selectbox("Buscar Patente", df_ots_cabecera['ots_v_patente'].unique() , index=None, placeholder='Patente',label_visibility="collapsed")
        if patente_filter:
            df_ots_cabecera = filtros_detalles(df_ots_cabecera, patente=patente_filter)

        estado_filter = col3.selectbox("Buscar Estado", ("Abiertas","Finalizadas") , index=None, placeholder='Estado',label_visibility="collapsed")
        if estado_filter:
            df_ots_cabecera = filtros_detalles(df_ots_cabecera, estado=estado_filter)

        df_ots_cabecera = df_ots_cabecera.drop(columns=['rut_name'])

        df_ots_cabecera = df_ots_cabecera.rename(columns={'ots_id':'ID OT',
                                                        'ots_rut_cliente':'RUT Cliente',
                                                        'cliente_nombre':'Nombre Cliente',
                                                        'ots_v_patente':'Patente',
                                                        'ots_v_marca':'Marca',
                                                        'ots_v_modelo':'Modelo',
                                                        'cat_nombre':'Tipo Reparación',
                                                        'estado_tipo_nombre':'Estado OT',
                                                        'date_created':'Fecha Creación',
                                                        'created_by':'Creado Por'})

        df_ots_detalle = df_ots_detalle.rename(columns={'ots_id':'ID OT',
                                                        'ots_rut_cliente':'RUT Cliente',
                                                        'cliente_nombre':'Nombre Cliente',
                                                        'cliente_correo':'Correo Cliente',
                                                        'cliente_telefono':'Teléfono Cliente',
                                                        'cliente_direccion':'Dirección Cliente',
                                                        'ots_v_patente':'Patente',
                                                        'ots_v_marca':'Marca',
                                                        'ots_v_modelo':'Modelo',
                                                        'ots_v_año':'Año',
                                                        'ots_v_vin':'VIN',
                                                        'ots_descripcion':'Descripción',
                                                        'cat_nombre':'Tipo Reparación',
                                                        'estado_tipo_nombre':'Estado OT',
                                                        'date_created':'Fecha Creación',
                                                        'date_mod':'Fecha Modificación',
                                                        'created_by':'Creado Por', 
                                                        'mod_por':"Modificado Por"})

        data = st.dataframe(df_ots_cabecera,
                on_select='rerun',
                selection_mode='single-row',
                hide_index=True,
                height=220,
                use_container_width=True)
        
        if len(data.selection['rows']):
            selected_row = data.selection['rows'][0]
            selected_id_ot = df_ots_cabecera.iloc[selected_row]['ID OT']
            st.session_state['selected_id_ot'] = selected_id_ot
        else:
            selected_row = None
            selected_id_ot = None
            st.session_state['selected_id_ot'] = None
        
    
    with st.container(height=600):
        df_ejemplo = pd.DataFrame({
        "Id": ["AAAAA", "BBBBB", "CCCCC", "DDDDD", "EEEEE", "FFFFF", "GGGGG"],
        "Item": ["Pastillas","Amortiguadores","Uno","Fish","Cincuenta","Error","Botella"],
        "Cantidad": [74,82,1,5,50,11,2],
        "Precio Total": ["$1.555","222.444","$1","$666.666","$50","$321.123","$500"]
        })
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Info General", 
                                                            "Repuestos", 
                                                            "Servicios Extras", 
                                                            "Imágenes", 
                                                            "Cotizaciones", 
                                                            "Cobranza", 
                                                            "Registro Estados"])
        with tab1:
            if selected_row is not None:
                detalle = df_ots_detalle.iloc[[selected_row]]
                #data = st.dataframe(detalle, hide_index=True, height=300)
                cliente_info = detalle[['RUT Cliente','Nombre Cliente','Correo Cliente','Teléfono Cliente','Dirección Cliente']].transpose()
                vehiculo_info = detalle[['Patente','Marca','Modelo','Año','VIN']].transpose()
                ot_info = detalle[['ID OT','Descripción','Tipo Reparación','Estado OT','Fecha Creación','Creado Por']].transpose()
                
                cliente_info = cliente_info.rename(columns={selected_row:'Detalle'})
                vehiculo_info = vehiculo_info.rename(columns={selected_row:'Detalle'})
                ot_info = ot_info.rename(columns={selected_row:'Detalle'})

                col1, col2, col3, col4= st.columns((1,1,1,1))
                with col1:
                    st.markdown("<h4>"+"Cliente"+"</h4>", unsafe_allow_html=True)
                    st.dataframe(cliente_info, use_container_width=True)
                with col2:
                    st.markdown("<h4>"+"Vehículo"+"</h4>", unsafe_allow_html=True)
                    st.dataframe(vehiculo_info, use_container_width=True)
                with col3:
                    st.markdown("<h4>"+"OT"+"</h4>", unsafe_allow_html=True)
                    st.dataframe(ot_info, use_container_width=True)
                with col4:
                    st.markdown("<h4>"+"Info Venta"+"</h4>", unsafe_allow_html=True)
                    st.dataframe(detalle[['Estado OT','Fecha Modificación','Modificado Por']].transpose(), use_container_width=True)
                
            else:
                st.write("No hay OT seleccionada")
        with tab2:
            if selected_row is not None:
                agregar_repuesto = st.button(label="Agregar ➕", type="primary")

                repuestos

                data = st.dataframe(df_ejemplo, hide_index=True, height=300)
            else:
                st.write("No hay OT seleccionada")

        # with tab3:
        #     if st.button(label="Agregar ➕",key="a1", type="primary"):
        #         st.markdown("pog")
        #     df_ejemplo
        # with tab4:
        #     if st.button(label="Agregar 📷",key="a5", type="primary"):
        #         st.markdown("pog")
        #     col1, col2 = st.columns((1,1))
        #     col1.image("src\\img\\auto (1).jpg")
        #     col2.image("src\\img\\auto (2).jpg")
        #     col1.image("src\\img\\auto (3).jpg")
        #     col2.image("src\\img\\auto (4).jpg")
        #     col1.image("src\\img\\auto (5).jpg")
        #     col2.image("src\\img\\auto (6).jpg")
        # with tab5:
        #     if st.button(label="Agregar ➕",key="a2", type="primary"):
        #         st.markdown("pog")
        #     df_ejemplo
        # with tab6:
        #     if st.button(label="Agregar ➕",key="a3", type="primary"):
        #         st.markdown("pog")
        #     df_ejemplo
        # with tab7:
        #     if st.button(label="Agregar ➕",key="a4", type="primary"):
        #         st.markdown("pog")
        #     df_ejemplo      
        #st.write(st.session_state)

    #st.image("src\\img\\taller.png",use_container_width=True)
    #cent_co


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()