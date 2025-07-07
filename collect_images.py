import os
import urllib.request
from duckduckgo_search import DDGS
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import pandas as pd

# Chargement du modèle BLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# Catégories et requêtes de recherche
categories = {
    "water_stress": "drought stress in crops",
    "extreme_temperatures": "heat damage in plants",
    "diseases": "plant disease symptoms",
    "light_stress": "light stress in plants",
    "salinity_pollution": "salinity damage in agriculture"
}

# Collecte d'images via DuckDuckGo
def download_images(query, folder, max_images=150):
    os.makedirs(folder, exist_ok=True)
    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=max_images)
        for i, result in enumerate(results):
            try:
                image_path = os.path.join(folder, f"{i+1}.jpg")
                urllib.request.urlretrieve(result["image"], image_path)
            except:
                continue

# Caption automatique via BLIP
def generate_caption(image_path):
    try:
        raw_image = Image.open(image_path).convert("RGB")
        inputs = processor(raw_image, return_tensors="pt").to(device)
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except:
        return "error"

# Pipeline complet
def build_dataset():
    records = []
    for category, query in categories.items():
        print(f"🔍 Téléchargement : {category}")
        folder_path = f"dataset/{category}"
        download_images(query, folder_path, max_images=150)

        print(f"🧠 Génération de captions : {category}")
        for img_file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_file)
            caption = generate_caption(img_path)
            records.append({
                "category": category,
                "image_path": img_path,
                "caption": caption
            })

    # Sauvegarde en CSV
    df = pd.DataFrame(records)
    df.to_csv("captions_dataset.csv", index=False)
    print("✅ Dataset exporté dans captions_dataset.csv")

if __name__ == "__main__":
    build_dataset()
