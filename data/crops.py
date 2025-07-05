# African crops database with realistic market data

AFRICAN_CROPS = [
    # Grains and Cereals
    {
        'name': 'Maize',
        'category': 'Grains',
        'price_per_kg': 2.10,
        'region': 'Nigeria',
        'season': 'wet',
        'shelf_life_days': 365,
        'nutrition': {'calories': 365, 'protein': 9.4, 'carbs': 74.3},
        'growing_period_months': 4,
        'water_requirement': 'moderate'
    },
    {
        'name': 'Rice',
        'category': 'Grains',
        'price_per_kg': 3.10,
        'region': 'Ghana',
        'season': 'wet',
        'shelf_life_days': 730,
        'nutrition': {'calories': 130, 'protein': 2.7, 'carbs': 28},
        'growing_period_months': 5,
        'water_requirement': 'high'
    },
    {
        'name': 'Millet',
        'category': 'Grains',
        'price_per_kg': 1.85,
        'region': 'Mali',
        'season': 'dry',
        'shelf_life_days': 365,
        'nutrition': {'calories': 378, 'protein': 11, 'carbs': 73},
        'growing_period_months': 3,
        'water_requirement': 'low'
    },
    {
        'name': 'Sorghum',
        'category': 'Grains',
        'price_per_kg': 1.95,
        'region': 'Sudan',
        'season': 'dry',
        'shelf_life_days': 365,
        'nutrition': {'calories': 339, 'protein': 10.6, 'carbs': 70.7},
        'growing_period_months': 4,
        'water_requirement': 'low'
    },
    {
        'name': 'Teff',
        'category': 'Grains',
        'price_per_kg': 4.50,
        'region': 'Ethiopia',
        'season': 'wet',
        'shelf_life_days': 365,
        'nutrition': {'calories': 367, 'protein': 13.3, 'carbs': 73},
        'growing_period_months': 3,
        'water_requirement': 'moderate'
    },
    
    # Root Crops and Tubers
    {
        'name': 'Cassava',
        'category': 'Tubers',
        'price_per_kg': 1.20,
        'region': 'Congo',
        'season': 'year-round',
        'shelf_life_days': 14,
        'nutrition': {'calories': 160, 'protein': 1.4, 'carbs': 38.1},
        'growing_period_months': 12,
        'water_requirement': 'low'
    },
    {
        'name': 'Yam',
        'category': 'Tubers',
        'price_per_kg': 2.80,
        'region': 'Nigeria',
        'season': 'wet',
        'shelf_life_days': 90,
        'nutrition': {'calories': 118, 'protein': 1.5, 'carbs': 27.9},
        'growing_period_months': 8,
        'water_requirement': 'moderate'
    },
    {
        'name': 'Sweet Potato',
        'category': 'Tubers',
        'price_per_kg': 1.60,
        'region': 'Uganda',
        'season': 'wet',
        'shelf_life_days': 30,
        'nutrition': {'calories': 86, 'protein': 1.6, 'carbs': 20.1},
        'growing_period_months': 4,
        'water_requirement': 'moderate'
    },
    {
        'name': 'Irish Potato',
        'category': 'Tubers',
        'price_per_kg': 2.20,
        'region': 'Kenya',
        'season': 'wet',
        'shelf_life_days': 60,
        'nutrition': {'calories': 77, 'protein': 2, 'carbs': 17},
        'growing_period_months': 3,
        'water_requirement': 'moderate'
    },
    
    # Legumes
    {
        'name': 'Cowpeas',
        'category': 'Legumes',
        'price_per_kg': 3.80,
        'region': 'Niger',
        'season': 'wet',
        'shelf_life_days': 365,
        'nutrition': {'calories': 336, 'protein': 24, 'carbs': 56.8},
        'growing_period_months': 3,
        'water_requirement': 'low'
    },
    {
        'name': 'Groundnuts',
        'category': 'Legumes',
        'price_per_kg': 4.20,
        'region': 'Senegal',
        'season': 'wet',
        'shelf_life_days': 365,
        'nutrition': {'calories': 567, 'protein': 25.8, 'carbs': 16.1},
        'growing_period_months': 4,
        'water_requirement': 'low'
    },
    {
        'name': 'Black-eyed Peas',
        'category': 'Legumes',
        'price_per_kg': 3.50,
        'region': 'Burkina Faso',
        'season': 'wet',
        'shelf_life_days': 365,
        'nutrition': {'calories': 336, 'protein': 24, 'carbs': 57},
        'growing_period_months': 3,
        'water_requirement': 'low'
    },
    {
        'name': 'Bambara Nuts',
        'category': 'Legumes',
        'price_per_kg': 5.10,
        'region': 'Botswana',
        'season': 'wet',
        'shelf_life_days': 365,
        'nutrition': {'calories': 367, 'protein': 19, 'carbs': 57},
        'growing_period_months': 4,
        'water_requirement': 'low'
    },
    
    # Vegetables
    {
        'name': 'Tomatoes',
        'category': 'Vegetables',
        'price_per_kg': 2.50,
        'region': 'Morocco',
        'season': 'wet',
        'shelf_life_days': 14,
        'nutrition': {'calories': 18, 'protein': 0.9, 'carbs': 3.9},
        'growing_period_months': 3,
        'water_requirement': 'high'
    },
    {
        'name': 'Onions',
        'category': 'Vegetables',
        'price_per_kg': 1.80,
        'region': 'Egypt',
        'season': 'dry',
        'shelf_life_days': 180,
        'nutrition': {'calories': 40, 'protein': 1.1, 'carbs': 9.3},
        'growing_period_months': 4,
        'water_requirement': 'moderate'
    },
    {
        'name': 'Cabbage',
        'category': 'Vegetables',
        'price_per_kg': 1.40,
        'region': 'Kenya',
        'season': 'wet',
        'shelf_life_days': 60,
        'nutrition': {'calories': 25, 'protein': 1.3, 'carbs': 5.8},
        'growing_period_months': 3,
        'water_requirement': 'moderate'
    },
    {
        'name': 'Spinach',
        'category': 'Vegetables',
        'price_per_kg': 3.20,
        'region': 'South Africa',
        'season': 'wet',
        'shelf_life_days': 7,
        'nutrition': {'calories': 23, 'protein': 2.9, 'carbs': 3.6},
        'growing_period_months': 2,
        'water_requirement': 'high'
    },
    {
        'name': 'Okra',
        'category': 'Vegetables',
        'price_per_kg': 2.80,
        'region': 'Ghana',
        'season': 'wet',
        'shelf_life_days': 7,
        'nutrition': {'calories': 33, 'protein': 1.9, 'carbs': 7.5},
        'growing_period_months': 2,
        'water_requirement': 'moderate'
    },
    
    # Fruits
    {
        'name': 'Mangoes',
        'category': 'Fruits',
        'price_per_kg': 3.50,
        'region': 'Mali',
        'season': 'wet',
        'shelf_life_days': 14,
        'nutrition': {'calories': 60, 'protein': 0.8, 'carbs': 15},
        'growing_period_months': 6,
        'water_requirement': 'moderate'
    },
    {
        'name': 'Bananas',
        'category': 'Fruits',
        'price_per_kg': 2.20,
        'region': 'Uganda',
        'season': 'year-round',
        'shelf_life_days': 7,
        'nutrition': {'calories': 89, 'protein': 1.1, 'carbs': 23},
        'growing_period_months': 12,
        'water_requirement': 'high'
    },
    {
        'name': 'Oranges',
        'category': 'Fruits',
        'price_per_kg': 2.80,
        'region': 'Morocco',
        'season': 'dry',
        'shelf_life_days': 30,
        'nutrition': {'calories': 47, 'protein': 0.9, 'carbs': 11.8},
        'growing_period_months': 8,
        'water_requirement': 'moderate'
    },
    {
        'name': 'Pineapples',
        'category': 'Fruits',
        'price_per_kg': 1.90,
        'region': 'Ivory Coast',
        'season': 'year-round',
        'shelf_life_days': 21,
        'nutrition': {'calories': 50, 'protein': 0.5, 'carbs': 13.1},
        'growing_period_months': 18,
        'water_requirement': 'moderate'
    },
    {
        'name': 'Papayas',
        'category': 'Fruits',
        'price_per_kg': 2.60,
        'region': 'Nigeria',
        'season': 'year-round',
        'shelf_life_days': 14,
        'nutrition': {'calories': 43, 'protein': 0.5, 'carbs': 10.8},
        'growing_period_months': 12,
        'water_requirement': 'moderate'
    },
    
    # Cash Crops
    {
        'name': 'Coffee Beans',
        'category': 'Cash Crops',
        'price_per_kg': 12.50,
        'region': 'Ethiopia',
        'season': 'dry',
        'shelf_life_days': 365,
        'nutrition': {'calories': 2, 'protein': 0.3, 'carbs': 0},
        'growing_period_months': 36,
        'water_requirement': 'high'
    },
    {
        'name': 'Cocoa Beans',
        'category': 'Cash Crops',
        'price_per_kg': 8.80,
        'region': 'Ghana',
        'season': 'wet',
        'shelf_life_days': 730,
        'nutrition': {'calories': 228, 'protein': 19.6, 'carbs': 57.9},
        'growing_period_months': 36,
        'water_requirement': 'high'
    },
    {
        'name': 'Cotton',
        'category': 'Cash Crops',
        'price_per_kg': 6.20,
        'region': 'Chad',
        'season': 'wet',
        'shelf_life_days': 1095,
        'nutrition': {'calories': 0, 'protein': 0, 'carbs': 0},
        'growing_period_months': 6,
        'water_requirement': 'moderate'
    },
    {
        'name': 'Sesame',
        'category': 'Cash Crops',
        'price_per_kg': 7.40,
        'region': 'Sudan',
        'season': 'wet',
        'shelf_life_days': 365,
        'nutrition': {'calories': 573, 'protein': 17.7, 'carbs': 23.4},
        'growing_period_months': 4,
        'water_requirement': 'low'
    },
    
    # Spices and Herbs
    {
        'name': 'Ginger',
        'category': 'Spices',
        'price_per_kg': 8.50,
        'region': 'Nigeria',
        'season': 'wet',
        'shelf_life_days': 90,
        'nutrition': {'calories': 80, 'protein': 1.8, 'carbs': 17.8},
        'growing_period_months': 8,
        'water_requirement': 'high'
    },
    {
        'name': 'Turmeric',
        'category': 'Spices',
        'price_per_kg': 12.20,
        'region': 'Madagascar',
        'season': 'wet',
        'shelf_life_days': 365,
        'nutrition': {'calories': 354, 'protein': 7.8, 'carbs': 64.9},
        'growing_period_months': 10,
        'water_requirement': 'high'
    },
    {
        'name': 'Black Pepper',
        'category': 'Spices',
        'price_per_kg': 18.50,
        'region': 'Madagascar',
        'season': 'wet',
        'shelf_life_days': 1095,
        'nutrition': {'calories': 251, 'protein': 10.4, 'carbs': 63.9},
        'growing_period_months': 36,
        'water_requirement': 'high'
    },
    {
        'name': 'Chili Peppers',
        'category': 'Spices',
        'price_per_kg': 6.80,
        'region': 'Ghana',
        'season': 'wet',
        'shelf_life_days': 14,
        'nutrition': {'calories': 40, 'protein': 1.9, 'carbs': 8.8},
        'growing_period_months': 4,
        'water_requirement': 'moderate'
    },
    
    # Additional African Staples
    {
        'name': 'Plantains',
        'category': 'Fruits',
        'price_per_kg': 1.80,
        'region': 'Cameroon',
        'season': 'year-round',
        'shelf_life_days': 14,
        'nutrition': {'calories': 122, 'protein': 1.3, 'carbs': 31.9},
        'growing_period_months': 12,
        'water_requirement': 'high'
    },
    {
        'name': 'Avocados',
        'category': 'Fruits',
        'price_per_kg': 4.50,
        'region': 'Kenya',
        'season': 'year-round',
        'shelf_life_days': 10,
        'nutrition': {'calories': 160, 'protein': 2, 'carbs': 8.5},
        'growing_period_months': 12,
        'water_requirement': 'moderate'
    },
    {
        'name': 'Palm Oil',
        'category': 'Oil Crops',
        'price_per_kg': 2.90,
        'region': 'Nigeria',
        'season': 'year-round',
        'shelf_life_days': 365,
        'nutrition': {'calories': 884, 'protein': 0, 'carbs': 0},
        'growing_period_months': 36,
        'water_requirement': 'high'
    },
    {
        'name': 'Shea Nuts',
        'category': 'Oil Crops',
        'price_per_kg': 3.20,
        'region': 'Burkina Faso',
        'season': 'dry',
        'shelf_life_days': 365,
        'nutrition': {'calories': 400, 'protein': 8, 'carbs': 15},
        'growing_period_months': 12,
        'water_requirement': 'low'
    }
]

