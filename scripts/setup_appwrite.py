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
CHALLENGE_FEEDBACK_COLLECTION_ID = os.getenv("CHALLENGE_FEEDBACK_COLLECTION_ID")
RESUMES_BUCKET_ID = os.getenv("RESUMES_BUCKET_ID")

# Initialize Appwrite Client
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

databases = Databases(client)
storage = Storage(client)

def setup_database():
    try:
        databases.get(DB_ID)
        print("Database already exists.")
    except AppwriteException:
        databases.create(DB_ID, "PASS DB")
        print("Database created.")

def setup_collections():
    # Jobs Collection
    try:
        databases.get_collection(DB_ID, JOBS_COLLECTION_ID)
        print("Jobs collection already exists.")
    except AppwriteException:
        databases.create_collection(DB_ID, JOBS_COLLECTION_ID, "Jobs")
        print("Jobs collection created.")
        databases.create_string_attribute(DB_ID, JOBS_COLLECTION_ID, "title", 255, True)
        databases.create_string_attribute(DB_ID, JOBS_COLLECTION_ID, "description", 10000, True)

    # Students Collection
    try:
        databases.get_collection(DB_ID, STUDENTS_COLLECTION_ID)
        print("Students collection already exists.")
    except AppwriteException:
        databases.create_collection(DB_ID, STUDENTS_COLLECTION_ID, "Students")
        print("Students collection created.")
        databases.create_string_attribute(DB_ID, STUDENTS_COLLECTION_ID, "name", 255, True)
        databases.create_string_attribute(DB_ID, STUDENTS_COLLECTION_ID, "email", 255, True)

    # Applications Collection
    try:
        databases.get_collection(DB_ID, APPLICATIONS_COLLECTION_ID)
        print("Applications collection already exists.")
    except AppwriteException:
        databases.create_collection(DB_ID, APPLICATIONS_COLLECTION_ID, "Applications")
        print("Applications collection created.")
        databases.create_string_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "job_id", 255, True)
        databases.create_string_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "student_id", 255, True)
        databases.create_string_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "resume_path", 255, True)
        databases.create_integer_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "score", required=False)
        databases.create_string_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "status", 255, True)
        databases.create_string_attribute(DB_ID, APPLICATIONS_COLLECTION_ID, "analysis_summary", 10000, required=False)

    # Challenges Collection
    try:
        databases.get_collection(DB_ID, CHALLENGES_COLLECTION_ID)
        print("Challenges collection already exists.")
    except AppwriteException:
        databases.create_collection(DB_ID, CHALLENGES_COLLECTION_ID, "Challenges")
        print("Challenges collection created.")
        databases.create_string_attribute(DB_ID, CHALLENGES_COLLECTION_ID, "application_id", 255, True)
        databases.create_string_attribute(DB_ID, CHALLENGES_COLLECTION_ID, "questions", 10000, True)
        databases.create_string_attribute(DB_ID, CHALLENGES_COLLECTION_ID, "results", 255, required=False)

    # Add missing attributes to Challenges collection if it already exists
    try:
        databases.get_attribute(DB_ID, CHALLENGES_COLLECTION_ID, "results")
    except AppwriteException:
        print("Adding 'results' attribute to Challenges collection.")
        databases.create_string_attribute(DB_ID, CHALLENGES_COLLECTION_ID, "results", 255, required=False)

    # Challenge Feedback Collection
    try:
        databases.get_collection(DB_ID, CHALLENGE_FEEDBACK_COLLECTION_ID)
        print("Challenge Feedback collection already exists.")
    except AppwriteException:
        databases.create_collection(DB_ID, CHALLENGE_FEEDBACK_COLLECTION_ID, "Challenge Feedback")
        print("Challenge Feedback collection created.")
        databases.create_string_attribute(DB_ID, CHALLENGE_FEEDBACK_COLLECTION_ID, "challenge_result_id", 255, True)
        databases.create_string_attribute(DB_ID, CHALLENGE_FEEDBACK_COLLECTION_ID, "feedback", 10000, required=False)

def setup_storage():
    try:
        storage.get_bucket(RESUMES_BUCKET_ID)
        print("Bucket already exists.")
    except AppwriteException:
        storage.create_bucket(RESUMES_BUCKET_ID, "Resumes")
        print("Bucket created.")

def setup_appwrite():
    setup_database()
    setup_collections()
    setup_storage()

if __name__ == "__main__":
    setup_appwrite()
