from qdrant_client import QdrantClient, models
import os
from dotenv import load_dotenv

load_dotenv()
client = QdrantClient(
    url="https://2a3f9b3d-06b4-48d5-9a17-14005a0a52e9.us-west-1-0.aws.cloud.qdrant.io", 
    api_key=os.getenv('QDRANT_API_KEY'),
)

print(client.get_collections())

def create_collection():
    client.recreate_collection(
        collection_name="resumes",
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),  # Fixed vector size
    )

try:
    client.get_collection(collection_name="resumes")
except Exception:
    create_collection()
