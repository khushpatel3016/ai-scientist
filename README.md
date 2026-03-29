# 🧬 AI Scientist

A locally-running AI system that reads research papers and answers questions about them
using semantic search and a large language model — built from scratch, no shortcuts.

---

## What this actually is

Most AI projects you see online wrap an API and call it a day.
This one builds the full pipeline manually:

- Extract raw text from a PDF
- Split it into chunks and convert each chunk into a vector embedding
- Store those embeddings in a FAISS index for fast similarity search
- When you ask a question, embed it the same way and find the most relevant chunks
- Pass those chunks as context to an LLM and get a grounded answer

No hallucination from thin air. The model only answers from what the paper actually says.

---

## Current State

Phase 2 is complete. The system can:

- Ingest any research paper as a PDF
- Understand it semantically, not just keyword-match
- Answer research-level questions about it in natural language

---

## How It Was Built

### Phase 1 — Reading and Processing
Started with extracting raw text from PDFs using PyMuPDF.
The text gets cleaned and split into overlapping chunks so context
isn't lost at chunk boundaries.

### Phase 2 — Making It Searchable and Answerable
Each chunk gets converted into a 384-dimension vector using
SentenceTransformers (all-MiniLM-L6-v2). These vectors go into a
FAISS index. When a question comes in, it gets embedded the same way,
and cosine similarity finds the top matching chunks.
Those chunks become the context window for LLaMA 3.3 70B running
through Groq's inference API, which generates the final answer.

---

## System Flow
```
PDF
 └─► Text Extraction (PyMuPDF)
      └─► Chunking
           └─► Embedding (SentenceTransformers)
                └─► FAISS Index
                     └─► Similarity Search on Query
                          └─► Context + Question → LLaMA 3.3 70B (Groq)
                               └─► Answer
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
│   └── sample.pdf
├── src/
│   ├── reader.py       # PDF extraction and chunking
│   ├── embedder.py     # Vector embedding
│   ├── retriever.py    # FAISS index and search
│   ├── qa.py           # LLM answer generation
│   └── main.py         # Pipeline entry point
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

Drop any research paper PDF into `data/` as `sample.pdf`, then:
```bash
python src/main.py
```

---

## Example
```
📄 Reading PDF...
🧠 Creating embeddings...
🔍 Building search index...
✅ Ready.

❓ What problem does this paper solve?

💬 The paper addresses the challenge of...
```

---

## What's Next

Planning to extend this into a proper research assistant that can
identify gaps in existing literature, suggest directions for new work,
and eventually surface all of this through a web interface.

---

## Author

Khush Patel — CSE undergrad building things that are harder than they look.