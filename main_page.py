import streamlit as st

home_page = st.Page("home_page.py", title="Home", icon="🏚️")
programming_language_expert = st.Page("chatbot.py", title="Programming Language Expert", icon="💻")
natural_languag_expert = st.Page("chatbot_nne.py", title="Natural Language Expert", icon="💬")

pg = st.navigation([home_page, programming_language_expert, natural_languag_expert])
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout='wide')

pg.run()