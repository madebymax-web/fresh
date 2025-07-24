import os

def find_wav_files(base_folder):
    wav_files = []

    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.lower().endswith(".wav"):
                wav_files.append(os.path.join(root, file))

    if not wav_files:
        voice_folder = os.path.join(base_folder, "Voice")
        if os.path.isdir(voice_folder):
            for root, dirs, files in os.walk(voice_folder):
                for file in files:
                    if file.lower().endswith(".wav"):
                        wav_files.append(os.path.join(root, file))

    return wav_files
