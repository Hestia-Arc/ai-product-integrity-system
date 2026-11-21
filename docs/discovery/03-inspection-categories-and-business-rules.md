# Product Listing Integrity Monitor

## 03 — Inspection Categories and Business Rules

### 1. Purpose

Define the initial inspection categories, detection approaches, severity levels, and input/output expectations for Product Listing Integrity Monitor.

### 2. Initial Product Domain

The first prototype will focus on furniture and home décor products.

Examples include:

- Chairs and tables.
- Sofas and beds.
- Cabinets and shelves.
- Outdoor furniture.
- Decorative products.

This restriction provides a manageable domain for defining category-specific product attributes and evaluating inspection results.

### 3. Inspection Categories

#### 3.1 Contradiction Detection

Identify conflicting information across product listing fields.

Examples:

- Product title identifies an item as wooden while the description identifies it as plastic.
- Product description specifies one material while structured attributes specify another.
- Product dimensions conflict across different listing fields.

Primary approach: LLM-assisted semantic comparison, supported by deterministic validation where possible.

#### 3.2 Missing Information Detection

Identify absent product attributes that are required by the applicable product category.

Examples:

- Furniture product without required material information.
- Chair listing without required dimensions.
- Product category requiring assembly information where none is provided.

Primary approach: Deterministic validation against category-specific attribute requirements.

An optional field being empty must not automatically generate a finding.

#### 3.3 Unsupported Claim Detection

Identify product claims that are not sufficiently supported by the information supplied in the listing.

Examples:

- Sustainability claims without supporting evidence.
- Durability claims without supporting product information.
- Claims of special material properties without corresponding specifications.

Primary approach: LLM-assisted claim extraction and evidence comparison.

A finding means that the supplied listing does not establish the claim. It does not prove that the claim is false.

#### 3.4 Attribute and Value Validation

Identify invalid, malformed, or suspicious product attribute values.

Examples:

- Negative product weight.
- Invalid dimension formats.
- Empty required material values.
- Unsupported measurement units.

Primary approach: Python validation and deterministic business rules.

### 4. AI and Deterministic Processing Responsibilities

| Capability                       | Primary approach    |
| -------------------------------- | ------------------- |
| Attribute extraction             | LLM                 |
| Semantic contradiction detection | LLM with validation |
| Required attribute checking      | Python rules        |
| Unsupported claim identification | LLM                 |
| Numeric and format validation    | Python              |
| Initial severity assignment      | Python rules        |

The system must not rely on an LLM when a deterministic rule can provide a more predictable result.

### 5. Severity Classification

**High**

- Significant contradictions that may materially misrepresent a product.
- Invalid values that could materially affect customer understanding.

**Medium**

- Missing important required attributes.
- Claims requiring additional verification.

**Low**

- Minor information quality and formatting concerns.

Severity indicates inspection priority, not proven legal or commercial risk.

### 6. Initial Input Contract

The application accepts one product listing as a JSON object.

Expected fields:

- `product_id`: unique product identifier.
- `title`: product title.
- `description`: product description.
- `category`: product category.
- `attributes`: structured product attributes.

Example:

    {
      "product_id": "CHAIR-001",
      "title": "Outdoor Teak Garden Chair",
      "description": "A durable outdoor chair made from premium plastic.",
      "category": "outdoor_furniture",
      "attributes": {
        "material": "100% teak wood",
        "weight": "8 kg",
        "weather_resistant": true,
        "dimensions": {
          "width": "60 cm",
          "height": "85 cm",
          "depth": "55 cm"
        },
        "warranty": null
      }
    }

### 7. Inspection Output

The application should return:

- Product identifier.
- Overall inspection status.
- A list of findings.
- Finding category.
- Severity.
- Finding title.
- Explanation.
- Supporting evidence.
- Suggested action.

Each finding must reference the relevant product listing information.

The application must not invent evidence or present an unsupported conclusion as a verified fact.

### 8. Initial Business Rules

1. Product information must be validated before AI processing.
2. Required attributes must be determined by product category.
3. Optional missing attributes must not automatically generate findings.
4. Contradiction findings must identify the conflicting fields.
5. Unsupported claims must be presented as requiring verification.
6. Invalid numeric or structured values should be handled through deterministic validation.
7. Severity must follow defined rules rather than arbitrary model-generated ratings.
8. AI findings must include evidence from the supplied listing.
9. Ambiguous cases should be marked for human review rather than forced into a definite conclusion.
10. The application must not automatically modify or approve product listings.

### 9. Initial Prototype Boundaries

The prototype will support:

- Single-product JSON input.
- Furniture and home décor listings.
- Four inspection categories.
- Structured inspection results.
- Evidence-backed findings.
- Human review of findings.

It will not initially support:

- Image-based inspection.
- External factual verification.
- Supplier integrations.
- Automatic catalogue modification.
- Continuous catalogue monitoring.
- Automatic publication decisions.

### 10. Evaluation Considerations

Inspection quality will be evaluated using labelled examples containing:

- Correct and consistent listings.
- Contradictory listings.
- Missing required attributes.
- Unsupported claims.
- Invalid attribute values.
- Ambiguous listings.

Evaluation must measure both detection quality and the correctness of the evidence supporting each finding.
