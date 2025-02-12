import whisper
from datetime import timedelta
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import librosa

# Configuration des langues
LANGUAGES = {
    "Français": "fr",
    "Anglais": "en",
    "Espagnol": "es",
    "Allemand": "de",
    "Italien": "it",
    "Japonais": "ja"
}

def sec_to_srt(time_sec):
    """Convertit des secondes en format temps SRT (HH:MM:SS,mmm)"""
    td = timedelta(seconds=time_sec)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    milliseconds = td.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        root.title("Subbiden")
        root.geometry("500x300")

        # Style
        style = ttk.Style()
        style.theme_use('clam')

        # Widgets
        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(expand=True, fill='both')

        self.btn_choose = ttk.Button(self.frame, text="Choisir un fichier audio", command=self.choose_file)
        self.btn_choose.grid(row=0, column=0, pady=10, sticky='ew')

        self.lang_label = ttk.Label(self.frame, text="Langue de sortie :")
        self.lang_label.grid(row=1, column=0, pady=5, sticky='w')

        self.lang_var = tk.StringVar()
        self.lang_selector = ttk.Combobox(self.frame,
                                        textvariable=self.lang_var,
                                        values=list(LANGUAGES.keys()),
                                        state="readonly")
        self.lang_selector.set("Anglais")
        self.lang_selector.grid(row=2, column=0, pady=5, sticky='ew')

        self.progress = ttk.Progressbar(self.frame, mode='determinate')
        self.status_label = ttk.Label(self.frame, text="Prêt")
        self.status_label.grid(row=4, column=0, pady=10)

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionnez un fichier audio",
            filetypes=[("Fichiers audio", "*.mp3 *.wav *.m4a *.ogg")]
        )
        if file_path:
            self.start_transcription(file_path)

    def start_transcription(self, audio_path):
        self.progress.grid(row=3, column=0, pady=10, sticky='ew')
        self.progress['value'] = 0
        self.status_label.config(text="Initialisation...")

        thread = threading.Thread(target=self.run_transcription, args=(audio_path,))
        thread.start()

    def run_transcription(self, audio_path):
        try:
            # Configuration langue
            lang_code = LANGUAGES.get(self.lang_var.get(), "en")
            task = "translate" if lang_code == "en" else "transcribe"

            # Chargement du modèle
            self.update_status("Chargement du modèle Whisper...")
            model = whisper.load_model("medium")

            # Calcul de la durée totale
            audio, sr = librosa.load(audio_path, sr=None)
            duration = librosa.get_duration(y=audio, sr=sr)
            self.root.after(0, lambda: self.progress.configure(maximum=duration))


            # Suppression du callback
            self.update_status("Analyse de l'audio en cours...")
            result = model.transcribe(
                audio_path,
                task=task,
                language=lang_code if lang_code != "en" else None
            )

            # Génération SRT
            srt_filename = audio_path.rsplit('.', 1)[0] + ".srt"
            self.generate_srt(result["segments"], srt_filename)

            self.update_status(f"Terminé ! Fichier créé : {srt_filename}", success=True)

        except Exception as e:
            self.update_status(f"Erreur : {str(e)}", error=True)
        finally:
            self.root.after(0, self.progress.grid_remove)

    def generate_srt(self, segments, filename):
        with open(filename, "w", encoding="utf-8") as srt_file:
            for i, segment in enumerate(segments, start=1):
                start = sec_to_srt(segment["start"])
                end = sec_to_srt(segment["end"])
                text = segment["text"].strip()
                srt_file.write(f"{i}\n{start} --> {end}\n{text}\n\n")


    def update_progress(self, segment):
        end_time = segment.get("end", 0)
        self.root.after(0, lambda: self.progress.configure(value=end_time))

    def update_status(self, message, success=False, error=False):
        self.root.after(0, lambda: self.status_label.config(
            text=message,
            foreground=("green" if success else ("red" if error else "black"))
        ))

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
