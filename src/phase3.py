import os
import sys
sys.path.append(os.path.dirname(__file__))

from reader import extract_text_from_pdf, split_text
from gap_finder import summarize_paper, find_gaps

papers_dir = "data/papers"

pdf_files = [
    f for f in os.listdir(papers_dir)
    if f.endswith(".pdf")
]

if len(pdf_files) < 2:
    print("❌ Add at least 2 PDF papers inside data/papers/")
    sys.exit()

print(f"📚 Found {len(pdf_files)} papers\n")

summaries = []

for pdf_file in pdf_files:
    path = os.path.join(papers_dir, pdf_file)
    print(f"📄 Reading: {pdf_file}")

    text = extract_text_from_pdf(path)
    chunks = split_text(text)

    print(f"   Summarizing...")
    summary = summarize_paper(chunks)
    summaries.append(summary)

    print(f"   ✅ Done\n")

print("🔍 Analyzing gaps across all papers...\n")
print("=" * 60)

gaps = find_gaps(summaries)
print(gaps)

print("=" * 60)

output_path = "data/gap_report.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("RESEARCH GAP ANALYSIS REPORT\n")
    f.write("=" * 60 + "\n\n")
    for i, s in enumerate(summaries):
        f.write(f"Paper {i+1} Summary:\n{s}\n\n")
    f.write("=" * 60 + "\n\n")
    f.write("GAP ANALYSIS:\n\n")
    f.write(gaps)

print(f"\n💾 Report saved to {output_path}")