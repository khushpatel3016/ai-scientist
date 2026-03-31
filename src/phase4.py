import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(__file__))

from reader import extract_text_from_pdf, split_text
from gap_finder import summarize_paper, find_gaps
from hypotheses import generate_hypotheses, rank_ideas

papers_dir = "data/papers"

pdf_files = [
    f for f in os.listdir(papers_dir)
    if f.endswith(".pdf")
]

if len(pdf_files) < 2:
    print("❌ Add at least 2 PDF papers inside data/papers/")
    sys.exit()

print(f"📚 Found {len(pdf_files)} papers\n")

# Step 1: Summarize all papers
summaries = []
for pdf_file in pdf_files:
    path = os.path.join(papers_dir, pdf_file)
    print(f"📄 Reading: {pdf_file}")
    text = extract_text_from_pdf(path)
    chunks = split_text(text)
    print(f"   Summarizing...")
    summary = summarize_paper(chunks)
    summaries.append((pdf_file, summary))
    print(f"   ✅ Done\n")

# Step 2: Find gaps
print("🔍 Finding research gaps...\n")
gap_report = find_gaps([s for _, s in summaries])

print("💡 Generating hypotheses...\n")
hypotheses = generate_hypotheses(gap_report)

print("📊 Ranking ideas...\n")
rankings = rank_ideas(hypotheses)

# Step 3: Print results
divider = "=" * 60

print(divider)
print("GAP ANALYSIS")
print(divider)
print(gap_report)

print(divider)
print("HYPOTHESES")
print(divider)
print(hypotheses)

print(divider)
print("RANKED IDEAS")
print(divider)
print(rankings)

# Step 4: Save full report
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_path = f"data/full_report_{timestamp}.txt"

with open(report_path, "w", encoding="utf-8") as f:
    f.write("AI SCIENTIST — FULL RESEARCH REPORT\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(divider + "\n\n")

    f.write("PAPER SUMMARIES\n")
    f.write(divider + "\n\n")
    for name, summary in summaries:
        f.write(f"📄 {name}\n{summary}\n\n")

    f.write(divider + "\n\n")
    f.write("GAP ANALYSIS\n")
    f.write(divider + "\n\n")
    f.write(gap_report + "\n\n")

    f.write(divider + "\n\n")
    f.write("HYPOTHESES\n")
    f.write(divider + "\n\n")
    f.write(hypotheses + "\n\n")

    f.write(divider + "\n\n")
    f.write("RANKED IDEAS\n")
    f.write(divider + "\n\n")
    f.write(rankings + "\n\n")

print(f"\n💾 Full report saved to {report_path}")