# Product Listing Integrity Monitor

## 04 — Functional and Non-Functional Requirements

### 1. Purpose

Define the functional and non-functional requirements for the initial Product Listing Integrity Monitor prototype.

### 2. Prototype Scope

The prototype will inspect individual product listings supplied as JSON.

The initial supported domain is furniture and home décor, including indoor and outdoor products.

The system will identify potential listing integrity issues and produce evidence-backed inspection findings for human review.

### 3. Functional Requirements

| ID    | Requirement                                                                                |
| ----- | ------------------------------------------------------------------------------------------ |
| FR-01 | The application must accept one product listing as a JSON object.                          |
| FR-02 | The application must validate required fields and data types before inspection.            |
| FR-03 | The application must support furniture and home décor product categories.                  |
| FR-04 | The system must extract relevant product attributes from listing information.              |
| FR-05 | The system must identify contradictions between related product fields.                    |
| FR-06 | The system must detect missing category-required attributes.                               |
| FR-07 | The system must identify claims requiring additional verification.                         |
| FR-08 | The system must validate structured attribute values using deterministic rules.            |
| FR-09 | The system must generate evidence-backed inspection findings.                              |
| FR-10 | Each finding must have a category, severity, explanation, and suggested action.            |
| FR-11 | The application must return a structured inspection report.                                |
| FR-12 | The application must handle ambiguous information without forcing unsupported conclusions. |
| FR-13 | Users must be able to review and dismiss findings through the interface.                   |
| FR-14 | The application must support configurable local and hosted model providers.                |

### 4. Non-Functional Requirements

**Reliability**

- Invalid input must be rejected gracefully.
- AI provider failures must be handled without crashing the application.
- The application must validate model responses before using them.

**Explainability**

- Findings must identify the product information that supports them.
- The system must distinguish observed contradictions from claims requiring verification.

**Consistency**

- Deterministic validation rules must produce predictable results.
- Severity assignment must follow defined business rules.

**Maintainability**

- AI integration, inspection logic, API, and interface must have clearly defined responsibilities.
- New inspection categories should be addable without rewriting the entire application.

**Portability**

- The application should be designed for eventual Docker containerization.
- Application configuration must be externalized.

**Testability**

- Business rules must have automated tests.
- API behaviour must have automated tests.
- AI outputs must be evaluated separately against labelled examples.

**Security**

- API keys and credentials must not be committed to source control.
- External model calls must use configured credentials.
- Only necessary product information should be sent to external model providers.

### 5. Evaluation Dataset

The initial evaluation dataset will contain approximately 40 labelled product listings.

| Dataset group                   | Target examples |
| ------------------------------- | --------------: |
| Correct and consistent listings |              10 |
| Contradictory listings          |              10 |
| Missing required attributes     |               5 |
| Unsupported claims              |               5 |
| Invalid attribute values        |               5 |
| Ambiguous listings              |               5 |
| **Total**                       |          **40** |

Each evaluation example should include:

- Input product listing.
- Expected inspection category.
- Expected findings.
- Expected severity where applicable.
- Supporting evidence.
- Expected handling of ambiguity.

### 6. Evaluation Metrics

**Precision:** Proportion of reported findings that are valid.

**Recall:** Proportion of known issues that the system successfully detects.

**False positive rate:** Frequency of incorrect issue reports.

**Evidence correctness:** Whether the evidence supports the reported finding.

**Structured-output validity:** Whether inspection responses conform to the defined schema.

The initial evaluation will establish a baseline. Performance targets will be refined using actual results.

### 7. Acceptance Criteria

The prototype will be considered functionally successful when:

1. Valid product JSON is accepted.
2. Invalid JSON or invalid product structures are rejected with useful errors.
3. Supported furniture and home décor listings can be inspected.
4. The system supports all four defined inspection categories.
5. Findings include relevant evidence.
6. Ambiguous cases can be flagged for human review.
7. Inspection reports conform to the response schema.
8. Deterministic business rules are independently testable.
9. At least one model provider can successfully perform the required AI tasks.
10. A user can complete an inspection through the prototype interface.

### 8. Quality Expectations

A successful demonstration must show more than an AI-generated description.

It should demonstrate:

- Correct identification of an intentional contradiction.
- Detection of a missing required attribute.
- Identification of a claim requiring verification.
- Rejection or handling of invalid structured values.
- Correct handling of a consistent product listing.
- Evidence supporting each reported issue.

### 9. Known Limitations

The initial prototype will not:

- Establish the physical truth of product claims.
- Guarantee that every product inconsistency is detected.
- Replace human catalogue review.
- Automatically correct or publish product listings.
- Guarantee production-level accuracy or availability.

The prototype is intended to validate the technical and product feasibility of AI-assisted product listing inspection.
