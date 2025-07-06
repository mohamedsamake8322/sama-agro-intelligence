import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import os
from PIL import Image
import io
import base64

# Import utility modules
from utils.auth import authenticate_user, create_user
from utils.database import get_user_products, get_all_products, get_user_messages
from utils.recommendations import get_recommendations
from utils.translations import get_translation, LANGUAGES
from utils.weather import get_weather_info
from utils.payments import process_mobile_payment
from data.crops import AFRICAN_CROPS
from data.locations import AFRICAN_LOCATIONS
from modules.marketplace import marketplace_page
from modules.analytics import analytics_page
from modules.messages import messages_page
from modules.weather import weather_page
from modules.profile import profile_page

# Page configuration
st.set_page_config(
    page_title="Sama AgroLink - Agricultural Marketplace",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)
DEVELOPER_MODE = True

def initialize_session_state():
    """Initialize session state variables"""
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'offline_mode' not in st.session_state:
        st.session_state.offline_mode = False

def language_selector():
    """Language selection sidebar"""
    st.sidebar.title("🌍 " + get_translation("language", st.session_state.language))

    language_options = {
        'en': 'English',
        'fr': 'Français',
        'pt': 'Português',
        'sw': 'Kiswahili',
        'ha': 'Hausa'
    }

    selected_lang = st.sidebar.selectbox(
        get_translation("select_language", st.session_state.language),
        options=list(language_options.keys()),
        format_func=lambda x: language_options[x],
        index=list(language_options.keys()).index(st.session_state.language)
    )

    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

def user_authentication():
    """Handle user authentication"""
    if st.session_state.user is None:
        auth_tab1, auth_tab2 = st.tabs([
            get_translation("login", st.session_state.language),
            get_translation("register", st.session_state.language)
        ])

        with auth_tab1:
            with st.form("login_form"):
                email = st.text_input(get_translation("email", st.session_state.language))
                password = st.text_input(
                    get_translation("password", st.session_state.language),
                    type="password"
                )
                submit_login = st.form_submit_button(get_translation("login", st.session_state.language))

                if submit_login:
                    user = authenticate_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.success(get_translation("login_success", st.session_state.language))
                        st.rerun()
                    else:
                        st.error(get_translation("invalid_credentials", st.session_state.language))

        with auth_tab2:
            with st.form("register_form"):
                name = st.text_input(get_translation("full_name", st.session_state.language))
                email = st.text_input(get_translation("email", st.session_state.language))
                phone = st.text_input(get_translation("phone", st.session_state.language))
                password = st.text_input(
                    get_translation("password", st.session_state.language),
                    type="password"
                )
                user_type = st.selectbox(
                    get_translation("user_type", st.session_state.language),
                    [get_translation("farmer", st.session_state.language),
                     get_translation("buyer", st.session_state.language)]
                )
                location = st.selectbox(
                    get_translation("location", st.session_state.language),
                    AFRICAN_LOCATIONS
                )
                submit_register = st.form_submit_button(get_translation("register", st.session_state.language))

                if submit_register:
                    if name and email and phone and password:
                        user = create_user(name, email, phone, password, user_type, location)
                        if user:
                            st.session_state.user = user
                            st.success(get_translation("registration_success", st.session_state.language))
                            st.rerun()
                        else:
                            st.error(get_translation("registration_failed", st.session_state.language))
                    else:
                        st.error(get_translation("fill_all_fields", st.session_state.language))
def main_navigation():
    """Main navigation sidebar"""
    if not st.session_state.get("user"):
        return  # Ne pas afficher la navigation si l'utilisateur n'est pas connecté

    # ✅ Pour éviter la disparition soudaine de la sidebar à cause d'un rerun trop rapide
    if "navigation_initialized" not in st.session_state:
        st.session_state.navigation_initialized = True

    st.sidebar.title(
        f"👋 {get_translation('welcome', st.session_state.language)} {st.session_state.user['name']}"
    )

    # ✅ Key unique par utilisateur pour éviter les duplications
    checkbox_key = f"offline_mode_checkbox_{st.session_state.user['email']}"
    st.session_state.offline_mode = st.sidebar.checkbox(
        label="📱 " + get_translation("offline_mode", st.session_state.language),
        value=st.session_state.offline_mode,
        key=checkbox_key
    )

    # 📍 Définition des pages
    pages = {
        'home': '🏠 ' + get_translation("home", st.session_state.language),
        'marketplace': '🛒 ' + get_translation("marketplace", st.session_state.language),
        'my_products': '📦 ' + get_translation("my_products", st.session_state.language),
        'messages': '💬 ' + get_translation("messages", st.session_state.language),
        'analytics': '📊 ' + get_translation("analytics", st.session_state.language),
        'weather': '🌤️ ' + get_translation("weather", st.session_state.language),
        'profile': '👤 ' + get_translation("profile", st.session_state.language)
    }

    selected_page = st.sidebar.radio(
            get_translation("navigation", st.session_state.language),
            options=list(pages.keys()),
            format_func=lambda x: pages[x],
            index=list(pages.keys()).index(st.session_state.current_page)
        )

    if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()

    if st.sidebar.button(get_translation("logout", st.session_state.language)):
            st.session_state.user = None
            st.session_state.current_page = 'home'
            st.rerun()

