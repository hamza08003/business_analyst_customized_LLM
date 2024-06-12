# utility functions


# Helper function to convert data to string
def data_to_str(data):
    return "".join(doc.page_content for doc in data)
