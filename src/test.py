import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

st.set_page_config(page_title="🤗💬 Cognicraft")

#credentials
hf_email = 'zjsantos25@gmail.com'
hf_pass = 'Th3ege@rprggrmmr1231231'

cookie_path_dir = "./cookies"
sign = Login(hf_email, hf_pass)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)


with st.sidebar:
    st.title('🤗💬 HugChat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](<https://streamlit.io/>)
    - [HugChat](<https://github.com/Soulter/hugging-chat-api>)
     - [OpenAssistant/oasst-sft-6-llama-30b-xor](<https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor>) LLM model
                
      💡 Note: No API key required!
    ''')

def question_params():


    question_params = {}

    #question type
    question_type = st.selectbox(
    "Question Type",
    ("Multiple Choice", "True or False", "Fill in the blanks"),
    index=None,
    placeholder="Select question type...",
    )
        
    if question_type == 'Multiple Choice':
        st.write('Right you Multiple choice')
        question_params.append(question_type)
    elif question_type == 'True or False':
        st.write('True or False')
        question_params.append(question_type)
    elif question_type == 'Fill in the blanks':
        st.write('Fill in the blanks')
        question_params.append(question_type)
    
    #question_number
    question_number = st.text_input('Number of Items')
    
    #taxomy level
    taxonomy_level = st.selectbox(
    "Taxonomy Level",
    ("Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"),
    index=None,
    placeholder="Select taxonomy level...",
    )

    #difficulty level
    difficulty = st.selectbox(
    "Question Difficulty",
    ("Easy", "Medium", "Hard"),
    index=None,
    placeholder="Select difficulty level...",
    )

#Session creation
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["How may I help you?"]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

input_container = st.container()
#colored_header(label='', description='', color_name='blue-30')
response_container = st.container()


#generation of the response from the LLM
def generate_response(prompt):
  # Send prompt to chatbot and get response

  chatbot = hugchat.ChatBot(cookies=cookies.get_dict()) 

  full_prompt = "Given the context {}, generate five multiple choice questions together with their corresponding distractors and give the answer it is simplest way".format(prompt)
  response = chatbot.chat(full_prompt)
  return response

## Conditional display of AI generated responses as a function of user provided prompts
#printings
def response_ai(user_message):
    with response_container:
        if user_message:
            response = generate_response(user_message)
            st.session_state.past.append(user_message)
            st.session_state.generated.append(response)
            
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                st.write(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                st.write(st.session_state['generated'][i], key=str(i))

# Applying the user input box
with input_container:
    
    # User input
    additional_prompts = question_params()
    
    user_message = st.text_input("Enter your message:", key="input") # taking user provided prompt as input
    if st.button("Submit") and user_message != " ":
        response_ai(user_message)


