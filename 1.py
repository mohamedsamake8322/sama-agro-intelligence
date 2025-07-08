import os
import urllib.request
from duckduckgo_search import DDGS
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import pandas as pd

# === Paramètres ===
train_dir = r"C:\Users\moham\Pictures\plantdataset\train"
output_dir = "dataset"
min_images_per_class = 7
max_images_to_download = 25

# === Chargement du modèle BLIP ===
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# === Étape 1 : Identifier les classes sous-représentées ===
def find_underrepresented_classes(train_path, min_count):
    underrepresented = {}
    for class_name in os.listdir(train_path):
        class_path = os.path.join(train_path, class_name)
        if os.path.isdir(class_path):
            num_images = len([f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            if num_images < min_count:
                query = class_name.replace("_", " ").replace("-", " ")
                underrepresented[class_name] = query
    return underrepresented

# === Étape 2 : Télécharger les images depuis DuckDuckGo ===
def download_images(query, folder, max_images=100):
    os.makedirs(folder, exist_ok=True)
    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=max_images)
        for i, result in enumerate(results):
            try:
                image_path = os.path.join(folder, f"{i+1}.jpg")
                urllib.request.urlretrieve(result["image"], image_path)
            except:
                continue

# === Étape 3 : Générer des captions avec BLIP ===
def generate_caption(image_path):
    try:
        raw_image = Image.open(image_path).convert("RGB")
        inputs = processor(raw_image, return_tensors="pt").to(device)
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except:
        return "error"

# === Étape 4 : Pipeline complet ===
def build_dataset():
    categories = find_underrepresented_classes(train_dir, min_images_per_class)
    records = []

    for category, query in categories.items():
        print(f"🔍 Téléchargement pour : {category} → '{query}'")
        folder_path = os.path.join(output_dir, category)
        download_images(query, folder_path, max_images=max_images_to_download)

        print(f"🧠 Génération de captions : {category}")
        for img_file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_file)
            caption = generate_caption(img_path)
            records.append({
                "category": category,
                "image_path": img_path,
                "caption": caption
            })

    df = pd.DataFrame(records)
    df.to_csv("captions_dataset.csv", index=False)
    print("✅ Dataset enrichi exporté dans captions_dataset.csv")

if __name__ == "__main__":
    build_dataset()
