# backend/data/test_search.py
# ChromaDB 저장 및 검색 테스트
# 실행: backend/ 폴더에서 python data/test_search.py

import chromadb
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAG_JSON = os.path.join(BASE_DIR, "rag_documents.json")
CHROMA_PATH = os.path.join(os.path.dirname(BASE_DIR), "chroma_db")

def load_rag_documents(json_path: str) -> list:
    """저장된 RAG 문서 JSON을 불러옵니다."""
    with open(json_path, "r", encoding="utf-8") as f:
        documents = json.load(f)
    print(f"✅ RAG 문서 {len(documents)}개 로드됨")
    return documents

def save_to_chromadb(documents: list, chroma_path: str) -> chromadb.Collection:
    """RAG 문서들을 ChromaDB에 저장합니다."""
    print("\n=== ChromaDB 저장 ===")
    client = chromadb.PersistentClient(path=chroma_path)
    
    collection = client.get_or_create_collection(
        name="careerfit_jobs",
        metadata={"description": "CareerFit AI 취업·공모전 데이터"}
    )
    
    # 기존 데이터가 있으면 초기화 (재실행 시 중복 방지)
    existing_count = collection.count()
    if existing_count > 0:
        print(f"🔄 기존 문서 {existing_count}개 발견 -> 초기화 후 재저장합니다.")
        existing = collection.get()
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
            
    # 문서 저장 (배치 처리)
    texts = [doc["text"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]
    ids = [doc["doc_id"] for doc in documents]
    
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ {collection.count()}개 문서 저장 완료")
    print(f"📍 저장 위치: {chroma_path}")
    return collection

def test_search(collection: chromadb.Collection) -> None:
    """저장된 문서로 질문 기반 검색을 테스트합니다."""
    print("\n=== ChromaDB 검색 테스트 ===")
    
    test_queries = [
        "Python과 SQL이 필요한 데이터 분석 공고",
        "경영학과 학생이 지원할 수 있는 직무",
        "오늘 점심 뭐 먹을까"
    ]
    
    for query in test_queries:
        print(f"\n질문: '{query}'")
        results = collection.query(
            query_texts=[query],
            n_results=2  # 가장 유사한 문서 2개 반換
        )
        
        # 결과 출력 구조화
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            distance = results["distances"][0][i]
            print(f"  [{i+1}] 결과")
            print(f"  회사: {meta.get('company', '?')} | 직무: {meta.get('title', '?')}")
            print(f"  거리(유사도): {round(distance, 4)}  (낮을수록 유사)")
            print(f"  문서 요약: {doc[:80]}...")

if __name__ == "__main__":
    # 1. 문서 로드 및 DB 적재 완료
    docs = load_rag_documents(RAG_JSON)
    coll = save_to_chromadb(docs, CHROMA_PATH)
    
    # 2. 최종 유사도 검색 테스트 수행
    test_search(coll)
    print("\n🎉 [3일차 실습 최종 완료] ChromaDB 저장 및 검색 테스트가 성공적으로 끝났습니다!")