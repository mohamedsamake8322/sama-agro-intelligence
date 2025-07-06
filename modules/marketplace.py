import streamlit as st
import pandas as pd
from utils.database import get_all_products, add_product
from utils.recommendations import get_product_recommendations
from utils.translations import get_translation
from data.crops import AFRICAN_CROPS, CROP_CATEGORIES, search_crops

def marketplace_page():
    """Marketplace page for browsing and purchasing products"""

    st.title("🛒 " + get_translation("marketplace", st.session_state.language))

    # Search and filter section
    col1, col2 = st.columns([2, 1])

    with col1:
        search_query = st.text_input(
            get_translation("search_products", st.session_state.language),
            placeholder=get_translation("search_placeholder", st.session_state.language)
        )

    with col2:
        category_filter = st.selectbox(
            get_translation("category", st.session_state.language),
            ["All"] + list(CROP_CATEGORIES.keys())
        )

    # Advanced filters in expandable section
    with st.expander("🔍 Advanced Filters"):
        filter_col1, filter_col2, filter_col3 = st.columns(3)

        with filter_col1:
            min_price, max_price = st.slider(
                get_translation("price_range", st.session_state.language),
                min_value=0.0,
                max_value=20.0,
                value=(0.0, 20.0),
                step=0.5
            )

        with filter_col2:
            sort_option = st.selectbox(
                get_translation("sort_by", st.session_state.language),
                [
                    get_translation("rating", st.session_state.language),
                    get_translation("price_low_high", st.session_state.language),
                    get_translation("price_high_low", st.session_state.language),
                    "Distance"
                ]
            )

        with filter_col3:
            organic_only = st.checkbox("🌱 Organic Only", key="filter_organic_only")
            fresh_only = st.checkbox("🆕 Fresh Harvest", key="filter_fresh_only")


    # Get products
    products = get_all_products()

    # Apply filters
    filtered_products = []
    for product in products:
        # Search filter
        if search_query:
            if not (search_query.lower() in product['name'].lower() or
                   search_query.lower() in product['description'].lower()):
                continue

        # Category filter
        if category_filter != "All" and product['category'] != category_filter:
            continue

        # Price filter
        if not (min_price <= product['price'] <= max_price):
            continue

        # Organic filter
        if organic_only and not product.get('organic', False):
            continue

        filtered_products.append(product)

    # Sort products
    if sort_option == get_translation("price_low_high", st.session_state.language):
        filtered_products.sort(key=lambda x: x['price'])
    elif sort_option == get_translation("price_high_low", st.session_state.language):
        filtered_products.sort(key=lambda x: x['price'], reverse=True)
    elif sort_option == get_translation("rating", st.session_state.language):
        filtered_products.sort(key=lambda x: x['rating'], reverse=True)

    # Display results count
    st.write(f"**{len(filtered_products)} {get_translation('products_found', st.session_state.language)}**")

    # Display products in grid
    if filtered_products:
        # Create product grid
        cols_per_row = 3
        for i in range(0, len(filtered_products), cols_per_row):
            cols = st.columns(cols_per_row)

            for j, product in enumerate(filtered_products[i:i+cols_per_row]):
                with cols[j]:
                    display_product_card(product)
    else:
        st.info("No products found matching your criteria. Try adjusting your filters.")

    # Recommendations section
    if st.session_state.user:
        st.subheader("🎯 " + get_translation("ai_recommendations", st.session_state.language))
        recommendations = get_product_recommendations(st.session_state.user)

        if recommendations:
            rec_cols = st.columns(min(3, len(recommendations)))
            for i, rec_product in enumerate(recommendations):
                with rec_cols[i % 3]:
                    display_recommendation_card(rec_product)

