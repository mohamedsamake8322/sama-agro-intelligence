import os
import pandas as pd

dataset_dir = r"C:\Users\moham\Pictures\plantdataset"
quarantine_dir = os.path.join(dataset_dir, "quarantaine")
csv_report = "image_cleaning_report.csv"

# === Scanner le dataset nettoyé ===
def count_valid_images(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                total += 1
    return total

# === Analyse du fichier CSV du nettoyage ===
def analyze_report(csv_path):
    if not os.path.exists(csv_path):
        print("Aucun rapport CSV trouvé.")
        return {}

    df = pd.read_csv(csv_path)
    summary = df['status'].value_counts().to_dict()
    total_removed = sum([v for k, v in summary.items() if k != 'ok'])
    return summary, total_removed

# === Affichage global ===
valid = count_valid_images(dataset_dir)
summary, total_quarantined = analyze_report(csv_report)

print(f"\n✅ Images valides restantes dans le dataset : {valid}")
print(f"🗃️ Images en quarantaine détectées dans le rapport : {total_quarantined}")
print(f"\n📊 Répartition par type d'image déplacée :")
for issue, count in summary.items():
    if issue != 'ok':
        print(f"   - {issue}: {count} image(s)")

print(f"\n📄 Rapport utilisé : {csv_report}")
print(f"📂 Quarantaine : {quarantine_dir}")
