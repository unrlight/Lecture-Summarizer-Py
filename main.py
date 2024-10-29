import os
import shutil
import time
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
import whisper
import ffmpeg
from whisper.utils import get_writer
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import tiktoken
from fastapi.staticfiles import StaticFiles

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
    with open(f"{output_dir}/transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    genai.configure(api_key=os.environ.get("gemini_api_keys"))

    with open("example.txt", "r", encoding="utf-8") as file:
        lectureExample = file.read()

    systemprompt = ""

    prompt = f"""
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
        prompt += "Ты должен ответить на русском языке.\n"

    prompt += f"""
Текст лекции, которую нужно пересказать:
{transcript}\n

Текст пересказа:
"""

    encoding = tiktoken.encoding_for_model("gpt-4")
    num_tokens = len(encoding.encode(systemprompt)) + len(encoding.encode(prompt))
    print(f"Количество input токенов: {num_tokens}")

    if num_tokens > 0: # temp solution
        sleep_flag = True
    else:
        sleep_flag = False

    model_gen = genai.GenerativeModel(
        model_name="gemini-1.5-pro-002"
    )

    max_attempts = session_data.get('max_attempts', 3)
    output = []
    max_tokens = 0
    max_output = ""

    for attempt in range(max_attempts):
        print(f"Попытка генерации: {attempt + 1}")
        chat = model_gen.start_chat(
            history=[
                {"role": "user", "parts": "Здравствуй!"},
                {"role": "model", "parts": "Здравствуй, чем могу помочь?"},
            ],
        )
        response = chat.send_message(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=8192,
                temperature=1.5
            ),
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
            }
        ).text
        output.append(response)

        num_tokens_output = len(encoding.encode(response))
        print(f"Количество output токенов: {num_tokens_output}")
        if num_tokens_output > max_tokens:
            max_tokens = num_tokens_output
            max_output = response

        if sleep_flag:
            print("Засыпаем на 65 секунд...")
            time.sleep(65)

    output_dir = './output_recognized'
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/summary.md", "w", encoding="utf-8") as f:
        f.write(max_output)

    shutil.rmtree('uploads')
    shutil.rmtree('temp')

    return templates.TemplateResponse("step4.html", {"request": request, "summary": max_output})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)