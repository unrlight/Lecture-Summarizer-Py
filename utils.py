import os
import shutil
from tiktoken import encoding_for_model
import re
import ffmpeg

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

def split_audio_file_into_parts(mp3_audio, max_size_mb=24):
    
    max_size = max_size_mb * 1024 * 1024

    file_size = os.path.getsize(mp3_audio)

    if file_size > max_size:
        num_parts = int((file_size + max_size - 1) // max_size)
    else:
        num_parts = 1

    probe = ffmpeg.probe(mp3_audio)
    duration = float(probe['format']['duration'])

    part_duration = duration / num_parts

    audio_parts = []
    for i in range(num_parts):
        start_time = i * part_duration
        if i == num_parts - 1:
            part_t = duration - start_time
        else:
            part_t = part_duration
        output_file = os.path.join(os.path.dirname(mp3_audio), f'part_{i+1}.mp3')
        (
            ffmpeg
            .input(mp3_audio, ss=start_time, t=part_t)
            .output(output_file, codec='copy')
            .run()
        )
        audio_parts.append(output_file)
        print(f"Создана часть {i+1} с размером {os.path.getsize(output_file) / (1024 * 1024):.2f} МБ")
    return audio_parts

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