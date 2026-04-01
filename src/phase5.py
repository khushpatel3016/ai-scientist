import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(__file__))

from paper_writer import write_full_paper, format_paper

print("=" * 60)
print("AI SCIENTIST — PHASE 5: PAPER WRITER")
print("=" * 60)
print()

print("Choose input mode:")
print("  1 — Load from Phase 4 report file automatically")
print("  2 — Enter idea manually")
print()

mode = input("Enter 1 or 2: ").strip()

if mode == "1":
    reports_dir = "data"
    report_files = [
        f for f in os.listdir(reports_dir)
        if f.startswith("full_report_") and f.endswith(".txt")
    ]

    if not report_files:
        print("No Phase 4 report found in data/. Run phase4.py first.")
        sys.exit()

    latest = sorted(report_files)[-1]
    path = os.path.join(reports_dir, latest)
    print(f"Loading: {latest}\n")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = content.split("=" * 60)

    gap = ""
    hypothesis = ""
    rankings = ""

    for i, section in enumerate(sections):
        if "GAP ANALYSIS" in section and i + 1 < len(sections):
            gap = sections[i + 1].strip()[:1500]
        if "HYPOTHESES" in section and i + 1 < len(sections):
            hypothesis = sections[i + 1].strip()[:1500]
        if "RANKED IDEAS" in section and i + 1 < len(sections):
            rankings = sections[i + 1].strip()[:1000]

    if not gap or not hypothesis:
        print("Could not parse report properly. Switching to manual mode.")
        mode = "2"
    else:
        idea = hypothesis[:500]
        print("Parsed from Phase 4 report successfully.\n")

if mode == "2":
    print("Enter your research idea (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    idea = "\n".join(lines).strip()

    print("\nDescribe the research gap this addresses:")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    gap = "\n".join(lines).strip()

    print("\nMain hypothesis:")
    hypothesis = input().strip()

    print("\nAny rankings or scores (optional, press Enter to skip):")
    rankings = input().strip()

print("\n🔬 Writing your research paper...\n")

paper = write_full_paper(
    idea=idea,
    gap=gap,
    hypothesis=hypothesis,
    rankings=rankings
)

formatted = format_paper(paper)

print("\n" + formatted)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"data/research_paper_{timestamp}.txt"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(formatted)

print(f"\n💾 Paper saved to {output_path}")