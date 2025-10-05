"""
Calorie and nutrition calculation utilities
"""

# Activity level multipliers
ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "lightly_active": 1.375,
    "moderately_active": 1.55,
    "very_active": 1.725,
    "extremely_active": 1.9
}

# Health goal adjustments (calorie deficit/surplus)
HEALTH_GOAL_ADJUSTMENTS = {
    "weight_loss": -500,
    "maintenance": 0,
    "muscle_gain": 300,
    "endurance": 200
}


def calculate_bmr(age: int, gender: str, weight: float, height: float) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
    
    Args:
        age: Age in years
        gender: "male" or "female"
        weight: Weight in kg
        height: Height in cm
    
    Returns:
        BMR in calories
    """
    if gender.lower() == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:  # female
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    return round(bmr, 2)


def calculate_daily_calories(bmr: float, activity_level: str, health_goal: str) -> int:
    """
    Calculate total daily calorie needs based on BMR, activity level, and health goal
    
    Args:
        bmr: Basal Metabolic Rate
        activity_level: Activity level key
        health_goal: Health goal key
    
    Returns:
        Daily calorie target
    """
    activity_multiplier = ACTIVITY_MULTIPLIERS.get(activity_level.lower(), 1.2)
    tdee = bmr * activity_multiplier
    
    goal_adjustment = HEALTH_GOAL_ADJUSTMENTS.get(health_goal.lower(), 0)
    daily_calories = tdee + goal_adjustment
    
    return int(daily_calories)


def calculate_macros(daily_calories: int, health_goal: str) -> dict:
    """
    Calculate macronutrient distribution based on calories and health goal
    
    Args:
        daily_calories: Total daily calories
        health_goal: Health goal (weight_loss, muscle_gain, etc.)
    
    Returns:
        Dictionary with protein, carbs, and fats in grams
    """
    # Protein: 25-30% for muscle gain, 20-25% for weight loss, 20% for maintenance
    # Fats: 25-30%
    # Carbs: remainder
    
    if health_goal.lower() == "muscle_gain":
        protein_percent = 0.30
        fat_percent = 0.25
    elif health_goal.lower() == "weight_loss":
        protein_percent = 0.25
        fat_percent = 0.30
    else:
        protein_percent = 0.20
        fat_percent = 0.25
    
    carb_percent = 1 - protein_percent - fat_percent
    
    # Calculate grams (protein: 4 cal/g, carbs: 4 cal/g, fats: 9 cal/g)
    protein_grams = int((daily_calories * protein_percent) / 4)
    carbs_grams = int((daily_calories * carb_percent) / 4)
    fat_grams = int((daily_calories * fat_percent) / 9)
    
    return {
        "protein": f"{protein_grams}g",
        "carbs": f"{carbs_grams}g",
        "fats": f"{fat_grams}g"
    }
