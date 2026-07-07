# CareerFit AI 🚀
> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치

## 📌 프로젝트 개요
수많은 취업 준비생들이 실제 기업이 원하는 요구사항과 자신의 포트폴리오 사이에서 방향성을 잡지 못해 막연한 불안감을 겪고 있습니다. 정보의 비대칭성으로 인해 불필요한 스펙을 쌓으며 시간과 비용을 낭비하는 문제를 해결하고자 본 프로젝트를 기획했습니다. 
이를 해결하기 위해 최신 채용 공고 및 공모전 데이터를 실시간으로 정제하여 저장하고, **RAG(검색 증강 생성) 아키텍처**를 활용해 유저의 스킬셋과 가장 의미론적으로 유사한 데이터를 매칭함으로써 환각 현상 없는 정밀한 맞춤형 포트폴리오 준비 전략을 제안합니다.

## 🛠 기술 스택
| 영역 | 기술 |
|---|---|
| **Backend** | Python 3.11, FastAPI |
| **AI API** | Gemini 2.5 Flash-lite |
| **Data** | Pandas, SQLite, ChromaDB (Vector DB) |
| **Frontend** | React, Vite, Nginx |
| **Infrastructure** | Docker, Render Cloud |

## 🏗 아키텍처
                 +---------------------------------------+
                 |         React / Vite Frontend         |
                 +---------------------------------------+
                                     │
                            (REST API 요청)
                                     ▼
                 +---------------------------------------+
                 |            FastAPI Backend            |
                 +---------------------------------------+
                                     │
             ┌───────────────────────┴───────────────────────┐
             ▼                                               ▼
 +-----------------------+                       +-----------------------+
 |   SQLite (Meta DB)    |                       |  ChromaDB (Vector DB) |
 |  - 구조화 데이터 관리  |                       |  - 의미론적 유사도 검색 |
 +-----------------------+                       +-----------------------+
             │                                               │
             └───────────────────────┬───────────────────────┘
                                     ▼
                 +---------------------------------------+
                 |         Gemini 2.5 Flash-Lite         |
                 |       (RAG 기반 컨설팅 답변 생성)        |
                 +---------------------------------------+

## ## 진행 현황

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
- [x] 4일차: RAG 기반 풀스택 인프라 연동 및 시스템 최적화
  * **ChromaDB 문서 임베딩 및 유사도 검증**: `rag_service.py` 기반으로 의미적 유사도가 높은 공고를 추출하는 Top-3 매칭 테스트 완료
  * **Gemini API RAG 파이프라인 구축**: `llm_service.py` 내에 프롬프트 엔지니어링을 적용, RAG 컨텍스트를 주입하여 사용자 맞춤형 역량 분석 응답 생성 최적화
  * **FastAPI 백엔드 윈도우 환경 예외 처리**: windows 멀티프로세싱 환경에서 `--reload` 옵션 활성화 시 발생하는 `SpawnProcess` 충돌 문제를 `multiprocessing.freeze_support()` 안전장치를 통해 해결
  * **CORS 설정 및 API 보안 강화**: `.env` 환경 변수 관리 시스템을 구축하여 `GEMINI_API_KEY` 무결성 검증을 통한 gRPC 통신 보안을 확보하고, 프론트엔드 출처(`http://localhost:5173`)에 대한 백엔드 교차출처(CORS) 허용 설정 완료
  * **React + Vite 프론트엔드 UI/UX 아키텍처 정립**: Tailwind CSS 기반으로 가시성을 극대화한 사용자 정보 입력 폼(`InputForm`), 분석 결과 뷰어(`ResultCard`), RAG 출처 카드(`SourceCard`) 컴포넌트 3종 구현 및 결합
  * **비동기 Fetch API 기반 실시간 데이터 바인딩**: 단일 페이지 내에서 `isLoading` 상태 관리를 통해 비동기 API 요청 중 스피너 UI(`분석 중...`) 및 렌더링 동적 제어 기능 완비
