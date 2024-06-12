from langchain_openai import OpenAI
from utils.config import OPENAI_API_KEY


# Function to query the model with the question related to the data
def query_model(prompt):
    openai_llm = OpenAI(api_key=OPENAI_API_KEY)
    response = openai_llm.invoke(prompt)
    return response
