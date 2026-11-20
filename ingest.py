
from document_loader import load_documents
from chunking import chunk_documents
from embeddings import load_embedding_model, generate_embeddings
from vector_store import store_embeddings


def ingest_documents():

    print("\n===== AGRICULTURAL DATA INGESTION =====")

    # 1. Load documents
    documents = load_documents()

    if not documents:
        print("No documents found!")
        return

    # 2. Split documents into chunks
    chunks = chunk_documents(documents)

    if not chunks:
        print("No chunks generated!")
        return

    # 3. Load embedding model
    model = load_embedding_model()

    # 4. Extract chunk text
    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    # 5. Generate embeddings
    embeddings = generate_embeddings(model, texts)

    # 6. Store in ChromaDB
    collection = store_embeddings(
        chunks,
        embeddings
    )

    print("\n===== INGESTION COMPLETED =====")
    print("Documents loaded:", len(documents))
    print("Chunks generated:", len(chunks))
    print("Vectors stored:", collection.count())


if __name__ == "__main__":
    ingest_documents()
