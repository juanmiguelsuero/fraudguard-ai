"""
crear_mini_dataset.py
─────────────────────
Crea creditcard_mini.csv con 50,000 filas:
  - Todos los 492 fraudes originales
  - 49,508 transacciones legítimas aleatorias
  - Misma estructura que creditcard.csv
  - Listo para subir a GitHub (< 10MB)

Ejecutar:
    python crear_mini_dataset.py
"""

import pandas as pd
import numpy as np
import os

print("=" * 55)
print("  Creador de Mini Dataset — FraudGuard AI")
print("=" * 55)

# ── Verificar que existe el CSV original ──────────────────
if not os.path.exists("creditcard.csv"):
    print("❌ No se encontró creditcard.csv en esta carpeta.")
    print("   Descárgalo primero desde:")
    print("   drive.google.com/uc?export=download&id=1Q0521PVFO5ZTJ8LOhLTchAwMHbXsfMRu")
    exit(1)

# ── Cargar dataset completo ───────────────────────────────
print("\n📂 Cargando creditcard.csv...")
df = pd.read_csv("creditcard.csv")
print(f"   Dataset completo: {len(df):,} filas")
print(f"   Fraudes: {df['Class'].sum()} ({df['Class'].mean()*100:.4f}%)")
print(f"   Legítimas: {(df['Class']==0).sum():,}")

# ── Crear muestra de 50,000 filas ─────────────────────────
print("\n✂️  Creando muestra de 50,000 filas...")

# Todos los fraudes (492) + muestrear legítimas
fraudes = df[df["Class"] == 1]  # 492 fraudes
legitimas = df[df["Class"] == 0].sample(49508, random_state=42)  # 49,508 legítimas

# Combinar y mezclar
mini = (
    pd.concat([fraudes, legitimas])
    .sample(frac=1, random_state=42)
    .reset_index(drop=True)
)

# ── Verificar resultado ───────────────────────────────────
print(f"\n✅ Mini dataset creado:")
print(f"   Total filas:  {len(mini):,}")
print(f"   Fraudes:      {mini['Class'].sum()} ({mini['Class'].mean()*100:.4f}%)")
print(f"   Legítimas:    {(mini['Class']==0).sum():,}")
print(f"   Columnas:     {list(mini.columns)}")

# ── Guardar ───────────────────────────────────────────────
output = "creditcard_mini.csv"
print(f"\n💾 Guardando como {output}...")
mini.to_csv(output, index=False)

size_mb = os.path.getsize(output) / (1024 * 1024)
print(f"   Tamaño: {size_mb:.1f} MB")
print(f"\n🎉 Listo. Ahora corre:")
print(f"   git add creditcard_mini.csv")
print(f"   git commit -m 'add mini dataset'")
print(f"   git push")
print("=" * 55)
