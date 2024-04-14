from wake_word_detection import detect_wake_word
from recognize_speech import recognize_speech
from service import get_response
from text_to_speech import speak


def main():
    while True:
        wake_word_detected = detect_wake_word()
        if wake_word_detected:
            print("Trying to recognize speech...")
            user_input = recognize_speech()
            if user_input:
                print(f"User: {user_input}")
                response = get_response(user_input)
                speak(response)


if __name__ == "__main__":
    main()
