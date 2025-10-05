# 🏛️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER BROWSER                            │
│                   http://localhost:5173                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ HTTP Requests (JSON)
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   REACT FRONTEND                             │
│                     (Vite + React)                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Components                                          │   │
│  │  - UserForm.jsx (Input Form)                        │   │
│  │  - PlanResults.jsx (Display Results)                │   │
│  │  - App.jsx (Main Component)                         │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  API Layer (api.js)                                 │   │
│  │  - generatePlan()                                   │   │
│  │  - getUserHistory()                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Styling (TailwindCSS)                              │   │
│  │  - Responsive grid layout                           │   │
│  │  - Card components                                  │   │
│  │  - Color scheme                                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Axios HTTP Client
                      │ POST /generate-plan
                      │ GET /history/{user_id}
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   FASTAPI BACKEND                            │
│                  http://localhost:8000                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  API Endpoints (main.py)                            │   │
│  │  - POST /generate-plan                              │   │
│  │  - GET /history/{user_id}                           │   │
│  │  - GET / (info)                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Business Logic                                     │   │
│  │  - calculations.py (BMR, TDEE, Macros)             │   │
│  │  - ai_service.py (Gemini Integration)              │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Data Layer (database.py)                           │   │
│  │  - SQLAlchemy ORM                                   │   │
│  │  - User Model                                       │   │
│  │  - Plan Model                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Validation (schemas.py)                            │   │
│  │  - Pydantic Models                                  │   │
│  │  - UserInput, PlanResponse                          │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────┬────────────────────┬────────────────────────┘
              │                    │
              │                    │
              │                    └────────────────────┐
              │                                         │
┌─────────────▼───────────────┐     ┌─────────────────▼─────┐
│     SQLite Database         │     │   Google Gemini API    │
│   (diet_fitness.db)         │     │  (generativeai.google) │
│                             │     │                        │
│  Tables:                    │     │  Model: gemini-pro     │
│  - users                    │     │  Purpose: Generate     │
│  - plans                    │     │  - Meal plans          │
│                             │     │  - Exercises           │
│  Stores:                    │     │  - Grocery lists       │
│  - User profiles            │     │                        │
│  - Generated plans          │     │  Input: Structured     │
│  - Plan history             │     │  JSON prompt           │
│                             │     │                        │
│  Local file storage         │     │  Output: JSON with     │
│  No cloud needed            │     │  personalized plan     │
└─────────────────────────────┘     └────────────────────────┘
```

---

## Request Flow Diagram

```
USER ACTION: Submit Form
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ 1. Frontend: Form Validation                             │
│    - Check required fields                               │
│    - Validate data types                                 │
│    - Convert to proper format                            │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 2. Frontend: API Call                                    │
│    axios.post('/generate-plan', userData)                │
│    - Show loading spinner                                │
│    - Disable submit button                               │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 3. Backend: Receive Request                              │
│    FastAPI endpoint handler                              │
│    - CORS validation                                     │
│    - Pydantic schema validation                          │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 4. Backend: Save User to Database                        │
│    SQLAlchemy ORM                                        │
│    - Create User object                                  │
│    - Commit to SQLite                                    │
│    - Get user.id                                         │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 5. Backend: Calculate BMR                                │
│    Mifflin-St Jeor Equation                              │
│    - Male: (10×W) + (6.25×H) - (5×A) + 5               │
│    - Female: (10×W) + (6.25×H) - (5×A) - 161           │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 6. Backend: Calculate Daily Calories                     │
│    TDEE = BMR × Activity Factor                          │
│    Daily = TDEE + Goal Adjustment                        │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 7. Backend: Calculate Macros                             │
│    Based on goal and calories                            │
│    - Protein (grams)                                     │
│    - Carbs (grams)                                       │
│    - Fats (grams)                                        │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 8. Backend: Build AI Prompt                              │
│    Structured prompt with:                               │
│    - User profile data                                   │
│    - Calculated targets                                  │
│    - Dietary restrictions                                │
│    - Output format specification                         │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 9. External: Call Google Gemini API                      │
│    genai.GenerativeModel('gemini-pro')                   │
│    - Send prompt                                         │
│    - Wait for response (10-20 seconds)                   │
│    - Receive JSON                                        │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 10. Backend: Parse AI Response                           │
│     - Clean markdown formatting                          │
│     - Parse JSON                                         │
│     - Validate structure                                 │
│     - Handle errors (fallback)                           │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 11. Backend: Save Plan to Database                       │
│     SQLAlchemy ORM                                       │
│     - Create Plan object                                 │
│     - Link to user_id                                    │
│     - Store all components                               │
│     - Commit to SQLite                                   │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 12. Backend: Build Response                              │
│     PlanResponse schema                                  │
│     - user_id                                            │
│     - bmr, daily_calories                                │
│     - meal_plan (nested object)                          │
│     - macros (nested object)                             │
│     - exercises (array)                                  │
│     - grocery_list (array)                               │
│     - created_at (timestamp)                             │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 13. Backend: Return JSON Response                        │
│     FastAPI automatic serialization                      │
│     - Status: 200 OK                                     │
│     - Content-Type: application/json                     │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 14. Frontend: Receive Response                           │
│     axios promise resolved                               │
│     - Hide loading spinner                               │
│     - Parse JSON data                                    │
│     - Update state                                       │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│ 15. Frontend: Render Results                             │
│     PlanResults component                                │
│     - Display all sections                               │
│     - Format data beautifully                            │
│     - Scroll to results                                  │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
       USER: Views Plan
