import os
from time import sleep
from tiktoken import encoding_for_model
from google.generativeai import configure, GenerativeModel
import openai
import ollama
from dotenv import load_dotenv
from utils import split_transcript_into_parts


load_dotenv()

max_output_tokens = 8192
temperature = 1.5
max_total_tokens_gemini = 14000
max_total_tokens_openai = 16000
max_total_tokens_ollama = 16000
gemini_api_key = os.environ.get("gemini_api_keys")
openai_api_key = os.environ.get("open_ai_api_keys")

def summarize_transcript(transcript, language, display_language, user_max_attempts):
    configure(api_key=gemini_api_key)

    if language == 'ru':
            base_prompt_template = """

                Я предоставлю тебе текст лекции, распознанный при помощи Whisper.

                Твоя задача — сделать максимально подробный пересказ всей лекции, используя красивое и обильное форматирование.

                ### ⚠️ ВАЖНЫЕ ТРЕБОВАНИЯ К ПЕРЕСКАЗУ:

                1. **Подробность:**

                - Каждый раздел должен быть **глубоко разобран** и **расширен** до максимального уровня детализации.
                - Итоговый пересказ должен быть **длинным** и **полным**.
                - **Подробно объясняй каждую идею**, приводя примеры и разъяснения.

                2. **Структура:**

                - Определи все **темы** и **подтемы**.
                - Используй уровни заголовков: `# Заголовок 1`, `## Заголовок 2`, `### Заголовок 3` и т.д.
                - **Каждую подтему очень подробно разбери.** Не должно быть подтем с одним предложением.

                3. **Связность:**

                - **Обеспечь плавные переходы** между темами.
                - Одна тема должна **подводить** к следующей.
                - **Не просто перечисляй термины**, а создавай **осмысленные связи** между идеями.

                4. **Форматирование:**

                - Используй разнообразное форматирование для лучшего восприятия информации:
                    - **Жирный шрифт** для важных терминов и понятий.
                    - *Курсив* для выделения ключевых мыслей.
                    - Списки (маркированные и нумерованные) для перечисления.
                    - **Цитаты**, **таблицы**, **выделения цветом** при необходимости.
                - **Пример использования форматирования:**
                    - **Определение:** *Шифрование* — это процесс...

                5. **Предпочтения:**

                - Я предпочитаю **более длинные** и **более подробные** ответы.
                - **Не ограничивайся краткими описаниями**; развивай каждую мысль максимально полно.

                ---

                **Текст лекции, которую нужно пересказать:**

                {part_text}

                ---

                **Примечание:** Пожалуйста, внимательно следуй всем указанным требованиям, чтобы пересказ получился максимально информативным и соответствующим заданию.
                
                """
    else:
        base_prompt_template = """

                I will provide you with the lecture text, recognized by Whisper.

                Your task is to make the most detailed summary of the entire lecture, using beautiful and rich formatting.

                ### ⚠️ IMPORTANT REQUIREMENTS FOR SUMMARY:

                1. **Detail:**

                - Each section should be **deeply analyzed** and **expanded** to the maximum level of detail.
                - The final summary should be **long** and **complete**.
                - **Explain each idea in detail**, giving examples and explanations.

                2. **Structure:**

                - Identify all **topics** and **subtopics**.
                - Use heading levels: `# Heading 1`, `## Heading 2`, `### Heading 3`, etc.
                - **Explain each subtopic in great detail.** No one-sentence subtopics.

                3. **Coherence:**

                - **Make sure there are smooth transitions** between topics.
                - One topic should **lead** to the next.
                - **Don't just list terms**, make **meaningful connections** between ideas.

                4. **Formatting:**

                - Use a variety of formatting to make information more digestible:
                - **Bold** for important terms and concepts.
                - *Italics* to highlight key ideas.
                - Lists (bulleted and numbered) for listing.
                - **Quotes**, **tables**, **highlighting** when needed.
                - **Example of formatting:**
                - **Definition:** *Encryption* is the process of...

                5. **Preferences:**

                - I prefer **longer** and **more detailed** answers.
                - **Don't limit yourself to short descriptions**; develop each idea as fully as possible.

                ---

                **Text of the lecture to be summarized:**

            {part_text}

            ---

                **Note:** Please follow all the given requirements carefully to ensure that your retelling is as informative and relevant to the task as possible.
            """
        
    if display_language == 'ru':
        base_prompt_template += "\nОтвечай на русском языке"
    else:
        base_prompt_template += "\nAnswer in English"

    encoding = encoding_for_model("gpt-4")
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
                    "max_output_tokens": max_output_tokens,
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

