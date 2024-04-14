import google.generativeai as genai
from config import GOOGLE_API_KEY
import os
from database import FirestoreDB
from storage import GCStorage
from datetime import datetime
from uuid import uuid4
from google.ai.generativelanguage import Content, Part, FileData
from pi.camera import take_picture
from google.generativeai.types.file_types import File
import tempfile

genai.configure(api_key=GOOGLE_API_KEY)
db = FirestoreDB()
storage = GCStorage()

system_instruction = """
You are an AI assistant integrated into my smart glasses. 
Provide concise, real-time assistance based on my vision or general questions. 
If my question is vague or refers to something unspecified, use the glasses' visual feed for context. 
Keep responses to 2 sentences for audio output. Focus on relevant information and avoid tasks beyond providing answers. 
Tailor responses to our unique glasses-based interaction, making me feel like we're working together to enhance my daily life.
"""
model = genai.GenerativeModel(
    'models/gemini-1.5-pro-latest', system_instruction=system_instruction)


def create_history_from_firestore(n: int = 100):
    """Create history object from Firestore data."""
    n = min(n, 1000)
    items = db.get_data("data", field="created_at", limit=n, descending=True)
    history = []
    for item in items.values():
        user_content = Content(
            parts=[
                Part(text=item["input_prompt"]),
                Part(file_data=FileData(mime_type="image/jpeg",
                     file_uri=f"https://generativelanguage.googleapis.com/v1beta/files/{item['file_id']}"))
            ],
            role="user"
        )
        model_content = Content(
            parts=[
                Part(text=item["output_response"])
            ],
            role="model"
        )
        history.append(user_content)
        history.append(model_content)
    return history


initial_history = create_history_from_firestore()
chat = model.start_chat(history=initial_history)


def upload_file_to_genai(filepath: str, prompt: str) -> File:
    """Upload a file to Google's generative language service."""
    input_file = genai.upload_file(path=filepath, display_name=prompt)
    print(f"Uploaded file '{input_file.display_name}' as: {input_file.uri}")
    return input_file


def get_response(prompt: str) -> str:
    """Answer questions using the model. This function takes a picture before answering the question."""
    filepath = "picture.jpg"
    take_picture()
    print("Answering questions...", prompt)
    input_file = upload_file_to_genai(filepath, prompt)
    response = chat.send_message([prompt, input_file])
    file_id = input_file.uri.split("/")[-1]
    image_key = f"{file_id}.jpg"
    image_url = storage.upload_file("my-bucket", filepath, image_key)
    save_query_to_firestore(prompt, response.text, image_url, file_id)
    os.remove(filepath)
    return response.text


def save_query_to_firestore(prompt: str, response: str, image_url: str = None, file_id: str = None) -> None:
    data_id = uuid4().hex
    data = {
        "file_id": file_id,
        "image_url": image_url,
        "created_at": datetime.now(),
        "input_prompt": prompt,
        "output_response": response
    }
    db.save_data("data", data_id, data)
    print(f"Saved query to Firestore: {data}")


if __name__ == "__main__":
    while True:
        user_input = input("Enter your question: ")
        response = get_response(user_input)
        print(response)
        print("\n")
