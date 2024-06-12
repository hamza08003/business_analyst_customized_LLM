from utils.data_conversion import data_to_str
from langchain_community.utilities import ApifyWrapper
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.config import APIFY_API_KEY



# Function to crawl the entire given website, get the content and split it into chunks
def process_website(url):
    apify = ApifyWrapper(api_key=APIFY_API_KEY)
    loader = apify.call_actor(
        actor_id="apify/website-content-crawler",
        run_input={
            "startUrls": [{"url": url}],
            "crawlerType": "playwright:adaptive",
        },
        dataset_mapping_function=lambda item: Document(page_content=item["text"] or "", metadata={"source": item["url"]})
    )
    data = loader.load()
    text = data_to_str(data)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=70)
    chunks = text_splitter.split_text(text)
    return chunks
