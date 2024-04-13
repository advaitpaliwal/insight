from pydantic import BaseModel
from fastapi import APIRouter, File, UploadFile, Form
from generate import GenerativeAI
from storage import GCStorage
from database import FirestoreDB
import google.generativeai as genai

router = APIRouter()
generative_ai = GenerativeAI()
store = GCStorage()
db = FirestoreDB()


class ChatResponse(BaseModel):
    output: str


@router.post("/chat/", response_model=ChatResponse)
async def chat(
    prompt: str = Form(...),
    audio: UploadFile = File(None),
    image: UploadFile = File(None)
):
    files = []

    if audio:
        audio_key = f"{audio.filename}"
        audio_path = f"/tmp/{audio_key}"
        with open(audio_path, "wb") as buffer:
            buffer.write(await audio.read())
        audio_url = store.upload_file(audio_key, audio_path)
        genai_audio_file = genai.upload_file(
            path=audio_path, display_name=audio_key)
        files.append(genai_audio_file)

    if image:
        image_key = f"{image.filename}"
        image_path = f"/tmp/{image_key}"
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())
        image_url = store.upload_file(image_key, image_path)
        genai_image_file = genai.upload_file(
            path=image_path, display_name=image_key)
        files.append(genai_image_file)

    output = generative_ai.generate_content(prompt, files)
    data = {
        "prompt": prompt,
        "audio_file": audio_url if audio else None,
        "image_file": image_url if image else None,
        "output": output
    }
    db.save_data("chats", f"chat_{len(db.get_data('chats')) + 1}", data)
    return ChatResponse(output=output)
