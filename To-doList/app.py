import streamlit as st
import json
import os
import matplotlib.pyplot as plt

# ==== APP CONFIG ====
st.set_page_config(page_title="✅ To-Do List App", page_icon="📝", layout="centered")
st.title("✅ To-Do List App")
st.write("A simple productivity app to manage your daily tasks.")

# FILE STORAGE
DATA_FILE = "todo.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

# SESSION STATE 
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

tasks = st.session_state.tasks

# ADD NEW TASK 
with st.form("add_task_form"):
    new_task = st.text_input("✏️ Enter a new task:")
    submitted = st.form_submit_button("Add Task ➕")
    if submitted and new_task:
        tasks.append({"name": new_task, "done": False})
        save_tasks(tasks)
        st.success(f"Added: {new_task}")
        st.rerun()

st.divider()

# TASK LIST 
if tasks:
    st.subheader("📋 Your Tasks")

    for i, task in enumerate(tasks):
        cols = st.columns([0.1, 0.7, 0.2])
        with cols[0]:
            done = st.checkbox("", value=task["done"], key=f"done_{i}")
            if done != task["done"]:
                task["done"] = done
                save_tasks(tasks)
        with cols[1]:
            text_style = "~~" if task["done"] else ""
            st.markdown(f"{text_style}{task['name']}{text_style}")
        with cols[2]:
            if st.button("🗑️ Delete", key=f"delete_{i}"):
                tasks.pop(i)
                save_tasks(tasks)
                st.rerun()

    if st.button("♻️ Clear all tasks"):
        tasks.clear()
        save_tasks(tasks)
        st.rerun()
else:
    st.info("No tasks yet. Add your first one above!")

# PROGRESS CHART 
st.divider()
st.subheader("📊 Progress Overview")

if tasks:
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    pending = total - done

    progress = done / total if total > 0 else 0
    st.progress(progress)

    st.write(f"**Completed:** {done}/{total} ({progress*100:.1f}%)")

    # Matplotlib Chart 
    labels = ['Completed', 'Pending']
    sizes = [done, pending]
    colors = ['#4CAF50', '#F44336']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.info("No data available for the chart.")