```

---

## Component Architecture

### Frontend Components

```
App.jsx (Main Container)
│
├── State Management
│   ├── plan (object|null)
│   ├── loading (boolean)
│   └── error (string|null)
│
├── Event Handlers
│   ├── handleSubmit(userData)
│   ├── handleReset()
│   └── handleError()
│
└── Rendered Components
    ├── Header (Gradient)
    ├── UserForm
    │   ├── Props: onSubmit, loading
    │   ├── State: formData
    │   └── Validation
    ├── Loading Spinner (conditional)
    ├── Error Message (conditional)
    ├── PlanResults (conditional)
    │   ├── Props: plan
    │   ├── BMR Card
    │   ├── Macros Card
    │   ├── Meal Plan Card
    │   ├── Exercises Card
    │   └── Grocery Card
    └── Footer
```

### Backend Modules

```
main.py (FastAPI App)
│
├── Middleware
│   └── CORS Configuration
│
├── Startup Events
│   └── init_db()
│
├── Endpoints
│   ├── GET /
│   ├── POST /generate-plan
│   │   ├── Depends: get_db()
│   │   ├── Input: UserInput
│   │   ├── Output: PlanResponse
│   │   └── Process:
│   │       ├── Save user
│   │       ├── Calculate BMR
│   │       ├── Calculate calories
│   │       ├── Calculate macros
│   │       ├── Generate AI plan
│   │       ├── Save plan
│   │       └── Return response
│   │
│   └── GET /history/{user_id}
│       ├── Depends: get_db()
│       ├── Query: User + Plans
│       └── Return: JSON
│
└── Error Handlers
    └── HTTPException
```

---

## Database Schema

```
┌─────────────────────────────────────────────────────────┐
│                      users                              │
├─────────────────────────────────────────────────────────┤
│ id                  INTEGER PRIMARY KEY                 │
│ age                 INTEGER NOT NULL                    │
│ gender              VARCHAR NOT NULL                    │
│ height              FLOAT NOT NULL                      │
│ weight              FLOAT NOT NULL                      │
│ activity_level      VARCHAR NOT NULL                    │
│ health_goal         VARCHAR NOT NULL                    │
│ food_preferences    VARCHAR NOT NULL                    │
│ allergies           VARCHAR NULL                        │
│ medical_conditions  VARCHAR NULL                        │
│ created_at          DATETIME DEFAULT NOW                │
└─────────────────────────────────────────────────────────┘
                       │
                       │ 1:N relationship
                       │
┌─────────────────────▼───────────────────────────────────┐
│                      plans                              │
├─────────────────────────────────────────────────────────┤
│ id                  INTEGER PRIMARY KEY                 │
│ user_id             INTEGER FOREIGN KEY                 │
│ bmr                 FLOAT NOT NULL                      │
│ daily_calories      INTEGER NOT NULL                    │
│ meal_plan           TEXT (JSON) NOT NULL                │
│ macros              TEXT (JSON) NOT NULL                │
│ exercises           TEXT (JSON) NOT NULL                │
│ grocery_list        TEXT (JSON) NOT NULL                │
│ created_at          DATETIME DEFAULT NOW                │
└─────────────────────────────────────────────────────────┘

