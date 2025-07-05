# Sama AgroLink - Agricultural Marketplace

## Overview

Sama AgroLink is a comprehensive agricultural marketplace platform built with Streamlit, designed to connect African farmers with buyers across the continent. The application provides a multi-language, offline-capable platform that includes real-time weather information, AI-powered recommendations, mobile payment integration, and comprehensive market analytics.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit (Python-based web framework)
- **UI Components**: Streamlit's native components with custom styling
- **Maps Integration**: Folium for interactive mapping with streamlit-folium bridge
- **Charts & Visualization**: Plotly for interactive charts and data visualization
- **State Management**: Streamlit's session state for user authentication and application state

### Backend Architecture
- **Application Server**: Streamlit server running on port 5000
- **Data Storage**: JSON file-based storage system (ready for database migration)
- **Authentication**: Custom hash-based authentication using SHA256
- **API Integration**: External weather API support with fallback to mock data
- **Multi-language Support**: Translation system supporting English, French, Portuguese, Swahili, and Hausa

### Core Modules
- **Authentication (`utils/auth.py`)**: User registration, login, and password hashing
- **Database (`utils/database.py`)**: JSON-based data persistence for users, products, and transactions
- **Recommendations (`utils/recommendations.py`)**: AI-powered recommendation engine
- **Weather (`utils/weather.py`)**: Weather information with OpenWeatherMap API integration
- **Payments (`utils/payments.py`)**: Mobile payment processing simulation
- **Translations (`utils/translations.py`)**: Multi-language content management

## Key Components

### Page Structure
- **Main App (`app.py`)**: Entry point with navigation and authentication
- **Marketplace (`pages/marketplace.py`)**: Product browsing, search, and purchasing
- **Analytics (`pages/analytics.py`)**: Market insights and trend analysis
- **Weather (`pages/weather.py`)**: Weather forecasts and agricultural advice
- **Messages (`pages/messages.py`)**: Communication system with AI assistant
- **Profile (`pages/profile.py`)**: User management and transaction history

### Data Models
- **Crops Database (`data/crops.py`)**: Comprehensive African crops with pricing and nutritional data
- **Locations Database (`data/locations.py`)**: African cities and regions for geographic functionality
- **User Data**: Email, password hash, phone, location, user type (farmer/buyer)
- **Product Data**: Name, category, price, quantity, seller information, location
- **Transaction Data**: Payment method, amount, status, timestamp

## Data Flow

1. **User Authentication**: Users register/login through hash-based authentication
2. **Product Discovery**: Search and filter products by category, price, location
3. **Weather Integration**: Real-time weather data influences agricultural recommendations
4. **AI Recommendations**: Personalized suggestions based on user type, location, and market trends
5. **Payment Processing**: Mobile money integration for transaction completion
6. **Communication**: AI assistant and peer-to-peer messaging system

## External Dependencies

### Production Dependencies
- **streamlit**: Web framework and UI components
- **streamlit-folium**: Interactive map integration
- **folium**: Mapping library for location-based features
- **plotly**: Interactive charts and data visualization
- **pandas**: Data manipulation and analysis
- **requests**: HTTP client for API calls
- **pillow**: Image processing capabilities

### External Services
- **OpenWeatherMap API**: Real-time weather data (optional, falls back to mock data)
- **Mobile Money APIs**: Payment processing integration (simulated)

### System Dependencies
- **Python 3.11+**: Runtime environment
- **Nix packages**: freetype, glibcLocales, lcms2, libimagequant, libjpeg, libtiff, libwebp, libxcrypt, openjpeg, tcl, tk, zlib

## Deployment Strategy

### Replit Configuration
- **Deployment Target**: Autoscale deployment on Replit
- **Run Command**: `streamlit run app.py --server.port 5000`
- **Port Configuration**: Server listens on port 5000
- **Workflow**: Parallel execution with Streamlit server task

### Scaling Considerations
- JSON file storage is suitable for prototyping but should migrate to a proper database (PostgreSQL recommended)
- Session state management works for single-instance deployment
- External API calls have fallback mechanisms for offline functionality
- Static assets and images are served through the application

### Production Readiness
- Environment variables for API keys (weather, payment services)
- HTTPS configuration for secure transactions
- Database migration path prepared
- Offline mode capability for areas with limited connectivity

## Changelog

- June 23, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.