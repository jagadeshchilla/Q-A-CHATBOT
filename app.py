import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith Tracking Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

## prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user queries."),
    ("human", "Question: {question}")
])

def generate_response(question, api_key, llm_model, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm_model, temperature=temperature, max_tokens=max_tokens, api_key=api_key)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

## Title of the app
st.title("Enhanced Q&A Chatbot with OpenAI")

## sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("OpenAI API Key",type="password")

## Drop down for model selection
llm_model=st.sidebar.selectbox("Select Model",["gpt-4o-mini","gpt-4-turbo","gpt-3.5-turbo"])
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

## Main chat interface for user interaction

st.write("Go Ahead and Ask Your Question!")
user_input=st.text_input("Enter your question:")
if user_input:
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
    else:
        response=generate_response(user_input,api_key,llm_model,temperature,max_tokens)
        st.write(response)
else:
    st.write("Please enter a question")