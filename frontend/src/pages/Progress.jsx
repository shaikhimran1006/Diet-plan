import { useState, useEffect } from 'react';
import { 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from 'recharts';
import { TrendingUp, Droplet, Flame, Dumbbell, Calendar, Loader, RefreshCw } from 'lucide-react';
import { format, subDays } from 'date-fns';
import axios from 'axios';

const Progress = ({ userId = 1 }) => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [weightData, setWeightData] = useState([]);
  const [calorieData, setCalorieData] = useState([]);
  const [hydrationData, setHydrationData] = useState([]);
  const [exerciseData, setExerciseData] = useState([]);

  useEffect(() => {
    fetchProgressData();
  }, [userId]);

  const fetchProgressData = async (showRefreshing = false) => {
    if (showRefreshing) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }

    try {
      // Fetch weight logs
      const weightResponse = await axios.get(`http://localhost:8000/weight-log/${userId}`);
      const weights = weightResponse.data
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(-7)
        .map(log => ({
          date: format(new Date(log.date), 'MMM d'),
          weight: log.weight
        }));
      setWeightData(weights);

      // Fetch user profile for calorie goal
      const profileResponse = await axios.get(`http://localhost:8000/user/${userId}`);
      const predictionResponse = await axios.get(`http://localhost:8000/predictions/calories/${userId}`);
      const calorieGoal = predictionResponse.data.prediction?.recommended_calories || 2000;

      // Fetch calorie logs for last 7 days
      const calorieResponse = await axios.get(`http://localhost:8000/calorie-log/${userId}`);
      const last7Days = Array.from({ length: 7 }, (_, i) => {
        const date = subDays(new Date(), 6 - i);
        const dateStr = format(date, 'yyyy-MM-dd');
        const dayLogs = calorieResponse.data.filter(log => 
          format(new Date(log.date), 'yyyy-MM-dd') === dateStr
        );
        const consumed = dayLogs.reduce((sum, log) => sum + log.calories_consumed, 0);
        
        return {
          date: format(date, 'EEE'),
          consumed,
          goal: calorieGoal
        };
      });
      setCalorieData(last7Days);

      // Fetch hydration logs for last 7 days
      const hydrationResponse = await axios.get(`http://localhost:8000/hydration-log/${userId}`);
      const hydrationLast7Days = Array.from({ length: 7 }, (_, i) => {
        const date = subDays(new Date(), 6 - i);
        const dateStr = format(date, 'yyyy-MM-dd');
        const dayLogs = hydrationResponse.data.filter(log => 
          format(new Date(log.date), 'yyyy-MM-dd') === dateStr
        );
        const glasses = dayLogs.reduce((sum, log) => sum + log.glasses, 0);
        
        return {
          date: format(date, 'EEE'),
          glasses
        };
      });
      setHydrationData(hydrationLast7Days);

      // Fetch exercise logs for last 7 days
      const exerciseResponse = await axios.get(`http://localhost:8000/exercise-log/${userId}`);
      const exerciseLast7Days = Array.from({ length: 7 }, (_, i) => {
        const date = subDays(new Date(), 6 - i);
        const dateStr = format(date, 'yyyy-MM-dd');
        const dayLogs = exerciseResponse.data.filter(log => 
          format(new Date(log.date), 'yyyy-MM-dd') === dateStr
        );
        const minutes = dayLogs.reduce((sum, log) => sum + log.duration, 0);
        
        return {
          date: format(date, 'EEE'),
          minutes
        };
      });
      setExerciseData(exerciseLast7Days);

    } catch (error) {
      console.error('Error fetching progress data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    fetchProgressData(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <Loader className="animate-spin h-12 w-12 text-primary-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading your progress...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Progress Tracking</h1>
          <p className="text-gray-600 mt-1">Monitor your health journey over time</p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className={`btn-secondary flex items-center gap-2 ${refreshing ? 'opacity-75' : ''}`}
        >
          <RefreshCw className={`h-5 w-5 ${refreshing ? 'animate-spin' : ''}`} />
          {refreshing ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {/* Weight Progress */}
      <div className="card">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-primary-50 rounded-lg">
            <TrendingUp className="h-6 w-6 text-primary-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Weight Progress</h2>
            <p className="text-sm text-gray-600">Recent weight logs</p>
          </div>
        </div>
        {weightData.length > 0 ? (
          <>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={weightData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="date" 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                  domain={['dataMin - 1', 'dataMax + 1']}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="weight" 
                  stroke="#4CAF50" 
                  strokeWidth={3}
                  dot={{ fill: '#4CAF50', r: 5 }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
            <div className="mt-4 p-4 bg-green-50 rounded-lg flex items-center justify-between">
              <span className="text-sm font-medium text-green-800">Total Progress</span>
              <span className="text-lg font-bold text-green-800">
                {weightData.length > 1 ? (weightData[weightData.length - 1].weight - weightData[0].weight).toFixed(1) : '0.0'} kg
              </span>
            </div>
          </>
        ) : (
          <div className="text-center py-12 text-gray-500">
            <TrendingUp className="h-16 w-16 mx-auto mb-3 opacity-30" />
            <p className="font-medium">No weight data yet</p>
            <p className="text-sm">Start logging your weight to track progress!</p>
          </div>
        )}
      </div>

      {/* Calorie Intake */}
      <div className="card">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-accent-50 rounded-lg">
            <Flame className="h-6 w-6 text-accent-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Calorie Intake</h2>
            <p className="text-sm text-gray-600">Last 7 days</p>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={calorieData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="date" 
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'white', 
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Legend />
            <Bar dataKey="consumed" fill="#FF9800" name="Consumed" radius={[8, 8, 0, 0]} />
            <Bar dataKey="goal" fill="#e5e7eb" name="Goal" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Two Column Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Hydration */}
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-secondary-50 rounded-lg">
              <Droplet className="h-6 w-6 text-secondary-600" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-gray-900">Hydration</h2>
              <p className="text-sm text-gray-600">Last 7 days</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={hydrationData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="date" 
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
              />
              <Bar dataKey="glasses" fill="#2196F3" name="Glasses" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Exercise */}
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-purple-50 rounded-lg">
              <Dumbbell className="h-6 w-6 text-purple-600" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-gray-900">Exercise</h2>
              <p className="text-sm text-gray-600">Last 7 days</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={exerciseData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="date" 
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
              />
              <Bar dataKey="minutes" fill="#9333ea" name="Minutes" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Progress;
