import os
import logging
from flask import Flask, render_template, request, jsonify
import math

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key_change_in_production")

class CalorieCalculator:
    """Main calculator class for BMR, calorie needs, and BMI calculations"""
    
    # Activity level multipliers based on Calculator.net
    ACTIVITY_MULTIPLIERS = {
        'bmr': 1.0,  # Basal Metabolic Rate
        'sedentary': 1.2,  # Sedentary: little or no exercise
        'light': 1.375,  # Light: exercise 1-3 times/week
        'moderate': 1.55,  # Moderate: exercise 4-5 times/week
        'active': 1.725,  # Active: daily exercise or intense exercise 3-4 times/week
        'very_active': 1.9,  # Very Active: intense exercise 6-7 times/week
        'extra_active': 2.2  # Extra Active: very intense exercise daily, or physical job
    }
    
    ACTIVITY_DESCRIPTIONS = {
        'bmr': 'Basal Metabolic Rate (BMR)',
        'sedentary': 'Sedentary: little or no exercise',
        'light': 'Light: exercise 1-3 times/week',
        'moderate': 'Moderate: exercise 4-5 times/week',
        'active': 'Active: daily exercise or intense exercise 3-4 times/week',
        'very_active': 'Very Active: intense exercise 6-7 times/week',
        'extra_active': 'Extra Active: very intense exercise daily, or physical job'
    }
    
    @staticmethod
    def mifflin_st_jeor(weight_kg, height_cm, age, gender):
        """
        Mifflin-St Jeor Equation (most accurate for general population)
        Men: BMR = 10W + 6.25H - 5A + 5
        Women: BMR = 10W + 6.25H - 5A - 161
        """
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age
        if gender.lower() == 'male':
            bmr += 5
        else:
            bmr -= 161
        return bmr
    
    @staticmethod
    def harris_benedict_revised(weight_kg, height_cm, age, gender):
        """
        Revised Harris-Benedict Equation
        Men: BMR = 13.397W + 4.799H - 5.677A + 88.362
        Women: BMR = 9.247W + 3.098H - 4.330A + 447.593
        """
        if gender.lower() == 'male':
            bmr = 13.397 * weight_kg + 4.799 * height_cm - 5.677 * age + 88.362
        else:
            bmr = 9.247 * weight_kg + 3.098 * height_cm - 4.330 * age + 447.593
        return bmr
    
    @staticmethod
    def katch_mcardle(weight_kg, body_fat_percent):
        """
        Katch-McArdle Formula (most accurate for lean individuals who know body fat %)
        BMR = 370 + 21.6(1 - F)W
        where F is body fat percentage as decimal
        """
        lean_body_mass = weight_kg * (1 - body_fat_percent / 100)
        bmr = 370 + 21.6 * lean_body_mass
        return bmr
    
    @staticmethod
    def calculate_bmi(weight_kg, height_cm):
        """Calculate BMI and return classification"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        # BMI classifications based on WHO standards
        if bmi < 16:
            classification = "Severe Thinness"
        elif bmi < 17:
            classification = "Moderate Thinness"
        elif bmi < 18.5:
            classification = "Mild Thinness"
        elif bmi < 25:
            classification = "Normal"
        elif bmi < 30:
            classification = "Overweight"
        elif bmi < 35:
            classification = "Obese Class I"
        elif bmi < 40:
            classification = "Obese Class II"
        else:
            classification = "Obese Class III"
        
        # Calculate healthy weight range
        height_m = height_cm / 100
        min_healthy_weight = 18.5 * (height_m ** 2)
        max_healthy_weight = 25 * (height_m ** 2)
        
        # BMI Prime
        bmi_prime = bmi / 25
        
        # Ponderal Index
        ponderal_index = weight_kg / (height_m ** 3)
        
        return {
            'bmi': round(bmi, 1),
            'classification': classification,
            'min_healthy_weight_kg': round(min_healthy_weight, 1),
            'max_healthy_weight_kg': round(max_healthy_weight, 1),
            'bmi_prime': round(bmi_prime, 2),
            'ponderal_index': round(ponderal_index, 1)
        }
    
    @staticmethod
    def convert_units(value, from_unit, to_unit):
        """Convert between different units"""
        # Weight conversions
        if from_unit == 'lbs' and to_unit == 'kg':
            return value * 0.453592
        elif from_unit == 'kg' and to_unit == 'lbs':
            return value / 0.453592
        
        # Height conversions
        elif from_unit == 'ft_in' and to_unit == 'cm':
            # Assuming value is in inches
            return value * 2.54
        elif from_unit == 'cm' and to_unit == 'in':
            return value / 2.54
        
        # Energy conversions
        elif from_unit == 'cal' and to_unit == 'kj':
            return value * 4.1868
        elif from_unit == 'kj' and to_unit == 'cal':
            return value / 4.1868
        elif from_unit == 'cal' and to_unit == 'j':
            return value * 4186.8
        elif from_unit == 'j' and to_unit == 'cal':
            return value / 4186.8
        elif from_unit == 'kj' and to_unit == 'j':
            return value * 1000
        elif from_unit == 'j' and to_unit == 'kj':
            return value / 1000
        
        return value

@app.route('/')
def index():
    """Main page with calorie and BMI calculators"""
    return render_template('index.html')

@app.route('/contact')
def contact():
    """Contact us page"""
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html')

@app.route('/disclaimer')
def disclaimer():
    """Disclaimer page"""
    return render_template('disclaimer.html')

@app.route('/terms')
def terms():
    """Terms and conditions page"""
    return render_template('terms.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculations for both calorie and BMI"""
    try:
        calc_type = request.form.get('calc_type', 'calorie')
        
        if calc_type == 'calorie':
            return calculate_calories()
        elif calc_type == 'bmi':
            return calculate_bmi()
        elif calc_type == 'energy':
            return convert_energy()
        else:
            return jsonify({'error': 'Invalid calculation type.'}), 400
        
    except Exception as e:
        logging.error(f"Calculation error: {str(e)}")
        return jsonify({'error': 'Calculation failed. Please check your inputs.'}), 400

