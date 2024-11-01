import os
import shutil
from tiktoken import encoding_for_model

max_tokens_per_part = 5000

def save_uploaded_files(files):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_paths = []
    for file in files:
        file_location = f"{upload_dir}/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        file_paths.append(file_location)
    return file_paths

def split_transcript_into_parts(transcript, max_transcript_tokens_per_part):
    encoding = encoding_for_model("gpt-4")
    tokens = encoding.encode(transcript)
    parts = []
    for i in range(0, len(tokens), max_transcript_tokens_per_part):
        part_tokens = tokens[i:i + max_transcript_tokens_per_part]
        part_text = encoding.decode(part_tokens)
        parts.append(part_text)
    return parts

def clean_up_directories(directories):
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
