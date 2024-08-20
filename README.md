# AIText2Voice

This is a simple Text-to-speech (TTS) application built using Python's `tkinter` library and OpenAI's API for text-to-speech conversion. It allows users to input text, select a voice, and generate audio files in MP3 format. Users can also apply optional audio filters using `ffmpeg`.

<a href="https://www.buymeacoffee.com/travin" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

<img src="./images/screenshot.png?raw=true" alt="Screenshot of AIText2Voice App" width="40%">

## Features
- Convert text (up to 500 characters) to speech using OpenAI's TTS models.
- Choose from multiple voice types.
- Apply custom `ffmpeg` filters to the generated audio.
- Export audio as an MP3 file.

## Requirements
- Python 3.7+
- Dependencies listed in `requirements.txt`
- `ffmpeg` is installed and is available in your system's PATH.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/TravinDSO/AIText2Voice.git
    cd AIText2Voice
    ```
``
2. **Install required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
    - Create a `.env` file in the project directory with the following variables:
    ```plaintext
    USE_AZURE=False
    OPENAI_API_KEY=your_openai_api_key
    OPENAI_API_TTS_MODEL=your_openai_tts_model_name

    # If using Azure:
    USE_AZURE=True
    AZURE_OPENAI_API_KEY=your_azure_openai_api_key
    AZURE_OPENAI_API_VERSION=your_azure_openai_api_version
    AZURE_OPENAI_API_ENDPOINT=your_azure_openai_api_endpoint
    AZURE_OPENAI_API_TTS_MODEL=your_azure_openai_tts_model_name
    ```

4. **Ensure `ffmpeg` is installed:**
    - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your PATH.
    - macOS: Install via Homebrew:
      ```bash
      brew install ffmpeg
      ```
    - Linux: Install via your package manager, e.g., on Ubuntu:
      ```bash
      sudo apt-get install ffmpeg
      ```

## Usage

1. **Run the application:**
    ```bash
    python main.py
    ```

2. **Using the GUI:**
    - Enter text (up to 500 characters).
    - Choose a voice from the dropdown.
    - Optionally, enter a filter complex string for audio modulation.
    - Click "Generate Audio" to create and save the MP3 file.

3. **Generated Audio:**
    - The generated audio will be saved to the specified file name (default is `output.mp3`).
    - If you apply a filter, the modulated audio will overwrite the original file.

## Troubleshooting

- Ensure the `.env` file is correctly set up with valid API keys.
- Make sure `ffmpeg` is correctly installed and added to your PATH.
- Check for any error messages in the application to troubleshoot issues.
