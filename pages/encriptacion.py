import streamlit as st
import bcrypt

# Simula una "base de datos"
users_db = {}

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

st.title("Login seguro con hash")

menu = st.sidebar.selectbox("Selecciona", ["Registrar", "Iniciar Sesión"])

if menu == "Registrar":
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    st.write(bcrypt.gensalt())
    st.write(username, password)
    if st.button("Registrar"):
        hashed = hash_password(password)
        st.write("Contraseña:", hashed)
        st.session_state['hashed'] = hashed
        st.success("Usuario registrado correctamente")

elif menu == "Iniciar Sesión":
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar"):
        hashed = users_db.get(username)
        st.write("Contraseña:", hashed)
        if check_password(password, st.session_state['hashed']):
            st.write("Contraseña:", hashed)
            st.write("Contraseña:", password)
            st.success("Acceso concedido")
        else:
            st.error("Usuario o contraseña incorrecta")