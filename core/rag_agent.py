from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from ingestion.documentloader import chunks
import google.generativeai as genai 
import time

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

model = genai.GenerativeModel("gemini-2.5-flash")

vector_db = FAISS.from_documents(chunks, embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k":3})

def run_rag_agent(question):
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""You are a helpful ai assitant 
    Use the context below to answer the question clearly and concisely.
    Limit your answer to 50 words.
    
    Context: {context}
    question: {question}
    Answer :
    """
    response = model.generate_content(prompt)
    time.sleep(2)
    return {
        "answer": response.text.strip(),
        "sources": [doc.page_content[:150] for doc in docs]
    }



