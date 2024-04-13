from google.cloud import texttospeech
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


model = genai.GenerativeModel('gemini-1.0-pro-latest')
response = model.generate_content("The opposite of hot is")
print(response.text)


sample_image_file = genai.upload_file(path="/Users/advaitpaliwal/mhacks/mhacks-google/image.png",
                                      display_name="Sample drawing")

print(
    f"Uploaded file '{sample_image_file.display_name}' as: {sample_image_file.uri}")


file = genai.get_file(name=sample_image_file.name)
print(f"Retrieved file '{file.display_name}' as: {sample_image_file.uri}")


model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

response = model.generate_content(
    ["Describe the image with a creative description.", sample_image_file], stream=True)

text = ''
for chunk in response:
    print(chunk.text, end='', flush=True)
    text += chunk.text

# genai.delete_file(sample_image_file.name)
# print(f'Deleted {sample_image_file.display_name}.')

sample_audo_file = genai.upload_file(
    path="/Users/advaitpaliwal/mhacks/mhacks-google/input.mp3", display_name="Sample audio")

print(
    f"Uploaded file '{sample_audo_file.display_name}' as: {sample_audo_file.uri}")

file = genai.get_file(name=sample_audo_file.name)
print(f"Retrieved file '{file.display_name}' as: {sample_audo_file.uri}")

response = model.generate_content(
    ["Do what the audio says.", sample_audo_file], stream=True)

text = ''
for chunk in response:
    print(chunk.text, end='', flush=True)
    text += chunk.text

# genai.delete_file(sample_audo_file.name)
# print(f'Deleted {sample_audo_file.display_name}.')

# client = texttospeech.TextToSpeechClient()

# synthesis_input = texttospeech.SynthesisInput(text=text)


# voice = texttospeech.VoiceSelectionParams(
#     language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
# )

# audio_config = texttospeech.AudioConfig(
#     audio_encoding=texttospeech.AudioEncoding.MP3
# )

# response = client.synthesize_speech(
#     input=synthesis_input, voice=voice, audio_config=audio_config
# )

# with open("output.mp3", "wb") as out:
#     # Write the response to the output file.
#     out.write(response.audio_content)
#     print('Audio content written to file "output.mp3"')
