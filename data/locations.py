# African locations database for the agricultural marketplace

AFRICAN_LOCATIONS = [
    # West Africa
    "Lagos, Nigeria",
    "Accra, Ghana", 
    "Abidjan, Ivory Coast",
    "Dakar, Senegal",
    "Bamako, Mali",
    "Ouagadougou, Burkina Faso",
    "Conakry, Guinea",
    "Freetown, Sierra Leone",
    "Monrovia, Liberia",
    "Lomé, Togo",
    "Porto-Novo, Benin",
    "Niamey, Niger",
    "Bissau, Guinea-Bissau",
    "Praia, Cape Verde",
    "Banjul, Gambia",
    "Kano, Nigeria",
    "Kumasi, Ghana",
    "Bouaké, Ivory Coast",
    "Kaolack, Senegal",
    "Sikasso, Mali",
    
    # East Africa
    "Nairobi, Kenya",
    "Dar es Salaam, Tanzania",
    "Kampala, Uganda",
    "Addis Ababa, Ethiopia",
    "Kigali, Rwanda",
    "Bujumbura, Burundi",
    "Mogadishu, Somalia",
    "Djibouti, Djibouti",
    "Asmara, Eritrea",
    "Juba, South Sudan",
    "Mombasa, Kenya",
    "Arusha, Tanzania",
    "Mwanza, Tanzania",
    "Entebbe, Uganda",
    "Gulu, Uganda",
    "Bahir Dar, Ethiopia",
    "Hawassa, Ethiopia",
    "Dire Dawa, Ethiopia",
    "Musanze, Rwanda",
    "Gitega, Burundi",
    
    # North Africa
    "Cairo, Egypt",
    "Alexandria, Egypt",
    "Casablanca, Morocco",
    "Rabat, Morocco",
    "Algiers, Algeria",
    "Tunis, Tunisia",
    "Tripoli, Libya",
    "Khartoum, Sudan",
    "Marrakech, Morocco",
    "Fez, Morocco",
    "Oran, Algeria",
    "Constantine, Algeria",
    "Sfax, Tunisia",
    "Sousse, Tunisia",
    "Benghazi, Libya",
    "Port Sudan, Sudan",
    "Kassala, Sudan",
    "El Obeid, Sudan",
    "Luxor, Egypt",
    "Aswan, Egypt",
    
    # Southern Africa
    "Cape Town, South Africa",
    "Johannesburg, South Africa",
    "Durban, South Africa",
    "Pretoria, South Africa",
    "Harare, Zimbabwe",
    "Bulawayo, Zimbabwe",
    "Gaborone, Botswana",
    "Windhoek, Namibia",
    "Maseru, Lesotho",
    "Mbabane, Eswatini",
    "Lusaka, Zambia",
    "Ndola, Zambia",
    "Lilongwe, Malawi",
    "Blantyre, Malawi",
    "Maputo, Mozambique",
    "Beira, Mozambique",
    "Antananarivo, Madagascar",
    "Toamasina, Madagascar",
    "Port Louis, Mauritius",
    "Victoria, Seychelles",
    
    # Central Africa
    "Kinshasa, Congo (DRC)",
    "Lubumbashi, Congo (DRC)",
    "Brazzaville, Congo",
    "Douala, Cameroon",
    "Yaoundé, Cameroon",
    "Bangui, Central African Republic",
    "N'Djamena, Chad",
    "Libreville, Gabon",
    "Malabo, Equatorial Guinea",
    "São Tomé, São Tomé and Príncipe",
    "Mbuji-Mayi, Congo (DRC)",
    "Kisangani, Congo (DRC)",
    "Kananga, Congo (DRC)",
    "Pointe-Noire, Congo",
    "Garoua, Cameroon",
    "Bamenda, Cameroon",
    "Sarh, Chad",
    "Moundou, Chad",
    "Port-Gentil, Gabon",
    "Franceville, Gabon"
]

