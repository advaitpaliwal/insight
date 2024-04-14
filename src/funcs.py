import cv2
import google.generativeai as genai
from config import GOOGLE_API_KEY
from time import sleep
import os
from src.database import FirestoreDB
from src.storage import GCStorage
from datetime import datetime
from uuid import uuid4


genai.configure(api_key=GOOGLE_API_KEY)
db = FirestoreDB()
storage = GCStorage()
system_instruction = "You are a helpful assistant who lives in a my glasses. I will ask you things in my vision or answer general questions if it doesn't require vision. If my question seems vague and referring to something that I don't specify, use vision. You will be saying these out loud to me so keep your responses short to 1-2 sentences. Do not perform any other tasks."
model = genai.GenerativeModel(
    'models/gemini-1.5-pro-latest', system_instruction=system_instruction)

chat = model.start_chat(history=[])


def take_picture():
    """Take a picture using the webcam and save it as picture.jpg."""
    print("Taking picture...")
    cap = cv2.VideoCapture(0)
    sleep(2)
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        cap.release()
        return None

    cv2.imwrite('picture.jpg', frame)
    print("Picture taken and saved as picture.jpg")
    cap.release()
    return "Picture taken and saved as picture.jpg"


def answer_question_about_vision(prompt: str):
    """
    Answer questions using the model. This function takes a picture before answering the question.

    Args:
        prompt (str): What the user prompted or told you.
    """
    filepath = "picture.jpg"
    take_picture()
    print("Answering questions...", prompt)
    input_file = genai.upload_file(
        path=filepath, display_name=prompt)
    print(
        f"Uploaded file '{input_file.display_name}' as: {input_file.uri}")
    file_id = input_file.uri.split("/")[-1]
    response = chat.send_message([prompt, input_file])
    image_key = f"{file_id}.jpg"
    image_url = storage.upload_file(image_key, filepath)
    save_query_to_firestore(prompt, response.text, image_url, file_id)
    os.remove("picture.jpg")
    return response.text


def save_query_to_firestore(prompt: str, response: str, image_url: str = None, file_id: str = None):
    db = FirestoreDB()
    data_id = uuid4().hex
    data = {
        "file_id": file_id,
        "image_url": image_url,
        "created_at": datetime.now(),
        "input_prompt": prompt,
        "output_response": response
    }
    db.save_data("data", data_id, data)


def get_response(user_input: str):
    """ Get response from the model given tools and user input."""
    response = answer_question_about_vision(user_input)
    return response


def get_all_items_firestore():
    """ Get all items from Firestore."""
    db = FirestoreDB()
    items = db.get_data("data")
    sorted_items = sorted(items.items(), key=lambda x: x[1]["created_at"])
    return sorted_items


def get_all_files():
    """ Get file from GenAI."""
    return [file for file in genai.list_files()]


def get_file_given_names(names: list = []):
    """ Get file from GenAI given names."""
    files = []
    for name in names:
        files.append(genai.get_file(f"files/{name}"))
    return files


while True:
    user_input = input("Enter your question: ")
    response = get_response(user_input)
    print(response)
    print("\n")
