import requests
import os
import random
from datetime import datetime, timedelta

def get_weather_info(location):
    """Get weather information for a specific location"""
    
    # Try to get real weather data from API
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if api_key:
        try:
            return get_real_weather_data(location, api_key)
        except:
            pass
    
    # Fallback to realistic mock data
    return get_mock_weather_data(location)

def get_real_weather_data(location, api_key):
    """Get real weather data from OpenWeatherMap API"""
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'
    }
    
    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    
    # Extract relevant information
    weather_info = {
        'location': location,
        'temperature': round(data['main']['temp']),
        'humidity': data['main']['humidity'],
        'rainfall': 0,  # Current weather doesn't include rainfall
        'wind_speed': round(data['wind']['speed'] * 3.6),  # Convert m/s to km/h
        'description': data['weather'][0]['description'].title(),
        'pressure': data['main']['pressure'],
        'visibility': data.get('visibility', 10000) / 1000,  # Convert to km
        'uv_index': get_uv_index(data['coord']['lat'], data['coord']['lon'], api_key),
        'advice': generate_agricultural_advice(data)
    }
    
    return weather_info

def get_uv_index(lat, lon, api_key):
    """Get UV index for given coordinates"""
    try:
        uv_url = "https://api.openweathermap.org/data/2.5/uvi"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key
        }
        
        response = requests.get(uv_url, params=params, timeout=5)
        data = response.json()
        return round(data.get('value', 5))
    except:
        return random.randint(3, 9)

def get_mock_weather_data(location):
    """Generate realistic mock weather data for African locations"""
    
    # Base weather patterns for different African regions
    weather_patterns = {
        'sahel': {
            'temp_range': (25, 40),
            'humidity_range': (20, 60),
            'rainfall_range': (0, 15),
            'wind_range': (10, 25)
        },
        'coastal': {
            'temp_range': (22, 32),
            'humidity_range': (60, 85),
            'rainfall_range': (0, 25),
            'wind_range': (15, 30)
        },
        'highland': {
            'temp_range': (15, 28),
            'humidity_range': (40, 75),
            'rainfall_range': (0, 20),
            'wind_range': (8, 20)
        },
        'tropical': {
            'temp_range': (24, 35),
            'humidity_range': (65, 90),
            'rainfall_range': (0, 35),
            'wind_range': (5, 18)
        }
    }
    
    # Determine region type based on location
    region_type = 'tropical'  # Default
    location_lower = location.lower()
    
    if any(sahel in location_lower for sahel in ['mali', 'niger', 'chad', 'sudan', 'burkina']):
        region_type = 'sahel'
    elif any(coastal in location_lower for coastal in ['lagos', 'accra', 'dakar', 'cape town', 'mombasa']):
        region_type = 'coastal'
    elif any(highland in location_lower for highland in ['nairobi', 'addis ababa', 'kampala', 'kigali']):
        region_type = 'highland'
    
    pattern = weather_patterns[region_type]
    
    # Generate seasonal adjustments
    current_month = datetime.now().month
    
    # Dry season (November to March)
    if current_month in [11, 12, 1, 2, 3]:
        temp_adjustment = 2
        humidity_adjustment = -10
        rainfall_adjustment = -5
    # Wet season (April to October)
    else:
        temp_adjustment = -1
        humidity_adjustment = 5
        rainfall_adjustment = 10
    
    weather_info = {
        'location': location,
        'temperature': random.randint(*pattern['temp_range']) + temp_adjustment,
        'humidity': max(20, min(95, random.randint(*pattern['humidity_range']) + humidity_adjustment)),
        'rainfall': max(0, random.randint(*pattern['rainfall_range']) + rainfall_adjustment),
        'wind_speed': random.randint(*pattern['wind_range']),
        'description': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Clear']),
        'pressure': random.randint(1010, 1025),
        'visibility': random.randint(8, 15),
        'uv_index': random.randint(6, 11),
        'advice': generate_mock_agricultural_advice(region_type, current_month)
    }
    
    return weather_info

