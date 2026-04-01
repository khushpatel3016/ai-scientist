import os
import sys
import tempfile
import streamlit as st

sys.path.append(os.path.dirname(__file__))

from reader import extract_text_from_pdf, split_text
from embedder import get_embeddings
from retriever import create_index, search
from qa import generate_answer
from gap_finder import summarize_paper, find_gaps
from hypotheses import generate_hypotheses, rank_ideas
from paper_writer import write_full_paper, format_paper

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Scientist",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #050508;
}

.main .block-container {
    padding: 2rem 2.5rem 4rem;
    max-width: 1100px;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0a0a10;
    border-right: 1px solid #1a1a2e;
}

section[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.25rem;
}

.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #c084fc, #818cf8, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}

.sidebar-sub {
    font-size: 0.7rem;
    color: #3f3f5a;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.6rem 0.9rem;
    border-radius: 10px;
    cursor: pointer;
    margin-bottom: 4px;
    font-size: 0.875rem;
    font-weight: 400;
    color: #6b6b8a;
    transition: all 0.15s;
    text-decoration: none;
}

.nav-item:hover, .nav-item.active {
    background: #12121f;
    color: #e2e2f0;
}

.nav-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #c084fc;
    flex-shrink: 0;
    display: none;
}

.nav-item.active .nav-dot { display: block; }

/* ── Hero ── */
.hero-wrap {
    position: relative;
    margin-bottom: 3rem;
    padding: 3.5rem 3rem;
    border-radius: 20px;
    overflow: hidden;
    background: #0c0c18;
    border: 1px solid #1a1a30;
}

.hero-glow {
    position: absolute;
    top: -60px;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 300px;
    background: radial-gradient(ellipse, rgba(129,140,248,0.12) 0%, transparent 70%);
    pointer-events: none;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(192,132,252,0.08);
    border: 1px solid rgba(192,132,252,0.2);
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #c084fc;
    margin-bottom: 1.25rem;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.05;
    color: #f0f0ff;
    margin-bottom: 1rem;
}

.hero-title span {
    background: linear-gradient(135deg, #c084fc 0%, #818cf8 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-desc {
    font-size: 1rem;
    color: #5a5a7a;
    line-height: 1.7;
    max-width: 520px;
    font-weight: 300;
}

/* ── Cards ── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2.5rem;
}

.feature-card {
    background: #0c0c18;
    border: 1px solid #1a1a2e;
    border-radius: 16px;
    padding: 1.5rem;
    transition: border-color 0.2s;
    cursor: default;
}

.feature-card:hover {
    border-color: #2a2a4a;
}

.card-phase {
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 0.75rem;
}

.phase-2 { color: #38bdf8; }
.phase-3 { color: #c084fc; }
.phase-4 { color: #34d399; }

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e2e2f0;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}

.card-desc {
    font-size: 0.8rem;
    color: #3f3f5a;
    line-height: 1.6;
    font-weight: 300;
}

/* ── Section headers ── */
.section-header {
    margin-bottom: 1.5rem;
}

.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3f3f5a;
    margin-bottom: 0.4rem;
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #e2e2f0;
    letter-spacing: -0.03em;
}

/* ── Upload zone ── */
.upload-hint {
    font-size: 0.8rem;
    color: #3f3f5a;
    margin-top: 0.5rem;
    font-weight: 300;
}

/* ── Stats row ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin: 1.5rem 0;
}

.stat-box {
    background: #0c0c18;
    border: 1px solid #1a1a2e;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    text-align: center;
}

.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #c084fc;
    letter-spacing: -0.03em;
}

.stat-label {
    font-size: 0.7rem;
    color: #3f3f5a;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}

/* ── Answer output ── */
.answer-wrap {
    background: #0c0c18;
    border: 1px solid #1a1a2e;
    border-left: 3px solid #c084fc;
    border-radius: 0 12px 12px 0;
    padding: 1.5rem 1.75rem;
    color: #b0b0d0;
    font-size: 0.9rem;
    line-height: 1.8;
    font-weight: 300;
    margin-top: 1rem;
}

/* ── Report output ── */
.report-wrap {
    background: #07070f;
    border: 1px solid #1a1a2e;
    border-radius: 12px;
    padding: 1.5rem;
    color: #6b6b8a;
    font-family: 'DM Mono', 'Fira Code', monospace;
    font-size: 0.78rem;
    line-height: 1.8;
    white-space: pre-wrap;
    max-height: 520px;
    overflow-y: auto;
}

