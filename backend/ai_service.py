"""
Google Generative AI (Gemini) integration for generating personalized diet and exercise plans
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_diet_plan(user_data: dict, daily_calories: int, macros: dict) -> dict:
    """
    Generate a personalized diet and exercise plan using Google Gemini AI
    
    Args:
        user_data: User profile information
        daily_calories: Calculated daily calorie target
        macros: Macronutrient breakdown
    
    Returns:
        Dictionary with meal_plan, exercises, and grocery_list
    """
    
    # Create structured prompt
    prompt = f"""
You are a professional nutritionist and fitness coach. Generate a detailed 1-day personalized diet and exercise plan.

**User Profile:**
- Age: {user_data['age']} years old
- Gender: {user_data['gender']}
- Height: {user_data['height']} cm
- Weight: {user_data['weight']} kg
- Activity Level: {user_data['activity_level']}
- Health Goal: {user_data['health_goal']}
- Food Preferences: {user_data['food_preferences']}
- Allergies: {user_data.get('allergies', 'None')}
- Medical Conditions: {user_data.get('medical_conditions', 'None')}

**Nutritional Targets:**
- Daily Calories: {daily_calories} kcal
- Protein: {macros['protein']}
- Carbs: {macros['carbs']}
- Fats: {macros['fats']}

**Instructions:**
Generate a complete plan in JSON format with the following structure:

{{
  "meal_plan": {{
    "breakfast": "Detailed breakfast meal with portions and approximate calories",
    "lunch": "Detailed lunch meal with portions and approximate calories",
    "dinner": "Detailed dinner meal with portions and approximate calories",
    "snacks": "Healthy snack options with portions and approximate calories"
  }},
  "exercises": [
    "Exercise 1 with sets/reps/duration",
    "Exercise 2 with sets/reps/duration",
    "Exercise 3 with sets/reps/duration",
    "Exercise 4 with sets/reps/duration",
    "Exercise 5 with sets/reps/duration"
  ],
  "grocery_list": [
    "Ingredient 1",
    "Ingredient 2",
    "Ingredient 3",
    "Ingredient 4",
    "Ingredient 5",
    "Ingredient 6",
    "Ingredient 7",
    "Ingredient 8",
    "Ingredient 9",
    "Ingredient 10"
  ]
}}

