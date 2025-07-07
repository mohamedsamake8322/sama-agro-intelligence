import pdfplumber
import pandas as pd
import re

# 📁 Chemin vers ton guide PDF
pdf_path = "Fertilizer_Recommendations_Guide.pdf"

# 📦 Conteneur pour les données extraites
records = []

# 🧠 Fonctions utiles
def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def extract_table_data(page):
    tables = page.extract_tables()
    for table in tables:
        for row in table:
            if row and any(cell for cell in row):
                records.append([clean_text(cell) if cell else "" for cell in row])

# 📖 Lecture du PDF
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text and any(keyword in text.lower() for keyword in ["fertilizer", "recommendation", "crop", "nutrient"]):
            print(f"🔍 Page {i+1} analysée")
            extract_table_data(page)

# 📄 Conversion en DataFrame
df = pd.DataFrame(records)
df.to_csv("fertilization_data_raw.csv", index=False, encoding="utf-8")

print(f"\n✅ Extraction terminée : {len(records)} lignes exportées dans fertilization_data_raw.csv")
