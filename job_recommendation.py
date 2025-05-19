"""
Job Recommender Application
This application allows users to upload their resumes in PDF format,
and it matches them with job descriptions based on the skills and
experience mentioned in the resume.
It uses embeddings to find the best matches and displays the top recommendations.
"""
import streamlit as st
import os
import tempfile
from utils.parser import extract_text_from_pdf
from utils.embeddings import generate_embedding, store_embedding
from utils.jobs import load_job_descriptions, generate_jd_embeddings
from utils.matcher import match_resume_to_jd
from utils.semantic_skills import find_missing_skills_semantically
from utils.semantic_skills import extract_skills  # Your skill extractor function\


st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("Resume Matcher – Get Job Recommendations Instantly")

# Load job descriptions
jobs = load_job_descriptions()
jd_embeddings = generate_jd_embeddings(jobs)

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    with st.spinner("Parsing your resume..."):
        resume_text = extract_text_from_pdf(file_path)

    os.remove(file_path)

    if resume_text:
        st.success("Resume parsed successfully!")
        st.text_area("Resume Text", resume_text, height=300)

        with st.spinner("Generating embedding and checking duplicates..."):
            success, resume_id = store_embedding(resume_text)

        if success:
            st.success("Resume embedding stored in vector DB!")
        else:
            st.warning("Duplicate resume detected. Using cached embedding.")

        resume_embedding = generate_embedding(resume_text)

        with st.spinner("Finding job matches..."):
            matches = match_resume_to_jd(resume_embedding, jd_embeddings)

        st.subheader("Top Job Recommendations")
        
        
        resume_skills = extract_skills(resume_text)

        # for job in matches:

        for jd, score in matches[:5]:
            jd_skills = jd["skills"]
            missing_skills = find_missing_skills_semantically(jd_skills, resume_skills)
            st.markdown(f"**{jd['title']}**")
            st.markdown(f"**Relevance Score**: `{round(score * 100, 2)}%`")
            st.markdown(f"**Missing skills**: `{', '.join(missing_skills)}`")
            st.markdown(f"**Job Description**: {jd['description']}")
            # st.markdown(f"**Required Skills**: `{', '.join(jd['skills'])}`")
            st.markdown("---")
    else:   
        st.error("Could not extract text from resume. Try a different file.")
else:
    st.info("Upload your resume to get started.")
