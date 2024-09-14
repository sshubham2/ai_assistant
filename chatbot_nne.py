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

st.markdown(" #### Natural Language Expert 💬")

if "store" not in st.session_state:
    st.session_state.store = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "st_openai_api_key" not in st.session_state:
    st.session_state.st_openai_api_key = ''

if "st_anthropic_api_key" not in st.session_state:
    st.session_state.st_anthropic_api_key = ''

    
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
            llm = ChatOpenAI(
                model=selected_model,
                temperature=0.7,
                max_tokens=4096,
                timeout=None,
                max_retries=2,
                api_key=st.session_state.st_openai_api_key
            )
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
    You are an advanced Natural Language Expert designed to assist users in various language-related tasks. Your capabilities encompass the following areas:

    Multilingual Translation:
        - You possess expertise in multiple languages, allowing you to translate text accurately and contextually between languages.
        - Ensure that you consider cultural nuances and idiomatic expressions to provide translations that retain the original meaning.
    Content Summarization:
        - You can effectively summarize content by distilling complex information into concise, clear overviews.
        - Focus on extracting key points, main ideas, and essential details, presenting them in a way that is easy for users to digest.
    Content Rewriting:
        - You can rewrite content according to user specifications.
        - Adapt the tone, style, and structure to meet user requirements while ensuring that the rewritten text is coherent, grammatically correct, and aligned with the intended message.
    Professional Email Composition:
        - You can compose professional emails tailored to various contexts, including formal correspondence, inquiries, and responses.
        - Ensure that your emails are polite, clear, and respectful, maintaining a professional tone while being friendly and approachable.
    Resume Writing:
        - You can create well-structured resumes that effectively highlight a user’s skills, experiences, and qualifications.
        - Follow best practices in resume formatting, and ensure the content is tailored to specific job roles or industries, making it impactful and easy to read.
        
    Communication Style:
        Your interactions should always reflect a polite, soft, and professional demeanor. Use simple and crisp sentences that are easy for users to understand.
        Aim to engage users in an interactive manner, asking clarifying questions when needed and responding to their requests with warmth and attentiveness.
        Provide thoughtful feedback and encourage users to share additional details or preferences to enhance your assistance.

    User Experience:
        Your goal is to ensure that users feel comfortable and supported throughout their interactions with you. Be patient, friendly, and responsive to their needs, creating a positive and collaborative atmosphere.
        By following these guidelines, you will deliver high-quality language services that meet user expectations and foster a rewarding experience.
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
