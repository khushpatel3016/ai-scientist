# 🧬 AI Scientist

An end-to-end autonomous research assistant that reads papers, answers questions,
finds gaps in existing literature, generates ranked hypotheses, writes full research
papers, and exposes everything through a web interface.

Built from scratch. No tutorials. No shortcuts.

---

## What this actually is

Most AI projects wrap an API and call it a day.
This one builds the full pipeline manually:

- Extract raw text from PDFs using PyMuPDF
- Split into chunks and embed each one using SentenceTransformers
- Store embeddings in a FAISS index for fast similarity search
- Embed your question the same way and retrieve the most relevant chunks
- Pass those chunks as context to LLaMA 3.3 70B and get a grounded answer
- Feed multiple papers together to find contradictions and unsolved problems
- Turn those gaps into specific, testable, ranked hypotheses
- Write a complete academic research paper from those hypotheses

No hallucination from thin air. The model only answers from what the papers say.

---

## What's been built

### Phase 1 — PDF Reading and Processing
Raw text extraction from research PDFs using PyMuPDF.
Text is cleaned and split into chunks so context isn't lost at boundaries.

### Phase 2 — Semantic Q&A
Each chunk is converted into a 384-dimension vector using SentenceTransformers
(all-MiniLM-L6-v2). Vectors go into a FAISS index. When a question comes in
it gets embedded the same way and cosine similarity finds the top matching chunks.
Those chunks become the context window for LLaMA 3.3 70B on Groq.

### Phase 3 — Research Gap Finder
Accepts multiple PDFs on the same topic. Summarizes each paper independently,
then passes all summaries to the LLM with a structured prompt that surfaces
unsolved problems, contradictions between papers, missing experiments,
and concrete directions for new research. Full report saved automatically.

### Phase 4 — Hypothesis Lab
Takes the gap report and generates 5 specific, testable hypotheses — each with
reasoning, a proposed experiment, and expected outcomes. Every hypothesis is
then scored and ranked by novelty, feasibility, and impact.

### Phase 5 — AI Paper Writer
Takes a research idea, gap, and hypothesis as input and generates a complete
academic research paper with title, abstract, introduction, related work,
methodology, results, and conclusion. Accepts input manually or automatically
from Phase 4 output. Paper saved as a text file.

### Web Interface
Full Streamlit web app wrapping all five phases. Upload PDFs from the browser,
ask questions, run gap analysis, generate hypotheses, write papers, and download
everything — no terminal needed.

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
                               └─► Answer / Gap Report / Hypotheses / Paper
```

---

## Web Interface

Five pages, one sidebar:

| Page | What it does |
|---|---|
| Home | Architecture overview, feature cards, tech stack |
| Paper Q&A | Upload PDF, ask questions, get grounded answers |
| Gap Finder | Upload multiple PDFs, get full gap analysis report |
| Hypothesis Lab | Generate and rank testable hypotheses from gaps |
| Paper Writer | Write a complete research paper from idea to conclusion |

The workflow is connected end to end — Gap Finder passes its output directly
to Hypothesis Lab, which passes its output directly to Paper Writer.

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
│   ├── sample.pdf               # Single paper for Q&A
│   ├── gap_report.txt           # Auto-generated gap report
│   ├── full_report_[timestamp].txt   # Phase 4 full report
│   ├── research_paper_[timestamp].txt  # Phase 5 generated paper
│   └── papers/                  # Multiple papers for gap analysis
│       ├── paper1.pdf
│       └── paper2.pdf
├── src/
│   ├── reader.py          # PDF extraction and chunking
│   ├── embedder.py        # Vector embedding
│   ├── retriever.py       # FAISS index and search
│   ├── qa.py              # LLM answer generation
│   ├── gap_finder.py      # Paper summarization and gap analysis
│   ├── hypothesis.py      # Hypothesis generation and ranking
│   ├── paper_writer.py    # Section-by-section paper generation
│   ├── main.py            # Phase 2 CLI
│   ├── phase3.py          # Phase 3 CLI
│   ├── phase4.py          # Phase 4 CLI
│   ├── phase5.py          # Phase 5 CLI
│   └── app.py             # Web interface
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

Enter your Groq API key in the sidebar and you're ready.

---

## CLI usage
```bash
# Phase 2 — single paper Q&A
python src/main.py

# Phase 3 — multi-paper gap analysis
python src/phase3.py

# Phase 4 — hypothesis generation and ranking
python src/phase4.py

# Phase 5 — AI paper writer
python src/phase5.py
```

---

## Full workflow example
```
1. Drop papers into data/papers/
2. Run Gap Finder → get gap_report.txt
3. Run Hypothesis Lab → get ranked hypotheses
4. Run Paper Writer → get full research paper
```

Or do the entire thing in the browser with no terminal.

---

## Author

Khush Patel — CSE undergrad building things that are harder than they look.
[GitHub](https://github.com/khushpatel3016/ai-scientist)