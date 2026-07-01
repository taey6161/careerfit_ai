# backend/routers/jobs.py

from fastapi import APIRouter

from typing import List

router = APIRouter()



# 목업 데이터: 3일차에 실제 CSV 데이터로 교체한다

MOCK_JOBS = [
    {
        "id": 1,
        "company": "네이버 (NAVER)",
        "title": "AI 플랫폼 백엔드 개발자",
        "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        "preferred_skills": ["Docker", "Kubernetes"],
        "description": "초거대 AI 모델 기반의 서비스 플랫폼 백엔드를 설계하고 개발합니다. 대규모 트래픽을 안정적으로 처리할 수 있는 고성능 API 인프라 구축을 담당합니다.",
        "deadline": "2026-08-31"
    },
    {
        "id": 2,
        "company": "카카오 (Kakao)",
        "title": "LLM/RAG 기반 서비스 개발 엔지니어",
        "required_skills": ["Python", "LangChain", "ChromaDB"],
        "preferred_skills": ["OpenAI API", "AWS"],
        "description": "사내 데이터 인프라와 LLM을 연동하는 RAG(검색 증강 생성) 시스템을 구축합니다. 사용자 맞춤형 AI 서비스의 프로토타이핑부터 프로덕션 배포까지 전 과정을 리드합니다.",
        "deadline": "2026-08-31"
    },
    {
        "id": 3,
        "company": "당근 (Daangn)",
        "title": "파이썬 백엔드 주니어 개발자",
        "required_skills": ["Python", "Django", "MySQL"],
        "preferred_skills": ["Redis", "Git"],
        "description": "지역 기반 커뮤니티 서비스의 핵심 비즈니스 로직을 개발하고 유지보수합니다. 마이크로서비스 아키텍처(MSA) 환경에서 동료들과 코드 리뷰를 통해 함께 성장합니다.",
        "deadline": "2026-08-31"
    }
]



@router.get("/jobs", tags=["Jobs"])

def get_jobs():

    """

    취업 공고 목록을 반환하는 엔드포인트.

    현재는 목업 데이터를 반환하며, 3일차에 실제 데이터로 교체한다.

    """

    return {

        "count": len(MOCK_JOBS),

        "jobs": MOCK_JOBS

    }



@router.get("/jobs/{job_id}", tags=["Jobs"])

def get_job_by_id(job_id: int):

    """

    특정 공고의 상세 정보를 반환한다.

    """

    for job in MOCK_JOBS:

        if job["id"] == job_id:

            return job

    # 찾지 못한 경우

    from fastapi import HTTPException

    raise HTTPException(status_code=404, detail=f"공고 ID {job_id}를 찾을 수 없습니다.")