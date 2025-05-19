"""
This module contains functions to match resumes to job descriptions using embeddings.
It uses cosine similarity to find the best matches based on the embeddings generated from the resume and job descriptions.
"""

from sklearn.metrics.pairwise import cosine_similarity

def match_resume_to_jd(resume_embedding, jd_embeddings):
    """
    Match resume embedding to job description embeddings using cosine similarity.
    
    """
    matches = []
    for jd in jd_embeddings:
        score = cosine_similarity([resume_embedding], [jd["embedding"]])[0][0]
        matches.append((jd, score))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches
