import os
import urllib.request
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import pandas as pd
from ddgs import DDGS

device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# Requêtes retravaillées pour + de résultats
categories = {
    "water_stress": "drought stress in crops",
    "extreme_temperatures": "heat damage in plants",
    "diseases": "plant disease symptoms",
    "light_stress": "light stress symptoms in plants",
    "salinity_pollution": "salinity stress symptoms in crops"
}

def download_images(query, folder, max_images=150):
    os.makedirs(folder, exist_ok=True)
    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=max_images)
        count = 0
        for i, result in enumerate(results):
            try:
                filename = os.path.join(folder, f"{i+1}.jpg")
                urllib.request.urlretrieve(result["image"], filename)
                count += 1
            except:
                continue
        print(f"✅ {count} images téléchargées pour '{query}' dans {folder}")

def generate_caption(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(image, return_tensors="pt").to(device)
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except:
        return "error"

def build_dataset():
    records = []
    for category, query in categories.items():
        folder = f"dataset/{category}"
        if not os.path.exists(folder) or len(os.listdir(folder)) < 100:
            print(f"🔍 Téléchargement en cours : {category}")
            download_images(query, folder, max_images=150)
        else:
            print(f"📁 Dossier déjà présent pour {category}, on saute le téléchargement.")

        print(f"🧠 Génération de captions : {category}")
        for img_file in os.listdir(folder):
            img_path = os.path.join(folder, img_file)
            if not img_file.lower().endswith(".jpg"):
                continue
            caption = generate_caption(img_path)
            records.append({
                "category": category,
                "image_path": img_path,
                "caption": caption
            })

    df = pd.DataFrame(records)
    df.to_csv("captions_dataset.csv", index=False)
    print("🎉 Dataset final exporté dans `captions_dataset.csv`.")

if __name__ == "__main__":
    build_dataset()
