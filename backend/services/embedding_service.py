from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle


# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Global memory store
vector_store = None
stored_chunks = []
FAISS_INDEX_FILE = "faiss_index.bin"
CHUNKS_FILE = "stored_chunks.pkl"

conversation_history = []

# Smart chunking
def split_into_chunks(text, chunk_size=500, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        chunk = text[start:start + chunk_size]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# Create embeddings (MULTI-PDF SAFE VERSION)
def create_embeddings(text):

    global vector_store
    global stored_chunks

    chunks = split_into_chunks(text)

    embeddings = model.encode(chunks)

    embeddings = np.array(embeddings)

    dimension = embeddings.shape[1]

    if vector_store is None:

        vector_store = faiss.IndexFlatL2(dimension)

    vector_store.add(embeddings)

    stored_chunks.extend(chunks)

    save_vector_store()

def save_vector_store():

    if vector_store is not None:

        faiss.write_index(vector_store, FAISS_INDEX_FILE)

        with open(CHUNKS_FILE, "wb") as f:

            pickle.dump(stored_chunks, f)

def load_vector_store():

    global vector_store
    global stored_chunks

    if os.path.exists(FAISS_INDEX_FILE):

        vector_store = faiss.read_index(FAISS_INDEX_FILE)

    if os.path.exists(CHUNKS_FILE):

        with open(CHUNKS_FILE, "rb") as f:

            stored_chunks = pickle.load(f)
# Semantic search
def search_similar_chunks(query):

    if vector_store is None:

        return [doc.page_content for doc in docs]


    query_embedding = model.encode([query])

    distances, indices = vector_store.search(
        np.array(query_embedding),
        k=3
    )

    return [stored_chunks[i] for i in indices[0]]

def update_conversation_history(question, answer):

    global conversation_history

    conversation_history.append({
        "question": question,
        "answer": answer
    })

    # keep last 5 exchanges only
    if len(conversation_history) > 5:

        conversation_history.pop(0)

def get_recent_context():

    context = ""

    for item in conversation_history:

        context += f"Q: {item['question']}\n"
        context += f"A: {item['answer']}\n"

    return context

def generate_answer_from_chunks(chunks):

    if not chunks:
        return "No relevant information found."

    # Combine top chunks intelligently
    combined_text = " ".join(chunks[:2])

    # Clean formatting
    combined_text = combined_text.replace("\n", " ").strip()

    # Limit length for readability
    return combined_text[:500]