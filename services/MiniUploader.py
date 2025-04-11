"""
Filename: MiniUploader.py
Author: Suraj
Created on: April 11, 2025
Description:
    - class initited to connect the minio load from env
    - Funcction to upload the file and return the exact path
"""

from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
import os

class MinioUploader:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        self.client = Minio(
            endpoint=os.getenv("MINIO_ENDPOINT"),  # example: "localhost:9000"
            access_key=os.getenv("MINIO_ROOT_USER"),
            secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
            secure=False  # because locally we don't use https
        )

        self.bucket_name = os.getenv("MINIO_BUCKET", "pdf-uploads")

        # Create bucket if it doesn't exist
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
            print(f"✅ Bucket '{self.bucket_name}' created.")
        else:
            print(f"ℹ️ Bucket '{self.bucket_name}' already exists.")

    def upload_file(self, file_object, filename):
        try:
            # Upload the file
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=filename,
                data=file_object,
                length=-1,
                part_size=10 * 1024 * 1024,
                content_type="application/pdf"
            )

            print(f"✅ Uploaded '{filename}' successfully!")

            # Generate file URL (public or private depending on bucket settings)
            file_url = f"http://{os.getenv('MINIO_ENDPOINT')}/{self.bucket_name}/{filename}"
            return file_url

        except S3Error as e:
            print(f"❌ Upload failed: {e}")
            return None