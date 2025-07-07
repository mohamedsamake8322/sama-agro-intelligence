import pdfplumber
import pandas as pd
import os
import re
import json

# 📁 Ton fichier PDF (mets le nom exact que tu as téléchargé)
PDF_PATH = r"C:\SamaAgroIntelligence\Fertilizer-Guidelines-2023.pdf"
OUTPUT_DIR = "minnesota_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🔗 Lecture du PDF :", PDF_PATH)

def clean(cell):
    return re.sub(r'\s+', ' ', str(cell)).strip() if cell else ""

raw_rows = []
cultures = ['corn', 'soybean', 'wheat', 'oat', 'canola', 'barley', 'alfalfa', 'sunflower', 'rye', 'sorghum']

with pdfplumber.open(PDF_PATH) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        if any(kw in text.lower() for kw in ['fertilizer recommendation', 'application', 'nitrogen rate', 'phosphate', 'potash']):
            print(f"📄 Traitement page {i+1}")
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    cleaned = [clean(cell) for cell in row]
                    if any(cleaned):
                        raw_rows.append(cleaned)

print(f"✅ {len(raw_rows)} lignes extraites brutes")

# 🔄 Export brut
df_raw = pd.DataFrame(raw_rows)
df_raw.to_excel(os.path.join(OUTPUT_DIR, "minnesota_raw.xlsx"), index=False)

# 🔍 Filtrage par nom de cultures
def contains_culture(row):
    content = ' '.join(str(cell).lower() for cell in row)
    return any(culture in content for culture in cultures)

df_filtered = df_raw[df_raw.apply(contains_culture, axis=1)]
df_filtered.to_excel(os.path.join(OUTPUT_DIR, "minnesota_cleaned.xlsx"), index=False)

# 📦 Génération JSON par culture
data_json = {}
for _, row in df_filtered.iterrows():
    line = [c for c in row if c]
    name = next((c for c in line if any(culture in c.lower() for culture in cultures)), None)
    if not name:
        continue
    key = name.lower()
    data_json.setdefault(key, []).append(line)

with open(os.path.join(OUTPUT_DIR, "minnesota_data.json"), "w", encoding="utf-8") as f:
    json.dump(data_json, f, indent=2, ensure_ascii=False)

print("📁 Extraction terminée dans :", os.path.abspath(OUTPUT_DIR))
