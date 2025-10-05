from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import date


class UserInput(BaseModel):
    age: int
    gender: str
    height: float  # cm
    weight: float  # kg
    activity_level: str
    health_goal: str
    food_preferences: str
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None


class MealPlan(BaseModel):
    breakfast: str
    lunch: str
    dinner: str
    snacks: str


class Macros(BaseModel):
    calories: int
    protein: str
    carbs: str
    fats: str


class PlanResponse(BaseModel):
    user_id: int
    bmr: float
    daily_calories: int
    meal_plan: MealPlan
    macros: Macros
    exercises: List[str]
    grocery_list: List[str]
    created_at: str


# Progress Tracking Schemas
class WeightLogCreate(BaseModel):
    weight: float
    notes: Optional[str] = None
    date: Optional[date] = None


class WeightLogResponse(BaseModel):
    id: int
    user_id: int
    weight: float
    date: date
    notes: Optional[str]
    
    class Config:
        from_attributes = True


class HydrationLogCreate(BaseModel):
    glasses: int
    date: Optional[date] = None


class HydrationLogResponse(BaseModel):
    id: int
    user_id: int
    glasses: int
    date: date
    
    class Config:
        from_attributes = True


class CalorieLogCreate(BaseModel):
    calories: int
    meal_type: str
    description: str
    date: Optional[date] = None


class CalorieLogResponse(BaseModel):
    id: int
    user_id: int
    calories: int
    meal_type: str
    description: str
    date: date
    
    class Config:
        from_attributes = True


class ExerciseLogCreate(BaseModel):
    exercise_name: str
    duration_minutes: int
    calories_burned: Optional[int] = None
    date: Optional[date] = None


class ExerciseLogResponse(BaseModel):
    id: int
    user_id: int
    exercise_name: str
    duration_minutes: int
    calories_burned: Optional[int]
    date: date
    
    class Config:
        from_attributes = True


class ProgressStats(BaseModel):
    current_weight: Optional[float]
    weight_change: Optional[float]
    total_hydration_today: int
    total_calories_today: int
    total_exercise_minutes_today: int
    weight_history: List[WeightLogResponse]
    hydration_history: List[HydrationLogResponse]
