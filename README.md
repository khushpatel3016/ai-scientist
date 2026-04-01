🧠 AI Scientist

A multi-stage autonomous research framework that moves beyond document retrieval and toward independent knowledge generation.

What this project is about

AI Scientist is built around a simple but powerful idea:

reading papers is not enough — systems should be able to analyze, question, and create new research directions

Instead of acting like a traditional RAG pipeline, this system takes multiple research papers, compares them, finds gaps, and turns those gaps into structured hypotheses and full academic drafts.

It is designed for workflows where understanding and discovery matter more than just answering queries.

Why AI Scientist

Most AI systems today stop at retrieval.

They can:

fetch relevant chunks
summarize content
answer questions

But they don’t:

compare multiple papers deeply
detect contradictions
identify missing experiments
propose new research ideas

AI Scientist is built to close that gap.

It keeps the grounding of RAG but extends it into a multi-phase research pipeline that simulates how actual researchers think.

What it does

The system can:

extract structured content from complex academic PDFs
build semantic understanding using embeddings
compare multiple papers side-by-side
identify research gaps and inconsistencies
generate multiple hypotheses with experimental directions
rank ideas based on impact and feasibility
expand the best idea into a full research paper
How it works
Research Analysis Flow

A set of research papers is uploaded into the system.

Each paper is:

parsed
chunked
embedded
summarized

These summaries are then compared using an LLM to identify:

contradictions
missing links
unexplored areas

The output is a structured Gap Report stored locally.

Research Synthesis Flow

The Gap Report becomes the input for idea generation.

The system:

generates multiple hypotheses
attaches experimental approaches
evaluates each idea using scoring metrics

The highest-ranked idea is then expanded into a complete academic manuscript with standard sections.

System Breakdown

The architecture is divided into phases, each handling a distinct part of the research lifecycle.

Phase 1 & 2 — Ingestion and Understanding
PDF extraction using PyMuPDF
Chunking and preprocessing
Embeddings using SentenceTransformers
FAISS-based semantic retrieval
Context-aware Q&A with LLaMA 3.3 70B
Phase 3 & 4 — Gap Discovery
multi-paper summarization
comparative reasoning
identification of:
missing experiments
conflicting claims
unexplored research areas
hypothesis generation with scoring
Phase 5 — Paper Generation
structured expansion of ideas into:
Abstract
Introduction
Related Work
Methodology
Results
Conclusion
Tech Stack
Layer	Implementation
Language	Python 3.13
PDF Processing	PyMuPDF
Embeddings	all-MiniLM-L6-v2
Vector Search	FAISS
LLM Inference	Groq API
Model	LLaMA 3.3 70B
Interface	Streamlit
Project Structure
.
├── data/               # PDFs, gap reports, generated papers
├── src/
│   ├── app.py
│   ├── reader.py
│   ├── embedder.py
│   ├── retriever.py
│   ├── qa.py
│   ├── gap_finder.py
│   ├── hypothesis.py
│   └── paper_writer.py
├── requirements.txt
└── .gitignore
Setup
Requirements
Python 3.13
Groq API key
virtual environment recommended
Environment
GROQ_API_KEY=your_api_key
Run locally
git clone https://github.com/khushpatel3016/ai-scientist.git
cd ai-scientist

pip install -r requirements.txt
streamlit run src/app.py
Design Approach

This project is built with a few clear principles in mind:

grounded generation over hallucination
everything is derived from actual research inputs
modular pipeline over monolithic design
each stage is independent and testable
research workflow over chatbot interaction
the goal is discovery, not just answers
speed and efficiency
FAISS for retrieval and Groq for fast inference
Where this can be used
academic research assistance
literature review automation
idea generation for projects or papers
early-stage research prototyping
student and IEEE-style projects