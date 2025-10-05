import { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  Droplet, 
  Flame, 
  Dumbbell, 
  Target,
  Plus,
  Calendar,
  Loader
} from 'lucide-react';
import { format, startOfDay, endOfDay } from 'date-fns';
import axios from 'axios';

const Dashboard = ({ userId = 1 }) => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    currentWeight: 0,
    weightChange: 0,
    calorieGoal: 2000,
    caloriesConsumed: 0,
    hydrationGoal: 8,
    hydrationCurrent: 0,
    exerciseMinutes: 0
  });

  const [todayMeals, setTodayMeals] = useState([]);
  const [userProfile, setUserProfile] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, [userId]);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // Fetch user profile
      const profileResponse = await axios.get(`http://localhost:8000/user/${userId}`);
      const profile = profileResponse.data;
      setUserProfile(profile);

      // Fetch weight logs to get current weight and change
      let currentWeight = profile.weight || 0;
      let weightChange = 0;
      
      try {
        const weightResponse = await axios.get(`http://localhost:8000/weight-log/${userId}`);
        const weightLogs = weightResponse.data;
        
        if (weightLogs.length > 0) {
          const sortedWeights = weightLogs.sort((a, b) => 
            new Date(b.date) - new Date(a.date)
          );
          currentWeight = sortedWeights[0].weight;
          
          if (sortedWeights.length > 1) {
            weightChange = sortedWeights[0].weight - sortedWeights[sortedWeights.length - 1].weight;
          }
        }
      } catch (err) {
        console.warn('Could not fetch weight logs:', err);
      }

      // Fetch today's calorie logs
      let caloriesConsumed = 0;
      let meals = [];
      
      try {
        const calorieResponse = await axios.get(`http://localhost:8000/calorie-log/${userId}`);
        const calorieLogs = calorieResponse.data;
        const today = new Date();
        const todayCalories = calorieLogs.filter(log => {
          const logDate = new Date(log.date);
          return logDate.toDateString() === today.toDateString();
        });
        
        caloriesConsumed = todayCalories.reduce((sum, log) => sum + log.calories_consumed, 0);
        
        // Build today's meals from calorie logs
        meals = todayCalories.map(log => ({
          name: log.meal_type ? log.meal_type.charAt(0).toUpperCase() + log.meal_type.slice(1) : 'Meal',
          calories: log.calories_consumed,
          time: format(new Date(log.date), 'hh:mm a')
        }));
      } catch (err) {
        console.warn('Could not fetch calorie logs:', err);
      }

      // Fetch today's hydration logs
      let hydrationCurrent = 0;
      
      try {
        const hydrationResponse = await axios.get(`http://localhost:8000/hydration-log/${userId}`);
        const hydrationLogs = hydrationResponse.data;
        const today = new Date();
        const todayHydration = hydrationLogs.filter(log => {
          const logDate = new Date(log.date);
          return logDate.toDateString() === today.toDateString();
        });
        
        hydrationCurrent = todayHydration.reduce((sum, log) => sum + log.glasses, 0);
      } catch (err) {
        console.warn('Could not fetch hydration logs:', err);
      }

      // Fetch today's exercise logs
      let exerciseMinutes = 0;
      
      try {
        const exerciseResponse = await axios.get(`http://localhost:8000/exercise-log/${userId}`);
        const exerciseLogs = exerciseResponse.data;
        const today = new Date();
        const todayExercise = exerciseLogs.filter(log => {
          const logDate = new Date(log.date);
          return logDate.toDateString() === today.toDateString();
        });
        
        exerciseMinutes = todayExercise.reduce((sum, log) => sum + log.duration, 0);
      } catch (err) {
        console.warn('Could not fetch exercise logs:', err);
      }

      // Get calorie predictions for daily goal (with fallback)
      let dailyCalorieGoal = 2000; // Default fallback
      
      try {
        const predictionResponse = await axios.get(`http://localhost:8000/predictions/calories/${userId}`);
        dailyCalorieGoal = predictionResponse.data.prediction?.recommended_calories || 2000;
      } catch (err) {
        console.warn('Could not fetch calorie predictions, using default:', err);
        // Fallback: calculate basic TDEE from profile
        const bmr = profile.gender === 'male'
          ? 10 * profile.weight + 6.25 * profile.height - 5 * profile.age + 5
          : 10 * profile.weight + 6.25 * profile.height - 5 * profile.age - 161;
        
        const activityMultipliers = {
          sedentary: 1.2,
          light: 1.375,
          moderate: 1.55,
          active: 1.725,
          very_active: 1.9
        };
        
        const tdee = bmr * (activityMultipliers[profile.activity_level] || 1.55);
        dailyCalorieGoal = Math.round(tdee);
      }

      setStats({
        currentWeight,
        weightChange,
        calorieGoal: dailyCalorieGoal,
        caloriesConsumed,
        hydrationGoal: 8,
        hydrationCurrent,
        exerciseMinutes
      });

      setTodayMeals(meals);

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Set default values on error
      setStats({
        currentWeight: 0,
        weightChange: 0,
        calorieGoal: 2000,
        caloriesConsumed: 0,
        hydrationGoal: 8,
        hydrationCurrent: 0,
        exerciseMinutes: 0
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <Loader className="animate-spin h-12 w-12 text-primary-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  const calorieProgress = (stats.caloriesConsumed / stats.calorieGoal) * 100;
  const hydrationProgress = (stats.hydrationCurrent / stats.hydrationGoal) * 100;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1 flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            {format(new Date(), 'EEEE, MMMM d, yyyy')}
          </p>
        </div>
        <button
          onClick={fetchDashboardData}
          className="btn-secondary flex items-center gap-2"
        >
          <Loader className="h-5 w-5" />
          Refresh
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Weight Card */}
        <div className="card card-hover">
          <div className="flex items-start justify-between mb-3">
            <div className="p-2 bg-primary-50 rounded-lg">
              <Target className="h-6 w-6 text-primary-600" />
            </div>
            <div className={`flex items-center gap-1 text-sm font-medium ${
              stats.weightChange < 0 ? 'text-green-600' : 'text-orange-600'
            }`}>
              {stats.weightChange < 0 ? (
                <TrendingDown className="h-4 w-4" />
              ) : (
                <TrendingUp className="h-4 w-4" />
              )}
              {Math.abs(stats.weightChange)} kg
            </div>
          </div>
          <p className="text-gray-600 text-sm mb-1">Current Weight</p>
          <p className="text-3xl font-bold text-gray-900">{stats.currentWeight} <span className="text-lg text-gray-500">kg</span></p>
        </div>

        {/* Calories Card */}
        <div className="card card-hover">
          <div className="flex items-start justify-between mb-3">
            <div className="p-2 bg-accent-50 rounded-lg">
              <Flame className="h-6 w-6 text-accent-600" />
            </div>
            <span className="text-sm font-medium text-gray-600">
              {stats.caloriesConsumed} / {stats.calorieGoal}
            </span>
          </div>
          <p className="text-gray-600 text-sm mb-1">Calories Today</p>
          <div className="progress-bar mt-2">
            <div 
              className="progress-fill" 
              style={{ width: `${Math.min(calorieProgress, 100)}%` }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {stats.calorieGoal - stats.caloriesConsumed} cal remaining
          </p>
        </div>

        {/* Hydration Card */}
        <div className="card card-hover">
          <div className="flex items-start justify-between mb-3">
            <div className="p-2 bg-secondary-50 rounded-lg">
              <Droplet className="h-6 w-6 text-secondary-600" />
            </div>
            <span className="text-sm font-medium text-gray-600">
              {stats.hydrationCurrent} / {stats.hydrationGoal}
            </span>
          </div>
          <p className="text-gray-600 text-sm mb-1">Water Intake</p>
          <div className="progress-bar mt-2">
            <div 
              className="h-full bg-gradient-to-r from-secondary-400 to-secondary-600 transition-all duration-500" 
              style={{ width: `${Math.min(hydrationProgress, 100)}%` }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {stats.hydrationGoal - stats.hydrationCurrent} glasses left
          </p>
        </div>

        {/* Exercise Card */}
        <div className="card card-hover">
          <div className="flex items-start justify-between mb-3">
            <div className="p-2 bg-purple-50 rounded-lg">
              <Dumbbell className="h-6 w-6 text-purple-600" />
            </div>
            <span className="text-sm font-medium text-purple-600">Active</span>
          </div>
          <p className="text-gray-600 text-sm mb-1">Exercise Time</p>
          <p className="text-3xl font-bold text-gray-900">{stats.exerciseMinutes} <span className="text-lg text-gray-500">min</span></p>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Today's Meals */}
        <div className="lg:col-span-2 card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900">Today's Meals</h2>
            <button className="flex items-center gap-2 text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors">
              <Plus className="h-4 w-4" />
              Add Meal
            </button>
          </div>
          <div className="space-y-3">
            {todayMeals.length > 0 ? (
              todayMeals.map((meal, index) => (
                <div 
                  key={index}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white rounded-lg shadow-sm">
                      <Flame className="h-5 w-5 text-accent-600" />
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">{meal.name}</p>
                      <p className="text-sm text-gray-600">{meal.time}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-gray-900">{meal.calories}</p>
                    <p className="text-sm text-gray-600">cal</p>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Flame className="h-12 w-12 mx-auto mb-3 opacity-30" />
                <p className="font-medium">No meals logged today</p>
                <p className="text-sm">Start tracking your meals to see them here!</p>
              </div>
            )}
            <button className="w-full py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-primary-400 hover:text-primary-600 transition-colors font-medium">
              + Log a Meal
            </button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Quick Actions</h2>
          <div className="space-y-3">
            <button className="w-full btn-primary text-left flex items-center justify-between">
              <span>Log Weight</span>
              <Plus className="h-5 w-5" />
            </button>
            <button className="w-full btn-secondary text-left flex items-center justify-between">
              <span>Add Water</span>
              <Droplet className="h-5 w-5" />
            </button>
            <button className="w-full bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 px-6 rounded-lg transition-colors duration-200 text-left flex items-center justify-between">
              <span>Log Exercise</span>
              <Dumbbell className="h-5 w-5" />
            </button>
            <button className="w-full bg-accent-500 hover:bg-accent-600 text-white font-semibold py-2 px-6 rounded-lg transition-colors duration-200 text-left flex items-center justify-between">
              <span>New Diet Plan</span>
              <Target className="h-5 w-5" />
            </button>
          </div>

          {/* Motivation Card */}
          <div className="mt-6 p-4 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg text-white">
            <p className="font-semibold mb-1">💪 Keep Going!</p>
            <p className="text-sm opacity-90">
              You're doing great! Stay consistent with your goals.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
