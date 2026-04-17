from fastapi import APIRouter, UploadFile, File
import os
import shutil

from services.transcription_service import transcribe_media
# from services.unified_store import UNIFIED_STORE
from services.unified_store import add_to_unified_store

router = APIRouter()

UPLOAD_DIR = "uploaded_media"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-media")
async def upload_media(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # transcribe media
    transcript = transcribe_media(file_path)

    # store transcript segments into unified store
    if "segments" in transcript:

        for seg in transcript["segments"]:

            add_to_unified_store({
    "source_type": "video",
    "source_id": file.filename,
    "content": seg["text"],
    "metadata": {
        "start_time": seg["start"],
        "end_time": seg["end"]
    }
})

    return {
        "filename": file.filename,
        "transcript": transcript.get("text", ""),
        "segments": transcript.get("segments", [])
    }