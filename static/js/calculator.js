// Calorie Calculator JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the calculator
    initializeCalculator();
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize energy converter
    initializeEnergyConverter();
});

function initializeCalculator() {
    // Set default values and sync across tabs
    syncFormValues();
    
    // Show/hide body fat input based on BMR formula selection
    toggleBodyFatInput();
}

function setupEventListeners() {
    // Calorie calculator form submission
    const calorieForm = document.getElementById('calorieForm');
    if (calorieForm) {
        calorieForm.addEventListener('submit', handleCalorieCalculation);
    }
    
    // BMI calculator form submission
    const bmiForm = document.getElementById('bmiForm');
    if (bmiForm) {
        bmiForm.addEventListener('submit', handleBMICalculation);
    }
    
    // Energy converter real-time updates
    const energyForm = document.getElementById('energyForm');
    if (energyForm) {
        const inputs = energyForm.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('input', handleEnergyConversion);
            input.addEventListener('change', handleEnergyConversion);
        });
    }
    
    // BMR formula selection
    const bmrFormulaSelects = document.querySelectorAll('select[name="bmr_formula"]');
    bmrFormulaSelects.forEach(select => {
        select.addEventListener('change', toggleBodyFatInput);
    });
    
    // Tab synchronization
    const unitTabs = document.querySelectorAll('#unitTabs button, #bmiUnitTabs button');
    unitTabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', syncFormValues);
    });
    
    // Form input synchronization between tabs
    setupFormSync();
}

function setupFormSync() {
    // Sync age between calorie calculator tabs
    const ageInputs = document.querySelectorAll('input[name="age"]');
    ageInputs.forEach(input => {
        input.addEventListener('input', function() {
            ageInputs.forEach(other => {
                if (other !== input) {
                    other.value = input.value;
                }
            });
        });
    });
    
    // Sync gender between calorie calculator tabs
    const genderInputs = document.querySelectorAll('input[name="gender"]');
    genderInputs.forEach(input => {
        input.addEventListener('change', function () {
            if (input.checked) {
                genderInputs.forEach(other => {
                    other.checked = (other.value === input.value);
                });
            }
        });
    });
    
    // Sync BMI age between tabs
    const bmiAgeInputs = document.querySelectorAll('input[name="bmi_age"]');
    bmiAgeInputs.forEach(input => {
        input.addEventListener('input', function() {
            bmiAgeInputs.forEach(other => {
                if (other !== input) {
                    other.value = input.value;
                }
            });
        });
    });
    
    // Sync BMI gender between tabs
    const bmiGenderInputs = document.querySelectorAll('input[name="bmi_gender"]');
    bmiGenderInputs.forEach(input => {
        input.addEventListener('change', function () {
            if (input.checked) {
                bmiGenderInputs.forEach(other => {
                    other.checked = (other.value === input.value);
                });
            }
        });
    });
}

function syncFormValues() {
    // This function can be used to sync values between different unit systems
    // Currently, the form handles this through HTML structure
    console.log('Form values synced');
}

function toggleBodyFatInput() {
    const formulaSelects = document.querySelectorAll('select[name="bmr_formula"]');
    const bodyFatGroups = document.querySelectorAll('#bodyFatGroup');
    
    formulaSelects.forEach(select => {
        const isKatchMcArdle = select.value === 'katch_mcardle';
        bodyFatGroups.forEach(group => {
            group.style.display = isKatchMcArdle ? 'block' : 'none';
        });
    });
}

