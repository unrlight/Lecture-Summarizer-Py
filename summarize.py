import os
from time import sleep
from tiktoken import encoding_for_model
from google.generativeai import configure, GenerativeModel
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import openai

from dotenv import load_dotenv

from utils import split_transcript_into_parts

load_dotenv()

example_file_path = "example.txt"
max_output_tokens = 8192
temperature = 1.5
max_total_tokens_gemini = 14000
max_total_tokens_openai = 16000
gemini_api_key = os.environ.get("gemini_api_keys")
openai_api_key = os.environ.get("open_ai_api_keys")

def summarize_transcript(transcript, language, user_max_attempts):
    configure(api_key=gemini_api_key)

    with open(example_file_path, "r", encoding="utf-8") as file:
        lecture_example = file.read()

    base_prompt_template = """
        Я дам тебе лекцию, распознанную при помощи Whisper.
        Ты обязан сделать подробный пересказ всей лекции.
        Ты обязан сделать максимально подробный пересказ всей лекции. Каждый раздел должен быть глубоко разобран и расширен до максимального уровня детализации, чтобы итоговый пересказ был длинным и полным.
        Вся лекция должна быть в твоём контекстом окне.
        Для пересказа ты определяешь все темы и подтемы и каждую из них очень подробно разбираешь.
        Не должно быть так, чтобы в подтеме было только одно предложение.
        Очень важно, чтобы одна тема подводила к другой. То есть важно, чтобы тема не была простым перечислением терминов, а имела осмысленное подведение к основным данным темы.
        Я предпочитаю более длинные и более подробные ответы.
        Используй больше оформления markdown, используй **утолщения шрифта**, *наклоненный шрифт*, списки и прочие способы оформления, чтобы лучше передать информацию.

        Вот хороший пример пересказанной лекции:
        {lecture_example}
        """
    base_prompt = base_prompt_template.format(lecture_example=lecture_example)
    if language == 'en':
        base_prompt += "Ты должен ответить на русском языке.\n"

    additional_prompt_template = """
        Текст лекции, которую нужно пересказать:
        {part_text}

        Текст пересказа:
        """

    encoding = encoding_for_model("gpt-4")
    tokens_in_base_prompt = len(encoding.encode(base_prompt))
    tokens_in_additional_prompt = len(encoding.encode(additional_prompt_template.format(part_text="")))

    tokens_in_transcript = len(encoding.encode(transcript))
    total_tokens = tokens_in_base_prompt + tokens_in_additional_prompt + tokens_in_transcript

    print(f"Токенов в базовом промпте: {tokens_in_base_prompt}")
    print(f"Токенов в дополнительном промпте: {tokens_in_additional_prompt}")
    print(f"Максимум токенов на часть транскрипта: {max_total_tokens_gemini - tokens_in_base_prompt - tokens_in_additional_prompt}")
    print(f"Всего токенов в транскрипте: {tokens_in_transcript}")
    print(f"Общее количество токенов: {total_tokens}")

    if total_tokens <= max_total_tokens_gemini:
        model_name = "gemini-1.5-pro-002"
        max_attempts = 1
        parts = [transcript]
        print("Используется модель gemini-1.5-pro-002 с 1 попыткой генерации.")
    else:
        model_name = "gemini-1.5-flash"
        max_attempts = user_max_attempts
        max_transcript_tokens_per_part = max_total_tokens_gemini - tokens_in_base_prompt - tokens_in_additional_prompt
        parts = split_transcript_into_parts(transcript, max_transcript_tokens_per_part)
        print(f"Транскрипт разделён на {len(parts)} частей.")
        print(f"Используется модель gemini-1.5-flash с {max_attempts} попытками генерации.")

    all_summaries = []
    request_counter = 0

    for part_number, part in enumerate(parts, start=1):

        part_lines = part.split('\n')
        if part_lines and part_lines[0].startswith('#'):
            print(f"Удаление первой строки части {part_number}, так как она начинается с '#'")
            part = '\n'.join(part_lines[1:])

        prompt = base_prompt + additional_prompt_template.format(part_text=part)
        num_tokens = len(encoding.encode(prompt))
        tokens_in_part_transcript = len(encoding.encode(part))
        print(f"\nЧасть {part_number}:")
        print(f"Токенов в части транскрипта: {tokens_in_part_transcript}")
        print(f"Общее количество токенов для части {part_number}: {num_tokens}")

        max_tokens_in_summary = 0
        best_summary = ""
        for attempt in range(max_attempts):
            request_counter += 1
            if request_counter % 2 == 0:
                sleep(65)

            print(f"Генерация для части {part_number}, попытка {attempt + 1}")
            model = GenerativeModel(model_name=model_name)

            chat = model.start_chat(
                history=[
                    {"role": "user", "parts": "Здравствуй!"},
                    {"role": "model", "parts": "Здравствуй, чем могу помочь?"},
                ],
            )

            response = chat.send_message(
                prompt,
                generation_config={
                    "max_output_tokens": max_output_tokens,
                    "temperature": temperature
                },
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
                }
            ).text.strip()

            tokens_in_response = len(encoding.encode(response))
            print(f"Токенов в ответе для части {part_number}: {tokens_in_response}")
            if tokens_in_response > max_tokens_in_summary:
                max_tokens_in_summary = tokens_in_response
                best_summary = response

        all_summaries.append(f"# Часть {part_number}:\n\n{best_summary}\n\n")

    full_summary = "".join(all_summaries)
    return full_summary


