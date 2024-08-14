import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import openai
import subprocess
import os
import time
from dotenv import load_dotenv

class TextToSpeechApp:
    def __init__(self, root):
        # Load environment variables
        load_dotenv('environment.env')
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found in the environment file.")
        
        # Initialize the OpenAI client
        self.openai_client = openai.OpenAI(api_key=self.api_key)

        self.voice_types = ["Alloy", "Amber", "Sage", "Jade"]

        self.setup_gui(root)

    def setup_gui(self, root):
        root.title("Text to Speech Converter")

        # Create the text input field
        tk.Label(root, text="Enter text to convert to speech:").pack(pady=10)
        self.text_entry = tk.Text(root, height=10, width=50)
        self.text_entry.pack(pady=10)

        # Create the dropdown for voice selection
        tk.Label(root, text="Select voice type:").pack(pady=10)
        self.voice_type_var = tk.StringVar(value=self.voice_types[0])
        voice_dropdown = ttk.Combobox(root, textvariable=self.voice_type_var, values=self.voice_types, state="readonly")
        voice_dropdown.pack(pady=10)

        # Volume control slider
        tk.Label(root, text="Volume (0.5 - 2.0):").pack(pady=5)
        self.volume_var = tk.DoubleVar(value=1.0)
        volume_slider = tk.Scale(root, variable=self.volume_var, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
        volume_slider.pack(pady=5)

        # Pitch control slider
        tk.Label(root, text="Pitch Shift (0.5x - 2.0x):").pack(pady=5)
        self.pitch_var = tk.DoubleVar(value=0.0)
        pitch_slider = tk.Scale(root, variable=self.pitch_var, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
        pitch_slider.pack(pady=5)

        # Tempo control slider
        tk.Label(root, text="Tempo (0.5x - 2.0x):").pack(pady=5)
        self.tempo_var = tk.DoubleVar(value=1.0)
        tempo_slider = tk.Scale(root, variable=self.tempo_var, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
        tempo_slider.pack(pady=5)

        # Create the submit button
        submit_button = tk.Button(root, text="Generate Audio", command=self.generate_audio)
        submit_button.pack(pady=20)

    def generate_audio(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        selected_voice = self.voice_type_var.get()
        volume = self.volume_var.get()
        pitch = self.pitch_var.get()
        tempo = self.tempo_var.get()

        if not text:
            messagebox.showwarning("Input Error", "Please enter some text to convert to speech.")
            return

        try:
            # Generate TTS audio using OpenAI client
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice=selected_voice.lower(),
                input=text,
            )

            audio_file = "output.mp3"
            with open(audio_file, "wb") as f:
                f.write(response.content)

            # Apply modulation
            self.apply_modulation(audio_file, volume, pitch, tempo)

            messagebox.showinfo("Success", "Audio generated and saved as 'output.mp3'.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def apply_modulation(self, audio_file, volume, pitch, tempo):
        modulated_file = "modulated_" + audio_file

        filter_complex = f"volume={volume},asetrate=44100*{pitch},atempo={tempo}"

        # Use Popen to run ffmpeg with more control over the process
        process = subprocess.Popen([
            "ffmpeg",
            "-i", audio_file,
            "-filter_complex", filter_complex,
            modulated_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to complete
        process.communicate()

        # Ensure the process has fully terminated
        process.wait()

        # Wait for a moment to ensure the file is released
        time.sleep(0.5)

        # Ensure all operations on audio_file are complete
        if os.path.exists(audio_file):
            try:
                os.remove(audio_file)
            except PermissionError:
                # If the file is still locked, introduce a slight delay and try again
                time.sleep(0.5)
                os.remove(audio_file)

        # Rename the modulated file to the original filename
        os.rename(modulated_file, audio_file)

def main():
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
