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
    font-size:15px!important;font-weight:700;
    border:1px solid #1e3a7a;border-radius:10px;
    padding:12px 20px;width:100%;cursor:pointer;transition:all 0.2s;}
div.stButton>button:hover{
    background:#00c2ff!important;color:#0b1c3d!important;border-color:#00c2ff!important;}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li{color:#fff!important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
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
    Aprende los dos lados de la seguridad en IA.
  </p>
</div>
<div style='display:flex;justify-content:center;gap:10px;margin:0 0 20px;flex-wrap:wrap;'>
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

# ── MODO SWITCH — en Streamlit nativo para que sea visible ───────────────────
if "mcp_modo" not in st.session_state:
    st.session_state["mcp_modo"] = "defensor"

modo = st.session_state["mcp_modo"]

st.markdown("""
<p style='text-align:center;color:#a0b4cc;font-size:14px;
font-weight:700;letter-spacing:2px;text-transform:uppercase;
margin-bottom:12px;'>Elige tu modo</p>
""", unsafe_allow_html=True)

col_l, col_def, col_atk, col_r = st.columns([1, 2, 2, 1])

with col_def:
    if modo == "defensor":
        st.markdown("""
<div style='background:#0a1f10;border:2px solid #00c46a;border-radius:12px;
padding:16px;text-align:center;'>
  <div style='font-size:28px;margin-bottom:6px;'>🛡️</div>
  <p style='color:#00c46a;font-size:16px;font-weight:700;margin:0 0 4px;'>MODO DEFENSOR</p>
  <p style='color:#5effa9;font-size:12px;margin:0;'>Activo</p>
</div>""", unsafe_allow_html=True)
    else:
        if st.button("🛡️  Modo Defensor\nConfigura tu servidor MCP", key="btn_def"):
            st.session_state["mcp_modo"] = "defensor"
            st.rerun()

with col_atk:
    if modo == "atacante":
        st.markdown("""
<div style='background:#1a0608;border:2px solid #ff3b3f;border-radius:12px;
padding:16px;text-align:center;'>
  <div style='font-size:28px;margin-bottom:6px;'>☠️</div>
  <p style='color:#ff3b3f;font-size:16px;font-weight:700;margin:0 0 4px;'>MODO ATACANTE</p>
  <p style='color:#ff8888;font-size:12px;margin:0;'>Activo</p>
</div>""", unsafe_allow_html=True)
    else:
        if st.button("☠️  Modo Atacante\nElige objetivo y ejecuta", key="btn_atk"):
            st.session_state["mcp_modo"] = "atacante"
            st.rerun()

st.markdown("<hr style='border-color:#1e3a7a;margin:20px 0;'>", unsafe_allow_html=True)

# ── DESCRIPCION DEL MODO ACTIVO ───────────────────────────────────────────────
if modo == "defensor":
    st.markdown("""
<div style='background:#061428;border-left:3px solid #00c2ff;
border-radius:0 10px 10px 0;padding:14px 18px;margin-bottom:20px;'>
<b style='color:#00c2ff;'>🛡️ Modo Defensor — 4 pasos:</b>
<span style='color:#a0b4cc;'>
Paso 1: Elige los recursos que puede acceder el modelo →
Paso 2: Define políticas de lectura, escritura y exportación →
Paso 3: Configura qué monitorea y qué bloquea →
Paso 4: Prueba ataques reales contra tu configuración
</span>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown("""
<div style='background:#1a0608;border-left:3px solid #ff3b3f;
border-radius:0 10px 10px 0;padding:14px 18px;margin-bottom:20px;'>
<b style='color:#ff3b3f;'>☠️ Modo Atacante — Educativo:</b>
<span style='color:#a0b4cc;'>
Paso 1: Elige tu objetivo (banco, fintech, salud) →
Paso 2: Elige tu nivel de acceso (externo, interno, proveedor) →
Paso 3: Elige el arma (Prompt Injection, Exfiltración, Escalada) →
Paso 4: Ve la probabilidad de éxito con y sin MCP configurado
</span>
</div>
""", unsafe_allow_html=True)

# ── CARGAR EL HTML CON EL MODO CORRECTO ───────────────────────────────────────
_html_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "mcp_builder.html"
)

try:
    with open(_html_path, "r", encoding="utf-8") as f:
        _html_raw = f.read()

    # Ocultar header del HTML (Streamlit ya lo tiene arriba)
    # Ocultar el mode-switch del HTML (Streamlit lo maneja arriba)
    # Arrancar en el modo correcto automáticamente
    _modo_js = f"setMode('{modo}');"

    _patch = f"""<style>
    body{{background:transparent!important;margin:0;padding:0}}
    .app{{padding:0 4px 24px!important;max-width:100%!important}}
    .hdr{{display:none!important}}
    .mode-wrap{{display:none!important}}
    </style>
    <script>
    // Auto-inicializar el modo correcto cuando carga
    window.addEventListener('DOMContentLoaded', function() {{
        setTimeout(function() {{ {_modo_js} }}, 100);
    }});
    </script>"""

    _html_patched = _html_raw.replace("</head>", _patch + "\n</head>")
    # También inicializar antes del cierre del body
    _html_patched = _html_patched.replace(
        "initRes();renderDNav(1);",
        f"initRes();renderDNav(1);\nsetMode('{modo}');"
    )

    components.html(_html_patched, height=1800, scrolling=True)

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

# ── FOOTER ────────────────────────────────────────────────────────────────────
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
