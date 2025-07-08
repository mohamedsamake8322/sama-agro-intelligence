#Nettoyer les images corrompus
import os
import shutil
import cv2
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm
import pandas as pd

# === PARAMÈTRES ===
dataset_dir = r"C:\Users\moham\Pictures\plantdataset"
quarantine_dir = r"C:\Users\moham\Pictures\plantdataset\quarantaine"
report_csv = "image_cleaning_report.csv"
min_width = 100
min_height = 100
blur_threshold = 100.0

# === Détection de flou ===
def is_blurry(image, threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

# === Vérification d’une image ===
def check_image(path):
    try:
        with Image.open(path) as img:
            w, h = img.size
            if w < min_width or h < min_height:
                return "too_small", w, h, None

        image_cv = cv2.imread(path)
        if image_cv is None:
            return "corrupted", 0, 0, None

        score = is_blurry(image_cv, blur_threshold)
        if score < blur_threshold:
            return "blurry", w, h, round(score, 2)
        return "ok", w, h, round(score, 2)

    except (UnidentifiedImageError, OSError):
        return "corrupted", 0, 0, None

# === Création du dossier de quarantaine ===
os.makedirs(quarantine_dir, exist_ok=True)

# === Collecte des fichiers à traiter ===
image_paths = []
for root, _, files in os.walk(dataset_dir):
    for name in files:
        if name.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_paths.append(os.path.join(root, name))

# === Traitement avec barre de progression ===
records = []
for path in tqdm(image_paths, desc="Nettoyage des images"):
    status, w, h, score = check_image(path)

    if status != "ok":
        rel_path = os.path.relpath(path, dataset_dir)
        quarantine_path = os.path.join(quarantine_dir, rel_path)
        os.makedirs(os.path.dirname(quarantine_path), exist_ok=True)
        shutil.move(path, quarantine_path)

    records.append({
        "path": path,
        "status": status,
        "width": w,
        "height": h,
        "blur_score": score
    })

# === Sauvegarde du rapport ===
pd.DataFrame(records).to_csv(report_csv, index=False)
print(f"\n✅ Nettoyage terminé. Rapport : {report_csv}")
print(f"🗃️ Fichiers déplacés vers : {quarantine_dir}")