# Regional groupings for better organization
REGIONAL_GROUPS = {
    'West Africa': [
        "Lagos, Nigeria", "Accra, Ghana", "Abidjan, Ivory Coast", "Dakar, Senegal",
        "Bamako, Mali", "Ouagadougou, Burkina Faso", "Conakry, Guinea", 
        "Freetown, Sierra Leone", "Monrovia, Liberia", "Lomé, Togo",
        "Porto-Novo, Benin", "Niamey, Niger", "Bissau, Guinea-Bissau",
        "Praia, Cape Verde", "Banjul, Gambia", "Kano, Nigeria",
        "Kumasi, Ghana", "Bouaké, Ivory Coast", "Kaolack, Senegal", "Sikasso, Mali"
    ],
    
    'East Africa': [
        "Nairobi, Kenya", "Dar es Salaam, Tanzania", "Kampala, Uganda",
        "Addis Ababa, Ethiopia", "Kigali, Rwanda", "Bujumbura, Burundi",
        "Mogadishu, Somalia", "Djibouti, Djibouti", "Asmara, Eritrea",
        "Juba, South Sudan", "Mombasa, Kenya", "Arusha, Tanzania",
        "Mwanza, Tanzania", "Entebbe, Uganda", "Gulu, Uganda",
        "Bahir Dar, Ethiopia", "Hawassa, Ethiopia", "Dire Dawa, Ethiopia",
        "Musanze, Rwanda", "Gitega, Burundi"
    ],
    
    'North Africa': [
        "Cairo, Egypt", "Alexandria, Egypt", "Casablanca, Morocco", "Rabat, Morocco",
        "Algiers, Algeria", "Tunis, Tunisia", "Tripoli, Libya", "Khartoum, Sudan",
        "Marrakech, Morocco", "Fez, Morocco", "Oran, Algeria", "Constantine, Algeria",
        "Sfax, Tunisia", "Sousse, Tunisia", "Benghazi, Libya", "Port Sudan, Sudan",
        "Kassala, Sudan", "El Obeid, Sudan", "Luxor, Egypt", "Aswan, Egypt"
    ],
    
    'Southern Africa': [
        "Cape Town, South Africa", "Johannesburg, South Africa", "Durban, South Africa",
        "Pretoria, South Africa", "Harare, Zimbabwe", "Bulawayo, Zimbabwe",
        "Gaborone, Botswana", "Windhoek, Namibia", "Maseru, Lesotho",
        "Mbabane, Eswatini", "Lusaka, Zambia", "Ndola, Zambia",
        "Lilongwe, Malawi", "Blantyre, Malawi", "Maputo, Mozambique",
        "Beira, Mozambique", "Antananarivo, Madagascar", "Toamasina, Madagascar",
        "Port Louis, Mauritius", "Victoria, Seychelles"
    ],
    
    'Central Africa': [
        "Kinshasa, Congo (DRC)", "Lubumbashi, Congo (DRC)", "Brazzaville, Congo",
        "Douala, Cameroon", "Yaoundé, Cameroon", "Bangui, Central African Republic",
        "N'Djamena, Chad", "Libreville, Gabon", "Malabo, Equatorial Guinea",
        "São Tomé, São Tomé and Príncipe", "Mbuji-Mayi, Congo (DRC)",
        "Kisangani, Congo (DRC)", "Kananga, Congo (DRC)", "Pointe-Noire, Congo",
        "Garoua, Cameroon", "Bamenda, Cameroon", "Sarh, Chad",
        "Moundou, Chad", "Port-Gentil, Gabon", "Franceville, Gabon"
    ]
}

