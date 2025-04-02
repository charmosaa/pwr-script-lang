import os
import sys
import utils
import subprocess
import argparse

# Rozszerzone funkcje do konwersji plików
def convert_video_or_audio(file_path, output_format, output_dir):
    timestamp = utils.get_timestamp()
    filename = os.path.basename(file_path)
    name, _ = os.path.splitext(filename)
    output_file = os.path.join(output_dir, f"{timestamp}-{name}.{output_format}")
    command = ["ffmpeg", "-i", file_path, output_file]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_file, "ffmpeg"
    except subprocess.CalledProcessError as e:
        print(f"Error converting {file_path}: {e}")
        return None, None

def convert_image(file_path, output_format, output_dir):
    timestamp = utils.get_timestamp()
    filename = os.path.basename(file_path)
    name, _ = os.path.splitext(filename)
    output_file = os.path.join(output_dir, f"{timestamp}-{name}.{output_format}")
    command = ["magick", file_path, output_file]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_file, "magick"
    except subprocess.CalledProcessError as e:
        print(f"Error converting {file_path}: {e}")
        return None, None

# Funkcja główna
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", "-d", default=os.getcwd(), help="Directory with media files")
    parser.add_argument("--output_vid", "-ov", default="webm", help="Output video file format")
    parser.add_argument("--output_img", "-oi", default="png", help="Output image file format")
    args = parser.parse_args()

    # Ścieżka do katalogu wejściowego
    args.directory = utils.get_full_path(args.directory)

    if not os.path.exists(args.directory) or not os.path.isdir(args.directory):
        sys.stderr.write("Invalid directory path\n")
        sys.exit(1)

    # Pobieranie ścieżki do folderu, w którym mają być zapisane pliki wynikowe
    output_dir = utils.get_converted_dir()

    # Tworzymy folder, jeśli nie istnieje
    utils.ensure_directory_exists(output_dir)

    # Historia konwersji
    history_file = os.path.join(output_dir, "history.json")

    # Rozszerzenia plików audio, wideo i obrazów
    VIDEO_AUDIO_EXTENSIONS = {".mp4", ".mp3", ".avi", ".mov", ".wav", ".mkv", ".webm"}
    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}

    # Wyszukiwanie plików do konwersji
    for file in os.listdir(args.directory):
        file_path = os.path.join(args.directory, file)
        file_extension = os.path.splitext(file)[1].lower()

        # Jeśli plik to obraz
        if file_extension in IMAGE_EXTENSIONS:
            output_file, program_used = convert_image(file_path, args.output_img, output_dir)
            output_format = args.output_img
        # Jeśli plik to audio lub wideo
        elif file_extension in VIDEO_AUDIO_EXTENSIONS:
            output_file, program_used = convert_video_or_audio(file_path, args.output_vid, output_dir)
            output_format = args.output_vid
        else:
            continue  # Pomijamy pliki nie będące obrazami, audio lub wideo

        if output_file:
            # Logujemy informację o konwersji (dodajemy użyty program)
            utils.log_conversion(history_file, file_path, output_format, output_file, program_used)
            print(f"Converted: {file_path} -> {output_file} using {program_used}")

if __name__ == "__main__":
    main()
