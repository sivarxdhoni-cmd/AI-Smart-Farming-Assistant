
from config import CHUNK_SIZE, CHUNK_OVERLAP


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Split text into overlapping chunks.
    Prefer paragraph and word boundaries where possible.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("CHUNK_SIZE must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "CHUNK_OVERLAP must be between 0 and CHUNK_SIZE."
        )

    text = " ".join(text.split())

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + chunk_size, text_length)

        if end < text_length:
            boundary = text.rfind(" ", start, end)

            # Prefer a word boundary if it is reasonably close
            if boundary > start + chunk_size * 0.7:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        next_start = end - overlap

        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


def chunk_documents(documents):
    """
    Convert loaded documents into chunks.

    Input:
        [
            {
                "content": "...",
                "metadata": {...}
            }
        ]

    Output:
        [
            {
                "content": "...",
                "metadata": {...}
            }
        ]
    """

    chunked_documents = []

    if not documents:
        return chunked_documents

    for document_index, document in enumerate(documents):

        content = document.get("content", "")
        metadata = document.get("metadata", {})

        if not isinstance(content, str) or not content.strip():
            continue

        text_chunks = split_text(content)

        for chunk_index, chunk in enumerate(text_chunks):

            chunk_metadata = metadata.copy()

            chunk_metadata.update({
                "chunk_index": chunk_index,
                "chunk_size": len(chunk),
                "document_index": document_index
            })

            chunked_documents.append({
                "content": chunk,
                "metadata": chunk_metadata
            })

    print("\nChunking completed!")
    print("Original documents:", len(documents))
    print("Generated chunks:", len(chunked_documents))

    return chunked_documents


if __name__ == "__main__":

    sample_text = """
    Rice is an important cereal crop.
    It requires suitable soil and water management.

    Several pests affect rice production.
    Farmers should monitor crops regularly.
    """

    chunks = split_text(sample_text)

    for index, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {index}:")
        print(chunk)