def home_page():
    """Home page with map and overview"""
    st.title("🌾 Sama AgroLink")
    st.subheader(get_translation("welcome_message", st.session_state.language))

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(get_translation("active_farmers", st.session_state.language), "2,543")
    with col2:
        st.metric(get_translation("products_available", st.session_state.language), "15,672")
    with col3:
        st.metric(get_translation("transactions_today", st.session_state.language), "127")
    with col4:
        st.metric(get_translation("average_rating", st.session_state.language), "4.7⭐")

    # Interactive map
    st.subheader(get_translation("marketplace_map", st.session_state.language))

    # Create map centered on Africa
    m = folium.Map(location=[0, 20], zoom_start=3)

    # Add sample farmer and buyer locations
    for location in AFRICAN_LOCATIONS[:20]:  # Show first 20 locations
        lat, lon = get_location_coordinates(location)
        if lat and lon:
            folium.Marker(
                [lat, lon],
                popup=f"{location} - {get_translation('farmers_and_buyers', st.session_state.language)}",
                icon=folium.Icon(color='green', icon='leaf')
            ).add_to(m)

    # Display map
    map_data = st_folium(m, width=700, height=500)

    # Featured products
    st.subheader(get_translation("featured_products", st.session_state.language))

    # Display sample products
    products_col1, products_col2, products_col3 = st.columns(3)

    featured_crops = AFRICAN_CROPS[:3]
    for i, crop in enumerate(featured_crops):
        with [products_col1, products_col2, products_col3][i]:
            st.image(f"https://via.placeholder.com/200x150?text={crop['name']}", use_column_width=True)
            st.write(f"**{crop['name']}**")
            st.write(f"💰 ${crop['price_per_kg']:.2f}/kg")
            st.write(f"📍 {crop['region']}")
            if st.button(f"{get_translation('view_details', st.session_state.language)}", key=f"featured_{i}"):
                st.session_state.current_page = 'marketplace'
                st.rerun()

