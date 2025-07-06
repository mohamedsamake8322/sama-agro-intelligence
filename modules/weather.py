import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.weather import get_weather_info, get_extended_forecast, get_agricultural_calendar
from utils.translations import get_translation
from data.locations import AFRICAN_LOCATIONS

def weather_page():
    """Weather information and agricultural advice page"""
    
    st.title("🌤️ " + get_translation("weather_forecast", st.session_state.language))
    
    # Location selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_location = st.selectbox(
            get_translation("select_location", st.session_state.language),
            AFRICAN_LOCATIONS,
            index=0 if not st.session_state.user else 
                  (AFRICAN_LOCATIONS.index(st.session_state.user.get('location', AFRICAN_LOCATIONS[0])) 
                   if st.session_state.user.get('location') in AFRICAN_LOCATIONS else 0)
        )
    
    with col2:
        if st.button("🔄 Refresh Weather"):
            st.rerun()
    
    # Get weather information
    weather_info = get_weather_info(selected_location)
    extended_forecast = get_extended_forecast(selected_location)
    
    # Current weather display
    display_current_weather(weather_info)
    
    # Weather tabs
    forecast_tab, advice_tab, calendar_tab, alerts_tab = st.tabs([
        get_translation("weekly_forecast", st.session_state.language),
        get_translation("agricultural_advice", st.session_state.language),
        "Planting Calendar",
        "Weather Alerts"
    ])
    
    with forecast_tab:
        display_extended_forecast(extended_forecast)
    
    with advice_tab:
        display_agricultural_advice(weather_info, selected_location)
    
    with calendar_tab:
        display_agricultural_calendar(selected_location)
    
    with alerts_tab:
        display_weather_alerts(weather_info, selected_location)

def display_current_weather(weather_info):
    """Display current weather conditions"""
    
    st.subheader(f"🌍 Current Weather - {weather_info['location']}")
    
    # Main weather metrics
    weather_col1, weather_col2, weather_col3, weather_col4 = st.columns(4)
    
    with weather_col1:
        st.metric(
            get_translation("temperature", st.session_state.language),
            f"{weather_info['temperature']}°C",
            help="Current temperature"
        )
    
    with weather_col2:
        st.metric(
            get_translation("humidity", st.session_state.language),
            f"{weather_info['humidity']}%",
            help="Relative humidity"
        )
    
    with weather_col3:
        st.metric(
            get_translation("rainfall", st.session_state.language),
            f"{weather_info['rainfall']}mm",
            help="Rainfall in last 24 hours"
        )
    
    with weather_col4:
        st.metric(
            get_translation("wind_speed", st.session_state.language),
            f"{weather_info['wind_speed']} km/h",
            help="Current wind speed"
        )
    
    # Additional weather details
    with st.expander("📊 Detailed Weather Information"):
        detail_col1, detail_col2, detail_col3 = st.columns(3)
        
        with detail_col1:
            st.write(f"**Description:** {weather_info.get('description', 'Clear')}")
            st.write(f"**Pressure:** {weather_info.get('pressure', 1013)} hPa")
        
        with detail_col2:
            st.write(f"**Visibility:** {weather_info.get('visibility', 10)} km")
            st.write(f"**UV Index:** {weather_info.get('uv_index', 5)}")
        
        with detail_col3:
            st.write(f"**Feels Like:** {weather_info['temperature'] + 2}°C")
            st.write(f"**Dew Point:** {weather_info['temperature'] - 5}°C")
    
    # Weather advice banner
    if weather_info.get('advice'):
        st.info(f"💡 **Agricultural Advice:** {weather_info['advice']}")

