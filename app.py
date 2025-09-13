import streamlit as st
import random
import string
import secrets
import hashlib
import re
import requests
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

# Configuración de la página
st.set_page_config(
  page_title="🔐 SmartPass AI",
  page_icon="🔐",
  layout="wide",
  initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
  .main-header {
      text-align: center;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
      padding: 2rem;
      border-radius: 10px;
      margin-bottom: 2rem;
      color: white;
  }
  .password-display {
      background-color: #f0f2f6;
      padding: 1rem;
      border-radius: 8px;
      border-left: 4px solid #667eea;
      font-family: 'Courier New', monospace;
      font-size: 1.2rem;
      margin: 1rem 0;
  }
  .strength-meter {
      height: 20px;
      border-radius: 10px;
      margin: 10px 0;
  }
  .metric-card {
      background-color: white;
      padding: 1rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      text-align: center;
  }
  .sidebar-section {
      background-color: #f8f9fa;
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 1rem;
  }
</style>
""", unsafe_allow_html=True)

# Clases para el generador de contraseñas
class PasswordGenerator:
  def __init__(self):
      self.common_words = [
          'casa', 'perro', 'gato', 'sol', 'luna', 'mar', 'montaña', 'río',
          'flor', 'árbol', 'cielo', 'estrella', 'fuego', 'agua', 'tierra',
          'viento', 'luz', 'sombra', 'tiempo', 'espacio', 'música', 'arte'
      ]
      self.animals = [
          'león', 'tigre', 'águila', 'delfín', 'lobo', 'oso', 'zorro',
          'ciervo', 'búho', 'halcón', 'puma', 'jaguar', 'cóndor'
      ]
      self.colors = [
          'azul', 'rojo', 'verde', 'amarillo', 'púrpura', 'naranja',
          'rosa', 'negro', 'blanco', 'dorado', 'plateado', 'turquesa'
      ]
      
  def generate_classic(self, length=12, use_uppercase=True, use_lowercase=True, 
                      use_numbers=True, use_symbols=True, exclude_ambiguous=False):
      """Genera contraseña clásica aleatoria"""
      chars = ""
      if use_lowercase:
          chars += string.ascii_lowercase
      if use_uppercase:
          chars += string.ascii_uppercase
      if use_numbers:
          chars += string.digits
      if use_symbols:
          chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
          
      if exclude_ambiguous:
          ambiguous = "0O1lI|"
          chars = ''.join(c for c in chars if c not in ambiguous)
          
      return ''.join(secrets.choice(chars) for _ in range(length))
  
  def generate_memorable(self, num_words=3, separator='-', add_numbers=True, capitalize=True):
      """Genera contraseña memorable con palabras"""
      words = random.sample(self.common_words + self.animals + self.colors, num_words)
      
      if capitalize:
          words = [word.capitalize() for word in words]
          
      password = separator.join(words)
      
      if add_numbers:
          password += separator + str(random.randint(1000, 9999))
          
      return password
  
  def generate_contextual(self, context, length=14):
      """Genera contraseña según contexto usando 'IA simulada'"""
      context_patterns = {
          'banking': {
              'prefix': ['Bank', 'Secure', 'Safe', 'Trust'],
              'symbols': ['$', '#', '@', '&'],
              'numbers': True,
              'complexity': 'high'
          },
          'social_media': {
              'prefix': ['Social', 'Connect', 'Share', 'Like'],
              'symbols': ['!', '@', '#'],
              'numbers': True,
              'complexity': 'medium'
          },
          'work': {
              'prefix': ['Work', 'Office', 'Pro', 'Team'],
              'symbols': ['-', '_', '.'],
              'numbers': True,
              'complexity': 'medium'
          },
          'gaming': {
              'prefix': ['Game', 'Play', 'Win', 'Epic'],
              'symbols': ['!', '@', '#', '*'],
              'numbers': True,
              'complexity': 'medium'
          },
          'email': {
              'prefix': ['Mail', 'Email', 'Msg', 'Send'],
              'symbols': ['.', '@', '_'],
              'numbers': True,
              'complexity': 'medium'
          }
      }
      
      pattern = context_patterns.get(context, context_patterns['work'])
      prefix = random.choice(pattern['prefix'])
      
      # Simular procesamiento de IA
      time.sleep(0.5)  # Simular tiempo de procesamiento
      
      base = prefix + random.choice(self.common_words).capitalize()
      
      if pattern['numbers']:
          base += str(random.randint(100, 999))
          
      base += random.choice(pattern['symbols'])
      base += str(datetime.now().year)
      
      # Ajustar longitud
      while len(base) < length:
          base += random.choice(string.ascii_letters + string.digits)
          
      return base[:length]
  
  def generate_passphrase(self, num_words=5, language='spanish'):
      """Genera frase de contraseña"""
      if language == 'spanish':
          words = random.sample(self.common_words + self.animals + self.colors, num_words)
      else:
          words = ['house', 'dog', 'sun', 'tree', 'music'][:num_words]
          
      return ' '.join(word.capitalize() for word in words)

class SecurityAnalyzer:
  def __init__(self):
      self.common_passwords = [
          '123456', 'password', '123456789', '12345678', '12345',
          '1234567', '1234567890', 'qwerty', 'abc123', 'password123'
      ]
  
  def analyze_strength(self, password):
      """Analiza la fortaleza de la contraseña"""
      score = 0
      feedback = []
      
      # Longitud
      if len(password) >= 12:
          score += 25
      elif len(password) >= 8:
          score += 15
          feedback.append("Considera usar al menos 12 caracteres")
      else:
          feedback.append("Muy corta - usa al menos 8 caracteres")
      
      # Variedad de caracteres
      if re.search(r'[a-z]', password):
          score += 15
      else:
          feedback.append("Añade letras minúsculas")
          
      if re.search(r'[A-Z]', password):
          score += 15
      else:
          feedback.append("Añade letras mayúsculas")
          
      if re.search(r'\d', password):
          score += 15
      else:
          feedback.append("Añade números")
          
      if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
          score += 20
      else:
          feedback.append("Añade símbolos especiales")
      
      # Patrones comunes
      if password.lower() in [p.lower() for p in self.common_passwords]:
          score -= 30
          feedback.append("Evita contraseñas comunes")
      
      # Secuencias
      if re.search(r'123|abc|qwe', password.lower()):
          score -= 10
          feedback.append("Evita secuencias obvias")
      
      score = max(0, min(100, score))
      
      if score >= 80:
          strength = "Muy Fuerte"
          color = "#28a745"
      elif score >= 60:
          strength = "Fuerte"
          color = "#17a2b8"
      elif score >= 40:
          strength = "Moderada"
          color = "#ffc107"
      else:
          strength = "Débil"
          color = "#dc3545"
          
      return {
          'score': score,
          'strength': strength,
          'color': color,
          'feedback': feedback,
          'estimated_crack_time': self.estimate_crack_time(score)
      }
  
  def estimate_crack_time(self, score):
      """Estima tiempo de cracking"""
      if score >= 80:
          return "Siglos"
      elif score >= 60:
          return "Décadas"
      elif score >= 40:
          return "Años"
      else:
          return "Días/Semanas"

# Inicializar objetos
if 'generator' not in st.session_state:
  st.session_state.generator = PasswordGenerator()
if 'analyzer' not in st.session_state:
  st.session_state.analyzer = SecurityAnalyzer()
if 'password_history' not in st.session_state:
  st.session_state.password_history = []

# Header principal
st.markdown("""
<div class="main-header">
  <h1>🔐 SmartPass AI</h1>
  <h3>Generador Inteligente de Contraseñas</h3>
  <p>Crea contraseñas seguras y personalizadas con inteligencia artificial</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Configuración
st.sidebar.markdown("## ⚙️ Configuración")

# Selector de modo
mode = st.sidebar.selectbox(
  "🎯 Modo de Generación",
  ["🎲 Clásico", "🧠 IA Contextual", "💭 Memorable", "📝 Frase de Contraseña"]
)

st.sidebar.markdown("---")

# Configuraciones específicas según el modo
if mode == "🎲 Clásico":
  st.sidebar.markdown("### Configuración Clásica")
  length = st.sidebar.slider("Longitud", 8, 50, 16)
  use_uppercase = st.sidebar.checkbox("Mayúsculas", True)
  use_lowercase = st.sidebar.checkbox("Minúsculas", True)
  use_numbers = st.sidebar.checkbox("Números", True)
  use_symbols = st.sidebar.checkbox("Símbolos", True)
  exclude_ambiguous = st.sidebar.checkbox("Excluir caracteres ambiguos (0, O, 1, l, I)")

elif mode == "🧠 IA Contextual":
  st.sidebar.markdown("### Configuración IA")
  context = st.sidebar.selectbox(
      "Contexto de Uso",
      ["banking", "social_media", "work", "gaming", "email"]
  )
  length = st.sidebar.slider("Longitud", 10, 30, 16)
  
  # Información del contexto
  context_info = {
      "banking": "🏦 Máxima seguridad para servicios financieros",
      "social_media": "📱 Optimizada para redes sociales",
      "work": "💼 Profesional y fácil de escribir",
      "gaming": "🎮 Creativa para plataformas de juegos",
      "email": "📧 Balanceada para correo electrónico"
  }
  st.sidebar.info(context_info[context])

elif mode == "💭 Memorable":
  st.sidebar.markdown("### Configuración Memorable")
  num_words = st.sidebar.slider("Número de palabras", 2, 6, 3)
  separator = st.sidebar.selectbox("Separador", ["-", "_", ".", " "])
  add_numbers = st.sidebar.checkbox("Añadir números", True)
  capitalize = st.sidebar.checkbox("Capitalizar palabras", True)

else:  # Frase de contraseña
  st.sidebar.markdown("### Configuración Frase")
  num_words = st.sidebar.slider("Número de palabras", 4, 8, 5)
  language = st.sidebar.selectbox("Idioma", ["spanish", "english"])

st.sidebar.markdown("---")

# Configuraciones adicionales
st.sidebar.markdown("### 🛡️ Seguridad")
auto_analyze = st.sidebar.checkbox("Análisis automático", True)
show_strength_meter = st.sidebar.checkbox("Mostrar medidor de fuerza", True)

# Layout principal
col1, col2 = st.columns([2, 1])

with col1:
  st.markdown("## 🚀 Generador de Contraseñas")
  
  # Botón principal de generación
  if st.button("🎯 Generar Contraseña", type="primary", use_container_width=True):
      with st.spinner("🤖 Generando contraseña inteligente..."):
          if mode == "🎲 Clásico":
              password = st.session_state.generator.generate_classic(
                  length, use_uppercase, use_lowercase, use_numbers, 
                  use_symbols, exclude_ambiguous
              )
          elif mode == "🧠 IA Contextual":
              password = st.session_state.generator.generate_contextual(context, length)
          elif mode == "💭 Memorable":
              password = st.session_state.generator.generate_memorable(
                  num_words, separator, add_numbers, capitalize
              )
          else:  # Frase de contraseña
              password = st.session_state.generator.generate_passphrase(num_words, language)
          
          # Guardar en historial
          st.session_state.password_history.append({
              'password': password,
              'mode': mode,
              'timestamp': datetime.now(),
              'analysis': st.session_state.analyzer.analyze_strength(password) if auto_analyze else None
          })
          
          st.session_state.current_password = password
  
  # Mostrar contraseña generada
  if hasattr(st.session_state, 'current_password'):
      st.markdown("### 🔑 Contraseña Generada")
      
      # Display de la contraseña
      st.markdown(f"""
      <div class="password-display">
          <strong>{st.session_state.current_password}</strong>
      </div>
      """, unsafe_allow_html=True)
      
      # Botones de acción
      col_copy, col_regenerate, col_analyze = st.columns(3)
      
      with col_copy:
          if st.button("📋 Copiar", use_container_width=True):
              st.success("¡Contraseña copiada al portapapeles!")
      
      with col_regenerate:
          if st.button("🔄 Regenerar", use_container_width=True):
              st.rerun()
      
      with col_analyze:
          if st.button("🔍 Analizar", use_container_width=True):
              analysis = st.session_state.analyzer.analyze_strength(st.session_state.current_password)
              st.session_state.current_analysis = analysis
      
      # Análisis de fortaleza
      if auto_analyze or hasattr(st.session_state, 'current_analysis'):
          if not hasattr(st.session_state, 'current_analysis'):
              st.session_state.current_analysis = st.session_state.analyzer.analyze_strength(st.session_state.current_password)
          
          analysis = st.session_state.current_analysis
          
          st.markdown("### 📊 Análisis de Seguridad")
          
          # Medidor de fuerza
          if show_strength_meter:
              progress_html = f"""
              <div style="background-color: #f0f0f0; border-radius: 10px; padding: 3px;">
                  <div style="background-color: {analysis['color']}; width: {analysis['score']}%; 
                       height: 20px; border-radius: 8px; transition: width 0.3s;"></div>
              </div>
              """
              st.markdown(progress_html, unsafe_allow_html=True)
          
          # Métricas
          metric_cols = st.columns(4)
          with metric_cols[0]:
              st.metric("Puntuación", f"{analysis['score']}/100")
          with metric_cols[1]:
              st.metric("Fortaleza", analysis['strength'])
          with metric_cols[2]:
              st.metric("Tiempo de Cracking", analysis['estimated_crack_time'])
          with metric_cols[3]:
              st.metric("Longitud", len(st.session_state.current_password))
          
          # Feedback
          if analysis['feedback']:
              st.markdown("#### 💡 Recomendaciones")
              for tip in analysis['feedback']:
                  st.warning(f"• {tip}")

with col2:
  st.markdown("## 📈 Panel de Control")
  
  # Estadísticas
  if st.session_state.password_history:
      st.markdown("### 📊 Estadísticas")
      
      total_passwords = len(st.session_state.password_history)
      avg_strength = sum(p.get('analysis', {}).get('score', 0) 
                        for p in st.session_state.password_history if p.get('analysis')) / max(1, total_passwords)
      
      st.metric("Total Generadas", total_passwords)
      st.metric("Fortaleza Promedio", f"{avg_strength:.1f}/100")
      
      # Gráfico de fortaleza en el tiempo
      if len(st.session_state.password_history) > 1:
          df_history = pd.DataFrame([
              {
                  'timestamp': p['timestamp'],
                  'strength': p.get('analysis', {}).get('score', 0),
                  'mode': p['mode']
              }
              for p in st.session_state.password_history
              if p.get('analysis')
          ])
          
          if not df_history.empty:
              fig = px.line(df_history, x='timestamp', y='strength', 
                           title='Evolución de Fortaleza',
                           color='mode')
              fig.update_layout(height=300)
              st.plotly_chart(fig, use_container_width=True)
  
  # Historial reciente
  st.markdown("### 📝 Historial Reciente")
  
  if st.session_state.password_history:
      for i, entry in enumerate(reversed(st.session_state.password_history[-5:])):
          with st.expander(f"{entry['mode']} - {entry['timestamp'].strftime('%H:%M')}"):
              st.code(entry['password'])
              if entry.get('analysis'):
                  st.caption(f"Fortaleza: {entry['analysis']['strength']} ({entry['analysis']['score']}/100)")
  else:
      st.info("No hay contraseñas generadas aún")
  
  # Limpiar historial
  if st.button("🗑️ Limpiar Historial", use_container_width=True):
      st.session_state.password_history = []
      st.success("Historial limpiado")

# Footer con información adicional
st.markdown("---")

# Tabs adicionales
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Consejos de Seguridad", "📚 Guía de Uso", "🔧 Herramientas", "ℹ️ Acerca de"])

with tab1:
  st.markdown("""
  ### 🛡️ Mejores Prácticas de Seguridad
  
  #### ✅ Hacer:
  - Usar contraseñas únicas para cada cuenta
  - Activar autenticación de dos factores (2FA)
  - Actualizar contraseñas regularmente
  - Usar un gestor de contraseñas confiable
  - Verificar regularmente si tus cuentas han sido comprometidas
  
  #### ❌ Evitar:
  - Reutilizar contraseñas entre sitios
  - Usar información personal (nombres, fechas)
  - Compartir contraseñas por email o mensajes
  - Usar contraseñas obvias o comunes
  - Almacenar contraseñas en archivos de texto plano
  
  #### 🎯 Recomendaciones por Contexto:
  - **Banca**: Mínimo 16 caracteres, símbolos especiales
  - **Redes Sociales**: Memorable pero segura, 12+ caracteres
  - **Trabajo**: Fácil de escribir, cumplir políticas corporativas
  - **Gaming**: Creativa, evitar información personal
  - **Email**: Muy segura, es la llave a otras cuentas
  """)

with tab2:
  st.markdown("""
  ### 📚 Guía de Uso
  
  #### 🎲 Modo Clásico
  Genera contraseñas aleatorias tradicionales con control total sobre los caracteres incluidos.
  **Ideal para**: Usuarios que prefieren control granular
  
  #### 🧠 Modo IA Contextual
  Utiliza inteligencia artificial simulada para crear contraseñas optimizadas según el contexto de uso.
  **Ideal para**: Diferentes tipos de servicios y plataformas
  
  #### 💭 Modo Memorable
  Crea contraseñas usando palabras comunes que son más fáciles de recordar.
  **Ideal para**: Usuarios que necesitan memorizar sus contraseñas
  
  #### 📝 Modo Frase de Contraseña
  Genera frases completas que son seguras y relativamente fáciles de recordar.
  **Ideal para**: Contraseñas maestras de gestores de contraseñas
  """)

with tab3:
  st.markdown("### 🔧 Herramientas Adicionales")
  
  # Verificador de contraseñas existentes
  st.markdown("#### 🔍 Analizar Contraseña Existente")
  existing_password = st.text_input("Ingresa una contraseña para analizar:", type="password")
  
  if existing_password and st.button("Analizar Contraseña Existente"):
      analysis = st.session_state.analyzer.analyze_strength(existing_password)
      
      col_a, col_b = st.columns(2)
      with col_a:
          st.metric("Puntuación", f"{analysis['score']}/100")
          st.metric("Fortaleza", analysis['strength'])
      with col_b:
          st.metric("Tiempo de Cracking", analysis['estimated_crack_time'])
          st.metric("Longitud", len(existing_password))
      
      if analysis['feedback']:
          st.markdown("**Recomendaciones:**")
          for tip in analysis['feedback']:
              st.warning(f"• {tip}")
  
  # Generador de múltiples contraseñas
  st.markdown("#### 🎯 Generación en Lote")
  batch_count = st.number_input("Cantidad de contraseñas", 1, 10, 3)
  
  if st.button("Generar Lote"):
      st.markdown("**Contraseñas generadas:**")
      for i in range(batch_count):
          password = st.session_state.generator.generate_classic(16, True, True, True, True)
          analysis = st.session_state.analyzer.analyze_strength(password)
          st.code(f"{i+1}. {password} (Fortaleza: {analysis['strength']})")

with tab4:
  st.markdown("""
  ### ℹ️ Acerca de SmartPass AI
  
  **SmartPass AI** es un generador de contraseñas inteligente que combina algoritmos de seguridad 
  criptográfica con inteligencia artificial para crear contraseñas seguras y personalizadas.
  
  #### 🔧 Características Técnicas:
  - **Generación Criptográficamente Segura**: Utiliza el módulo `secrets` de Python
  - **Análisis de Fortaleza**: Evaluación multi-criterio de seguridad
  - **IA Contextual**: Adaptación según el tipo de servicio
  - **Interfaz Intuitiva**: Diseño moderno con Streamlit
  - **Sin Almacenamiento**: Las contraseñas no se guardan permanentemente
  
  #### 🛡️ Seguridad y Privacidad:
  - Las contraseñas se generan localmente en tu navegador
  - No se envían datos a servidores externos
  - El historial se mantiene solo durante la sesión
  - Código abierto y auditable
  
  #### 👨‍💻 Desarrollado por:
  **Tu Nombre** - Especialista en Ciberseguridad
  
  📧 Email: tu-email@ejemplo.com  
  🐙 GitHub: [@tu-usuario](https://github.com/tu-usuario)  
  🔗 LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)
  
  #### 📄 Licencia:
  MIT License - Libre para uso personal y comercial
  
  ---
  
  **Versión**: 1.0.0 | **Última actualización**: Septiembre 2024
  """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
  <p>🔐 SmartPass AI - Generador Inteligente de Contraseñas</p>
  <p>Desarrollado con ❤️ usando Streamlit | © 2024</p>
</div>
""", unsafe_allow_html=True)
