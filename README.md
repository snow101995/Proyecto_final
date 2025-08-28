# 🚀 Proyecto Streamlit - Inspección de Tapas + Chatbot RAG

Este repositorio contiene:
- **Detector YOLO** para inspección visual de tapas.
- **Chatbot con RAG** que responde únicamente en base al manual cargado.
- **Manual de inspección** accesible desde la app.

## 📂 Estructura
- `app.py` → Entrada principal de Streamlit
- `chatbot.py` → Lógica del chatbot con RAG
- `data/manual_tapas.md` → Manual cargado al RAG
- `models/best.pt` → Pesos de YOLO
- `utils/gradcam.py` → Funciones auxiliares

## ▶️ Cómo ejecutar
```bash
pip install -r requirements.txt
streamlit run app.py
