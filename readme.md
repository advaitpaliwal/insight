# Insight

Insight uses gemini 1.5 pro to answer questions based on what you see and hear, and it remembers those memories for you.

check demo on [here](https://twitter.com/advaitpaliwal/status/1779697730526310521)

## Hardware Requirements

- Raspberry Pi (model 4 or newer)
- Webcam
- Mini usb mic
- Logitech webcam
- Sony headphones with jack
- needed a monitor, keyboard, and mouse to interface with the pi

## Software Requirements

- pvporcupine
- google-generativeai
- SpeechRecognition
- firebase-admin
- google-cloud-texttospeech
- picamera2

## Setup

1. Clone the repository to your Raspberry Pi or local machine:
   ```
   git clone https://github.com/advaitpaliwal/insight
   ```
2. Install the required dependencies:
   ```
   cd [repo-name]
   pip install -r requirements.txt
   ```
3. Add the neccessary api keys to the config.py file, check config.example.py

## Usage

1. Run the main script:
   ```
   python main.py
   ```

## Configuration

The project's configuration can be modified by editing the `config.example.py` file and saving it as `config.py`.

## License

This project is licensed under the [License Name] - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

@advaitpaliwal
