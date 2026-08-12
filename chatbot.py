# this is a test CLI Edition of the code 

import warnings
warnings.filterwarnings("ignore")
import os
from neo4j import GraphDatabase
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.markdown import Markdown
from rich import print as rprint
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
GEMINI_API_KEY = ""
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# --- Init ---
console = Console()
client  = genai.Client(api_key=GEMINI_API_KEY)
driver  = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# --- Query Neo4j ---
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

# --- Build context string from graph results ---
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

# --- Extract symptoms from user input ---
def extract_symptoms(text: str) -> list[str]:
    known_symptoms = [
        "fever", "chills", "body ache", "weakness", "headache",
        "runny nose", "sneezing", "dry cough", "cough", "mucus",
        "chest congestion", "blocked nose", "facial pain", "joint stiffness",
        "muscle pain", "restlessness", "anxiety", "thirst", "loss of appetite",
        "high temperature", "watery discharge", "thick discharge"
    ]
    text_lower = text.lower()
    found = [s for s in known_symptoms if s in text_lower]
    # remove 'cough' if 'dry cough' already matched
    if "dry cough" in found and "cough" in found:
        found.remove("cough")
    return found

# --- Ask Gemini (new SDK) ---
def ask_gemini(chat_history: list, user_input: str, context: str) -> str:
    prompt = f"""You are a knowledgeable and caring homeopathic medicine assistant.
Use ONLY the information provided below from the knowledge base to answer the question.
Do not invent medicines or conditions not present in the data.
Always remind the user to consult a qualified homeopathic practitioner.

Knowledge base:
{context}

User question: {user_input}

Answer:"""

    chat_history.append({"role": "user", "parts": [{"text": prompt}]})

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=chat_history,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=1024,
        )
    )

    reply = response.text
    chat_history.append({"role": "model", "parts": [{"text": reply}]})
    return reply

# --- Main chat loop ---
def chat():
    console.print()
    console.print(Panel.fit(
        "[bold green]🌿 Homeopathic Assistant[/bold green]\n"
        "[dim]Powered by Neo4j Knowledge Graph + Google Gemini[/dim]",
        border_style="green"
    ))
    console.print("[dim]Describe your symptoms or ask a question. Type 'quit' to exit.[/dim]\n")

    chat_history = []

    while True:
        # User input
        console.print(Rule(style="dim"))
        user_input = console.input("[bold cyan]You:[/bold cyan] ").strip()

        if user_input.lower() in ("quit", "exit"):
            console.print("\n[bold green]Goodbye! Stay healthy 🌿[/bold green]\n")
            break

        if not user_input:
            continue

        # Symptom detection
        symptoms = extract_symptoms(user_input)
        if symptoms:
            console.print(
                f"[dim]  ✦ Detected symptoms: [italic]{', '.join(symptoms)}[/italic][/dim]"
            )
            graph_results = query_graph(symptoms)
            context = build_context(graph_results)

            # Show matched conditions as a subtle info line
            if graph_results:
                conditions = [r["condition"] for r in graph_results]
                console.print(
                    f"[dim]  ✦ Matched conditions: [italic]{', '.join(conditions)}[/italic][/dim]"
                )
        else:
            context = "No specific symptoms detected. Answering from general knowledge base context."

        # Gemini response
        with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
            reply = ask_gemini(chat_history, user_input, context)

        # Render reply as markdown inside a panel
        console.print()
        console.print(Panel(
            Markdown(reply),
            title="[bold green]🌿 Assistant[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))

    driver.close()

if __name__ == "__main__":
    chat()