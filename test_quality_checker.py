
from quality_checker import check_retrieval_quality

results = [
    {
        "content": "Rice requires sufficient water during its growth.",
        "distance": 0.25,
        "metadata": {
            "source": "TNAU.pdf",
            "page_number": 10,
            "chunk_index": 0
        }
    },
    {
        "content": "Rice requires sufficient water during its growth.",
        "distance": 0.25,
        "metadata": {
            "source": "TNAU.pdf",
            "page_number": 10,
            "chunk_index": 0
        }
    },
    {
        "content": "Sugarcane requires proper irrigation.",
        "distance": 0.30,
        "metadata": {
            "source": "TNAU.pdf",
            "page_number": 11,
            "chunk_index": 1
        }
    }
]

result = check_retrieval_quality(results)

print("Duplicate test result:")
print(result)
