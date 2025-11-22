from pymongo import MongoClient
import os

# URL de connexion à MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

# Nom de la base de données
DB_NAME = os.getenv("MONGO_DB", "articles_db")

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections utilisées
articles_col = db["articles"]
predictions_col = db["predictions"]
toxicity_stats_col = db["toxicity_stats"]
