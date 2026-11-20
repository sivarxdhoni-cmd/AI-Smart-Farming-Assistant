
import json

from search import semantic_search
from quality_checker import check_retrieval_quality


def run_evaluation():

    # Load test questions
    with open("test_queries.json", "r", encoding="utf-8") as file:
        test_queries = json.load(file)

    print("\n" + "=" * 60)
    print("SMART FARMING RAG - EVALUATION")
    print("=" * 60)

    for test in test_queries:

        query = test["query"]

        print("\n" + "=" * 60)
        print("TEST ID:", test["id"])
        print("QUERY:", query)
        print("EXPECTED CATEGORY:", test["expected_category"])
        print("EXPECTED CROP:", test["expected_crop"])
        print("=" * 60)

        # Retrieve documents using semantic_search()
        results = semantic_search(query, top_k=5)

        # Convert results into quality_checker format
        normalized_results = []

        for result in results:

            normalized_results.append({
                "content": result.get("content", ""),
                "distance": result.get("distance"),
                "metadata": {
                    "source": result.get("source"),
                    "chunk_index": result.get("chunk_index"),
                    "category": "Unknown",
                    "language": "Unknown"
                }
            })

        # Check retrieval quality
        quality = check_retrieval_quality(normalized_results)

        print("\nQUALITY CHECK")
        print("STATUS:", quality["status"])
        print("MESSAGE:", quality["message"])
        print("TOTAL RESULTS:", quality["total_results"])
        print("VALID RESULTS:", quality["valid_results"])

        print("\nRETRIEVAL DETAILS")

        for result in quality["results"]:

            print("-" * 40)
            print("Rank:", result["rank"])
            print("Source:", result["source"])
            print("Chunk index:", result["chunk_index"])
            print("Similarity:", result["similarity"])
            print("Distance:", result["distance"])
            print("Warnings:", result["warnings"])

        if quality["warnings"]:
            print("\nQUALITY WARNINGS")

            for warning in quality["warnings"]:
                print(warning)

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    run_evaluation()
