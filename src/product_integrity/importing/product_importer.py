
import csv
import io
import json
from typing import Any


REQUIRED_FIELDS = {
    "product_id",
    "title",
    "description",
    "category",
}


class ProductImportError(Exception):
    """Raised when an uploaded catalogue cannot be parsed."""


def validate_product(
    product: Any,
    row_number: int,
) -> tuple[dict | None, list[str]]:
    """Validate one product record."""

    if not isinstance(product, dict):
        return None, [f"Record {row_number}: Product must be a JSON object."]

    errors = []

    for field in REQUIRED_FIELDS:
        value = product.get(field)

        if not isinstance(value, str) or not value.strip():
            errors.append(
                f"Record {row_number}: '{field}' is required and must be text."
            )

    attributes = product.get("attributes", {})

    if not isinstance(attributes, dict):
        errors.append(
            f"Record {row_number}: 'attributes' must be an object."
        )

    if errors:
        return None, errors

    normalized_product = {
        "product_id": product["product_id"].strip(),
        "title": product["title"].strip(),
        "description": product["description"].strip(),
        "category": product["category"].strip(),
        "attributes": attributes,
    }

    return normalized_product, []


def normalize_csv_row(row: dict) -> dict:
    """Convert a flat CSV row into our standard product structure."""

    attributes = {}

    for key, value in row.items():
        if key in REQUIRED_FIELDS:
            continue

        if key == "attributes":
            if value:
                try:
                    parsed_attributes = json.loads(value)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        "CSV 'attributes' column must contain valid JSON."
                    ) from exc

                if not isinstance(parsed_attributes, dict):
                    raise ValueError(
                        "CSV 'attributes' must contain a JSON object."
                    )

                attributes.update(parsed_attributes)

        elif value is not None and value.strip():
            attributes[key] = value.strip()

    return {
        "product_id": row.get("product_id"),
        "title": row.get("title"),
        "description": row.get("description"),
        "category": row.get("category"),
        "attributes": attributes,
    }


def import_json(content: str) -> tuple[list[dict], list[str]]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ProductImportError(
            f"Invalid JSON file: {exc.msg} at line {exc.lineno}."
        ) from exc

    if isinstance(data, dict) and "products" in data:
        products = data["products"]
    elif isinstance(data, list):
        products = data
    elif isinstance(data, dict):
        products = [data]
    else:
        raise ProductImportError(
            "JSON must contain a product object or a list of products."
        )

    if not isinstance(products, list):
        raise ProductImportError(
            "The 'products' field must contain a list."
        )

    return validate_products(products)


def import_csv(content: str) -> tuple[list[dict], list[str]]:
    try:
        reader = csv.DictReader(io.StringIO(content))

        if not reader.fieldnames:
            raise ProductImportError("CSV file has no header row.")

        missing_columns = REQUIRED_FIELDS - set(reader.fieldnames)

        if missing_columns:
            raise ProductImportError(
                "CSV is missing required columns: "
                + ", ".join(sorted(missing_columns))
            )

        products = []
        errors = []

        for row_number, row in enumerate(reader, start=2):
            try:
                products.append(normalize_csv_row(row))
            except ValueError as exc:
                errors.append(f"Row {row_number}: {exc}")

        valid_products, validation_errors = validate_products(products)

        return valid_products, errors + validation_errors

    except csv.Error as exc:
        raise ProductImportError(
            f"Unable to read CSV file: {exc}"
        ) from exc


def validate_products(
    products: list,
) -> tuple[list[dict], list[str]]:
    valid_products = []
    errors = []
    seen_ids = set()

    for index, product in enumerate(products, start=1):
        normalized, product_errors = validate_product(product, index)

        if product_errors:
            errors.extend(product_errors)
            continue

        product_id = normalized["product_id"]

        if product_id in seen_ids:
            errors.append(
                f"Record {index}: Duplicate product ID '{product_id}'."
            )
            continue

        seen_ids.add(product_id)
        valid_products.append(normalized)

    return valid_products, errors
