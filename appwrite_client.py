
import os
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage

load_dotenv()

# Appwrite Configuration
APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")

# Initialize the Appwrite client
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

# Initialize Appwrite services
databases = Databases(client)
storage = Storage(client)

# Database and Collection IDs
db_id = os.getenv("DB_ID")
jobs_collection_id = os.getenv("JOBS_COLLECTION_ID")
students_collection_id = os.getenv("STUDENTS_COLLECTION_ID")
applications_collection_id = os.getenv("APPLICATIONS_COLLECTION_ID")
