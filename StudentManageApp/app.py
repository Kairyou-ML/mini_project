## Class Student (OOP)
## CRUD (Add / Edit / Delete students)
## GPA auto-calculation
## Ranking table
## GPA progress chart using Plotly
## Persistent storage using JSON

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
import plotly.express as px

# ---------- Student Class ----------
class Student:
    def __init__(self, name, age, student_id, grades=None, gpa=0.0):
        self.name = name
        self.age = age
        self.student_id = student_id
        self.grades = grades or []
        self.gpa = gpa

    def calculate_gpa(self):
        if not self.grades:
            self.gpa = 0.0
        else:
            self.gpa = round(sum(self.grades) / len(self.grades), 2)

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "student_id": self.student_id,
            "grades": self.grades,
            "gpa": self.gpa,
        }

#  Utility Functions 
DATA_FILE = "students_data.json"

def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [Student(**item) for item in data]
    return []

def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump([s.to_dict() for s in students], f, indent=4)

#  Streamlit UI 
st.set_page_config(page_title="Student Management System", page_icon="🎓", layout="centered")
st.title("Student Management System")

students = load_students()

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Add Student", "View Students", "GPA Ranking", "Statistics"])

#  Add Student 
if menu == "Add Student":
    st.subheader("Add New Student")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    student_id = st.text_input("Student ID")
    grades_str = st.text_input("Enter grades separated by commas (e.g., 8.0, 7.5, 9.0)")

    if st.button("Add Student"):
        if name and student_id:
            grades = [float(x.strip()) for x in grades_str.split(",") if x.strip()]
            student = Student(name, age, student_id, grades)
            student.calculate_gpa()
            students.append(student)
            save_students(students)
            st.success(f"Student '{name}' added successfully!")
            st.rerun()
        else:
            st.warning("Please enter both name and student ID!")

#  View Students 
elif menu == "View Students":
    st.subheader("Student List")

    if not students:
        st.info("No students found. Add new students first.")
    else:
        for i, s in enumerate(students):
            with st.expander(f"{s.name} ({s.student_id})"):
                st.write(f"**Age:** {s.age}")
                st.write(f"**Grades:** {s.grades}")
                st.write(f"**GPA:** {s.gpa}")
                col1, col2 = st.columns(2)

                if col1.button(f"🗑️ Delete {s.name}", key=f"del_{i}"):
                    students.pop(i)
                    save_students(students)
                    st.success(f"Deleted student {s.name}")
                    st.rerun()

                if col2.button(f"✏️ Recalculate GPA", key=f"edit_{i}"):
                    s.calculate_gpa()
                    save_students(students)
                    st.success(f"GPA recalculated for {s.name}")
                    st.rerun()

#  GPA Ranking 
elif menu == "GPA Ranking":
    st.subheader(" GPA Ranking")
    if not students:
        st.info("No students to rank yet.")
    else:
        sorted_students = sorted(students, key=lambda s: s.gpa, reverse=True)
        ranking_data = [{"Rank": i+1, "Name": s.name, "GPA": s.gpa} for i, s in enumerate(sorted_students)]
        st.table(ranking_data)

#  GPA Statistics 
elif menu == "Statistics":
    st.subheader(" GPA Statistics")

    if not students:
        st.info("No GPA data available.")
    else:
        names = [s.name for s in students]
        gpas = [s.gpa for s in students]

        fig = px.bar(x=names, y=gpas, labels={"x": "Student", "y": "GPA"},
                     title="Student GPA Comparison", color=gpas, color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)
