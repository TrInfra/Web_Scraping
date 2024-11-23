import os
from dotenv import load_dotenv
from minio import Minio

def connection():
    load_dotenv()
    client = Minio(
        endpoint=os.getenv('MINIO_URL'),
        secure=False,
        access_key=os.getenv('MINIO_ACCESS_KEY_ID'),
        secret_key=os.getenv('MINIO_SECRET_ACCESS_KEY')
    )
    return client
