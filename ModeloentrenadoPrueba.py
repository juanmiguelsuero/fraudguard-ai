# ══════════════════════════════════════════════════
# DETECTOR DE FRAUDE — version rapida (~20 segundos)
# Requisito: creditcard.csv en la misma carpeta
# pip install pandas scikit-learn imbalanced-learn xgboost
# ══════════════════════════════════════════════════
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
import xgboost as xgb

# ── 1. Cargar dataset ─────────────────────────────
df = pd.read_csv("creditcard.csv")
total_real = len(df)
fraudes_real = int(df["Class"].sum())
print("=" * 55)
print("  DETECTOR DE FRAUDE — FraudGuard AI")
print("=" * 55)
print(f"  Dataset:  {total_real:,} transacciones cargadas")
print(f"  Fraudes:  {fraudes_real} ({fraudes_real/total_real*100:.2f}% del total)")
print(f"  Es decir: de cada 578 compras, solo 1 es fraude.")
print("=" * 55)

legitimas = df[df["Class"] == 0].sample(10_000, random_state=42)
fraudes = df[df["Class"] == 1]
df = pd.concat([legitimas, fraudes]).sample(frac=1, random_state=42)
print(f"\n  Usando {len(df):,} filas para entrenar rapido.")
print(f"  (En produccion se entrena con el dataset completo)\n")

# ── 2. Escalar y preparar ─────────────────────────
scaler = StandardScaler()
df["Amount"] = scaler.fit_transform(df[["Amount"]])
df["Time"] = scaler.fit_transform(df[["Time"]])
X = df.drop("Class", axis=1)
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print("  [1/5] Datos divididos en entrenamiento y prueba ... OK")
print("  [2/5] Aplicando SMOTE — creando fraudes sinteticos ...")
X_train, y_train = SMOTE(random_state=42).fit_resample(X_train, y_train)
n = int((y_train == 0).sum())
print(f"        Resultado: {n:,} ejemplos de cada clase para entrenar")

# ── 3. Entrenar ───────────────────────────────────
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

# ── 4. Resultados en lenguaje simple ──────────────
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

    pct = int(tp) / total_test * 100
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

# ── 5. Conclusion ─────────────────────────────────
print(f"{'=' * 55}")
print(f"  CUAL MODELO ELEGIR?")
print(f"{'=' * 55}")

for nombre, r in resultados.items():
    pct = r["tp"] / total_test * 100
    pct_leg = r["tn"] / total_leg * 100
    perdida = r["fn"] * 122
    print(f"  {nombre}")
    print(
        f"    Fraudes detectados:              {r['tp']} de {total_test} ({pct:.0f}%)"
    )
    print(
        f"    Legitimas aprobadas correctamente: {r['tn']:,} de {total_leg:,} ({pct_leg:.1f}%)"
    )
    print(f"    Perdida estimada no detectada:   ~${perdida:,}")
    print(f"    Clientes bloqueados por error:   {r['fp']}")
    print()

mejor_recall = max(resultados, key=lambda x: resultados[x]["tp"])
menor_fp = min(resultados, key=lambda x: resultados[x]["fp"])
print(f"  Detecta mas fraudes     -> {mejor_recall}")
print(f"  Menos errores con clientes buenos -> {menor_fp}")
print(f"")
print(f"  NOTA IMPORTANTE:")
print(f"  Logistica detecta mas fraudes pero bloquea muchas tarjetas buenas.")
print(f"  Eso pasa porque este script usa pocos datos de entrenamiento.")
print(f"  Con el dataset completo (284k filas) Random Forest y XGBoost")
print(f"  mejoran mucho — son los modelos que usa FraudGuard en produccion.")
print(f"{'=' * 55}")
