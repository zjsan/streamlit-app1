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
    ("Multiple Choice", "True or False", "Fill in the Blanks"),
    index=None,
    placeholder="Select question type...",
    )
        
    #condition for question type
    if question_type == 'Multiple Choice':
        st.write('Multiple choice')
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
        

#Session creation
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Here is the generated questions"]
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
            st.write(full_prompt)# Debugging
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
            st.write(full_prompt)# Debugging
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
            st.write(full_prompt)# Debugging
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
            st.write(full_prompt)  # Debugging

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
            st.write(full_prompt)  # Debugging

            response = chatbot.chat(full_prompt)
            return response
        
        else:
            return False 
  
  elif question_parameters[0] == 'Fill in the Blanks':
      
      if question_parameters[2] == 'Remembering':
          #prompt template for Fill in the Blanks
        # Generate `{num_questions}` fill-in-the-blank questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question.
        prompt = "Exam questions creation: Generate {} fill-in-the-blank question items at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy  based in this context: {} Ensure the blanks are clearly identified and essential to the question and has clear answers.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)
    
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
        st.write(full_prompt)  # Debugging
        response = chatbot.chat(full_prompt)
        return response 
      
      elif question_parameters[2] == 'Understanding':
        #prompt template for Fill in the Blanks
        # Generate `{num_questions}` fill-in-the-blank questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question.
        prompt = "Exam questions creation: Generate {} fill-in-the-blank question items at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy  based in this context: {} Ensure the blanks are clearly identified and essential to the question and has clear answers.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)
    
        #feeding sample data for the llm for optimization of responses
        few_shot_prompt = '''
                            For example: 

                            **Question:** Although both are forms of precipitation, rain and snow differ because _______ determines whether water vapor freezes into ice crystals or falls as liquid droplets.
        
                                *Answer: temperature
                        '''
                
        full_prompt = prompt + few_shot_prompt
        st.write(full_prompt)  # Debugging
        response = chatbot.chat(full_prompt)
        return response 
      
      elif question_parameters[2] == 'Applying':    
        #prompt template for Fill in the Blanks
        # Generate `{num_questions}` fill-in-the-blank questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question.
        prompt = "Exam questions creation: Generate {} fill-in-the-blank question items at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy  based in this context: {} Ensure the blanks are clearly identified and essential to the question and has clear answers.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)
    
        #feeding sample data for the llm for optimization of responses
        few_shot_prompt = '''
                            For example: 

                            **Question:**  If you want to increase the speed of a moving object, you would need to apply more _______. 
        
                                *Answer: force
                        '''
                
        full_prompt = prompt + few_shot_prompt
        st.write(full_prompt)  # Debugging
        response = chatbot.chat(full_prompt)
        return response
      
      else:

        #prompt template for Fill in the Blanks
        # Generate `{num_questions}` fill-in-the-blank questions at a `{difficulty_level}` difficulty level that test {taxonomy_level} knowledge in the area of {subject_area} (if applicable). Ensure the blanks are clearly identified and essential to the question.
        prompt = "Exam questions creation: Generate {} fill-in-the-blank question items at a {} difficulty level that is alignn with the {} cognitive level of bloom's taxonomy  based in this context: {} Ensure the blanks are clearly identified and essential to the question and has clear answers.".format(question_parameters[1],question_parameters[3],question_parameters[2],prompt)
        st.write(prompt)  # Debugging
        response = chatbot.chat(prompt)
        return response
          

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
        st.write(additional_prompts)#checking the index location of the additional promptsg

        if 'True or False' in additional_prompts and 'Remembering' in additional_prompts or 'Understanding' in additional_prompts:
            st.write('Good')
        else:
            st.write('Bad')
        
        user_message = st.text_input("Enter text context:", key="input") # taking user provided prompt as input
        if st.button("Submit") and user_message != " ":
            response_ai(user_message, additional_prompts)

if __name__ == "__main__":
    main()



