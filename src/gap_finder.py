import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def find_gaps(paper_summaries: list[str]) -> str:
    combined = ""
    for i, summary in enumerate(paper_summaries):
        combined += f"\n\n--- Paper {i+1} ---\n{summary}"

    prompt = f"""You are an expert AI research analyst.

Below are summaries extracted from multiple research papers on the same topic.

{combined}

Analyze these papers carefully and provide:

1. UNSOLVED PROBLEMS
   - What challenges do these papers admit they haven't solved?
   - What limitations do they mention?

2. CONTRADICTIONS
   - Where do these papers disagree with each other?
   - What claims conflict?

3. RESEARCH GAPS
   - What important questions are none of these papers answering?
   - What experiments have not been tried?

4. SUGGESTED DIRECTIONS
   - Based on the gaps, suggest 3 specific new research ideas
     that would be genuinely novel and feasible

Be specific. Reference actual content from the papers, not generic advice."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )

    return response.choices[0].message.content


def summarize_paper(chunks: list[str]) -> str:
    sample = " ".join(chunks[:10])

    prompt = f"""Summarize this research paper extract in 200 words.
Focus on: problem being solved, method used, key results, and limitations.

Paper extract:
{sample}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )

    return response.choices[0].message.content