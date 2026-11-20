import argparse
from ingest import ingest_knowledge_base
from search import search_agriculture_knowledge, display_results

def run_test():
    query = "How can a farmer monitor crop pests before deciding on pest control?"
    results = search_agriculture_knowledge(query, k=3)
    display_results(query, results)
    if results:
        print("\\nTEST PASSED: ChromaDB returned relevant agriculture knowledge.")
    else:
        print("\\nTEST FAILED: No results. First run: python main.py ingest")

def main():
    parser = argparse.ArgumentParser(
        description="Multilingual Smart Farming RAG - vector database pipeline"
    )
    parser.add_argument("command", choices=["ingest", "search", "test"])
    args = parser.parse_args()

    if args.command == "ingest":
        ingest_knowledge_base()
    elif args.command == "search":
        question = input("Ask an agriculture question: ").strip()
        if question:
            display_results(question, search_agriculture_knowledge(question))
    elif args.command == "test":
        run_test()

if __name__ == "__main__":
    main()