# Crop categories for easy filtering
CROP_CATEGORIES = {
    'Grains': ['Maize', 'Rice', 'Millet', 'Sorghum', 'Teff'],
    'Tubers': ['Cassava', 'Yam', 'Sweet Potato', 'Irish Potato'],
    'Legumes': ['Cowpeas', 'Groundnuts', 'Black-eyed Peas', 'Bambara Nuts'],
    'Vegetables': ['Tomatoes', 'Onions', 'Cabbage', 'Spinach', 'Okra'],
    'Fruits': ['Mangoes', 'Bananas', 'Oranges', 'Pineapples', 'Papayas', 'Plantains', 'Avocados'],
    'Cash Crops': ['Coffee Beans', 'Cocoa Beans', 'Cotton', 'Sesame'],
    'Spices': ['Ginger', 'Turmeric', 'Black Pepper', 'Chili Peppers'],
    'Oil Crops': ['Palm Oil', 'Shea Nuts']
}

# Regional crop specialties
REGIONAL_SPECIALTIES = {
    'West Africa': ['Yam', 'Cassava', 'Cocoa Beans', 'Palm Oil', 'Plantains', 'Ginger'],
    'East Africa': ['Coffee Beans', 'Bananas', 'Sweet Potato', 'Avocados', 'Teff'],
    'North Africa': ['Oranges', 'Tomatoes', 'Onions', 'Cotton'],
    'Southern Africa': ['Maize', 'Spinach', 'Groundnuts'],
    'Central Africa': ['Cassava', 'Plantains', 'Coffee Beans', 'Palm Oil']
}

