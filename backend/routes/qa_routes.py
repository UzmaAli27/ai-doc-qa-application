from fastapi import APIRouter
from pydantic import BaseModel

from services.embedding_service import search_similar_chunks
from services.qa_service import generate_answer

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


# 🔥 helper function to clean retrieved context
def clean_context(chunks):
    cleaned = []

    for chunk in chunks:

        if not chunk:
            continue

        text = str(chunk)

        # remove noise
        text = text.replace("Q:", "").replace("A:", "")

        # remove broken words caused by bad splitting
        text = " ".join(text.split())

        cleaned.append(text)

    # 🔥 IMPORTANT: limit total size (prevents truncation)
    final_context = "\n\n".join(cleaned)

    return final_context[:4000]   # limit total tokens safely


@router.post("/ask-question")
def ask_question(request: QuestionRequest):

    # 1. Get relevant chunks from vector DB
    raw_context = search_similar_chunks(request.question)

    # 2. Clean context before sending to LLM
    context = clean_context(raw_context)

    # 3. Generate final answer (ONLY based on current question)
    answer = generate_answer(
        question=request.question,
        context=context
    )

    # 4. Return clean response (no junk exposure to frontend)
    return {
        "question": request.question,
        "answer": answer,
        "context_used": context  # optional (you can remove in production)
    }