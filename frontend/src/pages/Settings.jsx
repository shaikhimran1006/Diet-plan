import { useState, useEffect } from 'react';
import { User, Target, Droplet, Bell, Save, Loader } from 'lucide-react';
import axios from 'axios';

const Settings = ({ userId = 1 }) => {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);
  
  const [profile, setProfile] = useState({
    age: 25,
    gender: 'male',
    height: 175,
    weight: 70,
    activity_level: 'moderate'
  });

  const [goals, setGoals] = useState({
    daily_calories: 2000,
    protein: 150,
    carbs: 200,
    fats: 65,
    hydration_goal: 8
  });

  const [notifications, setNotifications] = useState({
    meal_reminders: true,
    hydration_alerts: true,
    exercise_reminders: false,
    weekly_summary: true
  });

  // Fetch user data on mount
  useEffect(() => {
    fetchUserData();
  }, [userId]);

  const fetchUserData = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/user/${userId}`);
      const userData = response.data;
      
      setProfile({
        age: userData.age,
        gender: userData.gender,
        height: userData.height,
        weight: userData.weight,
        activity_level: userData.activity_level
      });
      
      // Calculate goals based on user data
      const bmrResponse = await axios.get(`http://localhost:8000/predictions/calories/${userId}`);
      if (bmrResponse.data.prediction) {
        setGoals({
          ...goals,
          daily_calories: bmrResponse.data.prediction.recommended_calories
        });
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
      setMessage({ type: 'error', text: 'Could not load user data. Using defaults.' });
    } finally {
      setLoading(false);
    }
  };

  const handleProfileChange = (field, value) => {
    setProfile({ ...profile, [field]: value });
  };

  const handleGoalChange = (field, value) => {
    setGoals({ ...goals, [field]: value });
  };

  const handleNotificationChange = (field) => {
    setNotifications({ ...notifications, [field]: !notifications[field] });
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage(null);
    
    try {
      // Save profile to backend
      const response = await axios.put(`http://localhost:8000/user/${userId}`, {
        age: parseInt(profile.age),
        gender: profile.gender,
        height: parseFloat(profile.height),
        weight: parseFloat(profile.weight),
        activity_level: profile.activity_level,
        health_goal: 'weight_loss', // Get from state if needed
        food_preferences: '',
        allergies: null,
        medical_conditions: null
      });
      
      setMessage({ 
        type: 'success', 
        text: `Settings saved! New BMR: ${Math.round(response.data.updated_metrics.bmr)} cal, Recommended: ${response.data.updated_metrics.daily_calories} cal/day`
      });
      
      // Update goals with new calculated values
      setGoals({
        ...goals,
        daily_calories: response.data.updated_metrics.daily_calories
      });
      
    } catch (error) {
      console.error('Error saving settings:', error);
      setMessage({ 
        type: 'error', 
        text: 'Failed to save settings. Please try again.' 
      });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <Loader className="animate-spin h-12 w-12 text-primary-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading your settings...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1">Manage your profile and preferences</p>
      </div>

      {/* Success/Error Message */}
      {message && (
        <div className={`p-4 rounded-lg ${
          message.type === 'success' 
            ? 'bg-green-50 text-green-800 border border-green-200' 
            : 'bg-red-50 text-red-800 border border-red-200'
        }`}>
          <p className="font-medium">{message.text}</p>
        </div>
      )}

      {/* Profile Settings */}
      <div className="card">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-primary-50 rounded-lg">
            <User className="h-6 w-6 text-primary-600" />
          </div>
          <h2 className="text-xl font-bold text-gray-900">Profile Information</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Age</label>
            <input
              type="number"
              value={profile.age}
              onChange={(e) => handleProfileChange('age', parseInt(e.target.value))}
              className="input-field"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
            <select
              value={profile.gender}
              onChange={(e) => handleProfileChange('gender', e.target.value)}
              className="input-field"
            >
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Height (cm)</label>
            <input
              type="number"
              value={profile.height}
              onChange={(e) => handleProfileChange('height', parseFloat(e.target.value))}
              className="input-field"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Weight (kg)</label>
            <input
              type="number"
              value={profile.weight}
              onChange={(e) => handleProfileChange('weight', parseFloat(e.target.value))}
              className="input-field"
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Activity Level</label>
            <select
              value={profile.activity_level}
              onChange={(e) => handleProfileChange('activity_level', e.target.value)}
              className="input-field"
            >
              <option value="sedentary">Sedentary (little or no exercise)</option>
              <option value="light">Light (exercise 1-3 times/week)</option>
              <option value="moderate">Moderate (exercise 4-5 times/week)</option>
              <option value="active">Active (daily exercise or intense exercise 3-4 times/week)</option>
              <option value="very_active">Very Active (intense exercise 6-7 times/week)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Goals Settings */}
      <div className="card">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-accent-50 rounded-lg">
            <Target className="h-6 w-6 text-accent-600" />
          </div>
          <h2 className="text-xl font-bold text-gray-900">Daily Goals</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Daily Calories</label>
            <input
              type="number"
              value={goals.daily_calories}
              onChange={(e) => handleGoalChange('daily_calories', parseInt(e.target.value))}
              className="input-field"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Protein (g)</label>
            <input
              type="number"
              value={goals.protein}
              onChange={(e) => handleGoalChange('protein', parseInt(e.target.value))}
              className="input-field"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Carbs (g)</label>
            <input
              type="number"
              value={goals.carbs}
              onChange={(e) => handleGoalChange('carbs', parseInt(e.target.value))}
              className="input-field"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Fats (g)</label>
            <input
              type="number"
              value={goals.fats}
              onChange={(e) => handleGoalChange('fats', parseInt(e.target.value))}
              className="input-field"
            />
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center gap-3 mb-4">
            <Droplet className="h-5 w-5 text-secondary-600" />
            <label className="block text-sm font-medium text-gray-700">Hydration Goal (glasses/day)</label>
          </div>
          <input
            type="number"
            value={goals.hydration_goal}
            onChange={(e) => handleGoalChange('hydration_goal', parseInt(e.target.value))}
            className="input-field max-w-xs"
          />
        </div>
      </div>

      {/* Notifications */}
      <div className="card">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-secondary-50 rounded-lg">
            <Bell className="h-6 w-6 text-secondary-600" />
          </div>
          <h2 className="text-xl font-bold text-gray-900">Notifications</h2>
        </div>

        <div className="space-y-4">
          {[
            { key: 'meal_reminders', label: 'Meal Reminders', desc: 'Get notified for breakfast, lunch, and dinner' },
            { key: 'hydration_alerts', label: 'Hydration Alerts', desc: 'Reminders to drink water throughout the day' },
            { key: 'exercise_reminders', label: 'Exercise Reminders', desc: 'Daily motivation to stay active' },
            { key: 'weekly_summary', label: 'Weekly Summary', desc: 'Receive your weekly progress report' }
          ].map((item) => (
            <div key={item.key} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <p className="font-medium text-gray-900">{item.label}</p>
                <p className="text-sm text-gray-600">{item.desc}</p>
              </div>
              <button
                onClick={() => handleNotificationChange(item.key)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  notifications[item.key] ? 'bg-primary-500' : 'bg-gray-300'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    notifications[item.key] ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button 
          onClick={handleSave}
          disabled={saving}
          className={`btn-primary flex items-center gap-2 ${saving ? 'opacity-75 cursor-not-allowed' : ''}`}
        >
          {saving ? (
            <>
              <Loader className="h-5 w-5 animate-spin" />
              Saving...
            </>
          ) : (
            <>
              <Save className="h-5 w-5" />
              Save Changes
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default Settings;
