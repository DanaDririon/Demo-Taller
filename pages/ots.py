import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os


def repuestos(id_ots) -> pd.DataFrame:
    df_repuestos = ct.select_data(tabla="repuestos", 
                                  columns='repuesto_id, ' \
                                    'repuesto_proveedor, ' \
                                    'repuesto_item, ' \
                                    'repuesto_cantidad, ' \
                                    'repuesto_precio_compra,' \
                                    'repuesto_precio_venta,' \
                                    'repuesto_ots_id' , 
                                    where="deleted = 0 and repuesto_ots_id = {}".format(id_ots))
    df_repuestos['total_compra'] = df_repuestos['repuesto_precio_compra'] * df_repuestos['repuesto_cantidad']
    df_repuestos['total_venta'] = df_repuestos['repuesto_precio_venta'] * df_repuestos['repuesto_cantidad']
    return df_repuestos

def servicios_extras(id_ots) -> pd.DataFrame:

    df = ct.select_data(tabla="serv_extra", 
                                  columns='serv_extra_id,' \
                                  'serv_ots_id, ' \
                                    'serv_extra_desc, ' \
                                    'serv_extra_proveedor, ' \
                                    'serv_extra_costo,' \
                                    'serv_extra_precio_venta',
                                    where="deleted = 0 and serv_ots_id = {}".format(id_ots))

    #df['total_compra'] = df['serv_extra_costo'].sum()
    #df['total_venta'] = df['serv_extra_precio_venta'].sum()
    return df

def imagenes():
    pass

def cotizaciones(id_ots):
    df_cotizaciones_cab = ct.select_data(tabla="cotiz_cab",
                                        columns='cotiz_id, cotiz_ots_id',
                                        where="deleted = 0 and cotiz_ots_id = {}".format(id_ots))
    df_cotizaciones_cab['cotiz_ots_id'] = df_cotizaciones_cab['cotiz_ots_id'].astype(int)
    id_cabecera = df_cotizaciones_cab['cotiz_id'].values[0]
    df_cotizaciones_det = ct.select_data(tabla="cotiz_det",
                                        columns='cotiz_cab_id, cotiz_tipo_prod, cotiz_costo, cotiz_precio_venta',
                                        where="deleted = 0 and cotiz_cab_id = {}".format(id_cabecera))
    df_cotizaciones_det['cotiz_tipo_prod'] = df_cotizaciones_det['cotiz_tipo_prod'].astype(int)
    df_cotizaciones_det['cotiz_cab_id'] = df_cotizaciones_det['cotiz_cab_id'].astype(int)
    #st.write(df_cotizaciones_det)
    df_cotizaciones_det = df_cotizaciones_det.groupby(['cotiz_cab_id','cotiz_tipo_prod']).agg({'cotiz_costo':'sum',
                                                                'cotiz_precio_venta':'sum',}).reset_index()
    df_cotiz = pd.merge(df_cotizaciones_cab, df_cotizaciones_det, how='left', left_on='cotiz_id', right_on='cotiz_cab_id').drop(columns=['cotiz_cab_id'])
    #st.write(df_cotiz)
    df_cotiz['margen'] = df_cotiz['cotiz_precio_venta'] - df_cotiz['cotiz_costo']
    df_cotiz['porc_margen'] = round((df_cotiz['margen'] / df_cotiz['cotiz_precio_venta']) * 100,2)

    df_tipo_prod = ct.select_data(tabla="tipo_prod",
                                  columns='tipo_prod_id, tipo_prod_descripcion',
                                  where="deleted = 0")
    df_tipo_prod['tipo_prod_id'] = df_tipo_prod['tipo_prod_id'].astype(int)
    df_cotiz = pd.merge(df_cotiz, df_tipo_prod, how='left', left_on='cotiz_tipo_prod', right_on='tipo_prod_id')
    df_cotiz = df_cotiz.drop(columns=['cotiz_tipo_prod', 'tipo_prod_id'])

    return df_cotiz

