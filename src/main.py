from reader import extract_text_from_pdf
from summarizer import summarize_text

pdf_path = "data.sample/pdf"

text = extract_text_from_pdf(pdf_path)
summary = summarize_text(text)

print("\n--- SUMMARY ---\n")
print(summary)