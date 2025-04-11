"""
Filename: mongo_upload.py
Author: Suraj
Created on: April 11, 2025
Description:
    - Initialize the mongo client
    - upload the coontent to the mongodb database
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MongoUploader:
    def __init__(self):
        self.client = MongoClient(
            host=os.getenv("MONGO_HOST", "localhost"),
            port=int(os.getenv("MONGO_PORT", 27017)),
            username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),
            password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
        )
        self.db = self.client["file_uploads_db"]
        self.collection = self.db["uploads"]

    def upload_metadata(self, prjname: str, file_path: str):
        document = {
            "prjname": prjname,
            "file_path": file_path
        }
        result = self.collection.insert_one(document)
        print(f"✅ Metadata uploaded with id {result.inserted_id}")
        return str(result.inserted_id)
