
import streamlit as st

from product_integrity.importing.product_importer import (
    ProductImportError,
    import_csv,
    import_json,
)


def render_import_section():
    st.subheader("Import your products")

    st.write(
        "Upload a product catalogue exported from your existing "
        "store or catalogue management system."
    )

    uploaded_file = st.file_uploader(
        "Upload a product file",
        type=["csv", "json"],
        accept_multiple_files=False,
        help="Supported formats: CSV and JSON.",
    )

    st.caption("Supported formats: CSV and JSON.")

    return uploaded_file


def process_uploaded_file(uploaded_file):
    content = uploaded_file.getvalue().decode("utf-8-sig")

    if uploaded_file.name.lower().endswith(".csv"):
        return import_csv(content)

    if uploaded_file.name.lower().endswith(".json"):
        return import_json(content)

    raise ProductImportError("Unsupported file format.")


def render_import_results(products, errors):
    st.divider()
    st.subheader("Import results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Products imported", len(products))

    with col2:
        st.metric("Import issues", len(errors))

    if products:
        st.subheader("Product preview")

        preview_rows = [
            {
                "Product ID": product["product_id"],
                "Title": product["title"],
                "Category": product["category"],
                "Attributes": len(product["attributes"]),
            }
            for product in products
        ]

        st.dataframe(
            preview_rows,
            use_container_width=True,
            hide_index=True,
        )

    if errors:
        st.subheader("Import issues")

        for error in errors:
            st.warning(error)

    if not products and not errors:
        st.info("No products were found in the uploaded file.")
