# Contact Manager App

Contact Manager App is a simple Streamlit-based application that allows users to **add, view, search, edit, delete, and analyze contacts**.  
It provides an intuitive web interface with persistent JSON storage and visual statistics powered by Plotly.

---

## Features

- Add, view, search, edit, and delete contact information
- Persistent data storage in `contacts.json`
- Real-time editable contact list using Streamlit UI
- Contact distribution visualization by initial letter (Plotly bar chart)
- Sidebar menu for easy navigation between modules
- Input validation for required fields

---

## Tech Stack

- **Python 3.9+**
- **Streamlit**
- **Pandas**
- **Plotly**
- **JSON (built-in)**

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mini_project.git
cd mini_project/ContactManageApp

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

---
## How to Use
1. Launch the app with streamlit run app.py.

2. Use the sidebar to navigate:

  - Add: Enter new contact details and click Save Contact.

  - View All: View all contacts in a sortable table.

  - Search: Find contacts by partial or full name.

  - Edit/Delete: Update or remove existing contacts.

  - Statistics: View contact distribution by name initials.

3. All changes are automatically saved in contacts.json.

---
## Project Structure
```bash
ContactManageApp/
│
├── app.py              # Main Streamlit app
├── contacts.json       # JSON file storing contact data
├── contact.json        # (Optional backup or sample file)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```
## License
This project is licensed under the MIT License.
