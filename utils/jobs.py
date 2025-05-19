import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

def load_job_descriptions():
    with open("data/job_descriptions.json", "r") as f:
        return json.load(f)

def generate_jd_embeddings(jobs):
    jd_embeddings = []
    for job in jobs:
        embedding = model.encode(job["description"])
        jd_embeddings.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "description": job["description"],
            "skills": job["skills"],
            "embedding": embedding
        })
    return jd_embeddings
