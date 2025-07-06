import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import get_user_messages, add_message
from utils.translations import get_translation

def messages_page():
    """Messages page for communication between users"""
    
    st.title("💬 " + get_translation("messages", st.session_state.language))
    
    if not st.session_state.user:
        st.error("Please login to view messages")
        return
    
    # Messages layout
    msg_col1, msg_col2 = st.columns([1, 2])
    
    with msg_col1:
        display_ai_assistant()
    
    with msg_col2:
        display_conversations()

def display_ai_assistant():
    """AI chatbot assistant for farmers and buyers"""
    
    st.subheader("🤖 " + get_translation("ai_assistant", st.session_state.language))
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {
                'role': 'assistant',
                'content': f"Hello! I'm your AI assistant for Sama AgroLink. How can I help you today?",
                'timestamp': datetime.now()
            }
        ]
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.write(f"**You:** {message['content']}")
            else:
                st.write(f"**AI Assistant:** {message['content']}")
            st.caption(message['timestamp'].strftime("%H:%M"))
            st.write("")
    
    # Chat input
    user_input = st.text_input(
        get_translation("ask_question", st.session_state.language),
        placeholder=get_translation("chatbot_placeholder", st.session_state.language),
        key="ai_chat_input"
    )
    
    if st.button("Send", key="ai_send") and user_input:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Generate AI response
        ai_response = generate_ai_response(user_input)
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now()
        })
        
        st.rerun()
    
    # Quick action buttons
    st.subheader("Quick Help")
    quick_actions = [
        ("💰 Market Prices", "What are the current market prices?"),
        ("🌤️ Weather Info", "What's the weather forecast?"),
        ("🚚 Delivery", "How does delivery work?"),
        ("💳 Payments", "What payment methods are available?")
    ]
    
    for action_text, action_query in quick_actions:
        if st.button(action_text, key=f"quick_{action_text}"):
            # Add to chat history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': action_query,
                'timestamp': datetime.now()
            })
            
            ai_response = generate_ai_response(action_query)
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': ai_response,
                'timestamp': datetime.now()
            })
            
            st.rerun()

def generate_ai_response(user_input):
    """Generate AI response based on user input"""
    
    user_input_lower = user_input.lower()
    
    # Price-related queries
    if any(keyword in user_input_lower for keyword in ['price', 'cost', 'expensive', 'cheap', 'market']):
        return get_translation("price_info", st.session_state.language)
    
    # Weather-related queries
    elif any(keyword in user_input_lower for keyword in ['weather', 'rain', 'forecast', 'temperature', 'climate']):
        return get_translation("weather_info", st.session_state.language)
    
    # Delivery-related queries
    elif any(keyword in user_input_lower for keyword in ['delivery', 'shipping', 'transport', 'logistics']):
        return get_translation("delivery_info", st.session_state.language)
    
    # Payment-related queries
    elif any(keyword in user_input_lower for keyword in ['payment', 'pay', 'money', 'mobile money', 'bank']):
        return get_translation("payment_info", st.session_state.language)
    
    # Farming advice
    elif any(keyword in user_input_lower for keyword in ['plant', 'grow', 'harvest', 'crop', 'farm', 'agriculture']):
        return "For farming advice, consider factors like soil type, weather patterns, and market demand. Check our weather page for detailed forecasts and planting recommendations."
    
    # Quality and storage
    elif any(keyword in user_input_lower for keyword in ['quality', 'fresh', 'store', 'storage', 'preserve']):
        return "Maintain product quality by proper harvesting, cleaning, and storage. Use appropriate containers and ensure good ventilation. Our farmers are trained in post-harvest best practices."
    
    # Platform features
    elif any(keyword in user_input_lower for keyword in ['how to', 'help', 'use', 'feature']):
        return "Navigate using the sidebar menu. Farmers can list products, buyers can browse and purchase. Use the map to find local suppliers and check analytics for market trends."
    
    # Default response
    else:
        return get_translation("default_response", st.session_state.language)

def display_conversations():
    """Display user conversations and messaging interface"""
    
    st.subheader(get_translation("conversations", st.session_state.language))
    
    # Get user messages
    messages = get_user_messages(st.session_state.user['email'])
    
    if not messages:
        st.info(get_translation("no_messages", st.session_state.language))
        return
    
    # Group messages by conversation
    conversations = {}
    for message in messages:
        # Determine conversation partner
        if message['from'] == st.session_state.user['email']:
            partner = message['to']
        else:
            partner = message['from']
        
        if partner not in conversations:
            conversations[partner] = []
        conversations[partner].append(message)
    
    # Display conversations
    selected_conversation = st.selectbox(
        "Select Conversation",
        list(conversations.keys()),
        format_func=lambda x: x.split('@')[0].title()
    )
    
    if selected_conversation:
        display_conversation_thread(conversations[selected_conversation], selected_conversation)

