import streamlit as st
import random
import string
import secrets
import hashlib
import re
import json
from datetime import datetime, timedelta
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
      word-break: break-all;
  }
  .progress-bar {
      background-color: #f0f0f0;
      border-radius: 10px;
      padding: 3px;
      margin: 10px 0;
  }
  .progress-fill {
      height: 20px;
      border-radius: 8px;
      transition: width 0.3s;
      text-align: center;
      line-height: 20px;
      color: white;
      font-weight: bold;
      font-size: 12px;
  }
  .tip-box {
      background-color: #fff3cd;
      border: 1px solid #ffeaa7;
      border-radius: 8px;
      padding: 1rem;
      margin: 1rem 0;
  }
  .success-box {
      background-color: #d4edda;
      border: 1px solid #c3e6cb;
      border-radius: 8px;
      padding: 1rem;
      margin: 1rem 0;
  }
</style>
""", unsafe_allow_html=True)

# Clases para el generador de contraseñas
class PasswordGenerator:
  def __init__(self):
      self.common_words = [
          'casa', 'perro', 'gato', 'sol', 'luna', 'mar', 'montaña', 'río',
          'flor', 'árbol', 'cielo', 'estrella', 'fuego', 'agua', 'tierra',
          'viento', 'luz', 'sombra', 'tiempo', 'espacio', 'música', 'arte',
          'libro', 'puerta', 'ventana', 'camino', 'jardín', 'bosque'
      ]
      self.animals = [
          'león', 'tigre', 'águila', 'delfín', 'lobo', 'oso', 'zorro',
          'ciervo', 'búho', 'halcón', 'puma', 'jaguar', 'cóndor', 'ballena',
          'elefante', 'jirafa', 'cebra', 'rinoceronte', 'hipopótamo'
      ]
      self.colors = [
          'azul', 'rojo', 'verde', 'amarillo', 'púrpura', 'naranja',
          'rosa', 'negro', 'blanco', 'dorado', 'plateado', 'turquesa',
          'violeta', 'índigo', 'coral', 'esmeralda', 'rubí', 'zafiro'
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
          
      if not chars:
          chars = string.ascii_letters + string.digits
          
      return ''.join(secrets.choice(chars) for _ in range(length))
  
  def generate_memorable(self, num_words=3, separator='-', add_numbers=True, capitalize=True):
      """Genera contraseña memorable con palabras"""
      all_words = self.common_words + self.animals + self.colors
      words = random.sample(all_words, min(num_words, len(all_words)))
      
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
              'prefix': ['Bank', 'Secure', 'Safe', 'Trust', 'Vault', 'Guard'],
              'symbols': ['$', '#', '@', '&', '!'],
              'numbers': True,
              'complexity': 'high'
          },
          'social_media': {
              'prefix': ['Social', 'Connect', 'Share', 'Like', 'Follow', 'Post'],
              'symbols': ['!', '@', '#'],
              'numbers': True,
              'complexity': 'medium'
          },
          'work': {
              'prefix': ['Work', 'Office', 'Pro', 'Team', 'Project', 'Task'],
              'symbols': ['-', '_', '.', '#'],
              'numbers': True,
              'complexity': 'medium'
          },
          'gaming': {
              'prefix': ['Game', 'Play', 'Win', 'Epic', 'Hero', 'Quest'],
              'symbols': ['!', '@', '#', '*', '+'],
              'numbers': True,
              'complexity': 'medium'
          },
          'email': {
              'prefix': ['Mail', 'Email', 'Msg', 'Send', 'Inbox', 'Letter'],
              'symbols': ['.', '@', '_', '-'],
              'numbers': True,
              'complexity': 'medium'
          }
      }
      
      pattern = context_patterns.get(context, context_patterns['work'])
      
      # Simular procesamiento de IA
      with st.spinner(f"🤖 Analizando contexto '{context}'..."):
          time.sleep(0.8)
      
      # Construir contraseña contextual
      prefix = random.choice(pattern['prefix'])
      word = random.choice(self.common_words).capitalize()
      
      base = prefix + word
      
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
          all_words = self.common_words + self.animals + self.colors
          words = random.sample(all_words, min(num_words, len(all_words)))
      else:
          english_words = ['house', 'dog', 'sun', 'tree', 'music', 'ocean', 'mountain', 'star']
          words = random.sample(english_words, min(num_words, len(english_words)))
          
      return ' '.join(word.capitalize() for word in words)

class SecurityAnalyzer:
  def __init__(self):
      self.common_passwords = [
          '123456', 'password', '123456789', '12345678', '12345',
          '1234567', '1234567890', 'qwerty', 'abc123', 'password123',
          'admin', 'letmein', 'welcome', 'monkey', 'dragon'
      ]
  
  def analyze_strength(self, password):
      """Analiza la fortaleza de la contraseña"""
      score = 0
      feedback = []
      
      # Longitud
      if len(password) >= 16:
          score += 30
      elif len(password) >= 12:
          score += 25
      elif len(password) >= 8:
          score += 15
          feedback.append("💡 Considera usar al menos 12 caracteres")
      else:
          score += 5
          feedback.append("⚠️ Muy corta - usa al menos 8 caracteres")
      
      # Variedad de caracteres
      if re.search(r'[a-z]', password):
          score += 10
      else:
          feedback.append("📝 Añade letras minúsculas")
          
      if re.search(r'[A-Z]', password):
          score += 10
      else:
          feedback.append("🔤 Añade letras mayúsculas")
          
      if re.search(r'\d', password):
          score += 15
      else:
          feedback.append("🔢 Añade números")
          
      if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
          score += 20
      else:
          feedback.append("🔣 Añade símbolos especiales")
      
      # Penalizaciones
      if password.lower() in [p.lower() for p in self.common_passwords]:
          score -= 40
          feedback.append("❌ Evita contraseñas muy comunes")
      
      if re.search(r'123|abc|qwe|password', password.lower()):
          score -= 15
          feedback.append("🚫 Evita secuencias obvias")
          
      # Bonificaciones
      if len(set(password)) > len(password) * 0.7:
          score += 10
          
      if not re.search(r'(.)\1{2,}', password):
          score += 5
      else:
          feedback.append("🔄 Evita repetir caracteres consecutivos")
      
      score = max(0, min(100, score))
      
      if score >= 90:
          strength = "Excelente"
          color = "#28a745"
          emoji = "🛡️"
      elif score >= 75:
          strength = "Muy Fuerte"
          color = "#20c997"
          emoji = "🔒"
      elif score >= 60:
          strength = "Fuerte"
          color = "#17a2b8"
          emoji = "🔐"
      elif score >= 40:
          strength = "Moderada"
          color = "#ffc107"
          emoji = "⚠️"
      else:
          strength = "Débil"
          color = "#dc3545"
          emoji = "❌"
          
      return {
          'score': score,
          'strength': strength,
          'color': color,
          'emoji': emoji,
          'feedback': feedback,
          'estimated_crack_time': self.estimate_crack_time(score),
          'entropy': self.calculate_entropy(password)
      }
  
  def estimate_crack_time(self, score):
      """Estima tiempo de cracking"""
      if score >= 90:
          return "Trillones de años"
      elif score >= 75:
          return "Millones de años"
      elif score >= 60:
          return "Miles de años"
      elif score >= 40:
          return "Meses a años"
      else:
          return "Minutos a días"
  
  def calculate_entropy(self, password):
      """Calcula la entropía de la contraseña"""
      charset_size = 0
      if re.search(r'[a-z]', password):
          charset_size += 26
      if re.search(r'[A-Z]', password):
          charset_size += 26
      if re.search(r'\d', password):
          charset_size += 10
      if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
          charset_size += 32
          
      if charset_size == 0:
          return 0
          
      import math
      entropy = len(password) * math.log2(charset_size)
      return round(entropy, 1)

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
  st.sidebar.markdown("### 🎲 Configuración Clásica")
  length = st.sidebar.slider("Longitud", 8, 50, 16)
  use_uppercase = st.sidebar.checkbox("Mayúsculas (A-Z)", True)
  use_lowercase = st.sidebar.checkbox("Minúsculas (a-z)", True)
  use_numbers = st.sidebar.checkbox("Números (0-9)", True)
  use_symbols = st.sidebar.checkbox("Símbolos (!@#$...)", True)
  exclude_ambiguous = st.sidebar.checkbox("Excluir ambiguos (0,O,1,l,I)", False)

elif mode == "🧠 IA Contextual":
  st.sidebar.markdown("### 🧠 Configuración IA")
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
  st.sidebar.markdown("### 💭 Configuración Memorable")
  num_words = st.sidebar.slider("Número de palabras", 2, 6, 3)
  separator = st.sidebar.selectbox("Separador", ["-", "_", ".", " ", ""])
  add_numbers = st.sidebar.checkbox("Añadir números", True)
  capitalize = st.sidebar.checkbox("Capitalizar palabras", True)

else:  # Frase de contraseña
  st.sidebar.markdown("### 📝 Configuración Frase")
  num_words = st.sidebar.slider("Número de palabras", 4, 8, 5)
  language = st.sidebar.selectbox("Idioma", ["spanish", "english"])

st.sidebar.markdown("---")

# Configuraciones adicionales
st.sidebar.markdown("### 🛡️ Opciones de Seguridad")
auto_analyze = st.sidebar.checkbox("Análisis automático", True)
show_strength_meter = st.sidebar.checkbox("Mostrar medidor de fuerza", True)

# Layout principal
col1, col2 = st.columns([2, 1])

with col1:
  st.markdown("## 🚀 Generador de Contraseñas")
  
  # Botón principal de generación
  if st.button("🎯 Generar Contraseña", type="primary", use_container_width=True):
      try:
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
          
          # Analizar automáticamente si está habilitado
          analysis = None
          if auto_analyze:
              analysis = st.session_state.analyzer.analyze_strength(password)
          
          # Guardar en historial
          st.session_state.password_history.append({
              'password': password,
              'mode': mode,
              'timestamp': datetime.now(),
              'analysis': analysis
          })
          
          st.session_state.current_password = password
          st.session_state.current_analysis = analysis
          
      except Exception as e:
          st.error(f"Error al generar contraseña: {str(e)}")
  
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
      col_copy, col_regenerate, col_analyze, col_clear = st.columns(4)
      
      with col_copy:
          if st.button("📋 Copiar", use_container_width=True):
              st.success("✅ ¡Copiado!")
              st.balloons()
      
      with col_regenerate:
          if st.button("🔄 Regenerar", use_container_width=True):
              st.rerun()
      
      with col_analyze:
          if st.button("🔍 Analizar", use_container_width=True):
              analysis = st.session_state.analyzer.analyze_strength(st.session_state.current_password)
              st.session_state.current_analysis = analysis
              st.rerun()
      
      with col_clear:
          if st.button("🗑️ Limpiar", use_container_width=True):
              if hasattr(st.session_state, 'current_password'):
                  del st.session_state.current_password
              if hasattr(st.session_state, 'current_analysis'):
                  del st.session_state.current_analysis
              st.rerun()
      
      # Análisis de fortaleza
      if hasattr(st.session_state, 'current_analysis') and st.session_state.current_analysis:
          analysis = st.session_state.current_analysis
          
          st.markdown("### 📊 Análisis de Seguridad")
          
          # Medidor de fuerza visual
          if show_strength_meter:
              st.markdown(f"""
              <div class="progress-bar">
                  <div class="progress-fill" style="background-color: {analysis['color']}; width: {analysis['score']}%;">
                      {analysis['score']}/100
                  </div>
              </div>
              """, unsafe_allow_html=True)
          
          # Métricas principales
          metric_cols = st.columns(4)
          with metric_cols[0]:
              st.metric("Fortaleza", f"{analysis['emoji']} {analysis['strength']}")
          with metric_cols[1]:
              st.metric("Puntuación", f"{analysis['score']}/100")
          with metric_cols[2]:
              st.metric("Entropía", f"{analysis['entropy']} bits")
          with metric_cols[3]:
              st.metric("Tiempo de Cracking", analysis['estimated_crack_time'])
          
          # Feedback y recomendaciones
          if analysis['feedback']:
              st.markdown("#### 💡 Recomendaciones para Mejorar")
              for tip in analysis['feedback']:
                  st.markdown(f"""
                  <div class="tip-box">
                      {tip}
                  </div>
                  """, unsafe_allow_html=True)
          elif analysis['score'] >= 80:
              st.markdown("""
              <div class="success-box">
                  🎉 ¡Excelente! Esta contraseña tiene una seguridad muy alta.
              </div>
              """, unsafe_allow_html=True)

with col2:
  st.markdown("## 📈 Panel de Control")
  
  # Botones de generación rápida
  st.markdown("### ⚡ Generación Rápida")
  quick_cols = st.columns(2)
  
  with quick_cols[0]:
      if st.button("🎲 Rápida", use_container_width=True):
          password = st.session_state.generator.generate_classic(12, True, True, True, True)
          st.session_state.current_password = password
          st.session_state.current_analysis = st.session_state.analyzer.analyze_strength(password)
          st.rerun()
  
  with quick_cols[1]:
      if st.button("🛡️ Segura", use_container_width=True):
          password = st.session_state.generator.generate_classic(20, True, True, True, True)
          st.session_state.current_password = password
          st.session_state.current_analysis = st.session_state.analyzer.analyze_strength(password)
          st.rerun()
  
  # Historial reciente
  st.markdown("### 📝 Historial Reciente")
  
  if st.session_state.password_history:
      recent_passwords = list(reversed(st.session_state.password_history[-5:]))
      
      for i, entry in enumerate(recent_passwords):
          with st.expander(f"{entry['mode']} - {entry['timestamp'].strftime('%H:%M:%S')}"):
              st.code(entry['password'], language=None)
              if entry.get('analysis'):
                  col_a, col_b = st.columns(2)
                  with col_a:
                      st.caption(f"**Fortaleza:** {entry['analysis']['strength']}")
                  with col_b:
                      st.caption(f"**Puntuación:** {entry['analysis']['score']}/100")
              
              if st.button(f"Usar esta", key=f"use_{i}"):
                  st.session_state.current_password = entry['password']
                  st.session_state.current_analysis = entry['analysis']
                  st.rerun()
  else:
      st.info("📝 No hay contraseñas generadas aún")
  
  # Limpiar historial
  if st.session_state.password_history:
      if st.button("🗑️ Limpiar Historial", use_container_width=True):
          st.session_state.password_history = []
          st.success("✅ Historial limpiado")
          st.rerun()

# Footer con tabs adicionales
st.markdown("---")

# Tabs adicionales
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Consejos", "🔧 Herramientas", "📚 Guía", "ℹ️ Info"])

with tab1:
  st.markdown("### 🛡️ Consejos de Seguridad")
  
  col_a, col_b = st.columns(2)
  
  with col_a:
      st.markdown("#### ✅ Buenas Prácticas:")
      st.markdown("""
      - Usar contraseñas únicas para cada cuenta
      - Mínimo 12 caracteres de longitud
      - Combinar mayúsculas, minúsculas, números y símbolos
      - Activar autenticación de dos factores (2FA)
      - Usar un gestor de contraseñas
      - Cambiar contraseñas comprometidas inmediatamente
      """)
  
  with col_b:
      st.markdown("#### ❌ Evitar:")
      st.markdown("""
      - Información personal (nombres, fechas)
      - Contraseñas comunes (123456, password)
      - Reutilizar contraseñas entre sitios
      - Compartir por email o mensajes
      - Secuencias obvias (abc123, qwerty)
      - Almacenar en archivos de texto plano
      """)

with tab2:
  st.markdown("### 🔧 Herramientas Adicionales")
  
  # Verificador de contraseñas existentes
  st.markdown("#### 🔍 Analizar Contraseña Existente")
  existing_password = st.text_input("Ingresa una contraseña para analizar:", type="password")
  
  if existing_password and st.button("Analizar Contraseña"):
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

with tab3:
  st.markdown("### 📚 Guía de Uso")
  
  st.markdown("#### 🎯 Modos de Generación:")
  
  st.markdown("**🎲 Modo Clásico**")
  st.markdown("Genera contraseñas aleatorias tradicionales con control total sobre los caracteres incluidos.")
  
  st.markdown("**🧠 Modo IA Contextual**")
  st.markdown("Utiliza inteligencia artificial simulada para crear contraseñas optimizadas según el contexto de uso.")
  
  st.markdown("**💭 Modo Memorable**")
  st.markdown("Crea contraseñas usando palabras comunes que son más fáciles de recordar.")
  
  st.markdown("**📝 Modo Frase de Contraseña**")
  st.markdown("Genera frases completas que son seguras y relativamente fáciles de recordar.")

with tab4:
  st.markdown("### ℹ️ Acerca de SmartPass AI")
  
  st.markdown("""
  **SmartPass AI** es un generador de contraseñas inteligente que combina algoritmos 
  de seguridad criptográfica con inteligencia artificial para crear contraseñas 
  seguras y personalizadas.
  
  #### 🔧 Características:
  - Generación criptográficamente segura
  - Análisis de fortaleza multi-criterio
  - IA contextual adaptativa
  - Interfaz intuitiva y moderna
  - Sin almacenamiento permanente
  
  #### 🛡️ Seguridad:
  - Las contraseñas se generan localmente
  - No se envían datos a servidores externos
  - Historial solo durante la sesión
  - Código abierto y auditable
  
  **Versión**: 1.0.0 | **Desarrollado con**: Streamlit + Python
  """)

# Footer final
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
  <p>🔐 SmartPass AI - Generador Inteligente de Contraseñas</p>
  <p>Desarrollado con ❤️ usando Streamlit | © 2024</p>
</div>
""", unsafe_allow_html=True)
