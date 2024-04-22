import streamlit as st
import mysql.connector


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
  

header_section = st.container()
main_section = st.container()
auth_section = st.container()
logout_section = st.container()

#creating user session
if 'email' not in st.session_state:
    st.session_state['email'] = None #initial value of the session since no login yet

def show_auth_page():
    with auth_section:
        # Login/Registration Section
        if st.session_state['email'] is None:

            #-------login part-------------
            login_email = st.text_input("Email")
            login_password = st.text_input("Password", type="password")
            login_clicked = st.button("Login")

            #login functionality and logic
            if login_clicked:
                if login_email and login_password:
                    try:
                        #etablishing connection to the database
                        db =  get_db_connection()
                        cursor = db.cursor()#creating cursor object for queries
                        cursor.execute("SELECT * FROM user WHERE user_email = %s", (login_email,))
                        user = cursor.fetchone()#fetching one record
                        
                        #accessing user password
                        if user:
                            password_db = user[2]  # Retrieve password hash from database
                            st.write(password_db)
                            st.write(login_password)

                            if str(login_password) == str(password_db):
                                st.session_state['email'] = login_email
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

            #--------registration part------
            if st.checkbox("Register here"):
                st.write('Please Register using  your Hugging Face Credentials')
                with st.form("registration_form"):
                    email = st.text_input("Email")
                    new_password = st.text_input("Password", type="password")
                    password_confirmation = st.text_input("Confirm Password", type="password")
                    submit_button =  st.form_submit_button('Register')

                    if submit_button:
                        if email and new_password and password_confirmation:
                            if new_password == password_confirmation:
                                st.write(email,new_password,password_confirmation)
                                try:
                                    db = get_db_connection()
                                    cursor = db.cursor()
                                    # Check for email availability
                                    cursor.execute("SELECT * FROM user WHERE user_email = %s", (email,))
                                    existing_email = cursor.fetchone()

                                    if not existing_email:
                                        # Insert new user into database
                                        cursor.execute("INSERT INTO user (user_email, user_password) VALUES (%s, %s)", (email, new_password))
                                        db.commit()
                                        st.success("Successfully stored in the database!")  
                                    else:
                                        st.error("Email already exists. Please choose another.")
                                    cursor.close()
                                    db.close()
                                except Exception as e:
                                    st.error(f"Error connecting to database: {e}")
                            else:
                                st.warning('Passwords does not matched')
                        else:
                            st.error('Please Fill up the form')         


def main_section():
     st.write(f"Welcome, {st.session_state['username']}!")

def showlogout_page():
    auth_section.empty()
    with logout_section:
        st.button('Logout', key='logout', on_click=logout_clicked)

def logout_clicked():
    st.session_state['email'] = None
  
with header_section:
    if 'email' not in st.session_state:
        st.session_state['email'] = None
        show_auth_page()
    else:
        if st.session_state['email']:
            logout_section()
            main_section()
        else:
            show_auth_page()