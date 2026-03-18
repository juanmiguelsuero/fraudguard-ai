# 🛡️ Sistema Inteligente de Detección de Fraude

Aplicación web con Streamlit + RandomForest para detección de fraude en tarjetas de crédito.

## 📁 Estructura del proyecto

```
/proyecto
├── train_model.py      ← Entrena y guarda el modelo
├── app.py              ← Aplicación Streamlit
├── creditcard.csv      ← Dataset (debes descargarlo de Kaggle)
├── fraud_model.pkl     ← Generado tras entrenar
├── scaler.pkl          ← Generado tras entrenar
└── Logo.png            ← Opcional (tu logo fintech)
```

## ⚙️ Instalación de dependencias

```bash
pip install streamlit scikit-learn pandas numpy
```

## 🚀 Ejecución

### Paso 1 – Entrenar el modelo
```bash
python train_model.py
```
Esto genera `fraud_model.pkl` y `scaler.pkl`.

### Paso 2 – Lanzar la aplicación
```bash
streamlit run app.py
```

## 📊 Dataset

Descarga el dataset desde Kaggle:  
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

Coloca `creditcard.csv` en la misma carpeta que los scripts.

## 🔍 Lógica del simulador

| Parámetro | Efecto |
|-----------|--------|
| Monto | Reemplaza el campo `Amount` de la transacción real |
| Nivel de riesgo (0–100) | Amplifica las variables V1–V28 hasta un factor de 1.5 |
| Tipo "Sospechosa" | Multiplica V14, V12 y V10 por −1.5 |
| Umbral de fraude | 30% de probabilidad |
