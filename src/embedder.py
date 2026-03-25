from sentence_transformers import SentenceTranformer

model = SentenceTranformer('all_MiniLM-L6-v2')

def get_embeddings(text_chunks):
    return model.encode(text_chunks)