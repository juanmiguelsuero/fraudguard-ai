"""
construye_modelo.py  —  Página pública para la charla
Ejecutar: streamlit run construye_modelo.py
"""

import streamlit as st
import os
import pandas as pd
from openai import OpenAI

st.set_page_config(
    page_title="FraudML — Aprende Detección de Fraude", page_icon="🛡️", layout="wide"
)

DEEPSEEK_API_KEY = "sk-23261b5ee48143d38288c5a86ebb156f"
DATASET_LINK = "https://raw.githubusercontent.com/juanmiguelsuero/fraudguard-ai/main/creditcard_mini.csv"  # 50k filas, ~25MB
LOGO_URL = "https://hackconrd.org/uploads/2024/12/logo1200x600-1-768x175.png"
HACKCON_URL = "https://hackconrd.org"

st.markdown(
    """
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
.stTabs [data-baseweb="tab-list"]{
    background:#0d2248;border-radius:12px;padding:4px;gap:4px;margin-bottom:4px;}
.stTabs [data-baseweb="tab"]{
    color:#a0b4cc;font-weight:600;border-radius:8px;
    padding:12px 28px!important;font-size:15px!important;white-space:nowrap;}
.stTabs [aria-selected="true"]{background:#0b1c3d!important;color:#00c2ff!important;}
div.stButton>button{
    background:#0d2248!important;color:#fff!important;
    font-size:14px!important;font-weight:600;
    border:1px solid #1e3a7a;border-radius:10px;
    padding:10px 16px;width:100%;cursor:pointer;transition:all 0.2s;}
div.stButton>button:hover{
    background:#00c2ff!important;color:#0b1c3d!important;border-color:#00c2ff!important;}
pre{border-radius:10px!important;font-size:13px!important;line-height:1.7!important;
    background:#061428!important;color:#00d4ff!important;}
pre code{color:#00d4ff!important;}
code{color:#00d4ff!important;background:#061428!important;
     padding:2px 6px;border-radius:4px;}
.explain-box{
    background:#061428;border-left:3px solid #00c2ff;
    border-radius:0 10px 10px 0;padding:14px 18px;margin:10px 0 6px;}
.tip-box{
    background:#0a1a10;border-left:3px solid #00c46a;
    border-radius:0 10px 10px 0;padding:12px 16px;margin:6px 0 10px;
    font-size:14px;color:#5effa9;}
.warn-box{
    background:#1a0f00;border-left:3px solid #ff8c42;
    border-radius:0 10px 10px 0;padding:12px 16px;margin:6px 0 10px;
    font-size:14px;color:#ffb877;}
.step-badge{
    display:inline-block;background:#00c2ff;color:#0b1c3d;
    font-weight:800;font-size:13px;border-radius:20px;
    padding:3px 12px;margin-bottom:8px;}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li{color:#fff!important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""",
    unsafe_allow_html=True,
)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<div style='text-align:center;padding:20px 0 12px;'>
  <a href='{HACKCON_URL}' target='_blank'>
    <img src='{LOGO_URL}'
         style='max-width:340px;width:70%;margin-bottom:18px;filter:brightness(1.1);'
         alt='HackConRD'>
  </a><br>
  <div style='font-size:46px;margin-bottom:8px;'>🛡️</div>
  <h1 style='font-size:2.2rem;margin:0 0 10px;color:#fff!important;'>
    FraudML — Detección de Fraude con Machine Learning</h1>
  <p style='color:#a0b4cc;font-size:16px;margin:0 0 20px;'>
    Aprende a construir un detector de fraude bancario paso a paso.<br>
    Sin experiencia previa. Solo Python y ganas de aprender.
  </p>
  <a href="{DATASET_LINK}"
     style='display:inline-block;background:linear-gradient(135deg,#00c46a,#00a855);
     color:#fff;font-weight:700;font-size:15px;padding:14px 36px;border-radius:12px;
     text-decoration:none;box-shadow:0 4px 20px #00c46a44;letter-spacing:.5px;'
     target="_blank">
    ⬇️ &nbsp; Paso 0 — Descarga el Dataset (creditcard_mini.csv · 25MB · 50,000 filas)
  </a>
  <p style='color:#4a8a5a;font-size:13px;margin-top:10px;'>
    50,000 transacciones reales · 492 fraudes · Gratis</p>
