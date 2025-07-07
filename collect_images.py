from duckduckgo_search import DDGS
import os, urllib.request

def download_images(query, folder, max_images=100):
    os.makedirs(folder, exist_ok=True)
    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=max_images)
        for i, result in enumerate(results):
            try:
                urllib.request.urlretrieve(result["image"], f"{folder}/{i+1}.jpg")
            except:
                continue

categories = {
    "water_stress": "drought stress in crops",
    "extreme_temperatures": "heat damage in plants",
    "diseases": "plant disease symptoms",
    "light_stress": "light stress in plants",
    "salinity_pollution": "salinity damage in agriculture"
}

for folder, query in categories.items():
    download_images(query, f"dataset/{folder}")
