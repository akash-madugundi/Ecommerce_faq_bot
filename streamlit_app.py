import streamlit as st
import requests

# Set up FastAPI server URL (replace with your local or deployed FastAPI server URL)
FASTAPI_URL = "http://localhost:8000"  # Replace with your FastAPI server URL

# Title and description of the Streamlit app
st.title("Ecommerce Chatbot")
st.markdown("""
    Welcome to the Ecommerce Chatbot! 
    Type your query below, and the bot will respond.
""")

# User input for the query
user_input = st.text_input("Your Query:")

# When the user submits a query
if st.button("Send"):
    if user_input:
        # Prepare the payload for the request
        payload = {
            "queryResult": {
                "intent": {
                    "displayName": "order.related"  # Modify this for other intents as needed
                },
                "parameters": {
                    "food-item": user_input  # You can modify this as per the expected parameters
                },
                "outputContexts": [{
                    "name": "projects/ecommerce-faq-dpfu/agent/sessions/user-123456:outputContexts",
                    "parameters": {}
                }]
            }
        }
        
        # Send the request to FastAPI
        response = requests.post(FASTAPI_URL, json=payload)
        
        # Check if the response is successful
        if response.status_code == 200:
            bot_response = response.json().get("fulfillmentText", "No response from bot.")
            st.success(f"Bot: {bot_response}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    else:
        st.warning("Please enter a query.")
