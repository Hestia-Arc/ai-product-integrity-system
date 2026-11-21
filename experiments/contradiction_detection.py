
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


# 1. Define the structure of an individual contradiction finding.

class ContradictionFinding(BaseModel):
    field_name: str = Field(
        description="The product attribute where the contradiction was found."
    )
    source_a: str = Field(
        description="The first source containing the conflicting information."
    )
    value_a: str = Field(
        description="The exact value extracted from the first source."
    )
    source_b: str = Field(
        description="The second source containing the conflicting information."
    )
    value_b: str = Field(
        description="The exact value extracted from the second source."
    )
    explanation: str = Field(
        description="A concise explanation of why the two values conflict."
    )


# 2. Define the complete detection response.

class ContradictionDetectionResult(BaseModel):
    findings: list[ContradictionFinding] = Field(
        description="List of supported contradictions. Empty if none are found."
    )


# 3. Use the extraction result from our previous experiment.
# This is a temporary test fixture. We'll connect the experiments later.

EXTRACTED_PRODUCT = {
    "product_type": "Outdoor Teak Garden Chair",
    "description_materials": ["plastic"],
    "attribute_materials": ["100% teak wood"],
    "weight": "8 kg",
    "intended_use": "outdoor",
    "description_weather_resistant": None,
    "attribute_weather_resistant": True,
    "dimensions": {
        "width": "60 cm",
        "height": "85 cm",
        "depth": "55 cm",
    },
    "other_claims": [
        "comfortable outdoor chair",
        "Designed for relaxing in your garden or on your patio",
    ],
    "unknown_or_missing": ["warranty information"],
}


# 4. Tell the AI how to inspect the extracted information.

DETECTION_PROMPT = """
You are a product listing contradiction detection system.

Inspect the supplied extracted product information.

Your task is to identify contradictions between:
- Materials explicitly extracted from the product description.
- Materials explicitly extracted from structured product attributes.

Rules:
- Compare only information about the same product attribute.
- Identify a contradiction when the sources provide materially
  incompatible values.
- Preserve the exact values from both sources.
- Identify both sources clearly.
- Explain briefly why the values conflict.
- Do not decide which source is correct.
- Do not invent evidence.
- Do not treat missing information as a contradiction.
- If there is no supported contradiction, return an empty findings list.
- Do not assign severity or recommend automatic corrections.
"""


# 5. Send the extracted information to Gemini.

def main():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing from .env")

    prompt = (
        f"{DETECTION_PROMPT}\n\n"
        "Extracted product information:\n"
        f"{json.dumps(EXTRACTED_PRODUCT, indent=2)}"
    )

    with genai.Client(api_key=api_key) as client:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ContradictionDetectionResult,
            ),
        )

    if response.parsed is None:
        raise RuntimeError("Gemini returned no parsed contradiction findings.")

    result = response.parsed

    print(f"Model: {model}")
    print("\nContradiction detection results:\n")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
