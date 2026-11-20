
def check_retrieval_quality(results, max_distance=0.75):
    """
    Checks retrieval output for basic quality issues.
    This is a heuristic checker, not a factual verification system.
    """

    if not results:
        return {
            "status": "NO_RESULTS",
            "message": "No documents were retrieved.",
            "total_results": 0,
            "valid_results": 0,
            "warnings": [],
            "results": []
        }

    checked_results = []
    warnings = []
    seen_chunks = set()

    for index, item in enumerate(results, start=1):

        metadata = item.get("metadata") or {}
        content = item.get("content") or ""
        distance = item.get("distance")

        source = metadata.get("source")
        page_number = metadata.get("page_number")
        chunk_index = metadata.get("chunk_index")

        result_warnings = []
        similarity = None

        # Check empty content
        if not content.strip():
            result_warnings.append("EMPTY_CONTENT")

        # Check missing source
        if not source:
            result_warnings.append("MISSING_SOURCE")

        # Check distance
        if (
            not isinstance(distance, (int, float))
            or isinstance(distance, bool)
            or not 0 <= distance <= 2
        ):
            result_warnings.append("INVALID_DISTANCE")

        else:
            similarity = 1 - distance

            if distance > max_distance:
                result_warnings.append("LOW_SIMILARITY")

        # Check duplicate chunks using page number
        if source and chunk_index is not None:

            if page_number is not None:
                chunk_key = (
                    source,
                    page_number,
                    chunk_index
                )
            else:
                chunk_key = (
                    source,
                    chunk_index,
                    content.strip()
                )

            if chunk_key in seen_chunks:
                result_warnings.append("DUPLICATE_CHUNK")
            else:
                seen_chunks.add(chunk_key)

        checked_results.append({
            "rank": index,
            "content": content,
            "distance": distance,
            "similarity": (
                round(similarity, 4)
                if similarity is not None
                else None
            ),
            "source": source or "Unknown",
            "page_number": page_number,
            "chunk_index": chunk_index,
            "language": metadata.get("language", "Unknown"),
            "category": metadata.get("category", "Unknown"),
            "has_content": bool(content.strip()),
            "has_source": bool(source),
            "warnings": result_warnings
        })

    valid_results = [
    item for item in checked_results
    if item["has_content"]
    and item["has_source"]
    and item["similarity"] is not None
]
    

    for item in checked_results:
        for warning in item["warnings"]:
            warnings.append(
                f"Result {item['rank']}: {warning}"
            )

    if not valid_results:
        status = "LOW_QUALITY"
        message = "No results passed the basic quality checks."

    elif warnings:
        status = "REVIEW_REQUIRED"
        message = (
            "Some retrieval quality issues were detected. "
            "Review the warnings before using these results."
        )

    else:
        status = "BASIC_CHECKS_PASSED"
        message = (
            "Basic structural checks passed. "
            "Relevance and factual accuracy still require review."
        )

    return {
        "status": status,
        "message": message,
        "total_results": len(checked_results),
        "valid_results": len(valid_results),
        "warnings": warnings,
        "results": checked_results
    }
