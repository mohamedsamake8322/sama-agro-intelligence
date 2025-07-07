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

# Élément → requête (élargie à 15 éléments)
elements = {
    "N": "nitrogen deficiency in plants",
    "P": "phosphorus deficiency in plants",
    "K": "potassium deficiency in plants",
    "Ca": "calcium deficiency in plants",
    "Mg": "magnesium deficiency in plants",
    "S": "sulfur deficiency in plants",
    "Fe": "iron deficiency in plants",
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
        print(f"✅ {count} images téléchargées pour '{query}' → {folder}")

def generate_caption(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(image, return_tensors="pt").to(device)
        out = model.generate(**inputs)
        return processor.decode(out[0], skip_special_tokens=True)
    except:
        return "error"

def build_deficiency_dataset():
    records = []
    for element, query in elements.items():
        folder = f"deficiencies/{element}"
        print(f"\n🔍 Téléchargement en cours : {element}")
        download_images(query, folder, max_images=100)

        print(f"🧠 Génération de captions : {element}")
        for img_file in os.listdir(folder):
            img_path = os.path.join(folder, img_file)
            if not img_file.lower().endswith(".jpg"):
                continue
            caption = generate_caption(img_path)
            records.append({
                "element": element,
                "image_path": img_path,
                "caption": caption
            })

    df = pd.DataFrame(records)
    df.to_csv("nutrient_deficiencies_dataset.csv", index=False)
    print("\n🎉 Dataset final exporté : `nutrient_deficiencies_dataset.csv`")

if __name__ == "__main__":
    build_deficiency_dataset()