/* ── Input field ── */
.stTextInput input, .stTextArea textarea {
    background: #0c0c18 !important;
    border: 1px solid #1a1a2e !important;
    border-radius: 10px !important;
    color: #e2e2f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #c084fc !important;
    box-shadow: 0 0 0 2px rgba(192,132,252,0.1) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.75rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.15s !important;
    width: 100% !important;
}

.stButton > button:hover {
    opacity: 0.88 !important;
}

/* ── Radio buttons (nav) ── */
.stRadio > div {
    gap: 4px !important;
}

.stRadio label {
    background: transparent !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.75rem !important;
    color: #6b6b8a !important;
    font-size: 0.875rem !important;
    transition: all 0.15s !important;
}

.stRadio label:hover {
    background: #12121f !important;
    color: #e2e2f0 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #0c0c18 !important;
    border: 1px dashed #1a1a2e !important;
    border-radius: 12px !important;
}

/* ── Success / info ── */
.stSuccess {
    background: rgba(52,211,153,0.05) !important;
    border-left: 3px solid #34d399 !important;
    border-radius: 0 8px 8px 0 !important;
    color: #34d399 !important;
}

/* ── Progress ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #7c3aed, #38bdf8) !important;
}

/* ── Divider ── */
hr {
    border-color: #1a1a2e !important;
}

/* ── Flow diagram ── */
.flow-wrap {
    background: #07070f;
    border: 1px solid #1a1a2e;
    border-radius: 14px;
    padding: 2rem;
    display: flex;
    align-items: center;
    gap: 0;
    overflow-x: auto;
    margin-top: 1.5rem;
}

.flow-node {
    background: #0c0c18;
    border: 1px solid #1a1a2e;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.72rem;
    color: #6b6b8a;
    white-space: nowrap;
    flex-shrink: 0;
}

.flow-node.highlight {
    border-color: #7c3aed;
    color: #c084fc;
}

.flow-arrow {
    color: #1a1a2e;
    font-size: 1rem;
    padding: 0 0.4rem;
    flex-shrink: 0;
}

.stack-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #0c0c18;
    border: 1px solid #1a1a2e;
    border-radius: 999px;
    padding: 0.35rem 0.85rem;
    font-size: 0.72rem;
    color: #6b6b8a;
    margin: 0.25rem;
}

.stack-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #7c3aed;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1a1a2e; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>AI Scientist</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-sub'>Autonomous Research System</div>", unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["Home", "Paper Q&A", "Gap Finder", "Hypothesis Lab"],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.7rem;color:#3f3f5a;text-transform:uppercase;"
        "letter-spacing:0.1em;margin-bottom:0.75rem;'>API Key</p>",
        unsafe_allow_html=True
    )

    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        label_visibility="collapsed"
    )

    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
        st.success("Key active")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.68rem;color:#2a2a3a;line-height:1.6;'>"
        "PyMuPDF · SentenceTransformers<br>FAISS · LLaMA 3.3 70B · Groq"
        "</p>",
        unsafe_allow_html=True
    )

    page = st.radio(
    "nav",
    ["Home", "Paper Q&A", "Gap Finder", "Hypothesis Lab", "Paper Writer"],
    label_visibility="collapsed"
)


