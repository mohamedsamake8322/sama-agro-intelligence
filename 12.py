import os
import rasterio
import numpy as np
import csv
from concurrent.futures import ThreadPoolExecutor

# 📁 Répertoire principal contenant les données GAEZ
base_path = r"C:\Users\moham\Music\2\Rendements et production réels"
output_csv = "gaez_gap_extracted_stream.csv"

# 🔧 Taille de la fenêtre (en pixels) pour lire par morceaux
window_size = 1024  # Peut augmenter ou diminuer selon ta RAM

# 🧵 Fonction pour traiter un seul fichier
def process_tif(file_path, category, year, filename):
    data = []
    try:
        with rasterio.open(file_path) as src:
            transform = src.transform
            nodata = src.nodata

            # Parcours par fenêtre
            for ji, window in src.block_windows(1):
                band = src.read(1, window=window)
                mask = (band != nodata) & (~np.isnan(band))
                rows, cols = np.where(mask)

                if rows.size == 0:
                    continue

                xs, ys = rasterio.transform.xy(transform, rows + window.row_off, cols + window.col_off)
                for x, y, val in zip(xs, ys, band[rows, cols]):
                    data.append([x, y, val, int(year), category, filename])
    except Exception as e:
        print(f"❌ Erreur sur {file_path} : {e}")
    return data

# ✍️ Écriture dans le CSV principal
with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["x", "y", "value", "year", "category", "layer"])

    tasks = []

    with ThreadPoolExecutor(max_workers=4) as executor:  # 💡 adapte max_workers à ton CPU
        for category in os.listdir(base_path):
            cat_path = os.path.join(base_path, category)
            if not os.path.isdir(cat_path): continue

            for year in os.listdir(cat_path):
                year_path = os.path.join(cat_path, year)
                if not os.path.isdir(year_path): continue

                print(f"🔍 Traitement : {category}/{year}")

                for filename in os.listdir(year_path):
                    if not filename.endswith(".tif"): continue
                    file_path = os.path.join(year_path, filename)
                    tasks.append(executor.submit(process_tif, file_path, category, year, filename))

        # Collecte les résultats au fur et à mesure
        for task in tasks:
            for row in task.result():
                writer.writerow(row)

print(f"✅ Terminé : les résultats sont dans {output_csv}")
