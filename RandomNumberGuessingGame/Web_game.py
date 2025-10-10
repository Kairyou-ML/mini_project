import streamlit as st
import random

st.set_page_config(page_title="Number Guessing Game", page_icon="🎯")

st.title("Number Guessing Game")
st.write("I am thinking about a number from 1 to 100, let guess it!")

# --- Khởi tạo trạng thái ---
if "so_bi_mat" not in st.session_state:
    st.session_state.so_bi_mat = random.randint(1, 100)
    st.session_state.so_lan_doan = 0
if "ky_luc" not in st.session_state:
    st.session_state.ky_luc = None

# --- Nhập dự đoán ---
du_doan = st.number_input("Type your guessing number", min_value=1, max_value=100, step=1)
if st.button("Check!"):
    st.session_state.so_lan_doan += 1

    if du_doan < st.session_state.so_bi_mat:
        st.warning("🔻 Your number is smaller!")
    elif du_doan > st.session_state.so_bi_mat:
        st.warning("🔺 Your number is bigger!")
    else:
        st.success(f"Congratulation, the number is {st.session_state.so_bi_mat}.")
        st.balloons()

        # Cập nhật kỷ lục
        if st.session_state.ky_luc is None or st.session_state.so_lan_doan < st.session_state.ky_luc:
            st.session_state.ky_luc = st.session_state.so_lan_doan
            st.info(f"🏆 New achievement: {st.session_state.ky_luc} guessing times!")

        else:
            st.info(f"Your guess comes true after {st.session_state.so_lan_doan} times!")

        # Reset game
        if st.button("Replay 🎮"):
            st.session_state.so_bi_mat = random.randint(1, 100)
            st.session_state.so_lan_doan = 0
            st.experimental_rerun()

st.write("---")
st.write(f"Guessing times: {st.session_state.so_lan_doan}")
if st.session_state.ky_luc:
    st.write(f"🏆 Best achievement: Guess in just {st.session_state.ky_luc} times ")

if st.button("🔁 Reset all"):
    st.session_state.clear()
    st.experimental_rerun()