def pagos(id_ots):
    df = ct.select_data(tabla="pagos",
                        columns='pagos_id, pagos_ots_id, pagos_tipo_pago, pagos_monto, pagos_num_comprobante,pagos_fecha_pago,created_by,date_created',
                        where="deleted = 0 and pagos_ots_id = {}".format(id_ots))
    #df['pagos_ots_id'] = df['pagos_ots_id'].astype(int)
    return df

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
    # fill NA from estado_tipo_nombre
    df_max_log_ots['estado_tipo_nombre'] = df_max_log_ots['estado_tipo_nombre'].fillna('En preparación')
    df_max_log_ots = df_max_log_ots.drop(columns=['date_created', 'created_by'])

    df_ots_clientes_2= pd.merge(df_ots_clientes_1, df_max_log_ots, how='left', left_on='ots_id', right_on='log_ots_id')
    df_ots_clientes_2 = df_ots_clientes_2.drop(columns=['log_ots_id'])

    df_cat_ots = ct.select_data(tabla="categorias_ots", columns='cat_id, cat_nombre', where="deleted = 0")

    df_ots_clientes_final = pd.merge(df_ots_clientes_2, df_cat_ots, how='left', left_on='ots_cat_id', right_on='cat_id')
    df_ots_clientes_final = df_ots_clientes_final.drop(columns=['cat_id', 'ots_cat_id'])

    
    #df_serv_extras = servicios_extras()
    #df_cotizaciones = cotizaciones()
    #df_pagos = pagos()
    #df_sum_repuestos = df_repuestos.groupby(['repuesto_ots_id']).agg({'repuesto_precio_compra':'sum',
    #                                                            'repuesto_precio_venta':'sum',}).reset_index()


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
                                           'ots_rut_facturacion',
                                           'ots_nombre_facturacion',
                                           'ots_dir_facturacion',
                                           'ots_telefono_facturacion',
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
                                                        'ots_rut_facturacion':'RUT Facturación',
                                                        'ots_nombre_facturacion':'Nombre Facturación',
                                                        'ots_dir_facturacion':'Dirección Facturación',
                                                        'ots_telefono_facturacion':'Teléfono Facturación',
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
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Info General", 
                                                            "Repuestos", 
                                                            "Servicios Extras",
                                                            "Mano de Obra", 
                                                            "Imágenes", 
                                                            "Cotizaciones", 
                                                            "Cobranza", 
                                                            "Registro Estados"])
        with tab1:
            if selected_row is not None:
                detalle = df_ots_detalle.iloc[[selected_row]]
                #data = st.dataframe(detalle, hide_index=True, height=300)
                cliente_info = detalle[['RUT Cliente',
                                        'Nombre Cliente',
                                        'Correo Cliente',
                                        'Teléfono Cliente',
                                        'Dirección Cliente',
                                        'RUT Facturación',
                                        'Nombre Facturación',
                                        'Dirección Facturación',
                                        'Teléfono Facturación']].transpose()
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
                df_repuestos = repuestos(selected_id_ot)
                agregar_repuesto = st.button(label="Agregar ➕", type="primary")
                repuestos_filtered = df_repuestos[df_repuestos['repuesto_ots_id'] == selected_id_ot]
                repuestos_filtered['margen'] = repuestos_filtered['total_venta'] - repuestos_filtered['total_compra']
                repuestos_filtered['porc_margen'] = round((repuestos_filtered['margen'] / repuestos_filtered['total_venta']) * 100,2)
                
                df_sum_repuestos = pd.DataFrame(repuestos_filtered.rename(columns={'total_compra':'Total Compra',
                                                                       'total_venta':'Total Venta'}))
                sum_valores_repuestos = df_sum_repuestos.agg({'Total Compra':'sum',
                                                           'Total Venta':'sum'} ).reset_index()
                sum_valores_repuestos = sum_valores_repuestos.rename(columns={'index':'Datos', 0:'Valores'})
                #set Datos as columns and Valores as values
                sum_valores_repuestos = sum_valores_repuestos.set_index('Datos').T
                sum_valores_repuestos['$ Margen'] = sum_valores_repuestos['Total Venta'] - sum_valores_repuestos['Total Compra']
                sum_valores_repuestos['% Margen'] = round((sum_valores_repuestos['$ Margen'] / sum_valores_repuestos['Total Venta']) * 100,2)
                #set format to currency
                sum_valores_repuestos = sum_valores_repuestos.style.format({'Total Compra':'${:,.0f}',
                                                                            'Total Venta':'${:,.0f}',
                                                                            '$ Margen':'${:,.0f}',
                                                                            '% Margen':'{:.2f}%'})

                repuestos_filtered = repuestos_filtered.drop(columns=['repuesto_ots_id'])
                repuestos_filtered = repuestos_filtered.rename(columns={'repuesto_id':'ID Repuesto',
                                                                        'repuesto_proveedor':'Proveedor',
                                                                        'repuesto_item':'Item',
                                                                        'repuesto_cantidad':'Cantidad',
                                                                        'repuesto_precio_compra':'Precio Compra Unit',
                                                                        'repuesto_precio_venta':'Precio Venta Unit',
                                                                        'total_compra':'Precio Total Compra',
                                                                        'total_venta':'Precio Total Venta',
                                                                        'margen':'Margen',
                                                                        'porc_margen':'% Margen'})
                #set format to currency
                repuestos_filtered = repuestos_filtered.style.format({'Precio Compra Unit':'${:,.0f}',
                                                                        'Precio Venta Unit':'${:,.0f}',
                                                                        'Precio Total Compra':'${:,.0f}',
                                                                        'Precio Total Venta':'${:,.0f}',
                                                                        'Margen':'${:,.0f}',
                                                                        '% Margen':'{:.2f}%'})

                col1, col2 = st.columns((3,2))
                col1.dataframe(repuestos_filtered, hide_index=True, use_container_width=True)
                col2.dataframe(sum_valores_repuestos, hide_index=True, use_container_width=True)
            else:
                st.write("No hay OT seleccionada")

        with tab3:
            if selected_row is not None:
                st.button(label="Agregar Serv Extra ➕",key="serv_extra_button", type="primary")
                df_serv_extras = servicios_extras(selected_id_ot)
                serv_extras_filtered = df_serv_extras[df_serv_extras['serv_ots_id'] == selected_id_ot]
                
                serv_extras_filtered = serv_extras_filtered[serv_extras_filtered['serv_ots_id'] == selected_id_ot]
                serv_extras_filtered['margen'] = serv_extras_filtered['serv_extra_precio_venta'] - serv_extras_filtered['serv_extra_costo']
                serv_extras_filtered['porc_margen'] = round((serv_extras_filtered['margen'] / serv_extras_filtered['serv_extra_precio_venta']) * 100,2)
                serv_extras_filtered = pd.DataFrame(serv_extras_filtered)
                serv_extras_filtered = serv_extras_filtered.drop(columns=['serv_ots_id'])
                serv_extras_filtered = serv_extras_filtered.rename(columns={'serv_extra_id':'ID Serv Extra',
                                                                            'serv_extra_desc':'Descripción',
                                                                            'serv_extra_proveedor':'Proveedor',
                                                                            'serv_extra_costo':'Costo Unitario',
                                                                            'serv_extra_precio_venta':'Precio Venta Unit',
                                                                            'margen':'Margen',
                                                                            'porc_margen':'% Margen'})


                sum_valores_serv_extras = serv_extras_filtered.agg({'Costo Unitario':'sum',
                                                            'Precio Venta Unit':'sum'} ).reset_index()
                sum_valores_serv_extras = sum_valores_serv_extras.rename(columns={'index':'Datos', 0:'Valores'})
                #set Datos as columns and Valores as values
                sum_valores_serv_extras = sum_valores_serv_extras.set_index('Datos').T
                sum_valores_serv_extras = sum_valores_serv_extras.rename(columns={'Costo Unitario':'Total Costo',
                                                                            'Precio Venta Unit':'Total Venta'})
                sum_valores_serv_extras['$ Margen'] = sum_valores_serv_extras['Total Venta'] - sum_valores_serv_extras['Total Costo']
                sum_valores_serv_extras['% Margen'] = round((sum_valores_serv_extras['$ Margen'] / sum_valores_serv_extras['Total Venta']) * 100,2)
                #set format to currency
                sum_valores_serv_extras = sum_valores_serv_extras.style.format({'Total Costo':'${:,.0f}',
                                                                            'Total Venta':'${:,.0f}',
                                                                            '$ Margen':'${:,.0f}',
                                                                            '% Margen':'{:.2f}%'})
                
                col1, col2 = st.columns((3,2))
                col1.dataframe(serv_extras_filtered, hide_index=True, use_container_width=True)
                col2.dataframe(sum_valores_serv_extras, hide_index=True, use_container_width=True)
            else:
                st.write("No hay OT seleccionada")
        with tab4:
            st.write("En proceso de desarrollo")

        with tab5:
            if selected_row is not None:
                st.button(label="Agregar 📷",key="a5", type="primary")
                col1, col2 = st.columns((1,1))
                col1.image("src\\img\\auto (1).jpg")
                col2.image("src\\img\\auto (2).jpg")
                col1.image("src\\img\\auto (3).jpg")
                col2.image("src\\img\\auto (4).jpg")
                col1.image("src\\img\\auto (5).jpg")
                col2.image("src\\img\\auto (6).jpg")
            else:
                st.write("No hay OT seleccionada")
        with tab6:
            if selected_row is not None:
                st.button(label="Ir a Detalle",key="a3", type="primary")
                df_cotizaciones = cotizaciones(selected_id_ot)
                df_cotizaciones_filtered = df_cotizaciones[df_cotizaciones['cotiz_ots_id'] == selected_id_ot]
                df_cotizaciones_filtered = df_cotizaciones_filtered[['cotiz_id',
                                                                    'cotiz_ots_id',
                                                            'tipo_prod_descripcion',
                                                            'cotiz_costo',
                                                            'cotiz_precio_venta',
                                                            'margen',
                                                            'porc_margen']]
                df_cotizaciones_filtered = df_cotizaciones_filtered.rename(columns={'cotiz_id':'ID Cotización',
                                            'cotiz_ots_id':'ID OT',
                                            'tipo_prod_descripcion':'Tipo Producto',
                                            'cotiz_costo':'Costo Unitario',
                                            'cotiz_precio_venta':'Precio Venta Unit',
                                            'margen':'Margen',
                                            'porc_margen':'% Margen'})
                
                df_cotizaciones_filtered = df_cotizaciones_filtered.style.format({'Costo Unitario':'${:,.0f}',
                                                                            'Precio Venta Unit':'${:,.0f}',
                                                                            'Margen':'${:,.0f}',
                                                                            '% Margen':'{:.2f}%'})

                st.dataframe(df_cotizaciones_filtered, hide_index=True, width=1000, on_select='rerun', selection_mode='single-row')
            else:
                st.write("No hay OT seleccionada")

        with tab7:
            if selected_row is not None:
                df_pagos = pagos(selected_id_ot)
                st.button(label="Añadir Pagos ➕",key="a4", type="primary")
                df_pagos_filtered = df_pagos[df_pagos['pagos_ots_id'] == selected_id_ot]
                df_pagos_filtered = df_pagos_filtered.drop(columns=['pagos_ots_id'])
                df_pagos_filtered = df_pagos_filtered.rename(columns={'pagos_id':'ID Pago',
                                                            'pagos_tipo_pago':'Tipo Pago',
                                                            'pagos_monto':'Monto',
                                                            'pagos_num_comprobante':'Num Comprobante',
                                                            'pagos_fecha_pago':'Fecha Pago',
                                                            'created_by':'Creado Por'})
                st.dataframe(df_pagos_filtered, hide_index=True, width=1500)

        with tab8:
            if selected_row is not None:
                df_log_filtered = df_log_ots_3[df_log_ots_3['log_ots_id']==selected_id_ot]
                df_log_filtered = df_log_filtered.rename(columns={'log_ots_id':'ID OT',
                                                            'estado_tipo_nombre':'Estado OT',
                                                            'date_created':'Fecha',
                                                            'created_by':'Creado Por'})
                st.dataframe(df_log_filtered, hide_index=True, width=700)
            else:
                st.write("No hay OT seleccionada")


if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()