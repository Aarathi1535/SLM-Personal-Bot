# utils/responder.py

import os
import requests
from dotenv import load_dotenv
from utils.embedder import search_context

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_response(prompt, category=None):
    context_chunks = search_context(prompt, k=5)
    context = "\n".join(context_chunks)

    # Customize system message based on category
    category_instructions = {
        "cold_email": "Write a professional cold email using the resume and idea context.",
        "application_answer": "Write an answer for a job application question using the resume context.",
        "linkedin_dm": "Draft a LinkedIn DM using a friendly yet professional tone based on resume and ideas.",
        "startup_related": "Help with startup tasks or ideas using the provided context."
    }

    extra_instruction = category_instructions.get(category, "")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a personal assistant helping a job applicant based on their resume and startup ideas. "
                + "Draft a" + extra_instruction + "based on my resume data and take the company's name or other details from the user as per the category chosen. Keep it very short and concise and to the point yet impactful."
            )
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nNow respond to this prompt:\n{prompt}"
        }
    ]


    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"
