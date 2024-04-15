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
    st.title("CogniCraft - Smart Exam Question Generation With AI and Bloom's Taxonomy")
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
    ("Multiple Choice", "True or False", "Fill in the Blanks","Matching Type"),
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
    elif question_type == 'Fill in the Blanks':
        st.write('Fill in the Blanks')
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
            st.write(full_prompt)# Debugging
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
            st.write(full_prompt)# Debugging
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
            st.write(full_prompt)# Debugging
            response = chatbot.chat(full_prompt)
            return response
        
        else:
            #Generate `{num_questions}` multiple choice questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure each question has at least 4 answer choices and a clear answer key.
            prompt = "Exam questions creation: Generate {} multiple choice questions at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy based on this context: {} Ensure each question has at least 4 answer choices and a clear answer key. The format of the questions must be like a formal exam paper.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)

            full_prompt = prompt + few_shot_prompt
            st.write(full_prompt)# Debugging
            response = chatbot.chat(full_prompt)
            return response
        
  elif question_parameters[0] == 'True or False':
        
        #prompt template for True or False
        # Generate `{num_questions}` True or False statements at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable)
        full_prompt = "Exam questions creation: Generate {} statements at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy based in this context: {} Ensure each question has a clear answer".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)
        st.write(full_prompt)  # Debugging

        response = chatbot.chat(full_prompt)
        return response
  
  elif question_parameters[0] == 'Fill in the Blanks':
        
        #prompt template for Fill in the Blanks
        # Generate `{num_questions}` fill-in-the-blank questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question.
        full_prompt = "Exam questions creation: Generate {} fill-in-the-blank question items at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy  based in this context: {} Ensure the blanks are clearly identified and essential to the question and has clear answers.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)
        st.write(full_prompt)  # Debugging

        response = chatbot.chat(full_prompt)
        return response 
  
    
  elif question_parameters[0] == 'Matching Type':
      
      #prompt template for Matching Type
      full_prompt = "Exam questions creation: Generate a matching type question where {} items need to be matched, assessing {} cognitive level of bloom's taxonomy based on this context {}. Ensure the difficulty level is {}. Create two list, one for the questions and one for the choices, questions should be in a number format".format(question_parameters[1], question_parameters[2],prompt,question_parameters[3])
      st.write(full_prompt)  # Debugging

      response = chatbot.chat(full_prompt)
      return response 
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


