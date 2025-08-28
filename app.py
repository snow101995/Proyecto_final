import os
import pandas as pd
import streamlit as st
from PIL import Image
from openai import OpenAI

# ==============================
# CONFIGURACIÓN API KEY
# ==============================
client = OpenAI(api_key="OPENAI_API_KEY")  
client = OpenAI()

# ==============================
# FUNCIONES AUXILIARES
# ==============================

# Leer manual (RAG)
def load_manual():
    with open("data/manual_tapas.md", "r", encoding="utf-8") as f:
        return f.read()

# Chatbot RAG
def chatbot_rag(user_input, manual_text):
    prompt = f"""
    Responde SOLO en base al siguiente documento:

    {manual_text}

    Pregunta: {user_input}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un experto en control de calidad de tapas."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ==============================
# STREAMLIT APP
# ==============================
st.set_page_config(page_title="Inspección de Tapas", layout="wide")
st.title("🔎 Sistema de Inspección de Tapas")

# Cargar dataset CSV una sola vez
csv_path = "data/jarlids_annots.csv"
df = None
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    st.error(f"No se encontró el archivo `{csv_path}`. Súbelo en la carpeta `data/`.")

# Tabs
tab1, tab2, tab3 = st.tabs(["🤖 Chatbot RAG", "📊 Dataset CSV", "🖼️ Imágenes con etiquetas"])

# ------------------------------
# TAB 1: CHATBOT
# ------------------------------
with tab1:
    st.header("Asistente de inspección (RAG)")
    manual_text = load_manual()
    user_input = st.text_input("Escribe tu consulta sobre las tapas:")
    if st.button("Preguntar"):
        if user_input.strip() != "":
            answer = chatbot_rag(user_input, manual_text)
            st.markdown(f"**Respuesta:** {answer}")
        else:
            st.warning("Por favor, escribe una pregunta.")

# ------------------------------
# TAB 2: DATASET CSV
# ------------------------------
with tab2:
    st.header("Dataset de anotaciones")
    if df is not None:
        st.dataframe(df)
    else:
        st.error("No se pudo cargar el CSV.")

# ------------------------------
# TAB 3: IMÁGENES CON ETIQUETAS
# ------------------------------
with tab3:
    st.header("Galería de imágenes con sus etiquetas")
    img_dir = "data/imagenes"

    if df is not None and os.path.exists(img_dir):
        # Seleccionar una fila del dataset
        selected_row = st.selectbox("Selecciona un registro", df.index)

        # Obtener info de esa fila
        row = df.loc[selected_row]
        filename = row["filename"] if "filename" in df.columns else None
        label = row["label"] if "label" in df.columns else "Etiqueta no encontrada"

        if filename:
            img_path = os.path.join(img_dir, filename)
            if os.path.exists(img_path):
                image = Image.open(img_path)
                st.image(image, caption=f"{filename} | Etiqueta: {label}", use_column_width=True)
            else:
                st.error(f"La imagen `{filename}` no se encontró en la carpeta {img_dir}.")
        else:
            st.warning("El CSV no contiene una columna llamada 'filename'.")
    else:
        st.error("Verifica que existan tanto el CSV como la carpeta `data/imagenes/`.")
