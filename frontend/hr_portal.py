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
from ai import get_resume_analysis, generate_challenge, score_challenge, get_skill_gaps
from dotenv import load_dotenv
import os
import json

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
@st.cache_resource
def get_appwrite_client():
    client = Client()
    client.set_endpoint(APPWRITE_ENDPOINT)
    client.set_project(APPWRITE_PROJECT_ID)
    client.set_key(APPWRITE_API_KEY)
    return client

client = get_appwrite_client()
databases = Databases(client)
storage = Storage(client)

@st.cache_data
def get_jobs():
    result = databases.list_documents(DB_ID, JOBS_COLLECTION_ID)
    return result['documents']

@st.cache_data
def get_job_details(job_id):
    return databases.get_document(DB_ID, JOBS_COLLECTION_ID, job_id)

@st.cache_data
def get_applications(job_id):
    result = databases.list_documents(
        DB_ID,
        APPLICATIONS_COLLECTION_ID,
        queries=[
            Query.equal("job_id", job_id),
            Query.order_desc("score")
        ]
    )
    return result['documents']

@st.cache_data
def get_challenge(application_id):
    result = databases.list_documents(
        DB_ID,
        CHALLENGES_COLLECTION_ID,
        queries=[Query.equal("application_id", application_id)]
    )
    return result['documents']

@st.cache_data
def get_resume_content(resume_path):
    return storage.get_file_download(RESUMES_BUCKET_ID, resume_path)

@st.cache_data
def cached_get_skill_gaps(resume_text, job_description):
    return get_skill_gaps(resume_text, job_description)

def hr_portal():
    st.header("HR Portal")

    st.subheader("Manage Jobs")
    job_title = st.text_input("Job Title")
    job_description = st.text_area("Job Description")

    if st.button("Add Job"):
        job_data = {"title": job_title, "description": job_description}
        try:
            databases.create_document(DB_ID, JOBS_COLLECTION_ID, ID.unique(), job_data)
            st.success("Job added successfully!")
            st.cache_data.clear()
        except AppwriteException as e:
            st.error(f"Error adding job: {e.message}")

    st.subheader("Current Jobs")
    try:
        jobs = get_jobs()
        if jobs:
            job_df = pd.DataFrame(jobs)
            st.dataframe(job_df[['title', 'description']])

            selected_job_id = st.selectbox("Select a job to view applications", jobs, format_func=lambda job: job['title'])['$id']

            if st.button("View Applications"):
                try:
                    applications = get_applications(selected_job_id)
                    if applications:
                        for app in applications:
                            st.subheader(f"Application from Student ID: {app['student_id']}")
                            st.write(f"Score: {app['score']}")
                            st.write(f"Status: {app['status']}")

                            with st.expander("View Details"):
                                st.write("**AI-Generated Fit Verdict:**")
                                st.write(app['analysis_summary'])

                                # Get skill gaps
                                resume_content = get_resume_content(app['resume_path'])
                                try:
                                    resume_text = resume_content.decode('utf-8')
                                except UnicodeDecodeError:
                                    try:
                                        resume_text = resume_content.decode('latin-1')
                                    except UnicodeDecodeError:
                                        st.warning("Could not decode the resume file.")
                                        resume_text = ""
                                job_details = get_job_details(app['job_id'])
                                job_description = job_details['description']
                                skill_gaps = cached_get_skill_gaps(resume_text, job_description)
                                st.write("**Skill Gaps:**")
                                if skill_gaps:
                                    for skill in skill_gaps:
                                        st.write(f"- {skill}")
                                else:
                                    st.write("No skill gaps identified.")

                                # Get challenge details
                                if app['status'] in ["challenge sent", "challenge submitted", "challenge scored"]:
                                    challenges = get_challenge(app['$id'])
                                    if challenges:
                                        challenge = challenges[0]
                                        st.write("**Technical Challenge:**")
                                        st.write(f"**Questions:**\n{challenge['questions']}")

                                        results = {}
                                        if challenge.get('results'):
                                            results = json.loads(challenge['results'])

                                        if results.get('answers'):
                                            st.write(f"**Answers:**\n{results['answers']}")

                                        if results.get('score') is not None:
                                            st.write(f"**Score:** {results['score']}")
                                        if results.get('feedback'):
                                            st.write("**Feedback:**")
                                            st.markdown(results['feedback'])
                                        if results.get('proctoring_flags'):
                                            st.write(f"**Proctoring Flags:**\n{results['proctoring_flags']}")

                    else:
                        st.info("No applications for this job yet.")
                except AppwriteException as e:
                    st.error(f"An error occurred: {e.message}")
        else:
            st.info("No jobs available at the moment.")
    except AppwriteException as e:
        st.error(f"An error occurred: {e.message}")
