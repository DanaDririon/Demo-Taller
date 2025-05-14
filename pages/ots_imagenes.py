import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from time import sleep
from control_taller import utils as ct
import os
from pathlib import Path
import uuid
from PIL import Image

def imagenes(id_ots):
    df_img = ct.select_data(tabla='img', columns='img_dir', where="deleted = 0 and img_ots_id = {}".format(id_ots))
    #split img_dir by \ and take the last element
    df_img['img_dir'] = df_img['img_dir'].str.split('\\').str[-1]
    df_img['img_dir'] = df_img['img_dir'].astype(str)
    #apply img_dir as path
    df_img['img_dir'] = df_img['img_dir'].apply(lambda x: str(Path("src") / "img" / "ot" / "OT-{}".format(id_ots) / x))
    return df_img

def main():

    # Este valor viene de la orden de trabajo. Si es que se recarga la página, no tira error 
    if 'selected_id_ot' not in st.session_state:
        st.session_state['selected_id_ot'] = 0
    
    #configuracion de pagina
    st.set_page_config(layout="wide", page_title='Imágenes OT', page_icon="src\\img\\taller_img\\icon_taller.jpg")
    ct.increase_page()
    ct.hide_deploy_button()
    st.markdown("<h1>"+"Imágenes OT #"+str(st.session_state['selected_id_ot'])+"</h1>", unsafe_allow_html=True)
    ct.sidebar()

    if 'selected_id_ot' not in st.session_state:
        st.session_state['selected_id_ot'] = 0

    id_ot = st.session_state['selected_id_ot']

    if 'upload_button' not in st.session_state:
        st.session_state['upload_button'] = str(uuid.uuid4())
    if 'img_array' not in st.session_state:
        st.session_state['img_array'] = []

    col1, col2, col3, col4, col99 = st.columns((0.5,1,0.2,2,0.1))

    if col1.button(label="Volver",icon=":material/arrow_back:"):
        ct.switch_page("ots.py")

    st.dataframe(pd.DataFrame({"Patente":["AB1234"]}),use_container_width=True,hide_index=True)

    
    # insert_img = col2.button(label="Agregar Imágenes",key="a2", type="primary",icon=":material/add:")
    st.subheader("Imágenes cargadas")

    with st.container(height=300):
        list_img = imagenes(id_ot)
        total_cargadas = len(list_img)
        cola, colb = st.columns((1,1))
        if len(list_img) > 0:
            for i in range(len(list_img)):
                if i % 2 == 0:
                    cola.image(list_img['img_dir'][i], width=720)
                else:
                    colb.image(list_img['img_dir'][i], width=720)
        else:    
            st.write("No hay imágenes disponibles")
            # insert_img = col1.button(label="Agregar Imágenes",key="a2", type="primary",icon=":material/add:")

    st.subheader("Subir Imagen")
    with st.container(height=600):
        colc, cold = st.columns((1,1))
        imgs = colc.file_uploader("Upload a file", type=["png", "jpg", "jpeg"], accept_multiple_files=True, label_visibility="collapsed", key=st.session_state['upload_button'])
        if imgs is not None:
            if len(imgs) > 10 - total_cargadas:
                colc.warning("Total de imágenes superado.")
                colc.button("Guardar Imágenes",disabled=True,icon=":material/upload:")
            
            else:
                for j in range(len(imgs)):
                    cold.write(imgs[j].name)
                    cold.image(imgs[j],width=720)
                    cold.write(imgs[j])
                    cold.markdown("---")

                if colc.button("Guardar Imágenes",type="primary",icon=":material/upload:"):
                    l = total_cargadas+1
                    for k in range(len(imgs)):

                        path_save = str(Path("src") / "img" / "ot" / "OT-{}".format(id_ot) / "OT-{}_{}.jpg".format(id_ot,str(l)) )
                        path_save = path_save.replace("\\","\\\\")
                        image = Image.open(imgs[k],)
                        image.save(path_save)
                        ct.insert_data('img',
                                       campos_insertar=['img_ots_id','img_dir','created_by','mod_by'],
                                       valores_insertar=[id_ot,path_save,'dana','dana'])
                    st.success("Imánges cargadas exitosamente.")                    
                    del st.session_state['upload_button']
                    sleep(1)
                    st.rerun()


if __name__ == "__main__":
    
#    import importlib
#    importlib.reload(cs)

#    cs.control_login(page,allow=True)
    main()