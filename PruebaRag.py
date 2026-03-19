# =====================================================
# FRAUDBOT - Mini-RAG con DeepSeek
# pip install openai pandas
# Necesitas: creditcard_mini.csv + API Key de DeepSeek
# =====================================================
import pandas as pd
import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-23261b5ee48143d38288c5a86ebb156f",
    base_url="https://api.deepseek.com",
)

# -- Cargar dataset ---------------------------------------
csv = (
    "creditcard_mini.csv" if os.path.exists("creditcard_mini.csv") else "creditcard.csv"
)
df = pd.read_csv(csv)

total = len(df)
fraudes = int(df["Class"].sum())
pct = round(df["Class"].mean() * 100, 2)
ratio = int((df["Class"] == 0).sum() // fraudes)
amt_fraud = round(df[df["Class"] == 1]["Amount"].mean(), 2)
amt_leg = round(df[df["Class"] == 0]["Amount"].mean(), 2)
fraude_max = round(df[df["Class"] == 1]["Amount"].max(), 2)
fraude_min = round(df[df["Class"] == 1]["Amount"].min(), 2)

# -- Distribucion por hora --------------------------------
df["hora"] = (df["Time"] / 3600 % 24).astype(int)
fraudes_por_hora = (
    df[df["Class"] == 1].groupby("hora").size().reindex(range(24), fill_value=0)
)
hora_pico = int(fraudes_por_hora.idxmax())
pico_cant = int(fraudes_por_hora.max())

# Construir string de distribucion horaria
lineas_horas = []
for h in range(24):
    cant = int(fraudes_por_hora[h])
    lineas_horas.append("  %02d:00h -> %d fraudes" % (h, cant))
dist_horas = "\n".join(lineas_horas)

# -- Muestra real del dataset -----------------------------
cols = ["Time", "V1", "V4", "V10", "V12", "V14", "V17", "Amount", "Class"]
muestra = (
    pd.concat(
        [
            df[df["Class"] == 1][cols].head(50),
            df[df["Class"] == 0][cols].head(150),
        ]
    )
    .sample(frac=1, random_state=42)
    .reset_index(drop=True)
)
muestra["hora"] = (muestra["Time"] / 3600 % 24).round(1)
muestra = muestra.drop(columns=["Time"])
muestra_txt = muestra.round(3).to_string(index=True)

print("=" * 55)
print("  FRAUDBOT - Mini-RAG con DeepSeek")
print("=" * 55)
print("  Dataset: %s | %d fraudes (%.2f%%)" % (csv, fraudes, pct))
print("  Hora pico de fraude: %02d:00h (%d fraudes)" % (hora_pico, pico_cant))
print("  Enviando 200 filas reales a DeepSeek...")
print("=" * 55)

# -- System prompt ----------------------------------------
SYSTEM_PROMPT = (
    "Eres FraudBot, analista de fraude de un banco dominicano.\n"
    "Tienes acceso a una muestra REAL del dataset. No inventes numeros.\n\n"
    "ESTADISTICAS DEL DATASET (%s):\n" % csv
    + "- %s transacciones | %d fraudes (%.2f%%)\n" % (format(total, ","), fraudes, pct)
    + "- Ratio: %d:1 (legitimas vs fraudes)\n" % ratio
    + "- Monto promedio fraude: $%.2f | legitima: $%.2f\n" % (amt_fraud, amt_leg)
    + "- Fraude maximo: $%.2f | minimo: $%.2f\n" % (fraude_max, fraude_min)
    + "- Hora pico de fraude: %02d:00h (%d fraudes)\n\n" % (hora_pico, pico_cant)
    + "DISTRIBUCION POR HORA (los %d fraudes):\n" % fraudes
    + dist_horas
    + "\n\n"
    + "MUESTRA REAL DE 200 FILAS (50 fraudes + 150 legitimas):\n"
    "Columnas: hora, V1,V4,V10,V12,V14,V17(patrones PCA), Amount, Class\n"
    "NOTA: V14 y V17 muy negativos = senal fuerte de fraude.\n\n" + muestra_txt + "\n\n"
    "Responde en espanol con los datos reales. Max 4 parrafos."
)

# -- Chat -------------------------------------------------
historial = []


def preguntar(pregunta):
    print("\n  Pregunta: " + pregunta)
    print("  " + "-" * 51)
    historial.append({"role": "user", "content": pregunta})
    r = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + historial,
        max_tokens=600,
        temperature=0.3,
    )
    respuesta = r.choices[0].message.content
    historial.append({"role": "assistant", "content": respuesta})
    print("  FraudBot: " + respuesta + "\n")
    return respuesta


print("\n  Iniciando preguntas...\n")

# 1. Horario con mas fraudes
preguntar(
    "En que horarios del dia ocurren mas fraudes segun el dataset? "
    "Dame los rangos de hora con mas actividad fraudulenta "
    "y cuantos fraudes hay en cada uno."
)

# 2. Patron de montos
preguntar(
    "Analiza los montos de los fraudes vs transacciones legitimas. "
    "El fraude promedio es $%.2f pero hay desde $%.2f hasta $%.2f. "
    "Que patron ves y por que los fraudsters no siempre roban lo maximo?"
    % (amt_fraud, fraude_min, fraude_max)
)

# 3. Impacto en dinero real
preguntar(
    "Si el modelo no detecta el 16%% de los %d fraudes del dataset "
    "y el monto promedio es $%.2f, cuanto dinero pierde el banco? "
    "Explica el impacto en terminos simples para alguien que no sabe de tecnologia."
    % (fraudes, amt_fraud)
)

print("=" * 55)
print("  Fin. Agrega mas preguntar() para seguir explorando.")
print("=" * 55)
