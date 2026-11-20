
from search import semantic_search
from quality_checker import check_retrieval_quality
from groq_llm import generate_answer
from language_detector import detect_language


MAX_DISTANCE = 0.75


def build_context(results):

    context_parts = []
    sources = []
    page_numbers = []

    seen_sources = set()
    seen_pages = set()

    for item in results:

        source = item.get("source", "Unknown")
        page = item.get("page_number")
        content = item.get("content", "")

        page_label = page if page is not None else "Not available"

        context_parts.append(
            f"""
Source: {source}
PDF Page: {page_label}

Content:
{content}
"""
        )

        if source not in seen_sources:
            sources.append({
                "source": source,
                "pages": []
            })
            seen_sources.add(source)

        source_entry = next(
            s for s in sources
            if s["source"] == source
        )

        if page is not None and page not in source_entry["pages"]:
            source_entry["pages"].append(page)

        if page is not None and page not in seen_pages:
            page_numbers.append(page)
            seen_pages.add(page)

    return "\n".join(context_parts), sources, page_numbers


def insufficient_evidence(question, quality=None):

    language = detect_language(question)

    messages = {
        "English": (
            "Sorry, the available agricultural knowledge base "
            "does not contain sufficient verified information "
            "to answer this question reliably."
        ),
        "Tamil": (
            "மன்னிக்கவும், இந்தக் கேள்விக்கு நம்பகமாகப் பதிலளிக்க "
            "தேவையான சரிபார்க்கப்பட்ட விவசாயத் தகவல்கள் "
            "தற்போதைய தரவுத்தளத்தில் இல்லை."
        ),
        "Hindi": (
            "क्षमा करें, इस प्रश्न का विश्वसनीय उत्तर देने के लिए "
            "उपलब्ध कृषि ज्ञान आधार में पर्याप्त सत्यापित जानकारी नहीं है।"
        ),
        "Kannada": (
            "ಕ್ಷಮಿಸಿ, ಈ ಪ್ರಶ್ನೆಗೆ ವಿಶ್ವಾಸಾರ್ಹವಾಗಿ ಉತ್ತರಿಸಲು "
            "ಲಭ್ಯವಿರುವ ಕೃಷಿ ಜ್ಞಾನದಲ್ಲಿ ಸಾಕಷ್ಟು ಪರಿಶೀಲಿತ ಮಾಹಿತಿ ಇಲ್ಲ."
        )
    }

    return {
        "status": "INSUFFICIENT_EVIDENCE",
        "question": question,
        "detected_language": language,
        "answer": messages.get(
            language,
            messages["English"]
        ),
        "sources": [],
        "page_numbers": [],
        "retrieval_info": {
            "quality": quality
        }
    }


def rag_pipeline(question, top_k=5):

    if not isinstance(question, str) or not question.strip():
        return {
            "status": "INVALID_QUESTION",
            "question": question,
            "answer": "Please enter a valid question.",
            "sources": [],
            "page_numbers": [],
            "retrieval_info": {}
        }

    question = question.strip()

    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
        return {
            "status": "INVALID_INPUT",
            "question": question,
            "answer": "top_k must be a positive integer.",
            "sources": [],
            "page_numbers": [],
            "retrieval_info": {}
        }

    # 1. Detect question language
    detected_language = detect_language(question)

    print("Detected language:", detected_language)

    # 2. Retrieve documents
    try:
        search_results = semantic_search(
            question,
            top_k=top_k
        )

    except Exception as error:
        print("Retrieval error:", type(error).__name__)

        return {
            "status": "RETRIEVAL_ERROR",
            "question": question,
            "detected_language": detected_language,
            "answer": "Unable to retrieve agricultural information.",
            "sources": [],
            "page_numbers": [],
            "retrieval_info": {}
        }

    if not search_results:
        return insufficient_evidence(question)

    # 3. Quality check
    checker_input = []

    for item in search_results:
        checker_input.append({
            "content": item.get("content", ""),
            "distance": item.get("distance"),
            "metadata": {
                "source": item.get("source"),
                "page_number": item.get("page_number"),
                "chunk_index": item.get("chunk_index"),
                "language": item.get("language", "Unknown"),
                "category": item.get("category", "Unknown")
            }
        })

    try:
        quality = check_retrieval_quality(
            checker_input,
            max_distance=MAX_DISTANCE
        )

    except Exception as error:
        print("Quality checker error:", type(error).__name__)

        return {
            "status": "QUALITY_CHECK_ERROR",
            "question": question,
            "detected_language": detected_language,
            "answer": "Unable to verify retrieved information.",
            "sources": [],
            "page_numbers": [],
            "retrieval_info": {}
        }

    # 4. Accept structurally valid results
    checked_results = quality.get("results", [])

    accepted_ranks = {
        item["rank"]
        for item in checked_results
        if item["has_content"]
        and item["has_source"]
        and item["similarity"] is not None
        and item["distance"] <= MAX_DISTANCE
        and not item["warnings"]
    }

    relevant_results = [
        item
        for index, item in enumerate(search_results, start=1)
        if index in accepted_ranks
    ]

    if not relevant_results:
        return insufficient_evidence(question, quality)

    # 5. Build context
    context, sources, page_numbers = build_context(
        relevant_results
    )

    # 6. Multilingual prompt
    prompt = f"""
You are an AI Smart Farming Assistant.

DETECTED QUESTION LANGUAGE: {detected_language}

Answer the farmer in {detected_language}.

RULES:
1. Use ONLY the supplied agricultural context.
2. Answer in the detected language.
3. Never invent agricultural facts.
4. Never invent pesticide dosages or chemical instructions.
5. If evidence is insufficient, clearly state that.
6. Do not use outside knowledge.
7. Give simple, farmer-friendly explanations.
8. Preserve important agricultural technical terms where necessary.
9. Never invent sources or page numbers.

AGRICULTURAL CONTEXT:
{context}

FARMER'S QUESTION:
{question}

Provide the answer in {detected_language}:
"""

    # 7. Generate answer
    try:
        answer = generate_answer(prompt)

        if not isinstance(answer, str) or not answer.strip():
            return {
                "status": "GENERATION_ERROR",
                "question": question,
                "detected_language": detected_language,
                "answer": "The AI could not generate a valid answer.",
                "sources": sources,
                "page_numbers": page_numbers,
                "retrieval_info": {
                    "quality": quality
                }
            }

    except Exception as error:
        print("Groq generation error:", type(error).__name__)

        return {
            "status": "GENERATION_ERROR",
            "question": question,
            "detected_language": detected_language,
            "answer": "Unable to generate an answer right now.",
            "sources": sources,
            "page_numbers": page_numbers,
            "retrieval_info": {
                "quality": quality
            }
        }

    # 8. Structured response
    return {
        "status": "SUCCESS",
        "question": question,
        "detected_language": detected_language,
        "answer": answer.strip(),
        "sources": sources,
        "page_numbers": page_numbers,
        "retrieval_info": {
            "total_retrieved": len(search_results),
            "accepted_results": len(relevant_results),
            "quality_status": quality["status"],
            "quality_warnings": quality["warnings"]
        }
    }