def my_products_page():
    """User's products page"""
    st.title("📦 " + get_translation("my_products", st.session_state.language))

    if st.session_state.user['type'] == get_translation("farmer", st.session_state.language) or st.session_state.user.get('type') == 'farmer':
        # Add new product
        st.subheader(get_translation("add_new_product", st.session_state.language))

        with st.form("add_product"):
            product_name = st.text_input(get_translation("product_name", st.session_state.language))
            category = st.selectbox(
                get_translation("category", st.session_state.language),
                ["Grains", "Vegetables", "Fruits", "Legumes", "Tubers"]
            )
            price = st.number_input(
                get_translation("price_per_kg", st.session_state.language),
                min_value=0.1, value=1.0, step=0.1
            )
            quantity = st.number_input(
                get_translation("quantity_available", st.session_state.language),
                min_value=1, value=100
            )
            description = st.text_area(get_translation("description", st.session_state.language))

            if st.form_submit_button(get_translation("add_product", st.session_state.language)):
                if product_name and price and quantity:
                    st.success(get_translation("product_added", st.session_state.language))
                else:
                    st.error(get_translation("fill_all_fields", st.session_state.language))

        # User's products
        st.subheader(get_translation("your_products", st.session_state.language))
        user_products = get_user_products(st.session_state.user['email'])

        if not user_products:
            st.info(get_translation("no_products", st.session_state.language))
        else:
            for product in user_products:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"**{product['name']}**")
                    st.write(product['description'])
                with col2:
                    st.write(f"💰 ${product['price']:.2f}/kg")
                with col3:
                    st.write(f"📦 {product['quantity']} kg")
                with col4:
                    if st.button(get_translation("edit", st.session_state.language), key=f"edit_{product['id']}"):
                        pass
                st.divider()
    else:
        # Buyer's orders and cart
        st.subheader(get_translation("shopping_cart", st.session_state.language))

        if not st.session_state.cart:
            st.info(get_translation("cart_empty", st.session_state.language))
        else:
            total_amount = 0
            for i, item in enumerate(st.session_state.cart):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"**{item['product']['name']}**")
                with col2:
                    st.write(f"${item['product']['price_per_kg']:.2f}/kg")
                with col3:
                    st.write(f"{item['quantity']} kg")
                with col4:
                    st.write(f"${item['total']:.2f}")
                    if st.button("🗑️", key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
                total_amount += item['total']

            st.write(f"**{get_translation('total', st.session_state.language)}: ${total_amount:.2f}**")

            if st.button(get_translation("proceed_to_payment", st.session_state.language)):
                st.session_state.current_page = 'payment'
                st.rerun()

def payment_page():
    """Payment processing page"""
    st.title("💳 " + get_translation("payment", st.session_state.language))

    if not st.session_state.cart:
        st.warning(get_translation("cart_empty", st.session_state.language))
        return

    # Order summary
    st.subheader(get_translation("order_summary", st.session_state.language))

    total_amount = 0
    for item in st.session_state.cart:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(item['product']['name'])
        with col2:
            st.write(f"{item['quantity']} kg")
        with col3:
            st.write(f"${item['total']:.2f}")
        total_amount += item['total']

    st.write(f"**{get_translation('total', st.session_state.language)}: ${total_amount:.2f}**")

    # Payment method
    st.subheader(get_translation("payment_method", st.session_state.language))

    payment_method = st.selectbox(
        get_translation("select_payment_method", st.session_state.language),
        ["M-Pesa", "Orange Money", "MTN Mobile Money", "Airtel Money", "Bank Transfer"]
    )

    if payment_method in ["M-Pesa", "Orange Money", "MTN Mobile Money", "Airtel Money"]:
        phone_number = st.text_input(get_translation("mobile_number", st.session_state.language))

        if st.button(get_translation("process_payment", st.session_state.language)):
            if phone_number:
                result = process_mobile_payment(payment_method, phone_number, total_amount)
                if result['success']:
                    st.success(get_translation("payment_success", st.session_state.language))
                    st.balloons()
                    st.session_state.cart = []
                    st.rerun()
                else:
                    st.error(get_translation("payment_failed", st.session_state.language))
            else:
                st.error(get_translation("enter_phone_number", st.session_state.language))

def get_location_coordinates(location):
    """Get coordinates for a location (mock implementation)"""
    coordinates = {
        'Lagos, Nigeria': (-6.5244, 3.3792),
        'Nairobi, Kenya': (-1.2921, 36.8219),
        'Cairo, Egypt': (30.0444, 31.2357),
        'Cape Town, South Africa': (-33.9249, 18.4241),
        'Casablanca, Morocco': (33.5731, -7.5898),
        'Addis Ababa, Ethiopia': (9.0325, 38.7469),
        'Accra, Ghana': (5.6037, -0.1870),
        'Tunis, Tunisia': (36.8065, 10.1815),
        'Khartoum, Sudan': (15.5007, 32.5599),
        'Kampala, Uganda': (0.3476, 32.5825)
    }
    return coordinates.get(location, (0, 0))

def main():
    initialize_session_state()
    language_selector()

    if DEVELOPER_MODE or st.session_state.user:
        # Simule un utilisateur en mode développeur
        if DEVELOPER_MODE and not st.session_state.user:
            st.session_state.user = {
                "name": "Développeur",
                "email": "dev@example.com",
                "type": "farmer"
            }

        # ✅ Empêche double affichage
        if not st.session_state.get("main_navigation_rendered"):
            st.session_state["main_navigation_rendered"] = True
            main_navigation()

        # Affiche la bonne page
        current_page = st.session_state.current_page
        if current_page == 'home':
            home_page()
        elif current_page == 'marketplace':
            marketplace_page()
        elif current_page == 'my_products':
            my_products_page()
        elif current_page == 'messages':
            messages_page()
        elif current_page == 'analytics':
            analytics_page()
        elif current_page == 'weather':
            weather_page()
        elif current_page == 'profile':
            profile_page()
        elif current_page == 'payment':
            payment_page()

    else:
        # 🔐 Si l'utilisateur n'est pas connecté
        st.title("🌾 Sama AgroLink")
        st.subheader(get_translation("welcome_message", st.session_state.language))
        user_authentication()

if __name__ == "__main__":
    main()
