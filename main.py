from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

MARKET_DATABASE = {
    "Product_Designer": {
        "title": "데이터 기반 프로덕트 디자이너",
        "target_salary": 85000000,
        "required_signals": ["Data", "CX", "UX", "소비자", "사용자", "실험", "Figma", "Strategy"],
        "opportunity": "온/오프라인 경계를 넘는 소비자 경험(CX) 설계 역량의 가치 급등",
        "threat": "단순 디자인 기능에 매몰된 인력의 시장 경쟁력 약화"
    },
    "KR_Semiconductor": {
        "title": "한국 반도체 전문가",
        "target_salary": 180000000,
        "required_signals": ["PhD", "Patents", "Process", "Design"],
        "opportunity": "글로벌 공급망 재편으로 인한 설계 전문가 희소성 증대",
        "threat": "국가 간 기술 격차 축소 및 기술 유출 위협"
    }
}

class AdvancedUserInput(BaseModel):
    target_sector: str
    current_job: str
    current_salary: int
    exp_years: int
    skills: List[str]
    achievement_text: str  # 4번 질문
    needed_point: str      # 6번 질문

@app.get("/")
def home():
    return {"message": "CTELAB AI: Unified CX Strategy Engine v2.1 Online", "status": "Ready"}

@app.post("/analyze_v2")
def analyze_v2(data: AdvancedUserInput):
    market = MARKET_DATABASE.get(data.target_sector)
    if not market:
        return {"error": "지원하지 않는 직군입니다."}

    # 1. 텍스트 분석 기반 강점 추출 (디지털/아날로그 통합 키워드)
    full_text = (data.achievement_text + " " + " ".join(data.skills)).lower()
    strengths = [s for s in market["required_signals"] if s.lower() in full_text]
    
    # 2. SWOT 리포트 구성
    swot = {
        "Strength (강점)": strengths if strengths else ["기초 역량 보유"],
        "Weakness (약점)": [f"성장을 위해 '{data.needed_point}' 보강 및 자산화 필요"],
        "Opportunity (기회)": market["opportunity"],
        "Threat (위협)": market["threat"]
    }

    # 3. 전략적 조언
    is_strategy_expert = any(word in full_text for word in ["데이터", "소비자", "지표", "경험", "cx", "ux"])
    
    advice = f"현재 {data.current_job}로서의 {data.exp_years}년 경력에 "
    if is_strategy_expert:
        advice += "소비자 경험을 데이터로 해석하는 능력이 결합되어 향후 시장에서 대체 불가능한 전략가로 평가될 것입니다."
    else:
        advice += "기술적 숙련도를 넘어 소비자 경험(CX)을 수치화하는 역량을 보강한다면 더 큰 도약이 가능합니다."

    return {
        "report_title": f"[{data.target_sector}] 전략 진단 리포트",
        "financial_analysis": {
            "current_salary": f"{data.current_salary:,}원",
            "market_target": f"{market['target_salary']:,}원",
            "potential_upside": f"{max(0, market['target_salary'] - data.current_salary):,}원"
        },
        "swot_analysis": swot,
        "strategic_advice": advice,
        "action_plan": [
            f"'{data.needed_point}' 역량을 증명할 수 있는 실전 성과 데이터 정리",
            "고객 여정 전반의 페인포인트(Pain-points)를 지표로 개선한 사례 구축"
        ]
    }
