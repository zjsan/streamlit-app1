import streamlit as st
import mysql.connector
import requests
import re
from hugchat import hugchat
from hugchat.login import Login

st.set_page_config(page_title="Cognicraft")

#secrets = dotenv_values('hf.env')#remove once sytem login credentials is working

#---------Data Base Connection ------------
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
  
 #3 maximum number of retry attempts for connection
# Function to make an HTTPS request with retry logic
def make_https_request_with_retry(url, max_retry_attempts=3):
    # Loop for the maximum number of retry attempts
    for attempt in range(max_retry_attempts):
        try:
            # Attempt to make the HTTPS request
            response = requests.get(url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                return response  # Return the response if successful
            # Raise an exception if the status code is unexpected
            else:
                raise requests.exceptions.RequestException(f"Unexpected status code: {response.status_code}")
        # Handle timeout errors
        except requests.exceptions.Timeout:
            if attempt < max_retry_attempts - 1:
                st.write(f"Connection attempt {attempt+1} timed out. Retrying...")#debug
            else:
                st.write("Connection timed out after multiple attempts. Check your internet connection")#debug
        # Handle other request exceptions
        except requests.exceptions.RequestException as e:
            if attempt < max_retry_attempts - 1:
                st.write("An error occurred:", e, "Retrying...")#debug
            else:
                st.write("Maximum retry attempts reached. Check your internet connection")#debug
    return None  # Return None if all attempts fail


#using regular expression for basic email validation
def validate_email(email):
  """
  This function validates an email address using a regular expression.

  Args:
      email: The email address to validate.

  Returns:
      True if the email address is valid, False otherwise.
  """
  email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$" #The email_regex variable holds the regular expression pattern for validating emails
  return bool(re.fullmatch(email_regex, email))
  
#@st.cache_resource
#def get_manager():
 #   return stx.CookieManager()

#cookie_manager = get_manager()

#-----Page Containers----------------
header_section = st.container()
main_section = st.container()
auth_section = st.container()
logout_section = st.container()

#------------Session States-----------------------------

#session = requests.Session()
#session.timeout = 10

# Use the session to make your API call
#response = session.get("https://huggingface.co/chat/")
# Make the API call with a timeout of 15 seconds
#response = requests.get("https://huggingface.co/your/api/endpoint", timeout=15)

#credentials for hugging face api - will move it in the login functionality
#need to replace with the actual login credentials - see line 95
if 'hf_email' not in st.session_state:
    hf_email = None #set to empty string ex: hf_email = " "
if 'hf_pass' not in st.session_state:
    hf_pass = None

#if st.session_state.hf_email and st.session_state.hf_password:
   # cookie_path_dir = "./cookies"
   # sign = Login( st.session_state.hf_email, st.session_state.hf_pass)
   # cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

#creating user session states - user logged in 
if 'email' not in st.session_state:
    st.session_state.email = None #initial value of the session since no login yet
if 'user' not in st.session_state:
    st.session_state.user = False
#query params - trying to fix page refresh issue - not working
if 'logged_in' not in st.query_params:
    st.query_params.logged_in = False

#Session creation for the language model
if 'generated' not in st.session_state:
    st.session_state['generated'] = [""]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']
if 'msg_context' not in st.session_state:
    st.session_state.msg_context = ''

#global variables
active_status = 0 #global variable to store the active status of the user 
login_token = None# Create a variable to store the login token (initially None)

#--------- Authentication Page-----------
def show_auth_page():
    # Clear main section
    main_section.empty()
    with auth_section:
        st.title("CogniCraft - Smart Exam Question Generation With AI and Bloom's Taxonomy")
        # Login/Registration Section
        if st.session_state.email is None:
            #st.write(f"User session state value: {st.session_state['user']}")#for debugging
            #st.write(f"Active Status value: {active_status}")#for debuggin
            #see code at line 177 first for the login fields
            #login functionality and logic
            def login_functionality(login_email,login_password):
                if login_email and login_password:
                    try:
                        #etablishing connection to the database
                        db =  get_db_connection()
                        cursor = db.cursor()#creating cursor object for queries
                        cursor.execute("SELECT * FROM user WHERE user_email = %s", (login_email,))
                        user = cursor.fetchone()#fetching one record
                        
                        #accessing user password
                        if user:
                            password_db = user[2]  # Retrieve password from database
                            #st.write(password_db)# for debugging
                            #st.write(login_password)#for debugging 
                            if str(login_password) == str(password_db):
                                st.session_state.email = login_email
                                st.session_state.user = True
                                st.query_params.logged_in = True

                                #------ hugging Face credentials ------ 
                                st.session_state.hf_email = login_email
                                st.session_state.hf_pass =  login_password

                                #active_status = 1
                               # cursor.execute("UPDATE user set active_status = %s WHERE user_email = %s", (active_status, st.session_state.email))
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
            st.button("Login", key='login',on_click=login_functionality, args=(login_email,login_password))
   
           
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
                        if validate_email(email):
                            if email and new_password and password_confirmation:
                                if new_password == password_confirmation:
                                    #st.write(email,new_password,password_confirmation) - for debugging
                                    try:
                                        db = get_db_connection()
                                        cursor = db.cursor()
                                        # Check for email availability
                                        cursor.execute("SELECT * FROM user WHERE user_email = %s", (email,))
                                        existing_email = cursor.fetchone()

                                        if not existing_email:#if the email is not yet in the database then proceed to the registration logic 
                                            #st.write(new_password)#for debugging 
                                            # Insert new user into database
                                            cursor.execute("INSERT INTO user (user_email, user_password) VALUES (%s, %s)", (email, new_password))
                                            db.commit()
                                            st.success("Successfully stored in the database!")  
                                        else:
                                            st.error("Email already exists. Please choose another.")
                                    except Exception as e:
                                        st.error(f"Error connecting to database: {e}")
                                    finally:
                                        cursor.close()
                                        db.close()
                                else:
                                    st.warning('Passwords does not matched')
                            else:
                                st.error('Please Fill up the form')
                        else:
                            st.error('Email is not valid. Please provide a valid email')          

            #-----Update User Details-----------
            option = st.selectbox('Update User Details',
                                  ('Email', 'Password'), index=None,placeholder='Email / Password')

            #--------Update Email----------
            if option == 'Email':
                #st.write('Please Update Email ')
                with st.form("update_email_form"):
                    email = st.text_input("Current email")
                    new_email = st.text_input("New email")
                    confirm_email_update = st.text_input("Confirm email")
                    submit_button =  st.form_submit_button('Save')

                    if submit_button:#check if input fields is filled
                        if validate_email(new_email):
                            if email and new_email and confirm_email_update:
                                if new_email == confirm_email_update:
                                #------------database queries----------
                                #user email update logic
                                    try:
                                        db = get_db_connection()
                                        cursor = db.cursor()
                                        #-----authenticating user-------
                                        # Check for email availability
                                        cursor.execute("SELECT * FROM user WHERE user_email = %s", (email,))
                                        existing_email = cursor.fetchone()#retrieving current user_email from database
                                        cursor.execute("SELECT * FROM user WHERE user_email = %s", (new_email,))
                                        new_email_db = cursor.fetchone()#to check if new_email already exists

                                        #---------------authentication logic-----------------------
                                        if existing_email:#check if the old email is in the database
                                            if not new_email_db:#if new_email is not yet in the database then proceed to update the old email 
                                                # Insert new user into database
                                                # cursor.execute("UPDATE user set active_status = %s WHERE user_email = %s", (active_status, st.session_state.email))
                                                cursor.execute("UPDATE user set user_email = %s WHERE user_email = %s", (new_email, email))
                                                db.commit()
                                                st.success("Your email has been updated successfully. Please log in again with your new credentials.")  
                                            else:
                                                st.error("Email already exists. Please choose another.")
                                        else:
                                            st.error("The current email provided is incorrect. Please double-check and try again..")

                                    except Exception as e:
                                        st.error(f"Error connecting to database: {e}")
                                    finally:
                                        cursor.close()
                                        db.close()
                                        st.rerun()
                                else:
                                    st.warning('Invalid email confirmation.Please double-check and try again.')
                            else:
                                st.error('Please Fill up the form') 
                                st.rerun()
                        else:
                            st.error('Email is not valid. Please provide a valid email') 
                            #st.rerun()

            #----Update Password----
            elif option == 'Password':
                # st.write('Please Update Email ')
                with st.form("update_password_form"):
                    email = st.text_input("Email")
                    password = st.text_input("Current password", type="password")
                    new_password = st.text_input("New password", type="password")
                    confirm_password_update = st.text_input("Confirm password", type="password")
                    submit_button = st.form_submit_button('Save')

                    if submit_button:
                        if email and password and new_password and confirm_password_update:
                            try:
                                # ----executing database interactions----
                                db = get_db_connection()
                                cursor = db.cursor()

                                # -----fetching user details-------
                                cursor.execute("SELECT * FROM user WHERE user_email = %s", (email,))
                                user_data = cursor.fetchone()

                                if user_data:
                                    db_user_password = user_data[2]  # plain text password from the database
                                    # Authenticate user by comparing plain text passwords
                                    if password == db_user_password:
                                        if new_password == confirm_password_update:
                                            if new_password != password:  # Ensure new password is not the same as old password
                                                # Update password
                                                cursor.execute("UPDATE user SET user_password = %s WHERE user_email = %s",
                                                            (new_password, email))
                                                db.commit()
                                                st.success("Your password has been updated successfully. Please log in again with your new credentials.")
                                            else:
                                                st.warning('Your new password cannot be the same as your current password. Please choose a different password.')
                                        else:
                                            st.warning('Passwords do not match. Please double-check and try again.')
                                    else:
                                        st.warning('The current password entered does not match with the password in the database.')
                                else:
                                    st.error("The email provided is incorrect. Please double-check and try again.")
                            except Exception as e:
                                st.error(f"Error connecting to database: {e}")
                            finally:
                                cursor.close()
                                db.close()
                                st.rerun()
                        else:
                            st.error('Please fill up the form')
                            #st.rerun()


#---------Main Page-------------
def show_main_section():
    
     auth_section.empty() # Clear authentication section
     with main_section:
        st.title("CogniCraft - Smart Exam Question Generation With AI and Bloom's Taxonomy")
       # st.write(f"Active Status value: {active_status}")#for debuggin
        st.sidebar.write(f"Welcome, {st.session_state['hf_email']}!")
        showlogout_page()
       # st.write(f"User session state value: {st.session_state['user']}")#for debugging
       # st.write(f"Active Status value: {active_status}")#for debugging

        if st.session_state.email and st.session_state.user and login_status:
            #Containers for llm and user response
            input_container = st.container()
            #colored_header(label='', description='', color_name='blue-30')
            response_container = st.container()
            
            #Main Page Sidebar
            with st.sidebar:
                st.markdown('''
                ## About
                This app is a LLM-powered exam question generator built using:
                - [Streamlit](<https://streamlit.io/>)
                - [HugChat](<https://github.com/Soulter/hugging-chat-api>)
                - [OpenAssistant/oasst-sft-6-llama-30b-xor](<https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor>) LLM model
                ''') 
            #----------Question Inputs Section----------------
            def question_params():
                question_params = []
                #question_params_length = len(question_params)

                #question type
                question_type = st.selectbox(
                "Question Type",
                ("Multiple Choice", "True or False", "Fill in the Blanks"),
                index=None,
                placeholder="Select question type...",
                )
                    
                #condition for question type
                if question_type == 'Multiple Choice':
                    st.write('Multiple choice')
                    st.write('Multiple-Choice Questions are versatile and can be used across various cognitive domains')
                    question_params.append(question_type)   
                elif question_type == 'True or False':
                    st.write('True or False')
                    #need to implement better mechanism for the true or false than this 
                    st.write("True or false questions are typically best suited for assessing the remembering and understanding levels of Bloom's taxonomy.")
                    st.write('Please select the appropriate cognitive level')
                    question_params.append(question_type)
                elif question_type == 'Fill in the Blanks':
                    st.write('Fill in the Blanks')
                    st.write("A fill-in-the-blank type of test question can be effective for assessing cognitive levels ranging from remembering to applying.")
                    st.write('Please select the appropriate cognitive level')
                    question_params.append(question_type)
                else:
                    st.write('Select Question type') 
                
                #question_number
                question_number = st.text_input('Number of Items')
                question_params.append(question_number)#add number of items

                #taxomy level
                #need to disable processing for True or False != Remembering and True or False != Understanding
                taxonomy_level = st.selectbox(
                "Taxonomy Level",
                ("Remembering", "Understanding", "Applying", "Analyzing", "Evaluating", "Creating"),
                index=None,
                placeholder="Select taxonomy level...",
                )

                #condition for taxonomy level
                if taxonomy_level == 'Remembering':
                    st.write('Remembering')
                    question_params.append(taxonomy_level)  
                elif taxonomy_level == 'Understanding':
                    st.write('Understanding')
                    question_params.append(taxonomy_level) 
                elif taxonomy_level == 'Applying':
                    st.write('Applying')
                    question_params.append(taxonomy_level)
                elif taxonomy_level == 'Analyzing':
                    st.write('Analyzing')
                    question_params.append(taxonomy_level)
                elif taxonomy_level == 'Evaluating':
                    st.write('Evaluating')
                    question_params.append(taxonomy_level)
                elif taxonomy_level == 'Creating':
                    st.write('Creating')
                    question_params.append(taxonomy_level)
                else:
                    st.write('Select Taxonomy Level') 

                #difficulty level
                difficulty = st.selectbox(
                "Question Difficulty",
                ("Easy", "Medium", "Hard"),
                index=None,
                placeholder="Select difficulty level...",
                )
                question_params.append(difficulty)
                
                return question_params

            #----------Generation of the response from the LLM----------------
            def generate_response(prompt,question_parameters):
                
                #hugchat credentials will act as the api for the language model
                cookie_path_dir = "./cookies"
                sign = Login( st.session_state.hf_email, st.session_state.hf_pass)
                cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
                # Send prompt to chatbot and get response
                chatbot = hugchat.ChatBot(cookies=cookies.get_dict()) 

                #----- Commented out statements for debugging---------
                #st.write(question_parameters)
                #st.write(question_parameters[3],question_parameters[2],question_parameters[1])
                #testing prompts parameters
                #added prompt templates for the ai to use in the question generation
                #addional_prompts[0] = Question Type
                #additional_prompts[1] = Question Number
                #additional_prompts[2] = Taxonomy Level
                #additional_prompts[3] = Difficulty level
                

                #------Checking connectivity with the api before processing response----------
                url = "https://huggingface.co"
                httpsresponse = make_https_request_with_retry(url)
                #---If connection succesful proceed to question generation--------------
                if httpsresponse:
                    # Process the response here
                    #st.write("Response:", httpsresponse.text)#debugging
                        
                    if question_parameters[0] == 'Multiple Choice':
                            #prompt template for multiple choice => aligning cognitive levels thru prompt tuning the model using few-shot learning
                            if question_parameters[2] == 'Remembering':
                                #Generate `{num_questions}` multiple choice questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure each question has at least 4 answer choices and a clear answer key.
                                prompt = "Exam questions creation: Generate {} multiple choice questions at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy based on this context: {} Ensure each question has at least 4 answer choices and a clear answer key. The format of the questions must be like a formal exam paper.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)
                            
                                #feeding sample data for the llm for optimization of responses
                                few_shot_prompt = '''
                                                For example:

                                                **Question:** Who wrote the novel "Noli Me Tangere"?

                                                * A) Jose Rizal (Correct Answer)
                                                * B) Andres Bonifacio
                                                * C) Emilio Aguinaldo
                                                * D) Marcelo H. del Pilar

                                            **Question:** What is the chemical symbol for oxygen?

                                                    * A) O (Correct Answer)
                                                    * B) H
                                                    * C) Au
                                                    * D) Na

                                            **Question:** Question: In which year did the Philippine Revolution against Spanish colonization begin?

                                                    * A) 1896 (Correct Answer)
                                                    * B) 1898
                                                    * C) 1872
                                                    * D) 1892

                                                **Question:** What is the formula for calculating the area of a rectangle?

                                                * A) Length * Width (Correct Answer)
                                                * B) Length + Width
                                                * C) Length ÷ Width
                                                * D) Length - Width

                                            '''
                                full_prompt = prompt + few_shot_prompt
                                #st.write(full_prompt)# Debugging
                                response = chatbot.chat(full_prompt)
                                return response    

                            elif question_parameters[2] == 'Understanding':
                                    #Generate `{num_questions}` multiple choice questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure each question has at least 4 answer choices and a clear answer key.
                                    prompt = "Exam questions creation: Generate {} multiple choice questions at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy based on this context: {} Ensure each question has at least 4 answer choices and a clear answer key. The format of the questions must be like a formal exam paper.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)

                                    #feeding sample data for the llm for optimization of responses
                                    few_shot_prompt = '''
                                                    For example:

                                                    **Question:** Which statement best explains the concept of natural selection?
                                                    
                                                        * A) Animals adapt to their environments over time.
                                                        * B) Evolution occurs due to random genetic mutations.
                                                        * C) Organisms that are better suited to their environment survive and reproduce. (Correct Answer)
                                                        * D) All species share a common ancestor
                                                    
                                                    **Question:** What is the main idea of the theory of relativity proposed by Albert Einstein?

                                                        * A) Time travel is possible.
                                                        * B) Gravity is caused by the curvature of space-time. (Correct Answer)
                                                        * C) Energy cannot be created or destroyed.
                                                        * D) Light behaves as both a wave and a particle.

                                                    **Question:** What is the main idea of the theory of relativity proposed by Albert Einstein?

                                                    * A) Time travel is possible.
                                                    * B) Gravity is caused by the curvature of space-time. (Correct Answer)
                                                    * C) Energy cannot be created or destroyed.
                                                    * D) Light behaves as both a wave and a particle.

                                                    **Question:** Which of the following best describes the concept of cultural relativism?

                                                    * A) All cultures are equally valid.
                                                    * B) There are universal moral truths
                                                    * C) Cultural norms should be judged based on their own context. (Correct Answer)
                                                    * D) Cultural diversity is harmful to society.

                                                    **Question:** What is the significance of the Magna Carta in English history?

                                                    * A) It established the principles of democracy.
                                                    * B) It granted certain rights to English nobles. (Correct Answer)
                                                    * C) It abolished the monarchy.
                                                    * D) It declared war on France.

                                                '''
                                    full_prompt = prompt + few_shot_prompt
                                    #st.write(full_prompt)# Debugging
                                    response = chatbot.chat(full_prompt)
                                    return response
                            elif question_parameters[2] == 'Applying':

                                #Generate `{num_questions}` multiple choice questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure each question has at least 4 answer choices and a clear answer key.
                                prompt = "Exam questions creation: Generate {} multiple choice questions at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy based on this context: {} Ensure each question has at least 4 answer choices and a clear answer key. The format of the questions must be like a formal exam paper.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)

                                #feeding sample data for the llm for optimization of responses
                                few_shot_prompt = '''
                                                For example:

                                                **Question:** If the radius of a circle is 5 cm, what is its area?
                                                
                                                    * A) 10π cm²
                                                    * B) 25π cm² (Correct Answer)
                                                    * C) 50 cm²
                                                    * D) 125π cm²
                                                
                                                **Question:** If a car travels at a constant speed of 60 km/h for 3 hours, how far does it travel?

                                                    * A) 120 km
                                                    * B) 180 km (Correct Answer)
                                                    * C) 240 km
                                                    * D) 360 km

                                                **Question:** Which of the following scenarios best illustrates the concept of opportunity cost?

                                                * A) Choosing to spend money on a new phone instead of saving for college.
                                                * B) Spending money on groceries instead of dining out.
                                                * C) Investing in stocks instead of bonds.
                                                * D) Using extra time to study for an exam instead of watching TV. (Correct Answer)

                                                **Question:** If a chemical reaction requires 20 grams of reactant A and 30 grams of reactant B, how much product will be produced?

                                                * A) 50 grams
                                                * B) 40 grams
                                                * C) 70 grams (Correct Answer)
                                                * D) 100 grams

                                                **Question:** In a programming task, if you want to sort an array in ascending order, which algorithm would you most likely use?

                                                * A) Bubble Sort
                                                * B) Merge Sort
                                                * C) Quick Sort
                                                * D) All of the above (Correct Answer)
                                            '''
                                full_prompt = prompt + few_shot_prompt
                            # st.write(full_prompt)# Debugging
                                response = chatbot.chat(full_prompt)
                                return response
                            
                            elif question_parameters[2] == 'Analyzing':

                                #Generate `{num_questions}` multiple choice questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure each question has at least 4 answer choices and a clear answer key.
                                prompt = "Exam questions creation: Generate {} multiple choice questions at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy based on this context: {} Ensure each question has at least 4 answer choices and a clear answer key. The format of the questions must be like a formal exam paper.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)

                                #feeding sample data for the llm for optimization of responses
                                few_shot_prompt = '''
                                                For example:

                                                **Question:**  Which of the following best explains the significance of a control group in an experiment?
                                                
                                                    * A) It ensures that the experiment is conducted ethically.
                                                    * B) It provides a baseline for comparison to determine the effect of the independent variable. (Correct Answer)
                                                    * C) It allows researchers to make predictions about future outcomes
                                                    * D) It ensures that the results of the experiment are valid.
                                                
                                                **Question:** In a scientific experiment investigating plant growth, which of the following variables would be considered the independent variable?

                                                    * A) The type of soil used
                                                    * B) The amount of sunlight received.
                                                    * C) The frequency of watering.
                                                    * D)  The presence or absence of fertilizer. (Correct Answer)

                                                **Question:** Given the graph of a quadratic function, which of the following statements about its vertex is true?

                                                * A) It is the highest point on the graph
                                                * B) It lies on the x-axis.
                                                * C) It is the point where the derivative is zero. (Correct Answer)
                                                * D) It is always at the origin.

                                                **Question:** if g(x) = √x+4, what is the domain of the function?

                                                * A) x ≥ -4 (Correct Answer)
                                                * B) x ≤ -4
                                                * C) x > 4
                                                * D) x < -4

                                                **Question:** When analyzing the efficiency of algorithms, which of the following factors is most important to consider?

                                                * A) Syntax
                                                * B) Runtime complexity (Correct Answer)
                                                * C) Variable naming conventions
                                                * D) Code readability
                                            '''

                                full_prompt = prompt + few_shot_prompt
                                #st.write(full_prompt)# Debugging
                                response = chatbot.chat(full_prompt)
                                return response

                            elif question_parameters[2] == 'Evaluating':
                                #Generate `{num_questions}` multiple choice questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure each question has at least 4 answer choices and a clear answer key.
                                prompt = "Exam questions creation: Generate {} multiple choice questions at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy based on this context: {} Ensure each question has at least 4 answer choices and a clear answer key. The format of the questions must be like a formal exam paper.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)

                                #feeding sample data for the llm for optimization of responses
                                few_shot_prompt = '''
                                                For example:

                                                **Question:** Which of the following marketing strategies would be most effective in reaching a target audience of young adults?
                                                
                                                    * A) Television commercials.
                                                    * B) Social media advertising. (Correct Answer)
                                                    * C) Newspaper ads.
                                                    * D) Billboards.
                                                
                                                **Question:** Which of the following arguments is most convincing in support of renewable energy sources?

                                                    * A) Renewable energy is environmentally friendly.
                                                    * B) Renewable energy creates jobs and stimulates economic growth.
                                                    * C) Renewable energy reduces dependence on fossil fuels and decreases greenhouse gas emissions. (Correct Answer)
                                                    * D) All of the above.

                                                **Question:** Which of the following scenarios presents the greatest ethical dilemma?

                                                * A) A doctor falsifies medical records to protect a patient's privacy.
                                                * B) An employee reports a coworker for unethical behavior.
                                                * C) A company knowingly sells a defective product to consumers. (Correct Answer)
                                                * D) A student cheats on an exam to maintain a high GPA.

                                                **Question:**  Which of the following criteria would you use to evaluate the effectiveness of a government policy?

                                                * A) Economic impact.
                                                * B) Social equity.
                                                * C) Environmental sustainability.
                                                * D) All of the above (Correct Answer)

                                            '''

                                full_prompt = prompt + few_shot_prompt
                                #st.write(full_prompt)# Debugging
                                response = chatbot.chat(full_prompt)
                                return response
                            
                            elif question_parameters[2] == 'Creating':
                                #Generate `{num_questions}` multiple choice questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure each question has at least 4 answer choices and a clear answer key.
                                prompt = "Exam questions creation: Generate {} multiple choice questions at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy based on this context: {} Ensure each question has at least 4 answer choices and a clear answer key. The format of the questions must be like a formal exam paper.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)

                                #feeding sample data for the llm for optimization of responses
                                few_shot_prompt = '''
                                                For example:

                                                **Question:** If you were tasked with designing a new product to solve a common problem, what features would you include?

                                                    * A) Increased durability and reliability.
                                                    * B) User-friendly interface and intuitive design.
                                                    * C) Integration of cutting-edge technology.
                                                    * D) All of the above (Correct Answer)

                                                **Question:** You have been tasked with designing a mobile app to help students learn programming concepts. Which of the following features would you prioritize to ensure an engaging and effective learning experience?

                                                    * A) A virtual coding playground where students can write and test their code.
                                                    * B) Interactive tutorials with step-by-step instructions and real-world examples. (Correct Answer)
                                                    * C) A leaderboard to track students' progress and encourage healthy competition.
                                                    * D) Social media integration for students to share their coding achievements with friends.

                                                **Question:** Imagine you are planning a science fair project to investigate the effects of different types of soil on plant growth. Which of the following experimental designs would be most suitable for testing your hypothesis?

                                                    * A) Watering plants with varying amounts of water daily.
                                                    * B) Using identical pots and seeds but different types of soil for each group. (Correct Answer)
                                                    * C) Keeping all variables constant except for the amount of sunlight received.
                                                    * D) Observing plants grown in different locations around the school.

                                                **Question:** Suppose you are developing a website for a local business. Which of the following design elements would you include to enhance user experience and accessibility?

                                                    * A) High-resolution images and flashy animations.
                                                    * B) Clear navigation menus and intuitive layout. (Correct Answer)
                                                    * C) Auto-playing videos and background music.
                                                    * D) Hidden content that requires users to hover over certain areas to reveal.   
                                            '''
                                full_prompt = prompt + few_shot_prompt
                                #st.write(full_prompt)# Debugging
                                response = chatbot.chat(full_prompt)
                                return response

                    elif question_parameters[0] == 'True or False':
                        if question_parameters[2] == 'Remembering':
                            # Generate `{num_questions}` True or False statements at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable)
                            prompt = "Exam questions creation: Generate {} True or False test questions at a {} difficulty level that is align with the {} cognitive level of bloom's taxonomy based in this context: {} Ensure each question has a clear answer use this format: ".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)
                            #feeding sample data for the llm for optimization of responses
                            few_shot_prompt = '''
                                            For example: 
                                            
                                            **Instruction: ** Write the T if the statement is True. Otherwise write F if the statement is False. Write the answer before the item.

                                            **Question:** **Create 4 underscores for the supposed answer** The sum of the interior angles of a triangle is 180 degrees.    

                                                *Answer: True
                                            
                                            **Question:** **_____** Water boils at 100 degrees Celsius at sea level.    

                                                *Answer: True
                                            
                                                    
                                            **Question:** **_____** HTML is a programming language. 

                                                *Answer: False

                                            **Question:** **_____** A prime number is divisible by only one and itself.

                                                *Answer: True
                                            
                                            **Question:** **_____**  Photosynthesis is the process by which plants convert carbon dioxide and water into oxygen and glucose.

                                                *Answer: True

                                            '''

                            #prompt template for True or False
                            full_prompt = prompt + few_shot_prompt
                            #st.write(full_prompt)  # Debugging

                            response = chatbot.chat(full_prompt)
                            return response

                        elif question_parameters[2] == 'Understanding':

                            # Generate `{num_questions}` True or False statements at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable)
                            prompt = "Exam questions creation: Generate {} True or False test questions at a {} difficulty level that is align with the {} cognitive level of bloom's taxonomy based in this context: {} Ensure each question has a clear answer use this format: ".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)

                            #feeding sample data for the llm for optimization of responses
                            few_shot_prompt = '''
                                            For example: 
                                            
                                            **Instruction: ** Write the T if the statement is True. Otherwise write F if the statement is False. Write the answer before the item.

                                            **Question:** **Create 4 underscores for the supposed answer** If a triangle has sides of lengths 3, 4, and 5 units, it is a right triangle..    

                                                *Answer: True
                                            
                                            **Question:** **_____** Electrons are negatively charged particles found in the nucleus of an atom.

                                                *Answer: False

                                            **Question:** **_____** Object-oriented programming focuses on breaking down a program into small, reusable pieces called functions.

                                                *Answer: False
                                            
                                            **Question:** **_____** The equation y = mx + b represents a linear function.

                                                *Answer: True
                                            
                                            **Question:** **_____** Newton's first law of motion states that an object at rest will remain at rest unless acted upon by an unbalanced force.

                                                *Answer: True    
                                            '''

                            #prompt template for True or False
                            full_prompt = prompt + few_shot_prompt
                        # st.write(full_prompt)  # Debugging

                            response = chatbot.chat(full_prompt)
                            return response
                        else:
                            return False 

                    elif question_parameters[0] == 'Fill in the Blanks':

                        difficulty_level = question_parameters[3]
                        difficulty_level_map = {
                            "Easy": 1,  # One blank for Easy difficulty
                            "Medium": 2,  # Two blanks for Medium difficulty
                            "Hard": 3   # Three blanks for Hard difficulty
                            }
                        
                        num_blanks = difficulty_level_map.get(difficulty_level, 1)  # Default to 1 blank
                        if question_parameters[2] == 'Remembering':
                            #prompt template for Fill in the Blanks
                            # Generate `{num_questions}` fill-in-the-blank questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question.
                            #"Generate `{num_questions}` fill-in-the-blank questions in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question. At a {difficulty_level} difficulty level, each question should have {num_blanks} blank(s)."
                            prompt = "Exam questions creation: Generate {} fill-in-the-blank question items that is alignn with the {} cognitive level of bloom's taxonomy  based in this context: {} Ensure the blanks are clearly identified and essential to the question. At a {} difficulty level, each question should have {} blank(s) and has clear answers.".format(question_parameters[1],question_parameters[2],prompt,question_parameters[3], num_blanks)
                        
                            #feeding sample data for the llm for optimization of responses
                            few_shot_prompt = '''
                                                For example: 

                                                **Question:** The process by which plants convert sunlight into energy is called _______.
                            
                                                    *Answer: photosynthesis

                                                **Question:** The process by which water evaporates from the Earth's surface and condenses back into rain is known as the _______ cycle.
                            
                                                    *Answer: water

                                                **Question:** The three primary colors used in mixing pigments for painting are _______, _______, and ______.
                            
                                                    *Answer: red, yellow, blue
                                            '''
                                    
                            full_prompt = prompt + few_shot_prompt
                        # st.write(full_prompt)  # Debugging
                            response = chatbot.chat(full_prompt)
                            return response 
                        
                        elif question_parameters[2] == 'Understanding':
                            #prompt template for Fill in the Blanks
                             # Generate `{num_questions}` fill-in-the-blank questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question.
                            #"Generate `{num_questions}` fill-in-the-blank questions in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question. At a {difficulty_level} difficulty level, each question should have {num_blanks} blank(s)."
                            prompt = "Exam questions creation: Generate {} fill-in-the-blank question items that is alignn with the {} cognitive level of bloom's taxonomy  based in this context: {} Ensure the blanks are clearly identified and essential to the question. At a {} difficulty level, each question should have {} blank(s) and has clear answers.".format(question_parameters[1],question_parameters[2],prompt,question_parameters[3], num_blanks)

                            #feeding sample data for the llm for optimization of responses
                            few_shot_prompt = '''
                                                For example: 

                                                **Question:** Although both are forms of precipitation, rain and snow differ because _______ determines whether water vapor freezes into ice crystals or falls as liquid droplets.
                            
                                                    *Answer: temperature
                                            '''
                                    
                            full_prompt = prompt + few_shot_prompt
                        # st.write(full_prompt)  # Debugging
                            response = chatbot.chat(full_prompt)
                            return response 
                        
                        elif question_parameters[2] == 'Applying':    
                            #prompt template for Fill in the Blanks
                            # Generate `{num_questions}` fill-in-the-blank questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question.
                            #"Generate `{num_questions}` fill-in-the-blank questions in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question. At a {difficulty_level} difficulty level, each question should have {num_blanks} blank(s)."
                            prompt = "Exam questions creation: Generate {} fill-in-the-blank question items that is alignn with the {} cognitive level of bloom's taxonomy  based in this context: {} Ensure the blanks are clearly identified and essential to the question. At a {} difficulty level, each question should have {} blank(s) and has clear answers.".format(question_parameters[1],question_parameters[2],prompt,question_parameters[3], num_blanks)
                            #feeding sample data for the llm for optimization of responses
                            few_shot_prompt = '''
                                                For example: 

                                                **Question:**  If you want to increase the speed of a moving object, you would need to apply more _______. 
                            
                                                    *Answer: force
                                            '''
                                    
                            full_prompt = prompt + few_shot_prompt
                        # st.write(full_prompt)  # Debugging
                            response = chatbot.chat(full_prompt)
                            return response  
                        else:
                            #prompt template for Fill in the Blanks
                            # Generate `{num_questions}` fill-in-the-blank questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question.
                            prompt = "Exam questions creation: Generate {} fill-in-the-blank question items at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy  based in this context: {} Ensure the blanks are clearly identified and essential to the question and has clear answers.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)
                        # st.write(prompt)  # Debugging
                            response = chatbot.chat(prompt)
                            return response
                        
                #----Abort further processing---------
                else:
                    st.warning("Failed to make the HTTPS request.")
                    st.warning("Check your internet connection and restart the application")
                    st.stop()

            #Handles the storage of question context and generated responses in the database
            def response_ai(user_message, additional_prompts):
                with response_container:
                    if user_message:
                        response = generate_response(user_message, additional_prompts)
                        st.session_state.past.append(user_message)
                        st.session_state.generated.append(response)

                        # Inserting record in the input_data table
                        try:
                            db = get_db_connection()
                            cursor = db.cursor()
                            # Check for email availability
                            cursor.execute("SELECT * FROM user WHERE user_email = %s", (st.session_state.email,))
                            user = cursor.fetchone()

                            if user:
                                user_id = user[0]  # Getting user_id
                                # st.write(user_id)
                                cursor.execute("INSERT INTO input_data (questions_context, user_id) VALUES (%s, %s)",
                                                    (st.session_state.msg_context, user_id))  # Insert user question context  into input_data table
                                cursor.execute("SELECT LAST_INSERT_ID()")  # Get the data_id of the newly inserted record
                                data_id = cursor.fetchone()[0]

                                # Insert AI-generated response into responses table
                                if st.session_state.generated:  # Check if generated responses exist
                                    for generated_response in st.session_state.generated:
                                        # Only insert if the response is not empty
                                        if generated_response:
                                            cursor.execute("INSERT INTO responses (responses, data_id) VALUES (%s, %s)",
                                                        (str(generated_response), data_id))
                                    db.commit()#proceed to insert the record
                                   
                                    #display the generated questions and question context
                                    for i in range(len(st.session_state['generated'])):
                                        st.write(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                                        st.write(st.session_state['generated'][i], key=str(i))

                                else:
                                    st.warning("No responses generated.")  # Inform user if no responses were generated
                            else:
                                st.error("User not found.")
                        except Exception as e:
                            st.error(f"Error connecting to database: {e}")
                        finally:
                            st.success("Questions Generated!")
                            st.success("Check Response History.")
                            cursor.close()  # Ensure cursor is closed even in case of exceptions
                            db.close()  # Ensure database connection is closed
                            #st.rerun()  # After the insertion, trigger a rerun of the Streamlit app


            #--------Implementing the Response History Feature--------
            def get_response_history_from_db():
                try:
                    db = get_db_connection()
                    cursor = db.cursor()
                    
                    # Retrieve user_id based on the current user's email
                    cursor.execute("SELECT user_id FROM user WHERE user_email = %s", (st.session_state.email,))
                    user_id_result = cursor.fetchone()
                    
                    if user_id_result:
                        user_id = user_id_result[0]  # Extract user_id from the result
                        
                        # Fetch conversation history for the logged-in user from the database using user_id
                        cursor.execute("SELECT DATE_FORMAT(responses.date_created, '%Y-%m-%d %h:%i %p') AS formatted_datetime, responses.responses, input_data.questions_context FROM responses INNER JOIN input_data ON responses.data_id = input_data.data_id WHERE input_data.user_id = %s ORDER BY responses.date_created DESC;", (user_id,))
                        response_history = cursor.fetchall()
                        
                        return response_history  # Return entire fetched rows with formatted datetime and responses
                    else:
                        st.error("User not found.")
                        return []
                except Exception as e:
                    st.error(f"Error connecting to database: {e}")
                    return []
                finally:
                    cursor.close()
                    db.close()

         # Function to delete a response from the database
            def delete_response_from_db(response):
                try:
                    db = get_db_connection()
                    cursor = db.cursor()
                    
                    cursor.execute("DELETE FROM responses WHERE responses = %s", (response,))
                    db.commit()

                except Exception as e:
                    st.error(f"Error connecting to database: {e}")
                finally:
                    cursor.close()
                    db.close()

            # Function to delete a response from the database
            def delete_question_context_from_db(question_context):
                try:
                    db = get_db_connection()
                    cursor = db.cursor()
                    
                    # Delete the response and question_context from the database
                    cursor.execute("DELETE FROM input_data WHERE questions_context = %s", (question_context,))
                    db.commit()

                except Exception as e:
                    st.error(f"Error connecting to database: {e}")
                finally:
                    cursor.close()
                    db.close()

            # Function to display response history in sidebar and handle interaction
            def display_response_history():
                st.sidebar.title("Response History")
                response_history = get_response_history_from_db()

                if response_history:
                    for i, (formatted_datetime, response, question_context) in enumerate(response_history):
                        # Show a snippet of each response in the sidebar
                        truncated_response = response[:50] + "..." if len(response) > 50 else response
                        
                        # Create unique keys for buttons using the index i
                        chats_button_key = f"chats_button_{i}"
                        delete_button_key = f"delete_button_{i}"
                        
                        # Create columns to place response and delete button side by side
                        col1, col2 = st.sidebar.columns([4,1])
                        
                        # Create buttons with unique keys
                        chats_button = col1.button(f"{formatted_datetime}: {truncated_response}", key=chats_button_key)
                        delete_button = col2.button("🗑️", key=delete_button_key)
                        
                        # Function to handle delete button click event
                        if delete_button:
                            print("Delete button clicked for response:", response)  # Debug statement
                            print("Question context:", question_context)  # Debug statement
                            delete_question_context_from_db(question_context)
                            delete_response_from_db(response)
                            st.rerun()  # Rerun the Streamlit app after deletion

                        # If a response is clicked, clear current view and load historical message in main view
                        if chats_button:
                            clear_chat_view()
                            load_historical_message(response, question_context)
                        
                        # Add a spacer between rows for better visual separation
                        st.sidebar.write("---")
                else:
                    st.sidebar.write("No response history available.")
                #st.rerun()  # Rerun the Streamlit app after deletion
    
            # Function to clear the current chat view
            def clear_chat_view():
                st.empty()
                # Implement logic to clear chat view here
                pass

            # Function to load historical message in main view
            def load_historical_message(response,question_context):
                st.empty()
                # Implement logic to load historical message in main view here
                st.write(question_context)
                st.write(response)
                #st.write(st.session_state.msg_context)
 
            def main():
                get_db_connection()  # checking database connection
                
                # Applying the user input box
                with input_container:
                    # User input
                    additional_prompts = list(question_params())
                    #st.write(additional_prompts)
                    
                    # Display response history
                    display_response_history()
                    
                    # If user enters needed parameters, enable text input for context
                    user_message = st.text_area("Enter text context:")  # taking user provided prompt as input
                    
                    if st.button("Submit"):
                        # ---Validating User Inputs----
                        if additional_prompts is not None:
                            if len(additional_prompts) >= 2 and additional_prompts[1] is not None:
                                if int(additional_prompts[1]) > 0:
                                    if user_message:#if text context is filled proceed to generate response
                                        st.session_state.msg_context = user_message#assigning text context to session state variable
                                        with st.spinner('Wait for it...'):
                                            response_ai(user_message, additional_prompts)#calling function that handles the the function call for question generation
                                    else:
                                        st.warning("Please provide the question context.")
                                else:
                                    st.warning('Question items must be greater than 0')
                            else:
                                st.warning("Missing input fields.")
                        else:
                            st.warning("Missing input fields.")

                    #else:
                     #  st.warning('Missing input fields')

            if __name__ == "__main__":
                main()
                #st.rerun()

def showlogout_page():
    #initial_login_email =  st.session_state['email']#use for logout
    # Clear main section
    main_section.empty()
    auth_section.empty()
    with logout_section:
        if st.session_state.email and st.sidebar.button('Logout', key='logout'):
        #----------implementing a pop window before logging out the user--------
            #logout_clicked()
        #st.button("Login", key='login',on_click=login_functionality, args=(login_email,login_password))
            #st.warning('Are you sure you want to log out?')
            #if st.button("Yes",key='proceed_logout',on_click=logout_clicked):
             #   st.success('You are now logged out')
           # elif st.button("No"):
            #    st.rerun()
            #show_auth_page()
            with st.container(border=True):
                st.sidebar.checkbox('Verify logout', key='verify_logout')
                if st.button("Yes",key='proceed_logout',on_click=logout_clicked):
                     st.success('You are now logged out')
                elif st.button("No"):
                    st.rerun()
                
            

def logout_clicked():
    # Clear main section
    main_section.empty()
    #logout logic and functionality
    st.session_state.email = None     
    st.session_state.user = False
    st.session_state.hf_email = None
    st.session_state.hf_pass = None
    st.query_params.clear()
   # active_status = 0
   # db = get_db_connection()
    #cursor = db.cursor()
    #show_auth_page()
   # cursor.execute("UPDATE user set active_status = %s WHERE user_email = %s", (active_status,login_email_after_session))
   # db.commit()
   # cursor.close()
   # db.close()

#main control flow 
with header_section:
    if 'hf_email' not in st.session_state and 'user' not in st.session_state:

        main_section.empty()# Clear main section
        show_auth_page()
        st.stop()
    else:
        login_status = st.query_params.get("logged_in")
       # st.write(login_status)
        if st.session_state.email and st.session_state.user and login_status:
            show_main_section()
            st.stop()
        else:
            main_section.empty()  # Clear main section
            logout_clicked()
            show_auth_page()
            st.stop()