def summarize_with_openai_api(transcript, model_type, language, display_language, user_max_attempts):
    openai.api_key = openai_api_key
    if language == 'ru':
        base_prompt_template = """

            Я предоставлю тебе текст лекции, распознанный при помощи Whisper.

            Твоя задача — сделать максимально подробный пересказ всей лекции, используя красивое и обильное форматирование.

            ### ⚠️ ВАЖНЫЕ ТРЕБОВАНИЯ К ПЕРЕСКАЗУ:

            1. **Подробность:**

            - Каждый раздел должен быть **глубоко разобран** и **расширен** до максимального уровня детализации.
            - Итоговый пересказ должен быть **длинным** и **полным**.
            - **Подробно объясняй каждую идею**, приводя примеры и разъяснения.

            2. **Структура:**

            - Определи все **темы** и **подтемы**.
            - Используй уровни заголовков: `# Заголовок 1`, `## Заголовок 2`, `### Заголовок 3` и т.д.
            - **Каждую подтему очень подробно разбери.** Не должно быть подтем с одним предложением.

            3. **Связность:**

            - **Обеспечь плавные переходы** между темами.
            - Одна тема должна **подводить** к следующей.
            - **Не просто перечисляй термины**, а создавай **осмысленные связи** между идеями.

            4. **Форматирование:**

            - Используй разнообразное форматирование для лучшего восприятия информации:
                - **Жирный шрифт** для важных терминов и понятий.
                - *Курсив* для выделения ключевых мыслей.
                - Списки (маркированные и нумерованные) для перечисления.
                - **Цитаты**, **таблицы**, **выделения цветом** при необходимости.
            - **Пример использования форматирования:**
                - **Определение:** *Шифрование* — это процесс...

            5. **Предпочтения:**

            - Я предпочитаю **более длинные** и **более подробные** ответы.
            - **Не ограничивайся краткими описаниями**; развивай каждую мысль максимально полно.

            ---

            **Текст лекции, которую нужно пересказать:**

            {part_text}

            ---

            **Примечание:** Пожалуйста, внимательно следуй всем указанным требованиям, чтобы пересказ получился максимально информативным и соответствующим заданию.
            
            """
    else:
        base_prompt_template = """

                I will provide you with the lecture text, recognized by Whisper.

                Your task is to make the most detailed summary of the entire lecture, using beautiful and rich formatting.

                ### ⚠️ IMPORTANT REQUIREMENTS FOR SUMMARY:

                1. **Detail:**

                - Each section should be **deeply analyzed** and **expanded** to the maximum level of detail.
                - The final summary should be **long** and **complete**.
                - **Explain each idea in detail**, giving examples and explanations.

                2. **Structure:**

                - Identify all **topics** and **subtopics**.
                - Use heading levels: `# Heading 1`, `## Heading 2`, `### Heading 3`, etc.
                - **Explain each subtopic in great detail.** No one-sentence subtopics.

                3. **Coherence:**

                - **Make sure there are smooth transitions** between topics.
                - One topic should **lead** to the next.
                - **Don't just list terms**, make **meaningful connections** between ideas.

                4. **Formatting:**

                - Use a variety of formatting to make information more digestible:
                - **Bold** for important terms and concepts.
                - *Italics* to highlight key ideas.
                - Lists (bulleted and numbered) for listing.
                - **Quotes**, **tables**, **highlighting** when needed.
                - **Example of formatting:**
                - **Definition:** *Encryption* is the process of...

                5. **Preferences:**

                - I prefer **longer** and **more detailed** answers.
                - **Don't limit yourself to short descriptions**; develop each idea as fully as possible.

                ---

                **Text of the lecture to be summarized:**

            {part_text}

            ---

                **Note:** Please follow all the given requirements carefully to ensure that your retelling is as informative and relevant to the task as possible.
            """
        
    if display_language == 'ru':
        base_prompt_template += "\nОтвечай на русском языке"
    else:
        base_prompt_template += "\nAnswer in English"


    encoding = encoding_for_model("gpt-4")
    tokens_in_transcript = len(encoding.encode(transcript))
    prompt_tokens = len(encoding.encode(base_prompt_template.format(part_text="")))
    total_tokens = tokens_in_transcript + prompt_tokens
    print(f"Общее количество токенов: {total_tokens}")

    if total_tokens <= max_total_tokens_openai:
        parts = [transcript]
        print("Транскрипт достаточно короткий, не требуется разделение.")
    else:
        max_transcript_tokens_per_part = max_total_tokens_openai - prompt_tokens
        parts = split_transcript_into_parts(transcript, max_transcript_tokens_per_part)
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

