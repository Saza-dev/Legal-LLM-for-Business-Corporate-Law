import streamlit as st
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from config.setup import retriever, llm
from utils.prompts import get_compliance_prompt
from utils.pdf_utils import load_pdf

def run():
    st.title("Compliance Checker")
    st.write("Upload a legal/business document (PDF) to check for compliance gaps.")

    doc = st.file_uploader("Upload a PDF", type="pdf")

    if doc is not None:
        documents = load_pdf(doc)
        user_input = "\n".join([page.page_content for page in documents])

        prompt = get_compliance_prompt()
        qa_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, qa_chain)

        response = rag_chain.invoke({"input": user_input})
        st.write(response["answer"])
