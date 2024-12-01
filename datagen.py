import numpy as np
import pandas as pd
import random
from faker import Faker

# Initialize Faker to generate random Product Names and IDs
fake = Faker()

# Number of records
num_records = 50000

# Function to simulate health condition-based features
def generate_health_condition():
    conditions = ['Healthy', 'Diabetic', 'Hypertension', 'Obese', 'Heart Disease']
    return random.choice(conditions)

def generate_activity_level():
    activity_levels = ['Low', 'Medium', 'High']
    return random.choice(activity_levels)

def generate_blood_sugar_level(health_condition, age):
    """Simulate blood sugar based on health condition and age"""
    if health_condition == 'Diabetic':
        # Diabetics generally have higher blood sugar levels
        return np.random.normal(200, 50)  # Mean of 200, std of 50
    return np.random.normal(100, 20)  # Normal for others

def generate_blood_pressure(health_condition, age, activity_level):
    """Simulate blood pressure based on condition, age, and activity level"""
    if health_condition == 'Hypertension':
        return np.random.normal(150, 20)  # Higher mean for hypertension
    if age > 60:
        return np.random.normal(140, 15)  # Older people tend to have higher blood pressure
    if activity_level == 'Low':
        return np.random.normal(120, 15)  # Less active people tend to have higher BP
    return np.random.normal(110, 10)  # Normal range

def generate_bmi(height, weight):
    """Calculate BMI using the standard formula"""
    height_in_meters = height / 100  # Convert cm to meters
    return weight / (height_in_meters ** 2)  # BMI formula

def health_compatibility_score(calories, sodium, bmi, health_condition, activity_level):
    """A more refined formula for health compatibility score"""
    score = 100 - (calories / 10 + sodium / 100 + (bmi - 22) * 2)  # Adjust BMI-related penalties
    if health_condition == 'Diabetic':
        score -= 20  # Diabetics are more sensitive to unhealthy food
    if health_condition == 'Hypertension':
        score -= 10  # Hypertension requires lower salt intake
    if activity_level == 'Low':
        score -= 5  # Less active people have a higher health risk
    return max(0, score)  # Ensure score doesn't go below 0

def health_risk(compatibility_score):
    """Determine health risk based on the compatibility score"""
    if compatibility_score < 50:
        return "High"
    elif compatibility_score < 75:
        return "Medium"
    return "Low"

# Generate synthetic data
def generate_data(num_records):
    data = []
    for _ in range(num_records):
        # Product Info
        product_id = 'P' + str(random.randint(1, 99999)).zfill(5)
        product_name = fake.word() + " Product"
        
        # Nutritional Info (Normal Distribution)
        calories = round(np.random.normal(250, 50), 2)  # Mean of 250, std of 50
        carbs = round(np.random.normal(40, 15), 2)  # Mean of 40g, std of 15g
        sugars = round(np.random.normal(15, 5), 2)  # Mean of 15g, std of 5g
        fat = round(np.random.normal(20, 8), 2)  # Mean of 20g, std of 8g
        protein = round(np.random.normal(15, 6), 2)  # Mean of 15g, std of 6g
        sodium = round(np.random.normal(800, 400), 2)  # Mean of 800mg, std of 400mg
        serving_size = round(np.random.normal(150, 50), 2)  # Mean of 150g, std of 50g
        
        # Health Info (Normal Distribution)
        health_condition = generate_health_condition()
        
        # Height and Weight based on human dimensions
        height = round(np.random.normal(170, 10), 2)  # Mean height of 170 cm, std of 10 cm
        weight = round(np.random.normal(70, 15), 2)  # Mean weight of 70 kg, std of 15 kg
        
        age = random.randint(18, 80)
        bmi = generate_bmi(height, weight)
        
        activity_level = generate_activity_level()
        blood_sugar_level = generate_blood_sugar_level(health_condition, age)
        blood_pressure = generate_blood_pressure(health_condition, age, activity_level)
        
        compatibility_score = health_compatibility_score(calories, sodium, bmi, health_condition, activity_level)
        health_risk_level = health_risk(compatibility_score)
        
        data.append([product_id, product_name, calories, carbs, sugars, fat, protein, sodium, serving_size, 
                    health_condition, height, weight, age, bmi, activity_level, blood_sugar_level, 
                    blood_pressure, compatibility_score, health_risk_level])
    
    return pd.DataFrame(data, columns=[
        'Product_ID', 'Product_Name', 'Calories', 'Carbs', 'Sugars', 'Fat', 'Protein', 'Sodium', 'Serving_Size',
        'Health_Condition', 'Height', 'Weight', 'Age', 'BMI', 'Activity_Level', 'Blood_Sugar_Level', 'Blood_Pressure',
        'Health_Compatibility_Score', 'Health_Risk'])

generated_data = generate_data(num_records)
generated_data.to_csv('generated_data_normal.csv', index=False)
generated_data.head()
