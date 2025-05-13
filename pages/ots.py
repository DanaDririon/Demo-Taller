import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os
from pathlib import Path

def delete_zip():
    #delete file with path
    os.remove(st.session_state['path_img_zipped'])
    st.session_state['ver_img'] = False
    del st.session_state['path_img_zipped']
    #st.rerun()

def repuestos(id_ots) -> pd.DataFrame:
    df_repuestos = ct.select_data(tabla='ots_det', 
                                  columns='ots_prov_prod, ' \
                                    'ots_item, ' \
                                    'ots_cant, ' \
                                    'ots_costo,' \
                                    'ots_precio_venta',
                                    where='ots_tipo_prod = 1 AND deleted = 0 AND ots_cab_id = {}'.format(id_ots)) # '1' = REPUESTOS
    df_repuestos['total_compra'] = df_repuestos['ots_costo'] * df_repuestos['ots_cant']
    df_repuestos['total_venta'] = df_repuestos['ots_precio_venta'] * df_repuestos['ots_cant']
    return df_repuestos

def servicios_extras(id_ots) -> pd.DataFrame:

    df = ct.select_data(tabla='ots_det', 
                                  columns='ots_item, ' \
                                    'ots_prov_prod, ' \
                                    'ots_costo,' \
                                    'ots_precio_venta',
                                    where='ots_tipo_prod = 3 AND deleted = 0 AND ots_cab_id = {}'.format(id_ots)) # '3' = SERVICIOS EXTRAS

    df['total_compra'] = df['ots_costo'].sum()
    df['total_venta'] = df['ots_precio_venta'].sum()
    return df

def imagenes(id_ots):
    df_img = ct.select_data(tabla="img", columns='img_dir', where="deleted = 0 and img_ots_id = {}".format(id_ots))
    #split img_dir by \ and take the last element
    df_img['img_dir'] = df_img['img_dir'].str.split('\\').str[-1]
    df_img['img_dir'] = df_img['img_dir'].astype(str)
    #apply img_dir as path
    df_img['img_dir'] = df_img['img_dir'].apply(lambda x: str(Path("src") / "img" / "ot" / "OT-{}".format(id_ots) / x))
    return df_img

def cotizaciones(id_ots):
    df_cotizaciones_cab = ct.select_data(tabla='cotiz_cab',
                                        columns='cotiz_id, cotiz_ots_id',
                                        where='deleted = 0 and cotiz_ots_id = {}'.format(id_ots)).reset_index()
    df_cotizaciones_cab['cotiz_ots_id'] = df_cotizaciones_cab['cotiz_ots_id'].astype(int)
    id_cabecera = df_cotizaciones_cab['cotiz_id'][0]
    df_cotizaciones_det = ct.select_data(tabla='cotiz_det',
                                        columns='cotiz_cab_id, cotiz_tipo_prod, cotiz_costo, cotiz_precio_venta',
                                        where='deleted = 0 and cotiz_cab_id = {}'.format(id_cabecera))
    df_cotizaciones_det['cotiz_tipo_prod'] = df_cotizaciones_det['cotiz_tipo_prod'].astype(int)
    df_cotizaciones_det['cotiz_cab_id'] = df_cotizaciones_det['cotiz_cab_id'].astype(int)
    #st.write(df_cotizaciones_det)
    df_cotizaciones_det = df_cotizaciones_det.groupby(['cotiz_cab_id','cotiz_tipo_prod']).agg({'cotiz_costo':'sum',
                                                                'cotiz_precio_venta':'sum',}).reset_index()
    df_cotiz = pd.merge(df_cotizaciones_cab, df_cotizaciones_det, how='left', left_on='cotiz_id', right_on='cotiz_cab_id').drop(columns=['cotiz_cab_id'])
    #st.write(df_cotiz)
    df_cotiz['margen'] = df_cotiz['cotiz_precio_venta'] - df_cotiz['cotiz_costo']
    df_cotiz['porc_margen'] = round((df_cotiz['margen'] / df_cotiz['cotiz_precio_venta']) * 100,2)

    df_tipo_prod = ct.select_data(tabla='tipo_prod',
                                  columns='tipo_prod_id, tipo_prod_descripcion',
                                  where='deleted = 0')
    df_tipo_prod['tipo_prod_id'] = df_tipo_prod['tipo_prod_id'].astype(int)
    df_cotiz = pd.merge(df_cotiz, df_tipo_prod, how='left', left_on='cotiz_tipo_prod', right_on='tipo_prod_id')
    df_cotiz = df_cotiz.drop(columns=['cotiz_tipo_prod', 'tipo_prod_id'])

    return df_cotiz

def pagos(id_ots):
    df = ct.select_data(tabla='pagos',
                        columns='pagos_id, pagos_ots_id, pagos_tipo_pago, pagos_monto, pagos_num_comprobante,pagos_fecha_pago,created_by,date_created',
                        where='deleted = 0 and pagos_ots_id = {}'.format(id_ots))
    #df['pagos_ots_id'] = df['pagos_ots_id'].astype(int)
    return df

