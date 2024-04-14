import speech_recognition as sr


def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        output = recognizer.recognize_google(audio)
        print(f"Recognized: {output}")
        return output
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            f"Could not request results from Google Speech Recognition service; {e}")

    return None


if __name__ == "__main__":
    recognize_speech()
