from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT
model = SentenceTransformer("all-mpnet-base-v2")

def embed_skills(skills):
    return model.encode(skills, convert_to_tensor=True)

kw_model = KeyBERT()

def extract_skills(text, top_n=10):
    """
    Extracts keywords from the given text using KeyBERT.
    Args:
        text (str): The text from which to extract keywords.
        top_n (int): The number of top keywords to extract. Default is 10.
    Returns:
        list: A list of extracted keywords.
    """
    if not text:
        return []
    # Ensure the text is a string
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")
    # If the text is empty, return an empty list
    if not text.strip():
        return []
    # Extract keywords using KeyBERT
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    return list(set([kw[0] for kw in keywords]))


def find_missing_skills_semantically(jd_skills, resume_skills, threshold=0.75):
    """
    Compares the skills in the resume with the skills in the job description
    using semantic similarity.
    Args:
        jd_skills (list): List of skills from the job description.
        resume_skills (list): List of skills from the resume.
        threshold (float): Similarity threshold for considering a skill as matched.
    Returns:
        list: List of skills from the job description that are not found in the resume.
    """
    if not resume_skills or not jd_skills:
        return jd_skills

    jd_embeddings = embed_skills(jd_skills)
    resume_embeddings = embed_skills(resume_skills)

    missing_skills = []
    for idx, jd_skill in enumerate(jd_skills):
        sim_scores = util.cos_sim(jd_embeddings[idx], resume_embeddings)
        if sim_scores.max().item() < threshold:
            missing_skills.append(jd_skill)
    return missing_skills
