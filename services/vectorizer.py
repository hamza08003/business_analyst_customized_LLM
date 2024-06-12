from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from utils.config import OPENAI_API_KEY



# Function to vector embeddings of the text data and save to the vector store
def create_embeddings_and_vector_store(text_data):
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_texts(text_data, embedding=embeddings)
    # vector_store.save_local("vector_store")
    return embeddings, vector_store