</div>
<div style='display:flex;justify-content:center;gap:10px;margin:0 0 28px;flex-wrap:wrap;'>
  <span style='background:#0d2248;border:1px solid #1e3a7a;border-radius:20px;
    padding:5px 14px;font-size:13px;color:#a0b4cc;'>🐍 Python 3.9+</span>
  <span style='background:#0a1f10;border:1px solid #1a4a2a;border-radius:20px;
    padding:5px 14px;font-size:13px;color:#00c46a;'>☁️ Google Colab (gratis)</span>
  <span style='background:#0d0d28;border:1px solid #c084fc44;border-radius:20px;
    padding:5px 14px;font-size:13px;color:#c084fc;'>🤖 DeepSeek API (gratis)</span>
  <span style='background:#1a1000;border:1px solid #ff8c4244;border-radius:20px;
    padding:5px 14px;font-size:13px;color:#ff8c42;'>⏱️ ~15 min total</span>
</div>
""",
    unsafe_allow_html=True,
)

# ── TABS ───────────────────────────────────────────────────────────────────────
tab_setup, tab_ml, tab_rag = st.tabs(
    [
        "⚙️  Configuración",
        "🤖  Modelo ML",
        "💬  Mini-RAG con DeepSeek",
    ]
)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 0 — CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════
with tab_setup:

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    op1, op2 = st.columns(2, gap="large")

    with op1:
        st.markdown(
            """
<div style='background:#0d1b35;border:1px solid #1e3a7a;border-radius:14px;padding:24px;'>

<p style='color:#00c2ff;font-size:17px;font-weight:700;margin-bottom:16px;'>
💻 Opción A — Tu propia máquina</p>

<div class='step-badge'>Paso 1</div>
<p style='color:#fff;font-weight:600;margin-bottom:4px;'>Instala Python</p>
<p style='color:#a0b4cc;margin-bottom:12px;'>
Ve a <b style='color:#fff;'>python.org/downloads</b> y descarga Python 3.9 o superior.
Durante la instalación marca la opción <b style='color:#ff8c42;'>☑ Add Python to PATH</b>.
Sin eso, nada funcionará.</p>

<div class='step-badge'>Paso 2</div>
<p style='color:#fff;font-weight:600;margin-bottom:4px;'>Instala las librerías</p>
<p style='color:#a0b4cc;margin-bottom:8px;'>
Abre la terminal (cmd en Windows, Terminal en Mac/Linux) y pega este comando:</p>
<pre style='background:#061428!important;color:#ffffff!important;padding:14px;font-size:13px;;font-weight:600'>pip install pandas numpy scikit-learn imbalanced-learn xgboost openai</pre>
<p style='color:#4a6a9a;font-size:13px;margin-top:6px;margin-bottom:16px;'>
⏱️ Tarda 2-3 minutos. Verás muchas líneas — es normal.</p>

<div class='step-badge'>Paso 3</div>
<p style='color:#fff;font-weight:600;margin-bottom:4px;'>Descarga el dataset</p>
<p style='color:#a0b4cc;margin-bottom:10px;'>
Guárdalo en la misma carpeta donde estará tu archivo <b style='color:#fff;'>fraude.py</b>.</p>
<a href='https://raw.githubusercontent.com/juanmiguelsuero/fraudguard-ai/main/creditcard_mini.csv' target='_blank'
   style='display:inline-block;background:linear-gradient(135deg,#00c46a,#00a855);
   color:#fff;font-weight:700;font-size:13px;padding:10px 22px;border-radius:10px;
   text-decoration:none;margin-bottom:16px;'>
   ⬇️ Descargar creditcard.csv (25MB)
</a>

<div class='step-badge'>Paso 4</div>
<p style='color:#fff;font-weight:600;margin-bottom:4px;'>Crea tu archivo y ejecuta</p>
<p style='color:#a0b4cc;margin-bottom:8px;'>
Abre VS Code, crea <b style='color:#fff;'>fraude.py</b> en esa carpeta y corre:</p>
<pre style='background:#061428!important;color:#ffffff!important;padding:10px;font-size:13px;;font-weight:600'>python fraude.py</pre>

</div>
""",
            unsafe_allow_html=True,
        )

    with op2:
        st.markdown(
            """
<div style='background:#0a1f10;border:1px solid #1a4a2a;border-radius:14px;padding:24px;'>

<p style='color:#00c46a;font-size:17px;font-weight:700;margin-bottom:16px;'>
☁️ Opción B — Google Colab (recomendada)</p>
<p style='color:#5effa9;font-size:13px;margin-bottom:16px;'>
✅ No necesitas instalar nada · GPU gratis · Funciona en el navegador</p>

