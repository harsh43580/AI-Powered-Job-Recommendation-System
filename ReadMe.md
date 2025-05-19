

## 🧠 **Project: AI-Powered Job Recommendation System**

---

### 🎯 **Objective**
Build  tool that:
- Lets users upload their resume
- Matches it to the top 10 most relevant job descriptions (JDs)
- Shows matching percentage and missing skills for each job

---

## 🔧 **System Components & Tools**

| Layer          | Technology       | Purpose |
|----------------|------------------|---------|
| **Frontend**   | Streamlit        | UI for uploading resume and displaying results |
| **Backend / Logic** | Python + HuggingFace Transformers | Embedding generation & skill analysis |
| **Vector Database** | Qdrant (local via Docker) | Store and search resume embeddings |
| **Job Data Source** | In-memory list or JSON file | Store JD texts + (optional) cached embeddings |
| **Embedding Model** | `all-MiniLM-L6-v2` (SentenceTransformers) | Generate text embeddings |
| **Skill Extraction** | spaCy or keyword extraction | Identify matched and missing skills |

---

## 📁 **Workflow Breakdown**

### 🔹 1. Resume Upload
- User uploads PDF in Streamlit
- Text is parsed using:
  - `PyPDF2` if it's a text-based PDF
  - `pytesseract + pdf2image` if it's image-based
- Cleaned text is hashed (`SHA-256`) to prevent duplicates

### 🔹 2. Resume Embedding + Storage
- If hash not already in Qdrant:
  - Generate embedding using SentenceTransformer
  - Store in Qdrant with payload (`user_id`, `hash`, `timestamp`)
- If already present:
  - Reuse existing vector (skip re-upload)

### 🔹 3. JD Matching
- Use list of job descriptions (in code or from JSON)
- Optionally pre-embed JDs and cache them
- For each JD:
  - Compute cosine similarity with resume embedding
  - Extract overlapping and missing skills
  - Calculate a **match score**:
    ```
    match_score = 0.7 * cosine_similarity + 0.3 * skill_match_ratio
    ```

### 🔹 4. Display Top 10 Matches
- Show job title, score (%), and missing skills
- Optional: Add charts or interactivity for skills visualization

---

## 🛡️ **Optimizations & Best Practices**

| Concern         | Solution |
|------------------|----------|
| Duplicate resumes | Hash text content before storing |
| Performance with many JDs | Cache JD embeddings |
| Skill clarity | Use noun phrase extraction or skill keywords |
| User preferences | Add filters in Streamlit (`role`, `location`, `skills`) |
| Scalable Search | Switch to vector DB for JDs if they grow large |

---

## ✨ Optional Future Add-ons
- Save user sessions or results
- User feedback loop (“Was this job relevant?”)
- Personalized job learning paths (from missing skills)
- Filter by industry, experience level, or remote/onsite
- Add `pgvector` or `Qdrant cloud` for production-scale

---

## 🏁 Final Architecture Snapshot (Local Dev)

```plaintext
[ Streamlit Frontend ]
        │
        ▼
[ Resume Upload & Parse ]
        │
        ▼
[ Hash + Embed + Store in Qdrant ]
        │
        ▼
[ Compare to Local JD List (embedded) ]
        │
        ▼
[ Match %, Missing Skills, Rank Top 10 ]
        │
        ▼
[ Display Results to User (Interactive) ]
```

---

## ✅ Summary: MVP Goals — All Covered
- ✔️ Resume-based job recommendations
- ✔️ Matching % + missing skills
- ✔️ Lightweight vector DB with deduplication
- ✔️ No unnecessary overhead

---

Would you like a `starter repo scaffold` with:
- Docker Qdrant setup
- Streamlit starter app
- Resume parser + deduplicator
- Matching engine?
```
job_recommender/
├── app.py                  # Streamlit frontend
├── data/
│   └── job_listings.json   # Sample JDs
├── resumes/
│   └── (uploaded resumes)
├── utils/
│   ├── parser.py           # Resume parsing (PDF + OCR)
│   ├── embeddings.py       # Embedding + hashing logic
│   ├── jobs.py             # JD handling, embedding
│   ├── matcher.py          # Matching + scoring
│   └── qdrant_client.py    # Qdrant connection helpers
├── cache/
│   └── jd_embeddings.pkl   # Cached JD embeddings (optional)
└── requirements.txt        # Dependencies
```