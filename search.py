
from embeddings import load_embedding_model
from vector_store import get_collection
from config import TOP_K


# Load embedding model once
embedding_model = None


def get_embedding_model():

    global embedding_model

    if embedding_model is None:
        print("Loading embedding model...")
        embedding_model = load_embedding_model()

    return embedding_model


def semantic_search(query, top_k=TOP_K):

    query = query.strip()

    if not query:
        print("Please enter a valid question.")
        return []

    if top_k < 1:
        print("top_k must be at least 1.")
        return []

    print("\nSearching agricultural knowledge base...")

    model = get_embedding_model()

    # Generate query embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    collection = get_collection()

    total_chunks = collection.count()

    if total_chunks == 0:
        print("Vector database is empty!")
        return []

    # Retrieve nearest chunks
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=min(top_k, total_chunks),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved_results = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances)
    ):

        # Calculate cosine similarity
        cosine_similarity = 1 - distance

        # Extract metadata
        source = metadata.get("source", "Unknown")
        page_number = metadata.get("page_number")
        chunk_index = metadata.get("chunk_index", -1)
        file_path = metadata.get("file_path", "Unknown")

        # Prepare result
        result = {
            "content": document,
            "source": source,
            "page_number": page_number,
            "chunk_index": chunk_index,
            "file_path": file_path,
            "cosine_similarity": cosine_similarity,
            "distance": distance
        }

        retrieved_results.append(result)

        # Display result
        print(f"\n{'=' * 50}")
        print(f"Result {i + 1}")
        print("=" * 50)

        print("Source:", source)

        if page_number is not None:
            print("PDF Page Number:", page_number)
        else:
            print("PDF Page Number: Not applicable")

        print("Chunk Index:", chunk_index)

        print(
            "Cosine Similarity:",
            round(cosine_similarity, 4)
        )

        print(
            "Cosine Distance:",
            round(distance, 4)
        )

        print("\nRetrieved Content:")
        print(document[:500])

    print("\nSearch completed.")
    print("Total results retrieved:", len(retrieved_results))

    return retrieved_results


if __name__ == "__main__":

    user_query = input(
        "\nEnter your farming question: "
    )

    if user_query.strip():
        semantic_search(user_query)

    else:
        print("Please enter a valid question.")
