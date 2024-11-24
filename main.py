import os
import uvicorn
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from utils import save_uploaded_files, clean_up_directories
from transcribe import transcribe_audio_files
from summarize import summarize_transcript, summarize_with_openai_api, summarize_with_ollama_api

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
output_dir = './output_summarized'

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/step2", response_class=HTMLResponse)
def step2(request: Request, files: list[UploadFile] = File(...)):
    uploaded_file_paths = save_uploaded_files(files)
    session_data['files'] = uploaded_file_paths
    return templates.TemplateResponse("step2.html", {"request": request})

@app.post("/step3", response_class=HTMLResponse)
def step3(
    request: Request,
    language: str = Form(...),
    display_language: str = Form(...),
    model_size: str = Form(...),
    max_attempts: int = Form(...),
    model_type: str = Form(...)
):
    session_data['language'] = language
    session_data['display_language'] = display_language
    session_data['model_size'] = model_size
    session_data['max_attempts'] = int(max_attempts)
    session_data['model_type'] = model_type
    return templates.TemplateResponse("step3.html", {"request": request})

@app.get("/process", response_class=HTMLResponse)
def process(request: Request):
    files = session_data.get('files', [])
    language = session_data.get('language', 'ru')
    display_language = session_data.get('display_language', 'ru')
    model_size = session_data.get('model_size', 'small')
    max_attempts = session_data.get('max_attempts', 3)
    model_type = session_data.get('model_type', 'gemini')

    transcript = transcribe_audio_files(files, language, model_size)
    
    if model_type == "gemini":
        summary = summarize_transcript(transcript, language, display_language, max_attempts)
    elif model_type == "qwen2.5":
        summary = summarize_with_ollama_api(transcript, language, display_language, max_attempts)
    else:
        summary = summarize_with_openai_api(transcript, model_type, language, display_language, max_attempts)

    current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/summary_{current_time}.md", "w", encoding="utf-8") as f:
        f.write(summary)

    clean_up_directories(['uploads', 'temp'])

    return templates.TemplateResponse("step4.html", {"request": request, "summary": summary})

@app.get("/reset", response_class=HTMLResponse)
def reset(request: Request):
    global session_data
    session_data = {}
    clean_up_directories(['uploads', 'temp'])
    return RedirectResponse(url="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
