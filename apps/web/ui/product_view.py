import streamlit as st


def render_product_selection(products):
    st.divider()
    st.subheader("Select a product to inspect")

    product_options = {
        f"{product['product_id']} — {product['title']}": product
        for product in products
    }

    selected_label = st.selectbox(
        "Choose a product",
        options=list(product_options.keys()),
    )

    selected_product = product_options[selected_label]

    st.markdown(f"### {selected_product['title']}")
    st.write(selected_product["description"])

    st.caption(f"Category: {selected_product['category']}")

    st.markdown("**Product attributes**")
    st.json(selected_product["attributes"])

    if st.button("Inspect product", type="primary"):
        st.session_state["show_inspection_results"] = True