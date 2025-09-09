import streamlit as st
import os, json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# 🚨 Configuración rápida de API Key (solo para pruebas)
import streamlit as st
import os
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Cargar SIGC
sigc_path = "sigc_tapas.md"
try:
    with open(sigc_path, "r", encoding="utf-8") as f:
        sigc_text = f.read()
except FileNotFoundError:
    st.error(f"⚠️ No se encontró el archivo {sigc_path}.")
    st.stop()

# Inicializar modelo GPT
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Prompt template
template = """
Eres un asistente virtual de calidad basado en un Sistema Integrado de Gestión de Calidad (SIGC).

Documento de referencia:
{sigc}

Consulta:
{question}

Responde solo con base en el SIGC, de forma clara y práctica.
Si la consulta no está en el SIGC, responde: "⚠️ Esa información no está en el SIGC".
"""

prompt = PromptTemplate(
    input_variables=["sigc", "question"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# Interfaz Streamlit
st.title("🤖 Asistente Virtual - Calidad de Tapas")

# Mostrar último resultado de app.py (si existe)
if os.path.exists("ultimo_resultado.json"):
    with open("ultimo_resultado.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        resultado = data.get("resultado", None)
        if resultado:
            st.info(f"📌 Última clasificación detectada: **{resultado}**")
            
            # Pregunta automática al SIGC
            consulta_auto = f"La tapa fue clasificada como {resultado}. ¿Qué acciones recomienda el SIGC?"
            respuesta_auto = chain.run(sigc=sigc_text, question=consulta_auto)
            st.success(f"🔎 Recomendación automática:\n\n{respuesta_auto}")

# Chat manual con el SIGC
st.write("### 💬 Haz una pregunta al SIGC")
user_q = st.text_area("Escribe tu consulta:")

if st.button("Preguntar"):
    if user_q.strip():
        response = chain.run(sigc=sigc_text, question=user_q)
        st.success(response)
    else:
        st.warning("Por favor escribe una pregunta antes de continuar.")