- [x] 5일차: Docker + 포트폴리오 완성 (feat: 4일차 RAG 풀스택 파이프라인 연동 및 UI 최적화 완료)
  * **Dockerfile 작성 완료**: 백엔드 및 프론트엔드 각각의 컨테이너 환경 패키징 명세 완비
  * **Docker build 성공**: 로컬 및 클라우드 환경 레이어 빌드 최적화 완수
  * **Docker run 후 /health 접속 확인**: 컨테이너 인프라 격리 가동 확인 완료
  * **README 최종화 완료**: 문제 정의, 데이터, 구현, 검증 4단계 완벽 반영
  * **.env 미포함 보안 확인**: 중요 API 키 및 크리덴셜 정보 유출 원천 차단 검증
  * **최종 하네스 파일 업데이트 완료**: 전체 테스트 케이스 명세 동기화
  * **GitHub 최종 커밋 완료**: 원격 저장소 형상 관리 최신화 완료
  * **팀 리플렉션 발표 준비 완료**: 템플릿 요구 명세 충족 및 슬라이드별 큐시트 제작 완료

### 📊 데이터 파이프라인 아키텍처

| 단계 | 도구 | 설명 |
| :--- | :--- | :--- |
| **수집 (Ingestion)** | CSV | 취업 공고 가공 데이터셋 구성 (`jobs.csv`) |
| **전처리 (Preprocessing)** | Pandas | 가상환경 내 자동 교차 검증 로드 및 결측치·중복 스킬 데이터 표준화 |
| **의미론적 검색 (RAG)** | ChromaDB | 사용자 전공·스킬 쿼리 기반 벡터 유사도 검색 및 Context 추출 |
| **생성 (Generation)** | Gemini LLM | 주입된 직무 컨텍스트 기반 맞춤형 취업 포트폴리오 코칭 서술문 생성 |
| **인터페이스 (UI)** | React + Vite | 비동기 호출 및 상태 관리를 통한 실시간 분석 결과 화면 렌더링 |

---

## 🚀 실행 방법

### 🐳 Docker로 실행 (권장)
```bash
# 백엔드 구동
cd backend
docker build -t careerfit-ai-backend .
docker run -p 8000:8000 --env-file .env careerfit-ai-backend

# 프론트엔드 구동
cd frontend
docker build -t careerfit-ai-frontend .
docker run -p 80:80 careerfit-ai-frontend
💻 로컬 개발 환경 실행
Bash
# 백엔드 구동 (http://localhost:8000/docs)
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 프론트엔드 구동 (http://localhost:5173)
cd frontend
npm install
npm run dev
✨ 주요 기능
RAG 기반 역량 분석: 학습 및 저장된 실제 도메인 취업 공고 데이터를 근거로 검증된 맞춤형 조언 제공

출처(Sources) 표시: 답변 생성 시 어떤 공고와 공모전 데이터를 참고했는지 메타데이터를 함께 투명하게 반환

Mock Mode: 외부 API 인하우스 한도 초과 또는 네트워크 단절 시 MOCK_MODE=true 설정을 통해 안정적인 시뮬레이션 폴백 제공

🔮 향후 개선 사항
[ ] 이력서 PDF 파일 업로드 후 파일 텍스트 자동 역량 추출 파싱 엔진 고도화

[ ] 실시간 공모전 마감일 push 알림 스케줄러 기능 도입

[ ] RAG 검색 결과 품질 정량 평가를 위한 지표 체계(Ragas 등) 빌드 파이프라인 추가

🔗 Live Demo
Front-end UI: https://careerfit-ai-frontend-oj7y.onrender.com

Back-end API (Swagger): https://careerfit-ai-backend-new.onrender.com

👥 Developer
Team: 강양이 (Gangyangi)

Name: 이태연 (Lee Taeyeon)

Role: Backend / AI Service & Cloud Infrastructure Engineering

GitHub: @taey6161