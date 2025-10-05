import React from 'react';

const PlanResults = ({ plan }) => {
  if (!plan) return null;

  return (
    <div className="space-y-6">
      {/* Header with BMR and Calories */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg shadow-lg p-6 text-white">
        <h2 className="text-3xl font-bold mb-4">Your Personalized Plan</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-blue-200 text-sm">Basal Metabolic Rate (BMR)</p>
            <p className="text-3xl font-bold">{plan.bmr.toFixed(0)} kcal</p>
          </div>
          <div>
            <p className="text-blue-200 text-sm">Daily Calorie Target</p>
            <p className="text-3xl font-bold">{plan.daily_calories} kcal</p>
          </div>
        </div>
      </div>

      {/* Macronutrients */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <span className="text-2xl mr-2">📊</span>
          Macronutrient Breakdown
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-red-50 p-4 rounded-lg border border-red-200">
            <p className="text-red-600 font-semibold text-sm">Protein</p>
            <p className="text-2xl font-bold text-red-700">{plan.macros.protein}</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
            <p className="text-yellow-600 font-semibold text-sm">Carbs</p>
            <p className="text-2xl font-bold text-yellow-700">{plan.macros.carbs}</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg border border-green-200">
            <p className="text-green-600 font-semibold text-sm">Fats</p>
            <p className="text-2xl font-bold text-green-700">{plan.macros.fats}</p>
          </div>
        </div>
      </div>

      {/* Meal Plan */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <span className="text-2xl mr-2">🍽️</span>
          Your Meal Plan
        </h3>
        <div className="space-y-4">
          <div className="border-l-4 border-orange-500 pl-4 py-2">
            <h4 className="font-bold text-orange-600 mb-1">Breakfast</h4>
            <p className="text-gray-700">{plan.meal_plan.breakfast}</p>
          </div>
          <div className="border-l-4 border-green-500 pl-4 py-2">
            <h4 className="font-bold text-green-600 mb-1">Lunch</h4>
            <p className="text-gray-700">{plan.meal_plan.lunch}</p>
          </div>
          <div className="border-l-4 border-blue-500 pl-4 py-2">
            <h4 className="font-bold text-blue-600 mb-1">Dinner</h4>
            <p className="text-gray-700">{plan.meal_plan.dinner}</p>
          </div>
          <div className="border-l-4 border-purple-500 pl-4 py-2">
            <h4 className="font-bold text-purple-600 mb-1">Snacks</h4>
            <p className="text-gray-700">{plan.meal_plan.snacks}</p>
          </div>
        </div>
      </div>

      {/* Exercise Recommendations */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <span className="text-2xl mr-2">💪</span>
          Exercise Recommendations
        </h3>
        <ul className="space-y-2">
          {plan.exercises.map((exercise, index) => (
            <li key={index} className="flex items-start">
              <span className="bg-blue-100 text-blue-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5 flex-shrink-0">
                {index + 1}
              </span>
              <span className="text-gray-700">{exercise}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Grocery List */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <span className="text-2xl mr-2">🛒</span>
          Grocery List
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {plan.grocery_list.map((item, index) => (
            <div key={index} className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              <span className="text-gray-700">{item}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Timestamp */}
      <div className="text-center text-sm text-gray-500">
        Generated on {new Date(plan.created_at).toLocaleString()}
      </div>
    </div>
  );
};

export default PlanResults;
