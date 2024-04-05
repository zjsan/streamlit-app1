import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

st.set_page_config(page_title="🤗💬 Cognicraft")


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

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm HugChat, How may I help you?"]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

input_container = st.container()
#colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User input
## Function for taking user provided prompt as input
# Function to get user input text
def get_text():
    input_text = st.text_input("Enter text:", key="input")
    return input_text

# Function to generate multiple-choice question with distractors
def generate_question(text):
    prompt1 = "Generate a multiple-choice question with distractors with this given text: "
    question = prompt1 + text
    # Add your code to generate the multiple-choice question with distractors here
    return question

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    # Create your ChatBot

    #chatbot = hugchat.ChatBot(cookies=cookies.get_dict()) 
    #response = chatbot.chat(prompt)
    return "This is a dummy response generated for the prompt: " + prompt

## Applying the user input box
with input_container:
    # Generate question
    # Get user input text
    user_input = get_text() 
    if user_input:
        question = generate_question(user_input)
        st.write(question)
        response = generate_response(question)
        st.write(response)
    else:
        st.write("Please provide text input.")


## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            st.write(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            st.write(st.session_state['generated'][i], key=str(i))