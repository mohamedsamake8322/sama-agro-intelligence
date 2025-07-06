import streamlit as st
import pandas as pd
from utils.auth import get_user_by_email, update_user_profile
from utils.database import get_user_products, get_transactions
from utils.translations import get_translation
from data.locations import AFRICAN_LOCATIONS

def profile_page():
    """User profile page with settings and transaction history"""

    st.title("👤 " + get_translation("user_profile", st.session_state.language))

    if not st.session_state.user:
        st.error("Please login to view your profile")
        return

    # Profile tabs
    profile_tab, transactions_tab, settings_tab = st.tabs([
        get_translation("profile_information", st.session_state.language),
        get_translation("transaction_history", st.session_state.language),
        "Settings"
    ])

    with profile_tab:
        display_profile_information()

    with transactions_tab:
        display_transaction_history()

    with settings_tab:
        display_user_settings()

def display_profile_information():
    """Affiche et modifie le profil utilisateur"""

    user = st.session_state.get("user", {})
    email = user.get("email", "")
    if not email:
        st.error("Aucun utilisateur connecté. Veuillez vous authentifier.")
        return

    # 📌 En-tête du profil
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(f"https://via.placeholder.com/150x150?text={user.get('name', '?')[0]}", width=150)
    with col2:
        st.subheader(user.get("name", "—"))
        st.write(f"📧 {email}")
        st.write(f"📱 {user.get('phone', 'Non renseigné')}")
        st.write(f"👤 {user.get('type', '—')}")
        st.write(f"📍 {user.get('location', 'Non précisé')}")

        stats_col1, stats_col2, stats_col3 = st.columns(3)
        with stats_col1:
            st.metric("Rating", f"{user.get('rating', 0):.1f}⭐")
        with stats_col2:
            st.metric("Total Transactions", user.get('total_transactions', 0))
        with stats_col3:
            verified = user.get('verified', False)
            st.write(f"**Status:** {'✅ Verified' if verified else '❌ Not Verified'}")

    st.divider()

    # ✏️ Formulaire de modification du profil
    st.subheader("✏️ Edit Profile")

    with st.form("edit_profile"):
        col1, col2 = st.columns(2)

        with col1:
            new_name = st.text_input("Full Name", value=user.get('name', ''))
            new_phone = st.text_input("Phone Number", value=user.get('phone', ''))
            location_value = user.get('location', '')
            location_index = AFRICAN_LOCATIONS.index(location_value) if location_value in AFRICAN_LOCATIONS else 0
            new_location = st.selectbox("Location", AFRICAN_LOCATIONS, index=location_index)

        with col2:
            bio = st.text_area(
                get_translation("bio", st.session_state.language),
                value=user.get('bio', ''),
                height=100
            )

            st.subheader(get_translation("notification_preferences", st.session_state.language))
            email_notifications = st.checkbox(
                get_translation("email_notifications", st.session_state.language),
                value=user.get('email_notifications', True),
                key="notif_email"
            )
            sms_notifications = st.checkbox(
                get_translation("sms_notifications", st.session_state.language),
                value=user.get('sms_notifications', True),
                key="notif_sms"
            )
            price_alerts = st.checkbox(
                get_translation("price_alerts", st.session_state.language),
                value=user.get('price_alerts', True),
                key="notif_price"
            )

        if st.form_submit_button(get_translation("update_profile", st.session_state.language)):
            updates = {
                "name": new_name,
                "phone": new_phone,
                "location": new_location,
                "bio": bio,
                "email_notifications": email_notifications,
                "sms_notifications": sms_notifications,
                "price_alerts": price_alerts
            }

            if update_user_profile(email, updates):
                st.session_state.user.update(updates)
                st.success(get_translation("profile_updated", st.session_state.language))
                st.rerun()
            else:
                st.error("Failed to update profile. Please try again.")

    # 🌾 Produits de l'utilisateur (si agriculteur)
    if user.get('type') in ['farmer', get_translation("farmer", st.session_state.language)]:
        st.divider()
        st.subheader("🌾 My Products")

        user_products = get_user_products(email)
        if user_products:
            for product in user_products:
                with st.container():
                    prod_col1, prod_col2, prod_col3, prod_col4 = st.columns([2, 1, 1, 1])
                    with prod_col1:
                        st.write(f"**{product.get('name', '—')}**")
                        st.write(product.get('description', '—'))
                    with prod_col2:
                        st.write(f"💰 ${product.get('price', 0):.2f}/kg")
                    with prod_col3:
                        st.write(f"📦 {product.get('quantity', 0)} kg")
                        availability = "🟢 Available" if product.get('available', True) else "🔴 Unavailable"
                        st.write(availability)
                    with prod_col4:
                        if st.button("Edit", key=f"edit_product_{product['id']}"):
                            st.session_state.editing_product = product['id']
                        if st.button("Delete", key=f"delete_product_{product['id']}"):
                            st.session_state.deleting_product = product['id']
                st.divider()
        else:
            st.info("You haven't listed any products yet.")


