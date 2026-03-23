"""
mcp_builder_app.py  —  MCP Builder independiente
FraudGuard AI · HackConRD
Ejecutar: streamlit run mcp_builder_app.py
"""
import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(
    page_title="MCP Builder — FraudGuard AI HackConRD",
    page_icon="🔌",
    layout="wide"
)

# Quitar todo padding de Streamlit para que el HTML ocupe toda la pantalla
st.markdown("""
<style>
html,body,[class*="css"]{background:#020810!important;}
.stApp{background:#020810!important;}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
.main .block-container{
    background:#020810!important;
    padding:0!important;
    max-width:100%!important;
    overflow-y:auto!important;
    height:auto!important;
    max-height:none!important;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stToolbar"]{display:none!important;}
[data-testid="stDecoration"]{display:none!important;}
iframe{border:none!important;}
</style>
""", unsafe_allow_html=True)

_html_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "mcp_builder.html"
)

try:
    with open(_html_path, "r", encoding="utf-8") as f:
        _html = f.read()
    components.html(_html, height=1900, scrolling=True)

except FileNotFoundError:
    st.error("No se encontró mcp_builder.html — ponlo en el mismo directorio.")
