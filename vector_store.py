
import chromadb
import hashlib

from config import CHROMA_DB_DIR, COLLECTION_NAME


# Initialize persistent ChromaDB
client = chromadb.PersistentClient(
    path=str(CHROMA_DB_DIR)
)


def get_collection():

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    print("ChromaDB collection ready!")

    return collection


def generate_chunk_id(chunk):

    metadata = chunk.get("metadata", {})

    source = metadata.get("source", "unknown")
    page_number = metadata.get("page_number", 0)
    chunk_index = metadata.get("chunk_index", 0)

    unique_text = (
        f"{source}_{page_number}_{chunk_index}_"
        f"{chunk['content']}"
    )

    return hashlib.sha256(
        unique_text.encode("utf-8")
    ).hexdigest()


def store_embeddings(chunks, embeddings):

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match!"
        )

    if not chunks:
        print("No chunks available to store.")
        return get_collection()

    collection = get_collection()

    ids = [
        generate_chunk_id(chunk)
        for chunk in chunks
    ]

    documents = [
        chunk["content"]
        for chunk in chunks
    ]

    metadatas = [
        chunk["metadata"]
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print("Embeddings stored successfully!")
    print("New chunks processed:", len(chunks))
    print("Total stored chunks:", collection.count())

    return collection


if __name__ == "__main__":

    collection = get_collection()

    print("\nCollection name:", collection.name)
    print("Collection metadata:", collection.metadata)

    print(
        "Current document count:",
        collection.count()
    )

    stored_data = collection.get(
        include=["documents", "metadatas"]
    )

    print("\nStored records:")

    for i, metadata in enumerate(stored_data["metadatas"]):

        print(f"\nRecord {i + 1}")

        print("ID:", stored_data["ids"][i])

        print("Source:", metadata.get("source"))

        print("Page number:", metadata.get("page_number"))

        print("Chunk index:", metadata.get("chunk_index"))

        print(
            "Content:",
            stored_data["documents"][i][:150]
        )
