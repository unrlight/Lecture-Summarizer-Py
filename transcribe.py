import os
import ffmpeg
import whisper
from datetime import datetime
from pathlib import Path

def transcribe_audio_files(files, language, model_size):
    transcript = ""
    temp_dir = './temp'
    os.makedirs(temp_dir, exist_ok=True)
    text_files = []
    audio_files = []

    for file in files:
        extension = os.path.splitext(file)[-1].lower()
        if extension in ['.txt', '.srt']:
            text_files.append(file)
        elif extension in ['.mp3', '.wav', '.mp4']:
            audio_files.append(file)
        else:
            print(f"Unsupported file format: {extension}")

    if text_files:
        combined_text = ""
        for text_file in text_files:
            with open(text_file, "r", encoding="utf-8") as f:
                combined_text += f.read() + "\n"
        transcript = combined_text

    if audio_files:
        model = whisper.load_model(model_size)
        audio_paths = []

        for file in audio_files:
            extension = os.path.splitext(file)[-1].lower()
            if extension == '.mp4':
                wav_file = os.path.join(temp_dir, f"{Path(file).stem}.wav")
                ffmpeg.input(file).output(wav_file, format='wav').run()
                audio_paths.append(wav_file)
            elif extension in ['.mp3', '.wav']:
                audio_paths.append(file)

        if len(audio_paths) > 1:
            combined_audio = os.path.join(temp_dir, 'combined.wav')
            inputs = [ffmpeg.input(f) for f in audio_paths]
            ffmpeg.concat(*inputs, v=0, a=1).output(combined_audio, acodec='pcm_s16le').run()
            final_audio = combined_audio
        else:
            final_audio = audio_paths[0]

        result = model.transcribe(audio=final_audio, language=language, verbose=False)
        audio_transcript = result.get('text', '')

        transcript += "\n" + audio_transcript

    output_dir = './output_transcribed'
    os.makedirs(output_dir, exist_ok=True)
    current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    with open(f"{output_dir}/transcript_{current_time}.txt", "w", encoding="utf-8") as f:
        f.write(transcript.strip())

    if os.path.exists(temp_dir):
        for temp_file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, temp_file))
        os.rmdir(temp_dir)

    return transcript