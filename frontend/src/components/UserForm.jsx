import React, { useState } from 'react';
import { generatePlan } from '../api/api';

const UserForm = ({ onPlanGenerated }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    age: '',
    gender: 'male',
    height: '',
    weight: '',
    activity_level: 'moderately_active',
    health_goal: 'maintenance',
    food_preferences: '',
    allergies: '',
    medical_conditions: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    // Convert numeric fields
    const processedData = {
      ...formData,
      age: parseInt(formData.age),
      height: parseFloat(formData.height),
      weight: parseFloat(formData.weight)
    };

    try {
      const result = await generatePlan(processedData);
      onPlanGenerated(result);
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'Failed to generate plan. Please check if the backend is running and try again.'
      );
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Loading State */}
      {loading && (
        <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-8 text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-blue-600 font-semibold text-lg">
            Generating your personalized plan...
          </p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-6">
          <h3 className="text-red-800 font-bold text-lg mb-2">Error</h3>
          <p className="text-red-600">{error}</p>
          <button
            onClick={() => setError(null)}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Dismiss
          </button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Your Profile</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Age */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Age *
          </label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            required
            min="10"
            max="100"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="25"
          />
        </div>

        {/* Gender */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Gender *
          </label>
          <select
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        {/* Height */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Height (cm) *
          </label>
          <input
            type="number"
            name="height"
            value={formData.height}
            onChange={handleChange}
            required
            min="100"
            max="250"
            step="0.1"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="175"
          />
        </div>

        {/* Weight */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Weight (kg) *
          </label>
          <input
            type="number"
            name="weight"
            value={formData.weight}
            onChange={handleChange}
            required
            min="30"
            max="300"
            step="0.1"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="70"
          />
        </div>

        {/* Activity Level */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Activity Level *
          </label>
          <select
            name="activity_level"
            value={formData.activity_level}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="sedentary">Sedentary (little/no exercise)</option>
            <option value="lightly_active">Lightly Active (1-3 days/week)</option>
            <option value="moderately_active">Moderately Active (3-5 days/week)</option>
            <option value="very_active">Very Active (6-7 days/week)</option>
            <option value="extremely_active">Extremely Active (athlete)</option>
          </select>
        </div>

        {/* Health Goal */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Health Goal *
          </label>
          <select
            name="health_goal"
            value={formData.health_goal}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="weight_loss">Weight Loss</option>
            <option value="maintenance">Maintenance</option>
            <option value="muscle_gain">Muscle Gain</option>
            <option value="endurance">Endurance</option>
          </select>
        </div>

        {/* Food Preferences */}
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Food Preferences *
          </label>
          <input
            type="text"
            name="food_preferences"
            value={formData.food_preferences}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., Vegetarian, Vegan, Keto, Mediterranean, No preference"
          />
        </div>

        {/* Allergies */}
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Allergies (Optional)
          </label>
          <input
            type="text"
            name="allergies"
            value={formData.allergies}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., Nuts, Dairy, Gluten"
          />
        </div>

        {/* Medical Conditions */}
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Medical Conditions (Optional)
          </label>
          <input
            type="text"
            name="medical_conditions"
            value={formData.medical_conditions}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., Diabetes, Hypertension, None"
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className={`mt-6 w-full py-3 px-6 rounded-lg font-semibold text-white transition-colors ${
          loading 
            ? 'bg-gray-400 cursor-not-allowed' 
            : 'bg-primary-600 hover:bg-primary-700'
        }`}
      >
        {loading ? 'Generating Your Plan...' : 'Generate My Plan'}
      </button>
    </form>
    </>
  );
};

export default UserForm;
