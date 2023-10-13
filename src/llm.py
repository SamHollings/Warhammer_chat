import os
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatAnthropic
import src.vectordb as vectordb


def create_llm():
    vectorstore = vectordb.create_vectorstore()

    llm = ChatAnthropic(anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"))

    retriever = vectorstore.as_retriever(search_kwargs={"k":4})
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff",retriever=retriever)

    return qa


# question = "From the provided context, can you write a paragraph describing the greatest acheivements of the emperor"

# answer = qa.run(question)
# print(answer)
