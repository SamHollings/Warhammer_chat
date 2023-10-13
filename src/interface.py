# Desc: a simple streamlit langchain chat interface, that uses the vectordb to retrieve documents

import streamlit as st
import src.llm as llm

qa = llm.create_llm() 

st.title("LangChain Chat Interface")

user_input = st.text_input("You:", "")

if user_input:
    response = qa.run(user_input)
    st.text_area("40kBot:", response)


