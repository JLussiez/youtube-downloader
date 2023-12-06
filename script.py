from pytube import YouTube

def download_and_convert_video(video_url, output_path="."):
    try:
        # Créer un objet YouTube à partir de l'URL
        youtube_video = YouTube(video_url)

        # Récupérer la meilleure résolution disponible
        video_stream = youtube_video.streams.get_highest_resolution()

        # Télécharger la vidéo
        print("Téléchargement de la vidéo...")
        video_stream.download(output_path)
        print("Téléchargement terminé.")

        # Renommer le fichier avec l'extension .mp4
        original_filename = video_stream.title
        new_filename = original_filename + ".mp4"
        new_filepath = f"{output_path}/{new_filename}"

        # Renommer le fichier
        print(f"Conversion en {new_filename}...")
        video_stream.download(output_path, filename=new_filename)
        print(f"Conversion terminée. La vidéo est disponible à l'emplacement : {new_filepath}")

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

if __name__ == "__main__":
    # Exemple d'utilisation
    video_url = input("Veuillez saisir l'URL de la vidéo YouTube : ")
    download_and_convert_video(video_url)
