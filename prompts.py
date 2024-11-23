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

openai_en_prompt = """
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