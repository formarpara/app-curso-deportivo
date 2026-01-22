import streamlit as st
import google.generativeai as genai
import json
import os

# 1. SEGURIDAD
if 'usuario_logueado' not in st.session_state or not st.session_state['usuario_logueado']:
    st.warning("🔒 Debes iniciar sesión en la página principal.")
    st.stop()

# 2. CONFIGURACIÓN
TITULO_TEMA = "Módulo 1: Fundamentos Tácticos"
ARCHIVO_PDF = "tema1.pdf"

st.title(TITULO_TEMA)

# 3. PDF
if os.path.exists(ARCHIVO_PDF):
    with open(ARCHIVO_PDF, "rb") as f:
        st.sidebar.download_button("📄 Descargar PDF", f, file_name=ARCHIVO_PDF)

# 4. IA (Cerebro)
try:
    # AQUÍ ESTABA EL ERROR: Ahora está en inglés correcto
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

# 5. INTERFAZ
st.info("🤖 Tu entrenador virtual está listo.")
duda = st.text_input("¿Qué duda tienes?")

if st.button("Generar Clase"):
    if duda:
        with st.spinner("Analizando..."):
            try:
                prompt = f"""
                Act as a sports tutor. Topic: {TITULO_TEMA}. User doubt: {duda}.
                Reply in strict JSON:
                {{
                 "conceptos": ["c1", "c2", "c3", "c4", "c5"],
                 "explicacion": "detailed explanation in Spanish...",
                 "quiz": [
                   {{"pregunta": "...", "tipo": "seleccion", "opciones": ["A","B","C"], "correcta": "A"}},
                   {{"pregunta": "...", "tipo": "fv", "opciones": ["Verdadero","Falso"], "correcta": "Verdadero"}},
                   {{"pregunta": "...", "tipo": "completar", "opciones": [], "correcta": "texto"}}
                 ],
                 "reflexion": "reflection in Spanish..."
                }}
                Ensure the quiz has exactly 9 questions.
                """
                response = model.generate_content(prompt)
                text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(text)

                st.subheader("Conceptos")
                for c in data['conceptos']: st.success(c)
                
                st.subheader("Explicación")
                st.write(data['explicacion'])
                
                st.subheader("Evaluación")
                # Lógica simple de visualización
                for q in data['quiz']:
                    st.write(f"**{q['pregunta']}**")
                    st.caption(f"Tipo: {q['tipo']}")

            except Exception as e:
                st.error(f"Error en la IA: {e}")
