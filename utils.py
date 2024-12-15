import os
import shutil
from tiktoken import encoding_for_model
import re
import ffmpeg
from prompts import *

max_tokens_per_part = 5000

def save_output(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        with open("debug_prompt.txt", "a", encoding="utf-8") as myfile:
            myfile.write(result)
        return result
    return wrapper

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

def split_transcript_into_parts(transcript, max_transcript_tokens_per_part, model):

    if model == "gpt-4o-mini" or "gpt-4o":
        encoding = encoding_for_model("gpt-4o")
    else:
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

@save_output
def prompt_constructor(input_language, display_language, part_number, part_text, model, context, parts_count):
    output_prompt = ""

    print(f"Создание промпта для части {part_number} из {parts_count}")

    ru_note = """**Примечание:** Пожалуйста, внимательно следуй всем указанным требованиям,
чтобы пересказ получился максимально информативным и соответствующим заданию.\n"""

    ru_first_part_info = f"""**Важно!** Строй повествование и пересказ с учетом того, что ты пересказываешь 1 часть из {parts_count}.
Ты обязан не делать заключение в этой части по причине того, что ты делаешь только 1 часть пересказа\n"""

    ru_last_part_info = f"""**Важно!** Строй повествование и пересказ с учетом того, что ты пересказываешь последнюю часть из {parts_count}.
Ты завершаешь пересказ лекции, поэтому ты не можешь начать делать введение.
Твоей задачей будет сделать пересказ последней части, а также сделать итоги и выводы всего пересказа.\n"""

    ru_middle_part_info = f"""**Важно!** Строй повествование и пересказ с учетом того, что ты пересказываешь {part_number} часть из {parts_count}.
Ты продолжаешь пересказ лекции, поэтому ты не можешь начать делать общее введение и общие выводы.
Твоей задачей будет сделать пересказ текущей части\n"""

    en_note = """**Note:** Please follow all the requirements carefully to ensure the summary is as informative and appropriate to the assignment as possible.\n"""

    en_first_part_info = f"""**Important!** Construct the narrative and summary with the understanding that you are summarizing part 1 of {parts_count}.
You must not draw conclusions in this part, as you are only making the first segment of the summary.\n"""

    en_last_part_info = f"""**Important!** Construct the narrative and summary with the understanding that you are summarizing the last part of {parts_count}.
You are finishing the summary of the lecture, so you cannot start making an introduction.
Your task is to summarize this final part and also provide overall conclusions and final insights.\n"""

    en_middle_part_info = f"""**Important!** Construct the narrative and summary with the understanding that you are summarizing part {part_number} of {parts_count}.
You are continuing the summary of the lecture, so you cannot start making a general introduction or conclusions.
Your task is to summarize the current part.\n"""

    if model == "gpt-4o":
        context_for_prompt = context[-1] if context else ""
        ru_context_text = f"Вот пересказ только прошлой части тебе для контекста:\n {context_for_prompt}\n"
        en_context_text = f"Here is only the summary of the previous part for your context:\n {context_for_prompt}\n"
    elif model == "gpt-4o-mini":
        full_context = "\n".join(context) if context else ""
        ru_context_text = f"Вот пересказы предыдущих частей тебе для контекста:\n {full_context}\n"
        en_context_text = f"Here are the summaries of the previous parts for your context:\n {full_context}\n"
    else:
        context_for_prompt = context[-1] if context else ""
        ru_context_text = f"Вот пересказ только прошлой части тебе для контекста:\n {context_for_prompt}\n"
        en_context_text = f"Here is only the summary of the previous part for your context:\n {context_for_prompt}\n"

    if input_language == "ru":
        if model == "gpt-4o" or model == "gpt-4o-mini":
            if parts_count > 1:
                if part_number == 1:
                    output_prompt = (
                        f"{openai_ru_prompt}\n{part_text}\n"
                        "---\n"
                        f"{ru_note}"
                        "---\n"
                        f"{ru_first_part_info}"
                    )
                elif part_number == parts_count:
                    output_prompt = (
                        f"{openai_ru_prompt}\n{part_text}\n"
                        "---\n"
                        f"{ru_note}"
                        "---\n"
                        f"{ru_last_part_info}"
                        "---\n"
                        f"{ru_context_text}"
                    )
                else:
                    output_prompt = (
                        f"{openai_ru_prompt}\n{part_text}\n"
                        "---\n"
                        f"{ru_note}"
                        "---\n"
                        f"{ru_middle_part_info}"
                        "---\n"
                        f"{ru_context_text}"
                    )
            else:
                output_prompt = (
                    f"{openai_ru_prompt}\n{part_text}\n"
                    "---\n"
                    f"{ru_note}"
                )

    elif input_language == "en":
        if model == "gpt-4o" or model == "gpt-4o-mini":
            if parts_count > 1:
                if part_number == 1:
                    output_prompt = (
                        f"{openai_en_prompt}\n{part_text}\n"
                        "---\n"
                        f"{en_note}"
                        "---\n"
                        f"{en_first_part_info}"
                    )
                elif part_number == parts_count:
                    output_prompt = (
                        f"{openai_en_prompt}\n{part_text}\n"
                        "---\n"
                        f"{en_note}"
                        "---\n"
                        f"{en_last_part_info}"
                        "---\n"
                        f"{en_context_text}"
                    )
                else:
                    output_prompt = (
                        f"{openai_en_prompt}\n{part_text}\n"
                        "---\n"
                        f"{en_note}"
                        "---\n"
                        f"{en_middle_part_info}"
                        "---\n"
                        f"{en_context_text}"
                    )
            else:
                output_prompt = (
                    f"{openai_en_prompt}\n{part_text}\n"
                    "---\n"
                    f"{en_note}"
                )

    if display_language == "ru":
        output_prompt += (
            "---\n"
            "Отвечай на русском языке\n"
            "---\n"
            "Текст пересказа:\n"
        )
    elif display_language == "en":
        output_prompt += (
            "---\n"
            "Answer in English\n"
            "---\n"
            "Summary text:\n"
        )

    return output_prompt


    