from openai import OpenAI
    
client = OpenAI()

def generate_answer(context, question):
    prompt = f"""
    Context: {context}
    Question: {question}
    Answer:
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content