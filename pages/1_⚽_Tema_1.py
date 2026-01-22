import streamlit as st
import google.generativeai as genai
import json

# 1. VERIFICACIÓN DE SEGURIDAD
if 'usuario_logueado' not in st.session_state or not st.session_state['usuario_logueado']:
    st.warning("🔒 Debes iniciar sesión en la página principal para ver este contenido.")
    st.stop()

st.title("Módulo 1: Fundamentos Tácticos")

# 2. CONFIGURACIÓN DE LA IA (GEMINI)
# Intentamos obtener la clave secreta desde Streamlit
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Falta configurar la API Key en los 'Secrets' de Streamlit.")
    st.stop()

# 3. INTERFAZ DE CONSULTA
st.info("Este módulo cuenta con un Tutor IA. Pregunta sobre el tema y generará una clase única para ti.")

duda_estudiante = st.text_area("¿Qué quieres aprender hoy sobre este tema?", height=100, placeholder="Ejemplo: Explícame la diferencia entre defensa en zona y defensa al hombre.")

# PROMPT DE INGENIERÍA PARA GEMINI
prompt_sistema = """
Eres un profesor experto en deportes. Responde en formato JSON estricto.
Estructura requerida:
{
 "conceptos": ["concepto1", "concepto2", "concepto3", "concepto4", "concepto5"],
 "explicacion": "Texto explicativo detallado...",
 "quiz": [
   {"pregunta": "Pregunta 1...", "tipo": "seleccion", "opciones": ["A", "B", "C"], "correcta": "A"},
   {"pregunta": "Pregunta 2...", "tipo": "fv", "opciones": ["Verdadero", "Falso"], "correcta": "Verdadero"},
   {"pregunta": "Pregunta 3...", "tipo": "completar", "opciones": [], "correcta": "palabra"}
   ... (hasta completar 9 preguntas variadas)
 ],
 "reflexion": "Texto reflexivo final..."
}
Genera contenido educativo de alto nivel.
"""

if st.button("🧠 Generar Clase y Evaluación"):
    if not duda_estudiante:
        st.warning("Por favor escribe tu duda primero.")
    else:
        with st.spinner("El entrenador virtual está analizando tu consulta..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-pro')
                response = model.generate_content(f"{prompt_sistema} La duda del estudiante es: {duda_estudiante}")
                
                # Limpieza del JSON (a veces la IA pone ```json al inicio)
                texto_json = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(texto_json)
                
                # --- A. MOSTRAR TEORÍA ---
                st.header("1. Conceptos Clave")
                cols = st.columns(2)
                for i, concepto in enumerate(data['conceptos']):
                    cols[i % 2].success(f"📌 {concepto}")
                
                st.markdown("### 📖 Explicación Teórica")
                st.write(data['explicacion'])
                
                st.divider()
                
                # --- B. MOSTRAR EVALUACIÓN ---
                st.header("2. Evaluación Dinámica (9 Preguntas)")
                
                # Usamos st.form para que no se recargue la página con cada click
                with st.form("examen_form"):
                    aciertos = 0
                    respuestas_usuario = []
                    
                    for idx, item in enumerate(data['quiz']):
                        st.write(f"**P{idx+1}: {item['pregunta']}**")
                        
                        if item['tipo'] == 'seleccion':
                            res = st.radio(f"Opción:", item['opciones'], key=f"q{idx}", index=None)
                        elif item['tipo'] == 'fv':
                            res = st.radio(f"Opción:", ["Verdadero", "Falso"], key=f"q{idx}", index=None)
                        else:
                            res = st.text_input("Tu respuesta:", key=f"q{idx}")
                            
                        respuestas_usuario.append(res)
                        st.write("---")
                    
                    submitted = st.form_submit_button("Calificar Examen")
                    
                    if submitted:
                        st.subheader("Resultados:")
                        score = 0
                        for i, (user_res, item) in enumerate(zip(respuestas_usuario, data['quiz'])):
                            # Normalizamos texto para comparar
                            val_user = str(user_res).strip().lower() if user_res else ""
                            val_correct = str(item['correcta']).strip().lower()
                            
                            if val_user == val_correct:
                                score += 1
                                st.success(f"✅ P{i+1} Correcta")
                            else:
                                st.error(f"❌ P{i+1} Incorrecta. Era: {item['correcta']}")
                        
                        st.metric(label="Calificación Final", value=f"{score}/9")

                st.divider()
                st.header("3. Reflexión Final")
                st.info(data['reflexion'])

            except Exception as e:
                st.error(f"Error conectando con la IA. Intenta de nuevo. Detalle: {e}")
