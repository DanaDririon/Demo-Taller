import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os

def clientes():
    df_clientes = ct.select_data(tabla="clientes", 
                                 columns='concat(cliente_rut," | ",cliente_nombre) as cliente_rut_nombre,\
                                    cliente_rut, \
                                    cliente_nombre, \
                                    cliente_correo, \
                                    cliente_telefono, \
                                    cliente_direccion', 
                                    where="deleted = 0",
                                    order="cast(left(cliente_rut,length(cliente_rut)-2) as double) ASC")
    return df_clientes

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Nueva Cotización', page_icon="src\\img\\taller_img\\icon_taller.jpg")
    ct.increase_page()
    st.markdown("<h1>"+"Nueva Cotización"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()
     
    col1, col2, col3, col99 = st.columns((2.5,1,2,0.3))
    #df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
    #df_ids_cotiz = ct.select_data(tabla='cotiz_cab', columns='cotiz_id')
    df_clientes = clientes()

    if col1.button(label="Volver",icon=":material/arrow_back:"):
        ct.switch_page("cotiz.py")

    with st.container(height=800):
        col1, col2, col3 = st.columns((2.5,2,2))
        col1.subheader("Datos Cliente")
        with col1.container(height=700):
            col_1a, col_1b = st.columns((4, 1))
            select_cliente = col_1a.selectbox("Cliente", df_clientes['cliente_rut_nombre'], placeholder="Seleccionar Cliente", index=None, label_visibility="collapsed", key="select_cliente")
            add_client = col_1b.button("Agregar Cliente", key="add_cliente")

            if select_cliente is not None:
                cliente_selected = df_clientes[df_clientes['cliente_rut_nombre'] == select_cliente].reset_index()
                rut_cliente_selected = st.text_input("RUT Cliente", cliente_selected['cliente_rut'][0],disabled=True)
                nombre_cliente_selected = st.text_input("Nombre Cliente", cliente_selected['cliente_nombre'][0],disabled=True)
                correo_cliente_selected = st.text_input("Correo Cliente", cliente_selected['cliente_correo'][0],disabled=True)
                telefono_cliente_selected = st.text_input("Teléfono Cliente", cliente_selected['cliente_telefono'][0],disabled=True)
                direccion_cliente_selected = st.text_input("Dirección Cliente", cliente_selected['cliente_direccion'][0],disabled=True)
            else:
                rut_cliente_selected = st.text_input("RUT Cliente", "",disabled=True)
                nombre_cliente_selected = st.text_input("Nombre Cliente", "",disabled=True)
                correo_cliente_selected = st.text_input("Correo Cliente", "",disabled=True)
                telefono_cliente_selected = st.text_input("Teléfono Cliente", "",disabled=True)
                direccion_cliente_selected = st.text_input("Dirección Cliente", "",disabled=True)
        
        
            rut_1, rut_3, rut_2 = st.columns((6, 1, 1.8))
            rut = None
            dig_ver = None
            x = rut_1.text_input("RUT Facturación", max_chars=8, placeholder="Ingresar RUT sin puntos ni dígito verificador")
            check_rut = ct.check_int(x)
            rut_clean = ""
            if check_rut:
                rut_clean = int(x)
                dig_ver = ct.digito_verificador(x)
                rut_clean = str(rut_clean)+'-'+str(dig_ver)
            rut_2.text_input(label="Digito Verificador", disabled=True, value=dig_ver)

            fact_nomb = st.text_input("Nombre Facturación", placeholder="Ingresar nombre facturación").upper()

        col2.subheader("Datos Vehículo")
        with col2.container(height=400):
            
            marca = st.text_input("Marca",placeholder="Marca vehículo").upper()
            modelo = st.text_input("Modelo",placeholder="Modelo vehículo").upper()
            año = st.text_input("Año",placeholder="XXXX",max_chars=4)
            check_año = ct.check_int(año)
            patente = st.text_input("Patente",placeholder="AAAA11").upper()

    # col3.markdown("<h4>"+"Preview"+"</h4>", unsafe_allow_html=True)
    # with col3.container(height=400):
    #     # tel_ini = ""
    #     # if check_telefono: tel_ini = "+56"
    #     resumen = pd.DataFrame({
    #         "Preview": ["RUT Cliente","RUT Facturación","Nombre Facturación","Marca","Modelo","Año","Patente"],
    #         " ": [rut_cliente_selected,rut_clean,fact_nomb,marca,modelo,año,patente],
    #     })

    #     st.dataframe(resumen,hide_index=True)
    #     if rut_cliente_selected and check_rut and check_año and fact_nomb and marca and modelo and patente:
    #         agregar = st.button(label='Agregar',type="primary")
    #         if agregar:
    #             #max_id = 1+int(ct.get_data('select MAX(cotiz_id) AS max_id FROM cotiz_cab')['max_id'])
                
    #             if ct.insert_data('cotiz_cab',
    #                             campos_insertar = ['cotiz_rut_cliente','cotiz_rut_facturacion','cotiz_nombre_facturacion',
    #                                                'cotiz_marca','cotiz_modelo','cotiz_year','cotiz_patente'
    #                                                'created_by','mod_by'],
    #                             valores_insertar = [rut_cliente_selected, rut_clean, fact_nomb,
    #                                                 marca,modelo,año,patente,
    #                                                  'dana', 'dana']):
    #                 st.success("Registro creado exitosamente.")
    #                 sleep(1.2)
    #                 ct.switch_page("cotiz.py")
    #             else:
    #                 st.error("Error de Query. Contactar desarrollador.")
    #     else:
    #         agregar = st.button(label='Agregar',type="primary", disabled=True)

    if add_client:
        ct.switch_page("clientes_nuevo.py")

if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()