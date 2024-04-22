import streamlit as st
import bcrypt
import mysql.connector
from hashlib import sha256
import bcrypt

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
  
#Hash passwords before storing
def hash_password(password):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')


#creating user session
if 'email' not in st.session_state:
    st.session_state['username'] = None


email = st.text_input("Email")
password = st.text_input("Password", type="password")
login_clicked = st.button("Login")

if login_clicked:
    if email and password:
        try:
            db =  get_db_connection()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user WHERE user_email = %s", (email,))
            user = cursor.fetchone()
            
            #accessing user password
            if user:
                password_db = user[2]  # Retrieve password hash from database
                st.write(password_db)
                st.write(password)

                if str(password) == str(password_db):
                    st.session_state['email'] = email
                    st.success("Login successful!")
                else:
                    st.error("Incorrect username or password.")
            else:
                st.error("Email not found.")
            cursor.close()
            db.close()
        except Exception as e:
            st.error(f"Error connecting to database: {e}")
    else:
        st.warning("Please enter username and password.")

if st.session_state['username'] is None:
    if st.checkbox("Register here"):
        st.write('Please Register using  your Hugging Face Credentials')
        with st.form("registration_form"):
            email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            password_confirmation = st.text_input("Confirm Password", type="password")

            submit_button =  st.form_submit_button('Register')
            if submit_button:
                if  new_password and password_confirmation and email:
                    if new_password == password_confirmation:
                        st.success("Successfully stored in the database!")
                    else:
                        st.warning('Passwords does not matched')
                else:
                    st.error('Please Fill up the form')        
