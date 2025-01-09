gemini_ru_prompt = """
Я предоставлю тебе текст лекции, распознанный при помощи Whisper.

Твоя задача — сделать аналитический пересказ всей лекции, демонстрируя глубокое понимание материала.

### ⚠️ КЛЮЧЕВЫЕ ТРЕБОВАНИЯ К ПЕРЕСКАЗУ:

1. **Анализ и Понимание:**

   - Выяви основные темы и подтемы лекции.
   - Проанализируй ключевые моменты и аргументы лектора.
   - Разбери каждую идею своими словами, избегая копирования текста из лекции.
   - Продемонстрируй понимание материала, связывая идеи друг с другом.
   - Не просто перечисляй термины, а создавай осмысленные связи между ними.
   - Попробуй сделать выводы на основе полученной информации.

2. **Структура:**

   -  Используй уровни заголовков: `# Заголовок 1`, `## Заголовок 2`, `### Заголовок 3` и т.д. для структурирования пересказа.
   -  Каждую подтему подробно разбери, не оставляй подтемы с одним предложением.

3. **Форматирование:**
    -  Выдели жирным шрифтом важные термины.
    -  Используй *курсив* для выделения ключевых мыслей.
    -  Используй списки для перечисления, если это уместно.
    -  При необходимости используй цитаты, таблицы, выделения цветом.

4.  **Формулы, код, схемы, таблицы:**
    -  Если в лекции упоминается или диктуется программный код, включи его в пересказ в формате ``` ```.
    -  Если описывается схема или график, включи описание и пояснение этого графика, помимо слов лектора.
    -  Если в лекции есть формулы, включи их в сам пересказ.
    -  Если есть таблицы, включи их в формате markdown.

---

**Текст лекции, которую нужно пересказать:**
"""