def clientes(df: pd.DataFrame) -> pd.DataFrame:
    df_clientes = ct.select_data(tabla='clientes', columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
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

def escribe():
    st.write("Escribiendo en el archivo...")

def main():
    
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Órdenes de Trabajo', page_icon="src\\img\\taller_img\\icon_taller.jpg")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Órdenes de Trabajo"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    if 'selected_id_ot' not in st.session_state:
        st.session_state['selected_id_ot'] = None

    if 'button_disabled' not in st.session_state:
        st.session_state.button_disabled = True

    col111, col222, col333, col444, col555, col666, col777 = st.columns((1,1,1,1,1,2,2))
    if col111.button("Nueva OT", type="primary",icon=":material/add:"):
        ct.switch_page("ots_nueva.py")

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
        col1, col2 , col3 , col4= st.columns((1,0.5,0.5,1))
        rut_name_filter = col1.selectbox("Buscar Cliente", df_ots_cabecera['rut_name'].sort_values().unique() , index=None, placeholder='Cliente',label_visibility="collapsed")
        if rut_name_filter is not None:
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
            st.session_state.button_disabled = False
        else:
            selected_row = None
            selected_id_ot = None
            st.session_state['selected_id_ot'] = None
            st.session_state.button_disabled = True

    modificar = col222.button("Modificar", type="primary",icon=":material/edit:", disabled=st.session_state.button_disabled)
    descargar = col333.button("Descargar PDF", type="primary",icon=":material/download:", disabled=st.session_state.button_disabled)
    
    with st.container(height=600):
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Info General", 
                                                            "Repuestos", 
                                                            "Servicios Extras",
                                                            "Mano de Obra", 
                                                            "Imágenes", 
                                                            "Cotizaciones", 
                                                            "Pagos", 
                                                            "Registro Estados"])

        with tab2: # Repuestos
            if selected_row is not None:
                df_repuestos = repuestos(selected_id_ot)
                agregar_repuesto = st.button(label="Agregar", type="primary", icon=":material/add:")
                repuestos_filtered = df_repuestos#[df_repuestos['repuesto_ots_id'] == selected_id_ot]
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
                sum_valores_repuestos_final = sum_valores_repuestos
                #set format to currency
                sum_valores_repuestos = sum_valores_repuestos.style.format({'Total Compra':'${:,.0f}',
                                                                            'Total Venta':'${:,.0f}',
                                                                            '$ Margen':'${:,.0f}',
                                                                            '% Margen':'{:.2f}%'})

                #repuestos_filtered = repuestos_filtered.drop(columns=['repuesto_ots_id'])
                repuestos_filtered = repuestos_filtered.rename(columns={#'repuesto_id':'ID Repuesto',
                                                                        'ots_prov_prod':'Proveedor',
                                                                        'ots_item':'Item',
                                                                        'ots_cant':'Cantidad',
                                                                        'ots_costo':'Precio Compra Unit',
                                                                        'ots_precio_venta':'Precio Venta Unit',
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

        with tab3: # Servicios Extras
            if selected_row is not None:
                st.button(label="Agregar Serv Extra", key="serv_extra_button", type="primary", icon=":material/add:")
                df_serv_extras = servicios_extras(selected_id_ot)
                serv_extras_filtered = df_serv_extras#[df_serv_extras['serv_ots_id'] == selected_id_ot]
                
                #serv_extras_filtered = serv_extras_filtered[serv_extras_filtered['serv_ots_id'] == selected_id_ot]
                serv_extras_filtered['margen'] = serv_extras_filtered['ots_precio_venta'] - serv_extras_filtered['ots_costo']
                serv_extras_filtered['porc_margen'] = round((serv_extras_filtered['margen'] / serv_extras_filtered['ots_precio_venta']) * 100,2)
                serv_extras_filtered = pd.DataFrame(serv_extras_filtered)
                #serv_extras_filtered = serv_extras_filtered.drop(columns=['serv_ots_id'])
                serv_extras_filtered = serv_extras_filtered.rename(columns={#'serv_extra_id':'ID Serv Extra',
                                                                            'ots_item':'Descripción',
                                                                            'ots_prov_prod':'Proveedor',
                                                                            'ots_costo':'Costo Unitario',
                                                                            'ots_precio_venta':'Precio Venta Unit',
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
                sum_valores_serv_extras_final = sum_valores_serv_extras
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
        with tab4: # Mano de Obra
            st.write("En proceso de desarrollo")

        with tab1: # Info General
            if selected_row is not None:
                detalle = df_ots_detalle.iloc[[selected_row]]
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
                print(sum_valores_repuestos_final['Total Compra'])
                info_venta = pd.DataFrame({'Detalle':["Repuestos","Servicios Extras","Mano de Obra","Otros","Total"],
                                           'Costo':[sum_valores_repuestos_final['Total Compra']['Valores'],sum_valores_serv_extras_final['Total Costo']['Valores'],0,0,int(sum_valores_repuestos_final['Total Compra']['Valores'])+int(sum_valores_serv_extras_final['Total Costo']['Valores'])],
                                           'Venta':[sum_valores_repuestos_final['Total Venta']['Valores'],sum_valores_serv_extras_final['Total Venta']['Valores'],0,0,int(sum_valores_repuestos_final['Total Venta'])+int(sum_valores_serv_extras_final['Total Venta'])],
                                           '% Margen':[sum_valores_repuestos_final['% Margen']['Valores'],sum_valores_serv_extras_final['% Margen']['Valores'],0,0,""],
                                           '$ Margen':[sum_valores_repuestos_final['$ Margen']['Valores'],sum_valores_serv_extras_final['$ Margen']['Valores'],0,0,""]})
                # info_venta = info_venta.style.format({'Costo':'${:,.0f}',
                #                                             'Venta':'${:,.0f}',
                #                                             '% Margen':'{:.2f}%',
                #                                             '$ Margen':'${:,.0f}'})
                #info_venta = detalle[['Estado OT','Fecha Modificación','Modificado Por']].transpose()
                
                cliente_info = cliente_info.rename(columns={selected_row:'Detalle'})
                vehiculo_info = vehiculo_info.rename(columns={selected_row:'Detalle'})
                ot_info = ot_info.rename(columns={selected_row:'Detalle'})
                #info_venta = info_venta.rename(columns={selected_row:'Detalle'})
                
                cliente_info['Detalle'] = cliente_info['Detalle'].astype(str)
                vehiculo_info['Detalle'] = vehiculo_info['Detalle'].astype(str)
                ot_info['Detalle'] = ot_info['Detalle'].astype(str)
                #info_venta['Detalle'] = info_venta['Detalle'].astype(str)
                
                
                

                col1, col2, col3, col4= st.columns((1,1,1,1.5))
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
                    st.dataframe(info_venta, use_container_width=True,hide_index=True)
                
            else:
                st.write("No hay OT seleccionada")
        with tab5: # Imágenes
            if selected_row is not None:
                list_img = imagenes(selected_id_ot)
                
                #st.write(list_img)
                col1, col2, col3 = st.columns((1,1,1))
                if len(list_img) > 0:
                    if len(list_img) < 9:
                        insert_img = col1.button(label="Agregar Imágenes",key="a1", type="primary",icon=":material/add:")    
                    check_img_download = col2.checkbox(label="Preparar Zip Imagenes", key="ver_img", value=False)                
                    if check_img_download:
                        
                        path = str(Path("src") / "img" / "ot" / "OT-{}".format(selected_id_ot))
                        #create unique name file
                        name_file = "OT-{}-{}.zip".format(selected_id_ot, pd.Timestamp.now().strftime("%Y-%m-%d %H-%M-%S"))
                        name_file_zip = "Imagenes OT-{}.zip".format(selected_id_ot)
                        path_img_zipped = ct.create_image_zip(name_file, path, "ots")
                        st.session_state['path_img_zipped'] = path_img_zipped
                        with open(path_img_zipped, 'rb') as file:
                            col3.download_button(label="Descargar Imágenes", key="descarga", data=file, file_name=name_file_zip, mime="application/zip", on_click=delete_zip)
                    for i in range(len(list_img)):
                        if i % 2 == 0:
                            col1.image(list_img['img_dir'][i], width=720)
                        else:
                            col2.image(list_img['img_dir'][i], width=720)
                else:
                    st.write("No hay imágenes disponibles")
                    insert_img = col1.button(label="Agregar Imágenes",key="a2", type="primary",icon=":material/add:")
            else:
                st.write("No hay OT seleccionada")
        with tab6: # Cotizaciones
            if selected_row is not None:
                try: 
                    cotizaciones(selected_id_ot)
                except:
                    st.write("No hay cotización asociada a esta OT.")
                else:
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

        with tab7: # Pagos
            if selected_row is not None:
                df_pagos = pagos(selected_id_ot)
                st.button(label="Añadir Pagos",key="a4", type="primary", icon=":material/add:")
                df_pagos_filtered = df_pagos[df_pagos['pagos_ots_id'] == selected_id_ot]
                df_pagos_filtered = df_pagos_filtered.drop(columns=['pagos_ots_id'])
                df_pagos_filtered = df_pagos_filtered.rename(columns={'pagos_id':'ID Pago',
                                                            'pagos_tipo_pago':'Tipo Pago',
                                                            'pagos_monto':'Monto',
                                                            'pagos_num_comprobante':'Num Comprobante',
                                                            'pagos_fecha_pago':'Fecha Pago',
                                                            'created_by':'Creado Por'})
                st.dataframe(df_pagos_filtered, hide_index=True, width=1500)

        with tab8: # Registro Estados
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