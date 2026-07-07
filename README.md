# CareerFit AI

> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치

## 프로젝트 개요
취업 준비를 위한 AI 역량 쌓기
채용공고, 공모전 데이터를 분석하여 취업을 하기 위한 방향과 포트폴리오 준비를 제안해주는 프로젝트입니다.

## 기술 스택s

| 영역 | 기술 |
|---|---|
| 백엔드 | Python, FastAPI |
| AI API | Gemini 2.5 Flash-Lite |
| 데이터 | Pandas, SQLite, ChromaDB |
| 프론트엔드 | React, Vite |
| 실행 환경 | Docker |

## 진행 현황

- [x] 1일차: 프로젝트 기획 및 개발 환경 세팅
- [x] 2일차: FastAPI 서버 구축 및 Gemini API 연결
    * **Python 가상환경(venv) 구축 및 패키지 관리 세팅 완료** (FastAPI, Uvicorn 등 필수 의존성 설치)
    * **FastAPI 백엔드 기본 아키텍처 및 라우터 분리 구조 설계** (`/backend` 패키지 구조화)
    * **핵심 API 엔드포인트 3종 구현 및 문서화** (`/health` 시스템 체크, `/jobs` 공고 조회, `/analyze` 취업 분석)
    * **LLM 서비스 연동 준비 완료** (Gemini 2.5 Flash-Lite API 호출 아키텍처 수립 및 Mock 데이터 레이어 설계)
    * **로컬 개발 편의성 제고** (환경변수를 활용한 `mock mode` 스위칭 설정 및 통합 Swagger UI API 테스트 성공)

- [x] 3일차: 데이터 파이프라인 구축
    * **데이터 관리 자동화**: `pandas` 라이브러리를 연동하여 취업 공고 데이터(`jobs.csv`)의 무결성 검증 인프라 확보
    * **서비스 레이어 아키텍처 수립**: `services/` 폴더 내 패키지 초기화(`__init__.py`) 및 라우터-서비스 간 비즈니스 로직 결합
    * **외부 LLM 통합 환경 조성**: 가상환경 내 `google-generativeai` 및 `python-dotenv` 종속성 식별 및 설치 완료
    * **데이터 전처리 파이프라인 자동화 구축**: `backend/data/preprocess.py` 스크립트를 신규 생성하여 파일 경로 시스템 구조화 및 데이터 전처리 토대 마련
    * **인코딩 예외 처리 메커니즘 구현**: 국내 취업 데이터 파일 로드 시 발생할 수 있는 인코딩 충돌을 방지하기 위해 `try-except` 블록 기반 `UTF-8` 및 `CP949` 자동 교차 검증 및 로드 기능 구현 완료

- [ ] 4일차: RAG 기반 서비스 + React UI

- [ ] 5일차: Docker + 포트폴리오 완성