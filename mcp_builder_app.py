"""
mcp_builder_app.py — App independiente MCP Builder
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

# ── Estilos globales ──────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] {
    background: #020810 !important;
    color: #e8f0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}
.stApp { background: #020810 !important; }
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
.main .block-container {
    background: #020810 !important;
    overflow-y: auto !important;
    height: auto !important;
    max-height: none !important;
    padding: 0 !important;
    max-width: 100% !important;
}
/* Ocultar header y footer de Streamlit */
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0b1c3d; }
::-webkit-scrollbar-thumb { background: #1e3a7a; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #00c2ff; }
</style>
""", unsafe_allow_html=True)

# ── Cargar el HTML del MCP Builder ───────────────────────────────────────────
_html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_builder.html")

try:
    with open(_html_path, "r", encoding="utf-8") as f:
        _html = f.read()
    components.html(_html, height=1500, scrolling=True)
except FileNotFoundError:
    st.error("⚠️ No se encontró mcp_builder.html en el mismo directorio.")
    st.info("Asegúrate de que mcp_builder.html esté junto a mcp_builder_app.py")
