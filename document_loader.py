
from pathlib import Path
from pypdf import PdfReader

from config import DATA_DIR


# Basic crop identification keywords
CROP_KEYWORDS = {
    "rice": ["rice", "paddy", "oryza sativa"],
    "sugarcane": ["sugarcane", "saccharum officinarum"],
    "tomato": ["tomato", "solanum lycopersicum"],
    "maize": ["maize", "corn", "zea mays"],
    "cotton": ["cotton", "gossypium"],
    "banana": ["banana", "musa"],
    "groundnut": ["groundnut", "peanut"],
}


# Basic agricultural topic identification
CATEGORY_KEYWORDS = {
    "disease": [
        "disease", "fungus", "fungal", "bacterial",
        "virus", "symptoms", "infection", "blight",
        "rot", "rust", "wilt"
    ],
    "pest": [
        "pest", "insect", "larvae", "caterpillar",
        "borer", "aphid", "whitefly", "thrips"
    ],
    "irrigation": [
        "irrigation", "water management",
        "drip irrigation", "water requirement"
    ],
    "fertilizer": [
        "fertilizer", "fertiliser", "nitrogen",
        "phosphorus", "potassium", "NPK",
        "nutrient management"
    ],
    "weed_management": [
        "weed", "weeding", "herbicide",
        "weed management"
    ],
}


def detect_crop(text):

    text_lower = text.lower()

    matched_crops = []

    for crop, keywords in CROP_KEYWORDS.items():

        if any(keyword in text_lower for keyword in keywords):
            matched_crops.append(crop)

    if len(matched_crops) == 1:
        return matched_crops[0]

    return "multiple" if matched_crops else "unknown"


def detect_category(text):

    text_lower = text.lower()

    matched_categories = []

    for category, keywords in CATEGORY_KEYWORDS.items():

        if any(keyword in text_lower for keyword in keywords):
            matched_categories.append(category)

    if len(matched_categories) == 1:
        return matched_categories[0]

    return "multiple" if matched_categories else "general"


def detect_language(text):

    # Basic script-based language detection
    for character in text:

        if "\u0B80" <= character <= "\u0BFF":
            return "Tamil"

    return "English"


def create_metadata(file_path, text, page_number=None):

    metadata = {
        "source": file_path.name,
        "file_path": str(file_path),
        "file_type": file_path.suffix.lower(),
        "crop": detect_crop(text),
        "category": detect_category(text),
        "language": detect_language(text)
    }

    if page_number is not None:
        metadata["page_number"] = page_number

    return metadata


def load_documents():

    documents = []

    supported_extensions = [".txt", ".md", ".pdf"]

    for file_path in DATA_DIR.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in supported_extensions:
            continue

        # Source registry is metadata, not farming knowledge
        if file_path.name.upper() == "SOURCE_REGISTRY.MD":
            continue

        try:

            if file_path.suffix.lower() == ".pdf":

                reader = PdfReader(str(file_path))

                for page_number, page in enumerate(
                    reader.pages, start=1
                ):

                    text = page.extract_text() or ""

                    if not text.strip():
                        continue

                    documents.append({
                        "content": text,
                        "metadata": create_metadata(
                            file_path,
                            text,
                            page_number
                        )
                    })

                    print(
                        f"Loaded: {file_path.name} "
                        f"| Page: {page_number}"
                    )

            else:

                text = file_path.read_text(
                    encoding="utf-8"
                )

                if not text.strip():
                    continue

                documents.append({
                    "content": text,
                    "metadata": create_metadata(
                        file_path,
                        text
                    )
                })

                print(f"Loaded: {file_path.name}")

        except Exception as error:

            print(
                f"Error loading {file_path.name}: {error}"
            )

    print(
        f"\nTotal document records loaded: {len(documents)}"
    )

    return documents


if __name__ == "__main__":

    docs = load_documents()

    for doc in docs[:5]:

        print("\nSource:", doc["metadata"]["source"])
        print("Page:", doc["metadata"].get("page_number", "N/A"))
        print("Crop:", doc["metadata"]["crop"])
        print("Category:", doc["metadata"]["category"])
        print("Language:", doc["metadata"]["language"])
        print("Characters:", len(doc["content"]))
        print("Preview:", doc["content"][:200])
