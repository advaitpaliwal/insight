import speech_recognition as sr


def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=2)
    names = sr.Microphone.list_microphone_names()
    print(names)
    with mic as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            f"Could not request results from Google Speech Recognition service; {e}")

    return None


if __name__ == "__main__":
    recognize_speech()