# Seasonal planting calendar
PLANTING_CALENDAR = {
    'Wet Season (April-September)': [
        'Maize', 'Rice', 'Yam', 'Sweet Potato', 'Cowpeas', 'Groundnuts',
        'Tomatoes', 'Cabbage', 'Okra', 'Ginger', 'Chili Peppers'
    ],
    'Dry Season (October-March)': [
        'Millet', 'Sorghum', 'Onions', 'Oranges', 'Sesame', 'Cotton'
    ],
    'Year-round': [
        'Cassava', 'Bananas', 'Plantains', 'Pineapples', 'Papayas', 'Avocados', 'Palm Oil'
    ]
}

def get_crops_by_category(category):
    """Get all crops in a specific category"""
    return [crop for crop in AFRICAN_CROPS if crop['category'] == category]

def get_crops_by_region(region):
    """Get all crops available in a specific region"""
    return [crop for crop in AFRICAN_CROPS if region.lower() in crop['region'].lower()]

def get_seasonal_crops(season):
    """Get crops suitable for a specific season"""
    return [crop for crop in AFRICAN_CROPS if crop['season'] == season or crop['season'] == 'year-round']

def get_crop_by_name(name):
    """Get crop details by name"""
    for crop in AFRICAN_CROPS:
        if crop['name'].lower() == name.lower():
            return crop
    return None

def get_price_range(category=None):
    """Get price range for crops in a category or all crops"""
    if category:
        crops = get_crops_by_category(category)
    else:
        crops = AFRICAN_CROPS
    
    prices = [crop['price_per_kg'] for crop in crops]
    return {
        'min': min(prices),
        'max': max(prices),
        'average': sum(prices) / len(prices)
    }

def search_crops(query, filters=None):
    """Search crops by name or description with optional filters"""
    results = []
    query = query.lower()
    
    for crop in AFRICAN_CROPS:
        # Search in name and category
        if (query in crop['name'].lower() or 
            query in crop['category'].lower() or 
            query in crop['region'].lower()):
            
            # Apply filters if provided
            if filters:
                if filters.get('category') and crop['category'] != filters['category']:
                    continue
                if filters.get('region') and filters['region'].lower() not in crop['region'].lower():
                    continue
                if filters.get('max_price') and crop['price_per_kg'] > filters['max_price']:
                    continue
                if filters.get('min_price') and crop['price_per_kg'] < filters['min_price']:
                    continue
                if filters.get('season') and crop['season'] != filters['season'] and crop['season'] != 'year-round':
                    continue
            
            results.append(crop)
    
    return results
