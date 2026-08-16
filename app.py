import warnings
warnings.filterwarnings("ignore")

import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


HF_API_KEY    = os.getenv("HF_API_KEY")
NEO4J_URI     = os.getenv("NEO4J_URI")
NEO4J_USER    = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


HF_MODEL = "moonshotai/Kimi-K3"


hf_client = InferenceClient(token=HF_API_KEY)
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))



def query_graph(symptoms: list[str]):
    with driver.session() as session:
        result = session.run("""
            MATCH (s:Symptom)<-[:HAS_SYMPTOM]-(c:Condition)-[:TREATS_WITH]->(m:Medicine)
            WHERE toLower(s.name) IN $symptoms
            WITH c, collect(DISTINCT s.name) AS matched_symptoms,
                 collect(DISTINCT m.name) AS medicines
            RETURN c.name AS condition,
                   matched_symptoms,
                   medicines,
                   size(matched_symptoms) AS match_score
            ORDER BY match_score DESC
        """, symptoms=[s.lower() for s in symptoms])
        return [record.data() for record in result]

def build_context(graph_results: list) -> str:
    if not graph_results:
        return "No matching conditions found in the knowledge base."
    lines = []
    for r in graph_results:
        lines.append(
            f"Condition: {r['condition']}\n"
            f"  Matched symptoms: {', '.join(r['matched_symptoms'])}\n"
            f"  Suggested medicines: {', '.join(r['medicines'])}"
        )
    return "\n\n".join(lines)

def extract_symptoms(text: str) -> list[str]:
    known_symptoms = [
        "fever", "chills", "body ache", "weakness", "headache",
        "runny nose", "sneezing", "dry cough", "cough", "mucus",
        "chest congestion", "blocked nose", "facial pain", "joint stiffness",
        "muscle pain", "restlessness", "anxiety", "thirst", "loss of appetite",
        "high temperature", "watery discharge", "thick discharge",
        "sore throat", "fatigue", "shortness of breath", "chest pain",
        "nausea", "vomiting", "diarrhea", "rash", "swelling", "pain",
        "inflammation", "infection", "chill", "sweating", "dehydration",
        "nasal obstruction", "loss of smell", "hoarseness", "paralysis",
        "trembling", "palpitations", "insomnia", "sleeplessness"
    ]
    text_lower = text.lower()
    found = [s for s in known_symptoms if s in text_lower]
    if "dry cough" in found and "cough" in found:
        found.remove("cough")
    return found


def ask_llm(chat_history: list, user_input: str, context: str) -> str:
    system_prompt = (
        "You are a careful and caring homeopathic health-information assistant. "
        "Use ONLY the provided knowledge base to answer. "
        "Match the user's symptoms or condition with the information in the knowledge base "
        "and mention only medicines explicitly associated with that condition. "
        "Never invent medicines, symptoms, conditions, dosages, potencies, or treatments. "
        "Do not diagnose the user or make personalized prescriptions. "
        "If the requested information is not present in the knowledge base, clearly say and tell to consult a professional"
        "Never write directly you are referring a knowledge base"
        "that you do not have enough information to answer. "
        "Keep responses concise, clear, and easy to understand. "
        "Do not present homeopathy as a guaranteed cure. "
        "Please remember that you should never ask a user to refer a qualified physician, the dataset you refer to is already made by a doctor"
        "professional before taking any medicine."

    )

    # Build messages for chat-completion style
    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history (already in {"role","content"} format from client)
    for msg in chat_history:
        messages.append(msg)

    # Add the current user message with context
    augmented = (
        f"Knowledge base context:\n{context}\n\n"
        f"User question: {user_input}"
    )
    messages.append({"role": "user", "content": augmented})

    response = hf_client.chat_completion(
        model=HF_MODEL,
        messages=messages,
        max_tokens=512,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input   = data.get("message", "").strip()
    chat_history = data.get("history", [])   # list of {role, content}

    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    # Symptom detection + graph query
    symptoms = extract_symptoms(user_input)
    graph_results = query_graph(symptoms) if symptoms else []
    context = build_context(graph_results)

    detected_conditions = [r["condition"] for r in graph_results] if graph_results else []

    try:
        reply = ask_llm(chat_history, user_input, context)
    except Exception as e:
        reply = f"⚠️ LLM error: {str(e)}"

    return jsonify({
        "reply": reply,
        "detected_symptoms": symptoms,
        "matched_conditions": detected_conditions,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)