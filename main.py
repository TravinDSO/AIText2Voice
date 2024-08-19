import tkinter as tk
import openai
import subprocess
import os
import webbrowser
from dotenv import load_dotenv
from tkinter import ttk
from tkinter import messagebox

class TextToSpeechApp:
    def __init__(self, root):
        # Load environment variables and initialize the OpenAI client
        load_dotenv('environment.env')
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found in the environment file.")
        
        # Initialize the OpenAI client
        self.openai_client = openai.OpenAI(api_key=self.api_key)

        # Predefined list of available voice types for TTS
        self.voice_types = ['Alloy', 'Echo', 'Fable', 'Onyx', 'Nova', 'Shimmer']

        # Setup the user interface for the application
        self.setup_gui(root)
     
    def setup_gui(self, root):
        # Set the window title
        root.title("Text to Speech Converter")

        # Create and pack the label and text input field for entering the text to convert
        tk.Label(root, text="Enter text to convert to speech (max 300 characters):").pack()
        self.text_entry = tk.Text(root, height=10, width=50)
        self.text_entry.pack(pady=5)

        # Create and pack the label to display the remaining character count
        self.char_count_label = tk.Label(root, text="300")
        self.char_count_label.pack(pady=5)

        # Bind the update_char_count method to key release events in the text entry field
        self.text_entry.bind("<KeyRelease>", self.update_char_count)

        # Add a visual separator in the UI
        ttk.Separator(root, orient="horizontal").pack(fill="x")

        # Create and pack the dropdown for voice selection
        tk.Label(root, text="Select voice type:").pack()
        self.voice_type_var = tk.StringVar(value=self.voice_types[0])  # Set default to the first voice type
        voice_dropdown = ttk.Combobox(root, textvariable=self.voice_type_var, values=self.voice_types, state="readonly")
        voice_dropdown.pack(pady=5)

        # Add another separator in the UI
        ttk.Separator(root, orient="horizontal").pack(fill="x")

        # Create and pack the input field for optional filter complex (with clickable help link)
        complexlabel = tk.Label(root, text="Enter filter complex (not required):", fg="blue", cursor="hand2")
        complexlabel.pack()
        complexlabel.bind("<Button-1>", lambda e: webbrowser.open("https://ffmpeg.org/ffmpeg-filters.html"))

        # Add a small grey and italicized note to provide an example of filter complex
        example_font = ("Helvetica", 8, "italic")
        tk.Label(root, text="Example: atempo=1.0,asetrate=16000,aresample=44100,volume=2", fg="grey", font=example_font).pack()

        # Filter dialog
        self.filter_entry = tk.Entry(root, width=50)
        self.filter_entry.pack(pady=5)

        # Add another separator in the UI
        ttk.Separator(root, orient="horizontal").pack(fill="x")

        # Create and pack the input field for file name with a default value 'output.mp3'
        tk.Label(root, text="Export to:").pack()
        self.filename_entry = tk.Entry(root, width=50)
        self.filename_entry.insert(0, "output.mp3")  # Set default file name
        self.filename_entry.pack(pady=5)

        # Add another separator in the UI
        ttk.Separator(root, orient="horizontal").pack(fill="x")

        # Create and pack the submit button to trigger audio generation
        submit_button = tk.Button(root, text="Generate Audio", command=self.generate_audio)
        submit_button.pack(pady=20)

    def update_char_count(self, event=None):
        # Calculate remaining characters and update the label
        char_count = 300 - len(self.text_entry.get("1.0", tk.END))
        color = "black" if char_count >= 0 else "red"
        self.char_count_label.config(text=f"{abs(char_count)}" if char_count >= 0 else f"Over by: {abs(char_count)}", fg=color)

    def generate_audio(self):
        # Retrieve the user input: text to convert, selected voice, and optional filter
        text = self.text_entry.get("1.0", tk.END).strip()
        selected_voice = self.voice_type_var.get()
        filter_complex = self.filter_entry.get().strip()
        audio_file = self.filename_entry.get().strip()

        # Validate the text and file name
        if len(text) > 300:
            messagebox.showwarning("Input Error", "Text must be less than 300 characters.")
            return

        if not audio_file.endswith(".mp3"):
            messagebox.showwarning("Input Error", "Please enter a valid filename ending with '.mp3'.")
            return

        if not text:
            messagebox.showwarning("Input Error", "Please enter some text to convert to speech.")
            return

        try:
            # Generate TTS audio using the OpenAI API client
            response = self.openai_client.audio.speech.create(
                model="tts-1",  # Specify the TTS model to use
                voice=selected_voice.lower(),  # Convert voice selection to lowercase as required
                input=text,  # Pass the user-input text
            )

            # Save the generated audio content to a file
            with open(audio_file, "wb") as f:
                f.write(response.content)

            # Apply optional audio modulation if a filter was provided
            if filter_complex:
                self.apply_modulation(audio_file, filter_complex)
                messagebox.showinfo("Success", f"Audio generated and saved as '{audio_file}'.")
            else:
                messagebox.showinfo("Success", f"Audio generated and saved as '{audio_file}'.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during audio generation: {e}")

    def apply_modulation(self, audio_file, filter_complex=None):
        # Generate a new filename for the modulated output
        modulated_file = "modulated_" + audio_file

        # If modulated file already exists, remove it
        if os.path.exists(modulated_file):
            os.remove(modulated_file)

        # Execute ffmpeg with the provided filter_complex to apply modulation
        process = subprocess.run([
            "ffmpeg",
            "-i", audio_file,
            "-filter_complex", filter_complex,
            modulated_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the modulated file was created successfully
        if process.returncode == 0 and os.path.exists(modulated_file):
            os.remove(audio_file)  # Remove the original audio file
            os.rename(modulated_file, audio_file)  # Rename the modulated file to the original filename
        else:
            raise RuntimeError("Modulation process failed.")

def main():
    # Create the main window and start the application
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
