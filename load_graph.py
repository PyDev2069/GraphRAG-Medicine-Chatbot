from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()
# --- Your connection details ---
URI = os.getenv("NEO4J_URI") # AuraDB URI, or "bolt://localhost:7687" for local
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# --- Your dataset ---
data = [
{
    "condition": "Typhoid",
    "symptoms": ["extreme weakness", "loss of appetite", "rose spots", "headache", "prolonged fever"],
    "medicines": [
      "Aconitum Napellus",
      "Gelsemium",
      "Taraxacum",
      "Apocynum Cannabinum",
      "Baptisia Tinctoria"
    ]
  },
  {
    "condition": "Hectic fever",
    "symptoms": ["wide temperature swings", "heavy sweating", "shivering", "dehydration"],
    "medicines": [
      "Abrotanum",
      "Acetic Acid",
      "Aconitum Napellus",
      "Belladonna",
      "Arsenicum album"
    ]
  },
  {
    "condition": "Hay fever",
    "symptoms": ["frequent sneezing", "watery eyes", "runny nose", "itchy throat"],
    "medicines": [
      "Allium Cepa",
      "Natrum Muriaticum",
      "Psorinum",
      "Tuberculinum-Bacillinum",
      "Histaminum"
    ]
  },
  {
    "condition": "Intermittent fever",
    "symptoms": ["temperature fluctuation", "headache", "digestive discomfort", "chils/sweating"],
    "medicines": [
      "Apis Mellifica",
      "Petroselinum",
      "Eupatorium Perfoliatum",
      "Ipecacuanha",
      "Lac Defloratum"
    ]
  },
  {
    "condition": "Pneumonia",
    "symptoms": ["fever", "chills", "shortness of breath", "chest pain"],
    "medicines": [
      "Chelidonium Majus",
      "Lycopodium Clavatum",
      "Hyoscyamus Niger",
      "Ranunculus Bulbosus",
      "Sanguinaria"
    ]
  },
  {
    "condition": "Malaria",
    "symptoms": ["high fever", "chills", "headache", "gastrointestinal issues"],
    "medicines": [
      "Cinchona (China)",
      "Terebinth",
      "Crotalus Horridus",
      "Arsenicum Album",
      "Chininum Sulphuricum"
    ]
  },
  {
    "condition": "Influenza",
    "symptoms": ["fever", "body ache", "fatigue", "headache","sore thorat"],
    "medicines": [
      "Camphora",
      "Eupatorium Perfoliatum",
      "Ipecacuanha",
      "Gelsemium",
      "Oscillococcinum"
    ]
  },
  {
    "condition": "Whooping cough",
    "symptoms": ["uncontrolled coughing", "runny nose", "stuffy nose", "watery eyes"],
    "medicines": [
      "Ambra Grisea",
      "Drosera Rotundifolia",
      "Kali Bromatum",
      "Cuprum Metallicum",
      "Antimony Crudum"
    ]
  },
  {
    "condition": "Measles",
    "symptoms": ["high fever", "sore throat", "koplik spots", "conjunctivitis"],
    "medicines": [
      "Apis Mellifica",
      "Drosera Rotundifolia",
      "Kali Carbonicum",
      "Eupatorium Perfoliatum",
      "Camphora"
    ]
  },
  {
    "condition": "Scarlet fever",
    "symptoms": ["high fever", "sore throat", "fatigue", "nausea", "rashes","strawberry tongue"],
    "medicines": [
      "Belladonna",
      "Mercurius Biniodide",
      "Dulcamara",
      "Phytolacca",
      "Apis Mellifica"
    ]
  },
  {
    "condition": "Laryngitis",
    "symptoms": ["throat discomfort", "voice change", "cough", "irritation"],
    "medicines": [
      "Allium Cepa",
      "Selenium",
      "Aconitum",
      "Argentum Nitricum",
      "Causticum"
    ]
  },
  {
    "condition": "Acute Bronchitis",
    "symptoms": ["cough with mucus", "sore throat", "breathing discomfort", "fatigue"],
    "medicines": [
      "Sanguinaria",
      "Pulsatilla",
      "Dulcamara",
      "Antimonium Tartaricum",
      "Ipecacuanha"
    ]
  },
  {
    "condition": "Croup",
    "symptoms": ["runny nose", "sneezing", "mild fever", "lethargy"],
    "medicines": [
      "Aconitum Napellus",
      "Kali Bichromicum",
      "Hepar Sulphuris",
      "Mercurius Cyanide",
      "Acetic Acid"
    ]
  },
  {
    "condition": "Tonsillitis",
    "symptoms": ["swollen tonsil", "painful swallowing", "fever", "sore thorat"],
    "medicines": [
      "Baryta Carbonica",
      "Capsicum",
      "Lachesis",
      "Mercurius",
      "Sabadilla"
    ]
  },
  {
    "condition": "Diphtheria",
    "symptoms": ["breathing difficulty", "pseudomembrane", "nasal discharge", "sore thorat"],
    "medicines": [
      "Kali Bichromicum",
      "Crotalus Horridus",
      "Causticum",
      "Lachesis",
      "Diphtherinum"
    ]
  },
  {
    "condition": "Pleurisy",
    "symptoms": ["chest pain", "shortness of breath", "pain radiation to neck,back", "relief by holding breath"],
    "medicines": [
      "Ranunculus Bulbosus",
      "Sabadilla",
      "Carbo Animalis",
      "Abrotanum",
      "Arnica Montana"
    ]
  },
  {
    "condition": "Mammary Abscess",
    "symptoms": ["painful lump in breast", "swelling", "fever", "nipple discharge"],
    "medicines": [
      "Phytolacca",
      "Graphites",
      "Silicea",
      "Bryonia Alba",
      "Belladonna"
    ]
  },
  {
    "condition": "Mumps",
    "symptoms": ["swollen glands", "difficulty eating", "fever", "headache"],
    "medicines": [
      "Mercurius",
      "Pulsatilla",
      "Belladonna",
      "Phytolacca Decandra",
      "Rhus Toxicodendron"
    ]
  },
  {
    "condition": "Catarrh",
    "symptoms": ["stuffy nose", "mucus sensation in throat", "constant need for throat clearing", "headache"],
    "medicines": [
      "Allium Cepa",
      "Diphtherinum",
      "Drosera Rotundifolia",
      "Euphrasia",
      "Kali Bichromicum"
    ]
  },
  {
    "condition": "Pharyngitis",
    "symptoms": ["throat pain", "difficulty swallowing", "swollen tonsil", "voice change"],
    "medicines": [
      "Aesculus Hippocastanum",
      "Mercurius Biniodide",
      "Belladonna",
      "Hepar Sulphuris",
      "Phytolacca"
    ]
  },
  {
    "condition": "Nasal Polyps",
    "symptoms": ["nasal obstruction", "loss of smell", "facial pressure", "mucus sensation in throat"],
    "medicines": [
      "Allium Cepa",
      "Mercurius Biniodide",
      "Sanguinaria",
      "Thuja Occidentalis",
      "Calcarea Carbonica"
    ]
  },
  {
    "condition": "Asthma",
    "symptoms": ["nasal obstruction", "loss of smell", "facial pressure", "mucus sensation in throat"],
    "medicines": [
      "Arsenic Album",
      "Cannabis Sativa",
      "Lobelia Inflata",
      "Hepar Sulphuris",
      "Bromium"
    ]
  },
  {
    "condition": "Fever with bladder problems",
    "symptoms": ["weakness","high temperature","groin pain","involuntary urination"],
    "medicines": [
      "Aconitum Napellus",
      "Apis Melifera",
      "Belladonna",
      "Bryonia alba",
      "Cantharis Vesicatoria"
    ]
  },
  {
    "condition": "Fever with ear problems",
    "symptoms": ["weakness","noises","coldness"],
    "medicines": [
      "Lachesis Muta",
      "Kalium Bichromicum",
      "Calcarea Sulphurica",
      "Crotalus Horridus",
      "Lycopodium Clavatum"
    ]
  },
  {
    "condition": "Fever with limb problems",
    "symptoms": ["weakness","noises","coldness","cramps","numbness","lameness"],
    "medicines": [
      "Cocculus Indicus",
      "Pulsatilla Pratensis",
      "Carbo Animalis",
      "Sepia Officinalis",
      "Menyanthes Trifoliata"
    ]
  },
  {
    "condition": "Paralysis",
    "symptoms": ["paralysis","weakness","trembling","pain","intermittent fever"],
    "medicines": [
      "Silicea Terra",
      "Plumbum Metallicum",
      "Natrium Sulphuricum",
      "Sepia Officinalis",
      "Eupatorium Perfoliatum"
    ]
  },
  {
    "condition": "Fever and face",
    "symptoms": ["glassy appearance","weakness","red eyes","pain","discoloration"],
    "medicines": [
      "Aconitum Napellus",
      "Spongia Tosta",
      "Helleborus Niger",
      "Sepia Officinalis",
      "Carbo Animalis"
    ]
  },
  {
    "condition": "Alternating temperature",
    "symptoms": ["chillness","weakening","overheating","coldness","hot twitches"],
    "medicines": [
      "Agaricus Muscarius",
      "Allium Cepa",
      "Asterias Rubens",
      "Borax Veneta",
      "Chelidonium Majus"
    ]
  },
  {
    "condition": "Burning heat",
    "symptoms": ["weakening","overheating","hot twitches","high thirst"],
    "medicines": [
      "Agaricus Muscarius",
      "Sarracenia Purpurea",
      "Ignatia Amara",
      "Digitalis Purpurea",
      "Bufo Rana"
    ]
  },
  {
    "condition": "Paroxysm",
    "symptoms": ["emotional","outbursts","anger","fever","weakness","hyperactivity"],
    "medicines": [
      "Arnica Montana",
      "Menyanthes Trifoliata",
      "Ferrum Metallicum",
      "Nux Vomica",
      "Ignatia Amara"
    ]
  },
  {
    "condition": "Continued Fever",
    "symptoms": ["fever","weakness","continuos pain","continuos heat","continuos chill"],
    "medicines": [
      "Ammonium Carbonicum",
      "Calcarea Carbonica",
      "Hydrocyanicum Acidum",
      "Lycopus Virginicus",
      "Veratrum Viride"
    ]
  },
  {
    "condition": "Fever and drinking",
    "symptoms": ["water","coffee","tea","alcohol","beer","cold water","sore throat"],
    "medicines": [
      "Cantharis Vesicatoria",
      "Nux Vomica",
      "Sumbulus Moschatus",
      "Fluoricum Acidum",
      "Natrium Muriaticum"
    ]
  },
  {
    "condition": "Gastric fever",
    "symptoms": ["indigestion","stomach ache","weakness","burning"],
    "medicines": [
      "Aconitum Napellus",
      "Cantharis Vesicatoria",
      "Eupatorium Perfoliatum",
      "Muriaticum Acidum",
      "Rheum Palmatum"
    ]
  },
  {
    "condition": "Insidious fever",
    "symptoms": ["fever","continous heat","continuos cold","slow onset"],
    "medicines": [
      "Aceticum Acidum",
      "Arsenicum Album",
      "Cocculus Indicus",
      "Conium Maculatum",
      "Secale Cornutum"
    ]
  },
  {
    "condition": "Irritative fever",
    "symptoms": ["inflammation","irritation","infection","weakness","heat"],
    "medicines": [
      "Aceticum Acidum",
      "Arnica Montana",
      "Baptisia Tinctoria",
      "Cantharis Vesicatoria",
      "Podophyllum Peltatum"
    ]
  },
  {
    "condition": "Fever during menses",
    "symptoms": ["menses","periods","irritating","uterine"],
    "medicines": [
      "Aesculus Hippocastanum",
      "Bryonia Alba",
      "Carbo Animalis",
      "Cuprum Metallicum",
      "Kalium Bichromicum"
    ]
  },
  {
    "condition": "Unconscious",
    "symptoms": ["weakness","passing away","unconscious","paralysis"],
    "medicines": [
      "Caladium Seguinum",
      "Arsenicum Album",
      "Spigelia Anthelmia",
      "Chamomilla",
      "Stramonium"
    ]
  },
  {
    "condition": "Insomnia",
    "symptoms": ["sleeplessness","anxiety","stress","weakness"],
    "medicines": [
      "Baryta Carbonica",
      "Hyoscyamus Niger",
      "Aconitum Napellus",
      "Bryonia Alba",
      "Rhus Toxicodendron"
    ]
  },
  {
    "condition": "Puerbal fever",
    "symptoms": ["after child birth","female","weakness","weakness","foul smell","chill"],
    "medicines": [
      "Apis Mellifera",
      "Cimicifuga Racemosa",
      "Ignatia Amara",
      "Millefolium Herba",
      "Veratrum Viride"
    ]
  },
  {
    "condition": "Yellow Fever",
    "symptoms": ["haemorrahage","paleness","headache","weakness","heaviness","trembling"],
    "medicines": [
      "Carbo Vegetabilis",
      "Argentum Nitricum",
      "Camphora Officinalis",
      "Daphne Indica",
      "Lobelia Inflata"
    ]
  },
  {
    "condition": "Zymotic Fever",
    "symptoms": ["infection","fever","heat","inflammation"],
    "medicines": [
      "Anthracinum",
      "Berberis Vulgaris",
      "Hyoscyamus Niger",
      "Mercurius Solubilis",
      "Nux Moschata"
    ]
  },
  {
    "condition": "Palpitations",
    "symptoms": ["pulsating","anxiety","trembling","fever","heart problems"],
    "medicines": [
      "Aconitum Napellus",
      "Aesculus Hippocastanum",
      "Baryta Carbonica",
      "Crotalus Horridus",
      "Mercurius Solubilis"
    ]
  }
]

def load_data(driver, records):
    with driver.session() as session:

        # Create constraints (prevents duplicate nodes)
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Condition) REQUIRE c.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (s:Symptom) REQUIRE s.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:Medicine) REQUIRE m.name IS UNIQUE")

        for item in records:
            # Create Condition node
            session.run(
                "MERGE (c:Condition {name: $name})",
                name=item["condition"]
            )

            # Create Symptom nodes + relationships
            for symptom in item["symptoms"]:
                session.run("""
                    MERGE (s:Symptom {name: $symptom})
                    WITH s
                    MATCH (c:Condition {name: $condition})
                    MERGE (c)-[:HAS_SYMPTOM]->(s)
                """, symptom=symptom, condition=item["condition"])

            # Create Medicine nodes + relationships
            for medicine in item["medicines"]:
                session.run("""
                    MERGE (m:Medicine {name: $medicine})
                    WITH m
                    MATCH (c:Condition {name: $condition})
                    MERGE (c)-[:TREATS_WITH]->(m)
                """, medicine=medicine, condition=item["condition"])

        print("✅ Graph loaded successfully!")

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
load_data(driver, data)
driver.close()