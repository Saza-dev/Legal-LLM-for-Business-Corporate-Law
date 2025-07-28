from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder

def get_contextual_prompt():

    contextualize_system_prompt = ( 
        "Using chat history and the latest user question, just reformulate question if needed and otherwise return it as is"
    )
    return ChatPromptTemplate.from_messages([
        ("system",contextualize_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

def get_assistant_prompt():
    system_prompt = (
    "You are an intelligent chatbot that can answer to business and coperate law in sri lanka, use the following context to answer the question. If you dont know the answer just say that you dont know."
    "\n\n"
    "{context}"
    )
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

def get_drafter_prompt():
    system_prompt = (
        "You are an Intelligent chatbot who can draft documents according to srilankan business and corporate law and based on the provided context. Apply the laws and rules in the context when drafting the documents. If you dont have the knowledge in the paticular area to draft the document say that you dont know. Give the Drafted document as output"
        "\n\n"
        "{context}"
    )
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

def get_compliance_prompt():
    system_prompt = (
    "You are an Intelligent chatbot when a user inputs the document you can identify the missing terms or non complient clauses based on the given context and help the user to fix those.If you dont have the knowledge in the paticular area to check the input say that you dont know."
    "\n\n"
    "{context}"
    )
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

def get_summary_prompts():
    chunks_prompt = """
        Please summarize the below content:
        Content: `{text}`
        summary:
        """
    final_prompt = """ 
        Provide the final summary of the entire content with these important points. 
        Add a Titile, Start the precise summary with an introduction and provide the summary in number points for the docs
        docs = {text} 
        """
    map_template = PromptTemplate(
        input_variables=["text"],
        template=chunks_prompt
    )
    combine_template = PromptTemplate(
        input_variables=["text"],
        template=final_prompt
    )
    return map_template, combine_template
