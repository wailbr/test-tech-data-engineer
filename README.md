🧠 NLP Toxicity Pipeline
Pipeline Scraping → NLP Classification → FastAPI → MongoDB → Docker

Ce projet implémente un pipeline complet d’ingénierie de données textuelles, depuis la collecte d’articles sur plusieurs sites d’actualité jusqu’à la détection automatique de toxicité et son exposition via une API FastAPI conteneurisée avec Docker.

Il s’agit d’un vrai projet Data Engineer regroupant :
✔ Web Scraping
✔ Stockage NoSQL (MongoDB)
✔ NLP (Modèle de toxicité)
✔ API REST
✔ Analyse statistique
✔ Dockerisation complète

📌 1. Architecture du projet



nlp-toxicity-pipeline/
│
├── scraping/           → Récupération des articles (BeautifulSoup)
│   ├── scraper.py
│   ├── .env.example
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── api/                → API FastAPI de classification toxicité
│   ├── app/
│   │   ├── api.py
│   │   ├── database.py
│   │   ├── model.py
│   │   ├── schema.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── analysis/           → Analyse statistique + Graphiques
│   ├── analyze_stats.py
│   ├── comparaison_toxicite_sites.png
│   ├── repartition_globale_toxicite.png
│   └── toxicite_sites.png
│
├── docs/               → Livrables finaux
│   ├── README_original.txt
│   ├── Rendu_Test_Technique.docx
│   └── Rendu_Test_Technique.pptx
│
├── data/               → Datasets (optionnel)
│
└── README.md           → Documentation principale

🕸️ 2. Scraping (Extract)

Le scraping récupère automatiquement des articles récents depuis plusieurs sites :

humanite.fr

gamespot.com

marianne.net

lemonde.fr

france24.com

franceinfo.fr

mediacites.fr

lepoint.fr

Chaque article contient :
✔ URL
✔ Titre
✔ Contenu textuel

Les données sont stockées dans MongoDB via docker-compose.

Lancer le scraping :
cd scraping
pip install -r requirements.txt
python scraper.py

🤖 3. NLP Toxicity Classification (Transform)

L’API utilise un modèle NLP (HuggingFace ou modèle custom) pour prédire si un texte est :

🔴 Très toxique

🟠 Légèrement toxique

🟢 Non toxique

Chaque prédiction est stockée dans MongoDB avec :
✔ texte
✔ prédiction
✔ score
✔ timestamp

🌐 4. API FastAPI (Load)

L’API expose un endpoint principal :

POST /predict

Input :

{
  "text": "Contenu textuel ici..."
}


Output :

{
  "prediction": "toxic",
  "confidence": 0.92
}

Lancer l'API :
cd api
uvicorn app.api:app --reload

📊 5. Analyse statistique

Le script analyze_stats.py :

Calcule le pourcentage de toxicité par site

Génère des graphiques (PNG)

Stocke les résultats dans MongoDB

Produit une interprétation finale

Générer les statistiques :
cd analysis
python analyze_stats.py


Graphiques :

comparaison_toxicite_sites.png

repartition_globale_toxicite.png

toxicite_sites.png

🐳 6. Déploiement Docker
Lancer toute l’infrastructure :
docker compose up --build


L’API sera disponible sur :
👉 http://localhost:8000

🧰 7. Technologies utilisées

Python 3.x

BeautifulSoup

FastAPI

MongoDB

Uvicorn

Transformers / NLP

Pandas, Matplotlib, Seaborn

Docker & Docker Compose

🎓 8. Compétences démontrées

✔ Web Scraping robuste
✔ Pipeline ETL complet
✔ Création API REST
✔ Traitement NLP
✔ Visualisation Data
✔ Base de données NoSQL
✔ Conteneurisation Docker
✔ Architecture projet propre et modulaire

👤 Auteur

Wail Brimesse
Bachelor Data & IA – ECE Paris
Recherche : Stage 6 mois (Data Engineer / Data Analyst / Data Scientist) – Mars 2026

🚀 9. Améliorations possibles

Système de retries + proxy pour scraping

Dashboard Streamlit

CI/CD GitHub Actions

Déploiement cloud (AWS / Render / Railway)

Modèle NLP entraîné sur mesure
