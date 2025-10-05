# 🧪 Testing Guide

## Quick Test Scenarios

### Test 1: Weight Loss Plan (Vegetarian)
**Profile:**
- Age: 28
- Gender: Female
- Height: 165 cm
- Weight: 75 kg
- Activity Level: Lightly Active
- Health Goal: Weight Loss
- Food Preferences: Vegetarian
- Allergies: None
- Medical Conditions: None

**Expected Results:**
- Calorie deficit (approx. 1400-1600 kcal)
- Higher protein percentage
- Vegetarian meal options
- Cardio-focused exercises

---

### Test 2: Muscle Gain Plan (No Restrictions)
**Profile:**
- Age: 25
- Gender: Male
- Height: 180 cm
- Weight: 70 kg
- Activity Level: Very Active
- Health Goal: Muscle Gain
- Food Preferences: No preference
- Allergies: None
- Medical Conditions: None

**Expected Results:**
- Calorie surplus (approx. 2800-3000 kcal)
- High protein (30% of calories)
- Strength training exercises
- Frequent meals including protein-rich options

---

### Test 3: Maintenance Plan (Vegan, Nut Allergy)
**Profile:**
- Age: 35
- Gender: Female
- Height: 170 cm
- Weight: 65 kg
- Activity Level: Moderately Active
- Health Goal: Maintenance
- Food Preferences: Vegan
- Allergies: Nuts, Peanuts
- Medical Conditions: None

**Expected Results:**
- Balanced calories (approx. 2000-2200 kcal)
- Vegan protein sources (no nuts)
- Balanced exercise routine
- Plant-based grocery list

---

### Test 4: Endurance Plan (Keto)
**Profile:**
- Age: 40
- Gender: Male
- Height: 175 cm
- Weight: 80 kg
- Activity Level: Extremely Active
- Health Goal: Endurance
- Food Preferences: Keto
- Allergies: Lactose intolerant
- Medical Conditions: Pre-diabetes

**Expected Results:**
- Moderate calorie increase (approx. 2600-2800 kcal)
- Low carb, high fat meals
- Endurance exercises (running, cycling)
- Lactose-free options

---

## Manual Testing Checklist

### Frontend Testing
- [ ] Form loads correctly
- [ ] All input fields are present
- [ ] Form validation works (try submitting empty form)
- [ ] Age accepts only numbers between 10-100
- [ ] Height/Weight accept decimals
- [ ] All dropdowns have correct options
- [ ] Submit button shows "Generating..." during load
- [ ] Loading spinner appears during generation
- [ ] Results display correctly after generation
- [ ] "Generate Another Plan" button works
- [ ] Page is responsive on mobile
- [ ] No console errors in browser (F12)

### Backend Testing
- [ ] Backend starts without errors
- [ ] GET / returns API info
- [ ] POST /generate-plan accepts valid data
- [ ] BMR calculation is accurate
- [ ] Calorie calculation is correct
- [ ] Macros add up correctly
- [ ] AI generates realistic meal plans
- [ ] Database file is created (diet_fitness.db)
- [ ] Data is saved to database
- [ ] GET /history/{user_id} returns saved plans

### Integration Testing
- [ ] Frontend connects to backend
- [ ] Form submission sends correct data format
- [ ] Loading state shows during AI generation
- [ ] Results display all sections:
  - [ ] BMR and calories
  - [ ] Macros (protein, carbs, fats)
  - [ ] Meal plan (4 meals)
  - [ ] Exercises (5+ items)
  - [ ] Grocery list (10+ items)
- [ ] Error handling works (stop backend and try submitting)
- [ ] Multiple plans can be generated

---

## API Testing with PowerShell

### Test 1: Check Backend is Running
```powershell
Invoke-RestMethod -Uri http://localhost:8000 -Method GET
```

