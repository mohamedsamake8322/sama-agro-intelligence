import json
import os

# 📁 Charge la base agronomique unifiée
with open("unified_fertilization/fertilization_master.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 📥 Inputs utilisateur
culture = input("🌱 Entrez la culture : ").strip().lower()
surface = float(input("📐 Entrez la superficie (en hectares) : "))

# 🔍 Recherche des enregistrements
recs = data.get(culture)
if not recs:
    print(f"❌ Aucune donnée pour {culture}")
    exit()

print(f"\n✅ {len(recs)} recommandations trouvées pour « {culture} »")

# 🔁 Parcours des lignes
for i, line in enumerate(recs, 1):
    line_str = [str(c) for c in line]
    line_joined = " | ".join(line_str)

    # 🔎 Détection des doses N-P-K par regex légère
    npk_values = [v for v in line if any(x in str(v).upper() for x in ['N', 'P', 'K'])]
    if len(npk_values) >= 3:
        print(f"\n📋 Plan #{i}")
        print("-" * 40)
        print("Ligne extraite :", line_joined)

        # Exemple : "N = 90", "P2O5 = 60", "K2O = 40"
        for v in npk_values:
            parts = str(v).replace(":", "=").split("=")
            if len(parts) == 2:
                nutrient = parts[0].strip().upper()
                try:
                    dose = float(parts[1].strip())
                    total = dose * surface
                    print(f"→ {nutrient}: {dose} kg/ha × {surface} ha = {total:.2f} kg")
                except ValueError:
                    continue

        print("-" * 40)

print("\n🎯 Fin de génération du plan brut (tu peux exporter en PDF ou enrichir via Streamlit)")
