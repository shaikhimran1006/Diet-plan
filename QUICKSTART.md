# 🚀 Quick Start Guide

## Prerequisites Check

Before starting, verify you have:
- [ ] Python 3.8 or higher installed
- [ ] Node.js 16 or higher installed
- [ ] PowerShell or Command Prompt

## Step-by-Step Setup

### 1. Backend Setup (Terminal 1)

```powershell
# Navigate to backend folder
cd "d:\DIet plan Suggestion\backend"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ Backend is ready at http://localhost:8000

---

### 2. Frontend Setup (Terminal 2)

Open a **NEW** terminal window:

```powershell
# Navigate to frontend folder
cd "d:\DIet plan Suggestion\frontend"

# Install dependencies
npm install

# Start the development server
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

✅ Frontend is ready at http://localhost:5173

---

## 3. Test the Application

1. Open your browser and go to: **http://localhost:5173**
2. Fill out the form with sample data:
   - Age: 25
   - Gender: Male
   - Height: 175 cm
   - Weight: 70 kg
   - Activity Level: Moderately Active
   - Health Goal: Muscle Gain
   - Food Preferences: Vegetarian
3. Click "Generate My Plan"
4. Wait 10-20 seconds for AI to generate your plan
5. View your personalized results!

---

## Common Issues & Solutions

### Issue: "python: command not found"
**Solution:** Install Python from https://www.python.org/downloads/

### Issue: "npm: command not found"
**Solution:** Install Node.js from https://nodejs.org/

### Issue: "Port 8000 already in use"
**Solution:** 
```powershell
# Use a different port
uvicorn main:app --reload --port 8001
```
Then update `frontend/src/api/api.js` to use port 8001.

### Issue: "Virtual environment activation fails"
**Solution:**
```powershell
# Enable script execution (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\venv\Scripts\Activate.ps1
```

### Issue: Frontend shows "Failed to generate plan"
**Solution:**
1. Verify backend is running at http://localhost:8000
2. Check that `.env` file exists in backend folder
3. Verify Google API key is valid

---

## Stopping the Application

### Stop Backend:
Press `CTRL + C` in the backend terminal

### Stop Frontend:
Press `CTRL + C` in the frontend terminal

---

## File Structure Overview

```
Diet plan Suggestion/
├── backend/          ← Python FastAPI server
│   ├── .env         ← Your Google API key (already configured)
│   ├── main.py      ← API endpoints
│   └── ...
├── frontend/         ← React application
│   ├── src/         ← React components
│   └── ...
└── README.md        ← Full documentation
```

---

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize the AI prompts in `backend/ai_service.py`
- Modify the UI styling in `frontend/src/components/`
- Add more features based on your needs

---

## Need Help?

1. Check console logs in both terminals
2. Verify all dependencies are installed
3. Ensure both servers are running
4. Check the browser console (F12) for errors

**Happy Planning! 🎯💪🍽️**
