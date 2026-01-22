import streamlit as st
import google.generativeai as genai
import json
import os

# --- 1. SEGURIDAD DE ACCESO ---
if 'usuario_logueado' not in st.session_state or not st.session_state['usuario_logueado']:
    st.warning("🔒 Debes iniciar sesión en la página principal para ver este contenido.")
    st.stop()

# ==========================================
# ⚙️ CONFIGURACIÓN DEL TEMA (EDITAR AQUÍ)
# ==========================================
TITULO_TEMA = "Módulo 1: Fundamentos Tácticos"  # <--- Pon el título que quieras
ARCHIVO_PDF = "tema1.pdf"                       # <--- Debe coincidir con el nombre de tu archivo subido
# ==========================================

st.title(TITULO_TEMA)

# --- 2. BOTÓN DE DESCARGA PDF ---
# Buscamos el archivo en la carpeta principal
ruta_pdf = ARCHIVO_PDF 

if os.path.exists(ruta_pdf):
    with open(ruta_pdf, "rb") as pdf_file:
        st.sidebar.download_button(
            label="📄 Descargar Guía de Estudio (PDF)",
            data=pdf_file,
            file_name=ARCHIVO_PDF,
            mime='application/octet-stream'
        )
else:
    st.sidebar.warning(f"⚠️ El archivo '{ARCHIVO_PDF}' no se encuentra cargado en GitHub.")

# --- 3. TUTOR IA (CEREBRO) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Falta configurar la API Key en los Secrets.")
    st.stop()

st.info("💡 Tu entrenador virtual está listo. Haz una pregunta sobre el documento.")

duda = st.text_input("¿Qué duda específica tienes?", placeholder="Ej: Explícame este concepto...")

# Prompt Ingeniería (Instrucciones para la IA)
prompt = f"""
Actúa como un profesor experto en el tema: '{TITULO_TEMA}'.
El estudiante tiene esta duda: '{duda}'.
Responde ESTRICTAMENTE en formato JSON con esta estructura:
{{
 "conceptos": ["concepto1", "concepto2", "concepto3", "concepto4", "concepto5"],
 "explicacion": "explicación detallada y pedagógica...",
 "quiz": [
   {{"pregunta": "...", "tipo": "seleccion", "opciones": ["A","B","C"], "correcta": "A"}},
   {{"pregunta": "...", "tipo": "fv", "opciones": ["Verdadero","Falso"], "correcta": "Verdadero"}},
   {{"pregunta": "...", "tipo": "completar", "opciones": [], "correcta": "palabra"}}
 ] (Genera exactamente 9 preguntas variadas),
 "reflexion": "conclusión crítica final..."
}}
"""

if st.button("🧠 Generar Clase Personalizada"):
    if duda:
        with st.spinner("Analizando táctica y generando ejercicios..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-pro')
                res = model.generate_content(prompt)
                # Limpieza del texto para evitar errores de JSON
                texto_limpio = res.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(texto_limpio)
                
                # A. CONCEPTOS
                st.subheader("1. Conceptos Clave")
                cols = st.columns(2)
                for i, c in enumerate(data['conceptos']):
                    cols[i%2].success(f"📌 {c}")
                
                # B. EXPLICACIÓN
                st.subheader("2. Teoría")
                st.write(data['explicacion'])
                
                st.markdown("---")
                
                # C. EXAMEN
                st.subheader("3. Evaluación (9 Puntos)")
                with st.form("examen"):
                    score = 0
                    for i, q in enumerate(data['quiz']):
                        st.write(f"**P{i+1}. {q['pregunta']}**")
                        if q['tipo'] == 'seleccion':
                            opcion = st.radio("Elige:", q['opciones'], key=f"q{i}", index=None)
                            if opcion == q['correcta']: score += 1
                        elif q['tipo'] == 'fv':
                            opcion = st.radio("¿V o F?", ["Verdadero", "Falso"], key=f"q{i}", index=None)
                            if opcion == q['correcta']: score += 1
                        else:
                            txt = st.text_input("Respuesta:", key=f"q{i}")
                            if str(txt).lower().strip() == str(q['correcta']).lower().strip(): score += 1
                        st.write("---")
                    
                    if st.form_submit_button("Calificar"):
                        st.metric("Tu Nota", f"{score}/9")
                        if score >= 6: st.balloons()
                        else: st.error("Repasa la teoría e intenta de nuevo.")
                
                # D. REFLEXIÓN
                st.subheader("4. Reflexión Final")
                st.info(data['reflexion'])

            except Exception as e:
                st.error(f"Error conectando con el tutor: {e}")
    else:
        st.warning("Por favor escribe tu duda primero.")
