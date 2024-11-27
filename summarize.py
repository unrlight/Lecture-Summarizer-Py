import os
from time import sleep
from tiktoken import encoding_for_model
from google.generativeai import configure, GenerativeModel
import openai
import ollama
from dotenv import load_dotenv
from utils import split_transcript_into_parts, markdown_math_fix
from prompts import *
from translate import *
import time
from huggingface_hub import InferenceClient

load_dotenv()

temperature = 1.5

max_total_tokens_gemini = 14000
max_output_tokens_gemini = 8192

max_total_tokens_openai = 16000
max_output_tokens_openai = 8192

max_total_tokens_ollama = 10000
model_ollama = "qwen2.5:latest"

max_total_tokens_hf = 16000
max_output_tokens_hf = 8000
model_hf = "mistralai/Mixtral-8x7B-Instruct-v0.1"
timeout_hf = 360

gemini_api_key = os.environ.get("gemini_api_keys")
openai_api_key = os.environ.get("open_ai_api_keys")
hf_api_key = os.environ.get("hf_api_keys")

def summarize_transcript(transcript, language, display_language, user_max_attempts):
    configure(api_key=gemini_api_key)

    if language == 'ru':
            base_prompt_template = gemini_ru_prompt + """

                {part_text}

                ---

                **Примечание:** Пожалуйста, внимательно следуй всем указанным требованиям, чтобы пересказ получился максимально информативным и соответствующим заданию.
                
                """
    else:
        base_prompt_template = gemini_en_prompt + """

            {part_text}

            ---

                **Note:** Please follow all the given requirements carefully to ensure that your retelling is as informative and relevant to the task as possible.
            """
        
    if display_language == 'ru':
        base_prompt_template += "\nОтвечай на русском языке"
    else:
        base_prompt_template += "\nAnswer in English"

    encoding = encoding_for_model("gpt-3.5")
    tokens_in_transcript = len(encoding.encode(transcript))

    prompt_tokens = len(encoding.encode(base_prompt_template.format(part_text="")))
    total_tokens = tokens_in_transcript + prompt_tokens
    print(f"Общее количество токенов: {total_tokens}")

    if total_tokens <= max_total_tokens_gemini:
        model_name = "gemini-1.5-pro-002"
        max_attempts = 1
        parts = [transcript]
        print("Используется модель gemini-1.5-pro-002 с 1 попыткой генерации.")
    else:
        model_name = "gemini-1.5-flash-002"
        max_attempts = user_max_attempts
        max_transcript_tokens_per_part = max_total_tokens_gemini - prompt_tokens
        parts = split_transcript_into_parts(transcript, max_transcript_tokens_per_part)
        print(f"Транскрипт разделён на {len(parts)} частей.")
        print(f"Используется модель gemini-1.5-flash с {max_attempts} попытками генерации.")

    all_summaries = []
    request_counter = 0

    for part_number, part in enumerate(parts, start=1):
        prompt = base_prompt_template.format(part_text=part)
        num_tokens = len(encoding.encode(prompt))
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
                    "max_output_tokens": max_output_tokens_gemini,
                    "temperature": temperature
                },
                safety_settings={}
            ).text.strip()

            tokens_in_response = len(encoding.encode(response))
            print(f"Токенов в ответе для части {part_number}: {tokens_in_response}")
            if tokens_in_response > max_tokens_in_summary:
                max_tokens_in_summary = tokens_in_response
                best_summary = response

        all_summaries.append(f"# Часть {part_number}:\n\n{best_summary}\n\n")

    full_summary = "".join(all_summaries)
    return full_summary

def summarize_with_openai_api(input_transcript, model_type, language, display_language, user_max_attempts):
    
    openai.api_key = openai_api_key

    main_transcript = input_transcript

    if language == 'ru':

        # main_transcript = translate_openai(main_transcript, "russian", "english")

        base_prompt_template = ollama_en_prompt + """

            {part_text}

            ---

                **Note:** Please follow all the given requirements carefully to ensure that your retelling is as informative and relevant to the task as possible.
            """

    else:
        base_prompt_template = ollama_en_prompt + """

            {part_text}

            ---

                **Note:** Please follow all the given requirements carefully to ensure that your retelling is as informative and relevant to the task as possible.
            """

    if display_language=="ru":
        base_prompt_template = base_prompt_template + "\nОтвечай на русском языке."
    else:
        base_prompt_template = base_prompt_template + "\nAnswer in English."

    encoding = encoding_for_model("gpt-4")
    tokens_in_transcript = len(encoding.encode(main_transcript))
    prompt_tokens = len(encoding.encode(base_prompt_template.format(part_text="")))
    total_tokens = tokens_in_transcript + prompt_tokens
    print(f"Общее количество токенов: {total_tokens}")

    if total_tokens <= max_total_tokens_openai:
        parts = [main_transcript]
        print("Транскрипт достаточно короткий, не требуется разделение.")
    else:
        max_transcript_tokens_per_part = max_total_tokens_openai - prompt_tokens
        parts = split_transcript_into_parts(main_transcript, max_transcript_tokens_per_part)
        print(f"Транскрипт разделён на {len(parts)} частей.")

    all_summaries = []

    for part_number, part in enumerate(parts, start=1):
        prompt = base_prompt_template.format(part_text=part)
        num_tokens = len(encoding.encode(prompt))
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
                max_tokens=max_output_tokens_openai,
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

    # if(display_language=="ru"):
    #    full_summary = translate_openai(full_summary,"english","russian")

    full_summary = markdown_math_fix(full_summary)

    return full_summary