def summarize_with_ollama_api(transcript, language, display_language, max_attempts):


    if language == 'ru':
        base_prompt_template = """

            Я предоставлю тебе текст лекции, распознанный при помощи Whisper.

            Твоя задача — сделать максимально подробный пересказ всей лекции, используя красивое и обильное форматирование.

            ### ⚠️ ВАЖНЫЕ ТРЕБОВАНИЯ К ПЕРЕСКАЗУ:

            1. **Подробность:**

            - Каждый раздел должен быть **глубоко разобран** и **расширен** до максимального уровня детализации.
            - Итоговый пересказ должен быть **длинным** и **полным**.
            - **Подробно объясняй каждую идею**, приводя примеры и разъяснения.

            2. **Структура:**

            - Определи все **темы** и **подтемы**.
            - Используй уровни заголовков: `# Заголовок 1`, `## Заголовок 2`, `### Заголовок 3` и т.д.
            - **Каждую подтему очень подробно разбери.** Не должно быть подтем с одним предложением.

            3. **Связность:**

            - **Обеспечь плавные переходы** между темами.
            - Одна тема должна **подводить** к следующей.
            - **Не просто перечисляй термины**, а создавай **осмысленные связи** между идеями.

            4. **Форматирование:**

            - Используй разнообразное форматирование для лучшего восприятия информации:
                - **Жирный шрифт** для важных терминов и понятий.
                - *Курсив* для выделения ключевых мыслей.
                - Списки (маркированные и нумерованные) для перечисления.
                - **Цитаты**, **таблицы**, **выделения цветом** при необходимости.
            - **Пример использования форматирования:**
                - **Определение:** *Шифрование* — это процесс...

            5. **Предпочтения:**

            - Я предпочитаю **более длинные** и **более подробные** ответы.
            - **Не ограничивайся краткими описаниями**; развивай каждую мысль максимально полно.

            ---

            **Текст лекции, которую нужно пересказать:**

            {part_text}

            ---

            **Примечание:** Пожалуйста, внимательно следуй всем указанным требованиям, чтобы пересказ получился максимально информативным и соответствующим заданию.
            
            """
    else:
        base_prompt_template = """

                I will provide you with the lecture text, recognized by Whisper.

                Your task is to make the most detailed summary of the entire lecture, using beautiful and rich formatting.

                ### ⚠️ IMPORTANT REQUIREMENTS FOR SUMMARY:

                1. **Detail:**

                - Each section should be **deeply analyzed** and **expanded** to the maximum level of detail.
                - The final summary should be **long** and **complete**.
                - **Explain each idea in detail**, giving examples and explanations.

                2. **Structure:**

                - Identify all **topics** and **subtopics**.
                - Use heading levels: `# Heading 1`, `## Heading 2`, `### Heading 3`, etc.
                - **Explain each subtopic in great detail.** No one-sentence subtopics.

                3. **Coherence:**

                - **Make sure there are smooth transitions** between topics.
                - One topic should **lead** to the next.
                - **Don't just list terms**, make **meaningful connections** between ideas.

                4. **Formatting:**

                - Use a variety of formatting to make information more digestible:
                - **Bold** for important terms and concepts.
                - *Italics* to highlight key ideas.
                - Lists (bulleted and numbered) for listing.
                - **Quotes**, **tables**, **highlighting** when needed.
                - **Example of formatting:**
                - **Definition:** *Encryption* is the process of...

                5. **Preferences:**

                - I prefer **longer** and **more detailed** answers.
                - **Don't limit yourself to short descriptions**; develop each idea as fully as possible.

                ---

                **Text of the lecture to be summarized:**

            {part_text}

            ---

                **Note:** Please follow all the given requirements carefully to ensure that your retelling is as informative and relevant to the task as possible.
            """
        
    if display_language == 'ru':
        base_prompt_template += "\nОтвечай на русском языке"
    else:
        base_prompt_template += "\nAnswer in English"

    encoding = encoding_for_model("gpt-4")
    prompt_tokens = len(encoding.encode(base_prompt_template.format(part_text="")))
    tokens_in_transcript = len(encoding.encode(transcript))
    total_tokens = tokens_in_transcript + prompt_tokens
    print(f"Общее количество токенов: {total_tokens}")


    if total_tokens <= max_total_tokens_ollama:
        parts = [transcript]
    else:
        max_transcript_tokens_per_part = max_total_tokens_ollama - prompt_tokens
        parts = split_transcript_into_parts(transcript, max_transcript_tokens_per_part)

    all_summaries = []
    for part_number, part in enumerate(parts, start=1):
        prompt = base_prompt_template.format(part_text=part)
        num_tokens = len(encoding.encode(prompt))
        print(f"Общее количество токенов для части {part_number}: {num_tokens}")

        max_tokens_in_summary = 0
        best_summary = ""

        for attempt in range(max_attempts):
            print(f"Попытка {attempt + 1} для части {part_number} с моделью Qwen2.5")
            
            response = ollama.chat(
                model="qwen2.5:latest",
                messages=[{"role": "user", "content": prompt}],
                options={
                    "num_predict": 4000,
                    "num_ctx": 24000,
                    "keep_alive": 0
                }
            )
            
            summary_text = response['message']['content'].strip()
            tokens_in_response = len(encoding.encode(summary_text))
            print(f"Токенов в ответе для части {part_number}, попытка {attempt + 1}: {tokens_in_response}")

            if tokens_in_response > max_tokens_in_summary:
                max_tokens_in_summary = tokens_in_response
                best_summary = summary_text

        all_summaries.append(f"# Часть {part_number}:\n\n{best_summary}\n\n")

    full_summary = "".join(all_summaries)

    return full_summary

