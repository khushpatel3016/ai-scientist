import faiss
import numpy as np

def create_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index

def search(index, query_embedding, k = 3):
    distances, indices = index.search(query_embedding, k)
    return indices[0]