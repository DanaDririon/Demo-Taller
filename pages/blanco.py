import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os
import base64
from PIL import Image
#resize png file

def resize_img(img_file):
    img = Image.open(img_file,)
    width, height = img.size
    if width > height:
        img = img.resize((720, int(height * (720 / width))))
    elif height > width:
        img = img.resize((int(width * (720 / height)), 720))
        img = img.transpose(Image.ROTATE_90) 
    else:
        img = img.resize((720, 720))
    return img

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def main():
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Clientes', page_icon="src\\img\\logo-servicena.png")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Clientes"+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    img = st.file_uploader("Upload a file", type=["png", "jpg", "jpeg"])
    
    if img is not None:
        img_path_save = 'src\\img\\'+img.name
        col1, col2 = st.columns((1, 1))
        new_img = resize_img(img)
        if col2.button("Rotar ->"):
            if 'angulo' not in st.session_state:
                st.session_state['angulo'] = 0
            if 'img' not in st.session_state:
                st.session_state['img'] = new_img

            st.session_state['angulo'] += 90
            new_img = new_img.rotate(st.session_state['angulo'])
            if st.session_state['angulo'] != 0:
                st.session_state['img'] = st.session_state['img'].rotate(st.session_state['angulo'])
            else:
                st.session_state['img'] = new_img

        
        if 'angulo' not in st.session_state:
            #st.write("Rotación: ", st.session_state['angulo'])
            pass
        else:
            st.write("Rotación: ", st.session_state['angulo'])
        if 'img' not in st.session_state:
            st.session_state['img'] = new_img

        col1.image(st.session_state['img'])
        if col2.button("Guardar"):
            st.session_state['img'].save(img_path_save)
            st.success("Imagen guardada")
            #st.switch_page("pages\\ots.py")

    #st.image()


if __name__ == "__main__":
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)

    main()