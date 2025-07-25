import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

# loading env variables
load_dotenv()

# hugging face embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# LLM from GROQ
llm = ChatGroq(model="llama3-70b-8192")

# Loading VectorStore
vectorstore = Chroma(persist_directory="chroma_legal_db", embedding_function=embedding_model)

# Retriver
retriever = vectorstore.as_retriever()

# Streamlit navigations
selected = option_menu(
        menu_title=None,
        options=["Assistant","Drafter","Compliance Checker","Summarizer"],
        icons = ["robot",'envelope','check','body-text'] ,# boostrap icons
        default_index=0, # default selected
        orientation='horizontal',
)

# Assistant
if selected == "Assistant":

    # History aware Retriver
    contextualize_system_prompt = ( 
        "Using chat history and the latest user question, just reformulate question if needed and otherwise return it as is"
    )

    contextualize_prompt = ChatPromptTemplate.from_messages(
        [
            ("system",contextualize_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human","{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm,retriever,contextualize_prompt
    )

    # Prompts
    system_prompt = (
    "You are an intelligent chatbot that can answer to business and coperate law in sri lanka, use the following context to answer the question. If you dont know the answer just say that you dont know."
    "\n\n"
    "{context}"
    )

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system",system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human","{input}"),
        ]
    )

    # chains
    qa_chain = create_stuff_documents_chain(llm,chat_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever,qa_chain)


    # Managing History
    store = {}

    def get_session_history(session_id:str)-> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    # Streamlit UI
    st.title("Assistant")
    st.write(f"You have selected Assistant. Please feel free to ask our assistant any questions you may have regarding Business and Case Law in Sri Lanka.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Past messages
    for msg in st.session_state.messages:
        with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
            st.markdown(msg.content)

    prompt = st.chat_input("Ask a legal question...")

    if prompt:
        # Show user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))

        # Invoke the RAG chain with session id
        response = conversational_rag_chain.invoke(
            {"input": prompt},
            config={"configurable": {"session_id": "001"}} 
        )

        answer = response["answer"]

        # Show assistant response
        st.chat_message("assistant").markdown(answer)
        st.session_state.messages.append(AIMessage(content=answer))

# Drafter
if selected == "Drafter":
    # Prompts
    system_prompt = (
        "You are an Intelligent chatbot who can draft documents according to srilankan business and corporate law and based on the provided context. Apply the laws and rules in the context when drafting the documents. If you dont have the knowledge in the paticular area to draft the document say that you dont know. Give the Drafted document as output"
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",system_prompt),
            ("human","{input}"),
        ]
    )

    # question answer chain
    qa_chain = create_stuff_documents_chain(llm,prompt)

    # rag chain
    rag_chain = create_retrieval_chain(retriever,qa_chain)

    # streamlit input 
    draft_input = st.text_input("Explain what kind of draft you need ?")

    if draft_input:
        # Invoking RAG chain
        response = rag_chain.invoke({"input":draft_input})

        # Output the answer
        st.write(response["answer"])



if selected == "Compliance Checker":
    st.title(f"You have selected {selected}")
if selected == "Summarizer":
    st.title(f"You have selected {selected}")