# Major agricultural zones and their specialties
AGRICULTURAL_ZONES = {
    'Sahel Region': {
        'locations': [
            "Niamey, Niger", "Bamako, Mali", "Ouagadougou, Burkina Faso",
            "N'Djamena, Chad", "Kano, Nigeria", "Khartoum, Sudan"
        ],
        'climate': 'Semi-arid',
        'main_crops': ['Millet', 'Sorghum', 'Cowpeas', 'Groundnuts', 'Sesame'],
        'growing_season': 'May to October',
        'challenges': ['Drought', 'Desertification', 'Erratic rainfall']
    },
    
    'Guinea Savanna': {
        'locations': [
            "Lagos, Nigeria", "Accra, Ghana", "Abidjan, Ivory Coast",
            "Kumasi, Ghana", "Bouaké, Ivory Coast"
        ],
        'climate': 'Tropical savanna',
        'main_crops': ['Maize', 'Yam', 'Cassava', 'Cocoa', 'Palm Oil'],
        'growing_season': 'April to November',
        'challenges': ['Pest management', 'Post-harvest losses', 'Market access']
    },
    
    'East African Highlands': {
        'locations': [
            "Nairobi, Kenya", "Addis Ababa, Ethiopia", "Kigali, Rwanda",
            "Kampala, Uganda", "Arusha, Tanzania"
        ],
        'climate': 'Highland tropical',
        'main_crops': ['Coffee', 'Tea', 'Irish Potato', 'Wheat', 'Barley'],
        'growing_season': 'March to June, October to December',
        'challenges': ['Climate change', 'Soil degradation', 'Small farm sizes']
    },
    
    'Nile Valley': {
        'locations': [
            "Cairo, Egypt", "Alexandria, Egypt", "Luxor, Egypt",
            "Aswan, Egypt", "Khartoum, Sudan"
        ],
        'climate': 'Arid with irrigation',
        'main_crops': ['Rice', 'Cotton', 'Wheat', 'Sugarcane', 'Vegetables'],
        'growing_season': 'Year-round with irrigation',
        'challenges': ['Water scarcity', 'Soil salinity', 'Climate change']
    },
    
    'Mediterranean Coast': {
        'locations': [
            "Casablanca, Morocco", "Rabat, Morocco", "Algiers, Algeria",
            "Tunis, Tunisia", "Tripoli, Libya"
        ],
        'climate': 'Mediterranean',
        'main_crops': ['Olives', 'Citrus', 'Wheat', 'Barley', 'Vegetables'],
        'growing_season': 'October to May',
        'challenges': ['Water scarcity', 'Soil erosion', 'Market competition']
    },
    
    'Central African Rainforest': {
        'locations': [
            "Kinshasa, Congo (DRC)", "Douala, Cameroon", "Yaoundé, Cameroon",
            "Libreville, Gabon", "Brazzaville, Congo"
        ],
        'climate': 'Tropical rainforest',
        'main_crops': ['Cassava', 'Plantain', 'Cocoa', 'Coffee', 'Palm Oil'],
        'growing_season': 'Year-round',
        'challenges': ['Infrastructure', 'Market access', 'Disease pressure']
    },
    
    'Southern African Plateau': {
        'locations': [
            "Johannesburg, South Africa", "Harare, Zimbabwe", "Lusaka, Zambia",
            "Gaborone, Botswana", "Windhoek, Namibia"
        ],
        'climate': 'Temperate to semi-arid',
        'main_crops': ['Maize', 'Tobacco', 'Cotton', 'Sunflower', 'Groundnuts'],
        'growing_season': 'November to April',
        'challenges': ['Drought', 'Land reforms', 'Input costs']
    }
}

# Climate zones and their characteristics
CLIMATE_ZONES = {
    'Tropical Rainforest': {
        'characteristics': 'High rainfall, high humidity, constant temperatures',
        'rainfall': '1500-3000mm annually',
        'temperature': '20-30°C year-round',
        'locations': [
            "Kinshasa, Congo (DRC)", "Douala, Cameroon", "Libreville, Gabon",
            "Abidjan, Ivory Coast", "Monrovia, Liberia"
        ]
    },
    
    'Tropical Savanna': {
        'characteristics': 'Distinct wet and dry seasons',
        'rainfall': '600-1500mm annually',
        'temperature': '18-35°C',
        'locations': [
            "Lagos, Nigeria", "Accra, Ghana", "Nairobi, Kenya",
            "Dar es Salaam, Tanzania", "Lusaka, Zambia"
        ]
    },
    
    'Semi-Arid (Sahel)': {
        'characteristics': 'Low, erratic rainfall, high temperatures',
        'rainfall': '200-600mm annually',
        'temperature': '20-40°C',
        'locations': [
            "Niamey, Niger", "Bamako, Mali", "Ouagadougou, Burkina Faso",
            "N'Djamena, Chad", "Khartoum, Sudan"
        ]
    },
    
    'Arid (Desert)': {
        'characteristics': 'Very low rainfall, extreme temperatures',
        'rainfall': 'Less than 200mm annually',
        'temperature': '15-45°C',
        'locations': [
            "Cairo, Egypt", "Tripoli, Libya", "Windhoek, Namibia"
        ]
    },
    
    'Mediterranean': {
        'characteristics': 'Mild, wet winters and dry summers',
        'rainfall': '300-800mm annually',
        'temperature': '10-30°C',
        'locations': [
            "Casablanca, Morocco", "Algiers, Algeria", "Tunis, Tunisia",
            "Cape Town, South Africa"
        ]
    },
    
    'Highland Tropical': {
        'characteristics': 'Cooler temperatures due to altitude, bimodal rainfall',
        'rainfall': '800-2000mm annually',
        'temperature': '10-25°C',
        'locations': [
            "Addis Ababa, Ethiopia", "Nairobi, Kenya", "Kigali, Rwanda",
            "Kampala, Uganda", "Antananarivo, Madagascar"
        ]
    }
}

def get_locations_by_region(region):
    """Get all locations in a specific region"""
    return REGIONAL_GROUPS.get(region, [])