def calculate_calories():
    """Calculate BMR and daily calorie needs"""
    # Get form data with proper validation
    age_str = request.form.get('age')
    gender = request.form.get('gender')
    unit_system = request.form.get('unit_system', 'us')
    activity_level = request.form.get('activity_level', 'sedentary')
    bmr_formula = request.form.get('bmr_formula', 'mifflin_st_jeor')
    results_unit = request.form.get('results_unit', 'calories')
    
    # Validate and convert age
    if not age_str:
        return jsonify({'error': 'Age is required.'}), 400
    
    try:
        age = int(age_str)
    except (ValueError, TypeError):
        return jsonify({'error': 'Age must be a valid number.'}), 400
        
    if age < 15 or age > 80:
        return jsonify({'error': 'Age must be between 15 and 80 years.'}), 400
    
    # Get height and weight based on unit system
    try:
        if unit_system == 'us':
            feet_str = request.form.get('feet', '0')
            inches_str = request.form.get('inches', '0')
            weight_lbs_str = request.form.get('weight_lbs')
            
            if not weight_lbs_str:
                return jsonify({'error': 'Weight is required.'}), 400
                
            feet = int(feet_str) if feet_str else 0
            inches = int(inches_str) if inches_str else 0
            weight_lbs = float(weight_lbs_str)
            
            # Convert to metric
            height_cm = CalorieCalculator.convert_units((feet * 12) + inches, 'ft_in', 'cm')
            weight_kg = CalorieCalculator.convert_units(weight_lbs, 'lbs', 'kg')
        else:
            height_cm_str = request.form.get('height_cm')
            weight_kg_str = request.form.get('weight_kg')
            
            if not height_cm_str or not weight_kg_str:
                return jsonify({'error': 'Height and weight are required.'}), 400
                
            height_cm = float(height_cm_str)
            weight_kg = float(weight_kg_str)
    except (ValueError, TypeError):
        return jsonify({'error': 'Please enter valid numbers for height and weight.'}), 400
    
    # Calculate BMR based on selected formula
    if bmr_formula == 'mifflin_st_jeor':
        bmr = CalorieCalculator.mifflin_st_jeor(weight_kg, height_cm, age, gender)
    elif bmr_formula == 'harris_benedict':
        bmr = CalorieCalculator.harris_benedict_revised(weight_kg, height_cm, age, gender)
    elif bmr_formula == 'katch_mcardle':
        body_fat = float(request.form.get('body_fat', 15))  # Default 15%
        bmr = CalorieCalculator.katch_mcardle(weight_kg, body_fat)
    else:
        bmr = CalorieCalculator.mifflin_st_jeor(weight_kg, height_cm, age, gender)
    
    # Calculate daily calorie needs
    activity_multiplier = CalorieCalculator.ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
    daily_calories = bmr * activity_multiplier
    
    # Weight management recommendations
    weight_loss_mild = daily_calories - 250  # 0.5 lb/week
    weight_loss_moderate = daily_calories - 500  # 1 lb/week
    weight_loss_extreme = daily_calories - 1000  # 2 lbs/week
    weight_gain_mild = daily_calories + 250  # 0.5 lb/week
    weight_gain_moderate = daily_calories + 500  # 1 lb/week
    
    # Convert to kilojoules if requested
    if results_unit == 'kilojoules':
        bmr = CalorieCalculator.convert_units(bmr, 'cal', 'kj')
        daily_calories = CalorieCalculator.convert_units(daily_calories, 'cal', 'kj')
        weight_loss_mild = CalorieCalculator.convert_units(weight_loss_mild, 'cal', 'kj')
        weight_loss_moderate = CalorieCalculator.convert_units(weight_loss_moderate, 'cal', 'kj')
        weight_loss_extreme = CalorieCalculator.convert_units(weight_loss_extreme, 'cal', 'kj')
        weight_gain_mild = CalorieCalculator.convert_units(weight_gain_mild, 'cal', 'kj')
        weight_gain_moderate = CalorieCalculator.convert_units(weight_gain_moderate, 'cal', 'kj')
    
    results = {
        'bmr': round(bmr),
        'daily_calories': round(daily_calories),
        'activity_description': CalorieCalculator.ACTIVITY_DESCRIPTIONS[activity_level],
        'weight_management': {
            'extreme_loss': round(weight_loss_extreme),
            'moderate_loss': round(weight_loss_moderate),
            'mild_loss': round(weight_loss_mild),
            'maintain': round(daily_calories),
            'mild_gain': round(weight_gain_mild),
            'moderate_gain': round(weight_gain_moderate)
        },
        'formula_used': bmr_formula.replace('_', ' ').title(),
        'results_unit': results_unit
    }
    
    return jsonify(results)

