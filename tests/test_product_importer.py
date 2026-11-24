
from product_integrity.importing.product_importer import (
    import_json,
    validate_products,
)

from product_integrity.importing.product_importer import (
    import_csv,
)


def test_import_json_single_product():
    content = """
    {
        "product_id": "CHAIR-001",
        "title": "Garden Chair",
        "description": "A teak garden chair.",
        "category": "outdoor_furniture",
        "attributes": {
            "material": "teak wood"
        }
    }
    """

    products, errors = import_json(content)

    assert len(products) == 1
    assert products[0]["product_id"] == "CHAIR-001"
    assert products[0]["attributes"]["material"] == "teak wood"
    assert errors == []


def test_reject_duplicate_product_ids():
    products = [
        {
            "product_id": "CHAIR-001",
            "title": "Garden Chair",
            "description": "A garden chair.",
            "category": "outdoor_furniture",
            "attributes": {},
        },
        {
            "product_id": "CHAIR-001",
            "title": "Another Chair",
            "description": "Another garden chair.",
            "category": "outdoor_furniture",
            "attributes": {},
        },
    ]

    valid, errors = validate_products(products)

    assert len(valid) == 1
    assert len(errors) == 1
    assert "Duplicate product ID" in errors[0]



def test_import_json_rejects_missing_required_fields():
    content = """
    {
        "product_id": "CHAIR-001",
        "description": "A garden chair.",
        "category": "outdoor_furniture",
        "attributes": {}
    }
    """

    products, errors = import_json(content)

    assert products == []
    assert any("'title' is required" in error for error in errors)


def test_import_json_keeps_valid_products_when_another_is_invalid():
    content = """
    {
        "products": [
            {
                "product_id": "CHAIR-001",
                "title": "Garden Chair",
                "description": "A teak chair.",
                "category": "outdoor_furniture",
                "attributes": {}
            },
            {
                "product_id": "CHAIR-002",
                "description": "A plastic chair.",
                "category": "outdoor_furniture",
                "attributes": {}
            }
        ]
    }
    """

    products, errors = import_json(content)

    assert len(products) == 1
    assert products[0]["product_id"] == "CHAIR-001"
    assert len(errors) == 1


def test_import_csv_products():
    content = """product_id,title,description,category,material,weight
CHAIR-001,Garden Chair,A teak chair.,outdoor_furniture,teak wood,8 kg
TABLE-001,Garden Table,A wooden table.,outdoor_furniture,oak wood,15 kg
"""

    products, errors = import_csv(content)

    assert len(products) == 2
    assert products[0]["attributes"]["material"] == "teak wood"
    assert products[1]["attributes"]["weight"] == "15 kg"
    assert errors == []


def test_import_csv_reports_invalid_attributes_json():
    content = """product_id,title,description,category,attributes
CHAIR-001,Garden Chair,A teak chair.,outdoor_furniture,"{invalid json}"
TABLE-001,Garden Table,A wooden table.,outdoor_furniture,"{""material"": ""oak""}"
"""

    products, errors = import_csv(content)

    assert len(products) == 1
    assert products[0]["product_id"] == "TABLE-001"
    assert len(errors) == 1
    assert "valid JSON" in errors[0]
