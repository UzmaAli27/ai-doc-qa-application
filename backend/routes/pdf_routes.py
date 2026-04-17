from fastapi import APIRouter, UploadFile, File
from services.pdf_service import extract_text_from_pdf

from services.embedding_service import (
    create_embeddings,
    search_similar_chunks,
    update_conversation_history,
    get_recent_context,
    generate_answer_from_chunks
)

router = APIRouter()


@router.post("/chat")
async def chat_with_documents(request: dict):

    question = request["question"]

    print("Received question:", question)

    relevant_chunks = search_similar_chunks(question)

    print("Relevant chunks:", relevant_chunks)

    if not relevant_chunks:
        return {
            "question": question,
            "answer": "No relevant information found in uploaded documents.",
            "context_used": []
        }

    previous_context = get_recent_context()

    answer = generate_answer_from_chunks(relevant_chunks)

    print("Generated answer:", answer)

    update_conversation_history(question, answer)

    return {
        "question": question,
        "previous_context": previous_context,
        "answer": answer,
        "context_used": relevant_chunks
    }