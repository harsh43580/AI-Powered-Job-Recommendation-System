import hashlib
import uuid
from sentence_transformers import SentenceTransformer
from utils.qdrant_client import client
from qdrant_client.http import models as rest  # NEW import

model = SentenceTransformer("all-mpnet-base-v2")

def generate_embedding(text):
    print(model.encode(text))
    return model.encode(text)

def hash_to_uuid(text):
    hash_hex = hashlib.sha256(text.strip().lower().encode()).hexdigest()
    return str(uuid.UUID(hash_hex[:32]))

# 🔥 This runs once to ensure the index exists
def ensure_hash_index():
    try:
        client.create_payload_index(
            collection_name="resumes",
            field_name="hash",
            field_schema=rest.PayloadSchemaType.KEYWORD
        )
        print("✅ Index on 'hash' created.")
    except Exception as e:
        if "already exists" in str(e):
            print("ℹ️ Index on 'hash' already exists.")
        else:
            print("⚠️ Index creation failed:", e)

def store_embedding(resume_text):
    # 🛡️ Ensure index exists before querying
    ensure_hash_index()

    point_id = hash_to_uuid(resume_text)
    embedding = generate_embedding(resume_text)

    # Check for existing point
    existing = client.scroll(
        collection_name="resumes",
        scroll_filter={"must": [{"key": "hash", "match": {"value": point_id}}]},
        limit=1
    )[0]

    if existing:
        return False, point_id  # Already exists

    client.upsert(
        collection_name="resumes",
        points=[{
            "id": point_id,
            "vector": embedding.tolist(),
            "payload": {"hash": point_id}
        }]
    )
    print(point_id)
    return True, point_id
