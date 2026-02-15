import os
import boto3
from ..core.config import settings

class ContentService:
    def __init__(self):
        self.storage_type = settings.STORAGE_TYPE
        if self.storage_type == "r2":
            self.client = get_r2_client()
            self.bucket = settings.R2_BUCKET_NAME
        else:
            self.local_path = settings.LOCAL_STORAGE_PATH
            # Ensure local directory exists
            os.makedirs(self.local_path, exist_ok=True)

    def get_content(self, key: str, db_content: str = None) -> str:
        """
        Retrieve content from configured storage (DB, Local or R2).
        If db_content is provided, return it directly.
        """
        if db_content:
            return db_content

        if self.storage_type == "db":
             return None # Should have been passed in db_content if available
        
        if self.storage_type == "local":
            return self._get_local_content(key)
        else:
            return self._get_r2_content(key)

    def _get_local_content(self, key: str) -> str:
        file_path = os.path.join(self.local_path, key)
        if not os.path.exists(file_path):
            print(f"Local file not found: {file_path}")
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading local file: {e}")
            return None

    def _get_r2_content(self, key: str) -> str:
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=key)
            return response['Body'].read().decode('utf-8')
        except Exception as e:
            print(f"Error fetching from R2: {e}")
            return None

def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.R2_ENDPOINT_URL,
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    )
