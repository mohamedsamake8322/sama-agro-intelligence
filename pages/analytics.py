import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from utils.translations import get_translation
from data.crops import AFRICAN_CROPS, CROP_CATEGORIES
from data.locations import AFRICAN_LOCATIONS

def analytics_page():
    """Market analytics and insights page"""
    
    st.title("📊 " + get_translation("market_analytics", st.session_state.language))
    
    # Analytics tabs
    overview_tab, trends_tab, regional_tab, predictions_tab = st.tabs([
        "Market Overview",
        get_translation("market_trends", st.session_state.language),
        "Regional Analysis",
        "Price Predictions"
    ])
    
    with overview_tab:
        display_market_overview()
    
    with trends_tab:
        display_market_trends()
    
    with regional_tab:
        display_regional_analysis()
    
    with predictions_tab:
        display_price_predictions()

def display_market_overview():
    """Display overall market statistics and key metrics"""
    
    st.subheader("📈 Market Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", "15,672", "+3.2%")
    with col2:
        st.metric("Active Farmers", "2,543", "+5.1%")
    with col3:
        st.metric("Daily Transactions", "127", "+8.7%")
    with col4:
        st.metric("Average Price/kg", "$2.85", "-2.1%")
    
    st.divider()
    
    # Market composition
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 " + get_translation("crop_distribution", st.session_state.language))
        
        # Create crop category distribution data
        category_data = {}
        for crop in AFRICAN_CROPS:
            category = crop['category']
            if category in category_data:
                category_data[category] += 1
            else:
                category_data[category] = 1
        
        # Create pie chart
        fig_pie = px.pie(
            values=list(category_data.values()),
            names=list(category_data.keys()),
            title="Crop Distribution by Category"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("🗺️ " + get_translation("regional_distribution", st.session_state.language))
        
        # Create regional data
        regional_data = {}
        for crop in AFRICAN_CROPS:
            region = crop['region']
            if region in regional_data:
                regional_data[region] += crop['price_per_kg']
            else:
                regional_data[region] = crop['price_per_kg']
        
        # Create bar chart
        regions = list(regional_data.keys())[:10]  # Top 10 regions
        values = [regional_data[region] for region in regions]
        
        fig_bar = px.bar(
            x=regions,
            y=values,
            title=get_translation("regional_sales", st.session_state.language),
            labels={'x': 'Region', 'y': get_translation("sales_usd", st.session_state.language)}
        )
        fig_bar.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Top performing products
    st.subheader("🏆 Top Performing Products")
    
    # Sort crops by price (as a proxy for performance)
    top_crops = sorted(AFRICAN_CROPS, key=lambda x: x['price_per_kg'], reverse=True)[:10]
    
    performance_data = []
    for i, crop in enumerate(top_crops):
        performance_data.append({
            'Rank': i + 1,
            'Product': crop['name'],
            'Category': crop['category'],
            'Price (USD/kg)': f"${crop['price_per_kg']:.2f}",
            'Region': crop['region'],
            'Trend': random.choice(['📈 Up', '📉 Down', '➡️ Stable'])
        })
    
    df_performance = pd.DataFrame(performance_data)
    st.dataframe(df_performance, use_container_width=True)

def display_market_trends():
    """Display market trends and price movements"""
    
    st.subheader("📈 " + get_translation("price_trends", st.session_state.language))
    
    # Time period selector
    time_periods = ["Last 7 Days", "Last 30 Days", "Last 3 Months", "Last Year"]
    selected_period = st.selectbox("Select Time Period", time_periods)
    
    # Product selector for detailed analysis
    product_names = [crop['name'] for crop in AFRICAN_CROPS]
    selected_products = st.multiselect(
        "Select Products to Compare",
        product_names,
        default=product_names[:5]
    )
    
    if selected_products:
        # Generate mock time series data
        price_data = generate_price_time_series(selected_products, selected_period)
        
        # Create price trend chart
        fig_trends = go.Figure()
        
        for product in selected_products:
            if product in price_data:
                fig_trends.add_trace(go.Scatter(
                    x=price_data[product]['dates'],
                    y=price_data[product]['prices'],
                    mode='lines+markers',
                    name=product,
                    line=dict(width=2)
                ))
        
        fig_trends.update_layout(
            title=get_translation("price_trends", st.session_state.language),
            xaxis_title="Date",
            yaxis_title=get_translation("price_usd_kg", st.session_state.language),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Price change summary
        st.subheader("📊 Price Change Summary")
        
        change_data = []
        for product in selected_products:
            if product in price_data:
                prices = price_data[product]['prices']
                start_price = prices[0]
                end_price = prices[-1]
                change_pct = ((end_price - start_price) / start_price) * 100
                
                change_data.append({
                    'Product': product,
                    'Start Price': f"${start_price:.2f}",
                    'Current Price': f"${end_price:.2f}",
                    'Change (%)': f"{change_pct:+.1f}%",
                    'Trend': '📈' if change_pct > 0 else '📉' if change_pct < 0 else '➡️'
                })
        
        df_changes = pd.DataFrame(change_data)
        st.dataframe(df_changes, use_container_width=True)
    
    # Market volatility analysis
    st.subheader("📈 Market Volatility")
    
    volatility_col1, volatility_col2 = st.columns(2)
    
    with volatility_col1:
        # Most volatile products
        volatile_products = random.sample(product_names, 5)
        volatility_scores = [random.uniform(5, 25) for _ in volatile_products]
        
        fig_volatility = px.bar(
            x=volatile_products,
            y=volatility_scores,
            title="Most Volatile Products (Last 30 Days)",
            labels={'x': 'Product', 'y': 'Volatility Score (%)'}
        )
        st.plotly_chart(fig_volatility, use_container_width=True)
    
    with volatility_col2:
        # Stability indicators
        st.write("**Market Stability Indicators**")
        stability_metrics = {
            'Overall Market Stability': '72%',
            'Price Prediction Accuracy': '89%',
            'Supply Chain Reliability': '94%',
            'Demand Forecast Confidence': '86%'
        }
        
        for metric, value in stability_metrics.items():
            st.metric(metric, value)

def display_regional_analysis():
    """Display regional market analysis"""
    
    st.subheader("🗺️ Regional Market Analysis")
    
    # Region selector
    selected_regions = st.multiselect(
        "Select Regions for Analysis",
        AFRICAN_LOCATIONS[:15],  # First 15 locations
        default=AFRICAN_LOCATIONS[:5]
    )
    
    if selected_regions:
        # Regional price comparison
        regional_price_data = []
        
        for region in selected_regions:
            regional_crops = [crop for crop in AFRICAN_CROPS if region.split(',')[0] in crop['region']]
            if regional_crops:
                avg_price = sum(crop['price_per_kg'] for crop in regional_crops) / len(regional_crops)
                total_products = len(regional_crops)
                
                regional_price_data.append({
                    'Region': region,
                    'Average Price (USD/kg)': round(avg_price, 2),
                    'Products Available': total_products,
                    'Market Activity': random.choice(['High', 'Medium', 'Low'])
                })
        
        if regional_price_data:
            # Regional comparison chart
            df_regional = pd.DataFrame(regional_price_data)
            
            fig_regional = px.bar(
                df_regional,
                x='Region',
                y='Average Price (USD/kg)',
                color='Market Activity',
                title="Average Prices by Region"
            )
            fig_regional.update_xaxes(tickangle=45)
            st.plotly_chart(fig_regional, use_container_width=True)
            
            # Regional data table
            st.dataframe(df_regional, use_container_width=True)
    
    # Supply and demand analysis
    st.subheader("⚖️ Supply & Demand Analysis")
    
    supply_demand_col1, supply_demand_col2 = st.columns(2)
    
    with supply_demand_col1:
        # Supply levels by category
        categories = list(CROP_CATEGORIES.keys())
        supply_levels = [random.randint(60, 95) for _ in categories]
        
        fig_supply = px.bar(
            x=categories,
            y=supply_levels,
            title="Supply Levels by Category (%)",
            color=supply_levels,
            color_continuous_scale="RdYlGn"
        )
        st.plotly_chart(fig_supply, use_container_width=True)
    
    with supply_demand_col2:
        # Demand forecast
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        demand_forecast = [random.randint(70, 120) for _ in months]
        
        fig_demand = px.line(
            x=months,
            y=demand_forecast,
            title="Demand Forecast (Next 6 Months)",
            markers=True
        )
        fig_demand.update_layout(yaxis_title="Demand Index")
        st.plotly_chart(fig_demand, use_container_width=True)

def display_price_predictions():
    """Display AI-powered price predictions"""
    
    st.subheader("🔮 AI Price Predictions")
    
    # Product selector for predictions
    product_for_prediction = st.selectbox(
        "Select Product for Price Prediction",
        [crop['name'] for crop in AFRICAN_CROPS]
    )
    
    if product_for_prediction:
        # Get crop data
        crop_data = next(crop for crop in AFRICAN_CROPS if crop['name'] == product_for_prediction)
        
        # Generate prediction data
        prediction_data = generate_price_predictions(crop_data)
        
        # Display current price and predictions
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric(
                "Current Price",
                f"${crop_data['price_per_kg']:.2f}/kg"
            )
            
            # Prediction factors
            st.subheader("🎯 Prediction Factors")
            factors = [
                ("🌦️ Weather Impact", random.choice(["Positive", "Neutral", "Negative"])),
                ("📈 Market Demand", random.choice(["High", "Medium", "Low"])),
                ("🚛 Supply Chain", random.choice(["Stable", "Disrupted", "Improving"])),
                ("🌍 Global Trends", random.choice(["Favorable", "Neutral", "Challenging"]))
            ]
            
            for factor, status in factors:
                color = "green" if status in ["Positive", "High", "Stable", "Favorable"] else "orange" if status in ["Neutral", "Medium", "Improving"] else "red"
                st.write(f"{factor}: :{color}[{status}]")
        
        with col2:
            # Prediction chart
            dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
            base_price = crop_data['price_per_kg']
            
            # Generate realistic price variations
            predictions = []
            current_price = base_price
            
            for i in range(30):
                # Add random walk with trend
                change = random.uniform(-0.1, 0.12)  # Slight upward bias
                current_price = max(0.1, current_price * (1 + change))
                predictions.append(current_price)
            
            fig_predictions = go.Figure()
            
            # Historical price (simulated)
            historical_dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
            historical_prices = [base_price * (1 + random.uniform(-0.2, 0.2)) for _ in range(30)]
            
            fig_predictions.add_trace(go.Scatter(
                x=historical_dates,
                y=historical_prices,
                mode='lines',
                name='Historical Prices',
                line=dict(color='blue', width=2)
            ))
            
            # Predicted prices
            fig_predictions.add_trace(go.Scatter(
                x=dates,
                y=predictions,
                mode='lines',
                name='Predicted Prices',
                line=dict(color='red', width=2, dash='dash')
            ))
            
            # Add confidence interval
            upper_bound = [p * 1.1 for p in predictions]
            lower_bound = [p * 0.9 for p in predictions]
            
            fig_predictions.add_trace(go.Scatter(
                x=dates,
                y=upper_bound,
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False
            ))
            
            fig_predictions.add_trace(go.Scatter(
                x=dates,
                y=lower_bound,
                fill='tonexty',
                mode='lines',
                line_color='rgba(0,0,0,0)',
                name='Confidence Interval',
                fillcolor='rgba(255,0,0,0.2)'
            ))
            
            fig_predictions.update_layout(
                title=f"Price Prediction for {product_for_prediction}",
                xaxis_title="Date",
                yaxis_title="Price (USD/kg)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_predictions, use_container_width=True)
        
        # Prediction summary
        st.subheader("📋 Prediction Summary")
        
        avg_predicted_price = sum(predictions) / len(predictions)
        price_change = ((avg_predicted_price - base_price) / base_price) * 100
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.metric(
                "30-Day Average Prediction",
                f"${avg_predicted_price:.2f}/kg",
                f"{price_change:+.1f}%"
            )
        
        with summary_col2:
            confidence_level = random.randint(75, 95)
            st.metric("Prediction Confidence", f"{confidence_level}%")
        
        with summary_col3:
            risk_level = random.choice(["Low", "Medium", "High"])
            st.metric("Price Volatility Risk", risk_level)

def generate_price_time_series(products, period):
    """Generate mock price time series data for selected products"""
    
    # Determine number of data points based on period
    if period == "Last 7 Days":
        days = 7
    elif period == "Last 30 Days":
        days = 30
    elif period == "Last 3 Months":
        days = 90
    else:  # Last Year
        days = 365
    
    price_data = {}
    
    for product in products:
        # Get base price for the product
        crop_data = next((crop for crop in AFRICAN_CROPS if crop['name'] == product), None)
        if not crop_data:
            continue
        
        base_price = crop_data['price_per_kg']
        
        # Generate dates
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), periods=days, freq='D')
        
        # Generate realistic price variations
        prices = []
        current_price = base_price
        
        for i in range(days):
            # Add seasonal and random variations
            seasonal_factor = 1 + 0.1 * (i / days)  # Slight seasonal trend
            random_factor = 1 + random.uniform(-0.05, 0.05)  # Daily random variation
            
            current_price = base_price * seasonal_factor * random_factor
            prices.append(round(current_price, 2))
        
        price_data[product] = {
            'dates': dates,
            'prices': prices
        }
    
    return price_data

def generate_price_predictions(crop_data):
    """Generate realistic price predictions for a crop"""
    
    base_price = crop_data['price_per_kg']
    
    # Factors affecting price prediction
    seasonal_factor = 1 + random.uniform(-0.2, 0.3)
    weather_factor = 1 + random.uniform(-0.15, 0.25)
    demand_factor = 1 + random.uniform(-0.1, 0.2)
    supply_factor = 1 + random.uniform(-0.2, 0.1)
    
    # Calculate predicted price range
    min_predicted = base_price * 0.8 * min(seasonal_factor, weather_factor, demand_factor, supply_factor)
    max_predicted = base_price * 1.2 * max(seasonal_factor, weather_factor, demand_factor, supply_factor)
    avg_predicted = (min_predicted + max_predicted) / 2
    
    return {
        'base_price': base_price,
        'min_predicted': min_predicted,
        'max_predicted': max_predicted,
        'avg_predicted': avg_predicted,
        'confidence': random.randint(75, 95),
        'factors': {
            'seasonal': seasonal_factor,
            'weather': weather_factor,
            'demand': demand_factor,
            'supply': supply_factor
        }
    }

