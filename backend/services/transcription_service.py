import whisper
import os
import subprocess
import uuid

model = whisper.load_model("base")


def transcribe_media(file_path: str):

    try:
        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            return {"error": "File not found"}

        # 🔥 FORCE WAV AUDIO EXTRACTION (MOST RELIABLE)
        audio_path = f"{uuid.uuid4()}.wav"

        command = [
            "ffmpeg",
            "-i", file_path,
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            audio_path,
            "-y"
        ]

        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 🔥 DEBUG: check if audio created
        if not os.path.exists(audio_path):
            return {"error": "Audio extraction failed"}

        # 🔥 TRANSCRIBE WAV ONLY
        result = model.transcribe(audio_path)

        # cleanup
        os.remove(audio_path)

        return {
            "text": result.get("text", ""),
            "segments": result.get("segments", [])
        }

    except Exception as e:
        return {"error": str(e)}