# ══════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════
if page == "Home":

    st.markdown("""
    <div class='hero-wrap'>
        <div class='hero-glow'></div>
        <div class='hero-badge'>&#9679; Research Intelligence</div>
        <div class='hero-title'>Turn papers into<br><span>research breakthroughs</span></div>
        <div class='hero-desc'>
            Upload research papers. Ask anything about them. 
            Discover what's unsolved across the field. 
            Generate and rank new hypotheses — all powered by LLaMA 3.3.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='feature-grid'>
        <div class='feature-card'>
            <div class='card-phase phase-2'>Phase 2</div>
            <div class='card-title'>Paper Q&A</div>
            <div class='card-desc'>Upload any PDF. Ask research-level questions. 
            Semantic search finds the right context before the LLM answers.</div>
        </div>
        <div class='feature-card'>
            <div class='card-phase phase-3'>Phase 3</div>
            <div class='card-title'>Gap Finder</div>
            <div class='card-desc'>Upload multiple papers on the same topic. 
            The AI finds contradictions, unsolved problems, and missing experiments.</div>
        </div>
        <div class='feature-card'>
            <div class='card-phase phase-4'>Phase 4</div>
            <div class='card-title'>Hypothesis Lab</div>
            <div class='card-desc'>Turns research gaps into specific, testable hypotheses — 
            scored by novelty, feasibility, and impact.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-header'>
        <div class='section-label'>Architecture</div>
        <div class='section-title'>How it works</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='flow-wrap'>
        <div class='flow-node highlight'>PDF Input</div>
        <div class='flow-arrow'>→</div>
        <div class='flow-node'>Text Extraction</div>
        <div class='flow-arrow'>→</div>
        <div class='flow-node'>Chunking</div>
        <div class='flow-arrow'>→</div>
        <div class='flow-node highlight'>Embeddings</div>
        <div class='flow-arrow'>→</div>
        <div class='flow-node'>FAISS Index</div>
        <div class='flow-arrow'>→</div>
        <div class='flow-node'>Similarity Search</div>
        <div class='flow-arrow'>→</div>
        <div class='flow-node highlight'>LLaMA 3.3 70B</div>
        <div class='flow-arrow'>→</div>
        <div class='flow-node'>Output</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div>
        <span class='stack-badge'><span class='stack-dot'></span>PyMuPDF</span>
        <span class='stack-badge'><span class='stack-dot'></span>SentenceTransformers</span>
        <span class='stack-badge'><span class='stack-dot'></span>FAISS</span>
        <span class='stack-badge'><span class='stack-dot'></span>LLaMA 3.3 70B</span>
        <span class='stack-badge'><span class='stack-dot'></span>Groq Inference</span>
        <span class='stack-badge'><span class='stack-dot'></span>Python 3.13</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAPER Q&A
# ══════════════════════════════════════════════════════════════
elif page == "Paper Q&A":

    st.markdown("""
    <div class='section-header'>
        <div class='section-label'>Phase 2</div>
        <div class='section-title'>Paper Q&A</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop your PDF here",
        type="pdf",
        label_visibility="collapsed"
    )
    st.markdown("<p class='upload-hint'>Supports any research paper PDF</p>", unsafe_allow_html=True)

    if uploaded:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        with st.spinner("Indexing paper..."):
            text = extract_text_from_pdf(tmp_path)
            chunks = split_text(text)
            embeddings = get_embeddings(chunks)
            index = create_index(embeddings)

        st.markdown(f"""
        <div class='stats-row'>
            <div class='stat-box'>
                <div class='stat-num'>{len(text) // 3000 + 1}</div>
                <div class='stat-label'>Pages</div>
            </div>
            <div class='stat-box'>
                <div class='stat-num'>{len(chunks)}</div>
                <div class='stat-label'>Chunks</div>
            </div>
            <div class='stat-box'>
                <div class='stat-num'>{len(embeddings)}</div>
                <div class='stat-label'>Embeddings</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"'{uploaded.name}' indexed and ready")
        st.markdown("<hr>", unsafe_allow_html=True)

        question = st.text_input(
            "Ask anything about this paper",
            placeholder="What problem does this paper solve and why is it important?",
            label_visibility="collapsed"
        )

        if st.button("Get Answer") and question:
            if not os.getenv("GROQ_API_KEY"):
                st.error("Add your Groq API key in the sidebar.")
            else:
                with st.spinner("Searching and reasoning..."):
                    query_emb = get_embeddings([question])
                    indices = search(index, query_emb)
                    context = " ".join([chunks[i] for i in indices if i < len(chunks)])
                    answer = generate_answer(context, question)

                st.markdown(
                    f"<div class='answer-wrap'>{answer}</div>",
                    unsafe_allow_html=True
                )


# ══════════════════════════════════════════════════════════════
# GAP FINDER
# ══════════════════════════════════════════════════════════════
elif page == "Gap Finder":

    st.markdown("""
    <div class='section-header'>
        <div class='section-label'>Phase 3</div>
        <div class='section-title'>Research Gap Finder</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='color:#3f3f5a;font-size:0.85rem;margin-bottom:1.5rem;font-weight:300;'>"
        "Upload 2 or more papers on the same topic. The system summarizes each one "
        "then analyzes them together to surface contradictions, unsolved problems, "
        "and unexplored experiments."
        "</p>",
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        st.markdown(
            f"<p style='font-size:0.8rem;color:#6b6b8a;margin-top:0.5rem;'>"
            f"{len(uploaded_files)} paper{'s' if len(uploaded_files) != 1 else ''} selected"
            f"{'  ·  Add at least one more' if len(uploaded_files) < 2 else ''}"
            f"</p>",
            unsafe_allow_html=True
        )

    if uploaded_files and len(uploaded_files) >= 2:
        if st.button("Find Research Gaps"):
            if not os.getenv("GROQ_API_KEY"):
                st.error("Add your Groq API key in the sidebar.")
            else:
                summaries = []
                progress = st.progress(0)
                status = st.empty()

                for i, f in enumerate(uploaded_files):
                    status.markdown(
                        f"<p style='font-size:0.8rem;color:#6b6b8a;'>Reading {f.name}...</p>",
                        unsafe_allow_html=True
                    )
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(f.read())
                        tmp_path = tmp.name

                    text = extract_text_from_pdf(tmp_path)
                    chunks = split_text(text)
                    summary = summarize_paper(chunks)
                    summaries.append(summary)
                    progress.progress((i + 1) / len(uploaded_files))

                status.markdown(
                    "<p style='font-size:0.8rem;color:#6b6b8a;'>Analyzing across all papers...</p>",
                    unsafe_allow_html=True
                )
                gap_report = find_gaps(summaries)
                status.empty()
                progress.empty()

                st.success("Analysis complete")
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='font-size:0.75rem;color:#3f3f5a;text-transform:uppercase;"
                    "letter-spacing:0.1em;margin-bottom:0.75rem;'>Gap Report</p>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div class='report-wrap'>{gap_report}</div>",
                    unsafe_allow_html=True
                )

                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "Download Gap Report",
                        data=gap_report,
                        file_name="gap_report.txt",
                        mime="text/plain"
                    )
                with col2:
                    if st.button("Send to Hypothesis Lab →"):
                        st.session_state["gap_report"] = gap_report
                        st.success("Sent — switch to Hypothesis Lab")

    elif uploaded_files and len(uploaded_files) < 2:
        st.warning("Upload at least 2 papers to compare.")


