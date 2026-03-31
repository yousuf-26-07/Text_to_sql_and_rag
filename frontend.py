import streamlit as st
import requests

st.title("Text to SQL Agent")

uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

if uploaded_file is not None:
    if st.button("Upload Document"):
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue())
        }

        res = requests.post(
            "http://localhost:8000/upload",
            files=files
        )

        if res.status_code == 200:
            st.success("File uploaded successfully")
        else:
            st.error("Upload failed")


question = st.text_input("Ask question about your data")

if st.button("Ask"):
    response = requests.post(
        "http://localhost:8000/query",
        json={"question": question}
    )

    data = response.json()

    st.write("Answer:")
    st.success(data.get("answer", ""))

    if data.get("sql"):
        st.write("SQL Query:")
        st.code(data["sql"])

    # if data.get("sources"):
    #     st.write("Sources:")
    #     for s in data["sources"]:
    #         st.code(s)