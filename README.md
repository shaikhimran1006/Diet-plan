# 🏋️ AI-Powered Personalized Diet & Fitness Recommendation System

A full-stack web application that generates personalized diet and fitness plans using AI. Built with React, FastAPI, and Google's Gemini AI.

![Tech Stack](https://img.shields.io/badge/React-18.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

## ✨ Features

- 📝 **User Profile Input**: Comprehensive form for age, gender, height, weight, activity level, health goals, food preferences, allergies, and medical conditions
- 🧮 **Smart Calorie Calculator**: Uses Mifflin-St Jeor equation for accurate BMR and TDEE calculations
- 🍽️ **Personalized Meal Plans**: AI-generated daily meal plans (breakfast, lunch, dinner, snacks)
- 📊 **Macro Breakdown**: Detailed protein, carbs, and fat distribution
- 💪 **Exercise Recommendations**: Customized workouts for home or gym
- 🛒 **Smart Grocery Lists**: Automated shopping lists based on your meal plan
- 💾 **Local Database**: SQLite storage for tracking history
- 🤖 **AI-Powered**: Google Gemini integration for intelligent recommendations

## 🛠️ Tech Stack

### Frontend
- **React.js** (Vite)
- **TailwindCSS** for styling
- **Axios** for API calls

### Backend
- **FastAPI** (Python)
- **SQLAlchemy** (ORM)
- **SQLite** (Database)
- **Google Generative AI** (Gemini)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** and npm ([Download](https://nodejs.org/))
- **Git** (optional, for cloning)

## 🚀 Installation & Setup

### 1️⃣ Clone or Download the Project

```bash
cd "d:\DIet plan Suggestion"
```

### 2️⃣ Backend Setup

#### Step 1: Navigate to backend directory
```powershell
cd backend
```

#### Step 2: Create a virtual environment (recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Step 3: Install Python dependencies
```powershell
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables
Create a `.env` file in the `backend` directory:
```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=AIzaSyAOIOTyTAIFD5fls08WcfcGSnrSH6TnzYY
```

> **Note**: Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

#### Step 5: Run the Backend Server
```powershell
uvicorn main:app --reload
```

The backend will start at `http://localhost:8000`

✅ **Verify**: Visit `http://localhost:8000` - you should see the API welcome message.

---

### 3️⃣ Frontend Setup

Open a **new terminal** and navigate to the frontend directory:

#### Step 1: Navigate to frontend directory
```powershell
cd "d:\DIet plan Suggestion\frontend"
```

#### Step 2: Install Node dependencies
```powershell
npm install
```

#### Step 3: Run the Development Server
```powershell
npm run dev
```

The frontend will start at `http://localhost:5173`

✅ **Verify**: Open `http://localhost:5173` in your browser.

---

## 🎮 Usage

1. **Open your browser** and go to `http://localhost:5173`
2. **Fill out the form** with your personal information:
   - Age, Gender, Height, Weight
   - Activity Level (sedentary to extremely active)
   - Health Goal (weight loss, maintenance, muscle gain, endurance)
   - Food Preferences (vegetarian, vegan, keto, etc.)
   - Allergies (optional)
   - Medical Conditions (optional)
3. **Click "Generate My Plan"**
4. **Wait 10-20 seconds** for AI to generate your personalized plan
5. **View your results**:
   - Daily calorie target and BMR
   - Macronutrient breakdown
   - Complete meal plan for the day
   - Exercise recommendations
   - Grocery shopping list

## 📁 Project Structure

```
Diet plan Suggestion/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # SQLAlchemy models & database setup
│   ├── schemas.py              # Pydantic schemas for validation
│   ├── calculations.py         # BMR & calorie calculation logic
│   ├── ai_service.py           # Google Gemini AI integration
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── diet_fitness.db         # SQLite database (auto-generated)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UserForm.jsx    # User input form component
│   │   │   └── PlanResults.jsx # Results display component
│   │   ├── api/
│   │   │   └── api.js          # API service layer
│   │   ├── App.jsx             # Main application component
│   │   ├── main.jsx            # React entry point
│   │   └── index.css           # TailwindCSS styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── .gitignore
└── README.md
```

## 🔑 API Endpoints

### Base URL: `http://localhost:8000`

#### `POST /generate-plan`
Generate a personalized diet and fitness plan.

**Request Body:**
```json
{
  "age": 25,
  "gender": "male",
  "height": 175,
  "weight": 70,
  "activity_level": "moderately_active",
  "health_goal": "muscle_gain",
  "food_preferences": "vegetarian",
  "allergies": "nuts",
  "medical_conditions": null
}
```

**Response:**
```json
{
  "user_id": 1,
  "bmr": 1680.5,
  "daily_calories": 2800,
  "meal_plan": {
    "breakfast": "...",
    "lunch": "...",
    "dinner": "...",
    "snacks": "..."
  },
  "macros": {
    "calories": 2800,
    "protein": "210g",
    "carbs": "315g",
    "fats": "78g"
  },
  "exercises": ["..."],
  "grocery_list": ["..."],
  "created_at": "2025-10-05T12:00:00"
}
```

#### `GET /history/{user_id}`
Retrieve all plans for a specific user.

## 🧪 Testing the Application

### Test Backend API (using PowerShell):
```powershell
# Test root endpoint
Invoke-RestMethod -Uri http://localhost:8000 -Method GET

# Test generate-plan endpoint
$body = @{
    age = 25
    gender = "male"
    height = 175
    weight = 70
    activity_level = "moderately_active"
    health_goal = "muscle_gain"
    food_preferences = "vegetarian"
    allergies = $null
    medical_conditions = $null
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/generate-plan -Method POST -Body $body -ContentType "application/json"
```

## 🔧 Troubleshooting

### Backend Issues:

**"Module not found" errors:**
```powershell
pip install -r requirements.txt
```

**"GOOGLE_API_KEY not found":**
- Ensure `.env` file exists in the `backend` directory
- Verify the API key is correct

**Port 8000 already in use:**
```powershell
uvicorn main:app --reload --port 8001
```
(Update frontend API URL to match)

### Frontend Issues:

**"npm: command not found":**
- Install Node.js from [nodejs.org](https://nodejs.org/)

**Blank page or errors:**
- Check browser console (F12)
- Ensure backend is running at `http://localhost:8000`
- Try clearing browser cache

**TailwindCSS not working:**
```powershell
npm install
npm run dev
```

## 🌟 Features Explained

### Calorie Calculation
Uses the **Mifflin-St Jeor Equation**:
- **Men**: BMR = (10 × weight) + (6.25 × height) - (5 × age) + 5
- **Women**: BMR = (10 × weight) + (6.25 × height) - (5 × age) - 161

Then multiplied by activity factor (1.2 - 1.9) and adjusted for health goals.

### AI Integration
The application uses Google's Gemini AI to:
- Generate contextual meal suggestions
- Consider dietary restrictions and preferences
- Create balanced meals matching calorie/macro targets
- Suggest appropriate exercises based on fitness level
- Build smart grocery lists

## 📝 Notes

- **Local Only**: This application runs entirely on your local machine
- **Data Privacy**: All data is stored locally in SQLite database
- **AI Response Time**: Plan generation takes 10-20 seconds
- **Educational Purpose**: Always consult healthcare professionals before starting new diet/exercise programs

## 🤝 Contributing

This is a local development project. Feel free to:
- Modify the code for your needs
- Add new features
- Customize the UI
- Improve AI prompts

## 📄 License

This project is for educational purposes. Use at your own discretion.

## 🆘 Support

If you encounter issues:
1. Check that both frontend and backend are running
2. Verify your Google API key is valid
3. Check Python version (3.8+) and Node.js version (16+)
4. Review the console logs for error messages

## 🎯 Future Enhancements

Potential features to add:
- User authentication
- Multi-day meal plans
- Recipe details with cooking instructions
- Progress tracking over time
- Export plans to PDF
- Mobile-responsive improvements
- Integration with fitness trackers

---

**Built with ❤️ using React, FastAPI, and Google Gemini AI**
