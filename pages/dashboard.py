import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import altair as alt
from babel.numbers import format_currency 
from time import sleep
from control_taller import utils as ct
import os


def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Dashboard - Taller', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Dashboard"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()


    col1, col2, = st.columns((1,1))

    df_ventas = pd.DataFrame({
        "Meses": ["Enero", "Febrero", "Marzo", "Abril","Mayo","Junio", "Julio"],
        #"Ventas":["$9.685.415", "$8.754.361", "16.487.591", "13.548.794","$0","$0","$0"]
        "Ventas":[9685415, 8754361, 16487591, 13548794,0,0,0]
    })

    df_ventas["Ventas_str"] = df_ventas["Ventas"].apply(lambda x: format_currency(x, currency="CLP", locale="es_CL"))

    points = alt.Chart(df_ventas).mark_circle(size = 0)
    lines = alt.Chart(df_ventas, title = 'Ventas Mensuales'.upper()).mark_line().encode(
                 x = alt.X('Meses:O', axis = alt.Axis(title = 'Meses'.upper())).sort(["Enero", "Febrero", "Marzo", "Abril","Mayo","Junio", "Julio"]),
                 y = alt.Y('Ventas:Q', axis = alt.Axis(title = 'Ventas'.upper()))
            ).properties(width=600).interactive()

    text = alt.Chart(df_ventas).mark_text(dx=0,dy=00,color="black",fontWeight='bold',fontSize=18).encode(
        x = alt.X('Meses:O', axis = alt.Axis(title = 'Meses'.upper())).sort(["Enero", "Febrero", "Marzo", "Abril","Mayo","Junio", "Julio"]),
        y = alt.Y('Ventas:Q', axis = alt.Axis(title = 'Ventas'.upper())),
        text = 'Ventas_str'
        ).properties(width=600)
    
    text_background = text.mark_text(
    stroke='white',
    strokeWidth=5,
    #strokeJoin='miter',
    fontWeight='bold',
    fontSize=18,
    dx=0
)
    chart = lines + points + text_background +  text 

    col1.altair_chart(chart, use_container_width=False)

    bars = alt.Chart(df_ventas, title = 'Ventas Mensuales'.upper()).mark_bar().encode(
                x = alt.X('Meses:O', axis = alt.Axis(title = 'Meses'.upper())).sort(["Enero", "Febrero", "Marzo", "Abril","Mayo","Junio", "Julio"]),
                y = alt.Y('Ventas:Q', axis = alt.Axis(title = 'Ventas'.upper()))
                ).properties(width=600).interactive()

    test2 = bars+ text_background+text

    col2.altair_chart(test2, use_container_width=False)
    #col1=st.line_chart(df_ventas,x="Meses",y="Ventas",x_label="Meses",y_label="Ventas")
    #col1
    #col2=st.bar_chart(df_ventas,x="Meses",y="Ventas",x_label="Meses",y_label="Ventas")
    #col1
    #col2

    col3, col4 = st.columns((1,1))

    df_proovedores = pd.DataFrame({
        "Proovedor": ["Imperial", "3M", "Mobil", "Otros"],
        #"Compras": ["$6.789.012", "$4.456.789", "$1.862.486", "$765.432"]
        "Compras": [6789012, 4456789, 1862486, 765432]
    })

    bars2 = alt.Chart(df_proovedores, title = 'Compras por Proovedor'.upper()).mark_bar().encode(
        x = alt.X('Compras:Q', axis = alt.Axis(title = 'Compras'.upper())),
        y = alt.Y('Proovedor:N', axis = alt.Axis(title = 'Proovedores'.upper())).sort(['Compras'])
        ).properties(width=600,height=300).interactive()
    col3.altair_chart(bars2, use_container_width=False)

    df_ots =  pd.DataFrame({
        "Mes": ["Enero","Enero","Febrero","Febrero","Marzo","Marzo","Abril","Abril","Mayo","Mayo","Junio","Junio"],
        "Tipos de OTs": ["Mantención","Específica","Mantención","Específica","Mantención","Específica","Mantención","Específica","Mantención","Específica","Mantención","Específica"],
        "# Órdenes de Trabajo": [23,12,19,7,38,22,33,15,25,15,21,9]
        })

    bars3 = alt.Chart(df_ots, title='Órdenes por mes'.upper()).mark_bar().encode(
        x=alt.X("Mes:O", axis=alt.Axis(title = 'Meses'.upper())).sort(["Enero", "Febrero", "Marzo", "Abril","Mayo","Junio", "Julio"]),
        xOffset="Tipos de OTs:N",
        y=alt.Y("# Órdenes de Trabajo:Q", axis = alt.Axis(title = '# Órdenes de Trabajo'.upper())),
        color=alt.Color("Tipos de OTs:N")
    ).properties(width=600).interactive()

    col4.altair_chart(bars3, use_container_width=False)

    cent_co = st.image("src\\img\\taller.png",use_container_width=True)
    #cent_co


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    ct.control_login(page,allow=True)

    main()