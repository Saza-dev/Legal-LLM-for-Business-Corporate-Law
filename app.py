import streamlit as st
from streamlit_option_menu import option_menu
from chains import assistant_chain, drafter_chain, compliance_chain, summarizer_chain

st.set_page_config(page_title="Legal Assistant", layout="wide")

selected = option_menu(
    menu_title=None,
    options=["Assistant", "Drafter", "Compliance Checker", "Summarizer"],
    icons=["robot", "envelope", "check", "body-text"],
    orientation="horizontal"
)

if selected == "Assistant":
    assistant_chain.run()
elif selected == "Drafter":
    drafter_chain.run()
elif selected == "Compliance Checker":
    compliance_chain.run()
elif selected == "Summarizer":
    summarizer_chain.run()
