# SmartBot — Interactive Learning Chatbot

SmartBot is a lightweight Streamlit-based chatbot application that can **learn custom question–answer pairs** and **fetch quick Wikipedia summaries**.  
It provides a simple conversational interface where users can interact, teach new responses, and explore topics dynamically.

---

## Features

- Chat interface built with Streamlit
- Learn new Q&A pairs dynamically using `learn:` syntax
- Retrieve Wikipedia summaries using the `wiki:` command
- Persistent local knowledge storage in `data.json`
- Styled chat bubbles for user and bot messages
- Option to clear the chat session

---

## Tech Stack

- **Python 3.9+**
- **Streamlit**
- **Requests**
- **JSON (built-in)**

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mini_project.git
cd mini_project/Chatbot

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```


## How to Use
1. Launch the Streamlit app using the command above.

2. Interact with SmartBot through the chat input:

  - Teach new responses:

  ```bash
  learn: hello => Hi there! How can I help you today?
  ```

  - Ask a learned question:

  ```nginx
  hello
  ```
  ➜ SmartBot replies with your saved answer.

  - Search Wikipedia topics:

  ```makefile
  wiki: Artificial Intelligence
  ```
  ➜ SmartBot returns a brief summary from Wikipedia.

3. Click "🧹 Clear Chat" to reset the conversation.

---
## Project Structure
```bash
Chatbot/
│
├── app.py              # Main Streamlit chatbot application
├── data.json           # JSON file for storing learned Q&A pairs
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```
---
## License
This project is licensed under the MIT License.
