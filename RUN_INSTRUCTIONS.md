# 🚀 Quick Start Guide

## How to Run the Project

### Option 1: Using the Batch File (Easiest)
```bash
# Double-click or run:
run_project.bat
```

### Option 2: Manual Start
```bash
# Navigate to project directory
cd C:\Users\Administrator\Desktop\Hackthon\DATA_HACKTHON

# Run the server
python start_server.py
```

### Option 3: Direct Python
```bash
python main.py
```

---

## 📍 Access the Application

Once running, open your browser to:
```
http://localhost:8000
```

---

## 🎯 Interactive Features

### 1. **Search Comments** 🔍
- Try SQL injection: `' OR '1'='1`
- Extract user data: `' UNION SELECT * FROM users --`

### 2. **Admin Login** 👤
- Default credentials: `admin / admin123` or `analyst / pass123`
- SQL Injection bypass: Username: `admin' OR '1'='1' --`

### 3. **Add Comment** 💬
- Test XSS: `<script>alert('XSS')</script>`
- Test HTML injection: `<h1>HACKED!</h1>`

### 4. **Upload File** 📁
- Try uploading any file type
- Test path traversal: filename `../../evil.txt`

### 5. **Network Check (Ping)** 🌐
- Command injection: `localhost & dir` (Windows)
- Or: `localhost; ls` (Linux)

---

## 🗄️ Database Info

The app creates `vulnerable_comments.db` with:

**Users Table:**
- admin / admin123 (role: admin)
- analyst / pass123 (role: user)

**Comments Table:**
- Stores all user comments (vulnerable to XSS)

---

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main dashboard |
| `/api/districts` | GET | Get all districts |
| `/api/stats` | GET | Statistics |
| `/api/search` | GET | Search comments (SQL Injection) |
| `/api/login` | POST | Login (SQL Injection) |
| `/api/comment` | POST | Add comment (XSS) |
| `/api/comments` | GET | Get comments |
| `/api/upload` | POST | Upload file (Unrestricted) |
| `/api/system/ping` | GET | Ping host (Command Injection) |
| `/api/export` | GET | Export data (IDOR) |

---

## ⚠️ Important Notes

1. **This is intentionally vulnerable** - for hackathon/educational purposes only
2. **Do not expose to internet** - run locally only
3. **See VULNERABILITIES.md** for detailed exploit examples
4. **Database is created automatically** on first run

---

## 🛠️ Requirements

All dependencies auto-install, but if needed manually:
```bash
pip install fastapi uvicorn pandas numpy
```

---

## 🎓 Hackathon Challenge

Can you:
- ✅ Bypass authentication
- ✅ Extract all user passwords
- ✅ Execute system commands
- ✅ Inject malicious JavaScript
- ✅ Upload malicious files
- ✅ Access unauthorized data

**Good luck! 🎯**
