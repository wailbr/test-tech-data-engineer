from fastapi import FastAPI, HTTPException
from datetime import datetime
from pymongo.errors import PyMongoError
from pymongo import UpdateOne

from app.database import articles_col, predictions_col
from app.model import predict_label
from app.schema import TextInput, PredictionOutput

app = FastAPI(
    title="API de détection de toxicité",
    description="Cette API prédit si un texte est toxique ou non, avec un score de confiance, et stocke les résultats dans MongoDB.",
    version="1.0.0",
)

@app.get("/")
def home():
    """Page d'accueil"""
    return {"message": "Bienvenue sur l’API de détection de toxicité 🚀"}

@app.post("/predict", response_model=PredictionOutput)
def predict_toxicity(input_data: TextInput):
    """Analyse un texte unique"""
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide.")
    try:
        label, score = predict_label(input_data.text)

        prediction_doc = {
            "text": input_data.text,
            "label": label,
            "score": float(score),
            "date": datetime.utcnow(),
            "url": str(input_data.url) if input_data.url else None
        }
        predictions_col.insert_one(prediction_doc)

        return PredictionOutput(
            label=label,
            score=score,
            date=prediction_doc["date"],
            url=input_data.url
        )

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Erreur MongoDB : {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")

@app.post("/process_all")
def process_all_articles():
    """
    Parcourt tous les articles non encore analysés dans MongoDB,
    exécute la prédiction, et stocke les résultats dans 'predictions'.
    """
    try:
        articles = list(articles_col.find({"analyzed": {"$ne": True}}))
        if not articles:
            return {"message": "Aucun nouvel article à analyser."}

        bulk_updates = []
        analyzed_count = 0

        for art in articles:
            text = art.get("content", "")
            url = art.get("url", "")
            source = art.get("source", "")
            title = art.get("title", "")

            if not text.strip():
                continue

            label, score = predict_label(text)

            prediction_doc = {
                "source": source,
                "title": title,
                "url": url,
                "text": text,
                "label": label,
                "score": float(score),
                "date": datetime.utcnow(),
            }
            predictions_col.insert_one(prediction_doc)

            bulk_updates.append(UpdateOne({"_id": art["_id"]}, {"$set": {"analyzed": True}}))
            analyzed_count += 1

        if bulk_updates:
            articles_col.bulk_write(bulk_updates)

        return {
            "message": f"{analyzed_count} articles analysés avec succès ✅",
            "details": f"Résultats enregistrés dans la collection 'predictions'."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")

@app.get("/health")
def health_check():
    """Vérifie que l'API fonctionne"""
    return {"status": "OK", "message": "API en ligne et fonctionnelle"}
