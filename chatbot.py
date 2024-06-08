# chatbot.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"

## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please response to the user queries"),
        ("user", "Question:{question}")
    ]
)

## streamlit framework
st.title('Sukoon Chatbot')
input_text = st.text_input("Enter your Query:")

# ollama Tinydolphin LLm
llm = Ollama(model="medllama2:7b")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser    

if input_text:
    with st.spinner('Loading...!'):
        response = chain.invoke({"question": input_text})
    st.write(response)