import google.generativeai as genai
from data.database import run_query,get_schema
import time

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_sql(question):
    schema = get_schema()
    
    prompt = f"""You are helpful AI assistant and a expert in sql query generator
    with the scheme provide and the question generate the exact correct SQL query
    Schema: {schema}
    question: {question}
    Answer :
    """
    response = model.generate_content(prompt)
    time.sleep(2)
    
    sql = response.text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def run_sql_agent(question):

    sql = generate_sql(question)

    try:
        rows = run_query(sql)

        context = str(rows)

        prompt = f"""
You are a data analyst.

Given the SQL result below, answer the question in a natural, user-friendly way.

Question:
{question}

SQL Result:
{context}

Answer:
"""

        response = model.generate_content(prompt)

        return {
            "answer": response.text.strip(),
            "sql": sql,
            "result": rows
        }

    except Exception as e:
        return {
            "answer": f"SQL Error: {str(e)}",
            "sql": sql
        }