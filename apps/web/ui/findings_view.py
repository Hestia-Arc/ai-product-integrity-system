
import streamlit as st

from product_integrity.presentation.mock_findings import MOCK_FINDINGS


def render_inspection_results():
    st.divider()
    st.subheader("Inspection results")

    st.caption(
        "Demonstration findings — these are mock results, "
        "not generated from the selected product."
    )

    findings = MOCK_FINDINGS

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total findings", len(findings))

    with col2:
        high_severity = sum(
            finding["severity"] == "High"
            for finding in findings
        )
        st.metric("High severity", high_severity)

    with col3:
        ai_findings = sum(
            finding["source"] == "AI detection"
            for finding in findings
        )
        st.metric("AI-detected", ai_findings)

    for index, finding in enumerate(findings, start=1):
        with st.container(border=True):
            st.markdown(
                f"**{index}. {finding['title']}**"
            )

            st.write(
                f"Category: {finding['category']}  |  "
                f"Severity: {finding['severity']}  |  "
                f"Source: {finding['source']}"
            )

            st.markdown("**Evidence**")
            st.write(finding["evidence"])

            st.markdown("**Why this matters**")
            st.write(finding["explanation"])

            st.markdown("**Suggested action**")
            st.write(finding["suggested_action"])

            st.selectbox(
                "Review status",
                options=[
                    "Needs review",
                    "Confirmed",
                    "Dismissed",
                ],
                key=f"review_status_{index}",
            )
