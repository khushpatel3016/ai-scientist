# 🧬 AI Scientist — Autonomous Research Assistant

An AI-powered system that reads research papers, understands them semantically, 
answers questions about them, and will evolve into a fully autonomous research agent 
capable of finding gaps, generating hypotheses, and proposing experiments.

> Built from scratch as a portfolio project — no tutorials, no copy-paste.

---

## 🚀 Live Demo
*Web interface coming soon (Phase 5)*

---

## 🧠 What It Does

| Feature | Status |
|---|---|
| PDF ingestion & text extraction | ✅ Done |
| Semantic search with embeddings | ✅ Done |
| AI-powered Q&A on research papers | ✅ Done |
| Research gap finder | 🔨 In Progress |
| Hypothesis generator | 🔨 In Progress |
| Web interface | 📅 Planned |

---

## 🏗️ System Architecture
```
PDF Input
   ↓
Text Extraction (PyMuPDF)
   ↓
Chunking + Embedding (SentenceTransformers)
   ↓
Vector Search (FAISS)
   ↓
Context Retrieval
   ↓
LLM Answer Generation (Groq - LLaMA 3.3)
   ↓
Research Insight Output
```

---

## ⚙️ Tech Stack

- **Language:** Python 3.13
- **PDF Processing:** PyMuPDF (fitz)
- **Embeddings:** SentenceTransformers (`all-MiniLM-L6-v2`)
- **Vector Database:** FAISS
- **LLM:** LLaMA 3.3 70B via Groq API
- **Web UI (coming):** Streamlit

---

## 📁 Project Structure
```
ai-scientist/
├── data/
│   └── sample.pdf          # Input research paper
├── src/
│   ├── reader.py           # PDF text extraction + chunking
│   ├── embedder.py         # Semantic embeddings
│   ├── retriever.py        # FAISS vector search
│   ├── qa.py               # LLM answer generation
│   └── main.py             # Main pipeline
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/khushpatel3016/ai-scientist.git
cd ai-scientist
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your API key
```bash
# Windows PowerShell
$env:GROQ_API_KEY="your-groq-api-key"

# Mac/Linux
export GROQ_API_KEY="your-groq-api-key"
```
Get a free Groq API key at: https://console.groq.com

### 5. Add a research paper
Place any PDF inside the `data/` folder and rename it `sample.pdf`

### 6. Run
```bash
python src/main.py
```

---

## 💬 Example Output
```
📄 Reading PDF...
   Split into 47 chunks

🧠 Creating embeddings...

🔍 Building search index...

✅ System ready! Ask anything about the paper.

❓ Your question: What problem does this paper solve?

💬 Answer:
The paper addresses the challenge of...
```

---

## 🗺️ Roadmap

- [x] Phase 1 — PDF reader + summarizer
- [x] Phase 2 — RAG system (semantic search + Q&A)
- [ ] Phase 3 — Research gap finder
- [ ] Phase 4 — Hypothesis + idea generator
- [ ] Phase 5 — Web interface (Streamlit)

---

## 👨‍💻 Author

**Khush Patel**  
CSE Student | AI/ML Enthusiast  
[GitHub](https://github.com/khushpatel3016)

---

## ⭐ Star this repo if you find it useful!

After pasting, run these in terminal to push it:
powershellgit add README.md
git commit -m "Added detailed README with architecture and roadmap"
git push