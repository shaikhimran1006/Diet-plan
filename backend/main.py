from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
import json

from database import init_db, get_db, User, Plan, WeightLog, HydrationLog, CalorieLog, ExerciseLog
from schemas import (
    UserInput, PlanResponse, MealPlan, Macros,
    WeightLogCreate, WeightLogResponse,
    HydrationLogCreate, HydrationLogResponse,
    CalorieLogCreate, CalorieLogResponse,
    ExerciseLogCreate, ExerciseLogResponse,
    ProgressStats
)
from calculations import calculate_bmr, calculate_daily_calories, calculate_macros
# Commented out AI service - using Python-based planner instead
# from ai_service import generate_diet_plan
from python_planner import generate_python_diet_plan
from prediction_engine import (
    PredictionEngine,
    get_weight_prediction,
    get_calorie_prediction,
    get_comprehensive_predictions
)

# Initialize FastAPI app
app = FastAPI(title="AI Diet & Fitness Planner", version="1.0.0")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and CRA default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def read_root():
    return {
        "message": "AI Diet & Fitness Recommendation System API",
        "version": "1.0.0",
        "endpoints": {
            "generate_plan": "/generate-plan (POST)",
            "get_history": "/history/{user_id} (GET)"
        }
    }


@app.post("/generate-plan", response_model=PlanResponse)
def generate_plan(user_input: UserInput, db: Session = Depends(get_db)):
    """
    Generate a personalized diet and fitness plan
    
    Steps:
    1. Calculate BMR using Mifflin-St Jeor equation
    2. Calculate daily calorie needs based on activity level and goal
    3. Calculate macronutrient distribution
    4. Generate AI-powered meal plan and exercise recommendations
    5. Store user data and plan in database
    6. Return complete plan
    """
    
    try:
        # Step 1: Save user data
        user = User(
            age=user_input.age,
            gender=user_input.gender,
            height=user_input.height,
            weight=user_input.weight,
            activity_level=user_input.activity_level,
            health_goal=user_input.health_goal,
            food_preferences=user_input.food_preferences,
            allergies=user_input.allergies,
            medical_conditions=user_input.medical_conditions
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Step 2: Calculate BMR
        bmr = calculate_bmr(
            age=user_input.age,
            gender=user_input.gender,
            weight=user_input.weight,
            height=user_input.height
        )
        
        # Step 3: Calculate daily calories
        daily_calories = calculate_daily_calories(
            bmr=bmr,
            activity_level=user_input.activity_level,
            health_goal=user_input.health_goal
        )
        
        # Step 4: Calculate macros
        macros = calculate_macros(
            daily_calories=daily_calories,
            health_goal=user_input.health_goal
        )
        
        # Step 5: Generate Python-based plan (NO AI/LLM required!)
        user_data = {
            "age": user_input.age,
            "gender": user_input.gender,
            "height": user_input.height,
            "weight": user_input.weight,
            "activity_level": user_input.activity_level,
            "health_goal": user_input.health_goal,
            "food_preferences": user_input.food_preferences,
            "allergies": user_input.allergies,
            "medical_conditions": user_input.medical_conditions
        }
        
        # Use Python-based algorithm instead of AI
        ai_plan = generate_python_diet_plan(user_data, daily_calories, macros)
        
        # Step 6: Save plan to database
        plan = Plan(
            user_id=user.id,
            bmr=bmr,
            daily_calories=daily_calories,
            meal_plan=json.dumps(ai_plan["meal_plan"]),
            macros=json.dumps(macros),
            exercises=json.dumps(ai_plan["exercises"]),
            grocery_list=json.dumps(ai_plan["grocery_list"])
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        
        # Step 7: Prepare response
        response = PlanResponse(
            user_id=user.id,
            bmr=bmr,
            daily_calories=daily_calories,
            meal_plan=MealPlan(**ai_plan["meal_plan"]),
            macros=Macros(calories=daily_calories, **macros),
            exercises=ai_plan["exercises"],
            grocery_list=ai_plan["grocery_list"],
            created_at=plan.created_at.isoformat()
        )
        
        return response
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating plan: {str(e)}")


@app.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user profile information
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "age": user.age,
        "gender": user.gender,
        "height": user.height,
        "weight": user.weight,
        "activity_level": user.activity_level,
        "health_goal": user.health_goal,
        "food_preferences": user.food_preferences,
        "allergies": user.allergies,
        "medical_conditions": user.medical_conditions
    }


@app.put("/user/{user_id}")
def update_user(user_id: int, user_input: UserInput, db: Session = Depends(get_db)):
    """
    Update user profile information
    This will cause predictions to recalculate based on new data
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    user.age = user_input.age
    user.gender = user_input.gender
    user.height = user_input.height
    user.weight = user_input.weight
    user.activity_level = user_input.activity_level
    user.health_goal = user_input.health_goal
    user.food_preferences = user_input.food_preferences
    user.allergies = user_input.allergies
    user.medical_conditions = user_input.medical_conditions
    
    db.commit()
    db.refresh(user)
    
    # Recalculate BMR with new data
    bmr = calculate_bmr(user.age, user.gender, user.weight, user.height)
    daily_calories = calculate_daily_calories(bmr, user.activity_level, user.health_goal)
    
    return {
        "message": "User profile updated successfully",
        "user": {
            "id": user.id,
            "age": user.age,
            "gender": user.gender,
            "height": user.height,
            "weight": user.weight,
            "activity_level": user.activity_level,
            "health_goal": user.health_goal
        },
        "updated_metrics": {
            "bmr": bmr,
            "daily_calories": daily_calories
        }
    }


@app.get("/history/{user_id}")
def get_user_history(user_id: int, db: Session = Depends(get_db)):
    """
    Get all plans for a specific user
    """
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    plans = db.query(Plan).filter(Plan.user_id == user_id).order_by(Plan.created_at.desc()).all()
    
    history = []
    for plan in plans:
        history.append({
            "id": plan.id,
            "bmr": plan.bmr,
            "daily_calories": plan.daily_calories,
            "meal_plan": json.loads(plan.meal_plan),
            "macros": json.loads(plan.macros),
            "exercises": json.loads(plan.exercises),
            "grocery_list": json.loads(plan.grocery_list),
            "created_at": plan.created_at.isoformat()
        })
    
    return {
        "user": {
            "id": user.id,
            "age": user.age,
            "gender": user.gender,
            "height": user.height,
            "weight": user.weight,
            "activity_level": user.activity_level,
            "health_goal": user.health_goal
        },
        "plans": history
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# ========== PROGRESS TRACKING ENDPOINTS ==========

@app.post("/weight-log/{user_id}", response_model=WeightLogResponse)
def log_weight(user_id: int, weight_log: WeightLogCreate, db: Session = Depends(get_db)):
    """Log daily weight"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    log = WeightLog(
        user_id=user_id,
        weight=weight_log.weight,
        notes=weight_log.notes,
        date=weight_log.date or date.today()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@app.get("/weight-log/{user_id}", response_model=list[WeightLogResponse])
def get_weight_logs(user_id: int, days: int = 30, db: Session = Depends(get_db)):
    """Get weight logs for the last N days"""
    logs = db.query(WeightLog).filter(
        WeightLog.user_id == user_id
    ).order_by(WeightLog.date.desc()).limit(days).all()
    return logs


@app.post("/hydration-log/{user_id}", response_model=HydrationLogResponse)
def log_hydration(user_id: int, hydration_log: HydrationLogCreate, db: Session = Depends(get_db)):
    """Log daily hydration"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if log exists for today
    today = hydration_log.date or date.today()
    existing = db.query(HydrationLog).filter(
        HydrationLog.user_id == user_id,
        HydrationLog.date == today
    ).first()
    
    if existing:
        existing.glasses += hydration_log.glasses
        db.commit()
        db.refresh(existing)
        return existing
    
    log = HydrationLog(
        user_id=user_id,
        glasses=hydration_log.glasses,
        date=today
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@app.get("/hydration-log/{user_id}", response_model=list[HydrationLogResponse])
def get_hydration_logs(user_id: int, days: int = 7, db: Session = Depends(get_db)):
    """Get hydration logs for the last N days"""
    logs = db.query(HydrationLog).filter(
        HydrationLog.user_id == user_id
    ).order_by(HydrationLog.date.desc()).limit(days).all()
    return logs


@app.post("/calorie-log/{user_id}", response_model=CalorieLogResponse)
def log_calories(user_id: int, calorie_log: CalorieLogCreate, db: Session = Depends(get_db)):
    """Log calorie intake"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    log = CalorieLog(
        user_id=user_id,
        calories=calorie_log.calories,
        meal_type=calorie_log.meal_type,
        description=calorie_log.description,
        date=calorie_log.date or date.today()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@app.get("/calorie-log/{user_id}", response_model=list[CalorieLogResponse])
def get_calorie_logs(user_id: int, days: int = 7, db: Session = Depends(get_db)):
    """Get calorie logs for the last N days"""
    logs = db.query(CalorieLog).filter(
        CalorieLog.user_id == user_id
    ).order_by(CalorieLog.date.desc(), CalorieLog.created_at.desc()).limit(days * 10).all()
    return logs


@app.post("/exercise-log/{user_id}", response_model=ExerciseLogResponse)
def log_exercise(user_id: int, exercise_log: ExerciseLogCreate, db: Session = Depends(get_db)):
    """Log exercise"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    log = ExerciseLog(
        user_id=user_id,
        exercise_name=exercise_log.exercise_name,
        duration_minutes=exercise_log.duration_minutes,
        calories_burned=exercise_log.calories_burned,
        date=exercise_log.date or date.today()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@app.get("/exercise-log/{user_id}", response_model=list[ExerciseLogResponse])
def get_exercise_logs(user_id: int, days: int = 7, db: Session = Depends(get_db)):
    """Get exercise logs for the last N days"""
    logs = db.query(ExerciseLog).filter(
        ExerciseLog.user_id == user_id
    ).order_by(ExerciseLog.date.desc(), ExerciseLog.created_at.desc()).limit(days * 10).all()
    return logs


@app.get("/progress/{user_id}", response_model=ProgressStats)
def get_progress_stats(user_id: int, db: Session = Depends(get_db)):
    """Get comprehensive progress statistics"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    today = date.today()
    
    # Get latest weight
    latest_weight = db.query(WeightLog).filter(
        WeightLog.user_id == user_id
    ).order_by(WeightLog.date.desc()).first()
    
    # Get first weight for comparison
    first_weight = db.query(WeightLog).filter(
        WeightLog.user_id == user_id
    ).order_by(WeightLog.date.asc()).first()
    
    weight_change = None
    if latest_weight and first_weight:
        weight_change = latest_weight.weight - first_weight.weight
    
    # Get today's hydration
    hydration_today = db.query(func.sum(HydrationLog.glasses)).filter(
        HydrationLog.user_id == user_id,
        HydrationLog.date == today
    ).scalar() or 0
    
    # Get today's calories
    calories_today = db.query(func.sum(CalorieLog.calories)).filter(
        CalorieLog.user_id == user_id,
        CalorieLog.date == today
    ).scalar() or 0
    
    # Get today's exercise
    exercise_today = db.query(func.sum(ExerciseLog.duration_minutes)).filter(
        ExerciseLog.user_id == user_id,
        ExerciseLog.date == today
    ).scalar() or 0
    
    # Get weight history (last 30 days)
    weight_history = db.query(WeightLog).filter(
        WeightLog.user_id == user_id
    ).order_by(WeightLog.date.desc()).limit(30).all()
    
    # Get hydration history (last 7 days)
    hydration_history = db.query(HydrationLog).filter(
        HydrationLog.user_id == user_id
    ).order_by(HydrationLog.date.desc()).limit(7).all()
    
    return ProgressStats(
        current_weight=latest_weight.weight if latest_weight else None,
        weight_change=weight_change,
        total_hydration_today=hydration_today,
        total_calories_today=calories_today,
        total_exercise_minutes_today=exercise_today,
        weight_history=weight_history,
        hydration_history=hydration_history
    )


# ========== PREDICTION ENDPOINTS ==========

@app.get("/predictions/weight/{user_id}")
def get_weight_predictions(user_id: int, db: Session = Depends(get_db)):
    """
    Get intelligent weight predictions based on historical data
    Returns trend analysis and future predictions
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get weight history
    weight_logs = db.query(WeightLog).filter(
        WeightLog.user_id == user_id
    ).order_by(WeightLog.date.asc()).all()
    
    if not weight_logs:
        return {
            "message": "No weight data available for predictions",
            "recommendation": "Start logging your weight daily for accurate predictions"
        }
    
    # Convert to dict format
    weight_history = [
        {"date": log.date, "weight": log.weight}
        for log in weight_logs
    ]
    
    prediction = get_weight_prediction(weight_history)
    
    return {
        "user_id": user_id,
        "current_weight": weight_history[-1]['weight'] if weight_history else None,
        "prediction": prediction,
        "data_points": len(weight_history),
        "analysis_period": f"{(weight_logs[-1].date - weight_logs[0].date).days} days"
    }


@app.get("/predictions/calories/{user_id}")
def get_calorie_predictions(user_id: int, db: Session = Depends(get_db)):
    """
    Get intelligent calorie recommendations based on progress
    Adjusts recommendations based on actual results
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get historical data
    weight_logs = db.query(WeightLog).filter(
        WeightLog.user_id == user_id
    ).order_by(WeightLog.date.asc()).all()
    
    calorie_logs = db.query(CalorieLog).filter(
        CalorieLog.user_id == user_id
    ).order_by(CalorieLog.date.desc()).limit(30).all()
    
    weight_history = [{"date": log.date, "weight": log.weight} for log in weight_logs]
    calorie_history = [{"date": log.date, "calories": log.calories} for log in calorie_logs]
    
    # Calculate BMR
    bmr = calculate_bmr(user.age, user.gender, user.weight, user.height)
    
    user_data = {
        "bmr": bmr,
        "age": user.age,
        "gender": user.gender,
        "weight": user.weight,
        "height": user.height,
        "activity_level": user.activity_level,
        "health_goal": user.health_goal
    }
    
    prediction = get_calorie_prediction(user_data, weight_history, calorie_history)
    
    return {
        "user_id": user_id,
        "prediction": prediction,
        "current_bmr": bmr,
        "goal": user.health_goal
    }


@app.get("/predictions/comprehensive/{user_id}")
def get_all_predictions(user_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive predictions including:
    - Weight trends and forecasts
    - Optimal calorie intake
    - Hydration needs
    - Exercise adherence analysis
    - Meal timing recommendations
    - Plateau risk assessment
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Gather all historical data
    weight_logs = db.query(WeightLog).filter(
        WeightLog.user_id == user_id
    ).order_by(WeightLog.date.asc()).all()
    
    calorie_logs = db.query(CalorieLog).filter(
        CalorieLog.user_id == user_id
    ).order_by(CalorieLog.date.desc()).limit(30).all()
    
    exercise_logs = db.query(ExerciseLog).filter(
        ExerciseLog.user_id == user_id
    ).order_by(ExerciseLog.date.desc()).limit(30).all()
    
    hydration_logs = db.query(HydrationLog).filter(
        HydrationLog.user_id == user_id
    ).order_by(HydrationLog.date.desc()).limit(7).all()
    
    # Prepare data structures
    historical_data = {
        "weight_logs": [{"date": log.date, "weight": log.weight} for log in weight_logs],
        "calorie_logs": [{"date": log.date, "calories": log.calories} for log in calorie_logs],
        "exercise_logs": [
            {"date": log.date, "duration_minutes": log.duration_minutes, 
             "exercise_name": log.exercise_name} 
            for log in exercise_logs
        ],
        "hydration_logs": [{"date": log.date, "glasses": log.glasses} for log in hydration_logs]
    }
    
    # Calculate BMR
    bmr = calculate_bmr(user.age, user.gender, user.weight, user.height)
    
    user_data = {
        "bmr": bmr,
        "age": user.age,
        "gender": user.gender,
        "weight": user.weight,
        "height": user.height,
        "activity_level": user.activity_level,
        "health_goal": user.health_goal,
        "food_preferences": user.food_preferences
    }
    
    # Get comprehensive predictions
    predictions = get_comprehensive_predictions(user_data, historical_data)
    
    # Calculate success probability
    engine = PredictionEngine()
    adherence_data = {
        "exercise_adherence": predictions['exercise_adherence']['adherence_rate'],
        "diet_adherence": 75,  # Default estimate
        "logging_consistency": (len(weight_logs) / 30) * 100 if len(weight_logs) > 0 else 0
    }
    
    success_prediction = engine.predict_success_probability(user_data, adherence_data)
    
    return {
        "user_id": user_id,
        "user_profile": {
            "age": user.age,
            "gender": user.gender,
            "weight": user.weight,
            "height": user.height,
            "goal": user.health_goal,
            "bmr": bmr
        },
        "predictions": predictions,
        "success_prediction": success_prediction,
        "generated_at": datetime.now().isoformat()
    }


@app.get("/recommendations/{user_id}")
def get_smart_recommendations(user_id: int, db: Session = Depends(get_db)):
    """
    Get AI-like smart recommendations without using LLM
    Provides actionable insights based on data analysis
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get recent data
    recent_weight = db.query(WeightLog).filter(
        WeightLog.user_id == user_id
    ).order_by(WeightLog.date.desc()).limit(14).all()
    
    recent_exercise = db.query(ExerciseLog).filter(
        ExerciseLog.user_id == user_id
    ).order_by(ExerciseLog.date.desc()).limit(7).all()
    
    recommendations = []
    
    # Weight-based recommendations
    if len(recent_weight) >= 7:
        weights = [log.weight for log in recent_weight]
        weight_change = weights[0] - weights[-1]
        
        if abs(weight_change) < 0.2:
            recommendations.append({
                "category": "Weight Management",
                "priority": "high",
                "title": "Potential Plateau Detected",
                "message": "Your weight hasn't changed much in the past week. Consider:",
                "actions": [
                    "Adjust calorie intake by 100-200 calories",
                    "Try a new exercise routine",
                    "Review your meal portions",
                    "Ensure you're drinking enough water"
                ]
            })
        elif weight_change < -1.0:
            recommendations.append({
                "category": "Weight Management",
                "priority": "medium",
                "title": "Rapid Weight Loss",
                "message": "You're losing weight quickly. While this is progress, consider:",
                "actions": [
                    "Ensure you're meeting minimum calorie needs",
                    "Focus on nutrient-dense foods",
                    "Monitor energy levels",
                    "Consider slightly increasing calories"
                ]
            })
    
    # Exercise-based recommendations
    exercise_days = len(set(log.date for log in recent_exercise))
    if exercise_days < 3:
        recommendations.append({
            "category": "Exercise",
            "priority": "high",
            "title": "Increase Activity Level",
            "message": f"You exercised {exercise_days} days this week. Aim for at least 3-4 days.",
            "actions": [
                "Start with 20-minute walks",
                "Schedule workouts in your calendar",
                "Find an exercise buddy",
                "Try a new activity you enjoy"
            ]
        })
    elif exercise_days >= 5:
        recommendations.append({
            "category": "Exercise",
            "priority": "low",
            "title": "Excellent Consistency!",
            "message": "You're exercising regularly. Great job!",
            "actions": [
                "Consider progressive overload",
                "Vary your workout routine",
                "Ensure adequate rest days",
                "Track strength improvements"
            ]
        })
    
    # Hydration recommendation
    recent_hydration = db.query(func.sum(HydrationLog.glasses)).filter(
        HydrationLog.user_id == user_id,
        HydrationLog.date == date.today()
    ).scalar() or 0
    
    if recent_hydration < 6:
        recommendations.append({
            "category": "Hydration",
            "priority": "medium",
            "title": "Increase Water Intake",
            "message": f"You've logged {recent_hydration} glasses today. Aim for 8-10.",
            "actions": [
                "Set hourly water reminders",
                "Keep a water bottle nearby",
                "Drink a glass with each meal",
                "Track your daily intake"
            ]
        })
    
    # General wellness
    recommendations.append({
        "category": "Wellness",
        "priority": "low",
        "title": "Consistency is Key",
        "message": "Focus on sustainable habits for long-term success",
        "actions": [
            "Log your progress daily",
            "Celebrate small wins",
            "Don't aim for perfection",
            "Stay patient with the process"
        ]
    })
    
    return {
        "user_id": user_id,
        "recommendations": recommendations,
        "total_recommendations": len(recommendations),
        "generated_at": datetime.now().isoformat()
    }
