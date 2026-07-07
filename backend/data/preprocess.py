# backend/data/preprocess.py

# 데이터 전처리 파이프라인

# 실행: backend/ 폴더에서 python data/preprocess.py

from datetime import date

import pandas as pd

import sqlite3

import json

import os



# ─── 1. 파일 경로 설정 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JOBS_CSV = os.path.join(BASE_DIR, "jobs.csv")

DB_PATH = os.path.join(BASE_DIR, "careerfit.db")

RAG_JSON = os.path.join(BASE_DIR, "rag_documents.json")



# ─── 2. CSV 읽기 

def load_data(filepath: str) -> pd.DataFrame:

    """

    CSV 파일을 읽어 DataFrame으로 반환합니다.

    인코딩 오류가 발생하면 cp949로 재시도합니다.

    """

    try:

        df = pd.read_csv(filepath, encoding="utf-8")

        print(f"✅ 파일 읽기 성공 (UTF-8): {filepath}")

    except UnicodeDecodeError:

        df = pd.read_csv(filepath, encoding="cp949")

        print(f"✅ 파일 읽기 성공 (CP949): {filepath}")

    print(f"   행 수: {len(df)}, 열 수: {len(df.columns)}")

    print(f"   컬럼: {df.columns.tolist()}")

    return df

# ------ 3. 결측치 및 중복 처리 함수들 정의 ------

def check_missing(df):
    print("\n[1] 각 컬럼별 결측치(빈값) 수 확인:")
    print(df.isnull().sum())
    return df

def handle_missing(df):
    # 결측치가 있으면 빈 문자열이나 기본값으로 채워주는 로직
    df = df.fillna("")
    print("✅ 결측치 처리 완료")
    return df

def remove_duplicates(df):
    # 중복된 데이터 제거
    before_len = len(df)
    df = df.drop_duplicates()
    after_len = len(df)
    print(f"✅ 중복 제거 완료 (이전: {before_len}행 -> 이후: {after_len}행)")
    return df
# ------ 4. 기술 스택 표준화 및 DB 저장 함수들 정의 ------

def standardize_skills(df):
    # 각 행의 required_skills를 돌면서 SKILL_NORMALIZATION 규칙에 따라 표준화하는 로직
    print("✅ 기술 스택 표준화 완료")
    return df

def save_to_sqlite(df, db_path):
    # 데이터를 SQLite 데이터베이스에 저장하는 로직
    import sqlite3
    conn = sqlite3.connect(db_path)
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ SQLite 저장 완료 : {db_path}")

def query_sqlite(db_path):
    # DB에 잘 들어갔나 확인차 쿼리 날려보는 로직
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]
    conn.close()
    print(f"🔍 DB 데이터 검증 : 총 {count}개 행이 저장되어 있습니다.")

def convert_to_rag_documents(df: pd.DataFrame) -> list:
    """
    DataFrame의 각 행을 RAG 검색에 적합한 자연어 문서로 변환합니다.

    요리 비유:
    냉장고의 재료 목록을 셰프가 바로 읽을 수 있는 레시피 카드로 변환합니다.
    """
    print("\n=== RAG 문서 변환 ===")
    documents = []

    for _, row in df.iterrows():
        # 자연어 문서 텍스트 생성
        doc_text = (
            f"{row.get('company', '')}에서 {row.get('title', '')}를 채용합니다. "
            f"필수 스킬은 {row.get('required_skills', '정보 없음')}입니다. "
            f"우대 스킬: {row.get('preferred_skills', '없음')}. "
            f"업무 내용: {row.get('description', '정보 없음')}"
        )

deadline = str(row.get("deadline", ""))
company = str(row.get("company", ""))

 metadata = {

"id": str(row.get("id", "")),

"company": company,

"title": str(row.get("title", "")),

"job_type": str(row.get("job_type", "")),

"deadline": deadline,

"source": "jobs.csv",



"deadline_month": deadline[5:7] if len(deadline) >= 7 and deadline[4] == "-" else "",

"is_startup": "true" if "스타트업" in company else "false",

"first_saved_date": date.today().isoformat()
# <- 수정
}
        documents.append({
            "text": doc_text,
            "metadata": metadata,
            "doc_id": f"job_{row.get('id', '')}"  # ChromaDB의 고유 ID
        })

    print(f"   ✅ {len(documents)}개 문서 변환 완료")
    print("\n   [첫 번째 문서 미리보기]")
    print(f"   ID: {documents[0]['doc_id']}")
    print(f"   텍스트: {documents[0]['text'][:100]}...")
    print(f"   메타데이터: {documents[0]['metadata']}")

    return documents


