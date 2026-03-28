import google.generativeai as genai
from data.database import run_query, get_schema
from config import GEMINI_MODEL
import time

model = genai.GenerativeModel(GEMINI_MODEL)

def generate_sql(question):
    schema = get_schema()

    prompt = f"""You are an expert SQL generator.

STRICT RULES:
1. Use ONLY tables and columns from schema
2. DO NOT invent column names
3. ALWAYS use correct joins when multiple tables are needed
4. If column not present, return: NOT_POSSIBLE
5. Output ONLY the raw SQL query, no markdown, no explanation

Schema: {schema}
Question: {question}
SQL:
"""
    response = model.generate_content(prompt)
    time.sleep(1)

    sql = response.text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql


def format_rows(question, rows):
    """Format SQL result rows into a human-readable answer without using an LLM."""
    if not rows:
        return "No results found in the database."

    # Flatten single-column results into a neat numbered list
    if len(rows[0]) == 1:
        items = "\n".join(f"{i+1}. {row[0]}" for i, row in enumerate(rows))
        return f"Here are the results:\n{items}"

    # Multi-column: return as a simple table-like string
    lines = []
    for i, row in enumerate(rows):
        lines.append(f"{i+1}. " + " | ".join(str(v) for v in row))
    return "Here are the results:\n" + "\n".join(lines)


def run_sql_agent(question):
    sql = generate_sql(question)

    try:
        rows = run_query(sql)

        return {
            "answer": format_rows(question, rows),
            "sql": sql,
            "result": rows
        }

    except Exception as e:
        return {
            "answer": f"SQL Error: {str(e)}",
            "sql": sql
        }