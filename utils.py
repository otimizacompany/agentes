import streamlit as st

def redirecionar_com_query_params(params: dict):
    """Função para redirecionar com query params usando JavaScript."""
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    js_code = f"""
    <script>
        const newUrl = window.location.origin + window.location.pathname + "?{query_string}";
        window.location.href = newUrl;
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)
