MOCK_FINDINGS = [
    {
        "category": "Contradiction",
        "severity": "High",
        "title": "Conflicting material information",
        "evidence": (
            "The product description identifies the chair as plastic, "
            "while its attributes identify the material as teak wood."
        ),
        "explanation": (
            "Customers may receive a product that differs from "
            "what the listing communicates."
        ),
        "suggested_action": (
            "Verify the actual product material and update the "
            "description or attributes."
        ),
        "source": "AI detection",
    },
    {
        "category": "Missing information",
        "severity": "Medium",
        "title": "Warranty information is missing",
        "evidence": "No warranty information was provided.",
        "explanation": (
            "Customers may need warranty details before making "
            "a purchasing decision."
        ),
        "suggested_action": (
            "Confirm the warranty policy and add it to the listing."
        ),
        "source": "Deterministic rule",
    },
    {
        "category": "Unsupported claim",
        "severity": "Low",
        "title": "Weather-resistance claim needs verification",
        "evidence": (
            "The listing describes the product as weather-resistant "
            "but provides no supporting evidence."
        ),
        "explanation": (
            "The claim may be accurate, but the available listing "
            "information does not establish that it is."
        ),
        "suggested_action": (
            "Request supporting product specifications or documentation."
        ),
        "source": "AI detection",
    },
]