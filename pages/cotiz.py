import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os
def cotizaciones_cabecera():
    df_cotizaciones_cab = ct.select_data(tabla="cotiz_cab",
                                        columns='cotiz_id, cotiz_ots_id, cotiz_rut_cliente, cotiz_nombre_facturacion, cotiz_patente, cotiz_marca, cotiz_modelo, cotiz_year, date_created',
                                        where="deleted = 0")
    df_cotizaciones_cab['cotiz_ots_id'] = df_cotizaciones_cab['cotiz_ots_id'].astype(int)
    df_cotizaciones_cab = df_cotizaciones_cab.fillna('')
    df_cotizaciones_det = ct.select_data(tabla="cotiz_det",
                                        columns='cotiz_cab_id, cotiz_costo, cotiz_precio_venta',
                                        where="deleted = 0")
    
    df_cotiz = pd.merge(df_cotizaciones_cab, df_cotizaciones_det, how='left', left_on='cotiz_id', right_on='cotiz_cab_id').drop(columns=['cotiz_cab_id'])
    df_cotiz = df_cotiz.groupby(['cotiz_id', 'cotiz_ots_id', 'cotiz_rut_cliente', 'cotiz_nombre_facturacion','cotiz_patente', 'cotiz_marca','cotiz_modelo','cotiz_year', 'date_created'], as_index=False).agg({'cotiz_costo': 'sum', 'cotiz_precio_venta': 'sum'})
    
    df_cotiz['margen'] = df_cotiz['cotiz_precio_venta'] - df_cotiz['cotiz_costo']
    df_cotiz['porc_margen'] = round((df_cotiz['margen'] / df_cotiz['cotiz_precio_venta']) * 100,2)
    df_cotiz = df_cotiz.rename(columns={'cotiz_id': 'ID Cotizacion', 'cotiz_ots_id': 'OT Asociada', 'cotiz_rut_cliente': 'Rut Cliente',
                                        'cotiz_nombre_facturacion': 'Nombre Facturacion', 'cotiz_patente': 'Patente',
                                         'cotiz_marca': 'Marca', 'cotiz_modelo': 'Modelo', 'cotiz_year': 'Año',
                                          'date_created': 'Fecha Creacion',
                                        'cotiz_costo': 'Costo', 'cotiz_precio_venta': 'Precio Venta', 'margen': 'Margen',
                                        'porc_margen': '% Margen'})
    df_cotiz = df_cotiz.sort_values(by=['Fecha Creacion'], ascending=False)
    return df_cotiz

