import streamlit as st
import pandas as pd
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.id import ID
from appwrite.exception import AppwriteException
from appwrite.input_file import InputFile
from appwrite.query import Query
import streamlit.components.v1 as components
from ai import get_resume_analysis, generate_challenge, score_challenge
from dotenv import load_dotenv
import os

load_dotenv()

# Appwrite Configuration
APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")
DB_ID = os.getenv("DB_ID")
JOBS_COLLECTION_ID = os.getenv("JOBS_COLLECTION_ID")
APPLICATIONS_COLLECTION_ID = os.getenv("APPLICATIONS_COLLECTION_ID")
STUDENTS_COLLECTION_ID = os.getenv("STUDENTS_COLLECTION_ID")
CHALLENGES_COLLECTION_ID = os.getenv("CHALLENGES_COLLECTION_ID")
RESUMES_BUCKET_ID = os.getenv("RESUMES_BUCKET_ID")

# Initialize Appwrite Client
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

databases = Databases(client)
storage = Storage(client)

def student_portal():
    st.header("Student Portal")

    # TODO: Replace with actual student ID from authentication
    student_id = "1" 

    # Check for challenges
    try:
        result = databases.list_documents(
            DB_ID, 
            APPLICATIONS_COLLECTION_ID,
            queries=[
                Query.equal("student_id", student_id),
                Query.equal("status", "challenge sent")
            ]
        )
        applications = result['documents']
        if applications:
            st.subheader("Your Technical Challenge")
            for app in applications:
                challenge_result = databases.list_documents(
                    DB_ID,
                    CHALLENGES_COLLECTION_ID,
                    queries=[Query.equal("application_id", app['$id'])]
                )
                challenges = challenge_result['documents']
                if challenges:
                    challenge = challenges[0]
                    st.markdown(challenge['questions'])

                    # Proctoring
                    with open("frontend/proctoring.js", "r") as f:
                        proctoring_js = f.read()
                    components.html(f"<script>{proctoring_js}</script>", height=0)

                    answers = st.text_area("Your Answers", key=challenge['$id'])
                    if st.button("Submit Answers", key=f"submit_{challenge['$id']}"):
                        proctoring_events = components.html(
                            """
                            <script>
                            const events = localStorage.getItem('proctoring_events');
                            Streamlit.setComponentValue(events);
                            </script>
                            """,
                            height=0
                        )
                        proctoring_flags = challenge.get("proctoring_flags", "")
                        if proctoring_events:
                            proctoring_flags += str(proctoring_events)
                        databases.update_document(DB_ID, CHALLENGES_COLLECTION_ID, challenge['$id'], {"answers": answers, "proctoring_flags": proctoring_flags})
                        databases.update_document(DB_ID, APPLICATIONS_COLLECTION_ID, app['$id'], {"status": "challenge submitted"})
                        st.success("Your answers have been submitted!")
    except AppwriteException as e:
        st.error(f"An error occurred: {e.message}")


    st.subheader("Available Jobs")
    try:
        result = databases.list_documents(DB_ID, JOBS_COLLECTION_ID)
        jobs = result['documents']
        if jobs:
            job_df = pd.DataFrame(jobs)
            st.dataframe(job_df[['title', 'description']])

            job_id = st.selectbox("Select a job to apply for", jobs, format_func=lambda job: job['title'])['$id']
            resume = st.file_uploader("Upload your resume")

            if 'analysis' not in st.session_state:
                st.session_state.analysis = None

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Analyze Resume (Before Applying)"):
                    if resume is not None:
                        with st.spinner("Analyzing your resume..."):
                            job_details = databases.get_document(DB_ID, JOBS_COLLECTION_ID, job_id)
                            job_description = job_details['description']
                            try:
                                resume_text = resume.getvalue().decode('utf-8')
                            except UnicodeDecodeError:
                                try:
                                    resume_text = resume.getvalue().decode('latin-1')
                                except UnicodeDecodeError:
                                    st.warning("Could not decode the resume file. Please upload a valid text file.")
                                    resume_text = ""
                            st.session_state.analysis = get_resume_analysis(resume_text, job_description)
                    else:
                        st.warning("Please upload your resume first.")
            
            if st.session_state.analysis:
                st.subheader("Analysis Results")
                st.metric("Relevance Score", f"{st.session_state.analysis['score']}%")
                st.info(f"Summary: {st.session_state.analysis['summary']}")
                st.subheader("Personalized Guidance")
                st.markdown(st.session_state.analysis['guidance'])

            with col2:
                if st.button("Apply"):
                    if resume is not None:
                        with st.spinner("Analyzing and submitting your application..."):
                            # Get job description
                            job_details = databases.get_document(DB_ID, JOBS_COLLECTION_ID, job_id)
                            job_description = job_details['description']
                            
                            # Get resume text
                            try:
                                resume_text = resume.getvalue().decode('utf-8')
                            except UnicodeDecodeError:
                                try:
                                    resume_text = resume.getvalue().decode('latin-1')
                                except UnicodeDecodeError:
                                    st.warning("Could not decode the resume file. Please upload a valid text file.")
                                    resume_text = ""
                            
                            # Analyze resume
                            if st.session_state.analysis:
                                analysis = st.session_state.analysis
                            else:
                                analysis = get_resume_analysis(resume_text, job_description)
                            score = analysis['score']
                            summary = analysis['summary']

                            # Upload resume to storage
                            file_id = ID.unique()
                            storage.create_file(RESUMES_BUCKET_ID, file_id, InputFile.from_bytes(resume.getvalue(), filename=resume.name))

                            # Create application data
                            application_data = {
                                "job_id": job_id,
                                "student_id": student_id,
                                "resume_path": file_id,
                                "score": score,
                                "analysis_summary": summary,
                                "status": "submitted"
                            }

                            # Check if score is above threshold
                            if score >= 70:
                                application_data["status"] = "challenge sent"
                                
                                # Generate challenge
                                questions = generate_challenge(resume_text)
                                
                                # Create application document
                                application_document = databases.create_document(DB_ID, APPLICATIONS_COLLECTION_ID, ID.unique(), application_data)
                                
                                # Create challenge document
                                challenge_data = {
                                    "application_id": application_document['$id'],
                                    "questions": questions
                                }
                                databases.create_document(DB_ID, CHALLENGES_COLLECTION_ID, ID.unique(), challenge_data)
                                
                                st.success("Application submitted successfully! You have a new challenge.")
                            else:
                                # Create application document
                                databases.create_document(DB_ID, APPLICATIONS_COLLECTION_ID, ID.unique(), application_data)
                                st.success("Application submitted successfully!")
                    else:
                        st.warning("Please upload your resume.")
        else:
            st.info("No jobs available at the moment.")
    except AppwriteException as e:
        st.error(f"An error occurred: {e.message}")