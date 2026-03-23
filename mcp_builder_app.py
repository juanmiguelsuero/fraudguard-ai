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

LOGO_URL    = "https://hackconrd.org/uploads/2024/12/logo1200x600-1-768x175.png"
HACKCON_URL = "https://hackconrd.org"

# ── Estilos globales — idénticos a construye_modelo.py ────────────────────────
st.markdown("""
<style>
html,body,[class*="css"]{background:#0b1c3d;color:#fff;font-family:'Segoe UI',sans-serif;}
.stApp{background:#0b1c3d;overflow-y:auto!important;}
[data-testid="stAppViewContainer"],[data-testid="stMain"],
section.main,.main .block-container{
    overflow-y:auto!important;height:auto!important;
    max-height:none!important;padding-bottom:80px!important;}
h1,h2,h3{color:#00c2ff!important;}
p,li{font-size:15px;line-height:1.8;}
::-webkit-scrollbar{width:7px;}
::-webkit-scrollbar-track{background:#0b1c3d;}
::-webkit-scrollbar-thumb{background:#1e3a7a;border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:#00c2ff;}
div.stButton>button{
    background:#0d2248!important;color:#fff!important;
    font-size:14px!important;font-weight:600;
    border:1px solid #1e3a7a;border-radius:10px;
    padding:10px 16px;width:100%;cursor:pointer;transition:all 0.2s;}
div.stButton>button:hover{
    background:#00c2ff!important;color:#0b1c3d!important;border-color:#00c2ff!important;}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li{color:#fff!important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── HEADER — idéntico a construye_modelo.py ───────────────────────────────────
st.markdown(f"""
<div style='text-align:center;padding:20px 0 12px;'>
  <a href='{HACKCON_URL}' target='_blank'>
    <img src='{LOGO_URL}'
         style='max-width:340px;width:70%;margin-bottom:18px;filter:brightness(1.1);'
         alt='HackConRD'>
  </a><br>
  <div style='font-size:46px;margin-bottom:8px;'>🔌</div>
  <h1 style='font-size:2.2rem;margin:0 0 10px;color:#fff!important;'>
    MCP Builder — Seguridad en Modelos de IA</h1>
  <p style='color:#a0b4cc;font-size:16px;margin:0 0 20px;'>
    Construye tu propio servidor MCP · Define políticas de seguridad · Prueba ataques reales.<br>
    Modo Defensor y Modo Atacante — aprende los dos lados de la seguridad en IA.
  </p>
</div>
<div style='display:flex;justify-content:center;gap:10px;margin:0 0 28px;flex-wrap:wrap;'>
  <span style='background:#0d0d28;border:1px solid #c084fc44;border-radius:20px;
    padding:5px 14px;font-size:13px;color:#c084fc;'>🔌 MCP Protocol</span>
  <span style='background:#0a1f10;border:1px solid #1a4a2a;border-radius:20px;
    padding:5px 14px;font-size:13px;color:#00c46a;'>🛡️ Modo Defensor</span>
  <span style='background:#1a0608;border:1px solid #ff3b3f44;border-radius:20px;
    padding:5px 14px;font-size:13px;color:#ff3b3f;'>☠️ Modo Atacante</span>
  <span style='background:#1a1000;border:1px solid #ff8c4244;border-radius:20px;
    padding:5px 14px;font-size:13px;color:#ff8c42;'>⚡ Ataques reales simulados</span>
</div>
""", unsafe_allow_html=True)

# ── MCP BUILDER HTML ──────────────────────────────────────────────────────────
_html_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "mcp_builder.html"
)

try:
    with open(_html_path, "r", encoding="utf-8") as f:
        _html_raw = f.read()

    # Ocultar el header del HTML (ya lo muestra Streamlit arriba)
    # y hacer el fondo transparente para que encaje
    _patch = """<style>
    body{background:transparent!important;margin:0;padding:0}
    .app{padding:0 4px 24px!important;max-width:100%!important}
    .hdr{display:none!important}
    </style>"""
    _html_patched = _html_raw.replace("</head>", _patch + "\n</head>")

    components.html(_html_patched, height=1700, scrolling=True)

except FileNotFoundError:
    st.markdown("""
<div style='background:#1a0608;border:1px solid #ff3b3f44;border-radius:12px;
padding:24px;text-align:center;'>
  <p style='color:#ff3b3f;font-size:16px;font-weight:700;margin-bottom:8px;'>
    ⚠️ Archivo no encontrado</p>
  <p style='color:#a0b4cc;font-size:14px;margin:0;'>
    Asegúrate de que <code style='color:#00c2ff'>mcp_builder.html</code>
    esté en el mismo directorio que <code style='color:#00c2ff'>mcp_builder_app.py</code>
  </p>
</div>
""", unsafe_allow_html=True)

# ── FOOTER — idéntico a construye_modelo.py ───────────────────────────────────
st.markdown(
    "<hr style='border-color:#1e3a7a;margin:40px 0 20px;'>",
    unsafe_allow_html=True
)

fc1, fc2, fc3 = st.columns(3)
for col, (icon, color, title, link, desc) in zip([fc1, fc2, fc3], [
    ("🔌", "#c084fc", "MCP Protocol",
     "modelcontextprotocol.io",
     "Estándar abierto de Anthropic para conectar modelos a recursos"),
    ("🛡️", "#00c2ff", "FraudGuard AI",
     "fraudguard-hackconrd.streamlit.app",
     "App principal · 14 tabs · Demos en vivo de fraude bancario"),
    ("💻", "#00c46a", "Código fuente",
     "github.com/juanmiguelsuero/fraudguard-ai",
     "Todo el código disponible públicamente en GitHub"),
]):
    with col:
        st.markdown(
            f"<div style='background:#0d1b35;border:1px solid {color}33;"
            f"border-radius:12px;padding:18px;text-align:center;'>"
            f"<div style='font-size:30px;margin-bottom:8px;'>{icon}</div>"
            f"<p style='color:{color};font-size:14px;font-weight:700;margin-bottom:4px;'>{title}</p>"
            f"<p style='color:#fff;font-size:13px;margin-bottom:4px;'>{link}</p>"
            f"<p style='color:#a0b4cc;font-size:12px;margin:0;'>{desc}</p></div>",
            unsafe_allow_html=True
        )

st.markdown(
    "<p style='text-align:center;color:#3a5a7a;font-size:13px;margin-top:20px;'>"
    "🛡️ FraudGuard AI &nbsp;·&nbsp; HackConRD &nbsp;·&nbsp; "
    "<a href='https://github.com/juanmiguelsuero/fraudguard-ai' "
    "style='color:#1e3a7a;text-decoration:none;'>"
    "github.com/juanmiguelsuero/fraudguard-ai</a></p>",
    unsafe_allow_html=True
)
