import requests

# Set the base URL of your FastAPI application
base_url = "http://127.0.0.1:8000"

# Prepare the request data
prompt = "What is in this image and audio?"

# Path to the local audio file
audio_path = "/Users/advaitpaliwal/mhacks/mhacks-google/input.mp3"

# Path to the local image file
image_path = "/Users/advaitpaliwal/mhacks/mhacks-google/image.png"

# Prepare the request files
files = {
    "audio": ("audio.mp3", open(audio_path, "rb"), "audio/mpeg"),
    "image": ("image.png", open(image_path, "rb"), "image/png"),
}

# Prepare the request data
data = {
    "prompt": prompt
}

# Send the POST request to the /chat endpoint
response = requests.post(f"{base_url}/chat/", data=data, files=files)

# Check the response status code
if response.status_code == 200:
    # Request successful
    chat_response = response.json()
    print("Chat Response:")
    print(chat_response)
else:
    # Request failed
    print(f"Request failed with status code: {response.status_code}")
    print("Error details:")
    print(response.text)
