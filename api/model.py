from transformers import pipeline

print("Chargement du modèle anglais (sentiment-analysis)...")

try:
    classifier = pipeline("sentiment-analysis")
except Exception as e:
    print("⚠️ Erreur lors du chargement du modèle :", e)
    classifier = None

def predict_label(text: str):
    if not classifier:
        raise RuntimeError("Le modèle n’a pas pu être chargé correctement.")

    try:
        result = classifier(text)[0]
        label = result.get("label", "").lower()
        score = float(result.get("score", 0.0))

        if "neg" in label:
            return "toxique", score
        elif "pos" in label:
            return "non toxique", score
        else:
            return "neutre", score

    except Exception as e:
        print("❌ Erreur dans predict_label :", e)
        return "erreur", 0.0
