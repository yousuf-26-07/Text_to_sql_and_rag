import streamlit as st
import requests

st.title("Text to SQL agent")

question = st.text_input("Ask question about your data")


if st.button("Ask"):

    response = requests.post(
        "http://localhost:8000/query",
        json={"question": question}
    )

    data = response.json()

    st.write("Answer:")
    st.success(data.get("answer", ""))

    st.write("Source:", data.get("source", ""))

    if data.get("sql"):
        st.write("SQL Query:")
        st.code(data["sql"])

    if data.get("sources"):
        st.write("Sources:")
        for s in data["sources"]:
            st.code(s)
    