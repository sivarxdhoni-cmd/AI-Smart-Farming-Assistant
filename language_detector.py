
from langdetect import detect, DetectorFactory, LangDetectException

# Ensure consistent detection results
DetectorFactory.seed = 0

SUPPORTED_LANGUAGES = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "kn": "Kannada"
}


def detect_language(text):
    """
    Detects English, Tamil, Hindi and Kannada.
    """

    if not isinstance(text, str) or not text.strip():
        return "Unknown"

    try:
        detected_code = detect(text.strip())

        return SUPPORTED_LANGUAGES.get(
            detected_code, "Unsupported"
        )

    except LangDetectException:
        return "Unknown"


if __name__ == "__main__":

    test_questions = [
        "What are the major pests affecting rice?",
        "நெல் பயிரில் முக்கியமான பூச்சிகள் எவை?",
        "धान की फसल में प्रमुख कीट कौन से हैं?",
        "ಭತ್ತದ ಬೆಳೆಯಲ್ಲಿ ಪ್ರಮುಖ ಕೀಟಗಳು ಯಾವುವು?"
    ]

    for question in test_questions:
        print("Question:", question)
        print("Language:", detect_language(question))
        print("-" * 40)
