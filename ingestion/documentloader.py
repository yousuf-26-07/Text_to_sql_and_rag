from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_document(file_path):
    loader = TextLoader(file_path)
    document = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=400,chunk_overlap=40)
    chunks = splitter.split_documents(document)
    return chunks

chunks = load_document("document/sample.txt")
