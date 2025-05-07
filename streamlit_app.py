import streamlit as st
import requests

st.title("Dialogflow Chatbot")

user_query = st.text_input("Enter your message:")

if st.button("Send"):
    if user_query.strip():
        response = requests.post(
            "http://localhost:8000/chat",
            json={"query": user_query}
        )
        if response.status_code == 200:
            st.markdown("**Bot:** " + response.json().get("response", "No response."))
        else:
            st.error("Failed to reach the chatbot backend.")