def get_location_climate(location):
    """Get climate information for a specific location"""
    for climate, info in CLIMATE_ZONES.items():
        if location in info['locations']:
            return {
                'climate_type': climate,
                'characteristics': info['characteristics'],
                'rainfall': info['rainfall'],
                'temperature': info['temperature']
            }
    return None

def get_agricultural_zone_info(location):
    """Get agricultural zone information for a location"""
    for zone, info in AGRICULTURAL_ZONES.items():
        if location in info['locations']:
            return {
                'zone': zone,
                'climate': info['climate'],
                'main_crops': info['main_crops'],
                'growing_season': info['growing_season'],
                'challenges': info['challenges']
            }
    return None

def get_nearby_locations(location, radius_km=500):
    """Get nearby locations within a specified radius (simplified)"""
    # This is a simplified implementation
    # In a real application, you would use actual geographic coordinates
    
    region = None
    for reg, locs in REGIONAL_GROUPS.items():
        if location in locs:
            region = reg
            break
    
    if region:
        # Return other locations in the same region as "nearby"
        nearby = [loc for loc in REGIONAL_GROUPS[region] if loc != location]
        return nearby[:10]  # Return up to 10 nearby locations
    
    return []

def search_locations(query):
    """Search for locations matching a query"""
    query = query.lower()
    matching_locations = []
    
    for location in AFRICAN_LOCATIONS:
        if query in location.lower():
            matching_locations.append(location)
    
    return matching_locations

def get_location_coordinates(location):
    """Get approximate coordinates for a location (mock data)"""
    # This is a simplified implementation with approximate coordinates
    coordinates_map = {
        'Lagos, Nigeria': (6.5244, 3.3792),
        'Nairobi, Kenya': (-1.2921, 36.8219),
        'Cairo, Egypt': (30.0444, 31.2357),
        'Cape Town, South Africa': (-33.9249, 18.4241),
        'Casablanca, Morocco': (33.5731, -7.5898),
        'Addis Ababa, Ethiopia': (9.0325, 38.7469),
        'Accra, Ghana': (5.6037, -0.1870),
        'Tunis, Tunisia': (36.8065, 10.1815),
        'Khartoum, Sudan': (15.5007, 32.5599),
        'Kampala, Uganda': (0.3476, 32.5825),
        'Dar es Salaam, Tanzania': (-6.7924, 39.2083),
        'Johannesburg, South Africa': (-26.2041, 28.0473),
        'Kinshasa, Congo (DRC)': (-4.4419, 15.2663),
        'Algiers, Algeria': (36.7538, 3.0588),
        'Dakar, Senegal': (14.7167, -17.4677),
        'Abidjan, Ivory Coast': (5.3600, -4.0083),
        'Bamako, Mali': (12.6392, -8.0029),
        'Harare, Zimbabwe': (-17.8252, 31.0335),
        'Lusaka, Zambia': (-15.3875, 28.3228),
        'Maputo, Mozambique': (-25.9692, 32.5732)
    }
    
    return coordinates_map.get(location, (0, 0))

def get_market_centers():
    """Get major agricultural market centers"""
    return [
        "Lagos, Nigeria",
        "Nairobi, Kenya", 
        "Cairo, Egypt",
        "Cape Town, South Africa",
        "Casablanca, Morocco",
        "Addis Ababa, Ethiopia",
        "Accra, Ghana",
        "Dar es Salaam, Tanzania",
        "Johannesburg, South Africa",
        "Kinshasa, Congo (DRC)",
        "Abidjan, Ivory Coast",
        "Dakar, Senegal",
        "Bamako, Mali",
        "Khartoum, Sudan",
        "Tunis, Tunisia"
    ]

def get_border_crossings():
    """Get major agricultural trade border crossings"""
    return {
        'West Africa': [
            'Elubo (Ghana-Ivory Coast)',
            'Aflao (Ghana-Togo)',
            'Seme (Nigeria-Benin)',
            'Kidira (Senegal-Mali)'
        ],
        'East Africa': [
            'Malaba (Kenya-Uganda)',
            'Namanga (Kenya-Tanzania)', 
            'Busia (Kenya-Uganda)',
            'Gatuna (Rwanda-Uganda)'
        ],
        'Southern Africa': [
            'Beitbridge (South Africa-Zimbabwe)',
            'Chirundu (Zambia-Zimbabwe)',
            'Kasumbalesa (DRC-Zambia)',
            'Machipanda (Zimbabwe-Mozambique)'
        ],
        'North Africa': [
            'Ras Jdir (Tunisia-Libya)',
            'Zouar (Chad-Libya)',
            'Maghnia (Algeria-Morocco)'
        ]
    }

