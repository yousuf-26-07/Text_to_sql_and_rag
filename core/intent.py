def classify_intent(question: str):

    question = question.lower()

    sql_keywords = [
        "film", "actor", "customer", "payment",
        "count", "total", "sum", "number",
        "list", "show", "top"
    ]

    for word in sql_keywords:
        if word in question:
            return "sql"

    return "rag"