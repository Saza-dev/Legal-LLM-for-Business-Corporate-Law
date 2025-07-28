import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain

from config.setup import llm
from utils.prompts import get_summary_prompts
from utils.pdf_utils import load_pdf

def run():
    st.title("Summarizer")
    st.write("Upload a legal/business document (PDF) to summarize.")

    doc = st.file_uploader("Upload a PDF", type="pdf")

    if doc is not None:
        pages = load_pdf(doc)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(pages)

        map_prompt, combine_prompt = get_summary_prompts()
        summary_chain = load_summarize_chain(
            llm=llm,
            chain_type="map_reduce",
            map_prompt=map_prompt,
            combine_prompt=combine_prompt
        )

        output = summary_chain.invoke(chunks)
        st.write(output["output_text"])
