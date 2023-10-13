# Desc: a simple streamlit langchain chat interface, that uses the vectordb to retrieve documents
# Maybe build something like this: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps#build-a-chatgpt-like-app

import streamlit as st
import src.llm as llm

qa = llm.create_llm() 

st.title("LangChain Chat Interface")

user_input = st.text_input("You:", "")

if user_input:
    response = qa.run(user_input)
    st.text_area("40kBot:", response)


