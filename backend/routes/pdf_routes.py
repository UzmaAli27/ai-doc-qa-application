from fastapi import APIRouter, UploadFile, File
from typing import List

from services.pdf_service import extract_text_from_pdf
from services.embedding_service import create_embeddings
from services.unified_store import UNIFIED_STORE

router = APIRouter()


@router.post("/upload-pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):

    uploaded_files = []

    for file in files:

        # extract text
        text = extract_text_from_pdf(file)

        # create embeddings
        create_embeddings(text)

        # split into chunks
        chunks = text.split("\n")

        for chunk in chunks:

            if chunk.strip():

                data = {
                    "source_type": "pdf",
                    "source_id": file.filename,
                    "content": chunk,
                    "metadata": {
                        "page": None
                    }
                }

                UNIFIED_STORE.append(data)

                print("Stored chunk:", data)

        uploaded_files.append(file.filename)

    print("TOTAL STORED CHUNKS:", len(UNIFIED_STORE))

    return {
        "message": "PDF upload successful",
        "files": uploaded_files
    }