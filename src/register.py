import streamlit as st


st.set_page_config(page_title="Login", page_icon=None)  # Customize title and icon

st.write('Use your Hugging Face Credentials to Register')
username = st.text_input("Email:")
password = st.text_input("Password:", type="password")  # Hide password input

login_button = st.button("Register")
st.write("Don't have an account yet? Click here: ", "https://huggingface.co/join")
