from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith Tracking Tracking
langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")
if langsmith_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
langsmith_project = os.getenv("LANGCHAIN_PROJECT_OLLAMA")
if langsmith_project:
    os.environ["LANGCHAIN_PROJECT"] = langsmith_project

## prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user queries."),
    ("human", "Question: {question}")
])

def generate_response(question,engine,temperature,max_tokens):
    lmm=Ollama(model=engine, temperature=temperature, num_predict=max_tokens)
    output_parser=StrOutputParser()
    chain=prompt|lmm|output_parser
    answer=chain.invoke({"question":question})
    return answer

## Title of the app
st.title("Enhanced Q&A Chatbot with Ollama")

## sidebar for settings
st.sidebar.title("Settings")
engine=st.sidebar.selectbox("Select Model",["gemma:2b"])

temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

## Main chat interface for user interaction
st.write("Go Ahead and Ask Your Question!")
user_input=st.text_input("Enter your question:")
if user_input:
    response=generate_response(user_input,engine,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please enter a question")
    