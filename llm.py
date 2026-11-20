
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


# Retry configuration
MAX_RETRIES = 3

RETRYABLE_ERRORS = [429, 500, 502, 503, 504]


def generate_answer(
    prompt,
    temperature=0.2,
    max_output_tokens=1024
):
    """
    Generate an answer using Google Gemini
    with timeout and retry handling.
    """

    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=types.HttpOptions(
            timeout=30000
        )
    )

    try:

        for attempt in range(1, MAX_RETRIES + 1):

            try:

                print("\nConnecting to Gemini...")
                print("Model:", GEMINI_MODEL)
                print(
                    f"Attempt {attempt}/{MAX_RETRIES}"
                )

                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config={
                        "temperature": temperature,
                        "max_output_tokens": max_output_tokens
                    }
                )

                answer = response.text

                if not answer:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                print("\nGemini response generated successfully!")

                return answer.strip()

            except Exception as error:

                error_code = getattr(error, "code", None)

                error_status = getattr(
                    error,
                    "status",
                    None
                )

                if (
                    error_code in RETRYABLE_ERRORS
                    and attempt < MAX_RETRIES
                ):

                    wait_time = 2 ** attempt

                    print(
                        f"\nTemporary Gemini error: {error_code}"
                    )

                    print(
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                print("\nGemini request failed.")
                print("Error type:", type(error).__name__)
                print("Error code:", error_code)
                print("Error status:", error_status)

                raise RuntimeError(
                    "Gemini API request failed. "
                    "Check the error details above."
                ) from None

        raise RuntimeError(
            "Gemini request failed after all retry attempts."
        )

    finally:
        client.close()


# Test Gemini connection
if __name__ == "__main__":

    print("Testing Gemini API connection...")

    try:

        test_prompt = (
            "Reply with exactly this sentence: "
            "Gemini connection successful."
        )

        result = generate_answer(test_prompt)

        print("\nGemini Response:")
        print(result)

        print("\nGemini API test completed!")

    except Exception as error:

        print("\nGemini Test Failed:")
        print(error)
