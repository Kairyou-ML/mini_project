# Personal Calculator

A simple web-based calculator built with **Streamlit**.  
This mini-project demonstrates how to create an interactive calculator interface using Python and Streamlit, with basic arithmetic and math functions.

---

## Features

- Real-time expression display
- Supports basic operations: addition, subtraction, multiplication, division
- Advanced operations: square root (`sqrt()`), power (`^`)
- Clear and evaluate buttons
- Simple and responsive layout using Streamlit columns

---

## Tech Stack

- **Language:** Python  
- **Framework:** Streamlit  
- **Library:** math

---

## Installation

1. Clone this repository or download the folder:
   ```bash
   git clone https://github.com/Kairyou-ML/mini_project.git
   cd mini_project/calculator
   ```

2. Install the dependencies:
   ```bash
   pip install streamlit
   ```

3. Run the app:
   ```bash
   streamlit run calculator.py
   ```

4. The app will open in your browser at:
   ```
   http://localhost:8501
   ```

---

## How to Use

1. Enter expressions using the on-screen buttons.  
2. Click `=` to evaluate.  
3. Use `√` for square root, `^` for power.  
4. Press **Clear** to reset the input field.

Example expressions:
```
2 + 3 * 4
sqrt(16)
2^5
```

---

## Project Structure

```
calculator/
│
├── calculator.py      # Main Streamlit app
└── README.md          # Project documentation
```

---

## License

This project is open-source and available under the [MIT License](../LICENSE).
