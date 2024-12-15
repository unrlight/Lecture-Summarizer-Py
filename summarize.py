import os
from time import sleep
from tiktoken import encoding_for_model
from google.generativeai import configure, GenerativeModel
import openai
import ollama
from dotenv import load_dotenv
from utils import split_transcript_into_parts, markdown_math_fix, prompt_contructor
from providers import oai_inference
from prompts import *
from translate import *
import time
from huggingface_hub import InferenceClient
from groq import Groq

load_dotenv()

temperature = 1.5

# It's a bit of a mess, but the values are set to best suit the limitations of each platform.

max_total_tokens_gemini = 14000 # for split function only; default is 14000
max_output_tokens_gemini = 8192 # 8192 is max; default is 8192

max_total_tokens_openai = 4096 # for split function only; default is 8192
max_output_tokens_openai = 4096 # 16384 is max; default is 8192

max_total_tokens_ollama = 10000 # for split function only; default is 10000
num_predict_ollama = 10000 # max output tokens; default is 10000
num_ctx_ollama = num_predict_ollama + 10000 # context size (contain max output tokens); default is 10000
model_ollama = "qwen2.5:latest"

# max_total_tokens_hf = 8000 # for split function only; default is 16000
# max_output_tokens_hf = 4000 # default is 8000
# model_hf = "NousResearch/Hermes-3-Llama-3.1-8B"
# timeout_hf = 360 # waiting in line for free hf inference; default is 360

max_total_tokens_hf = 4000 # for split function only; default is 16000
max_output_tokens_hf = 1900 # default is 8000
model_hf = "mistralai/Mixtral-8x7B-Instruct-v0.1"
timeout_hf = 360 # waiting in line for free hf inference; default is 360

max_total_tokens_groq = 3450 # for split function only; default is 10000
max_output_tokens_groq = 1450 # default is 5000
model_groq = "mixtral-8x7b-32768"
temp_groq = 1 # default is 1
top_p_groq = 1 # default is 1

