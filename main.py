import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
import whisper
import ffmpeg
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import tiktoken
from fastapi.staticfiles import StaticFiles
from datetime import datetime

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_data = {}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/step2", response_class=HTMLResponse)
async def step2(request: Request, files: list[UploadFile] = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    session_data['files'] = []
    for file in files:
        file_location = f"{upload_dir}/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        session_data['files'].append(file_location)
    return templates.TemplateResponse("step2.html", {"request": request})

@app.post("/step3", response_class=HTMLResponse)
async def step3(
    request: Request,
    language: str = Form(...),
    model_size: str = Form(...),
    max_attempts: int = Form(...)
):
    session_data['language'] = language
    session_data['model_size'] = model_size
    session_data['max_attempts'] = int(max_attempts)
    return templates.TemplateResponse("step3.html", {"request": request})

@app.get("/process", response_class=HTMLResponse)
async def process(request: Request):
    files = session_data.get('files', [])
    language = session_data.get('language', 'ru')
    model_size = session_data.get('model_size', 'small')

    transcript = ""
    is_text_file = False
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext == '.txt':
            is_text_file = True
            with open(file, "r", encoding="utf-8") as f:
                transcript = f.read()
            break

    if not is_text_file:
        model = whisper.load_model(model_size)
        TEMP_DIR = './temp'
        os.makedirs(TEMP_DIR, exist_ok=True)
        audio_files = []

        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext == '.mp4':
                wav_file = os.path.join(TEMP_DIR, f"{Path(file).stem}.wav")
                ffmpeg.input(file).output(wav_file, format='wav').run()
                audio_files.append(wav_file)
            elif ext in ['.mp3', '.wav']:
                audio_files.append(file)
            else:
                return HTMLResponse(f"Неподдерживаемый формат файла: {ext}", status_code=400)

        if len(audio_files) > 1:
            final_wav = os.path.join(TEMP_DIR, 'combined.wav')
            inputs = [ffmpeg.input(f) for f in audio_files]
            ffmpeg.concat(*inputs, v=0, a=1).output(final_wav, acodec='pcm_s16le').run()
        else:
            final_wav = audio_files[0]

        result = model.transcribe(audio=final_wav, language=language, verbose=False)
        transcript = result.get('text', '')

    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    with open(f"{output_dir}/transcript_{current_time}.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    genai.configure(api_key=os.environ.get("gemini_api_keys"))

    with open("example.txt", "r", encoding="utf-8") as file:
        lectureExample = file.read()

    base_prompt = f"""
        Я дам тебе лекцию, распознанную при помощи Whisper.
        Ты обязан сделать подробный пересказ всей лекции.
        Ты обязан сделать максимально подробный пересказ всей лекции. Каждый раздел должен быть глубоко разобран и расширен до максимального уровня детализации, чтобы итоговый пересказ был длинным и полным.
        Вся лекция должна быть в твоём контекстом окне.
        Для пересказа ты определяешь все темы и подтемы и каждую из них очень подробно разбираешь.
        Не должно быть так, чтобы в подтеме было только одно предложение.
        Очень важно, чтобы одна тема подводила к другой. То есть важно, чтобы тема не была простым перечислением терминов, а имела осмысленное подведение к основным данным темы.
        Я предпочитаю более длинные и более подробные ответы.

        Вот хороший пример пересказанной лекции:
        {lectureExample}\n
        """

    if language == 'en':
        base_prompt += "Ты должен ответить на русском языке.\n"

    additional_prompt = """
        Текст лекции, которую нужно пересказать:
        {part}\n

        Текст пересказа:
        """

    encoding = tiktoken.encoding_for_model("gpt-4")

    tokens_in_base_prompt = len(encoding.encode(base_prompt))
    tokens_in_additional_prompt = len(encoding.encode(additional_prompt.format(part="")))

    max_total_tokens = 14000
    max_transcript_tokens_per_part = max_total_tokens - tokens_in_base_prompt - tokens_in_additional_prompt

    tokens_in_transcript = len(encoding.encode(transcript))

    print(f"Токенов в базовом промпте: {tokens_in_base_prompt}")
    print(f"Токенов в дополнительном промпте: {tokens_in_additional_prompt}")
    print(f"Максимум токенов на часть транскрипта: {max_transcript_tokens_per_part}")
    print(f"Всего токенов в транскрипте: {tokens_in_transcript}")

    outputs = []
    if tokens_in_base_prompt + tokens_in_additional_prompt + tokens_in_transcript <= max_total_tokens:
        print("Общее количество токенов меньше или равно 14,000, используем gemini-1.5-pro-002")
        max_attempts = 1
        model_name = "gemini-1.5-pro-002"
        parts = [transcript]
    else:
        print("Общее количество токенов превышает 14,000, делим транскрипт и используем gemini-1.5-flash")
        max_attempts = session_data.get('max_attempts', 3)
        model_name = "gemini-1.5-flash"

        transcript_tokens = encoding.encode(transcript)
        parts = []
        start_idx = 0
        while start_idx < len(transcript_tokens):
            end_idx = start_idx + max_transcript_tokens_per_part
            if end_idx > len(transcript_tokens):
                end_idx = len(transcript_tokens)
            part_tokens = transcript_tokens[start_idx:end_idx]
            part_text = encoding.decode(part_tokens)
            parts.append(part_text)
            start_idx = end_idx

        print(f"Транскрипт разделён на {len(parts)} частей.")

    for idx, part in enumerate(parts, start=1):
        prompt = base_prompt + additional_prompt.format(part=part)
        num_tokens = len(encoding.encode(prompt))
        print(f"Общее количество токенов для части {idx}: {num_tokens}")

        max_output_tokens = 8192

        max_tokens = 0
        best_output = ""
        for attempt in range(max_attempts):
            print(f"Генерация для части {idx}, попытка {attempt + 1}")
            model_gen = genai.GenerativeModel(
                model_name=model_name
            )
            chat = model_gen.start_chat(
                history=[
                    {"role": "user", "parts": "Здравствуй!"},
                    {"role": "model", "parts": "Здравствуй, чем могу помочь?"},
                ],
            )
            response = chat.send_message(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_output_tokens,
                    temperature=1.5
                ),
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
                }
            ).text

            num_tokens_output = len(encoding.encode(response))
            print(f"Токенов в ответе для части {idx}: {num_tokens_output}")
            if num_tokens_output > max_tokens:
                max_tokens = num_tokens_output
                best_output = response

        outputs.append(f"# {idx} часть текста:\n\n{best_output}\n\n")

    max_output = "".join(outputs)

    output_dir = './output_recognized'
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/summary_{current_time}.md", "w", encoding="utf-8") as f:
        f.write(max_output)

    if os.path.exists('uploads'):
        shutil.rmtree('uploads')
    if os.path.exists('temp'):
        shutil.rmtree('temp')

    return templates.TemplateResponse("step4.html", {"request": request, "summary": max_output})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
