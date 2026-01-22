import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Academia Deportiva", page_icon="⚽", layout="wide")

# Estilos CSS para que se vea elegante
st.markdown("""
    <style>
    .stButton>button {width: 100%; border-radius: 5px; background-color: #004d40; color: white;}
    .titulo {font-size: 50px; font-weight: bold; color: #004d40; text-align: center;}
    .subtitulo {font-size: 20px; color: #555; text-align: center; margin-bottom: 30px;}
    </style>
""", unsafe_allow_html=True)

# Título Principal
st.markdown('<div class="titulo">CURSO DE ALTO RENDIMIENTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Plataforma de Formación Táctica y Estratégica</div>', unsafe_allow_html=True)

# Gestión de Sesión (Login simple)
if 'usuario_logueado' not in st.session_state:
    st.session_state['usuario_logueado'] = False

col1, col2 = st.columns([1, 1])

with col1:
    st.image("https://images.unsplash.com/photo-1517466787929-bc90951d0974?q=80&w=800", caption="Metodología Profesional")
    st.info("👈 Si ya iniciaste sesión, despliega el menú lateral (arriba a la izquierda) para ver los Temas.")

with col2:
    if not st.session_state['usuario_logueado']:
        st.header("🔐 Acceso a Estudiantes")
        st.write("Ingresa tu correo para desbloquear los contenidos.")
        
        email = st.text_input("Correo electrónico")
        # Aquí podrías poner una contraseña real más adelante
        if st.button("Ingresar al Curso"):
            if email:
                st.session_state['usuario_logueado'] = True
                st.session_state['email_usuario'] = email
                st.success(f"¡Bienvenido/a! Ahora tienes acceso a los módulos en el menú lateral.")
                st.rerun()
            else:
                st.error("Por favor escribe un correo.")
    else:
        st.success(f"✅ Sesión activa para: {st.session_state.get('email_usuario')}")
        st.write("Navega por los temas usando el menú lateral (sidebar).")
        if st.button("Cerrar Sesión"):
            st.session_state['usuario_logueado'] = False
            st.rerun()
