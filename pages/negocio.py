import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import altair as alt
from babel.numbers import format_currency 
from time import sleep
#from control_servicena import utils as cs
import os

def ChangeTheme():
    ms = st.session_state
    previous_theme = ms.themes["current_theme"]
    tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
    for vkey, vval in tdict.items(): 
        if vkey.startswith("theme"): st._config.set_option(vkey, vval)

    ms.themes["refreshed"] = False
    if previous_theme == "dark": ms.themes["current_theme"] = "light"
    elif previous_theme == "light": ms.themes["current_theme"] = "dark"

def sidebar():
    st.sidebar.title("Menú")
    if st.sidebar.button("Órdenes de Trabajo"):
        st.switch_page("pages\\ots.py")
    if st.sidebar.button("Cotizaciones"):
        st.switch_page("pages\\cotiz.py")
    #if st.sidebar.button("Inicio"):
        #st.switch_page("pages\\home.py")
    if st.sidebar.button("Clientes"):
        st.switch_page("pages\\clientes.py")
    if st.sidebar.button("Cobranza"):
        st.switch_page("pages\\cobranza.py")
    if st.sidebar.button("Inventario"):
        st.switch_page("pages\\inventario.py")
    if st.sidebar.button("Negocio"):
        st.switch_page("pages\\negocio.py")

    ms = st.session_state
    if "themes" not in ms: 
        ms.themes = {"current_theme": "light",
                            "refreshed": True,
                            
                            "light": {"theme.base": "dark",
                                    "theme.backgroundColor": "#0E1117",
                                    "theme.primaryColor": "#FF4B4B",
                                    "theme.secondaryBackgroundColor": "#262730",
                                    "theme.textColor": "#FAFAFA",
                                    "button_face": "🌜"},

                            "dark":  {"theme.base": "light",
                                    "theme.backgroundColor": "#FFFFFF",
                                    "theme.primaryColor": "#FF4B4B",
                                    "theme.secondaryBackgroundColor": "#F0F2F6",
                                    "theme.textColor": "#31333F",
                                    "button_face": "🌞"},
                            }
    btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
    st.sidebar.button(btn_face, on_click=ChangeTheme)

    if ms.themes["refreshed"] == False:
        ms.themes["refreshed"] = True
        st.rerun()

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
    st.markdown("<h1>"+"Negocio"+"</h1>", unsafe_allow_html=True)
    sidebar()


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


#if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

main()