import random
from data.crops import AFRICAN_CROPS

def get_recommendations(user):
    """Generate AI-powered recommendations for the user"""
    
    recommendations = []
    
    # Location-based recommendations
    user_location = user.get('location', '')
    if user_location:
        location_crops = [crop for crop in AFRICAN_CROPS if crop['region'] in user_location or user_location in crop['region']]
        if location_crops:
            crop = random.choice(location_crops)
            recommendations.append(f"Based on your location ({user_location}), {crop['name']} is in high demand with an average price of ${crop['price_per_kg']:.2f}/kg")
    
    # User type based recommendations
    if user.get('type') == 'farmer':
        recommendations.extend([
            "Weather forecast shows optimal planting conditions for maize in the next 2 weeks",
            "Cassava prices have increased by 12% this month - consider harvesting if ready",
            "New organic certification program available - could increase your product value by 20%",
            "Drought-resistant varieties are recommended for the upcoming dry season"
        ])
    else:  # buyer
        recommendations.extend([
            "Rice prices are expected to drop by 8% next week - consider waiting for better deals",
            "Fresh yam harvest from local farmers available at 15% below market price",
            "Bulk purchasing discounts available for orders above 100kg",
            "New suppliers in your area offering competitive prices for vegetables"
        ])
    
    # Seasonal recommendations
    import datetime
    current_month = datetime.datetime.now().month
    
    if current_month in [12, 1, 2]:  # Dry season
        recommendations.append("Dry season storage solutions: Consider investing in proper storage to reduce post-harvest losses")
    elif current_month in [6, 7, 8]:  # Rainy season
        recommendations.append("Rainy season alert: Focus on quick-harvesting crops and ensure proper drainage")
    
    # Market trend recommendations
    trending_crops = random.sample(AFRICAN_CROPS, 3)
    for crop in trending_crops:
        recommendations.append(f"{crop['name']} shows strong market performance with {random.randint(5, 25)}% price increase this quarter")
    
    # Quality and safety recommendations
    recommendations.extend([
        "Implement proper post-harvest handling to reduce losses by up to 30%",
        "Consider mobile storage solutions during peak harvest season",
        "Join farmer cooperatives to access better market prices and bulk discounts"
    ])
    
    # Return random selection of recommendations
    return random.sample(recommendations, min(5, len(recommendations)))

def get_product_recommendations(user, current_product=None):
    """Get product recommendations based on user behavior and preferences"""
    
    recommendations = []
    
    # If viewing a specific product, recommend similar ones
    if current_product:
        similar_products = [
            crop for crop in AFRICAN_CROPS 
            if crop['category'] == current_product.get('category') 
            and crop['name'] != current_product.get('name')
        ]
        recommendations.extend(random.sample(similar_products, min(3, len(similar_products))))
    
    # Location-based product recommendations
    user_location = user.get('location', '')
    if user_location:
        local_products = [
            crop for crop in AFRICAN_CROPS 
            if crop['region'] in user_location or user_location in crop['region']
        ]
        recommendations.extend(random.sample(local_products, min(2, len(local_products))))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_recommendations = []
    for item in recommendations:
        if item['name'] not in seen:
            seen.add(item['name'])
            unique_recommendations.append(item)
    
    return unique_recommendations[:5]

def get_price_predictions(crop_name):
    """Generate price prediction for a specific crop"""
    
    # Find the crop in our database
    crop = next((c for c in AFRICAN_CROPS if c['name'].lower() == crop_name.lower()), None)
    
    if not crop:
        return None
    
    current_price = crop['price_per_kg']
    
    # Generate realistic price fluctuations
    factors = {
        'seasonal': random.uniform(-0.2, 0.3),  # Seasonal variation
        'weather': random.uniform(-0.15, 0.25),  # Weather impact
        'demand': random.uniform(-0.1, 0.2),     # Market demand
        'supply': random.uniform(-0.2, 0.1)      # Supply chain factors
    }
    
    predictions = []
    
    for week in range(1, 5):  # 4-week prediction
        price_change = sum(factors.values()) * random.uniform(0.5, 1.5)
        predicted_price = current_price * (1 + price_change)
        predicted_price = max(0.1, predicted_price)  # Ensure positive price
        
        predictions.append({
            'week': week,
            'predicted_price': round(predicted_price, 2),
            'change_percentage': round(price_change * 100, 1),
            'confidence': random.randint(75, 95)
        })
        
        # Update current price for next week's calculation
        current_price = predicted_price
        
        # Add some randomness to factors for next week
        for key in factors:
            factors[key] += random.uniform(-0.05, 0.05)
    
    return {
        'crop_name': crop['name'],
        'current_price': crop['price_per_kg'],
        'predictions': predictions,
        'factors': {
            'weather_impact': 'Moderate rainfall expected',
            'seasonal_trend': 'Peak harvest season approaching',
            'market_demand': 'Steady demand from urban centers',
            'supply_status': 'Adequate supply in most regions'
        }
    }

def get_farming_recommendations(user_location, crop_type=None):
    """Get farming recommendations based on location and crop type"""
    
    recommendations = {
        'planting_calendar': [],
        'best_practices': [],
        'risk_factors': [],
        'yield_optimization': []
    }
    
    # Planting calendar recommendations
    import datetime
    current_month = datetime.datetime.now().month
    
    planting_seasons = {
        'wet_season': [4, 5, 6, 7],
        'dry_season': [11, 12, 1, 2],
        'transition': [3, 8, 9, 10]
    }
    
    if current_month in planting_seasons['wet_season']:
        recommendations['planting_calendar'] = [
            "Optimal time for planting maize, rice, and vegetables",
            "Ensure proper drainage for root crops",
            "Consider early-maturing varieties for quick harvest"
        ]
    elif current_month in planting_seasons['dry_season']:
        recommendations['planting_calendar'] = [
            "Focus on drought-resistant crops like millet and sorghum",
            "Implement irrigation systems for continuous production",
            "Plant legumes to improve soil fertility"
        ]
    
    # Best practices
    recommendations['best_practices'] = [
        "Use certified seeds for better yields and disease resistance",
        "Apply organic fertilizers to improve soil health",
        "Practice crop rotation to maintain soil fertility",
        "Implement integrated pest management strategies",
        "Harvest at optimal maturity for better market prices"
    ]
    
    # Risk factors
    recommendations['risk_factors'] = [
        "Monitor weather patterns for drought or flood risks",
        "Watch for pest outbreaks in neighboring farms",
        "Keep updated on market price fluctuations",
        "Ensure access to post-harvest storage facilities",
        "Consider crop insurance for high-value crops"
    ]
    
    # Yield optimization
    recommendations['yield_optimization'] = [
        "Space plants appropriately for optimal growth",
        "Apply fertilizers based on soil test recommendations",
        "Maintain proper weed control throughout growing season",
        "Ensure adequate water supply during critical growth stages",
        "Use modern farming tools and techniques"
    ]
    
    return recommendations
