import requests
import os
import time
import numpy as np

# 📁 Dossier de sortie
output_folder = "weather_data_africa"
os.makedirs(output_folder, exist_ok=True)

# 🌍 Bounding boxes (lon_min, lat_min, lon_max, lat_max)
grilles_par_pays = {

    "ZA": ["South Africa", [16.34, -34.82, 32.83, -22.09]],
    "ZM": ["Zambia", [21.89, -17.96, 33.49, -8.24]],
    "ZW": ["Zimbabwe", [25.26, -22.27, 32.85, -15.51]]
}

# 📌 Paramètres météo (6 bien tolérés)
parameters = [
    "WS2M_MIN", "WS2M_RANGE", "WD2M", "WS10M", "WS10M_MAX", "WS10M_MIN",
]

# 📅 Période
start_date = "20210101"
end_date = "20241231"

# 📐 Espacement de la grille (en degrés)
lat_step = 2.0
lon_step = 2.0

# 🔧 Fonction pour construire URL API
def build_power_url(lat, lon, params, start, end):
    param_str = ",".join(params)
    return (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"parameters={param_str}&community=AG&longitude={lon:.4f}&latitude={lat:.4f}"
        f"&start={start}&end={end}&format=CSV"
    )

# 📡 Fonction pour télécharger un point météo
def get_power_data(lat, lon, params, start, end, country_name):
    url = build_power_url(lat, lon, params, start, end)
    response = requests.get(url)

    if response.status_code == 200:
        fname = f"{country_name}_{round(lat, 2)}_{round(lon, 2)}.csv".replace(" ", "_")
        fpath = os.path.join(output_folder, fname)
        with open(fpath, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved: {fpath}")
        return True
    else:
        print(f"❌ Error {response.status_code} for {country_name} at ({lat}, {lon})")
        return False

# 🔁 Boucle sur tous les pays et génération de la grille
for code, (name, [lon_min, lat_min, lon_max, lat_max]) in grilles_par_pays.items():
    print(f"\n🌍 Processing {name} ({code})")

    latitudes = np.arange(lat_min, lat_max + lat_step, lat_step)
    longitudes = np.arange(lon_min, lon_max + lon_step, lon_step)

    for lat in latitudes:
        for lon in longitudes:
            success = get_power_data(lat, lon, parameters, start_date, end_date, name)
            time.sleep(2)  # Anti-saturation serveur NASA
