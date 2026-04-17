from fastapi import APIRouter
from pydantic import BaseModel

from services.unified_search import unified_search
from services.llm_service import generate_answer

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_question(request: QuestionRequest):

    query = request.question

    print("Received query:", query)

    results = unified_search(query)

    print("Search results count:", len(results))

    if not results:
        return {
            "answer": "No relevant information found.",
            "sources": []
        }

    answer = generate_answer(query, results)

    print("Generated answer:", answer)

    return {
        "answer": answer,
        "sources": results
    }