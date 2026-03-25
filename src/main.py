from reader import extract_text_from_pdf, split_text
from embedder import get_embeddings
from retriever import create_index, search
from qa import generate_answer

pdf_path = "data/sample.pdf"

print("Reading PDF...")
text = extract_text_from_pdf(pdf_path)

chunks = split_text(text)

print("Creating embeddings...")
embeddings = get_embeddings(chunks)

index = create_index(embeddings)

question = input("Ask a Question: ")

query_embedding = get_embeddings([question])

indices = search(index, query_embedding)

context = " ".join([chunks[i] for i in indices])

answer = generate_answer(context, question)

print("\nAnswer:\n", answer)