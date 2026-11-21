
import os

from dotenv import load_dotenv
from google import genai


def main() -> None:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Check your local .env file."
        )

    client = genai.Client(api_key=api_key)

    print(f"Connecting to Gemini model: {model}")

    response = client.models.generate_content(
        model=model,
        contents=(
            "You are assisting an e-commerce catalogue manager. "
            "In two sentences, explain why accurate product listings "
            "matter to an online furniture retailer."
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty text response.")

    print("\nGemini response:")
    print(response.text)


if __name__ == "__main__":
    main()