def display_conversation_thread(messages, partner_email):
    """Display a conversation thread with a specific user"""
    
    # Sort messages by timestamp
    messages.sort(key=lambda x: x['timestamp'])
    
    # Display messages
    st.subheader(f"Conversation with {partner_email.split('@')[0].title()}")
    
    message_container = st.container()
    with message_container:
        for message in messages:
            is_from_user = message['from'] == st.session_state.user['email']
            
            if is_from_user:
                st.write("**You:**")
            else:
                st.write(f"**{message['from'].split('@')[0].title()}:**")
            
            # Message subject (if it's the first message)
            if message.get('subject'):
                st.write(f"*Subject: {message['subject']}*")
            
            st.write(message['content'])
            
            # Timestamp
            timestamp = datetime.fromisoformat(message['timestamp']).strftime("%Y-%m-%d %H:%M")
            st.caption(f"{get_translation('sent', st.session_state.language)}: {timestamp}")
            
            # Read status
            if not is_from_user and not message.get('read', True):
                st.success("🆕 New")
            
            st.divider()
    
    # Reply form
    st.subheader(get_translation("reply", st.session_state.language))
    
    with st.form(f"reply_form_{partner_email}"):
        reply_content = st.text_area(
            "Your Reply",
            placeholder="Type your reply here...",
            height=100
        )
        
        if st.form_submit_button(get_translation("send_reply", st.session_state.language)):
            if reply_content.strip():
                # Add message to database
                new_message = add_message(
                    st.session_state.user['email'],
                    partner_email,
                    "Re: Conversation",
                    reply_content
                )
                
                if new_message:
                    st.success(get_translation("reply_sent", st.session_state.language))
                    st.rerun()
                else:
                    st.error("Failed to send reply. Please try again.")
            else:
                st.error("Please enter a reply message.")

def new_message_form():
    """Form to compose a new message"""
    
    st.subheader("✉️ Compose New Message")
    
    with st.form("new_message_form"):
        recipient_email = st.text_input("Recipient Email")
        subject = st.text_input("Subject")
        content = st.text_area("Message Content", height=150)
        
        if st.form_submit_button("Send Message"):
            if recipient_email and subject and content:
                new_message = add_message(
                    st.session_state.user['email'],
                    recipient_email,
                    subject,
                    content
                )
                
                if new_message:
                    st.success("Message sent successfully!")
                    st.rerun()
                else:
                    st.error("Failed to send message. Please try again.")
            else:
                st.error("Please fill in all fields.")

def message_notifications():
    """Display message notifications and unread count"""
    
    messages = get_user_messages(st.session_state.user['email'])
    unread_messages = [m for m in messages if not m.get('read', True) and m['to'] == st.session_state.user['email']]
    
    if unread_messages:
        st.sidebar.success(f"📩 {len(unread_messages)} new messages")
        
        # Show recent unread messages in sidebar
        with st.sidebar.expander("Recent Messages"):
            for message in unread_messages[:3]:  # Show only 3 most recent
                st.write(f"**From:** {message['from'].split('@')[0]}")
                st.write(f"**Subject:** {message.get('subject', 'No subject')}")
                timestamp = datetime.fromisoformat(message['timestamp']).strftime("%m/%d %H:%M")
                st.caption(timestamp)
                st.divider()

def farmer_buyer_matching():
    """Suggest potential conversation partners based on location and products"""
    
    st.subheader("🤝 Suggested Connections")
    
    user_type = st.session_state.user.get('type', '')
    user_location = st.session_state.user.get('location', '')
    
    # Create mock suggestions based on user type and location
    if user_type == 'farmer':
        suggestions = [
            {
                'name': 'Local Buyers Cooperative',
                'type': 'Buyer',
                'location': user_location,
                'interests': 'Bulk vegetable purchases',
                'email': 'buyers.coop@example.com'
            },
            {
                'name': 'Fresh Market Distributors',
                'type': 'Buyer',
                'location': user_location,
                'interests': 'Fresh produce distribution',
                'email': 'freshmarket@example.com'
            }
        ]
    else:  # buyer
        suggestions = [
            {
                'name': 'Green Valley Farm',
                'type': 'Farmer',
                'location': user_location,
                'specialties': 'Organic vegetables, fruits',
                'email': 'greenvalley@example.com'
            },
            {
                'name': 'Sunshine Agriculture',
                'type': 'Farmer',
                'location': user_location,
                'specialties': 'Grains, legumes',
                'email': 'sunshine.ag@example.com'
            }
        ]
    
    for suggestion in suggestions:
        with st.container():
            sug_col1, sug_col2 = st.columns([3, 1])
            
            with sug_col1:
                st.write(f"**{suggestion['name']}**")
                st.write(f"📍 {suggestion['location']}")
                if 'interests' in suggestion:
                    st.write(f"🛒 Interests: {suggestion['interests']}")
                if 'specialties' in suggestion:
                    st.write(f"🌾 Specialties: {suggestion['specialties']}")
            
            with sug_col2:
                if st.button("Connect", key=f"connect_{suggestion['email']}"):
                    st.session_state.suggested_contact = suggestion
                    st.success(f"Connection request sent to {suggestion['name']}!")
            
            st.divider()

