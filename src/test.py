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
  
#@st.cache_resource
#def get_manager():
 #   return stx.CookieManager()

#cookie_manager = get_manager()

header_section = st.container()
main_section = st.container()
auth_section = st.container()
logout_section = st.container()

#creating user session states
if 'email' not in st.session_state:
    st.session_state.email = None #initial value of the session since no login yet
if 'user' not in st.session_state:
    st.session_state.user = False

#global variables
active_status = 0 #global variable to store the active status of the user 
initial_login_email = ""
def show_auth_page():
    with auth_section:
        # Login/Registration Section
        if st.session_state['email'] is None:
            st.write(f"User session state value: {st.session_state['user']}")#for debugging
            st.write(f"Active Status value: {active_status}")#for debuggin
            #see code at line 81 first
            #login functionality and logic
            def login_functionality():
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
                            st.write(password_db)# for debugging
                            st.write(login_password)#for debugging 
                            if str(login_password) == str(password_db):
                                st.session_state.email = login_email
                                st.session_state.user = True
                                #active_status = 1
                                #cursor.execute("UPDATE user set active_status = %s WHERE user_email = %s", (active_status,login_email))
                               # db.commit()
                                st.success("Login successful!")

                            else:
                                st.error("Incorrect password.")
                        else:
                            st.error("Email not found.")
                        cursor.close()
                        db.close()
                    except Exception as e:
                        st.error(f"Error connecting to database: {e}")
                else:
                    st.warning("Please enter username and password.")

            #-------login form part-------------
            login_email = st.text_input("Email")
            login_password = st.text_input("Password", type="password")
            st.button("Login", key='login',on_click=login_functionality)

           
            #--------registration part------
            if st.checkbox("Register here"):
                st.write('Please Register using  your Hugging Face Credentials')
                st.write('Hugging Face Credentials: ')
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


def show_main_section():
     with main_section:
        st.write(f"Active Status value: {active_status}")#for debuggin
        while active_status:
            st.write(f"Welcome, {st.session_state['email']}!")
            st.write(f"User session state value: {st.session_state['user']}")#for debugging
            st.write(f"Active Status value: {active_status}")#for debuggin

def showlogout_page():

   # initial_login_email =  st.session_state['email']#use for logout
    st.write(initial_login_email)
    auth_section.empty()
    with logout_section:
        st.button('Logout', key='logout', on_click=logout_clicked(initial_login_email))

def logout_clicked(login_email_after_session):

    #logout logic and functionality
    st.session_state.email = None     
    st.session_state.user = False
    active_status = 0
   # db = get_db_connection()
    #cursor = db.cursor()
   # show_auth_page()
   # cursor.execute("UPDATE user set active_status = %s WHERE user_email = %s", (active_status,login_email_after_session))
   # db.commit()
   # cursor.close()
   # db.close()

#main control flow 
with header_section:
    if 'email' not in st.session_state and 'user' not in st.session_state:
        show_auth_page()
    else:
        if st.session_state['email'] and st.session_state['user']:
            showlogout_page()
            show_main_section()
        else:
            show_auth_page()