import pandas as pd
import json

# Dictionnaire pour mappings personnalisés
reco_map = {
    "N": "Apporter un engrais azoté (urée ou nitrate d’ammonium)",
    "P": "Appliquer un engrais phosphaté (type superphosphate)",
    "K": "Utiliser un engrais riche en potassium (K₂SO₄ ou KCl)",
    "Ca": "Appliquer du nitrate de calcium ou du gypse",
    "Mg": "Appliquer un engrais foliaire MgSO₄ à 2%",
    "S": "Incorporer du sulfate d’ammonium ou du soufre élémentaire",
    "Fe": "Pulvériser du chélate de fer (Fe-EDDHA)",
    "Mn": "Appliquer un engrais foliaire au MnSO₄",
    "Zn": "Utiliser un engrais foliaire à base de ZnSO₄",
    "Cu": "Pulvériser un engrais cuivrique (sulfate de cuivre)",
    "B": "Appliquer du borax ou acide borique à faible dose",
    "Mo": "Incorporer du molybdate de sodium ou d’ammonium",
    "Cl": "Améliorer le drainage ou ajuster les apports KCl si nécessaire",
    "Co": "Enrober les semences avec sulfate de cobalt",
    "Ni": "Amender avec des traces de nitrate de nickel (rarement requis)"
}

# Charger le CSV existant
df = pd.read_csv("nutrient_deficiencies_dataset.csv")

# Ajouter diagnostic et recommandation
df["diagnostic"] = df["element"].apply(lambda e: f"Carence en {e}")
df["recommandation"] = df["element"].apply(lambda e: reco_map.get(e, "—"))

# Sauvegarder nouveau CSV
df.to_csv("deficiencies_enriched.csv", index=False)

# Exporter version JSON
json_records = df.to_dict(orient="records")
with open("deficiencies_dataset.json", "w", encoding="utf-8") as f:
    json.dump(json_records, f, indent=4, ensure_ascii=False)

print("✅ Dataset enrichi avec diagnostic + recommandation")
print("📁 Exporté en : deficiencies_enriched.csv et deficiencies_dataset.json")
