
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing in .env")

client = Groq(api_key=GROQ_API_KEY)

try:
    print("Checking available Groq models...\n")

    models = client.models.list()

    for model in models.data:
        print("Model ID:", model.id)
        print("Active:", getattr(model, "active", "Unknown"))
        print("Context Window:", getattr(
            model, "context_window", "Unknown"
        ))
        print("-" * 50)

    print("\nModel listing completed!")

except Exception as error:
    print("Groq model listing failed!")
    print("Error:", type(error).__name__)
    print("Details:", str(error))

finally:
    client.close()