Important:
- Respect food preferences and allergies
- Consider medical conditions when recommending foods
- Make exercises appropriate for the activity level and health goal
- Include both home and gym exercise options when possible
- Ensure meals align with the calorie and macro targets
- Return ONLY valid JSON, no additional text
"""

    try:
        # Use the latest available Gemini model
        # Based on models available as of October 2025
        model_names = [
            'models/gemini-2.5-pro-preview-03-25',  # Latest recommended
            'models/gemini-2.5-flash-lite-preview-09-2025',  # Fast alternative
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-pro-latest',
            'gemini-1.5-flash',
            'gemini-pro'
        ]
        
        model = None
        last_error = None
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"✓ Using model: {model_name}")
                break
            except Exception as e:
                last_error = str(e)
                continue
        
        if model is None:
            raise Exception(f"No compatible model found. Last error: {last_error}")
        
        # Generate content
        response = model.generate_content(prompt)
        
        # Parse the response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        plan_data = json.loads(response_text)
        
        return plan_data
    
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        # Return a fallback structure
        return {
            "meal_plan": {
                "breakfast": "Oatmeal with fruits and nuts (400 kcal)",
                "lunch": "Grilled chicken with quinoa and vegetables (500 kcal)",
                "dinner": "Salmon with sweet potato and broccoli (550 kcal)",
                "snacks": "Greek yogurt with berries (200 kcal)"
            },
            "exercises": [
                "Warm-up: 5 minutes of light cardio",
                "Squats: 3 sets of 12 reps",
                "Push-ups: 3 sets of 10 reps",
                "Plank: 3 sets of 30 seconds",
                "Cool-down: 5 minutes stretching"
            ],
            "grocery_list": [
                "Oats", "Mixed fruits", "Nuts", "Chicken breast", "Quinoa",
                "Mixed vegetables", "Salmon", "Sweet potato", "Broccoli", "Greek yogurt"
            ]
        }
    
    except Exception as e:
        error_msg = str(e)
        print(f"Error generating plan: {e}")
        
        # Check if it's a quota error
        if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
            print("⚠️  Quota exceeded - using fallback demo plan")
            # Return a contextual fallback based on user goals
            goal = user_data.get('health_goal', 'maintenance').lower()
            preferences = user_data.get('food_preferences', '').lower()
            
            # Customize fallback based on goals
            if 'weight_loss' in goal:
                return get_weight_loss_fallback(daily_calories, macros, preferences)
            elif 'muscle_gain' in goal:
                return get_muscle_gain_fallback(daily_calories, macros, preferences)
            else:
                return get_maintenance_fallback(daily_calories, macros, preferences)
        
        # For other errors, re-raise
        raise


def get_weight_loss_fallback(calories: int, macros: dict, preferences: str) -> dict:
    """Fallback plan for weight loss goals"""
    is_veg = 'veg' in preferences
    
    return {
        "meal_plan": {
            "breakfast": f"Egg white omelet with spinach and tomatoes OR Oatmeal with berries ({int(calories * 0.25)} kcal)" if not is_veg else f"Oatmeal with chia seeds and berries ({int(calories * 0.25)} kcal)",
            "lunch": f"Grilled chicken salad with mixed greens and olive oil OR Lentil soup with vegetables ({int(calories * 0.35)} kcal)" if not is_veg else f"Quinoa bowl with chickpeas and roasted vegetables ({int(calories * 0.35)} kcal)",
            "dinner": f"Baked salmon with steamed broccoli and cauliflower ({int(calories * 0.30)} kcal)" if not is_veg else f"Tofu stir-fry with mixed vegetables and brown rice ({int(calories * 0.30)} kcal)",
            "snacks": f"Greek yogurt OR apple with almond butter ({int(calories * 0.10)} kcal)"
        },
        "exercises": [
            "Warm-up: 5-10 minutes brisk walking",
            "Cardio: 30 minutes jogging or cycling (moderate intensity)",
            "Bodyweight squats: 3 sets of 15 reps",
            "Push-ups (modified if needed): 3 sets of 10 reps",
            "Plank: 3 sets of 30-45 seconds",
            "Cool-down: 5 minutes stretching"
        ],
        "grocery_list": [
            "Eggs" if not is_veg else "Chia seeds",
            "Spinach", "Tomatoes", "Mixed greens", "Olive oil",
            "Chicken breast" if not is_veg else "Tofu",
            "Quinoa", "Lentils", "Chickpeas",
            "Broccoli", "Cauliflower", "Mixed vegetables",
            "Salmon" if not is_veg else "Extra tofu",
            "Greek yogurt", "Berries", "Apples", "Almond butter"
        ]
    }


def get_muscle_gain_fallback(calories: int, macros: dict, preferences: str) -> dict:
    """Fallback plan for muscle gain goals"""
    is_veg = 'veg' in preferences
    
    return {
        "meal_plan": {
            "breakfast": f"4 whole eggs scrambled with avocado and whole wheat toast OR Protein oatmeal with nuts and banana ({int(calories * 0.25)} kcal)" if not is_veg else f"Protein-rich smoothie with banana, oats, peanut butter, and plant protein ({int(calories * 0.25)} kcal)",
            "lunch": f"Grilled chicken breast with brown rice and mixed vegetables ({int(calories * 0.30)} kcal)" if not is_veg else f"Large tempeh bowl with quinoa, sweet potato, and avocado ({int(calories * 0.30)} kcal)",
            "dinner": f"Lean beef or turkey with pasta and marinara sauce ({int(calories * 0.30)} kcal)" if not is_veg else f"Lentil and bean curry with brown rice ({int(calories * 0.30)} kcal)",
            "snacks": f"Protein shake, cottage cheese with fruit, handful of almonds ({int(calories * 0.15)} kcal)"
        },
        "exercises": [
            "Warm-up: 5-10 minutes light cardio and dynamic stretching",
            "Barbell squats: 4 sets of 8-10 reps (or bodyweight if at home)",
            "Bench press or push-ups: 4 sets of 8-10 reps",
            "Deadlifts or Romanian deadlifts: 3 sets of 8 reps",
            "Pull-ups or rows: 3 sets of 8-10 reps",
            "Bicep curls: 3 sets of 12 reps",
            "Tricep dips: 3 sets of 12 reps",
            "Cool-down: 5-10 minutes stretching"
        ],
        "grocery_list": [
            "Eggs (2 dozen)" if not is_veg else "Plant-based protein powder",
            "Chicken breast" if not is_veg else "Tempeh",
            "Lean beef or turkey" if not is_veg else "Lentils and beans",
            "Brown rice", "Quinoa", "Whole wheat bread", "Pasta",
            "Sweet potato", "Avocados", "Mixed vegetables",
            "Bananas", "Mixed nuts", "Almond butter",
            "Cottage cheese" if not is_veg else "Nutritional yeast",
            "Protein powder", "Olive oil"
        ]
    }


def get_maintenance_fallback(calories: int, macros: dict, preferences: str) -> dict:
    """Fallback plan for maintenance goals"""
    is_veg = 'veg' in preferences
    
    return {
        "meal_plan": {
            "breakfast": f"Whole grain toast with avocado and eggs OR Greek yogurt parfait with granola ({int(calories * 0.25)} kcal)" if not is_veg else f"Smoothie bowl with fruits, granola, and nut butter ({int(calories * 0.25)} kcal)",
            "lunch": f"Turkey and hummus wrap with vegetables OR Chicken Caesar salad ({int(calories * 0.35)} kcal)" if not is_veg else f"Buddha bowl with quinoa, roasted chickpeas, and tahini dressing ({int(calories * 0.35)} kcal)",
            "dinner": f"Grilled fish with roasted vegetables and wild rice ({int(calories * 0.30)} kcal)" if not is_veg else f"Vegetable stir-fry with tofu and noodles ({int(calories * 0.30)} kcal)",
            "snacks": f"Fresh fruit, nuts, or protein bar ({int(calories * 0.10)} kcal)"
        },
        "exercises": [
            "Warm-up: 5 minutes light cardio",
            "Moderate cardio: 20-25 minutes (jogging, cycling, or swimming)",
            "Bodyweight exercises: squats, lunges, push-ups (3 sets of 12)",
            "Core work: planks and crunches (3 sets)",
            "Flexibility: yoga or stretching (10 minutes)",
            "Cool-down: 5 minutes walking"
        ],
        "grocery_list": [
            "Whole grain bread", "Avocados", "Eggs" if not is_veg else "Extra nut butter",
            "Greek yogurt" if not is_veg else "Coconut yogurt",
            "Turkey" if not is_veg else "Additional chickpeas",
            "Fish" if not is_veg else "Tofu",
            "Quinoa", "Wild rice", "Noodles",
            "Hummus", "Mixed vegetables", "Chickpeas",
            "Fresh fruits", "Mixed nuts", "Granola", "Tahini"
        ]
    }