def summarize_with_openai_api(transcript, model_type, language, user_max_attempts):
    openai.api_key = openai_api_key

    with open(example_file_path, "r", encoding="utf-8") as file:
        lecture_example = file.read()

    base_prompt_template = f"""
        Я дам тебе лекцию, распознанную при помощи Whisper.
        Ты обязан сделать подробный пересказ всей лекции.
        Ты обязан сделать максимально подробный пересказ всей лекции. Каждый раздел должен быть глубоко разобран и расширен до максимального уровня детализации, чтобы итоговый пересказ был длинным и полным.
        Вся лекция должна быть в твоём контекстом окне.
        Для пересказа ты определяешь все темы и подтемы и каждую из них очень подробно разбираешь.
        Не должно быть так, чтобы в подтеме было только одно предложение.
        Очень важно, чтобы одна тема подводила к другой. То есть важно, чтобы тема не была простым перечислением терминов, а имела осмысленное подведение к основным данным темы.
        Я предпочитаю более длинные и более подробные ответы.
        Используй больше оформления markdown, используй **утолщения шрифта**, *наклоненный шрифт*, списки и прочие способы оформления, чтобы лучше передать информацию.

        Вот хороший пример пересказанной лекции:
        {lecture_example}
    """
    base_prompt = base_prompt_template

    if language == 'en':
        base_prompt += "Ты должен ответить на русском языке.\n"

    additional_prompt_template = """
        Текст лекции, которую нужно пересказать:
        {part_text}

        Текст пересказа:
    """

    encoding = encoding_for_model(model_type)
    tokens_in_base_prompt = len(encoding.encode(base_prompt))
    tokens_in_additional_prompt = len(encoding.encode(additional_prompt_template.format(part_text="")))
    tokens_in_transcript = len(encoding.encode(transcript))
    total_tokens = tokens_in_base_prompt + tokens_in_additional_prompt + tokens_in_transcript

    print(f"Токенов в базовом промпте: {tokens_in_base_prompt}")
    print(f"Токенов в дополнительном промпте: {tokens_in_additional_prompt}")
    print(f"Максимум токенов на часть транскрипта: {max_total_tokens_openai - tokens_in_base_prompt - tokens_in_additional_prompt}")
    print(f"Всего токенов в транскрипте: {tokens_in_transcript}")
    print(f"Общее количество токенов: {total_tokens}")

    if total_tokens <= max_total_tokens_openai:
        parts = [transcript]
        print("Транскрипт достаточно короткий, не требуется разделение.")
    else:
        max_transcript_tokens_per_part = max_total_tokens_openai - tokens_in_base_prompt - tokens_in_additional_prompt
        parts = split_transcript_into_parts(transcript, max_transcript_tokens_per_part)
        print(f"Транскрипт разделён на {len(parts)} частей.")

    all_summaries = []

    for part_number, part in enumerate(parts, start=1):

        part_lines = part.split('\n')
        if part_lines and part_lines[0].startswith('#'):
            print(f"Удаление первой строки части {part_number}, так как она начинается с '#'")
            part = '\n'.join(part_lines[1:])

        prompt = base_prompt + additional_prompt_template.format(part_text=part)
        num_tokens = len(encoding.encode(prompt))
        tokens_in_part_transcript = len(encoding.encode(part))
        print(f"\nЧасть {part_number}:")
        print(f"Токенов в части транскрипта: {tokens_in_part_transcript}")
        print(f"Общее количество токенов для части {part_number}: {num_tokens}")

        max_tokens_in_summary = 0
        best_summary = ""

        for attempt in range(user_max_attempts):
            print(f"Попытка {attempt + 1} для части {part_number} с моделью OpenAI {model_type}")

            response = openai.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model_type,
                max_tokens=max_output_tokens,
                temperature=temperature / 2,
            )

            generated_text = response.choices[0].message.content.strip()
            tokens_in_response = len(encoding.encode(generated_text))
            print(f"Токенов в ответе для части {part_number}: {tokens_in_response}")

            if tokens_in_response > max_tokens_in_summary:
                max_tokens_in_summary = tokens_in_response
                best_summary = generated_text

        all_summaries.append(f"# Часть {part_number}:\n\n{best_summary}\n\n")

    full_summary = "".join(all_summaries)
    return full_summary



# def summarize_with_ollama_api(prompt): 

