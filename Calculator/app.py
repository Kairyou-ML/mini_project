import streamlit as st
import math


# Streamlit Configuration
st.set_page_config(page_title="Personal Calculator", page_icon="🧮", layout="centered")

st.title("🧮 Personal Calculator")
st.caption("A simple web-based calculator built with Streamlit")

# Session State
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Functions
def add_to_expression(value):
    st.session_state.expression += str(value)

def clear_expression():
    st.session_state.expression = ""

def calculate_result():
    try:
        # Replace math symbols if needed
        expr = st.session_state.expression.replace("^", "**")
        result = eval(expr, {"__builtins__": None}, {"sqrt": math.sqrt, "pow": pow, "math": math})
        st.session_state.expression = str(result)
    except Exception:
        st.session_state.expression = "Error"

# UI Display
st.markdown("### Display")
st.text_input("Expression", st.session_state.expression, key="display", disabled=True)

# Calculator Buttons
col1, col2, col3, col4 = st.columns(4)

# Row 1
with col1: st.button("7", on_click=add_to_expression, args=("7",))
with col2: st.button("8", on_click=add_to_expression, args=("8",))
with col3: st.button("9", on_click=add_to_expression, args=("9",))
with col4: st.button("/", on_click=add_to_expression, args=("/",))

# Row 2
col1, col2, col3, col4 = st.columns(4)
with col1: st.button("4", on_click=add_to_expression, args=("4",))
with col2: st.button("5", on_click=add_to_expression, args=("5",))
with col3: st.button("6", on_click=add_to_expression, args=("6",))
with col4: st.button("x", on_click=add_to_expression, args=("*",))

# Row 3
col1, col2, col3, col4 = st.columns(4)
with col1: st.button("1", on_click=add_to_expression, args=("1",))
with col2: st.button("2", on_click=add_to_expression, args=("2",))
with col3: st.button("3", on_click=add_to_expression, args=("3",))
with col4: st.button("minus", on_click=add_to_expression, args=("-",))

# Row 4
col1, col2, col3, col4 = st.columns(4)
with col1: st.button("0", on_click=add_to_expression, args=("0",))
with col2: st.button(".", on_click=add_to_expression, args=(".",))
with col3: st.button("=", on_click=calculate_result)
with col4: st.button("plus", on_click=add_to_expression, args=("+",))

# Row 5
col1, col2, col3, col4 = st.columns(4)
with col1: st.button("(", on_click=add_to_expression, args=("(",))
with col2: st.button(")", on_click=add_to_expression, args=(")",))
with col3: st.button("^", on_click=add_to_expression, args=("^",))
with col4: st.button("√", on_click=add_to_expression, args=("sqrt(",))

# Row 6 (Clear)
st.button("🧹 Clear", on_click=clear_expression, use_container_width=True)

st.markdown("---")
st.info("💡 Tip: You can use `sqrt(x)` or `^` for powers, e.g., `2^3` or `sqrt(16)`")

