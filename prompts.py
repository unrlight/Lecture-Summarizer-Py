gemini_ru_prompt = """
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
"""

gemini_en_prompt = """
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
"""

openai_ru_prompt = """
            Я дам тебе лекцию, распознанную при помощи Whisper.
            Ты обязан сделать подробный пересказ всей лекции.
            Ты обязан сделать максимально подробный пересказ всей лекции. Каждый раздел должен быть глубоко разобран и расширен до максимального уровня детализации, чтобы итоговый пересказ был длинным и полным.
            Вся лекция должна быть в твоём контекстом окне.
            Для пересказа ты определяешь все темы и подтемы и каждую из них очень подробно разбираешь.
            Не должно быть так, чтобы в подтеме было только одно предложение.
            Очень важно, чтобы одна тема подводила к другой. То есть важно, чтобы тема не была простым перечислением терминов, а имела осмысленное подведение к основным данным темы.
            Я предпочитаю более длинные и более подробные ответы.
            Используй больше оформления markdown, используй **утолщения шрифта**, *наклоненный шрифт*, списки и прочие способы оформления, чтобы лучше передать информацию.
"""

openai_en_prompt = """
               I will give you a lecture recognized by Whisper.
                You must provide a detailed summary of the entire lecture.
                You must provide a detailed summary of the entire lecture. Each section must be deeply analyzed and expanded to the maximum level of detail so that the final summary is long and complete.
                The entire lecture must be in your context window.
                For the summary, you identify all the topics and subtopics and analyze each of them in great detail.
                There should not be a situation where there is only one sentence in a subtopic.
                It is very important that one topic leads to another. That is, it is important that the topic is not a simple list of terms, but has a meaningful lead-in to the main data of the topic.
                I prefer longer and more detailed answers.
                Use more markdown, use **bold font**, *italic font*, lists and other formatting methods to better convey the information.
"""

ollama_ru_prompt = """
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
"""

ollama_en_prompt = """
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
"""

hf_ru_prompt = """
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
"""

hf_en_prompt = """
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
"""

groq_ru_prompt = """
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
"""

groq_en_prompt = """
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
"""