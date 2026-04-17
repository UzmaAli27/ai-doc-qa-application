from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Global FAISS index + storage
index = None
documents = []


def add_documents_to_vector_store(new_docs):
    global index
    global documents

    texts = [doc["content"] for doc in new_docs]

    if not texts:
        return

    embeddings = model.encode(texts)

    if index is None:
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    documents.extend(new_docs)


def semantic_search(query, top_k=5):
    global index
    global documents

    if index is None:
        return []

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])

    return results