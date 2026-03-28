import google.generativeai as genai

model = genai.GenerativeModel("gemma-3-1b-it")

def classify_query_llm(query):

    prompt = f"""
Classify the user query into one of these categories:
- rag → questions about documents, PDFs, context
- sql → database queries, tables, rows, data retrieval
- general → normal questions

Return ONLY one word: rag or sql or general

Query: {query}
Answer:
"""

    result = model.generate_content(prompt)
    result = result.text.strip().lower()

    if "sql" in result:
        return "sql"
    elif "rag" in result:
        return "rag"
    else:
        return "general"

def classify_query(query):
    q = query.lower()
    if any(word in q for word in ["select","table","sql","database","row","column"]):
        return "sql"
    elif any(word in q for word in ["pdf","document","context","file"]):
        return "rag"
    else:
        return classify_query_llm(query)
    
    