# ══════════════════════════════════════════════════════════════
# HYPOTHESIS LAB
# ══════════════════════════════════════════════════════════════
elif page == "Hypothesis Lab":

    st.markdown("""
    <div class='section-header'>
        <div class='section-label'>Phase 4</div>
        <div class='section-title'>Hypothesis Lab</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='color:#3f3f5a;font-size:0.85rem;margin-bottom:1.5rem;font-weight:300;'>"
        "Paste a gap report below — or run the Gap Finder first and send it here directly. "
        "The system generates 5 testable hypotheses and ranks them by novelty, feasibility, and impact."
        "</p>",
        unsafe_allow_html=True
    )

    gap_input = st.text_area(
        "Gap report",
        height=180,
        placeholder="Paste your gap analysis output here...",
        value=st.session_state.get("gap_report", ""),
        label_visibility="collapsed"
    )

    if st.button("Generate & Rank Hypotheses") and gap_input:
        if not os.getenv("GROQ_API_KEY"):
            st.error("Add your Groq API key in the sidebar.")
        else:
            with st.spinner("Generating hypotheses..."):
                hypotheses = generate_hypotheses(gap_input)

            with st.spinner("Scoring and ranking..."):
                rankings = rank_ideas(hypotheses)
            
            st.session_state["hypotheses"] = hypotheses
            st.session_state["rankings"] = rankings

            st.markdown("<hr>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    "<p style='font-size:0.75rem;color:#3f3f5a;text-transform:uppercase;"
                    "letter-spacing:0.1em;margin-bottom:0.75rem;'>Hypotheses</p>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div class='report-wrap'>{hypotheses}</div>",
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    "<p style='font-size:0.75rem;color:#3f3f5a;text-transform:uppercase;"
                    "letter-spacing:0.1em;margin-bottom:0.75rem;'>Rankings</p>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div class='report-wrap'>{rankings}</div>",
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)
            full_report = (
                f"HYPOTHESES\n{'='*60}\n\n{hypotheses}"
                f"\n\nRANKINGS\n{'='*60}\n\n{rankings}"
            )
            st.download_button(
                "Download Full Report",
                data=full_report,
                file_name="hypothesis_report.txt",
                mime="text/plain"
            )

# ══════════════════════════════════════════════════════════════
# PAPER WRITER
# ══════════════════════════════════════════════════════════════
elif page == "Paper Writer":

    st.markdown("""
    <div class='section-header'>
        <div class='section-label'>Phase 5</div>
        <div class='section-title'>AI Paper Writer</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='color:#3f3f5a;font-size:0.85rem;margin-bottom:1.5rem;font-weight:300;'>"
        "Give it a research idea, a gap, and a hypothesis — it writes a complete "
        "academic paper with title, abstract, introduction, methodology, results, and conclusion."
        "</p>",
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["Manual Input", "Load from Phase 4"])

    with tab1:
        idea = st.text_area(
            "Research idea",
            height=100,
            placeholder="Describe your research idea clearly...",
            label_visibility="collapsed"
        )
        gap = st.text_area(
            "Research gap",
            height=100,
            placeholder="What problem or gap does this address?",
            label_visibility="collapsed"
        )
        hypothesis = st.text_area(
            "Main hypothesis",
            height=80,
            placeholder="Your main testable hypothesis...",
            label_visibility="collapsed"
        )
        rankings = st.text_area(
            "Rankings or scores (optional)",
            height=60,
            placeholder="Paste idea rankings from Hypothesis Lab if available...",
            label_visibility="collapsed"
        )

        if st.button("Write Research Paper", key="manual_write"):
            if not idea or not gap or not hypothesis:
                st.error("Fill in at least the idea, gap, and hypothesis.")
            elif not os.getenv("GROQ_API_KEY"):
                st.error("Add your Groq API key in the sidebar.")
            else:
                with st.spinner("Writing your paper — this takes about 30 seconds..."):
                    paper = write_full_paper(idea, gap, hypothesis, rankings)
                    formatted = format_paper(paper)

                st.success("Paper generated")
                st.markdown(
                    f"<div class='report-wrap'>{formatted}</div>",
                    unsafe_allow_html=True
                )
                st.download_button(
                    "Download Paper",
                    data=formatted,
                    file_name="research_paper.txt",
                    mime="text/plain"
                )

    with tab2:
        st.markdown(
            "<p style='color:#3f3f5a;font-size:0.82rem;font-weight:300;'>"
            "Run the Gap Finder and Hypothesis Lab first, then come here. "
            "If you used the CLI (phase4.py), the report is in your data/ folder."
            "</p>",
            unsafe_allow_html=True
        )

        gap_val = st.session_state.get("gap_report", "")
        hyp_val = st.session_state.get("hypotheses", "")
        rank_val = st.session_state.get("rankings", "")

        if gap_val or hyp_val:
            st.success("Phase 4 data detected from this session")
            auto_idea = hyp_val[:500] if hyp_val else ""
            auto_gap = gap_val[:1000] if gap_val else ""
            auto_hyp = hyp_val[:500] if hyp_val else ""
            auto_rank = rank_val[:500] if rank_val else ""

            st.markdown(
                f"<p style='font-size:0.78rem;color:#6b6b8a;'>"
                f"Gap: {len(auto_gap)} chars · Hypothesis: {len(auto_hyp)} chars"
                f"</p>",
                unsafe_allow_html=True
            )

            if st.button("Write Paper from Phase 4 Data", key="auto_write"):
                if not os.getenv("GROQ_API_KEY"):
                    st.error("Add your Groq API key in the sidebar.")
                else:
                    with st.spinner("Writing your paper — this takes about 30 seconds..."):
                        paper = write_full_paper(auto_idea, auto_gap, auto_hyp, auto_rank)
                        formatted = format_paper(paper)

                    st.success("Paper generated")
                    st.markdown(
                        f"<div class='report-wrap'>{formatted}</div>",
                        unsafe_allow_html=True
                    )
                    st.download_button(
                        "Download Paper",
                        data=formatted,
                        file_name="research_paper.txt",
                        mime="text/plain"
                    )
        else:
            st.info("No Phase 4 data in this session yet. Use the Gap Finder and Hypothesis Lab first, or use Manual Input.")