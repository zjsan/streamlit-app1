import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from dotenv import dotenv_values

st.set_page_config(page_title="🤗💬 Cognicraft")

secrets = dotenv_values('hf.env')

#credentials
hf_email = secrets['EMAIL']
hf_pass = secrets['PASS']

cookie_path_dir = "./cookies"
sign = Login(hf_email, hf_pass)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)


with st.sidebar:
    st.title('CogniCraft')
    st.markdown('''
    ## About
    This app is a LLM-powered exam question generator built using:
    - [Streamlit](<https://streamlit.io/>)
    - [HugChat](<https://github.com/Soulter/hugging-chat-api>)
     - [OpenAssistant/oasst-sft-6-llama-30b-xor](<https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor>) LLM model
    ''')

def question_params():


    question_params = []
    #question_params_length = len(question_params)

    #question type
    question_type = st.selectbox(
    "Question Type",
    ("Multiple Choice", "True or False", "Fill in the blanks","Matching Type"),
    index=None,
    placeholder="Select question type...",
    )
        
    #condition for question type
    if question_type == 'Multiple Choice':
        st.write('Multiple choice')
        question_params.append(question_type)  
    elif question_type == 'True or False':
        st.write('True or False')
        question_params.append(question_type)
    elif question_type == 'Fill in the blanks':
        st.write('Fill in the blanks')
        question_params.append(question_type)
    elif question_type == 'Matching Type':
        st.write('Matching Type')
        question_params.append(question_type)
    else:
        st.write('Select Question type') 
    
    #question_number
    question_number = st.text_input('Number of Items')
    question_params.append(question_number)#add number of items
    
    #taxomy level
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
        

#Session creation
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["How may I help you?"]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

input_container = st.container()
#colored_header(label='', description='', color_name='blue-30')
response_container = st.container()


#generation of the response from the LLM
def generate_response(prompt,question_parameters):
  # Send prompt to chatbot and get response

  chatbot = hugchat.ChatBot(cookies=cookies.get_dict()) 

  st.write(question_parameters)
  st.write(question_parameters[3],question_parameters[2],question_parameters[1])
  #testing prompts parameters
  #added prompt templates for the ai to use in the question generation
  #addional_prompts[0] = Question Type
  #additional_prompts[1] = Question Number
  #additional_prompts[2] = Taxonomy Level
  #additional_prompts[3] = Difficulty level
  
  #there are errors in the full prompt
  #full_prompt does not execute well - problem in the string formatting
  if question_parameters[0] == 'Multiple Choice':
        
        st.write(question_parameters)

        #prompt template for multiple choice
        #Generate `{num_questions}` multiple choice questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure each question has at least 4 answer choices and a clear answer key.
        full_prompt = "Generate {} multiple choice questions at a {} difficulty level that test {} knowledge based on this context: {} Ensure each question has at least 4 answer choices and a clear answer key".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)
        st.write(full_prompt)# Debugging

        response = chatbot.chat(full_prompt)
        return response

  elif question_parameters[0] == 'True or False':
        
        # Generate `{num_questions}` True or False statements at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable)
        full_prompt = "Generate {} True or False statements at a {} difficulty level that test {} knowledge based in this context: {} Ensure each question has a clear answer".format(question_parameters[0], question_parameters[3], question_parameters[2],prompt)
        st.write(full_prompt)  # Debugging
        
        response = chatbot.chat(full_prompt)
        return response
  
  elif question_parameters[0] == 'Fill in the Blanks':
        full_prompt = "Generate a fill-in-the-blank question with a blank space at the most appropriate location. The question should target {} based on this context: {}. Have a {} difficulty level and number of items of {}".format(question_parameters[2], 
                       prompt, question_parameters[3], question_parameters[1])
        st.write(full_prompt)  # Debugging
        # response = chatbot.chat(full_prompt)
        # return response
  
  elif question_parameters[0] == 'Matching Type':
        full_prompt = "Generate a matching type question where {} items need to be matched, assessing {} based on this context {}. Ensure the difficulty level is {}.".format(question_parameters[1], 
                       question_parameters[2], prompt, question_parameters[3])
        st.write(full_prompt)  # Debugging
        # response = chatbot.chat(full_prompt)
        # return response
  else:
        st.write('Please Check your inputs')

## Conditional display of AI generated responses as a function of user provided prompts
#printings
def response_ai(user_message, additional_prompts):
    with response_container:
        if user_message:
            response = generate_response(user_message,additional_prompts)
            st.session_state.past.append(user_message)
            st.session_state.generated.append(response)
            
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                st.write(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                st.write(st.session_state['generated'][i], key=str(i))

def main():
    # Applying the user input box
    with input_container:
        # User input
        additional_prompts = list(question_params())
        print(additional_prompts)   
        st.write(additional_prompts)#checking the index location of the additional prompts
        
        user_message = st.text_input("Enter text context:", key="input") # taking user provided prompt as input
        if st.button("Submit") and user_message != " ":
            response_ai(user_message, additional_prompts)

if __name__ == "__main__":
    main()


