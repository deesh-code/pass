import streamlit as st
from student_portal import student_portal
from hr_portal import hr_portal

def main():
    st.title("Progressive Automated Screening System (PASS)")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Student Portal", "HR Portal"])

    if page == "Student Portal":
        student_portal()
    elif page == "HR Portal":
        hr_portal()

if __name__ == "__main__":
    main()