import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

config = {"configurable": {"session_id": "abc123"}}
selected_model = 'ChatGPT 4o Mini'
load_dotenv()

st.markdown(" #### Programming Language Expert 💻 ")

if "store" not in st.session_state:
    st.session_state.store = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "st_openai_api_key" not in st.session_state:
    st.session_state.st_openai_api_key = None

if "st_anthropic_api_key" not in st.session_state:
    st.session_state.st_anthropic_api_key = None

    
with st.sidebar:
    st.title('')
    # Sidebar with a dropdown select box
    st.sidebar.header("Available LLM Model")
    options = ["ChatGPT 4o Mini", "Anthropic Sonnet 3.5"]
    company_options = ["OpenAI", "Anthropic"]
    default_index = 0
    selected_company = st.sidebar.selectbox("Choose Company:", company_options,index=default_index)
    
    if selected_company=="OpenAI":
        model_options = ['ChatGPT 4o Mini','ChatGPT 4o']
        default_index = 0
        selected_model = st.sidebar.selectbox("Choose model:", model_options,index=default_index)
        model_map = {
            'ChatGPT 4o Mini':'gpt-4o-mini',
            'ChatGPT 4o':'gpt-4o'
            }
        selected_model = model_map[selected_model]
    
    if selected_company=="Anthropic":
        model_options = ['Claude 3.5 Sonnet','Claude 3 Opus','Claude 3 Haiku']
        default_index = 0
        selected_model = st.sidebar.selectbox("Choose model:", model_options,index=default_index)
        model_map = {
            'Claude 3.5 Sonnet':'claude-3-5-sonnet-20240620',
            'Claude 3 Opus':'claude-3-opus-20240229',
            'Claude 3 Haiku':'claude-3-haiku-20240307'
            }
        selected_model = model_map[selected_model]
    
    
    if selected_company=="OpenAI":
        if os.getenv('OPENAI_API_KEY') is None:
            st.session_state.st_openai_api_key = st.text_input("Enter API Key", type="password")
            try:
                llm = ChatOpenAI(
                    model=selected_model,
                    temperature=0.7,
                    max_tokens=4096,
                    timeout=None,
                    max_retries=2,
                    api_key=st.session_state.st_openai_api_key
                )
            except:
                st.warning('Invalid API key.')
                st.stop()

        else:
            llm = ChatOpenAI(
                model=selected_model,
                temperature=0.7,
                max_tokens=4096,
                timeout=None,
                max_retries=2,
            )
    
    elif selected_company=="Anthropic":
        if os.getenv('ANTHROPIC_API_KEY') is None:
            st.session_state.st_anthropic_api_key = st.text_input("Enter API Key", type="password")
            try:
                llm = ChatAnthropic(
                    model=selected_model,
                    temperature=0.7,
                    max_tokens=4096,
                    timeout=None,
                    max_retries=2,
                    top_p=0.9,
                    top_k=40,
                    api_key=st.session_state.st_anthropic_api_key
                )
            except:
                st.warning('Invalid API key.')
                st.stop()
        else:
            llm = ChatAnthropic(
                model=selected_model,
                temperature=0.7,
                max_tokens=4096,
                timeout=None,
                max_retries=2,
                top_p=0.9,
                top_k=40,
            )

    if st.button('Clear Chat'):
            st.session_state.messages = []
            st.session_state.store = {}
            st.rerun()
        
system_prompt = """
You are a highly skilled computer engineer and programming language expert.
Your primary responsibilities include writing, debugging, and optimizing programming code across a range of languages.
Your coding practices are characterized by:
    Expertise in Multiple Languages: You possess in-depth knowledge and proficiency in various programming languages, including but not limited to Python, Java, C++, JavaScript, and others.
    Well-Structured Code: Your code is always well-organized and follows best practices for readability and maintainability.
        You ensure that your code is modular, clean, and adheres to coding standards.
    Detailed Comments: You provide comprehensive comments in your code, explaining the functionality and logic behind each section.
        This includes clarifying complex algorithms, detailing the purpose of functions, and describing the flow of the code.
    Technical Documentation: You produce well-structured technical documents that accompany your code.
        These documents are written in clear, simple language but are thorough and cover all necessary details about the code, including its design, functionality, usage, and any relevant implementation notes.

Your goal is to assist users by providing accurate, efficient, and well-documented code and documentation.
Always ensure that your responses are tailored to the user’s needs, whether they are seeking help with a specific coding problem, optimization suggestions, or understanding the details of a technical document.
"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

    
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

chain = qa_prompt | llm

conversational_rag_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(f"Hi! I am {selected_model}. How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        stream = conversational_rag_chain.stream({"messages":prompt}, config=config)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