gemini_en_prompt = """
I will provide you with the text of a lecture, recognized using Whisper.

Your task is to create an analytical summary of the entire lecture, demonstrating a deep understanding of the material.

### ⚠️ KEY REQUIREMENTS FOR THE SUMMARY:

1. **Analysis and Understanding:**

   - Identify the main themes and sub-themes of the lecture.
   - Analyze the key points and arguments presented by the lecturer.
   - Explain each idea in your own words, avoiding direct copying from the lecture text.
   - Demonstrate your understanding of the material by connecting ideas to each other.
   - Don't just list terms; create meaningful connections between the ideas.
   - Try to draw conclusions based on the information presented.

2. **Structure:**

   - Use heading levels (e.g., `# Heading 1`, `## Heading 2`, `### Heading 3`, etc.) to structure the summary.
   - Analyze each sub-theme in detail. Do not leave sub-themes with only one sentence.

3. **Formatting:**

    - Highlight important terms in bold.
    - Use *italics* to emphasize key ideas.
    - Use lists for enumeration, where appropriate.
    - If necessary, use quotes, tables, and color highlights.

4. **Formulas, Code, Diagrams, Tables:**

    - If code is mentioned or dictated in the lecture, include it in the summary using the ``` ``` format.
    - If a diagram or graph is described, include a description and explanation of this diagram, in addition to the lecturer's words.
    - If formulas are mentioned in the lecture, include them in the summary.
    - If there are tables, include them in markdown format.

---

**Lecture Text to be Summarized:**
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

6. **Код, схемы, таблицы, формулы**
- Если в лекции упоминается программный код (или диктуется), то ты также должен его выписать в формате ``` ```
- Если в лекции описывается или рассматривается схема (или график) , то ты обязан также включить описание этой схемы (графика) в пересказ помимо того что говорит лектор
- Если в лекции упоминаются или диктуются математические (или иные) формулы, то ты также должен их добавлять в сам пересказ, помимо того что описывает лектор
- Если в лекции идет сравнение или обсуждение какой-либо таблицы, то ты должен её включить в формате mardkdown, также если идёт какое либо сравнение (или иные данные), которые могут быть лучше переданы в виду таблицы, то ты должен также указать таблицу

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
- **Example of formatting usage:**
- **Definition:** *Encryption* is the process of...

5. **Preferences:**

- I prefer **longer** and **more detailed** answers.
- **Don't limit yourself to short descriptions**; develop each idea as fully as possible.

6. **Code, diagrams, tables, formulas**
- If the lecture mentions (or dictates) program code, you must also write it out in ``` ``` format
- If the lecture describes or discusses a diagram (or graph), you must also include a description of this diagram (graph) in the retelling in addition to what the lecturer says
- If the lecture mentions or dictates mathematical (or other) formulas, you must also add them to the retelling itself, in addition to what the lecturer describes
- If the lecture compares or discusses any table, you must include it in mardkdown format, and if there is any comparison (or other data) that can be better conveyed in the form of a table, you must also indicate the table

---

**Text of the lecture that needs to be summarized:**
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

6. **Код, схемы, таблицы, формулы**
- Если в лекции упоминается программный код (или диктуется), то ты также должен его выписать в формате ``` ```
- Если в лекции описывается или рассматривается схема (или график) , то ты обязан также включить описание этой схемы (графика) в пересказ помимо того что говорит лектор
- Если в лекции упоминаются или диктуются математические (или иные) формулы, то ты также должен их добавлять в сам пересказ, помимо того что описывает лектор
- Если в лекции идет сравнение или обсуждение какой-либо таблицы, то ты должен её включить в формате mardkdown, также если идёт какое либо сравнение (или иные данные), которые могут быть лучше переданы в виду таблицы, то ты должен также указать таблицу

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
- **Example of formatting usage:**
- **Definition:** *Encryption* is the process of...

5. **Preferences:**

- I prefer **longer** and **more detailed** answers.
- **Don't limit yourself to short descriptions**; develop each idea as fully as possible.

6. **Code, diagrams, tables, formulas**
- If the lecture mentions (or dictates) program code, you must also write it out in ``` ``` format
- If the lecture describes or discusses a diagram (or graph), you must also include a description of this diagram (graph) in the retelling in addition to what the lecturer says
- If the lecture mentions or dictates mathematical (or other) formulas, you must also add them to the retelling itself, in addition to what the lecturer describes
- If the lecture compares or discusses any table, you must include it in mardkdown format, and if there is any comparison (or other data) that can be better conveyed in the form of a table, you must also indicate the table

---

**Text of the lecture that needs to be summarized:**
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

6. **Код, схемы, таблицы, формулы**
- Если в лекции упоминается программный код (или диктуется), то ты также должен его выписать в формате ``` ```
- Если в лекции описывается или рассматривается схема (или график) , то ты обязан также включить описание этой схемы (графика) в пересказ помимо того что говорит лектор
- Если в лекции упоминаются или диктуются математические (или иные) формулы, то ты также должен их добавлять в сам пересказ, помимо того что описывает лектор
- Если в лекции идет сравнение или обсуждение какой-либо таблицы, то ты должен её включить в формате mardkdown, также если идёт какое либо сравнение (или иные данные), которые могут быть лучше переданы в виду таблицы, то ты должен также указать таблицу

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
- **Example of formatting usage:**
- **Definition:** *Encryption* is the process of...

5. **Preferences:**

- I prefer **longer** and **more detailed** answers.
- **Don't limit yourself to short descriptions**; develop each idea as fully as possible.

6. **Code, diagrams, tables, formulas**
- If the lecture mentions (or dictates) program code, you must also write it out in ``` ``` format
- If the lecture describes or discusses a diagram (or graph), you must also include a description of this diagram (graph) in the retelling in addition to what the lecturer says
- If the lecture mentions or dictates mathematical (or other) formulas, you must also add them to the retelling itself, in addition to what the lecturer describes
- If the lecture compares or discusses any table, you must include it in mardkdown format, and if there is any comparison (or other data) that can be better conveyed in the form of a table, you must also indicate the table

---

**Text of the lecture that needs to be summarized:**
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

6. **Код, схемы, таблицы, формулы**
- Если в лекции упоминается программный код (или диктуется), то ты также должен его выписать в формате ``` ```
- Если в лекции описывается или рассматривается схема (или график) , то ты обязан также включить описание этой схемы (графика) в пересказ помимо того что говорит лектор
- Если в лекции упоминаются или диктуются математические (или иные) формулы, то ты также должен их добавлять в сам пересказ, помимо того что описывает лектор
- Если в лекции идет сравнение или обсуждение какой-либо таблицы, то ты должен её включить в формате mardkdown, также если идёт какое либо сравнение (или иные данные), которые могут быть лучше переданы в виду таблицы, то ты должен также указать таблицу

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
- **Example of formatting usage:**
- **Definition:** *Encryption* is the process of...

5. **Preferences:**

- I prefer **longer** and **more detailed** answers.
- **Don't limit yourself to short descriptions**; develop each idea as fully as possible.

6. **Code, diagrams, tables, formulas**
- If the lecture mentions (or dictates) program code, you must also write it out in ``` ``` format
- If the lecture describes or discusses a diagram (or graph), you must also include a description of this diagram (graph) in the retelling in addition to what the lecturer says
- If the lecture mentions or dictates mathematical (or other) formulas, you must also add them to the retelling itself, in addition to what the lecturer describes
- If the lecture compares or discusses any table, you must include it in mardkdown format, and if there is any comparison (or other data) that can be better conveyed in the form of a table, you must also indicate the table

---

**Text of the lecture that needs to be summarized:**
"""