import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(context, question):
    prompt = f"""You are an AI research assistant. Use the context below to answer the question.

Context:
{context}

Question: {question}

Answer clearly and concisely:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content