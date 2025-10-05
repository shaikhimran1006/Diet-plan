"""
Prediction Engine - Intelligent Recommendations without AI/LLM
Uses statistical analysis, pattern matching, and rule-based predictions
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
from collections import defaultdict


class PredictionEngine:
    """
    Smart prediction engine that analyzes user data to make intelligent recommendations
    Uses mathematical models, statistical analysis, and pattern recognition
    """
    
    def __init__(self):
        # Weight prediction models
        self.weight_trend_window = 14  # days to analyze
        self.calorie_adjustment_factor = 7700  # calories per kg (scientific constant)
        
    def predict_weight_trend(self, weight_history: List[Dict]) -> Dict:
        """
        Predict future weight based on historical data using linear regression
        Returns prediction for next 7, 14, and 30 days
        """
        if not weight_history or len(weight_history) < 3:
            return {
                "trend": "insufficient_data",
                "predictions": {},
                "confidence": 0,
                "weekly_change": 0
            }
        
        # Sort by date
        sorted_history = sorted(weight_history, key=lambda x: x['date'])
        
        # Calculate trend (simple linear regression)
        n = len(sorted_history)
        weights = [entry['weight'] for entry in sorted_history]
        
        # Calculate average weekly change
        if n >= 2:
            first_weight = weights[0]
            last_weight = weights[-1]
            days_span = (sorted_history[-1]['date'] - sorted_history[0]['date']).days
            
            if days_span > 0:
                daily_change = (last_weight - first_weight) / days_span
                weekly_change = daily_change * 7
            else:
                weekly_change = 0
        else:
            weekly_change = 0
        
        # Determine trend
        if abs(weekly_change) < 0.1:
            trend = "stable"
        elif weekly_change < 0:
            trend = "decreasing"
        else:
            trend = "increasing"
        
        # Predict future weights
        current_weight = weights[-1]
        predictions = {
            "7_days": round(current_weight + (daily_change * 7), 1),
            "14_days": round(current_weight + (daily_change * 14), 1),
            "30_days": round(current_weight + (daily_change * 30), 1)
        }
        
        # Calculate confidence based on data consistency
        variance = sum((w - sum(weights)/n)**2 for w in weights) / n
        confidence = max(0, min(100, 100 - (variance * 10)))
        
        return {
            "trend": trend,
            "weekly_change": round(weekly_change, 2),
            "predictions": predictions,
            "confidence": round(confidence, 1),
            "current_weight": current_weight
        }
    
    def predict_calorie_needs(self, user_data: Dict, weight_history: List[Dict], 
                            calorie_logs: List[Dict]) -> Dict:
        """
        Predict optimal calorie intake based on goals and actual progress
        Adjusts recommendations based on real results
        """
        # Get weight trend
        weight_trend = self.predict_weight_trend(weight_history)
        
        # Get current BMR (should be passed or calculated)
        current_bmr = user_data.get('bmr', 1500)
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        activity = user_data.get('activity_level', 'moderate')
        tdee = current_bmr * activity_multipliers.get(activity, 1.55)
        
        # Adjust based on goal
        goal = user_data.get('health_goal', 'maintenance')
        goal_adjustments = {
            'weight_loss': -500,  # 0.5 kg per week
            'aggressive_loss': -750,  # 0.75 kg per week
            'muscle_gain': +300,
            'maintenance': 0,
            'endurance': +200
        }
        
        base_calories = tdee + goal_adjustments.get(goal, 0)
        
        # Analyze actual progress vs expected
        if weight_trend['trend'] != 'insufficient_data':
            weekly_change = weight_trend['weekly_change']
            
            # If losing weight too fast or slow, adjust
            if goal == 'weight_loss':
                target_loss = -0.5  # kg per week
                difference = weekly_change - target_loss
                
                # If losing too slowly, reduce calories more
                if difference > 0.2:
                    adjustment = -100
                # If losing too fast, increase slightly
                elif difference < -0.2:
                    adjustment = +100
                else:
                    adjustment = 0
            elif goal == 'muscle_gain':
                target_gain = 0.25  # kg per week
                difference = weekly_change - target_gain
                
                if difference < -0.1:
                    adjustment = +150
                elif difference > 0.3:
                    adjustment = -50
                else:
                    adjustment = 0
            else:
                adjustment = 0
        else:
            adjustment = 0
        
        predicted_calories = int(base_calories + adjustment)
        
        return {
            "current_tdee": round(tdee),
            "recommended_calories": predicted_calories,
            "adjustment": adjustment,
            "reason": self._get_adjustment_reason(adjustment, goal),
            "weekly_target": goal_adjustments.get(goal, 0) / 1100  # kg change
        }
    
    def predict_meal_preferences(self, user_data: Dict, meal_history: List[Dict]) -> Dict:
        """
        Predict preferred meal types and timing based on past plans
        """
        preferences = {
            "preferred_proteins": [],
            "preferred_carbs": [],
            "meal_timing": {},
            "portion_preferences": {}
        }
        
        # Analyze food preferences from user input
        food_pref = user_data.get('food_preferences', '').lower()
        
        if 'vegetarian' in food_pref:
            preferences['preferred_proteins'] = ['tofu', 'tempeh', 'legumes', 'eggs', 'greek yogurt']
        elif 'vegan' in food_pref:
            preferences['preferred_proteins'] = ['tofu', 'tempeh', 'legumes', 'quinoa']
        else:
            preferences['preferred_proteins'] = ['chicken', 'fish', 'turkey', 'eggs', 'beef']
        
        if 'low carb' in food_pref or 'keto' in food_pref:
            preferences['preferred_carbs'] = ['cauliflower', 'zucchini', 'spinach']
        else:
            preferences['preferred_carbs'] = ['brown rice', 'sweet potato', 'oats', 'quinoa']
        
        return preferences
    
    def predict_exercise_adherence(self, exercise_logs: List[Dict]) -> Dict:
        """
        Predict likelihood of exercise completion based on patterns
        """
        if not exercise_logs:
            return {
                "adherence_rate": 0,
                "best_time": "morning",
                "preferred_duration": 30,
                "recommendation": "Start with short sessions"
            }
        
        # Calculate adherence
        total_days = 7  # week
        actual_days = len(set(log['date'] for log in exercise_logs))
        adherence_rate = (actual_days / total_days) * 100
        
        # Find preferred time (if timestamp available)
        durations = [log.get('duration_minutes', 30) for log in exercise_logs]
        avg_duration = sum(durations) / len(durations) if durations else 30
        
        # Generate recommendation
        if adherence_rate > 80:
            recommendation = "Excellent consistency! Consider increasing intensity"
        elif adherence_rate > 50:
            recommendation = "Good progress! Try to add one more session"
        else:
            recommendation = "Start small - aim for 3 days per week"
        
        return {
            "adherence_rate": round(adherence_rate, 1),
            "best_time": "morning",  # Default recommendation
            "preferred_duration": round(avg_duration),
            "recommendation": recommendation
        }
    
    def predict_hydration_needs(self, user_data: Dict, activity_level: str) -> Dict:
        """
        Calculate recommended water intake based on weight and activity
        """
        weight = user_data.get('weight', 70)  # kg
        
        # Base formula: 30-35 ml per kg of body weight
        base_water = weight * 35  # ml
        
        # Adjust for activity
        activity_adjustments = {
            'sedentary': 0,
            'light': 250,
            'moderate': 500,
            'active': 750,
            'very_active': 1000
        }
        
        adjustment = activity_adjustments.get(activity_level, 500)
        total_ml = base_water + adjustment
        
        # Convert to glasses (250ml per glass)
        glasses = round(total_ml / 250)
        
        return {
            "daily_ml": round(total_ml),
            "daily_glasses": glasses,
            "timing": self._get_hydration_timing(glasses)
        }
    
    def predict_macro_distribution(self, goal: str, current_performance: Dict) -> Dict:
        """
        Predict optimal macro distribution based on goal and progress
        """
        # Base distributions by goal
        distributions = {
            'weight_loss': {'protein': 35, 'carbs': 35, 'fats': 30},
            'muscle_gain': {'protein': 30, 'carbs': 45, 'fats': 25},
            'maintenance': {'protein': 25, 'carbs': 45, 'fats': 30},
            'endurance': {'protein': 20, 'carbs': 55, 'fats': 25}
        }
        
        base_dist = distributions.get(goal, distributions['maintenance'])
        
        # Adjust based on performance (if data available)
        if current_performance:
            energy_level = current_performance.get('energy_level', 'normal')
            
            if energy_level == 'low' and goal != 'weight_loss':
                # Increase carbs for energy
                base_dist['carbs'] += 5
                base_dist['fats'] -= 5
        
        return base_dist
    
    def predict_optimal_meal_timing(self, user_data: Dict) -> Dict:
        """
        Predict best meal timing based on activity level and goals
        """
        activity = user_data.get('activity_level', 'moderate')
        goal = user_data.get('health_goal', 'maintenance')
        
        if goal == 'muscle_gain':
            return {
                "breakfast": "07:00 AM",
                "snack_1": "10:00 AM",
                "lunch": "12:30 PM",
                "snack_2": "03:30 PM",
                "dinner": "06:30 PM",
                "post_workout": "Within 30 min after exercise",
                "note": "Frequent meals support muscle growth"
            }
        elif goal == 'weight_loss':
            return {
                "breakfast": "08:00 AM",
                "lunch": "01:00 PM",
                "snack": "04:00 PM",
                "dinner": "07:00 PM",
                "note": "3 meals + 1 snack for satiety"
            }
        else:
            return {
                "breakfast": "07:30 AM",
                "lunch": "12:30 PM",
                "snack": "03:30 PM",
                "dinner": "07:00 PM",
                "note": "Balanced timing for steady energy"
            }
    
    def predict_plateau_risk(self, weight_history: List[Dict], 
                            calorie_logs: List[Dict]) -> Dict:
        """
        Predict if user is approaching a weight plateau
        """
        if len(weight_history) < 14:
            return {
                "risk_level": "unknown",
                "recommendation": "Need more data to assess plateau risk"
            }
        
        # Analyze last 14 days
        recent = sorted(weight_history, key=lambda x: x['date'])[-14:]
        weights = [entry['weight'] for entry in recent]
        
        # Calculate variance in recent weights
        avg_weight = sum(weights) / len(weights)
        variance = sum((w - avg_weight)**2 for w in weights) / len(weights)
        
        # Low variance = potential plateau
        if variance < 0.5:  # Less than 0.5kg variance
            risk_level = "high"
            recommendation = "Consider calorie cycling or changing workout routine"
        elif variance < 1.0:
            risk_level = "moderate"
            recommendation = "Monitor closely, may need adjustments soon"
        else:
            risk_level = "low"
            recommendation = "Good progress, continue current plan"
        
        return {
            "risk_level": risk_level,
            "recommendation": recommendation,
            "variance": round(variance, 2)
        }
    
    def predict_success_probability(self, user_data: Dict, 
                                   adherence_data: Dict) -> Dict:
        """
        Predict probability of reaching goal based on current adherence
        """
        # Calculate adherence score
        factors = []
        
        # Exercise adherence
        exercise_rate = adherence_data.get('exercise_adherence', 0)
        factors.append(min(exercise_rate / 100, 1.0))
        
        # Diet adherence (if available)
        diet_rate = adherence_data.get('diet_adherence', 70)  # default 70%
        factors.append(min(diet_rate / 100, 1.0))
        
        # Consistency (weight logging)
        logging_rate = adherence_data.get('logging_consistency', 50)
        factors.append(min(logging_rate / 100, 1.0))
        
        # Calculate overall probability
        if factors:
            probability = (sum(factors) / len(factors)) * 100
        else:
            probability = 50  # neutral
        
        # Generate insight
        if probability > 80:
            insight = "Excellent! You're on track to reach your goal"
        elif probability > 60:
            insight = "Good progress! Small improvements will help"
        elif probability > 40:
            insight = "Need more consistency to reach your goal"
        else:
            insight = "Consider reassessing your approach"
        
        return {
            "success_probability": round(probability, 1),
            "insight": insight,
            "key_factors": self._identify_key_factors(adherence_data)
        }
    
    # Helper methods
    
    def _get_adjustment_reason(self, adjustment: int, goal: str) -> str:
        """Get human-readable reason for calorie adjustment"""
        if adjustment == 0:
            return "Progress is on track"
        elif adjustment > 0:
            if goal == 'weight_loss':
                return "Losing weight too quickly - slightly increasing calories"
            else:
                return "Not gaining enough - increasing calories"
        else:
            if goal == 'weight_loss':
                return "Progress slower than expected - reducing calories"
            else:
                return "Gaining too fast - slightly reducing calories"
    
    def _get_hydration_timing(self, total_glasses: int) -> List[str]:
        """Generate hydration timing recommendations"""
        timings = []
        if total_glasses >= 1:
            timings.append("Upon waking: 1-2 glasses")
        if total_glasses >= 3:
            timings.append("Before lunch: 1 glass")
        if total_glasses >= 5:
            timings.append("Afternoon: 1-2 glasses")
        if total_glasses >= 7:
            timings.append("With dinner: 1 glass")
        if total_glasses >= 8:
            timings.append("Evening: 1 glass")
        return timings
    
    def _identify_key_factors(self, adherence_data: Dict) -> List[str]:
        """Identify which factors need improvement"""
        factors = []
        
        exercise = adherence_data.get('exercise_adherence', 0)
        diet = adherence_data.get('diet_adherence', 0)
        logging = adherence_data.get('logging_consistency', 0)
        
        if exercise < 60:
            factors.append("Increase exercise frequency")
        if diet < 70:
            factors.append("Improve diet adherence")
        if logging < 50:
            factors.append("Log progress more consistently")
        
        if not factors:
            factors.append("Maintain current excellent habits")
        
        return factors


# Prediction API functions
def get_weight_prediction(weight_history: List[Dict]) -> Dict:
    """Wrapper function for weight prediction"""
    engine = PredictionEngine()
    return engine.predict_weight_trend(weight_history)


def get_calorie_prediction(user_data: Dict, weight_history: List[Dict], 
                          calorie_logs: List[Dict]) -> Dict:
    """Wrapper function for calorie prediction"""
    engine = PredictionEngine()
    return engine.predict_calorie_needs(user_data, weight_history, calorie_logs)


def get_comprehensive_predictions(user_data: Dict, historical_data: Dict) -> Dict:
    """
    Get all predictions in one call
    """
    engine = PredictionEngine()
    
    weight_history = historical_data.get('weight_logs', [])
    calorie_logs = historical_data.get('calorie_logs', [])
    exercise_logs = historical_data.get('exercise_logs', [])
    
    return {
        "weight_prediction": engine.predict_weight_trend(weight_history),
        "calorie_prediction": engine.predict_calorie_needs(
            user_data, weight_history, calorie_logs
        ),
        "hydration_needs": engine.predict_hydration_needs(
            user_data, user_data.get('activity_level', 'moderate')
        ),
        "exercise_adherence": engine.predict_exercise_adherence(exercise_logs),
        "meal_timing": engine.predict_optimal_meal_timing(user_data),
        "plateau_risk": engine.predict_plateau_risk(weight_history, calorie_logs),
        "macro_distribution": engine.predict_macro_distribution(
            user_data.get('health_goal', 'maintenance'), {}
        )
    }
