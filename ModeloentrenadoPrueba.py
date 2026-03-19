# ══════════════════════════════════════════════════
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
csv = (
    "creditcard_mini.csv" if os.path.exists("creditcard_mini.csv") else "creditcard.csv"
)
df = pd.read_csv(csv)
total_real = len(df)
fraudes_real = int(df["Class"].sum())
ratio = int((df["Class"] == 0).sum() // fraudes_real)
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
df["Time"] = scaler.fit_transform(df[["Time"]])
X = df.drop("Class", axis=1)
y = df["Class"]

# ── 3. Split ANTES de SMOTE (regla de oro) ────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print("  [1/5] Datos divididos en entrenamiento y prueba ... OK")
print("  [2/5] Aplicando SMOTE — creando fraudes sinteticos ...")
X_train, y_train = SMOTE(random_state=42).fit_resample(X_train, y_train)
n = int((y_train == 0).sum())
print(f"        Resultado: {n:,} ejemplos de cada clase para entrenar")

# ── 4. Entrenar 3 modelos ─────────────────────────
modelos = {
    "Random Forest": RandomForestClassifier(
        n_estimators=20, random_state=42, n_jobs=-1
    ),
    "XGBoost": xgb.XGBClassifier(
        n_estimators=50,
        scale_pos_weight=20,
        eval_metric="logloss",
        random_state=42,
        verbosity=0,
    ),
    "Logistica": LogisticRegression(class_weight="balanced", max_iter=1000),
}
for i, (nombre, modelo) in enumerate(modelos.items(), 3):
    print(f"  [{i}/5] Entrenando {nombre} ...")
    modelo.fit(X_train, y_train)

# ── 5. Resultados en lenguaje simple ──────────────
UMBRAL = 0.3
total_test = int((y_test == 1).sum())
total_leg = int((y_test == 0).sum())

print(f"\n{'=' * 55}")
print(f"  RESULTADOS DEL TEST")
print(f"  (Se probaron {len(y_test):,} transacciones nunca vistas)")
print(f"    -> {total_leg:,} transacciones legitimas")
print(f"    -> {total_test} transacciones fraudulentas")
print(f"{'=' * 55}\n")

resultados = {}
for nombre, modelo in modelos.items():
    proba = modelo.predict_proba(X_test)[:, 1]
    pred = (proba >= UMBRAL).astype(int)
    auc = roc_auc_score(y_test, proba)
    tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
    resultados[nombre] = {
        "tp": int(tp),
        "fn": int(fn),
        "fp": int(fp),
        "tn": int(tn),
        "auc": auc,
    }

    leg_ok = int(tn)
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


# ── 6. Prediccion con transacciones REALES del TEST ──
# Estas transacciones son 100% nuevas para el modelo
# — estaban en el 20% que NUNCA vio durante el entrenamiento
print(f"\n{'=' * 55}")
print(f"  PREDICE TRANSACCIONES REALES")
print(f"  (El modelo NUNCA vio estas durante el entrenamiento)")
print(f"  (No sabe si son fraude — tiene que adivinar)")
print(f"{'=' * 55}")

# Tomar ejemplos reales del conjunto de TEST
fraudes_test = X_test[y_test == 1].head(3)  # 3 fraudes reales del test
legitimas_test = X_test[y_test == 0].head(3)  # 3 legitimas reales del test

casos = list(zip(fraudes_test.iterrows(), ["FRAUDE real"] * 3)) + list(
    zip(legitimas_test.iterrows(), ["LEGITIMA real"] * 3)
)

modelo_principal = modelos["Random Forest"]  # usamos RF para la demo
for (idx, fila), etiqueta_real in casos:
    fila_df = fila.to_frame().T
    score = modelo_principal.predict_proba(fila_df)[0][1]
    pct = score * 100
    pred = "FRAUDE  ⚠" if score >= UMBRAL else "LEGITIMA ✓"
    bloques = int(score * 20)
    barra = "█" * bloques + "░" * (20 - bloques)
    nivel = "ALTO  " if pct >= 70 else "MEDIO " if pct >= 30 else "BAJO  "
    acierto = (
        "✓ CORRECTO"
        if (
            (score >= UMBRAL and "FRAUDE" in etiqueta_real)
            or (score < UMBRAL and "LEGITIMA" in etiqueta_real)
        )
        else "✗ ERROR"
    )
    print(f"\n  Realidad: {etiqueta_real}")
    print(f"  Modelo:   {pred}  {pct:5.1f}% [{barra}] {nivel} {acierto}")

print(f"\n{'=' * 55}")
print(f"  COMO INTERPRETAR:")
print(f"    0% - 29%  -> BAJO  — transaccion aprobada")
print(f"   30% - 69%  -> MEDIO — revision manual recomendada")
print(f"   70% - 100% -> ALTO  — transaccion bloqueada")
print(f"")
print(f"  TIP: Cambia .head(3) por .sample(3) para ver")
print(f"  transacciones aleatorias distintas cada vez.")
print(f"{'=' * 55}")

# ── 7. Crea tu propia transaccion ─────────────────
# Edita los valores abajo y corre el script de nuevo.
#
# RANGOS REALES del dataset:
#   Time   : 0 a 172,792  (segundos — 0=medianoche, 43200=mediodia)
#   V1-V28 : entre -5 y +5 normalmente
#             V14 y V17 muy negativos (-7 a -10) = señal fuerte de fraude
#   Amount : monto en dolares (sin escalar)
#
# EJEMPLO LEGITIMA: V14=0.31,  V17=-0.30, Amount=9.99,  Time=32400
# EJEMPLO FRAUDE:   V14=-9.53, V17=-7.74, Amount=1.00,  Time=406

print(f"\n{'=' * 55}")
print(f"  CREA TU PROPIA TRANSACCION")
print(f"  Edita los valores en el codigo y vuelve a correr")
print(f"{'=' * 55}")

# ── Edita estos valores ───────────────────────────
# TRANSACCION 1 — ejemplo de LEGITIMA
transaccion_1 = pd.DataFrame(
    [
        {
            "Time": 32400,  # 9:00am  (hora * 3600)
            "V1": 1.19,
            "V2": 0.26,
            "V3": 0.17,
            "V4": 0.45,
            "V5": 0.06,
            "V6": -0.08,
            "V7": -0.07,
            "V8": 0.09,
            "V9": 0.31,
            "V10": 0.17,
            "V11": 0.14,
            "V12": 0.12,
            "V13": 0.05,
            "V14": 0.31,  # <- positivo = señal de transaccion normal
            "V15": 0.02,
            "V16": -0.05,
            "V17": -0.30,  # <- cerca de cero = normal
            "V18": 0.01,
            "V19": 0.10,
            "V20": 0.02,
            "V21": 0.01,
            "V22": 0.02,
            "V23": 0.00,
            "V24": 0.00,
            "V25": 0.01,
            "V26": 0.01,
            "V27": 0.00,
            "V28": 0.00,
            "Amount": 9.99,  # monto en dolares
        }
    ]
)[X.columns]

# TRANSACCION 2 — ejemplo de FRAUDE
transaccion_2 = pd.DataFrame(
    [
        {
            "Time": 406,  # 12:06am (medianoche)
            "V1": -3.04,
            "V2": 1.35,
            "V3": -3.47,
            "V4": 0.74,
            "V5": -0.40,
            "V6": 0.83,
            "V7": -1.37,
            "V8": 0.14,
            "V9": -1.46,
            "V10": -2.06,
            "V11": 2.10,
            "V12": -2.63,
            "V13": 0.48,
            "V14": -9.53,  # <- muy negativo = señal fuerte de fraude
            "V15": 0.18,
            "V16": -0.26,
            "V17": -7.74,  # <- muy negativo = señal fuerte de fraude
            "V18": 0.49,
            "V19": 0.01,
            "V20": 0.24,
            "V21": 0.75,
            "V22": -0.56,
            "V23": -0.17,
            "V24": 0.06,
            "V25": -0.06,
            "V26": -0.01,
            "V27": 0.20,
            "V28": 0.14,
            "Amount": 1.00,  # monto en dolares
        }
    ]
)[X.columns]

# ── Evaluar las dos transacciones ─────────────────
mis_transacciones = [
    ("TRANSACCION 1 — Compra normal  $9.99 a las 09:00h", transaccion_1),
    ("TRANSACCION 2 — Compra online  $1.00 a las 00:06h", transaccion_2),
]

for desc, fila_df in mis_transacciones:
    print(f"\n  {desc}")
    print(f"  {'─' * 51}")
    for nombre, modelo in modelos.items():
        score = modelo.predict_proba(fila_df)[0][1]
        pct = score * 100
        pred = "FRAUDE  ⚠" if score >= UMBRAL else "LEGITIMA ✓"
        bloques = int(score * 20)
        barra = "█" * bloques + "░" * (20 - bloques)
        nivel = "ALTO  " if pct >= 70 else "MEDIO " if pct >= 30 else "BAJO  "
        print(f"    {nombre:15} {pred:12} {pct:5.1f}% [{barra}] {nivel}")

print(f"\n{'=' * 55}")
print(f"  COMO INTERPRETAR:")
print(f"    0% - 29%  -> BAJO  — transaccion aprobada")
print(f"   30% - 69%  -> MEDIO — revision manual recomendada")
print(f"   70% - 100% -> ALTO  — transaccion bloqueada")
print(f"")
print(f"  TIP PARA EXPERIMENTAR:")
print(f"    En TRANSACCION 1: cambia V14 a -9.53 y V17 a -7.74")
print(f"    y veras como pasa de LEGITIMA a FRAUDE al instante.")
print(f"{'=' * 55}")
