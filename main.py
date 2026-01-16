from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 어제와 오늘 데이터를 모두 합친 데이터베이스
MARKET_DATABASE = {
    "KR_Semiconductor": {"title": "한국 반도체", "target_salary": 180000000, "core_signals": {"PhD": 1.5, "Patents": 2.0}},
    "US_DataScientist": {"title": "미국 데이터 사이언티스트", "target_salary": 350000, "core_signals": {"FAANG": 2.0, "LLM": 1.5}},
    "Product_Designer": {
        "title": "데이터 기반 프로덕트 디자이너",
        "target_salary": 85000000,
        "core_signals": {
            "Data_Evidence": 2.5,  # 박사님이 강조하신 데이터 가중치
            "CX_UX_Strategy": 1.8,
            "Figma_Framer": 1.0,
            "A/B_Testing": 2.0
        }
    }
}

class UserCareer(BaseModel):
    sector: str
    current_salary: float
    my_signals: List[str]

@app.get("/")
def home():
    return {"message": "CTELAB AI: Multi-Sector Strategy Engine", "status": "Ready"}

@app.post("/analyze")
def analyze(data: UserCareer):
    market = MARKET_DATABASE.get(data.sector)
    if not market: return {"error": "Sector not found"}

    strategy_score = sum([market["core_signals"].get(s, 0.5) for s in data.my_signals])
    gap = market["target_salary"] - data.current_salary
    
    return {
        "target": market["title"],
        "strategy_score": round(strategy_score, 2),
        "salary_gap": gap,
        "advice": "Data-based CX evidence is key." if "Data_Evidence" in data.my_signals else "Need data evidence."
    }
