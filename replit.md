# Overview

This is a comprehensive Flask-based web application that replicates Calculator.net's health and fitness calculators, specifically focusing on calorie calculations, BMI calculations, and energy conversions. The application implements multiple BMR calculation formulas (Mifflin-St Jeor, Harris-Benedict, Katch-McArdle) and provides detailed calorie needs estimation based on different activity levels. The system supports both US and metric unit systems with seamless switching, offers weight management recommendations, and includes a robust BMI calculator with classification and healthy weight ranges.

## Recent Updates (August 2025)
- ✓ Implemented exact Calculator.net calorie calculator functionality
- ✓ Added comprehensive BMI calculator with WHO classifications
- ✓ Built responsive UI with Bootstrap 5.3.0 and Font Awesome icons
- ✓ Added real-time energy unit converter
- ✓ Implemented proper form validation and error handling
- ✓ Fixed all type safety issues for production deployment

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates for server-side rendering
- **UI Framework**: Bootstrap 5.3.0 for responsive design and component styling
- **Icons**: Font Awesome 6.0.0 for iconography
- **JavaScript**: Vanilla JavaScript for client-side interactions and real-time calculations
- **Styling**: Custom CSS with CSS variables for consistent theming and color management

## Backend Architecture
- **Web Framework**: Flask application with minimal configuration
- **Calculator Logic**: Object-oriented design with `CalorieCalculator` class containing static methods
- **Activity Multipliers**: Predefined constants based on Calculator.net standards for different exercise levels
- **BMR Calculation**: Implements Mifflin-St Jeor equation for accurate metabolic rate estimation
- **Unit Support**: Dual support for US and metric measurement systems

## Application Structure
- **Main Entry Point**: `main.py` serves as the application launcher
- **Core Logic**: `app.py` contains Flask routes and calculator implementation
- **Static Assets**: Organized into CSS and JavaScript directories for maintainability
- **Templates**: HTML templates with Bootstrap integration for responsive design

## Data Processing
- **Input Validation**: Client-side and server-side validation for user inputs
- **Real-time Calculations**: JavaScript-powered instant feedback for energy conversions
- **Form Handling**: AJAX-based form submissions for seamless user experience
- **Tab Management**: Dynamic content switching between US and metric units

# External Dependencies

## Frontend Libraries
- **Bootstrap 5.3.0**: Responsive CSS framework via CDN
- **Font Awesome 6.0.0**: Icon library via CDN

## Python Dependencies
- **Flask**: Web framework for application structure and routing
- **Python Standard Library**: Math module for calculations, os for environment variables, logging for debugging

## Development Environment
- **Session Management**: Flask sessions with configurable secret key
- **Environment Configuration**: Support for production environment variables
- **Debug Mode**: Development-friendly error handling and auto-reload