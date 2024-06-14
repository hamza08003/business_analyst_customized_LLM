from langchain_openai import OpenAI
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from utils.config import OPENAI_API_KEY
from dotenv import load_dotenv
import os


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)


# Function to query the Gemini model given the prompt
def query_gemini_model(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.candidates[0].content.parts[0].text.replace("*", "")
    except ResourceExhausted as e:
        print("API quota exceeded. Please try again later.")
        return


# Function to query the model with the question related to the data
def query_gpt_model(prompt):
    openai_llm = OpenAI(api_key=OPENAI_API_KEY)
    response = openai_llm.invoke(prompt)
    return response
