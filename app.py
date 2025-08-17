from flask import Flask, request, jsonify, render_template
from utils.parser import extract_resume_data
from utils.embedder import embed_data
from utils.responder import generate_response
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/init", methods=["POST"])
def initialize():
    # ✅ Load resume JSON
    with open("data/resume.json") as f:
        resume = json.load(f)

    # Convert sections into readable strings
    resume_chunks = []

    resume_chunks.append(f"Name: {resume.get('name')}")
    resume_chunks.append(f"Email: {resume.get('email')}")

    for edu in resume.get("education", []):
        resume_chunks.append(f"Education: {edu['degree']} at {edu['institution']} ({edu['year']})")

    for exp in resume.get("experience", []):
        resume_chunks.append(
            f"Experience: {exp['title']} at {exp['company']} ({exp['duration']}) - {exp['description']}"
        )

    for skill in resume.get("skills", []):
        resume_chunks.append(f"Skill: {skill}")

    for proj in resume.get("projects", []):
        resume_chunks.append(f"Project: {proj['name']} - {proj['description']}")

    # ✅ Load idea chunks
    with open("data/ideas.json") as f:
        ideas = json.load(f)
    idea_chunks = [idea["description"] for idea in ideas]

    # ✅ Combine and embed all
    all_chunks = resume_chunks + idea_chunks
    embed_data(all_chunks)

    return {"status": "Resume (from JSON) and ideas embedded successfully."}

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("prompt", "")
    category = data.get("category", None)

    if not prompt.strip():
        return jsonify({"response": "Prompt is empty!"})

    response = generate_response(prompt, category)

    # Format response with line breaks (for display in frontend)
    formatted_response = response.replace("  ", "\n\n")

    return jsonify({"response": formatted_response})


if __name__ == "__main__":
    app.run(debug=True)
