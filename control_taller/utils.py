import pandas as pd
import mysql.connector
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype
)
import streamlit as st
from time import sleep
from sqlalchemy import create_engine
import pymysql
from streamlit_javascript import st_javascript
import numpy as np
import janitor
import re
from itertools import cycle
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
import zipfile
import os

pd.options.mode.chained_assignment = None

def create_image_zip(zip_filename, image_dir, folder_temp):
    """
    Creates a zip file containing all images in a directory.

    Args:
        zip_filename (str): The name of the zip file to create.
        image_dir (str): The path to the directory containing the images.
    """
    zipfile_path = os.path.join("temps",folder_temp,zip_filename)
    with zipfile.ZipFile(zipfile_path, 'w') as zipf:
        #st.write("Archivos en la carpeta: ", image_dir)
        for root, _, files in os.walk(image_dir):
            for file in files:
                #st.write(file)
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    # Add the file to the zip archive, maintaining directory structure
                    zipf.write(file_path, os.path.relpath(file_path, image_dir))
    return zipfile_path

def connection():
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "daniel125",
            database = "taller"
        )
        return mydb
    except:
        mydb = mysql.connector.connect(
            host = "100.72.37.8",
            user = "eladio",
            password = "taller123",
            database = "taller"
        )
        return mydb
    
def get_data(query: str) -> pd.DataFrame:
    mydb = connection()
    mycursor = mydb.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns=mycursor.column_names, index=None)
    return df

def select_data(tabla: str, columns=None, where=None, group=None, order=None, limit=None) -> pd.DataFrame:
    """
    Obtiene los datos de la base de datos y los retorna en un dataframe

    Argumentos:
        tabla (str): Nombre de la tabla
        columns (str): Columnas a seleccionar
        where (str): Condicion de la consulta
        group (str): Agrupar por
        order (str): Ordenar por
        limit (str): Limite de registros

    Retorna:
        pd.DataFrame: Dataframe con los datos de la consulta
    """
    mydb = connection()
    mycursor = mydb.cursor()
    query = "SELECT "
    if columns==None:
        query += "*"
    else:
        query += columns
    query += " FROM "+tabla
    if where!=None:
        query += " WHERE "+where        
    if group!=None:
        query += " GROUP BY "+group       
    if order!=None:
        query += " ORDER BY "+order
    if limit!=None:
        query += " LIMIT "+limit

    #st.write(query)
    
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns=mycursor.column_names, index=None)

    # Cambiar el tipo de dato de las columnas a su tipo original
    df_types = get_data("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'taller' AND TABLE_NAME = '{}'".format(tabla))
    df_types
    for i in range(len(df_types)):
        if df_types['COLUMN_NAME'][i] in df.columns:
            if df_types['DATA_TYPE'][i] == 'int' or df_types['DATA_TYPE'][i] == 'bigint' or df_types['DATA_TYPE'][i] == 'smallint' or df_types['DATA_TYPE'][i] == 'tinyint':
                df[df_types['COLUMN_NAME'][i]] = df[df_types['COLUMN_NAME'][i]].astype(int)
            elif df_types['DATA_TYPE'][i] == 'float':
                df[df_types['COLUMN_NAME'][i]] = df[df_types['COLUMN_NAME'][i]].astype(float)
            elif df_types['DATA_TYPE'][i] == 'datetime' or df_types['DATA_TYPE'][i] == 'timestamp':
                df[df_types['COLUMN_NAME'][i]] = pd.to_datetime(df[df_types['COLUMN_NAME'][i]])
            elif df_types['DATA_TYPE'][i] == 'varchar' or df_types['DATA_TYPE'][i] == 'text' or df_types['DATA_TYPE'][i] == 'char':
                df[df_types['COLUMN_NAME'][i]] = df[df_types['COLUMN_NAME'][i]].astype('object')
            else:
                pass
        else:
            pass

    return df

def delete_data(table: str, user: str, str_id: str, id):
    mydb = connection()
    mycursor = mydb.cursor()
    query = "UPDATE "+table+" SET mod_by = '{}', deleted=1 WHERE "+str_id+" = {}".format(user, id)
    print(query)
    mycursor.execute(query)
    mydb.commit()

