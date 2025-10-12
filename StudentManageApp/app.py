## Student Class
##│
##├── attributes: id, name, scores, gpa
##│
##├── methods:
##│   ├── calculate_gpa()
##│   ├── to_dict()
##│
##└── App Logic
##    ├── Add / View / Delete students
##    ├── Rank by GPA
##    └── Save to file


import streamlit as st
import json
import os

# ================
# CLASS DEFINITION
# ================
class Student:
    def __init__(self, student_id, name, scores):
        self.student_id = student_id
        self.name = name
        self.scores = scores
        self.gpa = self.calculate_gpa()

    def calculate_gpa(self):
        if not self.scores:
            return 0.0
        return round(sum(self.scores.values()) / len(self.scores), 2)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "scores": self.scores,
            "gpa": self.gpa
        }

# =============
# FILE HANDLING
# =============
DATA_FILE = "students.json"

def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Student(**d) for d in data]
    return []

def save_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in students], f, indent=4, ensure_ascii=False)

# ============
# STREAMLIT UI
# ============
st.set_page_config(page_title="🎓 Student Manager", page_icon="📚", layout="centered")
st.title("🎓 Student Management System")

# Load data into session
if "students" not in st.session_state:
    st.session_state.students = load_students()

students = st.session_state.students

# --- Add Student 
st.subheader("➕ Add a new student")

with st.form("add_student_form"):
    student_id = st.text_input("Student ID")
    name = st.text_input("Full Name")

    math = st.number_input("Math", 0.0, 10.0, step=0.1)
    english = st.number_input("English", 0.0, 10.0, step=0.1)
    science = st.number_input("Science", 0.0, 10.0, step=0.1)

    submitted = st.form_submit_button("Add Student")

    if submitted and student_id and name:
        new_student = Student(student_id, name, {
            "Math": math,
            "English": english,
            "Science": science
        })
        students.append(new_student)
        save_students(students)
        st.success(f"✅ Added student {name} (GPA: {new_student.gpa})")
        st.experimental_rerun()

st.divider()

# --- Display Students
st.subheader("📋 Student List & GPA Ranking")

if students:
    # Sort by GPA descending
    students_sorted = sorted(students, key=lambda s: s.gpa, reverse=True)

    data = [{
        "Rank": i + 1,
        "ID": s.student_id,
        "Name": s.name,
        "Math": s.scores["Math"],
        "English": s.scores["English"],
        "Science": s.scores["Science"],
        "GPA": s.gpa
    } for i, s in enumerate(students_sorted)]

    st.dataframe(data, use_container_width=True)

    # Option to delete a student
    st.subheader("🗑️ Delete a student")
    del_id = st.text_input("Enter Student ID to delete")
    if st.button("Delete"):
        found = next((s for s in students if s.student_id == del_id), None)
        if found:
            students.remove(found)
            save_students(students)
            st.success(f"Deleted student {found.name}")
            st.experimental_rerun()
        else:
            st.error("No student found with that ID.")
else:
    st.info("No student data yet. Add your first student above!")

st.divider()
if st.button("💾 Save & Reload"):
    save_students(students)
    st.experimental_rerun()
