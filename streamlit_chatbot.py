import streamlit as st
import requests

# Set your Google API Key
GOOGLE_API_KEY = "AIzaSyDCZ5o_Kg1aQuKTVY34L5Tsyb8I3yPtPOA"

# Function to get the chatbot response from Google API
def get_chatbot_response(user_input):
    api_url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={GOOGLE_API_KEY}"
    
    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "prompt": {
            "text": user_input
        },
        "maxOutputTokens": 150
    }

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        # st.write("API Response:", response_data)  # Log the entire response for debugging

        # Try to extract the text from the most likely location
        if 'candidates' in response_data:
            return response_data['candidates'][0]['output']
        elif 'choices' in response_data:
            return response_data['choices'][0]['message']['content']
        elif 'output' in response_data:
            return response_data['output']
        else:
            return "Unexpected response structure: No recognizable keys found."
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.title("AI-Powered Chatbot")

st.write("Ask anything to the chatbot:")

user_input = st.text_input("You:")

if st.button("Send"):
    if user_input:
        response = get_chatbot_response(user_input)
        st.text_area("Chatbot:", value=response, height=200, max_chars=None)
    else:
        st.write("Please enter a message.")