def summarize_with_ollama_api(input_transcript, language, display_language, max_attempts):

    main_transcript = input_transcript

    if language == 'ru':

        # main_transcript = translate_ollama(main_transcript, "russian", "english")

        base_prompt_template = ollama_ru_prompt + """

            {part_text}

            ---

                **Примечание:** Пожалуйста, внимательно следуйте всем приведенным требованиям, чтобы ваш пересказ был максимально информативным и соответствовал заданию.            """

    else:
        base_prompt_template = ollama_en_prompt + """

            {part_text}

            ---

                **Note:** Please follow all the given requirements carefully to ensure that your retelling is as informative and relevant to the task as possible.
            """
    if display_language=="ru":
        base_prompt_template = base_prompt_template + "\nОтвечай на русском языке."
    else:
        base_prompt_template = base_prompt_template + "\nAnswer in English."

    encoding = encoding_for_model("gpt-3.5")
    prompt_tokens = len(encoding.encode(base_prompt_template.format(part_text="")))
    tokens_in_transcript = len(encoding.encode(main_transcript))
    total_tokens = tokens_in_transcript + prompt_tokens
    print(f"Общее количество токенов: {total_tokens}")


    if total_tokens <= max_total_tokens_ollama:
        parts = [main_transcript]
    else:
        max_transcript_tokens_per_part = max_total_tokens_ollama - prompt_tokens
        parts = split_transcript_into_parts(main_transcript, max_transcript_tokens_per_part)

    all_summaries = []
    for part_number, part in enumerate(parts, start=1):
        prompt = base_prompt_template.format(part_text=part)
        num_tokens = len(encoding.encode(prompt))
        print(f"Общее количество токенов для части {part_number}: {num_tokens}")

        max_tokens_in_summary = 0
        best_summary = ""

        for attempt in range(max_attempts):
            print(f"Попытка {attempt + 1} для части {part_number} с моделью Qwen2.5")
            
            start = time.time()

            response = ollama.chat(
                model=model_ollama,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "num_predict": 10000,
                    "num_ctx": 20000,
                    "keep_alive": 0
                }
            )

            end = time.time()
            length = end - start
            print("Вычисления заняли: ", length, " секунд")
            
            summary_text = response['message']['content'].strip()
            tokens_in_response = len(encoding.encode(summary_text))
            print(f"Токенов в ответе для части {part_number}, попытка {attempt + 1}: {tokens_in_response}")

            if tokens_in_response > max_tokens_in_summary:
                max_tokens_in_summary = tokens_in_response
                best_summary = summary_text

        all_summaries.append(f"# Часть {part_number}:\n\n{best_summary}\n\n")

    full_summary = "".join(all_summaries)

    # if(display_language=="ru"):
    #     full_summary = translate_ollama(full_summary,"english","russian")

    full_summary = markdown_math_fix(full_summary)

    return full_summary

def summarize_with_hf_inference_client(input_transcript, language, display_language):
    
    main_transcript = input_transcript

    hf_client = InferenceClient(model=model_hf, token=hf_api_key, headers={"x-wait-for-model": "true"}, timeout=timeout_hf)

    if language == 'ru':
        base_prompt_template = hf_ru_prompt + """
            Вот текст, который нужно пересказать:

            {part_text}

            ---

            **Примечание:** Пожалуйста, внимательно следуйте всем приведенным требованиям, чтобы ваш пересказ был максимально информативным и соответствовал заданию.
        """
    else:
        base_prompt_template = hf_en_prompt + """
            Here is the text that needs to be summarized:

            {part_text}

            ---

            **Note:** Please follow all the given requirements carefully to ensure that your retelling is as informative and relevant to the task as possible.
        """

    if display_language == 'ru':
        base_prompt_template += "\nОтвечай на русском языке."
    else:
        base_prompt_template += "\nAnswer in English."

    encoding = encoding_for_model("gpt-3.5")
    prompt_tokens = len(encoding.encode(base_prompt_template.format(part_text="")))
    tokens_in_transcript = len(encoding.encode(main_transcript))
    total_tokens = tokens_in_transcript + prompt_tokens
    print(f"Общее количество токенов: {total_tokens}")

    if total_tokens <= max_total_tokens_hf:
        parts = [main_transcript]
    else:
        max_transcript_tokens_per_part = max_total_tokens_hf - prompt_tokens
        parts = split_transcript_into_parts(main_transcript, max_transcript_tokens_per_part)

    all_summaries = []
    for part_number, part in enumerate(parts, start=1):
        prompt = base_prompt_template.format(part_text=part)
        num_tokens = len(encoding.encode(prompt))
        print(f"Общее количество токенов для части {part_number}: {num_tokens}")

        print(f"Генерация для части {part_number} с использованием модели {model_hf} (Hugging Face)")
        
        print(f"Ожидание очереди, максимум - {timeout_hf} секунд")
        response = hf_client.text_generation(
            prompt=prompt,
            max_new_tokens = max_output_tokens_hf
        )

        summary_text = response.strip()
        tokens_in_response = len(encoding.encode(summary_text))
        print(f"Токенов в ответе для части {part_number}: {tokens_in_response}")

        all_summaries.append(f"# Часть {part_number}:\n\n{summary_text}\n\n")

    full_summary = "".join(all_summaries)
    full_summary = markdown_math_fix(full_summary)
    return full_summary