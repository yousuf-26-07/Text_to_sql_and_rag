from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

retriever = None

def create_vector_db(chunks):
    global retriever
    vector_db = FAISS.from_documents(chunks, embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k":3})

def get_retriever():
    return retriever