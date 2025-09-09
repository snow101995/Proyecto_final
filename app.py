import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os, json

# 🚨 Configuración rápida de API Key (solo pruebas, no producción)
import streamlit as st
import os
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Cargar el modelo entrenado
model_path = "best.pt"
if not os.path.exists(model_path):
    st.error("⚠️ No se encontró 'best.pt'. Asegúrate de haber entrenado el modelo con train.py")
    st.stop()

model = YOLO(model_path)

st.title("🔍 Clasificador de Tapas")
st.write("Sube una imagen de una tapa y el modelo detectará si está **intacta** o **dañada**.")

uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png", "JPG"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Imagen subida", use_column_width=True)

    # Realizar predicción con YOLO
    results = model.predict(image)

    if results and results[0].boxes:
        names = model.names
        annotated_img = results[0].plot()  # Imagen con cajas
        st.image(annotated_img, caption="Resultado", use_column_width=True)

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = names[cls_id]
            st.success(f"👉 La tapa fue detectada como: **{label}**")

            # Guardar resultado en JSON para el asistente_virtual
            with open("ultimo_resultado.json", "w", encoding="utf-8") as f:
                json.dump({"resultado": label}, f, ensure_ascii=False, indent=2)

    else:
        st.warning("No se detectó ninguna tapa en la imagen.")
