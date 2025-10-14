import streamlit as st
import json
import os

# Load Q&A data
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Chatbot logic (rule-based)
def chatbot_response(user_input, data):
    user_input = user_input.lower().strip()
    for key, response in data.items():
        if key in user_input:
            return response
    return data.get("default", "Sorry, I didn’t understand that.")

# Streamlit UI
st.set_page_config(page_title="Mini Chatbot", page_icon="💬", layout="centered")

st.title("💬 Mini Chatbot")
st.caption("A simple rule-based chatbot built with Python + Streamlit")

# Load data
data = load_data()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    response = chatbot_response(user_input, data)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")

# Optional: reset chat
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.experimental_rerun()
