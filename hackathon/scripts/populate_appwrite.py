import sys
sys.path.append("..")
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.exception import AppwriteException
from dotenv import load_dotenv
import os

load_dotenv()

# Appwrite Configuration
APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")
DB_ID = os.getenv("DB_ID")
JOBS_COLLECTION_ID = os.getenv("JOBS_COLLECTION_ID")

# Initialize Appwrite Client
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

databases = Databases(client)

def populate_appwrite():
    jobs = [
        {"title": "Software Engineer", "description": "We are looking for a software engineer to join our team."},
        {"title": "Data Scientist", "description": "We are looking for a data scientist to join our team."},
        {"title": "Product Manager", "description": "We are looking for a product manager to join our team."},
    ]

    for job in jobs:
        try:
            databases.create_document(DB_ID, JOBS_COLLECTION_ID, ID.unique(), job)
            print(f"Successfully created job: {job['title']}")
        except AppwriteException as e:
            print(f"Error creating job: {e.message}")

if __name__ == "__main__":
    populate_appwrite()