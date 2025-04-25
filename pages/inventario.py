import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
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
    st.set_page_config(layout="wide", page_title='Clientes', page_icon="src\\img\\logo-servicena.png")
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
    st.markdown("<h1>"+"Inventario"+"</h1>", unsafe_allow_html=True)
    sidebar()

    df_ejemplo = pd.DataFrame({
        "Id": ["AAAAA", "BBBBB", "CCCCC", "DDDDD", "EEEEE", "FFFFF", "GGGGG"],
        "Item": ["Pastillas","Amortiguadores","Uno","Fish","Cincuenta","Error","Botella"],
        "Cantidad": [74,82,1,5,50,11,2],
        "Precio Total": ["$1.555","222.444","$1","$666.666","$50","$321.123","$500"]
    })

    st.button(label="Agregar Item", key="new_item")

    with st.container(height=500):
        st.dataframe(df_ejemplo, hide_index=True, height=200)

    st.image("src\\img\\taller.png",use_container_width=True)


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()

