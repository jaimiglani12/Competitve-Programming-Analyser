from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from analyzer import analyze_tags, dif_analysis, analysis, tags, dash, insights_analysis, user_prog, contest_analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "CF Analyzer Running"}

@app.get("/analysis-tags/{handle}")
def analysis_tags(handle: str):
    return tags(handle)

@app.get("/skill-analysis/{handle}")
def skill_analysis(handle: str):
    return analyze_tags(handle)

@app.get("/difficulty-analysis/{handle}")
def diff_analysis(handle: str):
    return dif_analysis(handle)

@app.get("/profile-analysis/{handle}")
def profile_analysis(handle: str):
    return analysis(handle)

@app.get("/dashboard/{handle}")
def dashboard(handle: str):
    return dash(handle)

@app.get("/insights/{handle}")
def insights(handle: str):
    return insights_analysis(handle)

@app.get("/progress/{handle}")
def progress(handle: str):
    return user_prog(handle)

@app.get("/contest-performance/{handle}")
def contest(handle: str):
    return contest_analysis(handle)