gemini_api_key = os.environ.get("gemini_api_keys")
openai_api_key = os.environ.get("open_ai_api_keys")
hf_api_key = os.environ.get("hf_api_keys")
groq_api_key = os.environ.get("groq_api_keys")

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
        model_name = "gemini-1.5-pro"
        max_attempts = 1
        parts = [transcript]
        print("Используется модель gemini-1.5-pro с 1 попыткой генерации.")
    else:
        model_name = "gemini-1.5-flash"
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

    encoding = encoding_for_model("gpt-4o")

    tokens_in_transcript = len(encoding.encode(input_transcript))

    print(f"Количество токенов в транскрипте: {tokens_in_transcript}")

    if tokens_in_transcript <= max_total_tokens_openai:
        parts = [input_transcript]
        print("Транскрипт достаточно короткий, не требуется разделение.")
    else:
        parts = split_transcript_into_parts(input_transcript, max_total_tokens_openai, model_type)
        print(f"Транскрипт разделён на {len(parts)} частей.")

    all_summaries = []
    parts_count = len(parts)

    for part_number, part in enumerate(parts, start=1):

        prompt = prompt_contructor(language, display_language, part_number, part, model_type, all_summaries, parts_count)
        print(f"Количество токенов в текущем промпте: {len(encoding.encode(prompt))}")

        generated_text = oai_inference(prompt, max_output_tokens_openai, temperature, model_type)

        tokens_in_response = len(encoding.encode(generated_text))
        print(f"Токенов в ответе для части {part_number}: {tokens_in_response}")

        all_summaries.append(f"# Часть {part_number}:\n\n{generated_text}\n\n")

    output_summary = "".join(all_summaries)

    output_summary = markdown_math_fix(output_summary)

    return output_summary

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
            print(f"Попытка {attempt + 1} для части {part_number} с моделью {model_ollama}")
            
            start = time.time()

            response = ollama.chat(
                model=model_ollama,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "num_predict": num_predict_ollama,
                    "num_ctx": num_ctx_ollama,
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
        
        print(f"Ожидание очереди, пользовательский максимум - {timeout_hf} секунд")

        start = time.time()

        response = hf_client.text_generation(
            prompt=prompt,
            max_new_tokens = max_output_tokens_hf,
        )

        end = time.time()
        length = end - start
        print("Ожидание очереди с учетом инференса заняли: ", length, " секунд")

        summary_text = response.strip()
        tokens_in_response = len(encoding.encode(summary_text))
        print(f"Токенов в ответе для части {part_number}: {tokens_in_response}")

        all_summaries.append(f"# Часть {part_number}:\n\n{summary_text}\n\n")

    full_summary = "".join(all_summaries)
    full_summary = markdown_math_fix(full_summary)
    return full_summary

def summarize_with_groq(input_transcript, language, display_language, max_attempts):

    main_transcript = input_transcript

    client = Groq(api_key=groq_api_key)

    if language == 'ru':

        # main_transcript = translate_ollama(main_transcript, "russian", "english")

        base_prompt_template = groq_ru_prompt + """

            {part_text}

            ---

                **Примечание:** Пожалуйста, внимательно следуйте всем приведенным требованиям, чтобы ваш пересказ был максимально информативным и соответствовал заданию.            """

    else:
        base_prompt_template = groq_en_prompt + """

            {part_text}

            ---

                **Note:** Please follow all the given requirements carefully to ensure that your retelling is as informative and relevant to the task as possible.
            """
    if display_language=="ru":
        base_prompt_template = base_prompt_template + "\nОтвечай на русском языке.\nОтвечай в 3 раза подробнее и больше"
    else:
        base_prompt_template = base_prompt_template + "\nAnswer in English.\nAnswer in 3 times more detail and more"

    encoding = encoding_for_model("gpt-3.5")
    prompt_tokens = len(encoding.encode(base_prompt_template.format(part_text="")))
    tokens_in_transcript = len(encoding.encode(main_transcript))
    total_tokens = tokens_in_transcript + prompt_tokens
    print(f"Общее количество токенов: {total_tokens}")


    if total_tokens <= max_total_tokens_groq:
        parts = [main_transcript]
    else:
        max_transcript_tokens_per_part = max_total_tokens_groq - prompt_tokens
        parts = split_transcript_into_parts(main_transcript, max_transcript_tokens_per_part)

    all_summaries = []
    for part_number, part in enumerate(parts, start=1):
        prompt = base_prompt_template.format(part_text=part)
        num_tokens = len(encoding.encode(prompt))
        print(f"Общее количество токенов для части {part_number}: {num_tokens}")

        max_tokens_in_summary = 0
        best_summary = ""

        for attempt in range(max_attempts):
            print(f"Попытка {attempt + 1} для части {part_number} с моделью {model_groq} (GROQ)")

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model_groq,
                max_tokens=max_output_tokens_groq,
                temperature=temp_groq,
                top_p=top_p_groq
            )

            summary_text = chat_completion.choices[0].message.content.strip()
            tokens_in_response = len(encoding.encode(summary_text))
            print(f"Токенов в ответе для части {part_number}, попытка {attempt + 1}: {tokens_in_response}")

            if (len(parts) > 1) or (max_attempts > 1):
                print("Засыпаем на 65 секунд, из-за ограничений API")
                sleep(65)

            if tokens_in_response > max_tokens_in_summary:
                max_tokens_in_summary = tokens_in_response
                best_summary = summary_text

        all_summaries.append(f"# Часть {part_number}:\n\n{best_summary}\n\n")

    full_summary = "".join(all_summaries)

    # if(display_language=="ru"):
    #     full_summary = translate_ollama(full_summary,"english","russian")

    full_summary = markdown_math_fix(full_summary)

    return full_summary