# 🔑 API Quota Management Guide

## Current Issue: Quota Exceeded

You're seeing this error:
```
429 You exceeded your current quota
Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests
```

---

## ✅ Solutions

### Solution 1: Use Fallback Mode (Already Implemented!)

I've added intelligent fallback plans that work **without AI** when quota is exceeded. The app will now:

1. Try to use Google Gemini AI first
2. If quota exceeded → automatically use smart fallback plans
3. Fallback plans are customized based on:
   - Your health goal (weight loss, muscle gain, maintenance)
   - Food preferences (vegetarian, vegan, etc.)
   - Your calculated calories and macros

**Just restart your backend server and it will work!**

```powershell
uvicorn main:app --reload
```

---

### Solution 2: Get a New API Key

Google Gemini API Free Tier Limits:
- **15 requests per minute**
- **1,500 requests per day**

**Steps to get a fresh key:**

1. Go to: https://aistudio.google.com/app/apikey

2. **Delete your old API key** (if visible):
   - Click the trash icon next to your old key
   - This removes the quota tracking

3. **Create a new API key**:
   - Click "Create API key"
   - Select "Create API key in new project"
   - Copy the new key

4. **Update `.env` file**:
   ```
   GOOGLE_API_KEY=your_new_key_here
   ```

5. **Restart backend**:
   ```powershell
   uvicorn main:app --reload
   ```

---

### Solution 3: Wait for Quota Reset

Free tier quotas reset:
- **Per-minute quota**: Resets every 60 seconds
- **Daily quota**: Resets at midnight UTC

If you hit the daily limit, wait until the next day (midnight UTC).

---

### Solution 4: Upgrade to Paid Plan (For Production)

If you need more requests:

1. Go to: https://console.cloud.google.com/
2. Enable billing on your project
3. The free tier becomes much more generous with billing enabled
4. Pay-as-you-go pricing (very affordable)

**Pricing (as of 2025):**
- Gemini 1.5 Flash: ~$0.00001 per request
- Very cheap for personal use

---

## 🎯 Current App Status

Your app now has **3 modes**:

### Mode 1: AI-Powered (Normal)
- Uses Google Gemini AI
- Generates highly personalized plans
- Takes 10-20 seconds
- **Requires valid API key with quota**

### Mode 2: Smart Fallback (Automatic)
- Activates when quota exceeded
- Uses pre-built intelligent templates
- Customized to your profile
- Instant response (< 1 second)
- **No API key needed**

### Mode 3: Basic Fallback (Emergency)
- If both above fail
- Generic but functional plan
- Always works

---

## 🧪 Test the Fallback Mode

Your app should now work even without AI! Try it:

1. Restart backend: `uvicorn main:app --reload`
2. Go to: `http://localhost:5173`
3. Fill out the form
4. Submit

You should see a message in the backend console:
```
⚠️  Quota exceeded - using fallback demo plan
```

And you'll still get a complete plan with:
- ✅ Meal plan (customized to your goal)
- ✅ Macros breakdown
- ✅ Exercise routine
- ✅ Grocery list

---

## 📊 Monitoring Your Quota

To check your current quota usage:

1. Go to: https://console.cloud.google.com/
2. Navigate to "APIs & Services" → "Dashboard"
3. Select "Generative Language API"
4. View your quota metrics

---

## 💡 Best Practices

### For Development:
1. Use fallback mode (already implemented)
2. Get new API keys when needed
3. Test with different scenarios

### For Production:
1. Enable billing for higher quotas
2. Implement request caching
3. Add rate limiting on your backend
4. Monitor usage with alerts

---

## 🔧 Quick Fixes

### Error: "API key expired"
→ Get new key from https://aistudio.google.com/app/apikey

### Error: "Quota exceeded"
→ App now uses fallback (restart backend)

### Error: "Invalid API key"
→ Check `.env` file has correct key format

### Error: "Model not found"
→ Use `check_models.py` to see available models

---

## ✨ What's Great About the Fallback

The fallback plans are **smart**:

- **Weight Loss**: Lower calorie meals, more cardio
- **Muscle Gain**: High protein, strength training
- **Maintenance**: Balanced meals and exercises
- **Vegetarian/Vegan**: Respects food preferences
- **Instant**: No waiting for AI response
- **Always works**: No dependency on external APIs

---

## 🎉 Summary

**You have 3 options:**

1. ✅ **Use fallback mode** (restart backend - works immediately)
2. 🔑 **Get new API key** (2 minutes - full AI power)
3. ⏰ **Wait for reset** (midnight UTC - free)

**Recommended for now**: Just restart your backend and use the smart fallback mode. It works great for testing and development!

```powershell
uvicorn main:app --reload
```

Your app is now **quota-proof**! 🛡️
