import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os
#@st.cache_resource
#@st.cache_data

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

def vehiculos():
    df_vehiculos_0 = ct.select_data(tabla="vehiculos", 
                                 columns='vehiculo_patente, \
                                    vehiculo_marca, \
                                    vehiculo_modelo, \
                                    vehiculo_year, \
                                    vehiculo_vin',
                                    where="deleted = 0",)
    df_vehiculos_1 = df_vehiculos_0[df_vehiculos_0['vehiculo_patente']=="SIN PATENTE"]
    df_vehiculos_2 = df_vehiculos_0[df_vehiculos_0['vehiculo_patente']!="SIN PATENTE"]
    df_vehiculos_2 = df_vehiculos_2.sort_values(by=['vehiculo_patente'], ascending=True)
    df_vehiculos = pd.concat([df_vehiculos_1, df_vehiculos_2], ignore_index=True).reset_index()
    return df_vehiculos

def clear_text():
    st.session_state["aa"] = ""

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Nueva Cotización', page_icon="src\\img\\taller_img\\icon_taller.jpg")
    ct.increase_page()
    st.markdown("<h1>"+"Nueva Cotización"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    if 'valid_patente' not in st.session_state.keys():
        st.session_state['valid_patente'] = False
        st.session_state['patente_nueva'] = ""


    height_container = 670
    height_subcontainer = height_container - 100
    col1_button, col2_button, col3_button, col4_button, col5_button, col6_button, col7_button = st.columns(7)

    col1, col2, col3 = st.columns((2.5,1.2,0.3))
    #df_clientes = ct.select_data(tabla="clientes", columns='cliente_rut, cliente_nombre, cliente_correo, cliente_telefono, cliente_direccion', where="deleted = 0")
    #df_ids_cotiz = ct.select_data(tabla='cotiz_cab', columns='cotiz_id')
    df_clientes = clientes()

    if col1_button.button(label="Volver",icon=":material/arrow_back:"):
        ct.switch_page("cotiz.py")

    with st.container(height=height_container):
        col1, col2, col3 = st.columns((2,2,2))
        col1.subheader("Datos Cliente")
        with col1.container(height=height_subcontainer):
            col_1a, col_1b = st.columns((3.5, 1.08))
            select_cliente = col_1a.selectbox("Cliente", df_clientes['cliente_rut_nombre'], placeholder="Seleccionar Cliente", index=None, label_visibility="collapsed", key="select_cliente")
            add_client = col_1b.button("Agregar", key="add_cliente", icon=":material/group_add:")
            if select_cliente is not None:
                cliente_selected = df_clientes[df_clientes['cliente_rut_nombre'] == select_cliente].reset_index()
                rut_cliente_selected = st.text_input("RUT Cliente", cliente_selected['cliente_rut'][0],disabled=True)
                nombre_cliente_selected = st.text_input("Nombre Cliente", cliente_selected['cliente_nombre'][0],disabled=True)
                correo_cliente_selected = st.text_input("Correo Cliente", cliente_selected['cliente_correo'][0],disabled=True)
                telefono_cliente_selected = st.text_input("Teléfono Cliente", cliente_selected['cliente_telefono'][0],disabled=True)
                direccion_cliente_selected = st.text_input("Dirección Cliente", cliente_selected['cliente_direccion'][0],disabled=True)
                same_info_selected = st.checkbox("Usar datos de cliente para facturación", value=False, key="same_info")
            else:
                rut_cliente_selected = st.text_input("RUT Cliente", "Cliente no seleccionado",disabled=True)
                nombre_cliente_selected = st.text_input("Nombre Cliente", "Cliente no seleccionado",disabled=True)
                correo_cliente_selected = st.text_input("Correo Cliente", "Cliente no seleccionado",disabled=True)
                telefono_cliente_selected = st.text_input("Teléfono Cliente", "Cliente no seleccionado",disabled=True)
                direccion_cliente_selected = st.text_input("Dirección Cliente", "Cliente no seleccionado",disabled=True)
                same_info_selected = False
            
            
            rut = None
            dig_ver = None

        col2.subheader("Datos Facturación")
        with col2.container(height=height_subcontainer):
            if same_info_selected:
                fact_rut = st.text_input("RUT Facturación", cliente_selected['cliente_rut'][0],disabled=True)
                fact_nomb = st.text_input("Nombre Facturación", cliente_selected['cliente_nombre'][0],disabled=True)
                fact_tel = st.text_input("Teléfono Facturación", cliente_selected['cliente_telefono'][0],disabled=True)
                fact_correo = st.text_input("Correo Facturación", cliente_selected['cliente_correo'][0],disabled=True)
                fact_direc = st.text_input("Dirección Facturación", cliente_selected['cliente_direccion'][0],disabled=True)
            else:
                rut_1, rut_2 = st.columns((3.5, 1.08))
                x = rut_1.text_input("RUT Facturación (*)", max_chars=8, placeholder="Ingresar RUT sin puntos ni dígito verificador")
                check_rut = ct.check_int(x)
                fact_dig_ver = None
                rut_clean = ""
                if check_rut:
                    fact_rut = int(x)
                    fact_dig_ver = ct.digito_verificador(x)
                    fact_rut = str(fact_rut)+'-'+str(fact_dig_ver)
                rut_2.text_input(label="Digito Verificador", disabled=True, value=fact_dig_ver)
                fact_nomb = st.text_input("Nombre Facturación (*)", placeholder="Ingresar nombre facturación")
                fact_tel = st.text_input("Teléfono Facturación (*)", placeholder="Ingresar teléfono facturación")
                fact_correo = st.text_input("Correo Facturación", placeholder="Ingresar correo facturación")
                fact_direc = st.text_input("Dirección Facturación", placeholder="Ingresar dirección facturación")
                
        col3.subheader("Datos Vehículo")
        with col3.container(height=height_subcontainer):
            pat_1, check_2 = st.columns((3.5, 1.08))
            df_vehiculos = vehiculos()
            patentes = df_vehiculos['vehiculo_patente']
            data_ingreso_manual = "Ingresar datos manualmente"
            patente_selected = pat_1.selectbox("Patente", options=[data_ingreso_manual]+list(patentes), index=0, placeholder="Seleccionar Patente", label_visibility="collapsed", key="select_patente", on_change=clear_text)
            if patente_selected == "Ingresar datos manualmente":
                patente = st.text_input("Patente (*)", placeholder="AAAA11", max_chars=6, key="aa")
                if len(patente) == 6 or len(patente) == 5:
                    cant_patentes = len(df_vehiculos[df_vehiculos['vehiculo_patente'] == patente.upper()].reset_index())
                    if cant_patentes == 0:
                        check_patente = False
                    else:
                        st.warning("Patente ya existe en la base de datos.")
                        check_patente = True
                else:
                    check_patente = True

                marca = st.text_input("Marca (*)",placeholder="Ingresar Marca", disabled=check_patente)
                modelo = st.text_input("Modelo (*)",placeholder="Ingresar Modelo", disabled=check_patente)
                x = st.text_input("Año (*)",placeholder="Ingresar Año",max_chars=4, disabled=check_patente)
                check_año = ct.check_int(x)
                if check_año:
                    año = int(x)
                vin = st.text_input("VIN",placeholder="VIN vehículo", disabled=check_patente)
            else:
                patente = patente_selected
                vehiculo_selected = df_vehiculos[df_vehiculos['vehiculo_patente'] == patente].reset_index()
                marca = st.text_input("Marca", vehiculo_selected['vehiculo_marca'][0], disabled=True)
                modelo = st.text_input("Modelo", vehiculo_selected['vehiculo_modelo'][0], disabled=True)
                año = st.text_input("Año", vehiculo_selected['vehiculo_year'][0], disabled=True)
                vin = st.text_input("VIN", vehiculo_selected['vehiculo_vin'][0], disabled=True)


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

    if select_cliente is not None \
            and fact_rut != "" \
            and fact_rut != "" and fact_nomb != "" and (fact_correo != "" or fact_tel != "") \
            and (patente=="SIN PATENTE" or (patente != "" and marca != "" and modelo != "" and año != "")):
        
        ingresar_cotiz = col2_button.button(label="Ingresar Cotizacion", key="save", type="primary")

    if add_client:
        ct.switch_page("clientes_nuevo.py")

if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()