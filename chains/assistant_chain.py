import streamlit as st
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

from config.setup import retriever, llm
from utils.prompts import get_contextual_prompt, get_assistant_prompt
from components.session_manager import get_session_history

def run():
    st.title("Assistant")
    st.write("Ask any legal question related to Sri Lankan business or corporate law.")

    contextualize_prompt = get_contextual_prompt()
    chat_prompt = get_assistant_prompt()

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_prompt
    )

    qa_chain = create_stuff_documents_chain(llm, chat_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
            st.markdown(msg.content)

    prompt = st.chat_input("Ask a legal question...")

    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))

        response = conversational_rag_chain.invoke(
            {"input": prompt},
            config={"configurable": {"session_id": "001"}}
        )

        answer = response["answer"]
        st.chat_message("assistant").markdown(answer)
        st.session_state.messages.append(AIMessage(content=answer))
