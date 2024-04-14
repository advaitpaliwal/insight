import cv2
import google.generativeai as genai
from config import GOOGLE_API_KEY
from time import sleep
import os
from src.database import FirestoreDB
from src.storage import GCStorage
from datetime import datetime
from uuid import uuid4
# Configure API with the key
genai.configure(api_key=GOOGLE_API_KEY)
db = FirestoreDB()
storage = GCStorage()


def answer_question(prompt: str):
    """
    Answer questions using the model.

    Args:
        prompt (str): The prompt to generate the answer from.
    """
    print("Answering question...", prompt)
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content(prompt)
    save_query_to_firestore(prompt, response.text)
    return response.text


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
        prompt (str): The prompt to generate the answer from.
    """
    filepath = "picture.jpg"
    take_picture()
    print("Answering questions...", prompt)
    input_file = genai.upload_file(
        path=filepath, display_name=prompt)
    print(
        f"Uploaded file '{input_file.display_name}' as: {input_file.uri}")
    file_id = input_file.uri.split("/")[-1]
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content([prompt, input_file])
    image_key = f"{file_id}.jpg"
    image_url = storage.upload_file(image_key, filepath)
    save_query_to_firestore(prompt, response.text, image_url, file_id)
    os.remove("picture.jpg")
    return response.text


def save_query_to_firestore(prompt: str, response: str, image_url: str = None, file_id: str = None):
    db = FirestoreDB()
    data_id = uuid4()
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

    tools = [answer_question, answer_question_about_vision]
    instruction = "You are a helpful assistant who lives in a human's glasses. You can answer about specific item in your vision or answer general questions if it doesn't require you to see. You will be saying these out loud so keep your responses short to 1-2 sentences. Do not perform any other tasks."

    model = genai.GenerativeModel(
        "models/gemini-1.5-pro-latest", tools=tools, system_instruction=instruction
    )

    chat = model.start_chat(enable_automatic_function_calling=True)

    response = chat.send_message(user_input)
    return response.text


def get_all_items_firestore():
    """ Get all items from Firestore."""
    db = FirestoreDB()
    items = db.get_data("data")
    return items


# print(get_all_items_firestore())
