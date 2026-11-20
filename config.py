from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "agriculture_knowledge"

CHUNK_SIZE = 800

CHUNK_OVERLAP = 150

TOP_K = 5

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

SUPPORTED_LANGUAGES = [
    "English",
    "Tamil",
    "Hindi",
    "Kannada"
]

DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)