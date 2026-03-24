from reader import extract_text_from_pdf
from summarizer import summarize_text

pdf_path = "data/sample.pdf"

print("Reading PDF...")
text = extract_text_from_pdf(pdf_path)

print("Summarizing...")
summary = summarize_text(text)

print("\n--- FINAL SUMMARY ---\n")
print(summary)