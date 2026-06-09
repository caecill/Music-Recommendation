import streamlit as st

st.title("Register")

username = st.text_input("Username Baru")
password = st.text_input("Password Baru", type="password")

if st.button("Daftar"):
    st.success("Akun berhasil dibuat")
