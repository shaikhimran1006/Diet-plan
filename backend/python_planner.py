"""
Python-based diet and exercise plan generator
No AI/LLM required - uses nutritional science and algorithms
"""

import random
from typing import Dict, List


# Food database with nutritional information (per 100g)
FOODS_DATABASE = {
    "proteins": {
        "chicken_breast": {"calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "name": "Chicken Breast"},
        "eggs": {"calories": 155, "protein": 13, "carbs": 1.1, "fats": 11, "name": "Eggs"},
        "greek_yogurt": {"calories": 97, "protein": 10, "carbs": 3.6, "fats": 5, "name": "Greek Yogurt"},
        "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fats": 13, "name": "Salmon"},
        "tuna": {"calories": 130, "protein": 28, "carbs": 0, "fats": 1, "name": "Tuna"},
        "turkey": {"calories": 135, "protein": 30, "carbs": 0, "fats": 1, "name": "Turkey"},
        "tofu": {"calories": 76, "protein": 8, "carbs": 1.9, "fats": 4.8, "name": "Tofu"},
        "lentils": {"calories": 116, "protein": 9, "carbs": 20, "fats": 0.4, "name": "Lentils"},
        "chickpeas": {"calories": 164, "protein": 8.9, "carbs": 27, "fats": 2.6, "name": "Chickpeas"},
        "cottage_cheese": {"calories": 98, "protein": 11, "carbs": 3.4, "fats": 4.3, "name": "Cottage Cheese"},
        "tempeh": {"calories": 193, "protein": 19, "carbs": 9, "fats": 11, "name": "Tempeh"},
        "protein_powder": {"calories": 120, "protein": 24, "carbs": 3, "fats": 1.5, "name": "Protein Powder"},
    },
    "carbs": {
        "oatmeal": {"calories": 389, "protein": 17, "carbs": 66, "fats": 7, "name": "Oatmeal"},
        "brown_rice": {"calories": 111, "protein": 2.6, "carbs": 23, "fats": 0.9, "name": "Brown Rice"},
        "quinoa": {"calories": 120, "protein": 4.4, "carbs": 21, "fats": 1.9, "name": "Quinoa"},
        "sweet_potato": {"calories": 86, "protein": 1.6, "carbs": 20, "fats": 0.1, "name": "Sweet Potato"},
        "whole_wheat_bread": {"calories": 247, "protein": 13, "carbs": 41, "fats": 3.4, "name": "Whole Wheat Bread"},
        "pasta": {"calories": 131, "protein": 5, "carbs": 25, "fats": 1.1, "name": "Whole Wheat Pasta"},
        "banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fats": 0.3, "name": "Banana"},
        "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fats": 0.2, "name": "Apple"},
        "berries": {"calories": 57, "protein": 0.7, "carbs": 14, "fats": 0.3, "name": "Mixed Berries"},
    },
    "vegetables": {
        "broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fats": 0.4, "name": "Broccoli"},
        "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fats": 0.4, "name": "Spinach"},
        "mixed_vegetables": {"calories": 65, "protein": 2.6, "carbs": 13, "fats": 0.4, "name": "Mixed Vegetables"},
        "tomatoes": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fats": 0.2, "name": "Tomatoes"},
        "cucumber": {"calories": 15, "protein": 0.7, "carbs": 3.6, "fats": 0.1, "name": "Cucumber"},
        "bell_peppers": {"calories": 31, "protein": 1, "carbs": 6, "fats": 0.3, "name": "Bell Peppers"},
        "cauliflower": {"calories": 25, "protein": 1.9, "carbs": 5, "fats": 0.3, "name": "Cauliflower"},
        "salad_greens": {"calories": 15, "protein": 1.4, "carbs": 2.9, "fats": 0.2, "name": "Salad Greens"},
    },
    "fats": {
        "avocado": {"calories": 160, "protein": 2, "carbs": 9, "fats": 15, "name": "Avocado"},
        "almonds": {"calories": 579, "protein": 21, "carbs": 22, "fats": 50, "name": "Almonds"},
        "olive_oil": {"calories": 884, "protein": 0, "carbs": 0, "fats": 100, "name": "Olive Oil"},
        "peanut_butter": {"calories": 588, "protein": 25, "carbs": 20, "fats": 50, "name": "Peanut Butter"},
        "walnuts": {"calories": 654, "protein": 15, "carbs": 14, "fats": 65, "name": "Walnuts"},
        "chia_seeds": {"calories": 486, "protein": 17, "carbs": 42, "fats": 31, "name": "Chia Seeds"},
    }
}

