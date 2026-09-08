# Homeopathic Medicine Chatbot (GraphRAG)

A Flask-based web application that utilizes a Large Language Model (LLM) and Neo4j AuraDB to provide intelligent, context-aware answers about homeopathic medicine using GraphRAG (Graph Retrieval-Augmented Generation).

## 📁 Project Structure

```text
HOMEOPATHIC MEDICINE CH.../
│
├── static/                 # Front-end asset files
│   ├── css/                # Stylesheets for web styling
│   └── js/                 # Client-side JavaScript for handling chat UI
│
├── templates/              # HTML views rendered by Flask
│   └── index.html          # Main web interface for the chatbot
│
├── .env                    # Environment variables (API keys & DB credentials)
├── .gitignore              # Specifies intentionally untracked files to ignore
├── app.py                  # Main Flask backend application (LLM & AuraDB integration)
├── chatbot.py              # Legacy Command Line Interface (CLI) version
├── homeopathy_dataset.json # Knowledge base containing raw medical data
├── load_graph.py           # Script to parse JSON and populate Neo4j AuraDB
└── requirements.txt        # Python package dependencies
```

## 🧠 How It Works

**1. Knowledge Graph Ingestion**
- The `load_graph.py` script parses structured medical data from `homeopathy_dataset.json` and creates a semantic graph database in Neo4j AuraDB
- Three node types are created: Conditions, Symptoms, and Medicines
- Relationships are established: Conditions have associated Symptoms and Treatments (Medicines)

**2. User Query Processing**
- When a user submits a message via the web interface, the system extracts symptom keywords from the input
- A Cypher query searches the Neo4j graph to find matching conditions, related symptoms, and recommended medicines
- Results are scored based on symptom overlap and returned in order of relevance

**3. Context-Augmented LLM Response**
- Retrieved graph context (conditions, symptoms, and medicines) is formatted and injected into the LLM prompt
- The LLM uses this grounded context to generate accurate, knowledge-base-aware responses
- Responses remain strictly aligned with the homeopathy dataset without fabrication

**4. Chat Interface**
- The Flask backend serves a web-based chat interface
- User messages and chat history are maintained for multi-turn conversations
- Detected symptoms and matched conditions are returned alongside LLM responses for transparency

## 🛠️ Prerequisites

Before setting up the project, ensure you have the following installed:
- Python 3.10 or higher
- A running instance of [Neo4j AuraDB](https://neo4j.com) (Free tier works perfectly)
- An API Key from your chosen LLM provider (e.g., OpenAI, Anthropic, or Groq)

## 🚀 Installation & Setup

Follow these steps to get the application running locally:

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd homeopathic-medicine-chatbot
```

### 2. Set Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named `.env` in the root directory and add your credentials:
```env
NEO4J_URI=neo4j+s://<your-aura-db-id>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<your-auradb-password>

HF_API_KEY=<your-llm-api-key>
```

### 5. Load the Knowledge Graph
Populate your Neo4j instance with the homeopathic dataset by running the data loader script:
```bash
python load_graph.py
```

### 6. Run the Application
Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000` to interact with the chatbot interface.

## ⚠️ Disclaimer
This chatbot is an AI-powered educational and research tool exploring GraphRAG applications in alternative medicine. It does not provide professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional before taking any medicine.
