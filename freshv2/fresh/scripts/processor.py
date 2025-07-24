import os
import config
from transcriber import transcribe_file
from file_utils import find_wav_files

def process_folder(folder_path, output_folder=config.PROCESSED_BASE):
    wav_files = find_wav_files(folder_path)
    if not wav_files:
        print(f"No .wav files found in {folder_path} or its Voice subfolder.")
        return

    transcripts = []
    for wav in wav_files:
        print(f"Transcribing {wav} ...")
        text = transcribe_file(wav)
        transcripts.append((wav, text))

    # Ensure the output directory exists before writing
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, os.path.basename(folder_path) + "_transcripts.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for wav, text in transcripts:
            f.write(f"{os.path.basename(wav)}\t{text}\n")

    print(f"Saved transcripts to {output_file}")
