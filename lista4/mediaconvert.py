import os
import sys
import utils
import subprocess
import argparse

VIDEO_AUDIO_EXTENSIONS = {".mp4", ".mp3", ".avi", ".mov", ".wav", ".mkv", ".webm"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}


def convert_media(file_path, output_dir, output_vid, output_img):
    timestamp = utils.get_timestamp()
    filename = os.path.basename(file_path)
    name, _ = os.path.splitext(filename)
    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension in IMAGE_EXTENSIONS:
        output_format = output_img
        output_file = os.path.join(output_dir, f"{timestamp}-{name}.{output_format}")
        program_used = "magick"
        command = [program_used, file_path, output_file]
   
    elif file_extension in VIDEO_AUDIO_EXTENSIONS:
        output_format = output_vid
        output_file = os.path.join(output_dir, f"{timestamp}-{name}.{output_format}")
        program_used = "ffmpeg"
        command = [program_used, "-i", file_path, output_file]
    else:
        return None,None, None
    
    # running subprocess for media files
    result = subprocess.run(command, check=True, capture_output=True)
    if result.returncode == 0:    
        return output_file, output_format, program_used
    else:
        print(f"Error processing {file_path}: {result.stderr}")
        return None, None, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", "-d", default=os.getcwd(), help="Directory with media files")
    parser.add_argument("--output_vid", "-ov", default="webm", help="Output video file format")
    parser.add_argument("--output_img", "-oi", default="png", help="Output image file format")
    args = parser.parse_args()

    # complete path to directory with media/image files
    args.directory = utils.get_full_path(args.directory)

    if not os.path.exists(args.directory) or not os.path.isdir(args.directory):
        sys.stderr.write("Invalid directory path\n")
        sys.exit(1)

    # path to directory to store the results
    output_dir = utils.get_converted_dir()

    # create directory if not existing
    utils.ensure_directory_exists(output_dir)

    # path to history file
    history_file = os.path.join(output_dir, "history.json")

    # converting files from directory
    for file in os.listdir(args.directory):
        file_path = os.path.join(args.directory, file)
        
        output_file, output_format, program_used = convert_media(file_path, output_dir, args.output_vid, args.output_img)

        # log in history file if success
        if output_file:
            utils.log_conversion(history_file, file_path, output_format, output_file, program_used)
            print(f"Converted: {file_path} -> {output_file} using {program_used}")

if __name__ == "__main__":
    main()
