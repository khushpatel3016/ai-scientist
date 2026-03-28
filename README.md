# 🧬 AI Scientist: Research Paper Intelligence System

An advanced AI system that reads research papers, understands them, and answers questions using modern Retrieval-Augmented Generation (RAG) techniques.

---

## 🚀 Project Overview

This project aims to simulate the early stages of an **AI Scientist** by enabling machines to:

* 📄 Read and process research papers (PDFs)
* 🧠 Understand content using embeddings
* 🔍 Retrieve relevant knowledge
* 💬 Answer complex questions intelligently

---

## 🧩 Completed Phases

### 🥇 Phase 1: PDF Reader & Summarizer

**Objective:** Convert research papers into readable summaries

**What I built:**

* Extracted text from PDFs using PyMuPDF
* Implemented sentence-based summarization using NLTK
* Built a clean pipeline: `PDF → Text → Summary`

**Tech Used:**

* Python
* PyMuPDF (`fitz`)
* NLTK

---

### 🥈 Phase 2: RAG-Based Question Answering System

**Objective:** Enable AI to answer questions from research papers

**What I built:**

* Split document into meaningful chunks
* Generated embeddings using sentence-transformers
* Stored embeddings in FAISS vector database
* Implemented similarity search to retrieve relevant context
* Integrated OpenAI API to generate intelligent answers

**Pipeline:**

```
PDF → Text → Chunks → Embeddings → Vector DB → Query → Context → AI Answer
```

**Tech Used:**

* sentence-transformers (MiniLM model)
* FAISS (vector search)
* OpenAI API (LLM)
* NumPy

---

## ⚙️ System Architecture

```
                ┌──────────────┐
                │   PDF File   │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Text Extract │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Text Chunks  │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Embeddings   │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ FAISS Index  │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Query Input  │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Context Fetch│
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ OpenAI Model │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Final Answer │
                └──────────────┘
```

---

## 💻 How to Run

### 1. Clone Repository

```bash
git clone https://github.com/your-username/ai-scientist.git
cd ai-scientist
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install pymupdf nltk sentence-transformers faiss-cpu openai
```

### 4. Set OpenAI API Key

```bash
setx OPENAI_API_KEY "your-api-key"
```

### 5. Run the Project

```bash
python src/main.py
```

---

## 🧪 Example Usage

```
Ask a question:
→ What problem does this paper solve?

Answer:
→ The paper proposes...
```

---

## 📈 Key Learnings

* Handling real-world dependency issues (Python compatibility, transformers, etc.)
* Understanding embedding-based retrieval systems
* Building a full RAG pipeline from scratch
* Managing GitHub project structure professionally
* Integrating APIs securely using environment variables

---

## 🔥 Future Scope (Upcoming Phases)

### 🥉 Phase 3: AI Research Idea Generator

* Generate novel research ideas from papers

### 🧪 Phase 4: Experiment Generator

* Convert ideas into runnable ML experiments

### 📝 Phase 5: AI Paper Writer

* Automatically generate full research papers

---

## 🎯 Why This Project Stands Out

* Goes beyond basic ML projects
* Implements real-world AI architecture (RAG)
* Demonstrates system design + AI integration
* Shows strong problem-solving and debugging skills

---

## 👨‍💻 Author

**Khush Patel**
CSE Core Student | AI & Systems Enthusiast

---

## ⭐ If you like this project

Give it a star ⭐ and follow for upcoming phases!
