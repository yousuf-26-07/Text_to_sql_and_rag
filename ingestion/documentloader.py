from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
def load_document(file_path):
    if file_path.endswith("txt"):
        loader = TextLoader(file_path)
    elif file_path.endswith("pdf"):
        loader = PyPDFLoader(file_path)
    document = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=400,chunk_overlap=40)
    chunks = splitter.split_documents(document)
    return chunks