def generate_agricultural_advice(weather_data):
    """Generate agricultural advice based on real weather data"""
    
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    
    advice = []
    
    # Temperature-based advice
    if temp > 35:
        advice.append("High temperatures - ensure adequate irrigation and provide shade for livestock.")
    elif temp < 15:
        advice.append("Cool temperatures - protect sensitive crops and delay planting of warm-season crops.")
    else:
        advice.append("Favorable temperatures for most crop activities.")
    
    # Humidity-based advice
    if humidity > 80:
        advice.append("High humidity increases disease risk - monitor crops for fungal infections.")
    elif humidity < 30:
        advice.append("Low humidity - increase irrigation frequency and consider mulching.")
    
    # Wind-based advice
    wind_speed = weather_data.get('wind', {}).get('speed', 0) * 3.6
    if wind_speed > 20:
        advice.append("Strong winds expected - secure structures and delay spraying activities.")
    
    return " ".join(advice)

def generate_mock_agricultural_advice(region_type, month):
    """Generate mock agricultural advice based on region and season"""
    
    seasonal_advice = {
        'dry_season': [
            "Focus on irrigation and water conservation techniques.",
            "Good time for land preparation and soil improvement.",
            "Consider drought-resistant crop varieties.",
            "Protect livestock from heat stress.",
            "Harvest and store crops properly to prevent pest damage."
        ],
        'wet_season': [
            "Ensure proper drainage to prevent waterlogging.",
            "Monitor crops for fungal diseases due to high humidity.",
            "Good conditions for planting most crops.",
            "Weed control is crucial during this period.",
            "Take advantage of natural rainfall for crop establishment."
        ]
    }
    
    regional_advice = {
        'sahel': [
            "Water conservation is critical in this region.",
            "Consider agroforestry practices to combat desertification.",
            "Early planting recommended to maximize growing season."
        ],
        'coastal': [
            "High humidity may increase pest and disease pressure.",
            "Good conditions for rice and vegetable production.",
            "Salt-tolerant varieties recommended near the coast."
        ],
        'highland': [
            "Cool temperatures favor temperate crops like potatoes and wheat.",
            "Frost protection may be needed during cool months.",
            "Excellent conditions for coffee and tea cultivation."
        ],
        'tropical': [
            "Year-round growing season allows for multiple harvests.",
            "Disease management is crucial in this humid environment.",
            "Ideal for tropical fruits and root crops."
        ]
    }
    
    # Determine season
    season = 'dry_season' if month in [11, 12, 1, 2, 3] else 'wet_season'
    
    # Combine seasonal and regional advice
    advice_pool = seasonal_advice[season] + regional_advice[region_type]
    selected_advice = random.sample(advice_pool, min(2, len(advice_pool)))
    
    return " ".join(selected_advice)

def get_extended_forecast(location, days=7):
    """Get extended weather forecast for multiple days"""
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if api_key:
        try:
            return get_real_extended_forecast(location, api_key, days)
        except:
            pass
    
    # Fallback to mock forecast
    return get_mock_extended_forecast(location, days)

def get_real_extended_forecast(location, api_key, days):
    """Get real extended forecast from OpenWeatherMap API"""
    
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric',
        'cnt': days * 8  # 8 forecasts per day (every 3 hours)
    }
    
    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    
    # Process forecast data
    daily_forecasts = []
    current_date = None
    daily_data = []
    
    for item in data['list']:
        forecast_date = datetime.fromtimestamp(item['dt']).date()
        
        if current_date != forecast_date:
            if daily_data:
                # Process previous day's data
                daily_forecast = process_daily_forecast_data(daily_data, current_date)
                daily_forecasts.append(daily_forecast)
            
            current_date = forecast_date
            daily_data = [item]
        else:
            daily_data.append(item)
    
    # Process last day
    if daily_data:
        daily_forecast = process_daily_forecast_data(daily_data, current_date)
        daily_forecasts.append(daily_forecast)
    
    return daily_forecasts[:days]