def insert_data(table, campos_insertar: list, valores_insertar: list, check_duplicado=False, campo_contar=None, campos_check_duplicado: list = None, valores_check_duplicado: list = None):
    if check_duplicado:
        check_query_add = ""
        for i in range(len(campos_check_duplicado)):
            check_query_add += " AND {} = '{}'".format(campos_check_duplicado[i], valores_check_duplicado[i])
        print(check_query_add)
        if select_data(table, columns='count({}) as contar'.format(campo_contar), where='deleted = 0 {}'.format(check_query_add))['contar'][0] > 0:                
            return False
    else:
        pass

    mydb = connection()
    mycursor = mydb.cursor()
    query = "INSERT INTO "+table+" ("
    for i in range(len(campos_insertar)):
        if i == len(campos_insertar)-1:
            query += campos_insertar[i]+") VALUES ("
        else:
            query += ""+campos_insertar[i]+","
    
    for i in range(len(valores_insertar)):
        if i == len(valores_insertar)-1:
            query += "'"+str(valores_insertar[i])+"')"
        else:
            query += "'"+str(valores_insertar[i])+"',"

    print(query)
    mycursor.execute(query)
    mydb.commit()
    return True

def update_data(table: str, campos_modificar: list, valores_modificar: list, campos_id: list, valores_id: list):
    mydb = connection()
    mycursor = mydb.cursor()
    query = "UPDATE "+table+" SET "
    for i in range(len(campos_modificar)):
        if i == len(campos_modificar)-1:
            query += campos_modificar[i]+" = '"+str(valores_modificar[i])+"' WHERE "
        else:
            query += campos_modificar[i]+" = '"+str(valores_modificar[i])+"', "
    
    for i in range(len(campos_id)):
        if i == len(campos_id)-1:
            query += campos_id[i]+" = '"+str(valores_id[i])+"'"
        else:
            query += campos_id[i]+" = '"+str(valores_id[i])+"' AND "

    print(query)
    mycursor.execute(query)
    mydb.commit()
    return True

def login_check(user: str, password:str, metodo_login: int) -> bool:
    #df = get_data(querys.query_data_login)
    if metodo_login == 1:
        return True
    else:
        user_profile = select_data(tabla='usuarios')
        usuario_login = user_profile[user_profile['usuario_nombre']==user].reset_index(drop=True)
        if usuario_login['pass'][0] == password:
            st.session_state['login'] = True
            for i in range(len(usuario_login.columns.sort_values())):
                usuario_login.columns[i]
                st.session_state[usuario_login.columns[i]] = usuario_login[usuario_login.columns[i]][0]
            del st.session_state['pass']
            return True       
        else:
            return False

def control_login(page: str = None, allow: bool = False):
    #if 'login' in st.session_state or len(st.session_state) > 0 or st.session_state['login']==True:
    if allow==True:
        pass
    else:
        if len(st.session_state) > 0:
            if 'login' in st.session_state or st.session_state['login']==True:
                if allow==True:
                    pass
                else:
                    modulo_check = select_data(tabla='usuarios')
                    modulo_check = modulo_check[modulo_check['user']==st.session_state['user']]['rol_'+page].reset_index(drop=True)
                    modulo_check = modulo_check[0]
                    if st.session_state['rol_'+page]>0:
                        pass
                    else:
                        st.warning("Usted no tiene permisos para acceder a esta página.")
                        st.warning("será redirigido a la página de inicio.")
                        #Redirigir a la pagina de inicio con contador visual de 5 segundos
                        sleep(3)
                        switch_page("home.py")
            else:
                st.warning("Usted no se ha logueado, será redirigido a la página de inicio.")
                #Redirigir a la pagina de inicio con contador visual de 5 segundos
                sleep(3)
                switch_page("login.py")
        else:
            st.warning("Usted no se ha logueado, será redirigido a la página de inicio.")
            #Redirigir a la pagina de inicio con contador visual de 5 segundos
            sleep(3)
            switch_page("login.py")

