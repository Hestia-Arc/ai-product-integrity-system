
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class ProductDimensions(BaseModel):
    width: str | None = Field(default=None, description="Product width as stated.")
    height: str | None = Field(default=None, description="Product height as stated.")
    depth: str | None = Field(default=None, description="Product depth as stated.")

class ProductExtraction(BaseModel):
    product_type: str = Field(
        description="The type of product identified in the listing."
    )

    description_materials: list[str] = Field(
        description="Materials explicitly mentioned in the product description."
    )

    attribute_materials: list[str] = Field(
        description="Materials explicitly specified in structured product attributes."
    )

    weight: str | None = Field(
        description="Product weight as stated, or null if not provided."
    )

    intended_use: str | None = Field(
        description="Intended use such as indoor, outdoor, or both, if stated."
    )

    description_weather_resistant: bool | None = Field(
    description="Weather resistance explicitly stated in the product description, or null if not stated."
    )

    attribute_weather_resistant: bool | None = Field(
    description="Weather resistance explicitly stated in the structured attributes, or null if not stated."
    )

    dimensions: ProductDimensions = Field(
    description="Product dimensions extracted from the listing."
    )

    other_claims: list[str] = Field(
        description="Other notable product claims explicitly stated in the listing."
    )

    unknown_or_missing: list[str] = Field(
        description="Relevant product information that cannot be determined from the listing."
    )


SAMPLE_PRODUCT = {
    "product_id": "CHAIR-001",
    "title": "Outdoor Teak Garden Chair",
    "description": (
        "A comfortable outdoor chair made from premium plastic. "
        "Designed for relaxing in your garden or on your patio."
    ),
    "category": "outdoor_furniture",
    "attributes": {
        "material": "100% teak wood",
        "weight": "8 kg",
        "weather_resistant": True,
        "dimensions": {
            "width": "60 cm",
            "height": "85 cm",
            "depth": "55 cm",
        },
        "warranty": None,
    },
}


EXTRACTION_PROMPT = """
You are a product catalogue data extraction system.

Extract product information using ONLY information explicitly stated
in the supplied product listing.

Rules:
- Do not invent, assume, or infer product attributes.
- Keep description materials separate from structured attribute materials.
- Extract weather resistance separately from the description and structured attributes.
- Preserve the source of each extracted value.
- Extract claims as stated without treating them as verified facts.
- If a value is unavailable in a source, return null for that field.
- Use empty lists or empty objects when no information is found.
- Identify relevant information that is missing or cannot be determined.
- Do not resolve contradictions between sources.
- Do not decide whether the listing is trustworthy.
"""


def main() -> None:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing.")

    prompt = (
        f"{EXTRACTION_PROMPT}\n\n"
        "Extract information from this product listing:\n"
        f"{json.dumps(SAMPLE_PRODUCT, indent=2)}"
    )

    with genai.Client(api_key=api_key) as client:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ProductExtraction,
            ),
        )

    if response.parsed is None:
        raise RuntimeError("Gemini returned no parsed structured output.")

    extraction = response.parsed

    print(f"Model: {model}")
    print("\nExtracted product information:\n")
    print(extraction.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
