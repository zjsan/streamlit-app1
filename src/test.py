import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from dotenv import dotenv_values
import mysql.connector
from hashlib import sha256

def get_db_connection():
  #connect to the database
  try:
     connection = mysql.connector.connect(
        host = "localhost",
        port = 3306,
        database = "cognicraft",
        username = "root",
        password = ""
    )
     return connection
  except mysql.connector.Error as err:
        # Handle connection error here (e.g., print message, display error to user)
        print("Error connecting to database:", err)
        return None  # Or raise a custom exception

#creating user session
if 'email' not in st.session_state:
    st.session_state['username'] = None


username = st.text_input("Username")
password = st.text_input("Password", type="password")