def display_product_card(product):
    """Display a product card with details and actions"""

    # Product image placeholder
    st.image(product.get('image_url', f"https://via.placeholder.com/250x200?text={product['name']}"))

    # Product title and rating
    st.write(f"**{product['name']}**")
    rating_stars = "⭐" * int(product.get('rating', 0))
    st.write(f"{rating_stars} {product.get('rating', 0)} ({product.get('reviews_count', 0)} {get_translation('reviews', st.session_state.language)})")

    # Price and quantity
    st.write(f"💰 **${product['price']:.2f}/kg**")
    st.write(f"📦 {product['quantity']} kg available")

    # Location and seller
    st.write(f"📍 {product['location']}")
    st.write(f"👨‍🌾 {product['seller_name']}")

    # Organic badge
    if product.get('organic', False):
        st.success("🌱 Organic")

    # Add to cart section
    if st.session_state.user and st.session_state.user.get('type') != 'farmer':
        quantity = st.number_input(
            get_translation("quantity", st.session_state.language),
            min_value=1,
            max_value=min(100, product['quantity']),
            value=1,
            key=f"qty_{product['id']}"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button(get_translation("add_to_cart", st.session_state.language), key=f"cart_{product['id']}"):
                add_to_cart(product, quantity)

        with col2:
            if st.button(get_translation("contact_farmer", st.session_state.language), key=f"contact_{product['id']}"):
                contact_farmer(product)

    st.divider()

def display_recommendation_card(crop_data):
    """Display a recommendation card for crops from the database"""

    # Create a product-like structure from crop data
    st.image(f"https://via.placeholder.com/200x150?text={crop_data['name']}")
    st.write(f"**{crop_data['name']}**")
    st.write(f"💰 ${crop_data['price_per_kg']:.2f}/kg")
    st.write(f"📍 {crop_data['region']}")
    st.write(f"🌾 {crop_data['category']}")

    if st.button(f"{get_translation('view_details', st.session_state.language)}", key=f"rec_{crop_data['name']}"):
        st.session_state.selected_crop = crop_data['name']
        st.rerun()

def add_to_cart(product, quantity):
    """Add product to shopping cart"""

    cart_item = {
        'product': product,
        'quantity': quantity,
        'total': product['price'] * quantity
    }

    # Check if product already in cart
    existing_item = None
    for i, item in enumerate(st.session_state.cart):
        if item['product']['id'] == product['id']:
            existing_item = i
            break

    if existing_item is not None:
        # Update quantity
        st.session_state.cart[existing_item]['quantity'] += quantity
        st.session_state.cart[existing_item]['total'] = (
            st.session_state.cart[existing_item]['product']['price'] *
            st.session_state.cart[existing_item]['quantity']
        )
    else:
        # Add new item
        st.session_state.cart.append(cart_item)

    st.success(get_translation("added_to_cart", st.session_state.language))
    st.rerun()

def contact_farmer(product):
    """Open contact form for farmer"""

    st.session_state.contact_farmer_product = product
    st.success(f"Contact request sent to {product['seller_name']}!")

    # In a real implementation, this would create a message or notification

def product_detail_view(product):
    """Display detailed product information"""

    st.subheader(f"📦 {product['name']}")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(product.get('image_url', f"https://via.placeholder.com/400x300?text={product['name']}"))

    with col2:
        st.write(f"**Price:** ${product['price']:.2f}/kg")
        st.write(f"**Available Quantity:** {product['quantity']} kg")
        st.write(f"**Category:** {product['category']}")
        st.write(f"**Location:** {product['location']}")
        st.write(f"**Seller:** {product['seller_name']}")

        rating_stars = "⭐" * int(product.get('rating', 0))
        st.write(f"**Rating:** {rating_stars} {product.get('rating', 0)}/5")
        st.write(f"**Reviews:** {product.get('reviews_count', 0)}")

        if product.get('organic', False):
            st.success("🌱 Certified Organic")

        if product.get('harvest_date'):
            st.write(f"**Harvest Date:** {product['harvest_date'][:10]}")

        if product.get('expiry_date'):
            st.write(f"**Best Before:** {product['expiry_date'][:10]}")

    st.write("**Description:**")
    st.write(product['description'])

    # Nutritional information if available
    if 'nutrition' in product:
        st.subheader("📊 Nutritional Information (per 100g)")
        nutr_col1, nutr_col2, nutr_col3 = st.columns(3)

        with nutr_col1:
            st.metric("Calories", f"{product['nutrition'].get('calories', 'N/A')}")
        with nutr_col2:
            st.metric("Protein (g)", f"{product['nutrition'].get('protein', 'N/A')}")
        with nutr_col3:
            st.metric("Carbs (g)", f"{product['nutrition'].get('carbs', 'N/A')}")

def bulk_order_form():
    """Form for bulk orders"""

    st.subheader("📦 Bulk Order Request")

    with st.form("bulk_order"):
        crop_type = st.selectbox("Crop Type", list(CROP_CATEGORIES.keys()))
        quantity_needed = st.number_input("Quantity Needed (kg)", min_value=100, value=500, step=50)
        target_price = st.number_input("Target Price (USD/kg)", min_value=0.1, value=2.0, step=0.1)
        delivery_location = st.text_input("Delivery Location")
        delivery_date = st.date_input("Required Delivery Date")
        additional_requirements = st.text_area("Additional Requirements")

        if st.form_submit_button("Submit Bulk Order Request"):
            st.success("Bulk order request submitted! Farmers in your area will be notified.")
            # In real implementation, this would create notifications for relevant farmers

