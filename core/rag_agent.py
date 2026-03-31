from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai 
import time
from core.utils import retry
from ingestion.pdf_ingestion import get_retriever


model = genai.GenerativeModel("gemma-3-1b-it")



@retry
def call_llm(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

def run_rag_agent(question):
    retriever = get_retriever()
    if retriever is None:
        return {"answer": "No document has been uploaded yet. Please upload a file first.", "sources": []}
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""You are a helpful ai assitant 
    Use the context below to answer the question clearly and concisely.
    Give answer in bullet points if possible.
    Limit your answer to 500 words.
    
    Context: {context}
    question: {question}
    Answer :
    """
    answer = call_llm(prompt)
    time.sleep(2)
    return {
        "answer": answer,
        "sources": [doc.page_content[:150] for doc in docs]
    }



