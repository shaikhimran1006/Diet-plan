import { useState } from 'react';
import { Plus, History, Calendar, Target } from 'lucide-react';
import UserForm from '../components/UserForm';
import PlanResults from '../components/PlanResults';

const Plans = () => {
  const [showForm, setShowForm] = useState(false);
  const [currentPlan, setCurrentPlan] = useState(null);
  const [planHistory, setPlanHistory] = useState([
    {
      id: 1,
      date: '2024-02-15',
      calories: 2000,
      goal: 'weight_loss',
      bmr: 1650
    },
    {
      id: 2,
      date: '2024-01-20',
      calories: 2200,
      goal: 'muscle_gain',
      bmr: 1680
    }
  ]);

  const handlePlanGenerated = (plan) => {
    setCurrentPlan(plan);
    setShowForm(false);
  };

  const handleNewPlan = () => {
    setShowForm(true);
    setCurrentPlan(null);
  };

  const getGoalBadge = (goal) => {
    const styles = {
      weight_loss: 'bg-green-100 text-green-700',
      muscle_gain: 'bg-purple-100 text-purple-700',
      maintenance: 'bg-blue-100 text-blue-700',
      endurance: 'bg-orange-100 text-orange-700'
    };
    return styles[goal] || 'bg-gray-100 text-gray-700';
  };

  const getGoalText = (goal) => {
    const text = {
      weight_loss: 'Weight Loss',
      muscle_gain: 'Muscle Gain',
      maintenance: 'Maintenance',
      endurance: 'Endurance'
    };
    return text[goal] || goal;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Diet Plans</h1>
          <p className="text-gray-600 mt-1">Generate and manage your personalized meal plans</p>
        </div>
        <button 
          onClick={handleNewPlan}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="h-5 w-5" />
          New Plan
        </button>
      </div>

      {/* Show Form or Plan */}
      {showForm ? (
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Generate New Plan</h2>
          <UserForm onPlanGenerated={handlePlanGenerated} />
        </div>
      ) : currentPlan ? (
        <div>
          <div className="mb-4">
            <button 
              onClick={() => setCurrentPlan(null)}
              className="text-primary-600 hover:text-primary-700 font-medium flex items-center gap-2"
            >
              <History className="h-4 w-4" />
              Back to History
            </button>
          </div>
          <PlanResults plan={currentPlan} />
        </div>
      ) : (
        /* Plan History */
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-gray-700">
            <History className="h-5 w-5" />
            <h2 className="text-xl font-bold">Your Plan History</h2>
          </div>

          {planHistory.length === 0 ? (
            <div className="card text-center py-12">
              <Target className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No Plans Yet</h3>
              <p className="text-gray-600 mb-6">Create your first personalized diet plan to get started!</p>
              <button 
                onClick={handleNewPlan}
                className="btn-primary inline-flex items-center gap-2"
              >
                <Plus className="h-5 w-5" />
                Create First Plan
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {planHistory.map((plan) => (
                <div 
                  key={plan.id}
                  className="card card-hover cursor-pointer"
                  onClick={() => {
                    // In real app, fetch full plan data
                    alert('Loading plan details... (Connect to API)');
                  }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="p-2 bg-primary-50 rounded-lg">
                      <Target className="h-6 w-6 text-primary-600" />
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getGoalBadge(plan.goal)}`}>
                      {getGoalText(plan.goal)}
                    </span>
                  </div>
                  
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Created Date</p>
                      <p className="font-semibold text-gray-900 flex items-center gap-2">
                        <Calendar className="h-4 w-4" />
                        {new Date(plan.date).toLocaleDateString('en-US', { 
                          month: 'short', 
                          day: 'numeric', 
                          year: 'numeric' 
                        })}
                      </p>
                    </div>

                    <div className="pt-3 border-t border-gray-100">
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <p className="text-xs text-gray-600">Daily Calories</p>
                          <p className="text-lg font-bold text-primary-600">{plan.calories}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600">BMR</p>
                          <p className="text-lg font-bold text-gray-900">{plan.bmr}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <button className="w-full mt-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors">
                    View Details
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Plans;
