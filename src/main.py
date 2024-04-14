from src.wake_word_detection import detect_wake_word
from src.recognize_speech import recognize_speech
from src.funcs import get_response
from src.text_to_speech import speak


def main():
    while True:
        wake_word_detected = detect_wake_word()
        if wake_word_detected:
            user_input = recognize_speech()
            if user_input:
                print(f"User said: {user_input}")
                response = get_response(user_input)
                speak(response)


if __name__ == "__main__":
    main()