def sidebar():
    st.sidebar.title("Menú")
    if st.sidebar.button("Órdenes de Trabajo"):
        switch_page("ots.py")
    if st.sidebar.button("Cotizaciones"):
        switch_page("cotiz.py")
    #if st.sidebar.button("Inicio"):
        #switch_page("home.py")
    if st.sidebar.button("Clientes"):
        switch_page("clientes.py")
    if st.sidebar.button("Pagos"):
        switch_page("pagos.py")
    if st.sidebar.button("Inventario"):
        switch_page("inventario.py")
    if st.sidebar.button("Dashboard"):
        switch_page("dashboard.py")
    if st.sidebar.button("Reportes"):
        switch_page("reportes.py")

    ms = st.session_state
    if "theme" not in ms: 
        ms.theme = {"current_theme": "dark",
                            "refreshed": True,

                            "dark":  {"theme.base": "light",
                                    "theme.backgroundColor": "#FFFFFF",
                                    "theme.primaryColor": "#FF4B4B",
                                    "theme.secondaryBackgroundColor": "#F0F2F6",
                                    "theme.textColor": "#31333F",
                                    "button_face": "🌞"},
                            
                            "light": {"theme.base": "dark",
                                    "theme.backgroundColor": "#0E1117",
                                    "theme.primaryColor": "#FF4B4B",
                                    "theme.secondaryBackgroundColor": "#262730",
                                    "theme.textColor": "#FAFAFA",
                                    "button_face": "🌜"},
                            }
    btn_face = ms.theme["dark"]["button_face"] if ms.theme["current_theme"] == "dark" else ms.theme["light"]["button_face"]
    st.sidebar.button(btn_face, on_click=ChangeTheme)

    if ms.theme["refreshed"] == False:
        ms.theme["refreshed"] = True
        st.rerun()

def ChangeTheme():
    ms = st.session_state
    previous_theme = ms.theme["current_theme"]
    tdict = ms.theme["dark"] if ms.theme["current_theme"] == "dark" else ms.theme["light"]
    for vkey, vval in tdict.items(): 
        if vkey.startswith("theme"): st._config.set_option(vkey, vval)

    ms.theme["refreshed"] = False
    if previous_theme == "dark": ms.theme["current_theme"] = "light"
    elif previous_theme == "light": ms.theme["current_theme"] = "dark"

def switch_page(page: str):
    """
    Cambia de página en Streamlit.

    Argumentos:
        page (str): Nombre de la página a la que se desea cambiar.
    """
    import os
    #page = 'reportes.py'
    path = Path("pages") / page
    # if have / replace for // or if have \ replace for \\
    #path = path.replace("\\", "\\\\")
    path_str = str(path)
    if path.exists():
        st.switch_page(path_str)
    else:
        st.warning("La página no existe.")

def increase_page():
    return     st.markdown("""
        <style>
                .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

def hide_deploy_button():
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

def digito_verificador(rut: int):
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    return (-s) % 11 if (-s) % 11 < 10 else 'K'

def validate_email_syntax(email):
    if email == "" or email == None:
        return False
    else:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if re.match(pattern, email) is not None:
            return True
        else:
            st.warning("Formato de correo inválido.")
            return False

def check_int(x):
    if x == "" or x == None:
        return False
    else:
        try:
            int(x)
            return True
        except:
            st.warning("No es un número entero.")
            return False
        
def generador_pdf(template: str, datos: dict) -> bytes:
    """
    Genera un PDF a partir de una plantilla HTML y datos proporcionados.

    Args:
        template (str): Nombre de la plantilla HTML.
        datos (dict): Datos para renderizar la plantilla.

    Returns:
        None
    """
    # Cargar plantilla
    env = Environment(loader=FileSystemLoader(['./templates']))
    template = env.get_template(template)
    # Renderizar HTML
    html_rendered = template.render(**datos)
    
    # Generar PDF
    pdf = HTML(string=html_rendered, base_url='.').write_pdf()
    return pdf