function handleCalorieCalculation(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculating...';
    submitBtn.disabled = true;
    
    // Clear previous errors
    clearErrors();
    
    fetch('/calculate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
        } else {
            displayCalorieResults(data);
        }
    })
    .catch(error => {
        showError('An error occurred while calculating. Please try again.');
        console.error('Error:', error);
    })
    .finally(() => {
        // Restore button state
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

function handleBMICalculation(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculating...';
    submitBtn.disabled = true;
    
    // Clear previous errors
    clearErrors();
    
    fetch('/calculate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
        } else {
            displayBMIResults(data);
        }
    })
    .catch(error => {
        showError('An error occurred while calculating BMI. Please try again.');
        console.error('Error:', error);
    })
    .finally(() => {
        // Restore button state
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

function initializeEnergyConverter() {
    // Set initial conversion
    handleEnergyConversion();
}

function handleEnergyConversion() {
    const form = document.getElementById('energyForm');
    const formData = new FormData(form);
    
    fetch('/calculate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (!data.error) {
            document.getElementById('convertedValue').textContent = data.converted_value;
        }
    })
    .catch(error => {
        console.error('Energy conversion error:', error);
    });
}

function displayCalorieResults(data) {
    // Update results values
    document.getElementById('dailyCalories').textContent = data.daily_calories.toLocaleString();
    document.getElementById('bmrValue').textContent = data.bmr.toLocaleString();
    document.getElementById('activityDescription').textContent = data.activity_description;
    document.getElementById('formulaUsed').textContent = data.formula_used;
    
    // Update units
    const unit = data.results_unit === 'kilojoules' ? 'kJ/day' : 'Calories/day';
    const unitShort = data.results_unit === 'kilojoules' ? 'kJ/day' : 'cal/day';
    
    document.getElementById('resultsUnit').textContent = unit;
    document.getElementById('bmrUnit').textContent = unit;
    
    // Update unit labels in weight management table
    const unitLabels = document.querySelectorAll('.unit-label');
    unitLabels.forEach(label => {
        label.textContent = unitShort;
    });
    
    // Update weight management values
    const weightManagement = data.weight_management;
    document.getElementById('extremeLoss').textContent = weightManagement.extreme_loss.toLocaleString();
    document.getElementById('moderateLoss').textContent = weightManagement.moderate_loss.toLocaleString();
    document.getElementById('mildLoss').textContent = weightManagement.mild_loss.toLocaleString();
    document.getElementById('maintain').textContent = weightManagement.maintain.toLocaleString();
    document.getElementById('mildGain').textContent = weightManagement.mild_gain.toLocaleString();
    document.getElementById('moderateGain').textContent = weightManagement.moderate_gain.toLocaleString();
    
    // Show results
    const resultsDiv = document.getElementById('calorieResults');
    resultsDiv.style.display = 'block';
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function displayBMIResults(data) {
    // Update BMI values
    document.getElementById('bmiValue').textContent = data.bmi;
    document.getElementById('bmiClassification').textContent = data.classification;
    document.getElementById('bmiPrime').textContent = data.bmi_prime;
    document.getElementById('ponderalIndex').textContent = data.ponderal_index;
    
    // Update healthy weight range
    let weightRange;
    if (data.unit_system === 'us') {
        weightRange = `${data.min_healthy_weight_lbs} lbs - ${data.max_healthy_weight_lbs} lbs`;
    } else {
        weightRange = `${data.min_healthy_weight_kg} kg - ${data.max_healthy_weight_kg} kg`;
    }
    document.getElementById('healthyWeightRange').textContent = weightRange;
    
    // Update BMI classification color
    const classificationElement = document.getElementById('bmiClassification');
    const classification = data.classification.toLowerCase();
    
    classificationElement.className = 'text-primary'; // Default
    if (classification.includes('thinness') || classification.includes('underweight')) {
        classificationElement.className = 'text-info';
    } else if (classification === 'normal') {
        classificationElement.className = 'text-success';
    } else if (classification === 'overweight') {
        classificationElement.className = 'text-warning';
    } else if (classification.includes('obese')) {
        classificationElement.className = 'text-danger';
    }
    
    // Show results
    const resultsDiv = document.getElementById('bmiResults');
    resultsDiv.style.display = 'block';
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showError(message) {
    // Remove existing error messages
    clearErrors();
    
    // Create error element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
    
    // Insert error message at the top of the container
    const container = document.querySelector('.container');
    container.insertBefore(errorDiv, container.firstChild);
    
    // Scroll to error message
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, 5000);
}

function clearErrors() {
    const errors = document.querySelectorAll('.error');
    errors.forEach(error => {
        if (error.parentNode) {
            error.parentNode.removeChild(error);
        }
    });
}

// Utility functions for form validation
function validateAge(age, min = 15, max = 80) {
    const ageNum = parseInt(age);
    return !isNaN(ageNum) && ageNum >= min && ageNum <= max;
}

function validateWeight(weight, unit = 'lbs') {
    const weightNum = parseFloat(weight);
    if (isNaN(weightNum) || weightNum <= 0) return false;
    
    if (unit === 'lbs') {
        return weightNum >= 50 && weightNum <= 1000;
    } else {
        return weightNum >= 20 && weightNum <= 500;
    }
}

function validateHeight(height, unit = 'cm') {
    const heightNum = parseFloat(height);
    if (isNaN(heightNum) || heightNum <= 0) return false;
    
    if (unit === 'cm') {
        return heightNum >= 100 && heightNum <= 250;
    } else {
        return heightNum >= 36 && heightNum <= 96; // inches
    }
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateAge,
        validateWeight,
        validateHeight
    };
}
document.addEventListener("DOMContentLoaded", () => {
  function syncRadios(selector, storageKey) {
    const radios = document.querySelectorAll(selector);

    // Restore from sessionStorage
    const saved = sessionStorage.getItem(storageKey);
    if (saved) {
      radios.forEach(r => { r.checked = (r.value === saved); });
    }

    // When one changes, update all + persist
    radios.forEach(radio => {
      radio.addEventListener("change", () => {
        if (radio.checked) {
          radios.forEach(r => { r.checked = (r.value === radio.value); });
          sessionStorage.setItem(storageKey, radio.value);
        }
      });
    });
  }

  // Apply to Calorie Calculator (name="gender")
  syncRadios('input[name="gender"]', "calorie_gender");

  // Apply to BMI Calculator (name="bmi_gender")
  syncRadios('input[name="bmi_gender"]', "bmi_gender");
});
