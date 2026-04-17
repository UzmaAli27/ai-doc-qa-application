from fastapi import APIRouter
from services.unified_search import unified_search

router = APIRouter()


@router.post("/ask")
def ask(query: str):

    results = unified_search(query)

    if not results:
        return {
            "answer": "No relevant information found",
            "sources": []
        }

    formatted = []

    for r in results[:5]:
        formatted.append({
            "source_type": r["source_type"],
            "text": r["content"],
            "metadata": r["metadata"]
        })

    return {
        "answer": f"Found {len(results)} relevant results",
        "sources": formatted
    }