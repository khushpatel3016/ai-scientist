import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_hypotheses(gap_report: str) -> str:
    prompt = f"""You are an expert research scientist.

Based on the research gap analysis below, generate 5 specific, testable hypotheses.

Gap Analysis:
{gap_report}

For each hypothesis provide:

HYPOTHESIS [number]:
- Statement: (one clear, testable claim)
- Reasoning: (why this gap exists and why this hypothesis makes sense)
- Experiment: (a concrete experiment that would test this hypothesis)
- Expected outcome: (what result would confirm or deny it)

Be specific and grounded in the gaps identified. No generic suggestions."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )

    return response.choices[0].message.content


def rank_ideas(hypotheses: str) -> str:
    prompt = f"""You are a research evaluation expert.

Below are research hypotheses. Score and rank each one.

Hypotheses:
{hypotheses}

For each hypothesis, provide scores out of 10 for:
- Novelty: How original is this idea?
- Feasibility: How realistic is it to test with limited resources?
- Impact: How significant would the results be if proven?
- Overall score: Average of the three

Then provide a final ranked list from most to least recommended,
with one sentence explaining why each is ranked where it is.

Be honest and critical. Not every idea deserves a high score."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )

    return response.choices[0].message.content