def display_extended_forecast(extended_forecast):
    """Display 7-day weather forecast"""
    
    st.subheader("📅 7-Day Weather Forecast")
    
    if not extended_forecast:
        st.warning("Extended forecast not available at the moment.")
        return
    
    # Create forecast display
    forecast_data = []
    for day_forecast in extended_forecast:
        forecast_data.append({
            'Date': day_forecast['date'],
            'Min Temp (°C)': day_forecast['min_temp'],
            'Max Temp (°C)': day_forecast['max_temp'],
            'Humidity (%)': day_forecast['avg_humidity'],
            'Description': day_forecast['description'],
            'Rain Probability (%)': day_forecast.get('rainfall_probability', 0)
        })
    
    df_forecast = pd.DataFrame(forecast_data)
    
    # Temperature trend chart
    fig_temp = go.Figure()
    
    fig_temp.add_trace(go.Scatter(
        x=df_forecast['Date'],
        y=df_forecast['Max Temp (°C)'],
        mode='lines+markers',
        name='Max Temperature',
        line=dict(color='red', width=3),
        marker=dict(size=8)
    ))
    
    fig_temp.add_trace(go.Scatter(
        x=df_forecast['Date'],
        y=df_forecast['Min Temp (°C)'],
        mode='lines+markers',
        name='Min Temperature',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))
    
    fig_temp.update_layout(
        title="Temperature Forecast",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Rainfall probability chart
    fig_rain = px.bar(
        df_forecast,
        x='Date',
        y='Rain Probability (%)',
        title="Rainfall Probability",
        color='Rain Probability (%)',
        color_continuous_scale='Blues'
    )
    
    st.plotly_chart(fig_rain, use_container_width=True)
    
    # Detailed forecast table
    st.subheader("📋 Detailed Forecast")
    st.dataframe(df_forecast, use_container_width=True)

def display_agricultural_advice(weather_info, location):
    """Display agricultural advice based on current weather"""
    
    st.subheader("🌾 " + get_translation("agricultural_advice", st.session_state.language))
    
    # Weather-based farming recommendations
    advice_sections = generate_agricultural_advice(weather_info, location)
    
    # Current conditions advice
    st.write("### 🌤️ Current Conditions Advice")
    if weather_info.get('advice'):
        st.success(weather_info['advice'])
    
    # Seasonal recommendations
    st.write("### 📅 Seasonal Recommendations")
    current_month = datetime.now().month
    
    if current_month in [12, 1, 2]:  # Dry season
        seasonal_advice = [
            "🌵 **Dry Season Focus:** Prioritize drought-resistant crops like millet and sorghum",
            "💧 **Water Management:** Implement efficient irrigation systems and mulching",
            "🏪 **Storage:** Prepare proper storage facilities for harvest season",
            "🐄 **Livestock:** Ensure adequate water sources for animals"
        ]
    elif current_month in [6, 7, 8]:  # Peak wet season
        seasonal_advice = [
            "🌧️ **Wet Season Management:** Ensure proper drainage to prevent waterlogging",
            "🦠 **Disease Prevention:** Monitor crops for fungal diseases due to high humidity",
            "🌱 **Planting Opportunity:** Ideal time for planting most staple crops",
            "🌿 **Weed Control:** Intensive weeding required during rapid growth period"
        ]
    else:  # Transition periods
        seasonal_advice = [
            "🔄 **Transition Period:** Prepare for upcoming season changes",
            "🌾 **Land Preparation:** Good time for soil preparation and improvement",
            "📋 **Planning:** Review and plan crop rotation strategies",
            "🛠️ **Equipment:** Maintain and prepare farming equipment"
        ]
    
    for advice in seasonal_advice:
        st.write(advice)
    
    # Crop-specific advice
    st.write("### 🌾 Crop-Specific Advice")
    
    crop_advice_col1, crop_advice_col2 = st.columns(2)
    
    with crop_advice_col1:
        st.write("**🌽 Grains & Cereals**")
        if weather_info['temperature'] > 30:
            st.write("- High temperatures may stress cereal crops")
            st.write("- Ensure adequate irrigation for maize and rice")
            st.write("- Consider heat-tolerant varieties")
        else:
            st.write("- Good conditions for grain production")
            st.write("- Monitor for optimal planting time")
        
        st.write("**🥕 Root Crops**")
        if weather_info['humidity'] > 80:
            st.write("- High humidity increases disease risk for tubers")
            st.write("- Ensure good drainage for cassava and yam")
            st.write("- Monitor for fungal infections")
        else:
            st.write("- Favorable conditions for root crop development")
    
    with crop_advice_col2:
        st.write("**🥬 Vegetables**")
        if weather_info['rainfall'] > 20:
            st.write("- Heavy rainfall may damage leafy vegetables")
            st.write("- Provide protection for tomatoes and peppers")
            st.write("- Harvest mature vegetables before heavy rains")
        else:
            st.write("- Good conditions for vegetable cultivation")
        
        st.write("**🍎 Fruits**")
        if weather_info['wind_speed'] > 20:
            st.write("- Strong winds may damage fruit trees")
            st.write("- Provide support for young fruit trees")
            st.write("- Delay spraying activities")
        else:
            st.write("- Suitable conditions for fruit development")

def display_agricultural_calendar(location):
    """Display agricultural planting and harvesting calendar"""
    
    st.subheader("📅 Agricultural Calendar")
    
    # Get agricultural calendar data
    calendar_data = get_agricultural_calendar(location)
    
    # Current month activities
    current_month = datetime.now().month
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    current_month_name = month_names[current_month - 1]
    
    st.write(f"### 📆 Current Month: {current_month_name}")
    
    # Monthly recommendations
    monthly_activities = get_monthly_activities(current_month, location)
    
    activity_col1, activity_col2 = st.columns(2)
    
    with activity_col1:
        st.write("**🌱 Planting Activities**")
        for activity in monthly_activities.get('planting', []):
            st.write(f"- {activity}")
        
        st.write("**🌾 Harvesting Activities**")
        for activity in monthly_activities.get('harvesting', []):
            st.write(f"- {activity}")
    
    with activity_col2:
        st.write("**🛠️ Farm Management**")
        for activity in monthly_activities.get('management', []):
            st.write(f"- {activity}")
        
        st.write("**⚠️ Important Reminders**")
        for reminder in monthly_activities.get('reminders', []):
            st.write(f"- {reminder}")
    
    # Yearly planting calendar
    st.write("### 📊 Annual Planting Calendar")
    
    # Create calendar visualization
    calendar_matrix = create_planting_calendar_matrix()
    
    fig_calendar = px.imshow(
        calendar_matrix['data'],
        x=calendar_matrix['months'],
        y=calendar_matrix['crops'],
        color_continuous_scale='Greens',
        title="Optimal Planting Times",
        labels={'color': 'Suitability Score'}
    )
    
    fig_calendar.update_layout(
        xaxis_title="Month",
        yaxis_title="Crops",
        height=400
    )
    
    st.plotly_chart(fig_calendar, use_container_width=True)
    
    # Legend
    st.write("**Legend:** Dark green = Optimal planting time, Light green = Suitable, White = Not recommended")

def display_weather_alerts(weather_info, location):
    """Display weather alerts and warnings"""
    
    st.subheader("⚠️ Weather Alerts & Warnings")
    
    # Generate alerts based on weather conditions
    alerts = generate_weather_alerts(weather_info)
    
    if alerts:
        for alert in alerts:
            alert_type = alert['type']
            message = alert['message']
            severity = alert['severity']
            
            if severity == 'high':
                st.error(f"🔴 **{alert_type.upper()}:** {message}")
            elif severity == 'medium':
                st.warning(f"🟡 **{alert_type.upper()}:** {message}")
            else:
                st.info(f"🔵 **{alert_type.upper()}:** {message}")
    else:
        st.success("✅ No weather alerts at this time. Conditions are favorable for farming activities.")
    
    # Agricultural impact assessment
    st.write("### 🌾 Agricultural Impact Assessment")
    
    impact_col1, impact_col2 = st.columns(2)
    
    with impact_col1:
        st.write("**Current Risk Levels:**")
        risk_factors = assess_agricultural_risks(weather_info)
        
        for factor, level in risk_factors.items():
            color = "🟢" if level == "Low" else "🟡" if level == "Medium" else "🔴"
            st.write(f"{color} {factor}: {level}")
    
    with impact_col2:
        st.write("**Recommended Actions:**")
        actions = get_recommended_actions(weather_info)
        
        for action in actions:
            st.write(f"• {action}")
    
    # Historical weather patterns
    st.write("### 📈 Historical Weather Patterns")
    
    # Create mock historical data for the location
    historical_data = generate_historical_weather_data(location)
    
    fig_historical = go.Figure()
    
    fig_historical.add_trace(go.Scatter(
        x=historical_data['months'],
        y=historical_data['temperature'],
        mode='lines+markers',
        name='Average Temperature',
        yaxis='y1',
        line=dict(color='red')
    ))
    
    fig_historical.add_trace(go.Bar(
        x=historical_data['months'],
        y=historical_data['rainfall'],
        name='Average Rainfall',
        yaxis='y2',
        opacity=0.7
    ))
    
    fig_historical.update_layout(
        title="Historical Weather Patterns",
        xaxis_title="Month",
        yaxis=dict(title="Temperature (°C)", side="left"),
        yaxis2=dict(title="Rainfall (mm)", side="right", overlaying="y"),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_historical, use_container_width=True)

def generate_agricultural_advice(weather_info, location):
    """Generate comprehensive agricultural advice based on weather"""
    
    advice = {
        'irrigation': [],
        'planting': [],
        'harvesting': [],
        'pest_management': [],
        'soil_management': []
    }
    
    temp = weather_info['temperature']
    humidity = weather_info['humidity']
    rainfall = weather_info['rainfall']
    wind_speed = weather_info['wind_speed']
    
    # Temperature-based advice
    if temp > 35:
        advice['irrigation'].append("Increase irrigation frequency due to high temperatures")
        advice['harvesting'].append("Harvest early in the morning to avoid heat stress")
    elif temp < 15:
        advice['planting'].append("Delay planting of heat-loving crops")
        advice['soil_management'].append("Consider soil warming techniques")
    
    # Humidity-based advice
    if humidity > 80:
        advice['pest_management'].append("Monitor for fungal diseases in high humidity")
        advice['harvesting'].append("Ensure proper drying after harvest")
    elif humidity < 30:
        advice['irrigation'].append("Increase irrigation to compensate for low humidity")
    
    # Rainfall-based advice
    if rainfall > 25:
        advice['soil_management'].append("Ensure proper drainage to prevent waterlogging")
        advice['planting'].append("Delay field operations until soil conditions improve")
    elif rainfall < 5:
        advice['irrigation'].append("Supplemental irrigation recommended")
    
    # Wind-based advice
    if wind_speed > 20:
        advice['pest_management'].append("Delay spraying activities due to strong winds")
        advice['harvesting'].append("Secure harvested crops and equipment")
    
    return advice

def get_monthly_activities(month, location):
    """Get farming activities for a specific month"""
    
    activities = {
        'planting': [],
        'harvesting': [],
        'management': [],
        'reminders': []
    }
    
    # Define activities by month (simplified)
    if month in [4, 5, 6]:  # Wet season planting
        activities['planting'] = [
            "Plant maize, rice, and vegetables",
            "Establish tree seedlings",
            "Start nurseries for transplanting"
        ]
        activities['management'] = [
            "Prepare and test irrigation systems",
            "Apply base fertilizers",
            "Control weeds in existing crops"
        ]
    elif month in [9, 10, 11]:  # Harvest season
        activities['harvesting'] = [
            "Harvest mature cereals",
            "Collect and process fruits",
            "Prepare storage facilities"
        ]
        activities['management'] = [
            "Post-harvest processing",
            "Market planning and sales",
            "Equipment maintenance"
        ]
    elif month in [12, 1, 2]:  # Dry season
        activities['planting'] = [
            "Plant drought-resistant crops",
            "Establish dry season vegetables with irrigation"
        ]
        activities['management'] = [
            "Soil preparation for next season",
            "Water conservation measures",
            "Livestock management"
        ]
    
    # Common reminders throughout the year
    activities['reminders'] = [
        "Monitor weather forecasts daily",
        "Check crop health regularly",
        "Maintain farm records",
        "Plan for upcoming season"
    ]
    
    return activities

def create_planting_calendar_matrix():
    """Create matrix data for planting calendar visualization"""
    
    crops = ['Maize', 'Rice', 'Cassava', 'Yam', 'Tomatoes', 'Onions', 'Millet', 'Sorghum']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Create suitability matrix (0-3: 0=not suitable, 3=optimal)
    import random
    data = []
    for crop in crops:
        row = []
        for month_idx in range(12):
            # Create realistic planting patterns
            if crop in ['Maize', 'Rice']:  # Wet season crops
                if month_idx in [3, 4, 5]:  # Apr-Jun
                    suitability = 3
                elif month_idx in [2, 6]:  # Mar, Jul
                    suitability = 2
                else:
                    suitability = 0
            elif crop in ['Millet', 'Sorghum']:  # Dry season crops
                if month_idx in [10, 11, 0]:  # Nov-Jan
                    suitability = 3
                elif month_idx in [9, 1]:  # Oct, Feb
                    suitability = 2
                else:
                    suitability = 0
            else:  # Other crops
                suitability = random.randint(0, 3)
            
            row.append(suitability)
        data.append(row)
    
    return {
        'data': data,
        'crops': crops,
        'months': months
    }

def generate_weather_alerts(weather_info):
    """Generate weather alerts based on current conditions"""
    
    alerts = []
    
    temp = weather_info['temperature']
    humidity = weather_info['humidity']
    rainfall = weather_info['rainfall']
    wind_speed = weather_info['wind_speed']
    
    # Temperature alerts
    if temp > 40:
        alerts.append({
            'type': 'Extreme Heat',
            'message': 'Extremely high temperatures may cause severe crop stress. Implement emergency cooling measures.',
            'severity': 'high'
        })
    elif temp > 35:
        alerts.append({
            'type': 'Heat Advisory',
            'message': 'High temperatures detected. Increase irrigation and provide shade for sensitive crops.',
            'severity': 'medium'
        })
    elif temp < 10:
        alerts.append({
            'type': 'Cold Warning',
            'message': 'Cold temperatures may damage tropical crops. Consider protective measures.',
            'severity': 'high'
        })
    
    # Rainfall alerts
    if rainfall > 50:
        alerts.append({
            'type': 'Heavy Rainfall',
            'message': 'Heavy rainfall may cause flooding and crop damage. Ensure proper drainage.',
            'severity': 'high'
        })
    elif rainfall > 30:
        alerts.append({
            'type': 'Moderate Rainfall',
            'message': 'Significant rainfall expected. Monitor for waterlogging in low-lying areas.',
            'severity': 'medium'
        })
    
    # Wind alerts
    if wind_speed > 30:
        alerts.append({
            'type': 'Strong Wind Warning',
            'message': 'Strong winds may damage crops and structures. Secure loose items and delay field operations.',
            'severity': 'high'
        })
    elif wind_speed > 20:
        alerts.append({
            'type': 'Wind Advisory',
            'message': 'Moderate winds expected. Avoid pesticide applications and support tall crops.',
            'severity': 'medium'
        })
    
    # Humidity alerts
    if humidity > 90:
        alerts.append({
            'type': 'High Humidity Alert',
            'message': 'Very high humidity increases disease risk. Monitor crops closely for fungal infections.',
            'severity': 'medium'
        })
    
    return alerts

def assess_agricultural_risks(weather_info):
    """Assess agricultural risks based on weather conditions"""
    
    risks = {}
    
    temp = weather_info['temperature']
    humidity = weather_info['humidity']
    rainfall = weather_info['rainfall']
    wind_speed = weather_info['wind_speed']
    
    # Heat stress risk
    if temp > 35:
        risks['Heat Stress'] = 'High'
    elif temp > 30:
        risks['Heat Stress'] = 'Medium'
    else:
        risks['Heat Stress'] = 'Low'
    
    # Disease risk
    if humidity > 80 and temp > 25:
        risks['Disease Pressure'] = 'High'
    elif humidity > 70:
        risks['Disease Pressure'] = 'Medium'
    else:
        risks['Disease Pressure'] = 'Low'
    
    # Drought risk
    if rainfall < 5 and temp > 30:
        risks['Drought Stress'] = 'High'
    elif rainfall < 10:
        risks['Drought Stress'] = 'Medium'
    else:
        risks['Drought Stress'] = 'Low'
    
    # Wind damage risk
    if wind_speed > 25:
        risks['Wind Damage'] = 'High'
    elif wind_speed > 15:
        risks['Wind Damage'] = 'Medium'
    else:
        risks['Wind Damage'] = 'Low'
    
    return risks

def get_recommended_actions(weather_info):
    """Get recommended actions based on weather conditions"""
    
    actions = []
    
    temp = weather_info['temperature']
    humidity = weather_info['humidity']
    rainfall = weather_info['rainfall']
    wind_speed = weather_info['wind_speed']
    
    if temp > 35:
        actions.append("Increase irrigation frequency and duration")
        actions.append("Provide shade for sensitive crops")
        actions.append("Harvest early morning or late evening")
    
    if humidity > 80:
        actions.append("Improve air circulation around crops")
        actions.append("Apply preventive fungicides if necessary")
        actions.append("Monitor for early signs of disease")
    
    if rainfall > 30:
        actions.append("Check and clear drainage channels")
        actions.append("Avoid heavy machinery on wet fields")
        actions.append("Cover harvested crops")
    
    if wind_speed > 20:
        actions.append("Secure farm equipment and structures")
        actions.append("Postpone spraying operations")
        actions.append("Support tall or heavy crops")
    
    if not actions:
        actions.append("Continue regular farming activities")
        actions.append("Monitor weather updates regularly")
    
    return actions

def generate_historical_weather_data(location):
    """Generate mock historical weather data for visualization"""
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Generate realistic seasonal patterns for African locations
    import random
    
    # Temperature pattern (varies by location)
    base_temp = 25
    temperature = []
    for i in range(12):
        seasonal_variation = 5 * (1 if i in [11, 0, 1, 2] else -1 if i in [5, 6, 7, 8] else 0)
        temp = base_temp + seasonal_variation + random.uniform(-2, 2)
        temperature.append(round(temp, 1))
    
    # Rainfall pattern (wet/dry seasons)
    rainfall = []
    for i in range(12):
        if i in [4, 5, 6, 7, 8, 9]:  # Wet season
            rain = random.uniform(80, 200)
        else:  # Dry season
            rain = random.uniform(5, 40)
        rainfall.append(round(rain, 1))
    
    return {
        'months': months,
        'temperature': temperature,
        'rainfall': rainfall
    }

