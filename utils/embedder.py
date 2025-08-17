# utils/embedder.py

import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(dimension)

# In-memory store
chunk_texts = []

# Step 1: Load resume.json from data folder
resume_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'resume.json')
with open(resume_path, 'r', encoding='utf-8') as f:
    resume_data = json.load(f)

# Step 2: Flatten JSON
def flatten_resume(resume_data):
    parts = []

    parts.append(f"Name: {resume_data.get('name')}")
    parts.append(f"Email: {resume_data.get('email')}")
    parts.append(f"Phone: {resume_data.get('phone')}")
    parts.append(f"Summary: {resume_data.get('summary')}")

    for edu in resume_data.get("education", []):
        parts.append(f"Education: {edu['degree']} at {edu['institution']} with CGPA {edu['cgpa']}")

    for exp in resume_data.get("experience", []):
        parts.append(f"Experience at {exp['company']} as {exp['role']} from {exp['start_date']} to {exp['end_date']}")
        for a in exp.get("achievements", []):
            parts.append(f" - {a}")

    for proj in resume_data.get("projects", []):
        parts.append(f"Project: {proj['name']}")
        for desc in proj.get("description", []):
            parts.append(f" - {desc}")
        parts.append(f"Technologies used: {', '.join(proj.get('technologies', []))}")

    for cert in resume_data.get("certifications", []):
        parts.append(f"Certification: {cert}")


    for pub in resume_data.get("publications", []):
        parts.append(f"Publication: {pub['title']} at {pub['conference']}")

    for skill in resume_data.get("technical_skills", []):
        parts.append(f"Skill: {skill}")

    return parts

# Step 3: Embed and store
def embed_data():
    global chunk_texts
    chunk_texts = flatten_resume(resume_data)
    embeddings = model.encode(chunk_texts)
    index.add(np.array(embeddings))

# Step 4: Search function
def search_context(query, k=5):
    query_vector = model.encode([query])
    distances, indices = index.search(np.array(query_vector), k)
    return [chunk_texts[i] for i in indices[0] if i < len(chunk_texts)]

# Initialize on import
embed_data()
