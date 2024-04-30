import tkinter as tk
from tkinter import ttk
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip
from ttkthemes import ThemedStyle

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Downloader")

        style = ThemedStyle(master)
        style.set_theme("yaru")

        self.label_url = tk.Label(master, text="URL de la vidéo YouTube:")
        self.label_url.grid(row=0, column=0, sticky="w")

        self.entry_url = ttk.Entry(master, width=50, style='My.TEntry')
        self.entry_url.grid(row=0, column=1)

        style.configure('My.TEntry', background='white', foreground='black')

        self.label_format = tk.Label(master, text="Format de sortie: (mp3/mp4)")
        self.label_format.grid(row=1, column=0, sticky="w")

        self.var_format = tk.StringVar(value="mp4")
        self.entry_format = ttk.Entry(master, textvariable=self.var_format)
        self.entry_format.grid(row=1, column=1)

        self.label_quality = tk.Label(master, text="Qualité:")
        self.label_quality.grid(row=2, column=0, sticky="w")

        self.quality_options = ttk.Combobox(master, width=25)
        self.quality_options.grid(row=2, column=1)

        self.button_download = tk.Button(master, text="Télécharger", command=self.download)
        self.button_download.grid(row=3, columnspan=2)

    def download(self):
        video_url = self.entry_url.get()
        output_format = self.var_format.get().lower()
        selected_quality = self.quality_options.get()
        download_and_convert_video(video_url, output_format, selected_quality)

def get_available_qualities(video_url):
    try:
        youtube_video = YouTube(video_url)
        qualities = [stream.resolution for stream in youtube_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')]
        return qualities
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération des qualités : {str(e)}")
        return []

def download_and_convert_video(video_url, output_format="mp4", selected_quality=None):
    try:
        youtube_video = YouTube(video_url)

        if selected_quality:
            video_stream = youtube_video.streams.filter(res=selected_quality, progressive=True, file_extension='mp4').first()
        else:
            video_stream = youtube_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        output_path = os.path.join(os.path.expanduser("~"), "Downloads")

        os.makedirs(output_path, exist_ok=True)

        print("Téléchargement de la vidéo...")
        video_stream.download(output_path)
        print("Téléchargement terminé.")

        if output_format == "mp4":
            original_filename = video_stream.title
            new_filename = original_filename + ".mp4"
            new_filepath = os.path.join(output_path, new_filename)
            print(f"Conversion en {new_filename}...")
            os.rename(os.path.join(output_path, video_stream.default_filename), new_filepath)
            print(f"Conversion terminée. La vidéo est disponible à l'emplacement : {new_filepath}")
        elif output_format == "mp3":
            print("Conversion en MP3...")
            video_clip = VideoFileClip(os.path.join(output_path, video_stream.default_filename))
            audio_clip = video_clip.audio
            if audio_clip:
                audio_filename = video_stream.default_filename.replace(".mp4", ".mp3")
                audio_clip.write_audiofile(os.path.join(output_path, audio_filename))
                audio_clip.close()
                video_clip.close()
                print("Conversion terminée.")
                os.remove(os.path.join(output_path, video_stream.default_filename))
            else:
                print("La vidéo ne contient pas de piste audio.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    app.entry_url.bind("<FocusOut>", lambda event: update_quality_options(app))
    root.mainloop()

def update_quality_options(app):
    video_url = app.entry_url.get()
    qualities = get_available_qualities(video_url)
    app.quality_options['values'] = qualities
    if qualities:
        app.quality_options.current(0)

if __name__ == "__main__":
    main()