def calculate_bmi():
    """Calculate BMI and related metrics"""
    # Get form data with proper validation
    age_str = request.form.get('bmi_age')
    gender = request.form.get('bmi_gender')
    unit_system = request.form.get('bmi_unit_system', 'us')
    
    # Validate and convert age
    if not age_str:
        return jsonify({'error': 'Age is required.'}), 400
    
    try:
        age = int(age_str)
    except (ValueError, TypeError):
        return jsonify({'error': 'Age must be a valid number.'}), 400
        
    if age < 2 or age > 120:
        return jsonify({'error': 'Age must be between 2 and 120 years.'}), 400
    
    # Get height and weight based on unit system
    try:
        if unit_system == 'us':
            feet_str = request.form.get('bmi_feet', '0')
            inches_str = request.form.get('bmi_inches', '0')
            weight_lbs_str = request.form.get('bmi_weight_lbs')
            
            if not weight_lbs_str:
                return jsonify({'error': 'Weight is required.'}), 400
                
            feet = int(feet_str) if feet_str else 0
            inches = int(inches_str) if inches_str else 0
            weight_lbs = float(weight_lbs_str)
            
            # Convert to metric
            height_cm = CalorieCalculator.convert_units((feet * 12) + inches, 'ft_in', 'cm')
            weight_kg = CalorieCalculator.convert_units(weight_lbs, 'lbs', 'kg')
        else:
            height_cm_str = request.form.get('bmi_height_cm')
            weight_kg_str = request.form.get('bmi_weight_kg')
            
            if not height_cm_str or not weight_kg_str:
                return jsonify({'error': 'Height and weight are required.'}), 400
                
            height_cm = float(height_cm_str)
            weight_kg = float(weight_kg_str)
    except (ValueError, TypeError):
        return jsonify({'error': 'Please enter valid numbers for height and weight.'}), 400
    
    # Calculate BMI
    bmi_results = CalorieCalculator.calculate_bmi(weight_kg, height_cm)
    
    # Convert healthy weight range back to original units if needed
    if unit_system == 'us':
        bmi_results['min_healthy_weight_lbs'] = round(
            CalorieCalculator.convert_units(bmi_results['min_healthy_weight_kg'], 'kg', 'lbs'), 1
        )
        bmi_results['max_healthy_weight_lbs'] = round(
            CalorieCalculator.convert_units(bmi_results['max_healthy_weight_kg'], 'kg', 'lbs'), 1
        )
    
    bmi_results['unit_system'] = unit_system
    return jsonify(bmi_results)

def convert_energy():
    """Convert between energy units"""
    energy_value_str = request.form.get('energy_value', '0')
    from_unit = request.form.get('energy_from_unit')
    to_unit = request.form.get('energy_to_unit')
    
    # Validate inputs
    if not from_unit or not to_unit:
        return jsonify({'error': 'Both from and to units are required.'}), 400
    
    try:
        value = float(energy_value_str)
    except (ValueError, TypeError):
        return jsonify({'error': 'Energy value must be a valid number.'}), 400
    
    # Energy unit mapping
    unit_map = {
        'cal_nutritional': 'cal',
        'cal_small': 'cal',  # Note: 1 nutritional calorie = 1000 small calories
        'kilojoules': 'kj',
        'joules': 'j'
    }
    
    from_unit_mapped = unit_map.get(from_unit, from_unit)
    to_unit_mapped = unit_map.get(to_unit, to_unit)
    
    # Handle small calories conversion (1 kcal = 1000 cal)
    if from_unit == 'cal_small':
        value = value / 1000  # Convert to kcal first
        from_unit_mapped = 'cal'
    
    converted_value = CalorieCalculator.convert_units(value, from_unit_mapped, to_unit_mapped)
    
    # Handle small calories conversion back
    if to_unit == 'cal_small':
        converted_value = converted_value * 1000
    
    return jsonify({
        'original_value': float(request.form.get('energy_value', 0)),
        'converted_value': round(converted_value, 4),
        'from_unit': from_unit,
        'to_unit': to_unit
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
