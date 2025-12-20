# 🎨 PROMPTS IA - Generador Inteligente de Prompts

> Generador profesional de prompts para herramientas de IA de generación de imágenes, potenciado por Gemini 2.5 Flash

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-green.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-orange.svg)](https://ai.google.dev/)

## 📋 Descripción

**PROMPTS IA** es una aplicación de escritorio que utiliza Google Gemini 2.5 Flash para convertir descripciones simples en prompts técnicos y detallados optimizados para herramientas de generación de imágenes con IA como Midjourney, DALL-E, Stable Diffusion, y más.

## ✨ Características

### 4 Categorías de Generación

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

### Características Generales
- 🤖 **IA Avanzada** - Gemini 2.5 Flash
- 🎯 **Prompts Técnicos** - Lenguaje profesional y directo
- 📋 **Copiar al Portapapeles** - Un click para copiar
- 🎨 **6 Estilos Artísticos** - Realista, Digital Art, Anime, 3D, Clásico, Auto-detectar
- 🌙 **Interfaz Moderna** - Tema oscuro profesional
- ⚡ **Generación Rápida** - Resultados en segundos

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
python app.py
```

## 📦 Dependencias

```txt
customtkinter==5.2.0
google-generativeai==0.3.0
```

## 💻 Uso

### Inicio Rápido

1. **Ejecuta** `python app.py`
2. **Selecciona** una categoría
3. **Describe** tu idea
4. **Elige** un estilo artístico
5. **Genera** y copia los prompts

### Ejemplo de Uso

**Entrada:**
```
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

## 🎯 Categorías Detalladas

### 🎭 Transformación de Rostro

**Tipos disponibles:**
- Disfraz/Vestuario
- Cambio de Edad
- Cambio de Estilo
- Maquillaje/Efectos
- Otro

**Opciones:**
- Mantener identidad facial: Sí/No

**Ideal para:**
- Face swap
- Edición facial
- Caracterización
- Envejecimiento/rejuvenecimiento

### 🖼️ Generación desde Cero

**Características:**
- Descripción libre
- Auto-detección de estilo
- Prompts técnicos optimizados

**Ideal para:**
- Crear imágenes nuevas
- Conceptos originales
- Ilustraciones

### 🎨 Modificación de Imagen

**Tipos disponibles:**
- Cambio de Fondo
- Agregar Elementos
- Eliminar Elementos
- Reemplazar Objetos
- Otro

**Ideal para:**
- Edición de fotos
- Composiciones
- Retoque digital

### ✨ Efectos Especiales

**Tipos disponibles:**
- Iluminación
- Clima/Atmósfera
- Hora del Día
- Color Grading
- Partículas/Humo
- Otro

**Ideal para:**
- Efectos cinematográficos
- Atmósferas
- Post-procesamiento

## 🎨 Estilos Artísticos

- **📸 Realista/Fotográfico** - Hiperrealismo, fotografía
- **🎨 Artístico/Digital Art** - Arte digital, ilustración
- **🌸 Anime/Manga** - Estilo japonés
- **🎮 3D/Render** - Modelado 3D, CGI
- **🖼️ Pintura Clásica** - Óleo, acuarela, técnicas tradicionales
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
├── app.py                    # Aplicación principal
├── api_key.txt              # API Key (no incluida)
└── requirements.txt         # Dependencias
```

## 🎨 Interfaz de Usuario

### Paleta de Colores

```python
COLORS = {
    "bg_primary": "#1a1d23",
    "bg_secondary": "#242831",
    "bg_tertiary": "#2d3139",
    "accent_primary": "#5b8c5a",
    "accent_danger": "#c75450",
    "text_primary": "#e8e8e8",
    "text_secondary": "#a0a0a0",
    "border": "#3a3f4b"
}
```

### Componentes

- **Scrollable Frame** - Interfaz fluida
- **Category Selector** - 4 categorías
- **Dynamic Fields** - Campos contextuales
- **Style Selector** - 6 estilos
- **Copy Buttons** - Copiar con un click
- **Modern Theme** - Diseño oscuro profesional

## 🔐 Configuración de API

### Obtener API Key de Google Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea un proyecto
3. Genera una API Key
4. Guárdala en `api_key.txt`

```bash
echo "tu-api-key-aqui" > api_key.txt
```

## 📚 Ejemplos de Prompts Generados

### Ejemplo 1: Generación desde Cero

**Entrada:** "Un gato en la playa al atardecer"

**Prompt Positivo:**
```
Fotografía de un gato atigrado descansando en una playa 
durante el atardecer, olas del océano en segundo plano 
reflejando tonos naranjas del cielo, arena detallada, 
iluminación natural lateral que define el pelaje del 
animal, composición horizontal con profundidad de campo, 
alta resolución, estilo fotorrealista
```

### Ejemplo 2: Efectos Especiales

**Entrada:** "Iluminación de atardecer dorado"

**Prompt Positivo:**
```
Escena con iluminación de atardecer dorado, rayos de luz 
volumétricos atravesando nubes, partículas de polvo visibles 
en el aire, color grading cálido con tonos naranjas y 
amarillos, sombras alargadas, atmósfera cinematográfica, 
alta calidad, estilo fotorrealista
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

## 📈 Roadmap

- [ ] Historial de prompts generados
- [ ] Exportar prompts a archivo
- [ ] Más categorías (Video, Audio)
- [ ] Plantillas predefinidas
- [ ] Modo batch (múltiples prompts)
- [ ] Integración directa con APIs de generación

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
- Email: lic.ing.jesusolvera@gmail.com

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub

**Hecho con ❤️ para creadores de contenido con IA**

**PROMPTS IA** - De idea a prompt perfecto 🎨✨
