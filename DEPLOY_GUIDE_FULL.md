# 🌐 THE ULTIMATE FREE DEPLOYMENT GUIDE

This guide covers **every single step** to get your GovOptima project online for free. Follow exactly in order.

---

## 🟢 PHASE 1: PREPARE YOUR CODE (GitHub)

You need to put your code on GitHub so other services can access it.

### **Step 1: Create a GitHub Account**
1. Go to [github.com/signup](https://github.com/signup)
2. Enter your email, create a password, and choose a username.
3. Solve the puzzle to verify you are human.
4. Go to your email inbox and click the verification link.
5. **Cost:** FREE

### **Step 2: Create a Repository**
1. Log in to GitHub.
2. Click the **+** icon in the top-right corner -> **New repository**.
3. **Repository name:** `govoptima-hackathon`
4. **Public/Private:** Select **Public**.
5. Scroll down and click **Create repository**.

### **Step 3: Upload Your Code**
You have two options. **Option A is easiest.**

#### **Option A: Web Upload (No Git installed)**
1. On your new repository page, click the link that says **uploading an existing file**.
2. Open your project folder on your computer: `C:\Users\Administrator\Desktop\Hackthon\DATA_HACKTHON`
3. Select **ALL files and folders** (Ctrl+A).
4. **Drag and drop** them into the GitHub webpage.
5. Wait for the upload bars to finish.
6. In the "Commit changes" box at the bottom, type: "Initial upload".
7. Click **Commit changes**.

#### **Option B: Command Line (If Git is installed)**
1. Open PowerShell in your project folder.
2. Run these commands one by one:
   ```powershell
   git init
   git add .
   git commit -m "Initial deploy"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/govoptima-hackathon.git
   git push -u origin main
   ```
   *(Replace YOUR_USERNAME with your actual GitHub username)*

---

## 🟡 PHASE 2: DEPLOY THE SERVER (Render.com)

Render is the best place to host Python apps for free.

### **Step 1: Create Account**
1. Go to [dashboard.render.com/register](https://dashboard.render.com/register)
2. Click **Sign up with GitHub**.
3. Click **Authorize Render** to link it to your GitHub account.
4. **Cost:** FREE

### **Step 2: Create Web Service**
1. Click the **New +** button in top-right -> Select **Web Service**.
2. Under "Connect a repository", you should see `govoptima-hackathon`. Click **Connect**.
3. You will see a setup form. Fill it EXACTLY like this:

| Field | Value |
|-------|-------|
| **Name** | `govoptima-app` (or any name) |
| **Region** | Singapore (or closest to you) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python main.py` |
| **Instance Type** | **Free** (Important!) |

4. Click **Create Web Service** at the bottom.

### **Step 3: Go Live**
1. Render will start building your app. You will see logs (text scrolling).
2. It installs dependencies -> `pip install...`
3. It starts the app -> `Uvicorn running on...`
4. **Wait about 5-10 minutes.**
5. When ready, you will see a green **Live** badge.
6. Your URL is at the top left, e.g., `https://govoptima-app.onrender.com`.
7. **Click it to verify your site works!**

---

## 🔵 PHASE 3: KEEP IT AWAKE (UptimeRobot)

Render's free tier "sleeps" after 15 minutes of no activity. This makes the first load slow (30s). UptimeRobot prevents this.

### **Step 1: create Account**
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Click **Register for FREE**.
3. Enter name, email, password.
4. **Cost:** FREE

### **Step 2: Create Monitor**
1. Click **+ Add New Monitor**.
2. **Monitor Type:** Select `HTTP(s)`.
3. **Friendly Name:** `GovOptima`.
4. **URL (or IP):** Paste your Render URL (e.g., `https://govoptima-app.onrender.com`).
5. **Monitoring Interval:** Select `5 minutes`.
6. Click **Create Monitor**.

### **Done!**
UptimeRobot will visit your site every 5 minutes to keep it "awake" and fast for judges.

---

## 🟣 ALTERNATIVE: RAILWAY.APP (Faster)

If Render fails or is slow, use Railway.

1. Go to [railway.app](https://railway.app).
2. Login with GitHub.
3. Click **New Project** -> **Deploy from GitHub repo**.
4. Select `govoptima-hackathon`.
5. Click **Deploy Now**.
6. Railway automatically detects Python and unnecessary config.
7. Once deployed, click the **Settings** tab -> **Generate Domain** to get your URL.

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] Code is on GitHub (Public repo)
- [ ] Render Web Service created
- [ ] Build & Start commands are correct
- [ ] Site opens and shows dashboard
- [ ] UptimeRobot monitor is running

**Good luck with your hackathon! 🏆**