def save_rag_documents(documents: list, json_path: str) -> None:
    """
    RAG 문서를 JSON 파일로 저장합니다.
    ChromaDB에 저장하기 전 중간 저장 역할을 합니다.
    """
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)
    print(f"\n   ✅ RAG 문서 JSON 저장: {json_path}")

# 원래 작성하셨던 실행 테스트 구간 (이 구조 바로 위에 넣으시면 됩니다!)
if __name__ == "__main__":
    df_jobs = load_data(JOBS_CSV)
    df_jobs = check_missing(df_jobs)
    df_jobs = handle_missing(df_jobs)
    df_jobs = remove_duplicates(df_jobs)
    df_jobs = standardize_skills(df_jobs)
    save_to_sqlite(df_jobs, DB_PATH)
    query_sqlite(DB_PATH)
    rag_docs = convert_to_rag_documents(df_jobs)  # ← 추가
    save_rag_documents(rag_docs, RAG_JSON)         # ← 추가
    print(f"\n✅ 전처리 완료: 최종 {len(df_jobs)}행, RAG 문서 {len(rag_docs)}개")

SKILL_NORMALIZATION = {

    "python": "Python",

    "sql": "SQL",

    "ai": "AI",

    "ml": "머신러닝",

    "machine learning": "머신러닝",

    "deep learning": "딥러닝",

    "r": "R",         # 대소문자 주의

    "js": "JavaScript",

    "javascript": "JavaScript",

    "tableau": "Tableau",

    "powerbi": "Power BI",

    "power bi": "Power BI",

}

def normalize_skills(skills_str: str) -> str:

    """

    스킬 키워드 문자열을 표준화합니다.

    입력: "python, sql, Machine Learning"

    출력: "Python, SQL, 머신러닝"

    """

    if not isinstance(skills_str, str) or not skills_str.strip():

        return ""

    skills = [s.strip() for s in skills_str.split(",")]

    normalized = []

    for skill in skills:

        # 소문자로 변환해서 사전에서 찾기

        lower = skill.lower()

        # 사전에 있으면 표준화된 이름으로, 없으면 원래 값 유지

        normalized.append(SKILL_NORMALIZATION.get(lower, skill))

    return ", ".join(normalized)

def standardize_skills(df: pd.DataFrame) -> pd.DataFrame:

    """

    required_skills, preferred_skills 컬럼 전체에 표준화를 적용합니다.

    """

    print("\n=== 스킬 키워드 표준화 ===")

    for col in ["required_skills", "preferred_skills"]:

        if col in df.columns:

            df[col] = df[col].apply(normalize_skills)

    print(" ✅ 표준화 완료")

    # 표준화 결과 샘플 출력

    print("\n [표준화 전후 비교 샘플]")

    print(df[["title", "required_skills"]].head(3).to_string())

    return df

    # preprocess.py에 추가
import sqlite3

def save_to_sqlite(df: pd.DataFrame, db_path: str) -> None:
    """
    전처리된 DataFrame을 SQLite 데이터베이스에 저장합니다.

    요리 비유:
    손질이 끝난 재료를 냉장고(SQLite)에 정리해서 넣는 단계입니다.
    """
    print(f"\n=== SQLite 저장 ===")

    conn = sqlite3.connect(db_path)

    # DataFrame을 SQL 테이블로 저장
    # if_exists="replace": 테이블이 이미 있으면 덮어씁니다
    df.to_sql("jobs", conn, if_exists="replace", index=False)

    # 저장 확인
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    print(f"   ✅ 저장 완료: jobs 테이블에 {count}행 저장됨")
    print(f"   파일 위치: {db_path}")

    conn.close()

    # preprocess.py에 추가

def query_sqlite(db_path: str) -> None:
    """
    SQLite에서 데이터를 조회해 저장 결과를 확인합니다.
    """
    print(f"\n=== SQLite 조회 테스트 ===")
    conn = sqlite3.connect(db_path)

    # 1. 전체 행 수
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jobs")
    print(f"   전체 공고 수: {cursor.fetchone()[0]}개")

    # 2. 직무 분류별 개수
    print("\n   [직무 분류별 공고 수]")
    cursor.execute("""
        SELECT job_type, COUNT(*) as count
        FROM jobs
        GROUP BY job_type
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        print(f"   - {row[0]}: {row[1]}개")

    # 3. Python 필수 스킬 공고만 조회
    print("\n   [Python이 필요한 공고]")
    cursor.execute("""
        SELECT company, title, required_skills
        FROM jobs
        WHERE required_skills LIKE '%Python%'
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"   - {row[0]} | {row[1]}")
        print(f"     스킬: {row[2]}")

    conn.close()