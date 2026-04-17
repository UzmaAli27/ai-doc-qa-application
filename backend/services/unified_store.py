
from services.vector_store import add_documents_to_vector_store

UNIFIED_STORE = []


def add_to_unified_store(doc):

    UNIFIED_STORE.append(doc)

    add_documents_to_vector_store([doc])