def display_transaction_history():
    """Display user transaction history"""

    user = st.session_state.user
    transactions = get_transactions(user['email'])

    if not transactions:
        st.info("No transactions found.")
        return

    # Transaction summary
    st.subheader("📊 Transaction Summary")

    total_transactions = len(transactions)
    completed_transactions = len([t for t in transactions if t.get('status') == 'completed'])
    total_amount = sum(t.get('total_amount', 0) for t in transactions if t.get('status') == 'completed')

    sum_col1, sum_col2, sum_col3 = st.columns(3)

    with sum_col1:
        st.metric("Total Transactions", total_transactions)
    with sum_col2:
        st.metric("Completed", completed_transactions)
    with sum_col3:
        st.metric("Total Value", f"${total_amount:.2f}")

    st.divider()

    # Transaction filters
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "completed", "pending", "cancelled"]
        )

    with filter_col2:
        sort_order = st.selectbox(
            "Sort by Date",
            ["Newest First", "Oldest First"]
        )

    # Filter transactions
    filtered_transactions = transactions
    if status_filter != "All":
        filtered_transactions = [t for t in transactions if t.get('status') == status_filter]

    # Sort transactions
    filtered_transactions.sort(
        key=lambda x: x.get('transaction_date', ''),
        reverse=(sort_order == "Newest First")
    )

    # Display transactions
    st.subheader("📋 Transaction Details")

    for transaction in filtered_transactions:
        with st.container():
            trans_col1, trans_col2, trans_col3, trans_col4 = st.columns([2, 1, 1, 1])

            with trans_col1:
                st.write(f"**{transaction['product_name']}**")
                if user.get('type') == 'buyer':
                    st.write(f"Seller: {transaction.get('seller_email', 'Unknown')}")
                else:
                    st.write(f"Buyer: {transaction.get('buyer_email', 'Unknown')}")

            with trans_col2:
                st.write(f"${transaction['total_amount']:.2f}")
                st.write(f"{transaction['quantity']} kg")

            with trans_col3:
                status_color = {
                    'completed': '🟢',
                    'pending': '🟡',
                    'cancelled': '🔴'
                }
                status = transaction.get('status', 'unknown')
                st.write(f"{status_color.get(status, '⚫')} {status.title()}")

            with trans_col4:
                transaction_date = transaction.get('transaction_date', '').split('T')[0]
                st.write(transaction_date)
                if transaction.get('delivery_date'):
                    delivery_date = transaction['delivery_date'].split('T')[0]
                    st.write(f"Delivery: {delivery_date}")

        st.divider()

def display_user_settings():
    """Display user settings and preferences"""

    st.subheader("⚙️ Account Settings")

    # Security settings
    with st.expander("🔒 Security Settings"):
        st.write("**Change Password**")

        with st.form("change_password"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")

            if st.form_submit_button("Change Password"):
                if new_password == confirm_password:
                    st.success("Password updated successfully!")
                else:
                    st.error("New passwords don't match!")

        st.divider()

        st.write("**Two-Factor Authentication**")
        two_fa_enabled = st.checkbox("Enable Two-Factor Authentication", value=False, key="security_2fa")
        if two_fa_enabled:
            st.info("Two-factor authentication will be enabled on your next login.")

    # Language and region settings
    with st.expander("🌍 Language & Region"):
        st.write("**Language Preference**")
        st.info(f"Current language: {st.session_state.language}")
        st.write("Change language using the sidebar selector.")

        st.write("**Currency Preference**")
        currency = st.selectbox("Display Currency", ["USD", "EUR", "GBP", "CFA", "KES", "NGN", "ZAR"])

        st.write("**Time Zone**")
        timezone = st.selectbox(
            "Time Zone",
            ["UTC", "CAT (Central Africa Time)", "WAT (West Africa Time)", "EAT (East Africa Time)"]
        )

    # Privacy settings
    with st.expander("🔐 Privacy Settings"):
        st.write("**Profile Visibility**")
        profile_public = st.checkbox("Make profile public", value=True, key="privacy_public")
        show_location = st.checkbox("Show location in profile", value=True, key="privacy_location")
        show_contact = st.checkbox("Allow other users to contact me", value=True, key="privacy_contact")

        st.write("**Data Sharing**")
        analytics_sharing = st.checkbox("Share anonymous usage data for platform improvement", value=True, key="privacy_analytics")
        marketing_emails = st.checkbox("Receive marketing emails", value=False, key="privacy_marketing")

    # Account management
    with st.expander("🗑️ Account Management"):
        st.write("**Export Data**")
        if st.button("Download My Data"):
            st.info("Your data export will be emailed to you within 24 hours.")

        st.write("**Delete Account**")
        st.warning("⚠️ Account deletion is permanent and cannot be undone.")
        if st.button("Delete My Account", type="secondary"):
            st.error("Account deletion requires email confirmation. Check your email for instructions.")

    # Save settings
    if st.button("Save Settings", type="primary"):
        st.success("Settings saved successfully!")

def user_verification():
    """Handle user verification process"""

    st.subheader("✅ Account Verification")

    if st.session_state.user.get('verified', False):
        st.success("Your account is verified!")
        return

    st.info("Verify your account to gain additional privileges and build trust with other users.")

    verification_steps = [
        "📧 Email verification",
        "📱 Phone number verification",
        "🆔 Identity document upload",
        "🏠 Address verification"
    ]

    for step in verification_steps:
        st.write(f"- {step}")

    if st.button("Start Verification Process"):
        st.success("Verification process initiated! Check your email for next steps.")

def display_user_stats():
    """Display detailed user statistics"""

    user = st.session_state.user

    st.subheader("📈 Your Statistics")

    # Create mock statistics based on user type
    if user.get('type') == 'farmer':
        stats_data = {
            'Products Listed': 12,
            'Total Sales': '$2,450',
            'Average Rating': '4.7⭐',
            'Response Rate': '94%',
            'Active Since': '2023'
        }
    else:
        stats_data = {
            'Orders Placed': 8,
            'Total Spent': '$1,890',
            'Favorite Categories': 'Vegetables, Fruits',
            'Average Order': '25kg',
            'Member Since': '2023'
        }

    stat_cols = st.columns(len(stats_data))

    for i, (label, value) in enumerate(stats_data.items()):
        with stat_cols[i]:
            st.metric(label, value)

