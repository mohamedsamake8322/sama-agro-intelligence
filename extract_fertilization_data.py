import pdfplumber
import pandas as pd
import os
import re
import json

# 📁 Nouveau chemin local vers ton guide de fertilisation
PDF_PATH = r"C:\SamaAgroIntelligence\1.pdf"
print("🔗 Chemin utilisé :", PDF_PATH)

# 📂 Dossier de sortie
OUTPUT_DIR = "fertilization_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 📦 Conteneur brut
raw_rows = []

# 🧠 Nettoie le texte
def clean(cell):
    if cell is None:
        return ""
    return re.sub(r'\s+', ' ', cell).strip()

# 📖 Lecture du PDF
print("🔍 Lecture du PDF...")
with pdfplumber.open(PDF_PATH) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        if any(kw in text.lower() for kw in ['fertilizer', 'recommendation', 'nutrient', 'application']):
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    cleaned = [clean(cell) for cell in row]
                    if any(cleaned):
                        raw_rows.append(cleaned)

print(f"✅ {len(raw_rows)} lignes extraites brutes")

# ⛏️ Tentative de structure automatique (tu pourras ajuster ensuite)
df_raw = pd.DataFrame(raw_rows)
df_raw.to_excel(os.path.join(OUTPUT_DIR, "fertilization_raw.xlsx"), index=False)

# 🧪 Tentative : filtrer les lignes qui contiennent des cultures
cultures = ['maize', 'rice', 'potato', 'tomato', 'bean', 'cabbage', 'onion', 'wheat']
df_filtered = df_raw[df_raw.apply(lambda row: any(culture in ' '.join(row).lower() for culture in cultures), axis=1)]
df_filtered.to_excel(os.path.join(OUTPUT_DIR, "fertilization_cleaned.xlsx"), index=False)

# (Optionnel) Générer un petit JSON par culture
data_json = {}

for _, row in df_filtered.iterrows():
    joined = [c for c in row if c]
    name = next((c for c in joined if any(culture in c.lower() for culture in cultures)), None)
    if not name:
        continue
    key = name.lower()
    if key not in data_json:
        data_json[key] = []
    data_json[key].append(joined)

with open(os.path.join(OUTPUT_DIR, "fertilization_data.json"), "w", encoding="utf-8") as f:
    json.dump(data_json, f, ensure_ascii=False, indent=2)

print("📁 Fichiers générés dans :", os.path.abspath(OUTPUT_DIR))
