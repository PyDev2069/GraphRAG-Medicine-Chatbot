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
# Create virtual environment
python -m venv venv

# Activate virtual environment
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
# Neo4j AuraDB Configuration
NEO4J_URI=neo4j+s://<your-aura-db-id>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<your-auradb-password>

# LLM Configuration
LLM_API_KEY=<your-llm-api-key>
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

## 🧠 How It Works
1. **Knowledge Graph Ingestion (`load_graph.py`)**: Parses structured data from `homeopathy_dataset.json` and builds a semantic graph database in Neo4j AuraDB.
2. **Graph Querying & Context Retrieval (`app.py`)**: When a user submits a prompt via the web interface (`index.html`), the backend searches the Neo4j graph for related medical nodes, symptoms, and remedies.
3. **LLM Generation**: The retrieved graph context is injected into the LLM prompt template, allowing the model to generate accurate answers grounded strictly in the homeopathy dataset.

## ⚠️ Disclaimer
This chatbot is an AI-powered educational and research tool exploring GraphRAG applications in alternative medicine. It does not provide professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.