def cotizaciones_detalle(id_cotizacion):
    df_cotizaciones_det = ct.select_data(tabla="cotiz_det",
                                        columns='cotiz_cab_id, cotiz_tipo_prod, cotiz_item, cotiz_cantidad, cotiz_costo, cotiz_precio_venta',
                                        where="deleted = 0 and cotiz_cab_id = {}".format(id_cotizacion))
    df_cotizaciones_det['cotiz_cab_id'] = df_cotizaciones_det['cotiz_cab_id'].astype(int)
    df_cotizaciones_det['cotiz_tipo_prod'] = df_cotizaciones_det['cotiz_tipo_prod'].astype(int)
    df_tipo_prod = ct.select_data(tabla="tipo_prod",
                                  columns='tipo_prod_id, tipo_prod_descripcion',
                                  where="deleted = 0")
    df_tipo_prod['tipo_prod_id'] = df_tipo_prod['tipo_prod_id'].astype(int)
    df_cotiz_det = pd.merge(df_cotizaciones_det, df_tipo_prod, how='left', left_on='cotiz_tipo_prod', right_on='tipo_prod_id')
    df_cotiz_det = df_cotiz_det.drop(columns=['cotiz_tipo_prod', 'tipo_prod_id', 'cotiz_cab_id'])
    df_cotiz_det = df_cotiz_det[['tipo_prod_descripcion', 'cotiz_item', 'cotiz_cantidad', 'cotiz_costo', 'cotiz_precio_venta']]
    df_cotiz_det['margen'] = df_cotiz_det['cotiz_precio_venta'] - df_cotiz_det['cotiz_costo']
    df_cotiz_det['porc_margen'] = round((df_cotiz_det['margen'] / df_cotiz_det['cotiz_precio_venta']) * 100,2)
    df_cotiz_det = df_cotiz_det.rename(columns={'tipo_prod_descripcion': 'Tipo Producto',
                                                'cotiz_item': 'Item', 'cotiz_cantidad': 'Cantidad', 'cotiz_costo': 'Costo',
                                                'cotiz_precio_venta': 'Precio Venta', 'margen': 'Margen', 'porc_margen': '% Margen'})
    df_cotiz_det = df_cotiz_det.sort_values(by=['Tipo Producto','Item'], ascending=True)

    df_cotiz_det_resumen = df_cotiz_det.groupby(['Tipo Producto'], as_index=False).agg({'Costo': 'sum', 'Precio Venta': 'sum'})
    df_cotiz_det_resumen['Margen'] = df_cotiz_det_resumen['Precio Venta'] - df_cotiz_det_resumen['Costo']
    df_cotiz_det_resumen['% Margen'] = round((df_cotiz_det_resumen['Margen'] / df_cotiz_det_resumen['Precio Venta']) * 100,2)
    # df_cotiz_det_resumen = df_cotiz_det_resumen.drop(columns=['ID Cotizacion'])
    return df_cotiz_det, df_cotiz_det_resumen

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Cotizaciones', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Cotizaciones"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    col1_a, col2_a, col3_a, col4_a, col5_a, col6_a = st.columns((1,1,1,0.8,1,2.5))
    nueva_cotiz = col1_a.button(label="Nueva Cotización ➕", type="primary")
    if nueva_cotiz:
        ct.switch_page("cotiz_nueva.py")


    #df_cotizaciones

    with st.container(height=400):
        st.subheader("Cotizaciones")
        df_cotizaciones = cotizaciones_cabecera()
        df_cotizaciones_styler = df_cotizaciones.style.format({'Costo': '${:,.0f}'.format,
                                    'Precio Venta': '${:,.0f}'.format,
                                    'Margen': '${:,.0f}'.format,
                                    '% Margen': '{:,.2f}%'.format})
        data = st.dataframe(df_cotizaciones_styler, hide_index=True, use_container_width=True, on_select="rerun", selection_mode="single-row")

    if len(data.selection['rows']):
        selected_row = data.selection['rows'][0]
        selected_id_cotiz = df_cotizaciones.iloc[selected_row]['ID Cotizacion']
        st.session_state['selected_id_ctoiz'] = selected_id_cotiz
        modificar_cotiz = col2_a.button(label="Modificar Cotización 🖊️", type="primary",disabled=False)
        add_items = col3_a.button(label="Modificar Detalle 📝", type="primary",disabled=False)
        generar_ot = col4_a.button(label="Generar OT 📋", type="primary",disabled=False)
    else:
        col2_a.button(label="Modificar Cotización 🖊️", type="primary",disabled=True)
        col3_a.button(label="Modificar Detalle 📝", type="primary",disabled=True)
        col4_a.button(label="Generar OT 📋", type="primary",disabled=True)
        col5_a.button(label="Descargar PDF 📥", type="primary",disabled=True)
        selected_row = None
        selected_id_cotiz = None
        st.session_state['selected_id_ctoiz'] = None
    
    with st.container(height=500):
        st.subheader("Detalles")
        if selected_id_cotiz is not None:
            df_cotizaciones_det, df_cotiz_det_resumen = cotizaciones_detalle(selected_id_cotiz)
            df_cotizaciones_det_styler = df_cotizaciones_det.style.format({'Costo': '${:,.0f}'.format,
                                    'Precio Venta': '${:,.0f}'.format,
                                    'Margen': '${:,.0f}'.format,
                                    '% Margen': '{:,.2f}%'.format})
            df_cotiz_det_resumen_styler = df_cotiz_det_resumen.style.format({'Costo': '${:,.0f}'.format,
                                    'Precio Venta': '${:,.0f}'.format,
                                    'Margen': '${:,.0f}'.format,
                                    '% Margen': '{:,.2f}%'.format})
            col1, col2 = st.columns((3,1.5))

            col1.dataframe(df_cotizaciones_det_styler, hide_index=True, use_container_width=True)
            col2.dataframe(df_cotiz_det_resumen_styler, hide_index=True, use_container_width=True)

            datos = {
                'tipo_documento': 'Cotizacion',
                'num_documento' : selected_id_cotiz,
                'nombre_cliente': df_cotizaciones.iloc[selected_row]['Nombre Facturacion'],
                'fecha_ingreso': pd.to_datetime(df_cotizaciones.iloc[selected_row]['Fecha Creacion']).strftime('%d-%m-%Y'),
                'fecha_entrega' : '',
                'marca': df_cotizaciones.iloc[selected_row]['Marca'],
                'modelo': df_cotizaciones.iloc[selected_row]['Modelo'],
                'year': df_cotizaciones.iloc[selected_row]['Año'],
                'patente': df_cotizaciones.iloc[selected_row]['Patente'],
                'kilometraje' : '',
                'repuestos' : df_cotizaciones_det[df_cotizaciones_det['Tipo Producto'] == 'REPUESTO'][['Item','Cantidad','Precio Venta']]\
                                .rename(columns={'Item': 'item', 'Cantidad': 'cantidad', 'Precio Venta': 'precio'})\
                                .assign(precio = lambda x: x['precio'].apply(lambda y: '${:,.0f}'.format(y)).replace(',','.'))\
                                .to_dict(orient='records'),
                'mano_obra' : df_cotizaciones_det[df_cotizaciones_det['Tipo Producto'] == 'MANO DE OBRA'][['Item','Precio Venta']]\
                                .rename(columns={'Item': 'detalle', 'Precio Venta': 'precio'})\
                                .assign(precio = lambda x: x['precio'].apply(lambda y: '${:,.0f}'.format(y)).replace(',','.'))\
                                .to_dict(orient='records'),
                'serv_adic' : df_cotizaciones_det[df_cotizaciones_det['Tipo Producto'] == 'SERVICIOS EXTRAS'][['Item','Precio Venta']]\
                                .rename(columns={'Item': 'detalle', 'Precio Venta': 'precio'})\
                                .assign(precio = lambda x: x['precio'].apply(lambda y: '${:,.0f}'.format(y)).replace(',','.'))\
                                .to_dict(orient='records'),

                'abonado': '${:,.0f}'.format(0),
                'precio_venta': '${:,.0f}'.format(\
                                    df_cotizaciones.iloc[selected_row]['Precio Venta'].sum()).replace(',','.'),
                'precio_iva': "${:,.0f}".format(\
                                    round(df_cotizaciones.iloc[selected_row]['Precio Venta'].sum() * 1.19 - df_cotizaciones.iloc[selected_row]['Precio Venta'].sum(),0))\
                                    .replace(',','.'),
                'precio_total': "${:,.0f}".format(\
                                    df_cotizaciones.iloc[selected_row]['Precio Venta'].sum() + round(df_cotizaciones.iloc[selected_row]['Precio Venta'].sum() * 1.19 - df_cotizaciones.iloc[selected_row]['Precio Venta'].sum(),0))\
                                    .replace(',','.'),
                'precio_pagar': "${:,.0f}".format(\
                                    df_cotizaciones.iloc[selected_row]['Precio Venta'].sum() + round(df_cotizaciones.iloc[selected_row]['Precio Venta'].sum() * 1.19 - df_cotizaciones.iloc[selected_row]['Precio Venta'].sum(),0))\
                                    .replace(',','.'),
                'comentarios_adic' : ''
            }      


            col5_a.download_button(label="Descargar PDF 📥", 
                    data=ct.generador_pdf(template="template_cotizacion_ot.html", datos=datos), 
                    file_name="cotizacion_{}.pdf".format(str(selected_id_cotiz)), 
                    mime="application/pdf", 
                    disabled=False,
                    type="primary")
            if add_items:
                st.session_state['selected_id_cotiz'] = selected_id_cotiz
                ct.switch_page("cotiz_items.py")
            if modificar_cotiz:
                st.session_state['selected_id_cotiz'] = selected_id_cotiz
                ct.switch_page("cotiz_modificar.py")

        else:
            st.write("Seleccione una cotizacion para ver los detalles")

            datos = {}




        


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()