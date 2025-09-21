import sys
sys.path.append("..")
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.exception import AppwriteException
from appwrite.services.storage import Storage
import os
from dotenv import load_dotenv

load_dotenv()

# Appwrite Configuration
APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")
DB_ID = os.getenv("DB_ID")
JOBS_COLLECTION_ID = os.getenv("JOBS_COLLECTION_ID")
STUDENTS_COLLECTION_ID = os.getenv("STUDENTS_COLLECTION_ID")
APPLICATIONS_COLLECTION_ID = os.getenv("APPLICATIONS_COLLECTION_ID")
CHALLENGES_COLLECTION_ID = os.getenv("CHALLENGES_COLLECTION_ID")
RESUMES_BUCKET_ID = os.getenv("RESUMES_BUCKET_ID")

# Initialize Appwrite Client
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

databases = Databases(client)
storage = Storage(client)

def setup_appwrite():
    try:
        databases.get(DB_ID)
        print("Database already exists.")
    except AppwriteException:
        databases.create(DB_ID, "PASS DB")
        print("Database created.")
        databases.create_collection(DB_ID, JOBS_COLLECTION_ID, "Jobs")
        print("Jobs collection created.")
        databases.create_string_attribute(DB_ID, JOBS_COLLECTION_ID, "title", 255, True)
        databases.create_string_attribute(DB_ID, JOBS_COLLECTION_ID, "description", 10000, True)
        databases.create_collection(DB_ID, STUDENTS_COLLECTION_ID, "Students")
        print("Students collection created.")
        databases.create_string_attribute(DB_ID, STUDENTS_COLLECTION_ID, "name", 255, True)
        databases.create_string_attribute(DB_ID, STUDENTS_COLLECTION_ID, "email", 255, True)
        databases.create_collection(DB_ID, APPLICATIONS_COLLECTION_ID, "Applications")
        print("Applications collection created.")
        databases.create_string_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "job_id", 255, True)
        databases.create_string_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "student_id", 255, True)
        databases.create_string_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "resume_path", 255, True)
        databases.create_integer_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "score", required=False)
        databases.create_string_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "status", 255, True)
        databases.create_string_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "analysis_summary", 10000, required=False)
        databases.create_collection(DB_ID, CHALLENGES_COLLECTION_ID, "Challenges")
        print("Challenges collection created.")
        databases.create_string_attribute(DB_ID, CHALLENGES_COLLECTION_ID, "application_id", 255, True)
        databases.create_string_attribute(DB_ID, CHALLENGES_COLLECTION_ID, "questions", 10000, True)
        databases.create_string_attribute(DB_ID, CHALLENGES_COLLECTION_ID, "answers", 10000, required=False)
        databases.create_integer_attribute(DB_ID, CHALLENGES_COLLECTION_ID, "score", required=False)
        databases.create_string_attribute(DB_ID, CHALLENGES_COLLECTION_ID, "proctoring_flags", 10000, required=False)

    try:
        storage.get_bucket(RESUMES_BUCKET_ID)
        print("Bucket already exists.")
    except AppwriteException:
        storage.create_bucket(RESUMES_BUCKET_ID, "Resumes")
        print("Bucket created.")

if __name__ == "__main__":
    setup_appwrite()
