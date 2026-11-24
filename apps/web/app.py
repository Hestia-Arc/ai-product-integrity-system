
import streamlit as st

from ui.import_view import (
    process_uploaded_file,
    render_import_results,
    render_import_section,
)

from ui.product_view import render_product_selection
from ui.findings_view import render_inspection_results

from product_integrity.importing.product_importer import ProductImportError

st.set_page_config(
    page_title="Product Listing Integrity Monitor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_header():
    st.title("Product Listing Integrity Monitor")

    st.write(
        "Inspect product listings for contradictions, "
        "missing information, and potential catalogue quality issues."
    )

    st.divider()


def main():
    render_header()

    uploaded_file = render_import_section()

    if uploaded_file is None:
        st.info(
            "Upload a product file to begin importing your catalogue."
        )
        return

    try:
        products, errors = process_uploaded_file(uploaded_file)

        render_import_results(products, errors)

        if products:
            render_product_selection(products)

            if st.session_state.get("show_inspection_results", False):
                render_inspection_results()

    except ProductImportError as exc:
        st.error(f"Unable to import file: {exc}")

    except UnicodeDecodeError:
        st.error(
            "The uploaded file must use UTF-8 text encoding."
        )


if __name__ == "__main__":
    main()
