# 🧬 AI Scientist

A locally-running AI system that reads research papers, answers questions about them,
and analyzes multiple papers together to surface research gaps and suggest new directions
— built from scratch, no shortcuts.

---

## What this actually is

Most AI projects you see online wrap an API and call it a day.
This one builds the full pipeline manually:

- Extract raw text from a PDF
- Split it into chunks and convert each chunk into a vector embedding
- Store those embeddings in a FAISS index for fast similarity search
- When you ask a question, embed it the same way and find the most relevant chunks
- Pass those chunks as context to an LLM and get a grounded answer
- Feed multiple papers together and let the system find what nobody has solved yet

No hallucination from thin air. The model only answers from what the papers actually say.

---

## Current State

Phase 3 is complete. The system can:

- Ingest any research paper as a PDF
- Understand it semantically, not just keyword-match
- Answer research-level questions about it in natural language
- Read multiple papers on the same topic and produce a research gap report

---

## How It Was Built

### Phase 1 — Reading and Processing
Started with extracting raw text from PDFs using PyMuPDF.
The text gets cleaned and split into chunks so context
isn't lost at boundaries.

### Phase 2 — Making It Searchable and Answerable
Each chunk gets converted into a 384-dimension vector using
SentenceTransformers (all-MiniLM-L6-v2). These vectors go into a
FAISS index. When a question comes in, it gets embedded the same way,
and similarity search finds the top matching chunks.
Those chunks become the context window for LLaMA 3.3 70B running
through Groq's inference API, which generates the final answer.

### Phase 3 — Research Gap Finder
The system now accepts multiple PDFs on the same topic.
It summarizes each paper independently, then passes all summaries
together to the LLM with a structured prompt that asks it to find:
unsolved problems, contradictions between papers, missing experiments,
and concrete suggestions for new research directions.
The full report is saved as a text file automatically.

---

## System Flow

### Single Paper Q&A (Phase 2)
```
PDF
 └─► Text Extraction (PyMuPDF)
      └─► Chunking
           └─► Embedding (SentenceTransformers)
                └─► FAISS Index
                     └─► Similarity Search on Query
                          └─► Context + Question → LLaMA 3.3 70B
                               └─► Answer
```

### Multi-Paper Gap Analysis (Phase 3)
```
Multiple PDFs
 └─► Extract + Chunk each paper
      └─► Summarize each paper via LLM
           └─► Combine all summaries
                └─► Gap analysis prompt → LLaMA 3.3 70B
                     └─► Gap Report (printed + saved to file)
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| PDF parsing | PyMuPDF |
| Embeddings | SentenceTransformers — all-MiniLM-L6-v2 |
| Vector search | FAISS |
| Language model | LLaMA 3.3 70B via Groq |
| Runtime | Python 3.13 |

---

## Project Structure
```
ai-scientist/
├── data/
│   ├── sample.pdf           # Single paper for Q&A
│   ├── gap_report.txt       # Auto-generated gap analysis report
│   └── papers/              # Multiple papers for gap analysis
│       ├── paper1.pdf
│       ├── paper2.pdf
│       └── paper3.pdf
├── src/
│   ├── reader.py            # PDF extraction and chunking
│   ├── embedder.py          # Vector embedding
│   ├── retriever.py         # FAISS index and search
│   ├── qa.py                # LLM answer generation
│   ├── main.py              # Phase 2 entry point — single paper Q&A
│   ├── gap_finder.py        # Summarization and gap analysis logic
│   └── phase3.py            # Phase 3 entry point — multi-paper analysis
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

## Usage

### Single Paper Q&A
Drop a PDF into `data/` as `sample.pdf`, then:
```bash
python src/main.py
```
```
📄 Reading PDF...
🧠 Creating embeddings...
🔍 Building search index...
✅ Ready.

❓ What problem does this paper solve?
💬 The paper addresses the challenge of...
```

### Multi-Paper Gap Analysis
Drop 2 or more PDFs into `data/papers/`, then:
```bash
python src/phase3.py
```
```
📚 Found 3 papers

📄 Reading: paper1.pdf
   Summarizing... ✅

📄 Reading: paper2.pdf
   Summarizing... ✅

🔍 Analyzing gaps across all papers...

UNSOLVED PROBLEMS
...

CONTRADICTIONS
...

RESEARCH GAPS
...

SUGGESTED DIRECTIONS
...

💾 Report saved to data/gap_report.txt
```

---

## What's Next

Planning to extend this with a web interface where you can upload
papers directly from the browser, run gap analysis with a click,
and read the full report without touching the terminal.

---

## Author

Khush Patel — CSE undergrad building things that are harder than they look.