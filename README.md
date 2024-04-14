
# Unofficial Thesis Project Repository(CogniCraft Development Stage)

CogniCraft a smart exam question generation that leverages the use of artificial intelligence with alignment of the concept of Revised Bloom's Taxonomy.

The application is running using the streamlit framework utilizing api calls to the Hugchat API powered by the OpenAssistant/oasst-sft-6-llama-30b-xor LLM model.



## API Reference


```http
 hugchat api - https://github.com/Soulter/hugging-chat-api
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| EMAIL and PASS | `string` | **Required**. API key |



## Installation

Clone the repository

```bash
  https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository?tool=desktop
```

Streamlit
```
pip install streamlit
```

Hugchat
```
pip install hugchat
```

dotenv
```
pip install python-dotenv
```
## Documentation

The project is running in a virtual environment 
```
https://code.visualstudio.com/docs/python/environments
```

Python version: Python 3.10.7

IDE: Visual Studio Code

Streamlit: https://streamlit.io/

hf.env - same directory level with test.py
       - change contents of email and password based in the huggingface credentials

## Launch

To launch the application simply the following command:
```

streamlit run test.py 
```

## Features 

    1. Generate Questions Based on the question type
    2. Intuitive and simple User Interface
    3. Working question parameters
    4. Integration of the concept of Revised Bloom's  Taxonomy in the question generation
    5. Flexible Web Layout


## Errors and Bugs

    1. Additional Testing in the buttons and Inout fields
    2. Further assurance of the generated Questions
    3. Web layout and Design
    4. Implementation of further features
    5. Bug in the text input
    6. Further checkin in the model response

## Need To Implement
    1. PDF Upload 
    2. Login Credentials for Users
    3. Database if needed 
    4. Chat History
    5. Multiple Pages and Layouts 
    6. Redesign of Web Components
    7. Landing Page
    8. Login Page - Redirect to huggingface
