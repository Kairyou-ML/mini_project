import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

DATA_FILE = "contacts.json"

# Hàm tiện ích 
def load_contacts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_contacts(contacts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)

def find_contact(contacts, name):
    return [c for c in contacts if name.lower() in c["name"].lower()]

# Giao diện
st.set_page_config(page_title="Contact Manager", page_icon="📞", layout="centered")
st.title("📞 Contact Manager App")

menu = ["Add", "View All", "Search", "Edit/Delete", "Statistics"]
choice = st.sidebar.radio("Menu", menu)

contacts = load_contacts()

#Thêm danh bạ 
if choice == "Add":
    st.subheader("➕ Add New Contact")
    name = st.text_input("Full name")
    phone = st.text_input("Phone number")
    email = st.text_input("Email (optional)")
    address = st.text_area("Address (optional)")
    
    if st.button("Save Contact"):
        if not name or not phone:
            st.warning("⚠️ Name and phone number are required.")
        else:
            contacts.append({
                "name": name,
                "phone": phone,
                "email": email,
                "address": address
            })
            save_contacts(contacts)
            st.success(f"Contact '{name}' saved successfully!")

#  Xem toàn bộ danh bạ
elif choice == "View All":
    st.subheader("👀 All Contacts")
    if contacts:
        df = pd.DataFrame(contacts)
        st.dataframe(df)
    else:
        st.info("No contacts available yet.")

# Tìm kiếm 
elif choice == "Search":
    st.subheader("🔍 Search Contacts")
    query = st.text_input("Enter name to search:")
    if query:
        results = find_contact(contacts, query)
        if results:
            st.success(f"Found {len(results)} contact(s).")
            st.table(pd.DataFrame(results))
        else:
            st.warning("No contact found.")

#  Chỉnh sửa / Xóa 
elif choice == "Edit/Delete":
    st.subheader("✏️ Edit or Delete Contact")
    if not contacts:
        st.info("No contacts available to edit.")
    else:
        names = [c["name"] for c in contacts]
        selected = st.selectbox("Select contact", names)
        contact = next(c for c in contacts if c["name"] == selected)
        
        new_name = st.text_input("Name", contact["name"])
        new_phone = st.text_input("Phone", contact["phone"])
        new_email = st.text_input("Email", contact["email"])
        new_address = st.text_area("Address", contact["address"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes"):
                contact.update({
                    "name": new_name,
                    "phone": new_phone,
                    "email": new_email,
                    "address": new_address
                })
                save_contacts(contacts)
                st.success("Changes saved successfully!")

        with col2:
            if st.button("🗑️ Delete Contact"):
                contacts = [c for c in contacts if c["name"] != selected]
                save_contacts(contacts)
                st.warning(f"Contact '{selected}' deleted.")
                st.rerun()

# Thống kê (bằng biểu đồ Plotly)
elif choice == "Statistics":
    st.subheader("📊 Statistics")

    if not contacts:
        st.info("No contacts to analyze.")
    else:
        df = pd.DataFrame(contacts)
        df["Initial"] = df["name"].str[0].str.upper()

        chart = df["Initial"].value_counts().reset_index()
        chart.columns = ["Initial", "Count"]

        fig = px.bar(chart, x="Initial", y="Count", color="Initial",
                     title="Distribution of Contacts by Initial Letter")
        st.plotly_chart(fig, use_container_width=True)

