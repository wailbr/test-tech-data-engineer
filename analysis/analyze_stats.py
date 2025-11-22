#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse statistique et visuelle de la toxicité :
 - Lecture des prédictions dans MongoDB
 - Calcul des % légèrement et très toxiques par site
 - Graphiques pro : barres comparatives + camembert global
 - Sauvegarde des résultats et d'un résumé analytique
"""

import datetime
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# =========================
# Connexion MongoDB
# =========================
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "articles_db"
PREDICTIONS_COLLECTION = "predictions"
STATS_COLLECTION = "toxicity_stats"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
predictions_col = db[PREDICTIONS_COLLECTION]
stats_col = db[STATS_COLLECTION]

# =========================
# Lecture des données
# =========================
predictions = list(predictions_col.find({}, {"_id": 0}))

if not predictions:
    print("⚠️ Aucune donnée trouvée dans la collection 'predictions'.")
    exit()

df = pd.DataFrame(predictions)
print(f"✅ {len(df)} prédictions chargées depuis MongoDB.")

# =========================
# Classification
# =========================
def classify_toxicity(row):
    if row["label"] != "toxique":
        return "non toxique"
    score = float(row.get("score", 0))
    if score >= 0.80:
        return "très toxique"
    elif score >= 0.50:
        return "légèrement toxique"
    else:
        return "faible"

df["niveau_toxicite"] = df.apply(classify_toxicity, axis=1)

# =========================
# Agrégation par source
# =========================
stats = (
    df.groupby("source")
      .apply(lambda x: pd.Series({
          "total": len(x),
          "pct_legèrement_toxique": round((x["niveau_toxicite"] == "légèrement toxique").mean() * 100, 2),
          "pct_très_toxique": round((x["niveau_toxicite"] == "très toxique").mean() * 100, 2),
          "pct_non_toxique": round((x["niveau_toxicite"] == "non toxique").mean() * 100, 2)
      }))
      .reset_index()
)

print("\n=== Résumé par site ===")
print(stats)

# =========================
# STYLE PRO (Seaborn)
# =========================
sns.set_theme(style="whitegrid", font_scale=1.2)
palette = {
    "non toxique": "#4CAF50",          # vert
    "légèrement toxique": "#FFB300",   # orange
    "legèrement toxique": "#FFB300",   # (fallback sans accent)
    "très toxique": "#E53935"          # rouge
}

# =========================
# BARRES COMPARATIVES
# =========================
bar_data = pd.melt(
    stats,
    id_vars=["source"],
    value_vars=["pct_non_toxique", "pct_legèrement_toxique", "pct_très_toxique"],
    var_name="niveau",
    value_name="pourcentage"
)

# Normalisation des labels (accents)
bar_data["niveau"] = (
    bar_data["niveau"]
    .str.replace("legèrement", "légèrement", regex=False)
    .str.replace("pct_", "")
    .str.replace("_", " ")
)

plt.figure(figsize=(12, 6))
sns.barplot(
    data=bar_data,
    x="source",
    y="pourcentage",
    hue="niveau",
    palette=palette
)
plt.title("Taux de toxicité par site", fontsize=16, fontweight="bold")
plt.xlabel("Source")
plt.ylabel("Pourcentage (%)")
plt.xticks(rotation=30, ha="right")
plt.legend(title="Niveau de toxicité")
plt.tight_layout()
plt.savefig("comparaison_toxicite_sites.png", dpi=300)
plt.show()
print("📊 Graphique comparatif enregistré sous 'comparaison_toxicite_sites.png'")

# =========================
# CAMEMBERT GLOBAL
# =========================
global_counts = df["niveau_toxicite"].value_counts()
colors = [palette.get(k, "#9E9E9E") for k in global_counts.index]

plt.figure(figsize=(6, 6))
plt.pie(
    global_counts,
    labels=global_counts.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=colors,
    explode=[0.02] * len(global_counts)
)
plt.title("Répartition globale de la toxicité des articles", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("repartition_globale_toxicite.png", dpi=300)
plt.show()
print("🥧 Camembert global enregistré sous 'repartition_globale_toxicite.png'")




# =========================
# CAMEMBERT STYLE AXONE DATA
# =========================
global_counts = df["niveau_toxicite"].value_counts()

# Palette Axone Data stylisée
palette_axone = {
    "non toxique": "#003366",         # bleu foncé (Axone)
    "légèrement toxique": "#00B0F0",  # bleu clair
    "très toxique": "#D9D9D9"         # gris neutre
}

colors = [palette_axone.get(k, "#CCCCCC") for k in global_counts.index]

plt.figure(figsize=(7, 7))
wedges, texts, autotexts = plt.pie(
    global_counts,
    labels=global_counts.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=colors,
    pctdistance=0.85,
    wedgeprops={"linewidth": 1, "edgecolor": "white"}
)

# Cercle blanc central pour effet "donut"
centre_circle = plt.Circle((0, 0), 0.70, fc="white")
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Titres et style
plt.title("Répartition globale de la toxicité (Style Axone Data)", fontsize=14, fontweight="bold", color="#003366")
plt.tight_layout()
plt.savefig("repartition_globale_toxicite_axone.png", dpi=300, facecolor="white")
plt.show()

print("🔵 Camembert 'Axone Data' enregistré sous 'repartition_globale_toxicite_axone.png'")


# =========================
# STOCKAGE + INTERPRÉTATION
# =========================
snapshot = {
    "created_at": datetime.datetime.utcnow(),
    "results": stats.to_dict(orient="records")
}
stats_col.insert_one(snapshot)
print(f"✅ Résultats enregistrés dans MongoDB ({STATS_COLLECTION})")

# =========================
# INTERPRÉTATION AUTOMATIQUE
# =========================
top_site = stats.sort_values("pct_très_toxique", ascending=False).iloc[0]
text = f"""
RAPPORT D’ANALYSE – {datetime.date.today().strftime("%d/%m/%Y")}

1️⃣ Site le plus toxique : {top_site['source']}
   → Taux de textes très toxiques : {top_site['pct_très_toxique']} %
   → Taux de textes légèrement toxiques : {top_site['pct_legèrement_toxique']} %

💡 INTERPRÉTATION :
Les sites présentant les taux les plus élevés de toxicité sont susceptibles d’utiliser un ton plus polémique,
des mots émotionnels ou polarisants. À l’inverse, les médias comme GameSpot ou France 3 montrent des contenus
majoritairement neutres ou informatifs.

📈 UTILITÉ :
Ces indicateurs peuvent servir de base pour un tableau de bord de suivi de la qualité rédactionnelle,
ou pour identifier les sources nécessitant une modération plus fine dans un pipeline de monitoring automatique.
"""

with open("rapport_analyse.txt", "w", encoding="utf-8") as f:
    f.write(text.strip())

print("\n🧠 Rapport automatique généré sous 'rapport_analyse.txt'")