def process_daily_forecast_data(daily_data, date):
    """Process hourly forecast data into daily summary"""
    
    temps = [item['main']['temp'] for item in daily_data]
    humidities = [item['main']['humidity'] for item in daily_data]
    descriptions = [item['weather'][0]['description'] for item in daily_data]
    
    return {
        'date': date.strftime('%A, %B %d'),
        'min_temp': round(min(temps)),
        'max_temp': round(max(temps)),
        'avg_humidity': round(sum(humidities) / len(humidities)),
        'description': max(set(descriptions), key=descriptions.count),
        'rainfall_probability': random.randint(0, 100)  # Not available in free API
    }

def get_mock_extended_forecast(location, days):
    """Generate mock extended forecast"""
    
    base_weather = get_mock_weather_data(location)
    forecasts = []
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        
        # Add some variation to base weather
        temp_variation = random.randint(-3, 3)
        humidity_variation = random.randint(-10, 10)
        
        forecast = {
            'date': date.strftime('%A, %B %d'),
            'min_temp': base_weather['temperature'] - 5 + temp_variation,
            'max_temp': base_weather['temperature'] + 5 + temp_variation,
            'avg_humidity': max(20, min(95, base_weather['humidity'] + humidity_variation)),
            'description': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Clear']),
            'rainfall_probability': random.randint(0, 80)
        }
        
        forecasts.append(forecast)
    
    return forecasts

def get_agricultural_calendar(location, crop_type=None):
    """Get agricultural calendar and recommendations for specific location and crop"""
    
    calendar_data = {
        'planting_seasons': [],
        'harvest_seasons': [],
        'pest_alerts': [],
        'irrigation_schedule': [],
        'fertilizer_schedule': []
    }
    
    # Get current weather to inform recommendations
    current_weather = get_weather_info(location)
    current_month = datetime.now().month
    
    # Define planting and harvest seasons for major African crops
    crop_calendars = {
        'maize': {
            'planting': [4, 5, 6],  # April-June (wet season)
            'harvest': [9, 10, 11], # September-November
            'water_needs': 'moderate',
            'pest_season': [6, 7, 8]
        },
        'rice': {
            'planting': [5, 6, 7],  # May-July
            'harvest': [10, 11, 12], # October-December
            'water_needs': 'high',
            'pest_season': [7, 8, 9]
        },
        'cassava': {
            'planting': [3, 4, 5, 6], # March-June
            'harvest': [12, 1, 2],    # December-February (following year)
            'water_needs': 'low',
            'pest_season': [8, 9, 10]
        }
    }
    
    if crop_type and crop_type.lower() in crop_calendars:
        crop_info = crop_calendars[crop_type.lower()]
        
        # Planting recommendations
        if current_month in crop_info['planting']:
            calendar_data['planting_seasons'].append(f"Optimal planting time for {crop_type}")
        
        # Harvest recommendations
        if current_month in crop_info['harvest']:
            calendar_data['harvest_seasons'].append(f"Harvest season for {crop_type}")
        
        # Pest alerts
        if current_month in crop_info['pest_season']:
            calendar_data['pest_alerts'].append(f"Monitor {crop_type} for common pests")
    
    # General recommendations based on weather
    if current_weather['rainfall'] < 10:
        calendar_data['irrigation_schedule'].append("Increase irrigation frequency due to low rainfall")
    
    if current_weather['temperature'] > 30:
        calendar_data['irrigation_schedule'].append("Early morning irrigation recommended due to high temperatures")
    
    # Fertilizer schedule based on season
    if current_month in [3, 4, 5]:  # Early growing season
        calendar_data['fertilizer_schedule'].append("Apply base fertilizers before planting")
    elif current_month in [6, 7, 8]:  # Mid growing season
        calendar_data['fertilizer_schedule'].append("Top-dress with nitrogen fertilizers")
    
    return calendar_data
