
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

# Load embedding model
def load_embedding_model():

    print("Loading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL)

    print("Embedding model loaded successfully!")

    return model


# Generate embeddings for text chunks
def generate_embeddings(model, texts):

    print(f"Generating embeddings for {len(texts)} texts...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    print("Embeddings generated successfully!")
    print("Embedding shape:", embeddings.shape)

    return embeddings


# Test embedding generation
if __name__ == "__main__":

    model = load_embedding_model()

    sample_texts = [
        "How to control pests in tomato plants?",
        "How to improve soil fertility?",
        "What is the importance of irrigation?"
    ]

    vectors = generate_embeddings(model, sample_texts)

    print("\nNumber of vectors:", len(vectors))
    print("Vector dimensions:", vectors.shape[1])

    print("\nFirst vector preview:")
    print(vectors[0][:10])
