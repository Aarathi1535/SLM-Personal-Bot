# parser.py
import json

def extract_resume_data(json_path="data/resume.json"):
    with open(json_path, "r") as f:
        resume_data = json.load(f)

    # You can flatten this into chunks of text for embedding
    text_chunks = []

    # Basic fields
    if "name" in resume_data:
        text_chunks.append(f"My name is {resume_data['name']}")
    if "summary" in resume_data:
        text_chunks.append(resume_data["summary"])
    if "skills" in resume_data:
        text_chunks.append("Skills: " + ", ".join(resume_data["skills"]))
    
    # Experience
    for exp in resume_data.get("experience", []):
        chunk = f"{exp['role']} at {exp['company']} from {exp['duration']}. {exp['description']}"
        text_chunks.append(chunk)

    # Education
    for edu in resume_data.get("education", []):
        chunk = f"Studied {edu['degree']} at {edu['institution']} ({edu['year']})"
        text_chunks.append(chunk)

    # Projects
    for project in resume_data.get("projects", []):
        chunk = f"Project: {project['title']}. {project['description']}"
        text_chunks.append(chunk)

    return text_chunks
