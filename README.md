# CF Analyzer — Codeforces Profile Analyzer

A web app to analyze your Codeforces profile — topics, difficulty, progress, contest performance, and personalized insights.

## 🚀 Live Demo
- **Frontend:** https://cf-analyzer.onrender.com
- **Backend API:** https://cf-analyzer-api.onrender.com
- **API Docs:** https://cf-analyzer-api.onrender.com/docs

## 📁 Project Structure
```
cf-analyzer/
  ├── main.py          # FastAPI backend
  ├── analyzer.py      # Analysis logic
  ├── fetch_data.py    # Fetch submissions from Codeforces API
  ├── fetch_info.py    # Fetch user info from Codeforces API
  ├── requirements.txt # Python dependencies
  └── index.html       # Frontend (single HTML file)
```

## ⚙️ Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn main:app --reload

# Open index.html in your browser
```

## 🌐 Deploy on Render

### Backend (Web Service)
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Static Site)
- Publish Directory: `.`

## 🔧 Features
- Profile overview (rating, rank, friends, contribution)
- Topic analysis with progress bars
- Difficulty breakdown (easy / medium / hard)
- Monthly activity tracker
- Contest performance stats
- Personalized insights & recommendations
