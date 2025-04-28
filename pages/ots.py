import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
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

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Ordenes de Trabajo', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Órdenes de Trabajo"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

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

    #a,b = st.columns((3.5,2))

    with st.container(height=320):
        df_ots['rut_name'] = df_ots['RUT Cliente'] +' | '+df_ots['Nombre Cliente']
        col1, col2 , col3 , col4= st.columns((1,0.5,0.5,1))
        #rut_filter = col1.selectbox("Buscar RUT", df_ots['RUT Cliente'].unique() , index=None, placeholder='RUT')
        rut_filter = col1.selectbox("Buscar Cliente", df_ots['rut_name'].sort_values().unique() , index=None, placeholder='Cliente',label_visibility="collapsed")
        if rut_filter:
            #df_ots = filtros_detalles(df_ots, rut=rut_filter)
            df_ots = filtros_detalles(df_ots, rut_name=rut_filter)

        #nombre_filter = col2.selectbox("Buscar Nombre", df_ots['Nombre Cliente'].unique() , index=None, placeholder='Nombre')
        #if nombre_filter:
            #df_ots = filtros_detalles(df_ots, nombre=nombre_filter)
        
        patente_filter = col2.selectbox("Buscar Patente", df_ots['Patente'].unique() , index=None, placeholder='Patente',label_visibility="collapsed")
        if patente_filter:
            df_ots = filtros_detalles(df_ots, patente=patente_filter)

        estado_filter = col3.selectbox("Buscar Estado", ("Abiertas","Finalizadas") , index=None, placeholder='Estado',label_visibility="collapsed")
        if estado_filter:
            df_ots = filtros_detalles(df_ots, estado=estado_filter)

        df_ots=df_ots[['Id Orden', 'RUT Cliente','Nombre Cliente', 'Patente', "Marca", "Estado"]]
        data = st.dataframe(df_ots,
                on_select='rerun',
                selection_mode='single-row',
                hide_index=True,
                height=220)
        
        if len(data.selection['rows']):
            selected_row = data.selection['rows'][0]
        else:
             selected_row = None
             st.session_state['selected_id_ot'] = None
        
    # with b.container(height=500,):
    #     st.subheader("Detalle OT")
    #     if len(data.selection['rows']):
    #         selected_row = data.selection['rows'][0]
    #         st.session_state['selected_id_ot'] = df_detalle.iloc[selected_row]['Id Orden']
    #         detalle = pd.DataFrame({
    #             "Item":["ID","RUT","Cliente","Patente","Marca","Modelo","Estado","Fecha Ingreso","Fecha Entrega","Repuestos"],
    #             "Detalle":[df_detalle.iloc[selected_row]['Id Orden'],
    #                        df_detalle.iloc[selected_row]['RUT Cliente'],
    #                        df_detalle.iloc[selected_row]['Nombre Cliente'],
    #                        df_detalle.iloc[selected_row]['Patente'],
    #                        df_detalle.iloc[selected_row]['Marca'],
    #                        df_detalle.iloc[selected_row]['Modelo'],
    #                        df_detalle.iloc[selected_row]['Estado'],
    #                        df_detalle.iloc[selected_row]['Fecha Ingreso'],
    #                        df_detalle.iloc[selected_row]['Fecha Entrega'],
    #                        ("4 Pastillas, 2 Amortiguadores")]
    #             })
    #         detalle = df_detalle.iloc[[selected_row]]
    #         data = st.dataframe(detalle, hide_index=True)
    #         #st.image(image=r'C:\slak.jpg', use_container_width =True)

    #     else:
    #         selected_row = None
    #         st.session_state['selected_id_ot'] = None
    #         detalle = pd.DataFrame({
    #             "Item":["ID","RUT","Cliente","Patente","Marca","Modelo","Estado","Fecha Ingreso","Fecha Entrega","Repuestos"],
    #             "Detalle":["","","","","","","","","",""]
    #             })
    #         data = st.dataframe(detalle, hide_index=True)
    
    df_ejemplo = pd.DataFrame({
        "Id": ["AAAAA", "BBBBB", "CCCCC", "DDDDD", "EEEEE", "FFFFF", "GGGGG"],
        "Item": ["Pastillas","Amortiguadores","Uno","Fish","Cincuenta","Error","Botella"],
        "Cantidad": [74,82,1,5,50,11,2],
        "Precio Total": ["$1.555","222.444","$1","$666.666","$50","$321.123","$500"]
    })
    
    with st.container(height=400):
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Info General", "Repuestos", "Servicios Extras", "Imágenes", "Cotizaciones", "Cobranza", "Registro Estados"])
    with tab1:
        if selected_row:
            detalle = df_detalle.iloc[[selected_row]]
            data = st.dataframe(detalle, hide_index=True)
    with tab2:
        if st.button(label="Agregar"):
            st.switch_page("pages\\repuestos.py")
        data = st.dataframe(df_ejemplo, hide_index=True, height=200)
    with tab3:
        if st.button(label="Agregar",key="a1"):
            st.markdown("pog")
        df_ejemplo
    with tab4:
        st.columns((1,1))
        st.image("src\\img\\auto (1).jpg")
        st.image("src\\img\\auto (2).jpg")
        st.image("src\\img\\auto (3).jpg")
        st.image("src\\img\\auto (4).jpg")
        st.image("src\\img\\auto (5).jpg")
        st.image("src\\img\\auto (6).jpg")
    with tab5:
        if st.button(label="Agregar",key="a2"):
            st.markdown("pog")
        df_ejemplo
    with tab6:
        if st.button(label="Agregar",key="a3"):
            st.markdown("pog")
        df_ejemplo
    with tab7:
        if st.button(label="Agregar",key="a4"):
            st.markdown("pog")
        df_ejemplo      
    #st.write(st.session_state)

    st.image("src\\img\\taller.png",use_container_width=True)
    #cent_co


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()