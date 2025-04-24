import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
#from control_servicena import utils as cs
import os


def filtros_detalles(df, rut=None, cod_nubox=None, nombre=None, fecha=None, patente=None, estado=None, rut_name=None) -> pd.DataFrame:
    if rut_name != None:
        #df = df[df['RUT Cliente']==rut]
        df = df[df['rut_name']==rut_name]
    if patente != None:
        df = df[df['Patente']==patente]
    if nombre != None:
        df = df[df['Nombre Cliente']==nombre]
    if estado != None:
        if estado=="Finalizadas":
            df = df[df['Estado']=="Finalizada"]
        else:
            df = df[df['Estado']!="Finalizada"]
    if fecha != None:
        if len(fecha) == 2:
            df = df[(pd.to_datetime(df['Fecha'])>=pd.to_datetime(fecha[0])) & (pd.to_datetime(df['Fecha'])<=pd.to_datetime(fecha[1]))]
        elif len(fecha) == 1:
            df = df[(pd.to_datetime(df['Fecha'])==pd.to_datetime(fecha[0]))]
        else:
            df = df
    return df

def sidebar():
    st.sidebar.title("Menú")
    if st.sidebar.button("Inicio"):
        st.switch_page("pages\\home.py")
    if st.sidebar.button("Clientes"):
        st.switch_page("pages\\clientes.py")
    if st.sidebar.button("Cotizaciones"):
        st.switch_page("pages\\cotiz.py")
    if st.sidebar.button("Órdenes de Trabajo"):
        st.switch_page("pages\\ots.py")
    if st.sidebar.button("Negocio"):
        st.switch_page("pages\\negocio.py")

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Inicio - Taller', page_icon="src\\img\\logo-servicena.png")
    #cs.increase_page()
    st.markdown("""
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            #MainMenu {visibility: hidden;}
            .stAppDeployButton {display:none;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
        """, unsafe_allow_html=True)
    st.markdown("""
        <style>
                .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
    st.markdown("<h1>"+"Órdenes de Trabajo"+"</h1>", unsafe_allow_html=True)
    sidebar()



    df_ots = pd.DataFrame({
        "Id Orden": [11111, 22222, 33333, 44444, 55555, 66666, 77777],
        "RUT Cliente": ["19.334.061-4","19.334.061-4","19.334.061-4","7.930.134-5","18.887.218-K","6.622.912-0","15.898.932-9"],
        "Nombre Cliente": ["Eladio","Eladio","Eladio","Daniel","Felipe","José","María"],
        "Patente": ["ABCD12","ABCD12","ABCD12","XYZW99","FGHJ55","PQRS88","LMNO44"],
        "Marca": ["Hyundai","Hyundai","Hyundai","Toyota","BMW","Ford","Suzuki"],
        "Modelo": ["Modelo1","Modelo1","Modelo1","Modelo2","Modelo3","Modelo4","Modelo5",],
        #"Año"
        #VIN
        #Descripcion
        #"Tipo Trabajo"
        "Estado":["Finalizada", "Desarme", "Armado", "Para entrega", "Proc. de repuesto","En preparación","Facturada"],
        "Fecha Ingreso":["03-MAR-2025", "05-ABR-2025", "05-ABR-2025", "20-MAR-2025", "28-MAR-2025","02-ABR-2025","23-ABR-2025"],
        "Fecha Entrega":["20-MAR-2025","-","-","-","-","-","22-ABR-2025"]
    },index=None)

    df_detalle = df_ots    

    a,b = st.columns((3.5,2))

    with a.container(height=500):
        df_ots['rut_name'] = df_ots['RUT Cliente'] +' | '+df_ots['Nombre Cliente']
        col1, col2 , col3 , col4= st.columns((1,0.5,0.5,1))
        #rut_filter = col1.selectbox("Buscar RUT", df_ots['RUT Cliente'].unique() , index=None, placeholder='RUT')
        rut_filter = col1.selectbox("Buscar Cliente", df_ots['rut_name'].sort_values().unique() , index=None, placeholder='Cliente')
        if rut_filter:
            #df_ots = filtros_detalles(df_ots, rut=rut_filter)
            df_ots = filtros_detalles(df_ots, rut_name=rut_filter)

        #nombre_filter = col2.selectbox("Buscar Nombre", df_ots['Nombre Cliente'].unique() , index=None, placeholder='Nombre')
        #if nombre_filter:
            #df_ots = filtros_detalles(df_ots, nombre=nombre_filter)
        
        patente_filter = col2.selectbox("Buscar Patente", df_ots['Patente'].unique() , index=None, placeholder='Patente')
        if patente_filter:
            df_ots = filtros_detalles(df_ots, patente=patente_filter)

        estado_filter = col3.selectbox("Buscar Estado", ("Abiertas","Finalizadas") , index=None, placeholder='Estado')
        if estado_filter:
            df_ots = filtros_detalles(df_ots, estado=estado_filter)

        df_ots=df_ots[['Id Orden', 'RUT Cliente','Nombre Cliente', 'Patente', "Marca", "Estado"]]
        data = st.dataframe(df_ots,
                on_select='rerun',
                selection_mode='single-row',
                hide_index=True)
        
    with b.container(height=500):
        st.subheader("Detalle OT")
        if len(data.selection['rows']):
            selected_row = data.selection['rows'][0]
            st.session_state['selected_id_ot'] = df_detalle.iloc[selected_row]['Id Orden']
            detalle = pd.DataFrame({
                "Item":["ID","RUT","Cliente","Patente","Marca","Modelo","Estado","Fecha Ingreso","Fecha Entrega","Repuestos"],
                "Detalle":[df_detalle.iloc[selected_row]['Id Orden'],
                           df_detalle.iloc[selected_row]['RUT Cliente'],
                           df_detalle.iloc[selected_row]['Nombre Cliente'],
                           df_detalle.iloc[selected_row]['Patente'],
                           df_detalle.iloc[selected_row]['Marca'],
                           df_detalle.iloc[selected_row]['Modelo'],
                           df_detalle.iloc[selected_row]['Estado'],
                           df_detalle.iloc[selected_row]['Fecha Ingreso'],
                           df_detalle.iloc[selected_row]['Fecha Entrega'],
                           ("4 Pastillas, 2 Amortiguadores")]
                })
            data = st.dataframe(detalle, hide_index=True)
            #st.image(image=r'C:\slak.jpg', use_container_width =True)

        else:
            selected_row = None
            st.session_state['selected_id_ot'] = None
            detalle = pd.DataFrame({
                "Item":["ID","RUT","Cliente","Patente","Marca","Modelo","Estado","Fecha Ingreso","Fecha Entrega","Repuestos"],
                "Detalle":["","","","","","","","","",""]
                })
            data = st.dataframe(detalle, hide_index=True)
    st.write(st.session_state)

    #left_co, cent_co,last_co = st.columns([0.5,1,0.5])
    cent_co = st.image("src\\img\\taller.png",use_container_width=True)
    #cent_co


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()