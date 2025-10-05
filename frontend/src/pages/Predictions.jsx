import { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Zap, 
  Target, 
  Brain,
  AlertCircle,
  CheckCircle,
  TrendingDown,
  Activity,
  RefreshCw
} from 'lucide-react';

const Predictions = ({ userId = 1 }) => {
  const [predictions, setPredictions] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchPredictions();
    fetchRecommendations();
  }, [userId]);

  const fetchPredictions = async (showRefreshing = false) => {
    if (showRefreshing) setRefreshing(true);
    try {
      const response = await fetch(`http://localhost:8000/predictions/comprehensive/${userId}`);
      const data = await response.json();
      setPredictions(data);
    } catch (error) {
      console.error('Error fetching predictions:', error);
    } finally {
      setLoading(false);
      if (showRefreshing) setRefreshing(false);
    }
  };

  const fetchRecommendations = async () => {
    try {
      const response = await fetch(`http://localhost:8000/recommendations/${userId}`);
      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  const handleRefresh = () => {
    fetchPredictions(true);
    fetchRecommendations();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600 font-semibold">Analyzing your data...</p>
        </div>
      </div>
    );
  }

  if (!predictions) {
    return (
      <div className="card text-center py-12">
        <Brain className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No Data Available</h3>
        <p className="text-gray-600">Start logging your progress to get intelligent predictions!</p>
      </div>
    );
  }

  const weightPred = predictions.predictions.weight_prediction;
  const caloriePred = predictions.predictions.calorie_prediction;
  const successPred = predictions.success_prediction;
  const plateauRisk = predictions.predictions.plateau_risk;

  const getPriorityColor = (priority) => {
    const colors = {
      high: 'border-red-200 bg-red-50',
      medium: 'border-orange-200 bg-orange-50',
      low: 'border-blue-200 bg-blue-50'
    };
    return colors[priority] || 'border-gray-200 bg-gray-50';
  };

  const getPriorityBadge = (priority) => {
    const styles = {
      high: 'bg-red-100 text-red-700',
      medium: 'bg-orange-100 text-orange-700',
      low: 'bg-blue-100 text-blue-700'
    };
    return styles[priority] || 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Brain className="h-8 w-8 text-primary-600" />
            Intelligent Predictions
          </h1>
          <p className="text-gray-600 mt-1">AI-like insights powered by mathematics & data analysis</p>
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

      {/* Success Probability */}
      <div className="card bg-gradient-to-br from-primary-50 to-secondary-50 border-2 border-primary-200">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-1">Success Probability</h2>
            <p className="text-gray-600">Likelihood of reaching your goal</p>
          </div>
          <div className="text-right">
            <div className="text-5xl font-bold text-primary-600">
              {successPred.success_probability}%
            </div>
          </div>
        </div>
        
        <div className="progress-bar h-4 mb-4">
          <div 
            className="progress-fill" 
            style={{ width: `${successPred.success_probability}%` }}
          />
        </div>

        <div className="bg-white rounded-lg p-4">
          <p className="text-gray-800 font-medium mb-3">{successPred.insight}</p>
          <div className="space-y-2">
            <p className="text-sm font-semibold text-gray-700">Key Focus Areas:</p>
            {successPred.key_factors.map((factor, index) => (
              <div key={index} className="flex items-center gap-2 text-sm text-gray-600">
                <CheckCircle className="h-4 w-4 text-primary-600" />
                <span>{factor}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weight Predictions */}
        {weightPred.trend !== 'insufficient_data' && (
          <div className="card">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-primary-50 rounded-lg">
                <TrendingDown className="h-6 w-6 text-primary-600" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">Weight Forecast</h2>
                <p className="text-sm text-gray-600">Based on current trends</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="text-gray-700">Current Weight</span>
                <span className="text-xl font-bold text-gray-900">{weightPred.current_weight} kg</span>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                  <span className="text-gray-700">In 7 days</span>
                  <span className="font-bold text-blue-600">{weightPred.predictions['7_days']} kg</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                  <span className="text-gray-700">In 14 days</span>
                  <span className="font-bold text-purple-600">{weightPred.predictions['14_days']} kg</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-primary-50 rounded-lg">
                  <span className="text-gray-700">In 30 days</span>
                  <span className="font-bold text-primary-600">{weightPred.predictions['30_days']} kg</span>
                </div>
              </div>

              <div className="pt-4 border-t border-gray-200">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Weekly Change</span>
                  <span className={`font-semibold ${
                    weightPred.weekly_change < 0 ? 'text-green-600' : 'text-orange-600'
                  }`}>
                    {weightPred.weekly_change > 0 ? '+' : ''}{weightPred.weekly_change} kg/week
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm mt-2">
                  <span className="text-gray-600">Confidence</span>
                  <span className="font-semibold text-gray-900">{weightPred.confidence}%</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Calorie Recommendations */}
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-accent-50 rounded-lg">
              <Zap className="h-6 w-6 text-accent-600" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Calorie Optimization</h2>
              <p className="text-sm text-gray-600">Smart adjustments</p>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="text-gray-700">Your TDEE</span>
              <span className="text-xl font-bold text-gray-900">{caloriePred.current_tdee} cal</span>
            </div>

            <div className="p-4 bg-gradient-to-br from-accent-50 to-accent-100 rounded-lg border-2 border-accent-200">
              <p className="text-sm text-gray-700 mb-2">Recommended Daily Intake</p>
              <p className="text-3xl font-bold text-accent-600">{caloriePred.recommended_calories} cal</p>
              {caloriePred.adjustment !== 0 && (
                <p className="text-sm text-gray-600 mt-2">
                  {caloriePred.adjustment > 0 ? '+' : ''}{caloriePred.adjustment} cal adjustment
                </p>
              )}
            </div>

            <div className="bg-blue-50 rounded-lg p-4">
              <p className="text-sm font-semibold text-blue-900 mb-1">Why this number?</p>
              <p className="text-sm text-blue-700">{caloriePred.reason}</p>
            </div>
          </div>
        </div>

        {/* Plateau Risk */}
        {plateauRisk.risk_level !== 'unknown' && (
          <div className="card">
            <div className="flex items-center gap-3 mb-6">
              <div className={`p-2 rounded-lg ${
                plateauRisk.risk_level === 'high' ? 'bg-red-50' :
                plateauRisk.risk_level === 'moderate' ? 'bg-orange-50' : 'bg-green-50'
              }`}>
                <AlertCircle className={`h-6 w-6 ${
                  plateauRisk.risk_level === 'high' ? 'text-red-600' :
                  plateauRisk.risk_level === 'moderate' ? 'text-orange-600' : 'text-green-600'
                }`} />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">Plateau Risk</h2>
                <p className="text-sm text-gray-600">Early detection system</p>
              </div>
            </div>

            <div className={`p-4 rounded-lg border-2 ${
              plateauRisk.risk_level === 'high' ? 'bg-red-50 border-red-200' :
              plateauRisk.risk_level === 'moderate' ? 'bg-orange-50 border-orange-200' : 
              'bg-green-50 border-green-200'
            }`}>
              <p className="font-semibold text-gray-900 mb-2">
                Risk Level: <span className="uppercase">{plateauRisk.risk_level}</span>
              </p>
              <p className="text-sm text-gray-700">{plateauRisk.recommendation}</p>
            </div>
          </div>
        )}

        {/* Hydration Needs */}
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-secondary-50 rounded-lg">
              <Activity className="h-6 w-6 text-secondary-600" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Hydration Target</h2>
              <p className="text-sm text-gray-600">Personalized water intake</p>
            </div>
          </div>

          <div className="text-center py-6">
            <p className="text-6xl font-bold text-secondary-600">
              {predictions.predictions.hydration_needs.daily_glasses}
            </p>
            <p className="text-gray-600 mt-2">glasses per day</p>
            <p className="text-sm text-gray-500">
              ({predictions.predictions.hydration_needs.daily_ml} ml)
            </p>
          </div>

          <div className="mt-4 space-y-2">
            {predictions.predictions.hydration_needs.timing.map((time, index) => (
              <div key={index} className="flex items-center gap-2 text-sm text-gray-600 bg-gray-50 p-2 rounded">
                <CheckCircle className="h-4 w-4 text-secondary-600" />
                <span>{time}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Smart Recommendations */}
      {recommendations.length > 0 && (
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
            <Target className="h-7 w-7 text-primary-600" />
            Smart Recommendations
          </h2>

          <div className="space-y-4">
            {recommendations.map((rec, index) => (
              <div 
                key={index} 
                className={`p-5 rounded-lg border-2 ${getPriorityColor(rec.priority)}`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-bold text-gray-900 text-lg">{rec.title}</h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold uppercase ${getPriorityBadge(rec.priority)}`}>
                        {rec.priority}
                      </span>
                    </div>
                    <p className="text-gray-700 mb-3">{rec.message}</p>
                  </div>
                </div>

                <div className="bg-white rounded-lg p-4">
                  <p className="font-semibold text-gray-900 mb-2 text-sm">Action Steps:</p>
                  <ul className="space-y-2">
                    {rec.actions.map((action, actionIndex) => (
                      <li key={actionIndex} className="flex items-start gap-2 text-sm text-gray-700">
                        <CheckCircle className="h-4 w-4 text-primary-600 mt-0.5 flex-shrink-0" />
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Info Banner */}
      <div className="card bg-gradient-to-r from-purple-50 to-blue-50 border-2 border-purple-200">
        <div className="flex items-start gap-4">
          <Brain className="h-8 w-8 text-purple-600 flex-shrink-0" />
          <div>
            <h3 className="font-bold text-gray-900 mb-2">🚀 Powered by Mathematics, Not AI</h3>
            <p className="text-sm text-gray-700">
              These predictions use advanced statistical analysis, linear regression, and evidence-based fitness science. 
              <strong> No AI APIs, no costs, 100% transparent calculations.</strong> The more you log, the more accurate the predictions become!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Predictions;
