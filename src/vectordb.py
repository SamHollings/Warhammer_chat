import toml
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.schema.document import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from tqdm import tqdm

config = toml.load('config.toml')

PERSIST_DIRECTORY = config['vectordb']["persist_directory"]
EMBEDDING_MODEL = config['vectordb']["embedding_model"]

def create_vectorstore(persist_directory=PERSIST_DIRECTORY, embedding_model=EMBEDDING_MODEL, chunk_size=1000):
    embedding = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL) #embedding_functions.DefaultEmbeddingFunction()
    vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding)

    return vectorstore