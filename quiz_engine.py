import json
import requests
import streamlit as st
import os
import re
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def fix_common_json_issues(text):
    fixed = re.sub(r'("type":\s*"(?:MCQ|Fill-in-the-blank)")\s*("answer":)', r'\1, \2', text)
    fixed = re.sub(r'("options":\s*\[[^\]]+\])\s*("answer":)', r'\1, \2', fixed)
    return fixed

def chunk_text(text, chunk_size=200):
    """Split text into chunks of ~chunk_size words"""
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def retrieve_relevant_chunks(text, query, top_k=3):
    """Perform RAG-style retrieval using semantic similarity"""
    chunks = chunk_text(text)
    chunk_embeddings = model.encode(chunks)
    query_embedding = model.encode([query])[0]

    index = faiss.IndexFlatL2(chunk_embeddings.shape[1])
    index.add(np.array(chunk_embeddings))

    distances, indices = index.search(np.array([query_embedding]), top_k)
    return [chunks[i] for i in indices[0]]

def generate_questions_from_text(text, num_questions=5, difficulty="Medium", question_type="MCQ"):
    if not OPENROUTER_API_KEY:
        st.error("OpenRouter API key is missing.")
        return None

    # Use a general-purpose query to fetch relevant chunks for question generation
    query = f"Generate {num_questions} {question_type} questions of {difficulty} difficulty"
    relevant_chunks = retrieve_relevant_chunks(text, query, top_k=3)
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
Generate exactly {num_questions} {difficulty.lower()}-level {question_type} questions based on the following context:

{context}

Rules:
- You MUST return EXACTLY {num_questions} questions. Do NOT return more or fewer.
- If type is "MCQ", DO NOT use any blanks or underscores. Write full sentences and include 4 options.
- If type is "Fill-in-the-blank", use underscores (______) to represent missing words in the question.
- Use only DOUBLE QUOTES for JSON formatting.
- For MCQ, include an "options" list with EXACTLY 4 items, and an "answer" key with the correct one.
- For Fill-in-the-blank, include the correct word/phrase in "answer".

Return ONLY in this exact JSON format:
[
  {{
    "question": "...",
    "type": "{question_type}",
    "options": ["...","...","...","..."], // Only for MCQ
    "answer": "..."
  }}
]
"""
    if question_type == "MCQ":
        system_prompt = (
            "You are a helpful assistant that generates ONLY multiple-choice questions (MCQs) "
            "in strict JSON format. Each question must have 4 options and a correct answer. "
            "Do NOT include fill-in-the-blank questions."
        )
    elif question_type == "Fill-in-the-blank":
        system_prompt = (
            "You are a helpful assistant that generates ONLY fill-in-the-blank questions "
            "in strict JSON format. Do NOT include multiple-choice questions."
        )
    else:
        system_prompt = "You are a helpful assistant that generates quiz questions in strict JSON."


    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://your-app-domain.com",
        "Content-Type": "application/json"
    }

    data = {
    "model": "anthropic/claude-3-haiku", 
    "messages": [
        {"role": "system", "content": "You are a helpful assistant that generates quiz questions in strict JSON."},
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.7,
    "top_p": 0.9
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        fixed_content = fix_common_json_issues(content)

        try:
            questions = json.loads(fixed_content)
            if isinstance(questions, list) and len(questions) > 0:
                for q in questions:
                    q["answer"] = q.get("answer", "No answer provided")
                return questions
        except json.JSONDecodeError:
            st.error("Failed to parse JSON from response:\n\n" + content)
            return None

    except requests.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None
