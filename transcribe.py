import os
import ffmpeg
import whisper
from datetime import datetime
from pathlib import Path

def transcribe_audio_files(files, language, model_size):
    transcript = ""
    is_text_file_present = False

    for file in files:
        extension = os.path.splitext(file)[-1].lower()
        if extension == '.txt':
            is_text_file_present = True
            transcript_file = file
            break

    if is_text_file_present:
        file = open(transcript_file, "r", encoding="utf-8")
        transcript = file.read()
        file.close()
    else:
        model = whisper.load_model(model_size)
        temp_dir = './temp'
        os.makedirs(temp_dir, exist_ok=True)
        audio_files = []

        for file in files:
            extension = os.path.splitext(file)[-1].lower()
            if extension == '.mp4':
                wav_file = os.path.join(temp_dir, f"{Path(file).stem}.wav")
                ffmpeg.input(file).output(wav_file, format='wav').run()
                audio_files.append(wav_file)
            elif extension in ['.mp3', '.wav']:
                audio_files.append(file)
            else:
                print(f"Неподдерживаемый формат файла: {extension}")
                continue

        if len(audio_files) > 1:
            combined_wav = os.path.join(temp_dir, 'combined.wav')
            inputs = [ffmpeg.input(f) for f in audio_files]
            ffmpeg.concat(*inputs, v=0, a=1).output(combined_wav, acodec='pcm_s16le').run()
            final_audio = combined_wav
        else:
            final_audio = audio_files[0]

        result = model.transcribe(audio=final_audio, language=language, verbose=False)
        transcript = result.get('text', '')

    output_dir = './output_transcribed'
    os.makedirs(output_dir, exist_ok=True)
    current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    with open(f"{output_dir}/transcript_{current_time}.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    return transcript
