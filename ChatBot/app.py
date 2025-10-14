import streamlit as st
import json
import os
import requests

DATA_FILE = "data.json"


# Load & Save data

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Wikipedia API 

def search_wikipedia(query):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '%20')}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            info = r.json()
            return info.get("extract", "No summary found.")
        else:
            return "Sorry, I couldn’t fetch information from Wikipedia."
    except Exception:
        return "Error connecting to Wikipedia."


# Chatbot logic

def chatbot_response(user_input, data):
    user_input = user_input.lower().strip()

    # Learning pattern: learn: question => answer
    if user_input.startswith("learn:"):
        try:
            _, qa = user_input.split("learn:", 1)
            question, answer = qa.split("=>")
            question, answer = question.strip().lower(), answer.strip()
            data[question] = answer
            save_data(data)
            return f"Got it! I’ve learned: '{question}' → '{answer}'"
        except Exception:
            return "Format error! Use: learn: question => answer"

    # Wikipedia query
    if user_input.startswith("wiki:"):
        topic = user_input.replace("wiki:", "").strip()
        return search_wikipedia(topic)

    # Normal response
    for key, response in data.items():
        if key in user_input:
            return response

    return data.get("default", "I'm not sure I understand that yet.")

# Streamlit UI
# -----------------------
st.set_page_config(page_title="SmartBot", page_icon="🤖", layout="centered")

# Custom CSS for chat bubbles
st.markdown("""
    <style>
    .chat-box {padding: 10px; border-radius: 15px; margin: 5px 0; max-width: 80%;}
    .user {background-color: #DCF8C6; margin-left: auto; text-align: right;}
    .bot {background-color: #F1F0F0; margin-right: auto;}
    </style>
""", unsafe_allow_html=True)

st.title("SmartBot — Your Learning Chatbot")
st.caption("Type `learn: question => answer` to teach me new things. Use `wiki: topic` to search Wikipedia.")

data = load_data()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Say something...")

if user_input:
    response = chatbot_response(user_input, data)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat as bubbles
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"<div class='chat-box user'>🧑 <b>You:</b> {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-box bot'>🤖 <b>Bot:</b> {msg}</div>", unsafe_allow_html=True)

if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
