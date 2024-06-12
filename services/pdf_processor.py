from utils.data_conversion import data_to_str
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile



# Function to process the uploaded PDF file and split it into chunks
def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        tmpfile.write(uploaded_file.getvalue())
        tmpfile_path = tmpfile.name

    loader = PyMuPDFLoader(tmpfile_path)
    data = loader.load()
    text = data_to_str(data)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=70)
    chunks = text_splitter.split_text(text)
    return chunks
