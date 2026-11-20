
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "qwen/qwen3.8-27b"
)


def generate_answer(prompt):

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing!")

    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt cannot be empty!")

    client = Groq(api_key=GROQ_API_KEY)

    try:
        print("Connecting to Groq...")
        print("Model:", GROQ_MODEL)

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content

        if not answer or not answer.strip():
            raise RuntimeError("Empty response received!")

        print("Groq response generated successfully!")

        return answer.strip()

    finally:
        client.close()


def generate_structured_answer(prompt):

    """
    Generates a structured JSON response.

    Expected response:
    {
        "status": "ANSWERED" or "INSUFFICIENT_EVIDENCE",
        "answer": "Generated answer"
    }
    """

    structured_prompt = f"""
{prompt}

IMPORTANT OUTPUT REQUIREMENTS:

Return ONLY valid JSON.

If the supplied context contains sufficient evidence:
{{
    "status": "ANSWERED",
    "answer": "Your answer here"
}}

If the supplied context does not contain sufficient evidence:
{{
    "status": "INSUFFICIENT_EVIDENCE",
    "answer": "Explain that verified information is insufficient."
}}

Do not invent agricultural facts.
Do not include Markdown code fences.
"""

    raw_response = generate_answer(structured_prompt)

    try:
        result = json.loads(raw_response)

    except json.JSONDecodeError as error:
        raise ValueError(
            "LLM returned invalid JSON response."
        ) from error

    status = result.get("status")
    answer = result.get("answer")

    if status not in [
        "ANSWERED",
        "INSUFFICIENT_EVIDENCE"
    ]:
        raise ValueError("Invalid LLM response status.")

    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("Invalid or empty LLM answer.")

    return {
        "status": status,
        "answer": answer.strip()
    }


# Test connection
if __name__ == "__main__":

    print("Testing Groq API connection...")

    try:
        result = generate_answer(
            "Reply with exactly this sentence: "
            "Groq connection successful."
        )

        print("\nGroq Response:")
        print(result)

    except Exception as error:
        print("\nGroq Test Failed!")
        print("Error:", type(error).__name__)
        print("Details:", str(error))
