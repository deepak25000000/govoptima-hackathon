# 🚀 COMPLETE GUIDE TO RUN GOVOPTIMA

## ⚠️ IMPORTANT: Follow These Steps EXACTLY

---

## 📍 **STEP 1: Open PowerShell**

1. Press `Windows + X` on your keyboard
2. Click **"Windows PowerShell"** or **"Terminal"**

---

## 📍 **STEP 2: Navigate to Project Folder**

Copy and paste this command:

```powershell
cd C:\Users\Administrator\Desktop\Hackthon\DATA_HACKTHON
```

Press **Enter**

---

## 📍 **STEP 3: Deactivate Virtual Environment (IMPORTANT)**

Your `.venv` folder is causing issues. Deactivate it:

```powershell
deactivate
```

Press **Enter** (if you see an error, that's okay - continue to next step)

---

## 📍 **STEP 4: Delete the Broken Virtual Environment**

```powershell
Remove-Item -Recurse -Force .venv
```

Press **Enter**

---

## 📍 **STEP 5: Install Dependencies Using System Python**

Now install the required packages:

```powershell
pip install fastapi uvicorn pandas numpy python-multipart
```

Press **Enter** and wait for installation to complete (may take 1-2 minutes)

**Alternative if above fails:**

```powershell
python -m pip install fastapi uvicorn pandas numpy python-multipart
```

---

## 📍 **STEP 6: Run the Application**

```powershell
python main.py
```

Press **Enter**

---

## 📍 **STEP 7: Wait for Server to Start**

You should see:

```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

✅ **Server is ready!**

---

## 📍 **STEP 8: Open Your Browser**

1. Open **Google Chrome**, **Edge**, or **Firefox**
2. Type in the address bar:

```
http://localhost:8000
```

3. Press **Enter**

---

## 🎯 **You Should See:**

- **GovOptima Intelligence Platform** header
- **5 gradient metric cards** (Total Enrollments, Biometric Updates, etc.)
- **Resource Allocation** section
- **Migration Alerts** section
- **Cost & ROI Analysis** section
- **System Performance** section

---

## 🎨 **Test All Features:**

### 1️⃣ **Resource Allocation**
- Click the **"Calculate"** button
- You'll see exact kit and staff requirements for each district

### 2️⃣ **Migration Alerts**
- Click the **"Load Alerts"** button
- You'll see 5 colored boxes: Very High / High / Normal / Low / Very Low
- Table shows all districts with migration scores

### 3️⃣ **Cost Analysis**
- Click **"Calculate Savings"** button
- See operational cost, infrastructure cost, and ₹36+ Crore savings

### 4️⃣ **System Performance**
- Click **"Update Metrics"** button
- See total operations (16M+), high-stress districts, etc.

### 5️⃣ **Export Report**
- Click **"📥 Export Report"** at the top
- CSV file downloads automatically to your Downloads folder

### 6️⃣ **Refresh Data**
- Click **"🔄 Refresh Data"** button
- Entire page reloads with fresh data

---

## ❌ **TROUBLESHOOTING**

### **Problem: "No module named 'fastapi'"**

**Solution:**
```powershell
pip install fastapi uvicorn pandas numpy python-multipart --force-reinstall
```

### **Problem: "pip is not recognized"**

**Solution:**
```powershell
python -m ensurepip --upgrade
python -m pip install fastapi uvicorn pandas numpy python-multipart
```

### **Problem: "Port 8000 is already in use"**

**Solution:**
1. Press `CTRL + C` in the PowerShell window
2. Run `python main.py` again

### **Problem: Browser shows "Cannot connect"**

**Solution:**
1. Check PowerShell still shows "Uvicorn running..."
2. Try `http://127.0.0.1:8000` instead
3. Try different browser

---

## 🎬 **QUICK START (Summary)**

```powershell
# 1. Open PowerShell and navigate
cd C:\Users\Administrator\Desktop\Hackthon\DATA_HACKTHON

# 2. Remove broken virtual environment
Remove-Item -Recurse -Force .venv

# 3. Install dependencies
pip install fastapi uvicorn pandas numpy python-multipart

# 4. Run application
python main.py

# 5. Open browser: http://localhost:8000
```

---

## ✅ **SUCCESS CHECKLIST**

- [ ] PowerShell shows "Uvicorn running on http://0.0.0.0:8000"
- [ ] Browser loads the GovOptima dashboard
- [ ] You see 5 colorful metric cards
- [ ] "Calculate" button shows resource data
- [ ] "Load Alerts" shows migration levels
- [ ] "Calculate Savings" shows ₹ values
- [ ] "Export Report" downloads CSV file

---

## 🏆 **YOU'RE READY FOR THE HACKATHON!**

Your application is fully functional with:
- ✅ Professional government-grade UI
- ✅ Real-time analytics
- ✅ Accurate calculations
- ✅ CSV export functionality
- ✅ Interactive charts
- ✅ District comparison tool

**Server URL:** `http://localhost:8000`

---

## 📞 **Still Having Issues?**

Run this diagnostic command:

```powershell
python --version
pip --version
python -c "import fastapi; print('FastAPI installed successfully!')"
```

If all three work, you're good to go! 🚀
