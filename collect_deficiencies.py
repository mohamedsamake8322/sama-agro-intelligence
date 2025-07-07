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

elements = {
    "Mn": "manganese deficiency in plants",
    "Zn": "zinc deficiency in plants",
    "Cu": "copper deficiency in plants",
    "B": "boron deficiency in plants",
    "Mo": "molybdenum deficiency in plants",
    "Cl": "chlorine deficiency in plants",
    "Co": "cobalt deficiency in plants",
    "Ni": "nickel deficiency in plants"
}

def download_images(query, folder, max_images=100):
    os.makedirs(folder, exist_ok=True)
    existing_files = set(os.listdir(folder))
    already_present = len([f for f in existing_files if f.endswith(".jpg")])
    if already_present >= max_images:
        print(f"📁 {folder} contient déjà {already_present} images — téléchargement ignoré.")
        return
    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=max_images)
        count = already_present
        for i, result in enumerate(results):
            if count >= max_images:
                break
            try:
                filename = os.path.join(folder, f"{count+1}.jpg")
                urllib.request.urlretrieve(result["image"], filename)
                count += 1
            except:
                continue
        print(f"✅ {count - already_present} nouvelles images pour '{query}' → {folder}")

def generate_caption(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(image, return_tensors="pt").to(device)
        out = model.generate(**inputs)
        return processor.decode(out[0], skip_special_tokens=True)
    except:
        return "error"

def build_deficiency_dataset():
    dataset_file = "nutrient_deficiencies_dataset.csv"
    existing_records = []

    if os.path.exists(dataset_file):
        df_existing = pd.read_csv(dataset_file)
        existing_paths = set(df_existing["image_path"])
        existing_records = df_existing.to_dict(orient="records")
    else:
        existing_paths = set()

    new_records = []
    for element, query in elements.items():
        folder = f"deficiencies/{element}"
        print(f"\n🔍 Traitement de l’élément : {element}")
        download_images(query, folder, max_images=100)

        print(f"🧠 Génération de captions pour {element}")
        for img_file in os.listdir(folder):
            img_path = os.path.join(folder, img_file)
            if not img_file.lower().endswith(".jpg"):
                continue
            if img_path in existing_paths:
                continue  # Caption déjà présente
            caption = generate_caption(img_path)
            new_records.append({
                "element": element,
                "image_path": img_path,
                "caption": caption
            })

    full_dataset = existing_records + new_records
    df = pd.DataFrame(full_dataset)
    df.to_csv(dataset_file, index=False)
    print(f"\n🎉 Dataset enrichi exporté : {dataset_file}")

if __name__ == "__main__":
    build_deficiency_dataset()
