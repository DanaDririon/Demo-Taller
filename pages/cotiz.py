import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os
def cotizaciones():
    df_cotizaciones_cab = ct.select_data(tabla="cotiz_cab",
                                        columns='cotiz_id, cotiz_ots_id',
                                        where="deleted = 0")
    df_cotizaciones_cab['cotiz_ots_id'] = df_cotizaciones_cab['cotiz_ots_id'].astype(int)
    df_cotizaciones_det = ct.select_data(tabla="cotiz_det",
                                        columns='cotiz_cab_id, cotiz_tipo_prod, cotiz_costo, cotiz_precio_venta',
                                        where="deleted = 0")
    df_cotizaciones_det['cotiz_tipo_prod'] = df_cotizaciones_det['cotiz_tipo_prod'].astype(int)
    df_cotiz = pd.merge(df_cotizaciones_cab, df_cotizaciones_det, how='left', left_on='cotiz_id', right_on='cotiz_cab_id').drop(columns=['cotiz_cab_id'])
    df_cotiz['margen'] = df_cotiz['cotiz_precio_venta'] - df_cotiz['cotiz_costo']
    df_cotiz['porc_margen'] = round((df_cotiz['margen'] / df_cotiz['cotiz_precio_venta']) * 100,2)

    df_tipo_prod = ct.select_data(tabla="tipo_prod",
                                  columns='tipo_prod_id, tipo_prod_descripcion',
                                  where="deleted = 0")
    df_tipo_prod['tipo_prod_id'] = df_tipo_prod['tipo_prod_id'].astype(int)
    df_cotiz = pd.merge(df_cotiz, df_tipo_prod, how='left', left_on='cotiz_tipo_prod', right_on='tipo_prod_id')
    df_cotiz = df_cotiz.drop(columns=['cotiz_tipo_prod', 'tipo_prod_id'])
    return df_cotiz

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Cotizaciones', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Cotizaciones"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    col1, col2, col3 = st.columns((1,1,7))
    col1.button(label="Nueva Cotizacion ➕", type="primary")
    col2.button(label="Modificar Cotizacion", type="primary",disabled=True)
    col3.button(label="Generar OT", type="primary",disabled=True)

    df_cotizaciones = cotizaciones()
    df_cotizaciones
    df_cotiz_cab = df_cotizaciones.groupby(['cotiz_cab_id','cotiz_tipo_prod']).agg({'cotiz_costo':'sum',
                                                                'cotiz_precio_venta':'sum',}).reset_index()

    with st.container(height=400):
        pass
    
    with st.container(height=350):
        st.markdown("Detalles")


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()