# Exercise database categorized by goal
EXERCISES_DATABASE = {
    "weight_loss": {
        "cardio": [
            "30-40 minutes brisk walking or jogging",
            "20-30 minutes cycling (moderate to high intensity)",
            "15-20 minutes HIIT (High-Intensity Interval Training)",
            "30 minutes swimming",
            "20 minutes jump rope intervals",
        ],
        "strength": [
            "Bodyweight squats: 3 sets of 15-20 reps",
            "Push-ups: 3 sets of 10-15 reps",
            "Lunges: 3 sets of 12 reps per leg",
            "Plank: 3 sets of 45-60 seconds",
            "Mountain climbers: 3 sets of 20 reps",
        ],
    },
    "muscle_gain": {
        "strength": [
            "Barbell squats: 4 sets of 8-10 reps (heavy weight)",
            "Bench press: 4 sets of 8-10 reps",
            "Deadlifts: 4 sets of 6-8 reps",
            "Pull-ups or lat pulldowns: 4 sets of 8-12 reps",
            "Overhead press: 3 sets of 8-10 reps",
            "Barbell rows: 4 sets of 8-10 reps",
            "Bicep curls: 3 sets of 10-12 reps",
            "Tricep dips: 3 sets of 10-12 reps",
        ],
        "cardio": [
            "10-15 minutes light cardio warm-up",
            "Optional: 20 minutes low-intensity cardio on rest days",
        ],
    },
    "maintenance": {
        "balanced": [
            "20-30 minutes moderate cardio (jogging, cycling)",
            "Full body workout: squats, push-ups, rows (3 sets of 12)",
            "Core exercises: planks, crunches (3 sets)",
            "Stretching or yoga: 10-15 minutes",
        ],
    },
    "endurance": {
        "cardio": [
            "45-60 minutes steady-state running",
            "30-40 minutes cycling (moderate intensity)",
            "30 minutes swimming",
            "Interval training: 5x (3 min hard, 2 min easy)",
        ],
        "strength": [
            "Light resistance training: 3 sets of 15 reps",
            "Core strengthening: planks, leg raises",
            "Flexibility work: 15 minutes stretching",
        ],
    },
}


def generate_meal(meal_type: str, calories_target: int, protein_g: int, carbs_g: int, fats_g: int, 
                 is_vegetarian: bool, allergies: List[str]) -> Dict:
    """Generate a meal based on nutritional targets"""
    
    # Filter foods based on preferences
    proteins = {k: v for k, v in FOODS_DATABASE["proteins"].items() 
                if not (not is_vegetarian or k in ["tofu", "lentils", "chickpeas", "tempeh"]) if is_vegetarian}
    
    if not is_vegetarian:
        proteins = FOODS_DATABASE["proteins"]
    else:
        proteins = {k: v for k, v in FOODS_DATABASE["proteins"].items() 
                   if k in ["tofu", "lentils", "chickpeas", "tempeh", "greek_yogurt", "cottage_cheese", "eggs", "protein_powder"]}
    
    # Remove allergens
    if allergies:
        allergen_keywords = [a.lower() for a in allergies]
        if any(word in allergen_keywords for word in ["nut", "almond", "peanut"]):
            FOODS_DATABASE["fats"] = {k: v for k, v in FOODS_DATABASE["fats"].items() 
                                      if k not in ["almonds", "peanut_butter", "walnuts"]}
    
    # Select foods based on meal type
    if meal_type == "breakfast":
        protein_choices = ["eggs", "greek_yogurt", "protein_powder", "cottage_cheese"]
        carb_choices = ["oatmeal", "whole_wheat_bread", "banana", "berries"]
    elif meal_type == "lunch":
        protein_choices = ["chicken_breast", "tuna", "turkey", "tofu", "chickpeas"]
        carb_choices = ["brown_rice", "quinoa", "sweet_potato", "whole_wheat_bread"]
    elif meal_type == "dinner":
        protein_choices = ["salmon", "chicken_breast", "turkey", "tempeh", "lentils"]
        carb_choices = ["brown_rice", "quinoa", "sweet_potato", "pasta"]
    else:  # snacks
        protein_choices = ["greek_yogurt", "cottage_cheese", "protein_powder"]
        carb_choices = ["apple", "banana", "berries"]
    
    # Filter based on diet
    if is_vegetarian:
        protein_choices = [p for p in protein_choices if p in ["eggs", "greek_yogurt", "protein_powder", 
                                                                "cottage_cheese", "tofu", "chickpeas", "tempeh", "lentils"]]
    
    # Select primary protein
    protein_food = random.choice([p for p in protein_choices if p in proteins])
    protein_data = proteins[protein_food]
    
    # Calculate portions (rough estimates)
    protein_portion = int(protein_g * 100 / protein_data["protein"]) if protein_data["protein"] > 0 else 100
    protein_portion = min(max(protein_portion, 50), 300)  # Between 50-300g
    
    # Select carb source
    carb_food = random.choice(carb_choices)
    carb_data = FOODS_DATABASE["carbs"][carb_food]
    carb_portion = int(carbs_g * 100 / carb_data["carbs"]) if carb_data["carbs"] > 0 else 100
    carb_portion = min(max(carb_portion, 30), 200)
    
    # Select vegetable
    veg_food = random.choice(list(FOODS_DATABASE["vegetables"].keys()))
    veg_data = FOODS_DATABASE["vegetables"][veg_food]
    veg_portion = 150  # Standard portion
    
    # Select fat source
    fat_food = random.choice(list(FOODS_DATABASE["fats"].keys()))
    fat_data = FOODS_DATABASE["fats"][fat_food]
    fat_portion = int(fats_g * 100 / fat_data["fats"]) if fat_data["fats"] > 0 else 15
    fat_portion = min(max(fat_portion, 10), 50)
    
    # Calculate actual calories
    actual_calories = (
        protein_portion * protein_data["calories"] / 100 +
        carb_portion * carb_data["calories"] / 100 +
        veg_portion * veg_data["calories"] / 100 +
        fat_portion * fat_data["calories"] / 100
    )
    
    # Build meal description
    meal = f"{protein_portion}g {protein_data['name']}, {carb_portion}g {carb_data['name']}, "
    meal += f"{veg_portion}g {veg_data['name']}, {fat_portion}g {fat_data['name']}"
    meal += f" (~{int(actual_calories)} kcal)"
    
    return {
        "description": meal,
        "calories": int(actual_calories),
        "items": [protein_data['name'], carb_data['name'], veg_data['name'], fat_data['name']]
    }


