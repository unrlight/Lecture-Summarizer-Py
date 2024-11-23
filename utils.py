import os
import shutil
from tiktoken import encoding_for_model
import re

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
    encoding = encoding_for_model("gpt-3.5")
    tokens = encoding.encode(transcript)
    total_tokens = len(tokens)
    print(f"Количество токенов в транскрипте: {total_tokens}")
    
    if total_tokens <= max_transcript_tokens_per_part:
        return [transcript]
    
    num_parts = (total_tokens + max_transcript_tokens_per_part - 1) // max_transcript_tokens_per_part
    
    part_size = total_tokens // num_parts
    
    parts = []
    for i in range(num_parts):
        start_idx = i * part_size
        end_idx = min((i + 1) * part_size, total_tokens)
        part_tokens = tokens[start_idx:end_idx]
        part_text = encoding.decode(part_tokens)
        parts.append(part_text)
        print(f"Количество токенов в части {i + 1}: {len(part_tokens)}")
    
    return parts

def clean_up_directories(directories):
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)

def markdown_math_fix(text_input):
    text_output = re.sub(r'\\\([ \t]*', r'$', text_input)
    text_output = re.sub(r'[ \t]*\\\)', r'$', text_output)
    text_output = re.sub(r'\\\[[ \t]*', r'$$', text_output)
    text_output = re.sub(r'[ \t]*\\\]', r'$$', text_output)
    
    return text_output