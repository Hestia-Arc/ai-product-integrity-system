# Product Listing Integrity Monitor

## 02 — Stakeholders and Workflow Analysis

### 1. Purpose

This document identifies the stakeholders involved in product catalogue quality management, examines the current product information inspection workflow, and establishes how Product Listing Integrity Monitor fits into that workflow.

### 2. Stakeholders

#### 2.1 Primary Stakeholder: Catalogue Manager

**Responsibilities**

- Maintain product catalogue quality.
- Review new and existing product listings.
- Identify incomplete or inconsistent information.
- Coordinate corrections with internal teams and suppliers.
- Determine whether listings are ready for publication.

**Needs**

- Efficient product information inspection.
- Clear identification of potential issues.
- Evidence supporting detected findings.
- Prioritization of issues requiring attention.
- Recommendations for resolving issues.

#### 2.2 Supporting Stakeholders

**Catalogue and Content Team**

- Creates and updates product listings.
- Transforms supplier information into catalogue content.
- Corrects identified listing problems.

**Suppliers**

- Provide product information and specifications.
- Clarify questionable or conflicting product details.
- Supply missing information when requested.

**E-commerce Operations Manager**

- Oversees catalogue quality processes.
- Monitors operational efficiency.
- Establishes product information quality expectations.

**Customers**

- Depend on accurate and complete product information when evaluating products and purchasing.

### 3. Current Business Workflow

The assumed current workflow is:

1. Receive product information from suppliers or other sources.
2. Create or update product listings.
3. Manually inspect product titles, descriptions, and specifications.
4. Identify missing or contradictory information.
5. Investigate questionable details with suppliers or internal teams.
6. Correct product information.
7. Publish or update the product listing.

### 4. Identified Workflow Challenges

Potential challenges include:

- Incomplete supplier information.
- Inconsistent product attributes.
- Contradictions between descriptions and specifications.
- Human errors during data entry and copying.
- Time-consuming manual inspection.
- Difficulty identifying the exact source of an inconsistency.
- Delays caused by supplier clarification.

These challenges are initial discovery assumptions requiring validation with real users.

### 5. Proposed Future Workflow

Product Listing Integrity Monitor supports the existing catalogue management workflow:

1. Catalogue manager submits product information.
2. Application extracts relevant product attributes.
3. Inspection engine evaluates product information.
4. Application generates structured findings.
5. Catalogue manager reviews findings and supporting evidence.
6. Manager corrects the listing or requests clarification.
7. Manager determines whether the listing is ready for publication.

The application assists with inspection but does not make final publication or product approval decisions.

### 6. System Boundary

#### Inside the System

- Product information intake.
- Product attribute extraction.
- Product information comparison.
- Missing information detection.
- Contradiction detection.
- Potentially unsupported claim identification.
- Finding classification and severity assignment.
- Evidence generation.
- Inspection report generation.

#### Outside the System

- Supplier communication.
- Live supplier integrations.
- Automatic product catalogue modification.
- Automatic product publication.
- E-commerce platform synchronization.
- Continuous monitoring of entire product catalogues.
- Independent verification of physical product properties.

### 7. Primary User Interaction

The primary interaction is:

**Submit Product → Inspect Listing → Review Findings → Take Action**

The system should provide enough evidence for a human to understand and investigate each finding.

### 8. Human Oversight

All findings are recommendations for review rather than final factual or business decisions.

Users should be able to:

- Review the evidence.
- Accept a finding as valid.
- Dismiss an incorrect finding.
- Correct the product information.
- Request additional clarification.

### 9. Initial Assumptions Requiring Validation

- Catalogue managers perform some form of manual product information review.
- Product information inconsistencies create operational effort.
- Users would benefit from evidence-backed automated inspection.
- A single-listing inspection capability can demonstrate meaningful value.
- Human review is appropriate for ambiguous or uncertain findings.

### 10. Initial Workflow Success Hypothesis

A catalogue manager should be able to submit a product listing, receive clearly explained inspection findings, and use those findings to determine what information requires further review or correction.
