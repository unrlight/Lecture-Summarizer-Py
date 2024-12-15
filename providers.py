import openai

def oai_inference (prompt, input_max_tokens, input_temp, input_model):

    response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=input_model,
        max_completion_tokens=input_max_tokens,
        temperature=input_temp / 2
    )

    generated_text = response.choices[0].message.content.strip()
    return generated_text