<div class='step-badge' style='background:#00c46a;'>Paso 1</div>
<p style='color:#fff;font-weight:600;margin-bottom:4px;'>Abre Google Colab</p>
<p style='color:#a0b4cc;margin-bottom:12px;'>
Ve a <b style='color:#fff;'>colab.research.google.com</b> e inicia sesión
con tu cuenta de Google. Haz clic en <b style='color:#fff;'>+ Nuevo notebook</b>.</p>

<div class='step-badge' style='background:#00c46a;'>Paso 2</div>
<p style='color:#fff;font-weight:600;margin-bottom:4px;'>Instala las librerías</p>
<p style='color:#a0b4cc;margin-bottom:8px;'>
En la primera celda escribe esto y presiona ▶:</p>
<pre style='background:#061428!important;color:#ffffff!important;padding:14px;font-size:13px;;font-weight:600'>!pip install imbalanced-learn xgboost openai</pre>
<p style='color:#4a6a9a;font-size:13px;margin-top:6px;margin-bottom:16px;'>
El <b style='color:#fff;'>!</b> al inicio indica que es un comando de terminal.
pandas, numpy y scikit-learn ya vienen instalados en Colab.</p>

<div class='step-badge' style='background:#00c46a;'>Paso 3</div>
<p style='color:#fff;font-weight:600;margin-bottom:4px;'>Descarga y sube el dataset</p>
<p style='color:#a0b4cc;margin-bottom:10px;'>
Primero descárgalo a tu computadora:</p>
<a href='https://raw.githubusercontent.com/juanmiguelsuero/fraudguard-ai/main/creditcard_mini.csv'
   target='_blank'
   style='display:inline-block;background:linear-gradient(135deg,#00c46a,#00a855);
   color:#fff;font-weight:700;font-size:13px;padding:10px 22px;border-radius:10px;
   text-decoration:none;margin-bottom:12px;'>
   ⬇️ Descargar creditcard.csv (25MB)
</a>
<p style='color:#a0b4cc;margin-bottom:12px;'>
Luego en Colab: panel izquierdo → ícono 📁 → ⬆️ → selecciona el archivo.</p>

<div class='step-badge' style='background:#00c46a;'>Paso 4</div>
<p style='color:#fff;font-weight:600;margin-bottom:4px;'>Pega y ejecuta</p>
<p style='color:#a0b4cc;margin-bottom:0;'>
Copia cada sección de código en una celda separada y
presiona ▶ para ejecutarla. El orden importa — ve de arriba a abajo.</p>

</div>
""",
            unsafe_allow_html=True,
        )

    # Librerías explicadas
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown(
        """
<p style='color:#00c2ff;font-size:15px;font-weight:700;margin-bottom:12px;'>
📦 ¿Para qué sirve cada librería?</p>
""",
        unsafe_allow_html=True,
    )

    libs = [
        (
            "pandas",
            "#00c2ff",
            "Maneja tablas de datos. Lee el CSV, filtra filas, calcula promedios.",
        ),
        (
            "numpy",
            "#00c2ff",
            "Matemáticas con arrays. Las otras librerías lo usan internamente.",
        ),
        (
            "scikit-learn",
            "#c084fc",
            "La librería de ML más usada. Incluye modelos, métricas y herramientas de preprocesamiento.",
        ),
        (
            "imbalanced-learn",
            "#ff8c42",
            "Especializada en datasets desbalanceados. Aquí usamos SMOTE para crear fraudes sintéticos.",
        ),
        (
            "xgboost",
            "#ff8c42",
            "El algoritmo de Gradient Boosting más popular. Ganó la mayoría de competencias de Kaggle.",
        ),
        (
            "openai",
            "#c084fc",
            "Librería para conectarse a APIs de LLMs. La usamos con DeepSeek (mismo formato que OpenAI).",
        ),
    ]

    lc = st.columns(3)
    for i, (name, color, desc) in enumerate(libs):
        with lc[i % 3]:
            st.markdown(
                f"<div style='background:#0d1b35;border:1px solid {color}33;"
                f"border-radius:10px;padding:14px;margin-bottom:12px;'>"
                f"<code style='color:{color};font-size:14px;font-weight:700;'>{name}</code>"
                f"<p style='color:#a0b4cc;font-size:13px;margin:8px 0 0;line-height:1.6;'>{desc}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MODELO ML
# ══════════════════════════════════════════════════════════════════════════════
with tab_ml:
    st.markdown(
        """