def generate_python_diet_plan(user_data: dict, daily_calories: int, macros: dict) -> dict:
    """
    Generate diet and exercise plan using Python algorithms (no AI/LLM)
    """
    
    # Parse user data
    goal = user_data.get('health_goal', 'maintenance').lower()
    preferences = user_data.get('food_preferences', '').lower()
    allergies_str = user_data.get('allergies', '') or ''
    allergies = [a.strip() for a in allergies_str.split(',') if a.strip()]
    
    is_vegetarian = any(word in preferences for word in ['vegetarian', 'vegan', 'plant-based'])
    
    # Parse macros
    protein_g = int(macros['protein'].replace('g', ''))
    carbs_g = int(macros['carbs'].replace('g', ''))
    fats_g = int(macros['fats'].replace('g', ''))
    
    # Distribute calories across meals
    breakfast_cal = int(daily_calories * 0.25)
    lunch_cal = int(daily_calories * 0.35)
    dinner_cal = int(daily_calories * 0.30)
    snack_cal = int(daily_calories * 0.10)
    
    # Distribute macros across meals
    breakfast_p, breakfast_c, breakfast_f = int(protein_g * 0.25), int(carbs_g * 0.25), int(fats_g * 0.25)
    lunch_p, lunch_c, lunch_f = int(protein_g * 0.35), int(carbs_g * 0.35), int(fats_g * 0.35)
    dinner_p, dinner_c, dinner_f = int(protein_g * 0.30), int(carbs_g * 0.30), int(fats_g * 0.30)
    snack_p, snack_c, snack_f = int(protein_g * 0.10), int(carbs_g * 0.10), int(fats_g * 0.10)
    
    # Generate meals
    breakfast = generate_meal("breakfast", breakfast_cal, breakfast_p, breakfast_c, breakfast_f, is_vegetarian, allergies)
    lunch = generate_meal("lunch", lunch_cal, lunch_p, lunch_c, lunch_f, is_vegetarian, allergies)
    dinner = generate_meal("dinner", dinner_cal, dinner_p, dinner_c, dinner_f, is_vegetarian, allergies)
    snacks = generate_meal("snacks", snack_cal, snack_p, snack_c, snack_f, is_vegetarian, allergies)
    
    # Generate exercise plan
    if 'weight_loss' in goal or 'loss' in goal:
        exercises = EXERCISES_DATABASE["weight_loss"]["cardio"][:3] + EXERCISES_DATABASE["weight_loss"]["strength"][:2]
    elif 'muscle' in goal or 'gain' in goal:
        exercises = EXERCISES_DATABASE["muscle_gain"]["strength"][:5] + EXERCISES_DATABASE["muscle_gain"]["cardio"][:1]
    elif 'endurance' in goal:
        exercises = EXERCISES_DATABASE["endurance"]["cardio"][:3] + EXERCISES_DATABASE["endurance"]["strength"][:2]
    else:
        exercises = EXERCISES_DATABASE["maintenance"]["balanced"]
    
    # Add warm-up and cool-down
    exercises = ["Warm-up: 5-10 minutes light cardio and stretching"] + exercises + ["Cool-down: 5-10 minutes stretching"]
    
    # Generate grocery list
    grocery_list = []
    for meal in [breakfast, lunch, dinner, snacks]:
        grocery_list.extend(meal["items"])
    
    # Remove duplicates and sort
    grocery_list = sorted(list(set(grocery_list)))
    
    return {
        "meal_plan": {
            "breakfast": breakfast["description"],
            "lunch": lunch["description"],
            "dinner": dinner["description"],
            "snacks": snacks["description"]
        },
        "exercises": exercises,
        "grocery_list": grocery_list
    }
