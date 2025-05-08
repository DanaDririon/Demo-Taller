import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os


def filtros_detalles(df, rut=None, cod_nubox=None, nombre=None, fecha=None) -> pd.DataFrame:
    if rut != None:
        df = df[df['cliente_rut']==rut]
    #if cod_nubox != None:
    #    df = df[df['Cod Nubox']==cod_nubox]
    if nombre != None:
        df = df[df['cliente_nombre']==nombre]
    if fecha != None:
        if len(fecha) == 2:
            df = df[(pd.to_datetime(df['Fecha'])>=pd.to_datetime(fecha[0])) & (pd.to_datetime(df['Fecha'])<=pd.to_datetime(fecha[1]))]
        elif len(fecha) == 1:
            df = df[(pd.to_datetime(df['Fecha'])==pd.to_datetime(fecha[0]))]
        else:
            df = df
    return df

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Clientes', page_icon="src\\img\\taller_img\\icon_taller.jpg")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Clientes"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    col01, col02, col3, col4, col5, col6, col7 = st.columns((1.2,1.5,1,1,1.5,2,2))

    if 'button_disabled' not in st.session_state:
        st.session_state.button_disabled = False
    
    if 'rut_selected' not in st.session_state:
        st.session_state.rut_selected = None

    if col01.button("Nuevo Cliente ➕", type="primary"):
        ct.switch_page("clientes_nuevo.py")

    with st.container(height=530):
        df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
    
        col1, col2, col3, col4 = st.columns((0.5,0.5,1,0.5))

        rut_filter = col1.selectbox("Buscar RUT", df_clientes['cliente_rut'].unique() , index=None, placeholder='RUT')
        if rut_filter:
            df_clientes = filtros_detalles(df_clientes, rut=rut_filter)

        nombre_filter = col2.selectbox("Buscar Nombre", df_clientes['cliente_nombre'].unique() , index=None, placeholder='Nombre')
        if nombre_filter:
            df_clientes = filtros_detalles(df_clientes, nombre=nombre_filter)

        data = st.dataframe(df_clientes, hide_index=True, height=405, 
                    column_order=((
                        "cliente_rut",
                        "cliente_nombre",
                        "cliente_correo",
                        "cliente_telefono",
                        "cliente_direccion")),
                    column_config={
                        'cliente_rut': st.column_config.Column("RUT"),#,width
                        'cliente_nombre':st.column_config.Column("Nombre"),
                        'cliente_correo':st.column_config.Column("Correo"),
                        'cliente_telefono':st.column_config.Column("Teléfono"),
                        'cliente_direccion':st.column_config.Column("Dirección")},
                    on_select='rerun',
                    selection_mode='single-row', use_container_width=True)

        if len(data.selection['rows']):
            selected_row = data.selection['rows'][0]
            st.session_state.rut_selected = df_clientes.at[selected_row,'cliente_rut']
            st.session_state.button_disabled = False
        else:
            selected_row = None
            st.session_state.rut_selected = None
            st.session_state.button_disabled = True

    if col02.button("Modificar Cliente 🖊️", type="primary", disabled=st.session_state.button_disabled):
        ct.switch_page("clientes_modificar.py")


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()