Example JSON stored in plans.meal_plan:
{
  "breakfast": "Oatmeal with berries...",
  "lunch": "Grilled chicken salad...",
  "dinner": "Salmon with vegetables...",
  "snacks": "Greek yogurt..."
}

Example JSON stored in plans.macros:
{
  "protein": "150g",
  "carbs": "200g",
  "fats": "60g"
}

Example JSON stored in plans.exercises:
[
  "Warm-up: 5 minutes",
  "Squats: 3 sets of 12",
  "Push-ups: 3 sets of 10",
  ...
]

Example JSON stored in plans.grocery_list:
[
  "Chicken breast",
  "Brown rice",
  "Broccoli",
  ...
]
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                    │
├─────────────────────────────────────────────────────────┤
│  React 18.2           │  Component-based UI             │
│  TailwindCSS 3.4      │  Utility-first CSS              │
│  Vite 5.0             │  Fast dev server & bundler      │
└─────────────────────────────────────────────────────────┘
                         │
                         │ HTTP/JSON
                         │
┌─────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                     │
├─────────────────────────────────────────────────────────┤
│  FastAPI 0.109        │  Modern Python web framework    │
│  Pydantic 2.5         │  Data validation                │
│  Python 3.8+          │  Programming language           │
└─────────────────────────────────────────────────────────┘
                         │
                         │
          ┌──────────────┴──────────────┐
          │                             │
┌─────────▼─────────┐        ┌──────────▼────────────┐
│   DATA LAYER      │        │   EXTERNAL SERVICES   │
├───────────────────┤        ├───────────────────────┤
│ SQLAlchemy 2.0    │        │ Google Gemini AI      │
│ SQLite 3          │        │ (generativeai 0.3.2)  │
│ Local Database    │        │ AI Model: gemini-pro  │
└───────────────────┘        └───────────────────────┘
```

---

## Deployment Architecture (Local)

```
┌──────────────────────────────────────────────────────────┐
│                  Windows Machine (Local)                  │
│                                                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Terminal 1: Backend                              │  │
│  │  $ cd backend                                     │  │
│  │  $ .\venv\Scripts\Activate.ps1                    │  │
│  │  $ uvicorn main:app --reload                      │  │
│  │                                                    │  │
│  │  Running on: http://localhost:8000                │  │
│  └───────────────────────────────────────────────────┘  │
│                                                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Terminal 2: Frontend                             │  │
│  │  $ cd frontend                                    │  │
│  │  $ npm run dev                                    │  │
│  │                                                    │  │
│  │  Running on: http://localhost:5173                │  │
│  └───────────────────────────────────────────────────┘  │
│                                                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Files                                            │  │
│  │  - backend/diet_fitness.db (SQLite)               │  │
│  │  - backend/.env (API Key)                         │  │
│  │  - backend/venv/ (Python packages)                │  │
│  │  - frontend/node_modules/ (Node packages)         │  │
│  └───────────────────────────────────────────────────┘  │
│                                                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Browser                                          │  │
│  │  http://localhost:5173                            │  │
│  │                                                    │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │   AI Diet & Fitness Planner UI              │  │  │
│  │  │   - Input Form                              │  │  │
│  │  │   - Results Display                         │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS
                           ▼
              ┌────────────────────────┐
              │  Google Cloud          │
              │  Gemini API            │
              │  (External Service)    │
              └────────────────────────┘
```

---

## Security Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                        │
└──────────────────────────────────────────────────────────┘

1. Environment Variables
   ├── .env file (not in git)
   ├── API keys stored securely
   └── No hardcoded secrets

2. Input Validation
   ├── Frontend: Form validation
   ├── Backend: Pydantic schemas
   └── Type checking

3. CORS Policy
   ├── Restricted to localhost
   ├── No wildcard origins
   └── Specific ports only

4. Database Security
   ├── SQLAlchemy ORM (SQL injection prevention)
   ├── Local file storage
   └── No remote access

5. API Security
   ├── Rate limiting (API provider)
   ├── Error handling
   └── No sensitive data in logs

6. Development Only
   ├── Not production-ready
   ├── Local-only access
   └── No authentication (yet)
```

---

**This architecture provides a solid foundation for a local full-stack AI application!**
