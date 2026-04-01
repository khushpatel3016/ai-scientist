# 🧬 AI Scientist

A locally-running AI research assistant that reads papers, answers questions,
finds research gaps, and generates ranked hypotheses — now with a full web interface.

Built from scratch. No tutorials. No shortcuts.

---

## What this actually is

Most AI projects wrap an API and call it a day.
This one builds the full pipeline manually:

- Extract raw text from a PDF using PyMuPDF
- Split into chunks and embed each one using SentenceTransformers
- Store embeddings in a FAISS index for fast similarity search
- Embed your question the same way and retrieve the most relevant chunks
- Pass those chunks as context to LLaMA 3.3 70B and get a grounded answer
- Feed multiple papers together to find what nobody has solved yet
- Turn those gaps into ranked, testable hypotheses

No hallucination from thin air. The model only answers from what the papers say.

---

## What's been built

### Phase 1 — PDF Reading and Processing
Raw text extraction from PDFs using PyMuPDF.
Text is cleaned and split into chunks so context isn't lost at boundaries.

### Phase 2 — Semantic Q&A
Each chunk is converted into a 384-dimension vector using SentenceTransformers
(all-MiniLM-L6-v2). Vectors go into a FAISS index. When a question comes in,
it gets embedded the same way and cosine similarity finds the top matching chunks.
Those chunks become the context window for LLaMA 3.3 70B on Groq.

### Phase 3 — Research Gap Finder
Accepts multiple PDFs on the same topic. Summarizes each paper independently,
then passes all summaries together to the LLM with a structured prompt that finds
unsolved problems, contradictions between papers, missing experiments, and
concrete directions for new research. Full report saved automatically.

### Phase 4 — Hypothesis Lab
Takes the gap report and generates 5 specific, testable hypotheses with reasoning,
proposed experiments, and expected outcomes. Each hypothesis is then scored and
ranked by novelty, feasibility, and impact.

### Phase 5 — Web Interface
Full Streamlit web app wrapping all four phases. Upload PDFs from the browser,
ask questions, run gap analysis, generate hypotheses, and download reports —
no terminal needed.

---

## System Flow
```
PDF Input
 └─► Text Extraction (PyMuPDF)
      └─► Chunking
           └─► Embedding (SentenceTransformers all-MiniLM-L6-v2)
                └─► FAISS Vector Index
                     └─► Similarity Search on query
                          └─► Context → LLaMA 3.3 70B (Groq)
                               └─► Answer / Gap Report / Hypotheses
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| PDF parsing | PyMuPDF |
| Embeddings | SentenceTransformers — all-MiniLM-L6-v2 |
| Vector search | FAISS |
| Language model | LLaMA 3.3 70B via Groq |
| Web interface | Streamlit |
| Runtime | Python 3.13 |

---

## Project Structure
```
ai-scientist/
├── data/
│   ├── sample.pdf
│   ├── gap_report.txt
│   └── papers/
│       ├── paper1.pdf
│       └── paper2.pdf
├── src/
│   ├── reader.py          # PDF extraction and chunking
│   ├── embedder.py        # Vector embedding
│   ├── retriever.py       # FAISS index and search
│   ├── qa.py              # LLM answer generation
│   ├── gap_finder.py      # Summarization and gap analysis
│   ├── hypothesis.py      # Hypothesis generation and ranking
│   ├── main.py            # Phase 2 CLI entry point
│   ├── phase3.py          # Phase 3 CLI entry point
│   ├── phase4.py          # Phase 4 CLI entry point
│   └── app.py             # Phase 5 — web interface
├── requirements.txt
└── .gitignore
```

---

## Setup
```bash
git clone https://github.com/khushpatel3016/ai-scientist.git
cd ai-scientist

python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

Get a free API key at https://console.groq.com and set it:
```bash
# Windows
$env:GROQ_API_KEY="your-key"

# Mac/Linux
export GROQ_API_KEY="your-key"
```

---

## Running the web interface
```bash
streamlit run src/app.py
```

Opens at http://localhost:8501

---

## CLI usage (no browser)
```bash
# Single paper Q&A
python src/main.py

# Multi-paper gap analysis
python src/phase3.py

# Full report with hypotheses
python src/phase4.py
```

---

## What's next

Planning to add fine-tuning of a small open-source model on academic text
so the system has domain-specific understanding beyond what the base LLM provides.

---

## Author

Khush Patel — CSE undergrad building things that are harder than they look.