<div class='explain-box' style='margin-bottom:16px;'>
<b style='color:#00c2ff;'>¿Qué hace este código?</b><br>
<span style='color:#a0b4cc;'>Carga el dataset, preprocesa, entrena 3 modelos y evalúa — todo en un solo bloque.
Cópialo completo en tu editor y ejecútalo.</span>
</div>
<div class='tip-box'>
💡 <b>Regla de oro:</b> Divide train/test ANTES de SMOTE. Si lo haces al revés, los fraudes
sintéticos se mezclan con el test y tus métricas serán falsas.
</div>
""",
        unsafe_allow_html=True,
    )

    st.code(
        r"""# ══════════════════════════════════════════════════
# DETECTOR DE FRAUDE — dataset completo
# Requisito: creditcard_mini.csv en la misma carpeta
# pip install pandas scikit-learn imbalanced-learn xgboost
# ══════════════════════════════════════════════════
import pandas as pd
import numpy as np
import warnings
import os

warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
import xgboost as xgb

# ── 1. Cargar dataset completo ────────────────────
csv = "creditcard_mini.csv" if os.path.exists("creditcard_mini.csv") else "creditcard.csv"
df = pd.read_csv(csv)
total_real   = len(df)
fraudes_real = int(df["Class"].sum())
ratio        = int((df["Class"] == 0).sum() // fraudes_real)
print("=" * 55)
print("  DETECTOR DE FRAUDE — FraudGuard AI")
print("=" * 55)
print(f"  Dataset:  {total_real:,} transacciones cargadas")
print(f"  Fraudes:  {fraudes_real} ({fraudes_real/total_real*100:.2f}% del total)")
print(f"  Es decir: de cada {ratio} compras, solo 1 es fraude.")
print(f"  Usando TODAS las {total_real:,} filas para entrenar.")
print("=" * 55)

# ── 2. Escalar y preparar ─────────────────────────
scaler = StandardScaler()
df["Amount"] = scaler.fit_transform(df[["Amount"]])
df["Time"]   = scaler.fit_transform(df[["Time"]])
X = df.drop("Class", axis=1)
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

print("  [1/5] Datos divididos en entrenamiento y prueba ... OK")
print("  [2/5] Aplicando SMOTE — creando fraudes sinteticos ...")
X_train, y_train = SMOTE(random_state=42).fit_resample(X_train, y_train)
n = int((y_train == 0).sum())
print(f"        Resultado: {n:,} ejemplos de cada clase para entrenar")

# ── 3. Entrenar ───────────────────────────────────
modelos = {
    "Random Forest": RandomForestClassifier(n_estimators=20, random_state=42, n_jobs=-1),
    "XGBoost":       xgb.XGBClassifier(n_estimators=50, scale_pos_weight=20,
                                        eval_metric="logloss", random_state=42, verbosity=0),
    "Logistica":     LogisticRegression(class_weight="balanced", max_iter=1000),
}
for i, (nombre, modelo) in enumerate(modelos.items(), 3):
    print(f"  [{i}/5] Entrenando {nombre} ...")
    modelo.fit(X_train, y_train)

# ── 4. Resultados en lenguaje simple ──────────────
UMBRAL     = 0.3
total_test = int((y_test == 1).sum())
total_leg  = int((y_test == 0).sum())

print(f"\n{'=' * 55}")
print(f"  RESULTADOS DEL TEST")
print(f"  (Se probaron {len(y_test):,} transacciones nunca vistas)")
print(f"    -> {total_leg:,} transacciones legitimas")
print(f"    -> {total_test} transacciones fraudulentas")
print(f"{'=' * 55}\n")

resultados = {}
for nombre, modelo in modelos.items():
    proba = modelo.predict_proba(X_test)[:, 1]
    pred  = (proba >= UMBRAL).astype(int)
    auc   = roc_auc_score(y_test, proba)
    tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
    resultados[nombre] = {"tp": int(tp), "fn": int(fn), "fp": int(fp), "tn": int(tn), "auc": auc}

    leg_ok  = int(tn)
    leg_err = int(fp)
    print(f"  [{nombre}]")
    print(f"  Transacciones legitimas  ({total_leg:,} en total):")
    print(f"    APROBO    {leg_ok:>4} correctamente           ✓")
    print(f"    BLOQUEO   {leg_err:>4} por error  (clientes molestos)  ✗")
    print(f"  Transacciones fraudulentas ({total_test} en total):")
    print(f"    DETECTO   {int(tp):>4} fraudes  ->  clientes protegidos  ✓")
    print(f"    PERDIO    {int(fn):>4} fraudes  ->  dinero que escapo    ✗")
    print(f"  Precision general AUC: {auc:.4f}  (1.0 = perfecto, 0.5 = azar)")
    print()

# ── 5. Conclusion ─────────────────────────────────
print(f"{'=' * 55}")
print(f"  CUAL MODELO ELEGIR?")
print(f"{'=' * 55}")

for nombre, r in resultados.items():
    pct     = r["tp"] / total_test * 100
    pct_leg = r["tn"] / total_leg * 100
    perdida = r["fn"] * 122
    print(f"  {nombre}")
    print(f"    Fraudes detectados:              {r['tp']} de {total_test} ({pct:.0f}%)")
    print(f"    Legitimas aprobadas correctamente: {r['tn']:,} de {total_leg:,} ({pct_leg:.1f}%)")
    print(f"    Perdida estimada no detectada:   ~${perdida:,}")
    print(f"    Clientes bloqueados por error:   {r['fp']}")
    print()

mejor_recall = max(resultados, key=lambda x: resultados[x]["tp"])
menor_fp     = min(resultados, key=lambda x: resultados[x]["fp"])
print(f"  Detecta mas fraudes     -> {mejor_recall}")
print(f"  Menos errores con clientes buenos -> {menor_fp}")
print(f"{'=' * 55}")
""",
        language="python",
    )

    st.markdown(
        """
<div class='warn-box'>
⚠️ <b>Resultado esperado:</b> Recall fraude ~84% · AUC ~0.98 · XGBoost suele ganar en Precision,
Random Forest en estabilidad. Si el entrenamiento tarda mucho, reduce <code>n_estimators=50</code>.
</div>
""",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MINI-RAG
# ══════════════════════════════════════════════════════════════════════════════
with tab_rag:

    st.markdown(
        """
<div style='background:#0d0d28;border:1px solid #c084fc44;border-radius:14px;
padding:20px 24px;margin-bottom:20px;'>
<p style='color:#c084fc;font-size:16px;font-weight:700;margin-bottom:8px;'>¿Qué es este Mini-RAG?</p>
<p style='color:#a0b4cc;font-size:14px;line-height:1.8;margin:0;'>
<b style='color:#fff;'>RAG = Retrieval Augmented Generation.</b>
Le inyectas al modelo un <b style='color:#c084fc;'>contexto</b> antes de cada pregunta
para que responda sobre un tema específico — en este caso, el dataset de fraude.<br>
En esta versión básica ese contexto vive en el <b style='color:#fff;'>system prompt</b>.
En producción se recupera de una base de datos vectorial (ChromaDB, Pinecone).<br>
Son <b style='color:#fff;'>~20 líneas de código</b> y puedes usarlo con cualquier tema.
</p>
</div>
""",
        unsafe_allow_html=True,
    )

    rc1, rc2 = st.columns([1, 1], gap="large")

    with rc1:
        st.markdown(
            """
<div style='background:#0d0d28;border:2px solid #c084fc;border-radius:12px;
padding:12px 16px;margin-bottom:8px;'>
<p style='color:#c084fc;font-size:13px;font-weight:700;letter-spacing:1px;margin-bottom:2px;'>
⚙️ SYSTEM PROMPT — el "cerebro" del RAG</p>
<p style='color:#5a4a7a;font-size:12px;margin:0;'>
Edítalo y observa cómo cambia el comportamiento de FraudBot</p>
</div>
""",
            unsafe_allow_html=True,
        )

        # ── Stats del CSV: reales si existe, fallback si no ──────────────
        _csv = "creditcard.csv"
        if os.path.exists(_csv):
            try:
                _df = pd.read_csv(_csv)
                _total = len(_df)
                _fraud = int(_df["Class"].sum())
                _pct = _df["Class"].mean() * 100
                _ratio = int((_df["Class"] == 0).sum() // _fraud)
                _af = _df[_df["Class"] == 1]["Amount"].mean()
                _al = _df[_df["Class"] == 0]["Amount"].mean()
                _ctx = (
                    f"- {_total:,} transacciones reales (2 días de datos europeos)\n"
                    f"- {_fraud} fraudes — el {_pct:.2f}% del total\n"
                    f"- Ratio: {_ratio}:1 (legítimas vs fraudes)\n"
                    f"- Monto promedio fraude: ${_af:.2f}  |  legítima: ${_al:.2f}\n"
                    f"- Columnas: Time, V1-V28 (PCA anonimizados), Amount, Class\n"
                    f"- Variables más correlacionadas con fraude: V17, V14, V12, V10, V16"
                )
            except Exception:
                _ctx = (
                    "- 50,000 transacciones · 492 fraudes (0.17%) · Ratio 578:1\n"
                    "- Monto promedio fraude: $122  |  legítima: $88\n"
                    "- Columnas: Time, V1-V28 (PCA anonimizados), Amount, Class"
                )
        else:
            _ctx = (
                "- 50,000 transacciones · 492 fraudes (0.17%) · Ratio 578:1\n"
                "- Monto promedio fraude: $122  |  legítima: $88\n"
                "- Columnas: Time, V1-V28 (PCA anonimizados), Amount, Class"
            )

        DEFAULT_SYS = f"""\
Eres FraudBot, un analista de fraude bancario de un banco dominicano.
Responde preguntas sobre el dataset de fraude y el modelo de ML.

SOBRE EL DATASET (creditcard.csv):
{_ctx}

SOBRE LOS MODELOS:
- Random Forest, XGBoost y Regresión Logística entrenados con SMOTE
- Recall típico: ~84%  |  Precision: ~88%  |  AUC-ROC: ~0.98

CONCEPTOS CLAVE:
- Recall: de todos los fraudes reales, cuántos detectamos (el más importante)
- Accuracy: inútil aquí — predecir todo como legítimo da 99.83%
- SMOTE: crea fraudes sintéticos solo en el train, nunca en el test
- Umbral 0.3: más sensible al fraude, aunque genera más falsas alarmas

Responde en español, claro y con ejemplos. Máximo 3 párrafos.\
"""

        system_prompt = st.text_area(
            "System Prompt:",
            value=DEFAULT_SYS,
            height=360,
            key="sys_prompt",
            label_visibility="collapsed",
        )

        st.markdown(
            """
<p style='color:#c084fc;font-size:13px;font-weight:700;
letter-spacing:1px;margin:16px 0 8px;'>📋 Código para tu máquina:</p>
""",
            unsafe_allow_html=True,
        )

        st.code(
            '''# =====================================================
# FRAUDBOT - Mini-RAG con DeepSeek
# pip install openai pandas
# Necesitas: creditcard.csv + API Key de DeepSeek
#   -> platform.deepseek.com -> API Keys -> Create (gratis)
# =====================================================
import pandas as pd
from openai import OpenAI

# -- Conectar a DeepSeek ----------------------------------
client = OpenAI(
    api_key="TU_API_KEY_AQUI",        # <- pega tu key aqui
    base_url="https://api.deepseek.com"
)

# -- Cargar el dataset y calcular stats reales ------------
df        = pd.read_csv("creditcard.csv")
total     = len(df)
fraudes   = int(df["Class"].sum())
pct       = round(df["Class"].mean() * 100, 2)
ratio     = int((df["Class"]==0).sum() // fraudes)
amt_fraud = round(df[df["Class"]==1]["Amount"].mean(), 2)
amt_leg   = round(df[df["Class"]==0]["Amount"].mean(), 2)

print(f"Dataset cargado: {total:,} transacciones")
print(f"Fraudes: {fraudes} ({pct}%) | Ratio: {ratio}:1")

# -- System prompt con datos REALES del CSV ---------------
# Este contexto se envia en CADA mensaje -> eso es el RAG
SYSTEM_PROMPT = f"""
Eres FraudBot, analista de fraude de un banco dominicano.
Responde preguntas sobre el dataset y el modelo de ML.

DATASET (creditcard.csv - cargado en vivo):
- {total:,} transacciones reales de tarjetas europeas
- {fraudes} fraudes - el {pct}% del total
- Ratio: {ratio}:1 (legitimas vs fraudes)
- Monto promedio fraude: ${amt_fraud} | legitima: ${amt_leg}
- Columnas: Time, V1-V28 (PCA anonimizados), Amount, Class

MODELOS ENTRENADOS:
- Random Forest, XGBoost, Logistica + SMOTE
- Recall ~84% | Precision ~88% | AUC-ROC ~0.98
- Umbral de decision: 0.3 (mas sensible al fraude)

CONCEPTOS CLAVE:
- Recall: % de fraudes reales detectados (prioridad maxima)
- Accuracy: inutil - predecir todo como legitimo da {100-pct}%
- SMOTE: genera fraudes sinteticos SOLO en train, nunca test
- Umbral 0.3: captura mas fraudes, pero genera mas alertas

Responde en espanol, claro y con ejemplos. Max 3 parrafos.
"""

# -- Chat con memoria -------------------------------------
historial = []

def preguntar(pregunta):
    historial.append({"role": "user", "content": pregunta})
    r = client.chat.completions.create(
        model       = "deepseek-chat",
        messages    = [{"role": "system", "content": SYSTEM_PROMPT}] + historial,
        max_tokens  = 400,
        temperature = 0.3
    )
    respuesta = r.choices[0].message.content
    historial.append({"role": "assistant", "content": respuesta})
    print(f"FraudBot: {respuesta}\n")
    return respuesta

# -- 5 preguntas de prueba --------------------------------
# Cada una muestra algo distinto del poder del RAG:

# 1. Usa los numeros REALES del CSV que acabas de cargar
preguntar(f"Tengo {total:,} transacciones y solo {fraudes} son fraudes. "
          f"Como afecta ese desbalance al entrenamiento?")

# 2. Pregunta de negocio — no tecnica
preguntar("Si el modelo no detecta un fraude de $500, "
          "cuanto le cuesta al banco vs bloquear una tarjeta buena?")

# 3. Usa las stats reales del sistema prompt
preguntar(f"El monto promedio de fraude es ${amt_fraud} y el legitimo ${amt_leg}. "
          f"Por que los fraudes no son siempre las transacciones mas grandes?")

# 4. El argumento que todo CEO necesita escuchar
preguntar("Tengo un modelo con 99.8% de Accuracy pero el banco dice que es inutil. "
          "Como le explico por que ese numero miente?")

# 5. La pregunta que conecta el lab con el mundo real
preguntar("El modelo funciona bien en el test. "
          "Cuales son los 3 problemas principales al ponerlo en produccion?")
''',
            language="python",
        )

    with rc2:
        st.markdown(
            """
<p style='color:#c084fc;font-size:13px;font-weight:700;
letter-spacing:1px;margin-bottom:12px;'>
🚀 Prueba FraudBot aquí — pregunta sobre el dataset:</p>
""",
            unsafe_allow_html=True,
        )

        QUICK = [
            (
                "📊 ¿Qué hay en el dataset?",
                "¿Qué contiene el dataset creditcard.csv y qué significan las columnas V1 a V28?",
            ),
            (
                "⚖️ ¿Por qué 0.17% de fraudes?",
                "¿Por qué hay tan pocos fraudes en el dataset y cómo afecta eso al entrenamiento?",
            ),
            (
                "🔄 ¿Cómo funciona SMOTE?",
                "¿Qué hace SMOTE exactamente y por qué solo se aplica al conjunto de entrenamiento?",
            ),
            (
                "📈 Recall vs Accuracy",
                "¿Por qué el Recall es más importante que el Accuracy en detección de fraude?",
            ),
            (
                "🌲 ¿Cuál modelo es mejor?",
                "¿Cuál de los 3 modelos es mejor para detectar fraude y en qué situaciones usarías cada uno?",
            ),
            (
                "🎚️ ¿Qué umbral elegir?",
                "¿Cómo decido si usar umbral 0.3 o 0.5? ¿Qué cambia en la práctica?",
            ),
            (
                "💰 ¿Cuánto cuesta un fraude no detectado?",
                "¿Cuál es el impacto real de no detectar un fraude vs generar una falsa alarma?",
            ),
            (
                "🚀 ¿Qué falta para producción?",
                "¿Qué pasos faltan para llevar este modelo a producción en un banco real?",
            ),
        ]

        qc1, qc2 = st.columns(2)
        for i, (lbl, q) in enumerate(QUICK):
            col = qc1 if i % 2 == 0 else qc2
            with col:
                if st.button(lbl, key=f"rq_{i}", use_container_width=True):
                    st.session_state["rag_prefill"] = q

        st.markdown("<div style='margin:10px 0'></div>", unsafe_allow_html=True)

        if "rag_msgs" not in st.session_state:
            st.session_state["rag_msgs"] = []

        if not st.session_state["rag_msgs"]:
            st.markdown(
                """
<div style='background:#0d1028;border:1px dashed #2a2a5a;border-radius:12px;
padding:28px 20px;text-align:center;color:#4a4a8a;font-size:14px;margin-bottom:10px;'>
Haz clic en una pregunta o escribe la tuya 👇<br>
<span style='font-size:12px;color:#2a2a5a;'>
FraudBot usa el system prompt que ves a la izquierda</span>
</div>""",
                unsafe_allow_html=True,
            )
        else:
            for msg in st.session_state["rag_msgs"]:
                if msg["role"] == "user":
                    st.markdown(
                        f"<div style='background:#0d2248;border:1px solid #1e3a7a;"
                        f"border-radius:12px 12px 4px 12px;padding:12px 16px;"
                        f"margin:5px 0;font-size:14px;color:#fff;'>"
                        f"<span style='font-size:11px;color:#4a6a9a;'>👤 TÚ</span><br>"
                        f"{msg['content']}</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div style='background:#0d0d28;border:1px solid #c084fc44;"
                        f"border-radius:12px 12px 12px 4px;padding:12px 16px;"
                        f"margin:5px 0;font-size:14px;color:#fff;'>"
                        f"<span style='font-size:11px;color:#c084fc;'>🤖 FRAUDBOT</span><br>"
                        f"{msg['content']}</div>",
                        unsafe_allow_html=True,
                    )

        pf = (
            st.session_state.pop("rag_prefill", "")
            if "rag_prefill" in st.session_state
            else ""
        )
        user_q = st.text_input(
            "Pregunta:",
            value=pf,
            placeholder="Ej: ¿Qué significa AUC-ROC y cómo se interpreta?",
            key="rag_input",
            label_visibility="collapsed",
        )

        bc1, bc2 = st.columns([5, 1])
        with bc1:
            ask = st.button(
                "💬 Preguntar a FraudBot", key="rag_ask", use_container_width=True
            )
        with bc2:
            if st.button("🗑️", key="rag_clear", use_container_width=True):
                st.session_state["rag_msgs"] = []
                st.rerun()

        if ask and user_q.strip():
            st.session_state["rag_msgs"].append(
                {"role": "user", "content": user_q.strip()}
            )
            try:
                c = OpenAI(
                    api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"
                )
                with st.spinner("FraudBot está pensando..."):
                    r = c.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {
                                "role": "system",
                                "content": st.session_state.get(
                                    "sys_prompt", DEFAULT_SYS
                                ),
                            }
                        ]
                        + st.session_state["rag_msgs"],
                        max_tokens=500,
                        temperature=0.3,
                    )
                st.session_state["rag_msgs"].append(
                    {"role": "assistant", "content": r.choices[0].message.content}
                )
            except Exception as e:
                st.session_state["rag_msgs"].append(
                    {"role": "assistant", "content": f"⚠️ Error: {e}"}
                )
            st.rerun()

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<hr style='border-color:#1e3a7a;margin:40px 0 20px;'>", unsafe_allow_html=True
)
fc1, fc2, fc3 = st.columns(3)
for col, (icon, color, title, link, desc) in zip(
    [fc1, fc2, fc3],
    [
        (
            "📥",
            "#00c2ff",
            "Dataset",
            "Botón verde de descarga ⬆️",
            "creditcard.csv · 50,000 transacciones · 25MB",
        ),
        (
            "🔑",
            "#c084fc",
            "API DeepSeek",
            "platform.deepseek.com → API Keys",
            "Registro gratis · $0.14 por millón de tokens",
        ),
        (
            "☁️",
            "#00c46a",
            "Google Colab",
            "colab.research.google.com",
            "Sin instalar nada · GPU gratis · Funciona en el navegador",
        ),
    ],
):
    with col:
        st.markdown(
            f"<div style='background:#0d1b35;border:1px solid {color}33;"
            f"border-radius:12px;padding:18px;text-align:center;'>"
            f"<div style='font-size:30px;margin-bottom:8px;'>{icon}</div>"
            f"<p style='color:{color};font-size:14px;font-weight:700;margin-bottom:4px;'>{title}</p>"
            f"<p style='color:#fff;font-size:13px;margin-bottom:4px;'>{link}</p>"
            f"<p style='color:#a0b4cc;font-size:12px;margin:0;'>{desc}</p></div>",
            unsafe_allow_html=True,
        )
