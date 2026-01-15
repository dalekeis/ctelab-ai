from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 현시선호 데이터베이스
MARKET_DATABASE = {
    "KR_Semiconductor": {"title": "한국 반도체", "high_mid": 180000000, "signals": ["PhD", "Patents", "S/SK Exp"]},
    "US_DataScientist": {"title": "미국 데이터 사이언티스트", "high_mid": 350000, "signals": ["FAANG", "OpenSource", "LLM"]},
    "JP_EV_Research": {"title": "일본 전기차 연구직", "high_mid": 12000000, "signals": ["Master", "Embedded", "Cross-border"]}
}

class UserCareer(BaseModel):
    sector: str
    current_salary: float
    my_signals: List[str]

@app.get("/")
def home():
    return {"message": "CTELAB Strategy Engine is Running", "status": "Ready for Founding 50"}

@app.post("/analyze")
def analyze(data: UserCareer):
    market = MARKET_DATABASE.get(data.sector)
    if not market: return {"error": "Not Found"}
    gap = market["high_mid"] - data.current_salary
    missing = [s for s in market["signals"] if s not in data.my_signals]
    return {"target": market["title"], "salary_gap": gap, "missing_signals": missing}
