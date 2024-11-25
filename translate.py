from utils import split_transcript_into_parts
from tiktoken import encoding_for_model
import ollama
import openai

def translate_ollama(text, input_language, output_language):
    
    if(input_language == "russian" and output_language == "english"):

        prompt = """Translate this text from {input_language_prompt} to {output_language_prompt}
        completely, from beginning to end, without skipping a word. You are required to preserve the full formatting of the text.
        
        Here is the full text:
        {part_text} 
        """
        
        parts = split_transcript_into_parts(text, 10000)

        max_attempts = 1
        translated_text = []
        encoding = encoding_for_model("gpt-3.5")
        for part_number, part in enumerate(parts, start=1):
            prompt = prompt.format(input_language_prompt=input_language, output_language_prompt=output_language, part_text=part)
            num_tokens = len(encoding.encode(prompt))
            print(f"Общее количество токенов для части {part_number}: {num_tokens}")

            max_tokens_in_summary = 0
            best_summary = ""

            for attempt in range(max_attempts):
                print(f"Попытка перевода {attempt + 1} (с {input_language} на {output_language}) для части {part_number} с моделью Qwen2.5")
                
                response = ollama.chat(
                    model="qwen2.5:3b",
                    messages=[{"role": "user", "content": prompt}],
                    options={
                        "num_predict": 10000,
                        "num_ctx": 20000,
                        "keep_alive": 0
                    }
                )
                
                summary_text = response['message']['content'].strip()
                tokens_in_response = len(encoding.encode(summary_text))
                print(f"Токенов в ответе для части {part_number}, попытка {attempt + 1}: {tokens_in_response}")

                if tokens_in_response > max_tokens_in_summary:
                    max_tokens_in_summary = tokens_in_response
                    best_summary = summary_text

            translated_text.append(f"{best_summary}\n\n")
            output_text = " ".join(translated_text)


    if(input_language == "english" and output_language == "russian"):

        prompt = """Translate this text from {input_language_prompt} to {output_language_prompt}
        completely, from beginning to end, without skipping a word. You are required to preserve the full formatting of the text.
        
        Here is the full text:
        {part_text} 
        """
        
        parts = split_transcript_into_parts(text, 4000)

        max_attempts = 1
        translated_text = []
        encoding = encoding_for_model("gpt-3.5")
        for part_number, part in enumerate(parts, start=1):
            prompt = prompt.format(input_language_prompt=input_language, output_language_prompt=output_language, part_text=part)
            num_tokens = len(encoding.encode(prompt))
            print(f"Общее количество токенов для части {part_number}: {num_tokens}")

            max_tokens_in_summary = 0
            best_summary = ""

            for attempt in range(max_attempts):
                print(f"Попытка перевода {attempt + 1} (с {input_language} на {output_language}) для части {part_number} с моделью Qwen2.5")
                
                response = ollama.chat(
                    #model="qwen2.5:latest",
                    model="qwen2.5:3b",
                    messages=[{"role": "user", "content": prompt}],
                    options={
                        "num_predict": 16000,
                        "num_ctx": 20000,
                        "keep_alive": 0
                    }
                )
                
                summary_text = response['message']['content'].strip()
                tokens_in_response = len(encoding.encode(summary_text))
                print(f"Токенов в ответе для части {part_number}, попытка {attempt + 1}: {tokens_in_response}")

                if tokens_in_response > max_tokens_in_summary:
                    max_tokens_in_summary = tokens_in_response
                    best_summary = summary_text

            translated_text.append(f"{best_summary}\n\n")
            output_text = " ".join(translated_text)

    return output_text

def translate_openai(text, input_language, output_language):
    
    if(input_language == "russian" and output_language == "english"):

        prompt = """Translate this text from {input_language_prompt} to {output_language_prompt}
        completely, from beginning to end, without skipping a word. You are required to preserve the full formatting of the text.
        
        Here is the full text:
        {part_text} 
        """
        
        parts = split_transcript_into_parts(text, 10000)

        max_attempts = 1
        translated_text = []
        encoding = encoding_for_model("gpt-4")
        for part_number, part in enumerate(parts, start=1):
            prompt = prompt.format(input_language_prompt=input_language, output_language_prompt=output_language, part_text=part)
            num_tokens = len(encoding.encode(prompt))
            print(f"Общее количество токенов для части {part_number}: {num_tokens}")

            max_tokens_in_summary = 0
            best_summary = ""

            for attempt in range(max_attempts):
                print(f"Попытка перевода {attempt + 1} (с {input_language} на {output_language}) для части {part_number} с моделью 4o-mini")
                
                response = openai.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="gpt-4o-mini",
                    max_tokens=16384,
                )
                
                summary_text = response.choices[0].message.content.strip()
                tokens_in_response = len(encoding.encode(summary_text))
                print(f"Токенов в ответе для части {part_number}, попытка {attempt + 1}: {tokens_in_response}")

                if tokens_in_response > max_tokens_in_summary:
                    max_tokens_in_summary = tokens_in_response
                    best_summary = summary_text

            translated_text.append(f"{best_summary}\n\n")
            output_text = " ".join(translated_text)


    if(input_language == "english" and output_language == "russian"):

        prompt = """Translate this text from {input_language_prompt} to {output_language_prompt}
        completely, from beginning to end, without skipping a word. You are required to preserve the full formatting of the text.
        
        Here is the full text:
        {part_text} 
        """
        
        parts = split_transcript_into_parts(text, 4000)

        max_attempts = 1
        translated_text = []
        encoding = encoding_for_model("gpt-4")
        for part_number, part in enumerate(parts, start=1):
            prompt = prompt.format(input_language_prompt=input_language, output_language_prompt=output_language, part_text=part)
            num_tokens = len(encoding.encode(prompt))
            print(f"Общее количество токенов для части {part_number}: {num_tokens}")

            max_tokens_in_summary = 0
            best_summary = ""

            for attempt in range(max_attempts):
                print(f"Попытка перевода {attempt + 1} (с {input_language} на {output_language}) для части {part_number} с моделью 4o-mini")
                
                response = openai.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="gpt-4o-mini",
                    max_tokens=16384,
                )
                
                summary_text = response.choices[0].message.content.strip()
                tokens_in_response = len(encoding.encode(summary_text))
                print(f"Токенов в ответе для части {part_number}, попытка {attempt + 1}: {tokens_in_response}")

                if tokens_in_response > max_tokens_in_summary:
                    max_tokens_in_summary = tokens_in_response
                    best_summary = summary_text

            translated_text.append(f"{best_summary}\n\n")
            output_text = " ".join(translated_text)

    return output_text