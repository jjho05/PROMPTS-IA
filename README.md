# 🎨🎬 PROMPTS IA - Generador Inteligente de Prompts

> Generador profesional de prompts para herramientas de IA de generación de **imágenes y videos**, potenciado por Gemini 2.5 Flash

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-green.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-orange.svg)](https://ai.google.dev/)

## 📋 Descripción

**PROMPTS IA** es una aplicación de escritorio que utiliza Google Gemini 2.5 Flash para convertir descripciones simples en prompts técnicos y detallados optimizados para herramientas de generación de **imágenes** (Midjourney, DALL-E, Stable Diffusion) y **videos** (Runway, Pika, Sora) con IA.

## ✨ Características Principales

### 🎯 Doble Modo: Imágenes y Videos
- **Modo Imagen**: 4 categorías especializadas para generación de imágenes
- **Modo Video**: 4 categorías especializadas para generación de videos
- Selector intuitivo para cambiar entre modos

### 📜 Historial de Prompts
- Guarda automáticamente todos los prompts generados
- Visualiza tu historial completo con metadata
- Recarga prompts anteriores fácilmente

### 💾 Exportación
- Exporta prompts a archivos de texto formateados
- Incluye toda la metadata (fecha, categoría, estilo, etc.)
- Perfecto para documentar tu trabajo

## 🖼️ Categorías para IMÁGENES

#### 🎭 Transformación de Rostro
- Disfraces y vestuarios
- Cambios de edad
- Cambios de estilo
- Maquillaje y efectos
- Opción de mantener identidad facial

#### 🖼️ Generación desde Cero
- Creación de imágenes completamente nuevas
- Descripciones técnicas detalladas
- Auto-detección de estilo óptimo

#### 🎨 Modificación de Imagen
- Cambio de fondos
- Agregar/eliminar elementos
- Reemplazar objetos
- Integración natural

#### ✨ Efectos Especiales
- Iluminación volumétrica
- Clima y atmósfera
- Hora del día
- Color grading
- Partículas y humo

## 🎬 Categorías para VIDEOS

#### 🎬 Generación desde Cero
- Crear videos desde descripciones de texto
- Especificar movimientos de cámara
- Control de duración flexible
- Múltiples relaciones de aspecto

#### 🖼️➡️🎬 Imagen a Video
- Animar imágenes estáticas
- Movimientos sutiles y naturales
- Preservar calidad de imagen original
- Transiciones suaves

#### ✨ Efectos y Transiciones
- Efectos visuales cinematográficos
- Transiciones fluidas
- Color grading dinámico
- Cambios de iluminación

#### 🎥 Movimientos de Cámara
- Paneo (izquierda/derecha)
- Zoom (acercar/alejar)
- Dolly (avance/retroceso)
- Tracking (seguimiento)
- Control de intensidad

### Parámetros de Video
- ⏱️ **Duración**: Flexible (3s, 5s, 10s, 30s, 1min, personalizado)
- 📐 **Relación de Aspecto**: 16:9, 9:16, 1:1, 4:3
- 🎥 **Movimiento de Cámara**: Estático, Paneo, Zoom, Dolly, Tracking
- 💫 **Intensidad**: Baja, Media, Alta
- 🎨 **Estilos**: Realista, Cinematográfico, Anime, 3D, Artístico

## 🚀 Instalación

### Requisitos Previos

- Python 3.11 o superior
- API Key de Google Gemini
- Sistema Operativo: Windows, macOS o Linux

### Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/jjho05/PROMPTS-IA.git
cd PROMPTS-IA

# Instalar dependencias
pip install -r requirements.txt

# Configurar API Key
echo "TU_API_KEY_AQUI" > api_key.txt

# Ejecutar aplicación
python main.py
```

## 📦 Dependencias

```txt
customtkinter==5.2.0
google-generativeai==0.3.0
```

## 💻 Uso

### Inicio Rápido

1. **Ejecuta** `python main.py`
2. **Selecciona** tipo de medio (Imagen o Video)
3. **Elige** una categoría
4. **Describe** tu idea
5. **Configura** parámetros (duración, movimiento, etc.)
6. **Selecciona** un estilo artístico
7. **Genera** y copia los prompts

### Ejemplo de Uso - Imagen

**Entrada:**
```
Tipo de Medio: 🖼️ Imagen
Categoría: 🎭 Transformación de Rostro
Descripción: Persona con disfraz de superhéroe
Tipo: Disfraz/Vestuario
Mantener identidad: Sí
Estilo: 📸 Realista/Fotográfico
```

**Salida:**
```
POSITIVE:
Retrato fotográfico de persona con disfraz de superhéroe, 
máscara roja y azul cubriendo parte superior del rostro, 
preservando rasgos faciales originales, traje detallado 
con textura de tela, iluminación frontal suave, enfoque 
nítido en rostro, alta resolución, estilo fotorrealista

NEGATIVE:
rostro distorsionado, anatomía facial incorrecta, ojos 
asimétricos, proporciones faciales incorrectas, rostro 
borroso, rasgos deformados, baja calidad, desenfoque
```

### Ejemplo de Uso - Video

**Entrada:**
```
Tipo de Medio: 🎬 Video
Categoría: 🎬 Generación desde Cero
Descripción: Gato caminando por una playa al atardecer
Duración: 5s
Relación de Aspecto: 16:9
Movimiento de Cámara: Paneo (Izq/Der)
Intensidad: Media
Estilo: 🎬 Cinematográfico
```

**Salida:**
```
POSITIVE:
Video de un gato atigrado caminando por una playa al atardecer, 
cámara con paneo lateral suave siguiendo al animal, olas en 
movimiento constante en segundo plano, arena con textura detallada, 
iluminación dorada del atardecer, movimiento fluido y natural, 
duración 5 segundos, aspecto 16:9, estilo cinematográfico realista

NEGATIVE:
movimiento brusco, saltos de frames, parpadeo, glitches, 
movimiento antinatural, cámara inestable, cortes abruptos, 
baja calidad, artefactos de compresión, distorsión temporal
```

## 🎨 Estilos Artísticos

- **📸 Realista/Fotográfico** - Hiperrealismo, fotografía
- **🎨 Artístico/Digital Art** - Arte digital, ilustración
- **🌸 Anime/Manga** - Estilo japonés
- **🎮 3D/Render** - Modelado 3D, CGI
- **🖼️ Pintura Clásica** - Óleo, acuarela, técnicas tradicionales
- **🎬 Cinematográfico** - Estilo de cine profesional (para videos)
- **✨ Auto-detectar** - La IA elige el mejor estilo

## 🤖 Tecnología

### Gemini 2.5 Flash

```python
# Configuración del modelo
model = genai.GenerativeModel('gemini-2.5-flash')
```

**Ventajas:**
- Respuestas rápidas
- Alta calidad
- Comprensión contextual
- Prompts técnicos precisos

### Arquitectura

```
PROMPTS-IA/
├── src/
│   ├── __init__.py          # Inicialización del paquete
│   ├── generator.py         # Generador de prompts con IA
│   ├── gui.py              # Interfaz gráfica
│   └── utils.py            # Utilidades (historial, exportación)
├── main.py                 # Punto de entrada
├── api_key.txt            # API Key (no incluida)
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## 📜 Historial

El historial se guarda automáticamente en `history.json` con la siguiente estructura:

```json
{
  "timestamp": "2026-01-09T19:30:00",
  "tipo_medio": "video",
  "categoria": "🎬 Generación desde Cero",
  "descripcion": "Gato caminando por playa",
  "estilo": "🎬 Cinematográfico",
  "prompt_positivo": "...",
  "prompt_negativo": "...",
  "detalles": {
    "duracion": "5s",
    "aspecto": "16:9",
    "movimiento_camara": "Paneo (Izq/Der)",
    "intensidad_movimiento": "Media"
  }
}
```

## 💾 Exportación

Los prompts exportados se guardan en `exports/` con formato:

```
╔══════════════════════════════════════════════════════════════╗
║              PROMPTS IA - Prompt Exportado                   ║
╚══════════════════════════════════════════════════════════════╝

📅 Fecha: 09/01/2026 19:30:00
🎬 Tipo de Medio: Video
📂 Categoría: 🎬 Generación desde Cero
🎨 Estilo: Cinematográfico

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 DESCRIPCIÓN:
Gato caminando por una playa al atardecer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PROMPT POSITIVO:
[prompt generado]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚫 PROMPT NEGATIVO:
[prompt generado]
```

## 🔐 Configuración de API

### Obtener API Key de Google Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea un proyecto
3. Genera una API Key
4. Guárdala en `api_key.txt`

```bash
echo "tu-api-key-aqui" > api_key.txt
```

## 🐛 Solución de Problemas

### Error: API Key Inválida

```bash
# Verifica que api_key.txt contenga una key válida
cat api_key.txt
```

### Error: Módulo no encontrado

```bash
# Reinstala dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: No se puede importar src

```bash
# Asegúrate de ejecutar desde el directorio raíz
cd PROMPTS-IA
python main.py
```

## 📈 Roadmap

- [x] Generación de prompts para imágenes
- [x] Generación de prompts para videos
- [x] Historial de prompts generados
- [x] Exportar prompts a archivo
- [ ] Plantillas predefinidas
- [ ] Modo batch (múltiples prompts)
- [ ] Integración directa con APIs de generación
- [ ] Soporte para audio

## 🤝 Contribuir

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -m 'feat: añadir mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autores

- **Jesús Javier Hernández Olvera** - *Desarrollo principal* - [@jjho05](https://github.com/jjho05)

## 🙏 Agradecimientos

- Google por la API de Gemini 2.5 Flash
- CustomTkinter por el framework de UI
- Comunidad de IA generativa

## 📞 Contacto

- GitHub: [@jjho05](https://github.com/jjho05)
- Email: jjho.reivaj05@gmail.com / hernandez.jesusjavier.20.0770@gmail.com

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub

**Hecho con ❤️ para creadores de contenido con IA**

**PROMPTS IA** - De idea a prompt perfecto 🎨🎬✨