**Expected Output:**
```json
{
  "message": "AI Diet & Fitness Recommendation System API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

---

### Test 2: Generate a Plan
```powershell
$body = @{
    age = 25
    gender = "male"
    height = 175
    weight = 70
    activity_level = "moderately_active"
    health_goal = "muscle_gain"
    food_preferences = "No preference"
    allergies = $null
    medical_conditions = $null
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri http://localhost:8000/generate-plan -Method POST -Body $body -ContentType "application/json"
$response | ConvertTo-Json -Depth 5
```

**Expected Output:**
```json
{
  "user_id": 1,
  "bmr": 1680.5,
  "daily_calories": 2900,
  "meal_plan": {
    "breakfast": "...",
    "lunch": "...",
    "dinner": "...",
    "snacks": "..."
  },
  "macros": {
    "calories": 2900,
    "protein": "218g",
    "carbs": "324g",
    "fats": "80g"
  },
  "exercises": [...],
  "grocery_list": [...],
  "created_at": "2025-10-05T..."
}
```

---

### Test 3: Check User History
```powershell
Invoke-RestMethod -Uri http://localhost:8000/history/1 -Method GET
```

**Expected Output:**
```json
{
  "user": {
    "id": 1,
    "age": 25,
    "gender": "male",
    ...
  },
  "plans": [...]
}
```

---

## Calculation Verification

### BMR Calculation (Mifflin-St Jeor)
**Example: 25-year-old male, 70kg, 175cm**

Formula (Male): BMR = (10 × 70) + (6.25 × 175) - (5 × 25) + 5
- = 700 + 1093.75 - 125 + 5
- = **1673.75 kcal**

**Example: 28-year-old female, 60kg, 165cm**

Formula (Female): BMR = (10 × 60) + (6.25 × 165) - (5 × 28) - 161
- = 600 + 1031.25 - 140 - 161
- = **1330.25 kcal**

### TDEE Calculation
**BMR × Activity Factor**

Activity Factors:
- Sedentary: 1.2
- Lightly Active: 1.375
- Moderately Active: 1.55
- Very Active: 1.725
- Extremely Active: 1.9

**Example: BMR 1673.75, Moderately Active**
- TDEE = 1673.75 × 1.55
- = **2594.31 kcal**

### Goal Adjustments
- Weight Loss: -500 kcal
- Maintenance: 0 kcal
- Muscle Gain: +300 kcal
- Endurance: +200 kcal

**Example: TDEE 2594.31, Muscle Gain**
- Daily Target = 2594.31 + 300
- = **2894 kcal** (rounded)

---

## Common Issues & Debugging

### Issue: "Failed to generate plan"
**Debug Steps:**
1. Check backend console for errors
2. Verify Google API key is valid
3. Check internet connection
4. Look for rate limiting errors

### Issue: Empty or Invalid Response
**Debug Steps:**
1. Check backend logs
2. Verify AI service is working
3. Test with simpler profile data
4. Check JSON parsing in ai_service.py

### Issue: Database Errors
**Debug Steps:**
1. Check if diet_fitness.db file exists
2. Delete database and restart backend
3. Check SQLAlchemy logs
4. Verify file permissions

### Issue: CORS Errors
**Debug Steps:**
1. Verify frontend runs on port 5173
2. Check backend CORS configuration
3. Clear browser cache
4. Try different browser

---

## Performance Testing

### Expected Response Times
- Form submission: < 100ms
- BMR calculation: < 10ms
- AI generation: 10-20 seconds
- Database save: < 50ms
- Total request: 10-25 seconds

### Load Testing (Optional)
Test with multiple concurrent requests:
```powershell
# Run this multiple times simultaneously
1..5 | ForEach-Object -Parallel {
    $body = @{
        age = 25
        gender = "male"
        height = 175
        weight = 70
        activity_level = "moderately_active"
        health_goal = "muscle_gain"
        food_preferences = "No preference"
    } | ConvertTo-Json
    
    Invoke-RestMethod -Uri http://localhost:8000/generate-plan -Method POST -Body $body -ContentType "application/json"
}
```

---

## Browser Testing

Test in multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)

Check:
- [ ] Layout renders correctly
- [ ] Forms work properly
- [ ] No console errors
- [ ] Responsive design works

---

## Accessibility Testing

- [ ] Tab navigation works
- [ ] Form labels are present
- [ ] Color contrast is sufficient
- [ ] Error messages are clear
- [ ] Screen reader friendly (optional)

---

## Security Testing

- [ ] API key is not exposed in frontend
- [ ] Input validation prevents injection
- [ ] CORS only allows localhost
- [ ] No sensitive data in console logs
- [ ] Database is local only

---

## Success Criteria

✅ All 4 test scenarios generate valid plans
✅ Calculations match expected values
✅ AI generates contextual recommendations
✅ Database stores and retrieves data
✅ UI is responsive and error-free
✅ No console errors or warnings
✅ Performance is acceptable (< 25s total)

---

**Happy Testing! 🧪✅**
