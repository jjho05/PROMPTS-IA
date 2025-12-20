# BrainCourse v2 - Generador de Prompts con IA (Gemini 2.5 Flash)
#Librerías estándar de Python
import os
import threading
from typing import Dict

# Librerías de terceros
import customtkinter as ctk
import google.generativeai as genai


class GeminiPromptGenerator:
    """
    Generador de prompts usando Google Gemini 2.5 Flash API
    
    Esta clase se encarga de comunicarse con la API de Gemini para generar
    prompts optimizados para herramientas de generación de imágenes con IA.
    """
    
    def __init__(self, api_key: str):
        """
        Inicializa el generador con la API key de Gemini
        
        Args:
            api_key (str): API key de Google Gemini
        """
        # Configurar la API de Gemini con la clave proporcionada
        genai.configure(api_key=api_key)
        
        # Inicializar el modelo Gemini 2.5 Flash (versión más reciente)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Categorías de generación disponibles
        self.categorias = {
            "🎭 Transformación de Rostro": "face_transform",
            "🖼️ Generación desde Cero": "generate",
            "🎨 Modificación de Imagen": "modify",
            "✨ Efectos Especiales": "effects"
        }
        
        # Diccionario de estilos artísticos disponibles
        # Cada estilo tiene un emoji para mejor UX y un valor descriptivo para el prompt
        self.estilos = {
            "📸 Realista/Fotográfico": "realista/fotográfico",
            "🎨 Artístico/Digital Art": "artístico/digital art",
            "🌸 Anime/Manga": "anime/manga",
            "🎮 3D/Render": "3D/render",
            "🖼️ Pintura Clásica": "pintura clásica",
            "✨ Auto-detectar": "auto-detectar el mejor estilo"
        }
    
    def generar_prompt_con_ia(self, categoria: str, descripcion: str, estilo: str, detalles_extra: Dict[str, str] = None) -> Dict[str, str]:
        """
        Usa Gemini 2.5 Flash para generar un prompt optimizado según la categoría
        
        Args:
            categoria (str): Categoría de generación seleccionada
            descripcion (str): Descripción del usuario sobre la imagen deseada
            estilo (str): Estilo artístico seleccionado
            detalles_extra (Dict[str, str]): Detalles adicionales específicos de la categoría
            
        Returns:
            Dict[str, str]: Diccionario con 'positivo' y 'negativo' prompts
        """
        
        # Seleccionar el prompt del sistema según la categoría
        if categoria == "face_transform":
            sistema_prompt = self._prompt_transformacion_rostro(descripcion, estilo, detalles_extra)
        elif categoria == "modify":
            sistema_prompt = self._prompt_modificacion_imagen(descripcion, estilo, detalles_extra)
        elif categoria == "effects":
            sistema_prompt = self._prompt_efectos_especiales(descripcion, estilo, detalles_extra)
        else:  # generate
            sistema_prompt = self._prompt_generacion_desde_cero(descripcion, estilo)
        
        # Enviar el prompt al modelo Gemini 2.5 Flash
        response = self.model.generate_content(sistema_prompt)
        texto = response.text
        
        # Parsear la respuesta para extraer los prompts positivo y negativo
        return self._parsear_respuesta(texto)
    
    def _prompt_transformacion_rostro(self, descripcion: str, estilo: str, detalles: Dict[str, str]) -> str:
        """Genera el prompt del sistema para transformación de rostros"""
        transformacion = detalles.get("transformacion", "") if detalles else ""
        mantener_identidad = detalles.get("mantener_identidad", "Sí") if detalles else "Sí"
        
        return f"""Eres un experto en crear prompts para TRANSFORMACIÓN DE ROSTROS con IA (face swap, edición facial, disfraces).

TAREA: Transformar un rostro según la descripción del usuario.

DESCRIPCIÓN: "{descripcion}"
TIPO DE TRANSFORMACIÓN: {transformacion}
ESTILO: {estilo}
MANTENER IDENTIDAD FACIAL: {mantener_identidad}

INSTRUCCIONES CRÍTICAS:

1. PROMPT POSITIVO:
   - Describe la transformación de forma TÉCNICA y ESPECÍFICA
   - Si debe mantener identidad: enfatiza "preservar rasgos faciales originales", "mantener estructura facial", "conservar identidad"
   - Si es disfraz/vestuario: describe el atuendo, accesorios, maquillaje con detalle técnico
   - Si es cambio de edad: especifica edad objetivo, características de piel, arrugas/suavidad
   - Si es cambio de estilo: describe peinado, maquillaje, expresión facial
   - Menciona: iluminación facial, ángulo de cámara, calidad de textura de piel
   - Incluye detalles como: "fotografía de retrato", "enfoque en rostro", "alta definición facial"
   - Tono TÉCNICO y DIRECTO, no poético

   EJEMPLO: "Retrato fotográfico de persona con disfraz de superhéroe, máscara roja y azul cubriendo parte superior del rostro, preservando rasgos faciales originales, traje detallado con textura de tela, iluminación frontal suave, enfoque nítido en rostro, alta resolución, estilo fotorrealista"

2. PROMPT NEGATIVO:
   - CRÍTICO para rostros: "rostro distorsionado, anatomía facial incorrecta, ojos asimétricos, proporciones faciales incorrectas, rostro borroso, rasgos deformados"
   - Agregar: "baja calidad, desenfoque, artefactos digitales, múltiples rostros, rostro duplicado"

IMPORTANTE:
- Todo en ESPAÑOL
- Enfoque en CALIDAD FACIAL y PRESERVACIÓN DE IDENTIDAD (si aplica)
- Tono técnico y profesional

FORMATO DE RESPUESTA:
POSITIVE:
[descripción técnica de la transformación facial]

NEGATIVE:
[elementos a evitar, especialmente defectos faciales]"""

    def _prompt_modificacion_imagen(self, descripcion: str, estilo: str, detalles: Dict[str, str]) -> str:
        """Genera el prompt del sistema para modificación de imágenes"""
        tipo_mod = detalles.get("tipo_modificacion", "") if detalles else ""
        
        return f"""Eres un experto en crear prompts para MODIFICACIÓN DE IMÁGENES con IA (cambio de fondos, agregar elementos, edición).

TAREA: Modificar una imagen existente según la descripción del usuario.

DESCRIPCIÓN: "{descripcion}"
TIPO DE MODIFICACIÓN: {tipo_mod}
ESTILO: {estilo}

INSTRUCCIONES IMPORTANTES:

1. PROMPT POSITIVO:
   - Describe la modificación de forma TÉCNICA y CLARA
   - Si es cambio de fondo: describe el nuevo fondo con detalle (ubicación, iluminación, elementos)
   - Si es agregar elementos: especifica qué agregar, dónde, cómo debe integrarse
   - Si es eliminar elementos: menciona "sin [elemento]", "fondo limpio", "área vacía"
   - Enfatiza: "integración natural", "iluminación coherente", "perspectiva correcta"
   - Menciona composición, balance de colores, coherencia visual
   - Tono TÉCNICO y DIRECTO

   EJEMPLO: "Fotografía de persona en playa tropical, fondo con palmeras y océano turquesa, arena blanca, integración natural de iluminación, sombras coherentes con luz solar, perspectiva correcta, alta resolución, estilo fotorrealista"

2. PROMPT NEGATIVO:
   - "elementos mal integrados, iluminación inconsistente, sombras incorrectas, perspectiva distorsionada, bordes artificiales, recorte visible"
   - Agregar: "baja calidad, artefactos, fusión defectuosa"

IMPORTANTE:
- Todo en ESPAÑOL
- Enfoque en INTEGRACIÓN NATURAL y COHERENCIA
- Tono técnico y profesional

FORMATO DE RESPUESTA:
POSITIVE:
[descripción técnica de la modificación]

NEGATIVE:
[elementos a evitar en la modificación]"""

    def _prompt_efectos_especiales(self, descripcion: str, estilo: str, detalles: Dict[str, str]) -> str:
        """Genera el prompt del sistema para efectos especiales"""
        tipo_efecto = detalles.get("tipo_efecto", "") if detalles else ""
        
        return f"""Eres un experto en crear prompts para EFECTOS ESPECIALES en imágenes con IA (iluminación, clima, atmósfera, filtros).

TAREA: Aplicar efectos especiales a una imagen según la descripción del usuario.

DESCRIPCIÓN: "{descripcion}"
TIPO DE EFECTO: {tipo_efecto}
ESTILO: {estilo}

INSTRUCCIONES IMPORTANTES:

1. PROMPT POSITIVO:
   - Describe el efecto de forma TÉCNICA y ESPECÍFICA
   - Si es iluminación: especifica tipo (dorada, azul, dramática), dirección, intensidad
   - Si es clima: describe condiciones (lluvia, niebla, nieve) con detalle técnico
   - Si es atmósfera: menciona mood, tonalidad de color, partículas (polvo, humo)
   - Si es hora del día: describe luz característica (amanecer, atardecer, noche)
   - Enfatiza: "iluminación volumétrica", "rayos de luz", "partículas en el aire", "color grading"
   - Tono TÉCNICO y DIRECTO

   EJEMPLO: "Escena con iluminación de atardecer dorado, rayos de luz volumétricos atravesando nubes, partículas de polvo visibles en el aire, color grading cálido con tonos naranjas y amarillos, sombras alargadas, atmósfera cinematográfica, alta calidad, estilo fotorrealista"

2. PROMPT NEGATIVO:
   - "iluminación plana, sin atmósfera, colores apagados, efectos artificiales, sobreexposición, subexposición"
   - Agregar: "baja calidad, efectos mal aplicados, artefactos"

IMPORTANTE:
- Todo en ESPAÑOL
- Enfoque en CALIDAD DE EFECTOS y ATMÓSFERA
- Tono técnico y profesional

FORMATO DE RESPUESTA:
POSITIVE:
[descripción técnica del efecto especial]

NEGATIVE:
[elementos a evitar en los efectos]"""

    def _prompt_generacion_desde_cero(self, descripcion: str, estilo: str) -> str:
        """Genera el prompt del sistema para generación desde cero (funcionalidad original)"""
        
        return f"""Eres un experto en crear prompts para generación de imágenes con IA (como Midjourney, DALL-E, Stable Diffusion).

Tu tarea es convertir una descripción simple del usuario en un prompt técnico, detallado y directo en español.

DESCRIPCIÓN DEL USUARIO: "{descripcion}"
ESTILO SOLICITADO: {estilo}

INSTRUCCIONES IMPORTANTES:

1. PROMPT POSITIVO:
   - Escribe una descripción TÉCNICA y DIRECTA de la imagen (NO poética ni exaltada)
   - Usa un tono profesional y objetivo
   - Describe los elementos visuales de forma clara y específica
   - Integra los detalles técnicos de forma natural en la descripción
   - Menciona: composición, iluminación, colores, perspectiva, detalles importantes
   - Incluye el estilo artístico de forma integrada
   - NO uses lenguaje florido, metáforas excesivas o adjetivos dramáticos
   - Debe ser descriptivo pero directo, como una ficha técnica narrativa

   EJEMPLO BUENO: "Fotografía de un gato atigrado descansando en una playa durante el atardecer, olas del océano en segundo plano reflejando tonos naranjas del cielo, arena detallada, iluminación natural lateral que define el pelaje del animal, composición horizontal con profundidad de campo, alta resolución, estilo fotorrealista"
   
   EJEMPLO MALO (muy poético): "Un majestuoso felino atigrado reposando serenamente sobre las doradas arenas de una playa paradisíaca, mientras las olas danzan suavemente bajo el resplandor mágico de un atardecer celestial..."

2. PROMPT NEGATIVO:
   - Lista concisa de elementos a evitar
   - Términos técnicos directos
   - Incluye: baja calidad, desenfoque, distorsión, anatomía incorrecta, elementos no deseados

IMPORTANTE: 
- Todo en ESPAÑOL
- Tono TÉCNICO y DIRECTO, no poético
- Descriptivo pero profesional y objetivo
- Integra los aspectos técnicos de forma fluida

FORMATO DE RESPUESTA (SIGUE ESTE FORMATO EXACTO):
POSITIVE:
[descripción técnica, detallada y directa en español]

NEGATIVE:
[lista de elementos a evitar en español]"""
    
    def _parsear_respuesta(self, texto: str) -> Dict[str, str]:
        """
        Parsea la respuesta de Gemini para extraer los prompts positivo y negativo
        
        Args:
            texto (str): Texto de respuesta generado por Gemini
            
        Returns:
            Dict[str, str]: Diccionario con 'positivo' y 'negativo' prompts parseados
        """
        # Dividir el texto en líneas para procesamiento
        lineas = texto.strip().split('\n')
        prompt_positivo = ""
        prompt_negativo = ""
        seccion_actual = None  # Rastrea si estamos en la sección POSITIVE o NEGATIVE
        
        # Iterar sobre cada línea para identificar y extraer los prompts
        for linea in lineas:
            linea_limpia = linea.strip()
            
            # Detectar inicio de la sección POSITIVE
            if linea_limpia.startswith("POSITIVE:"):
                seccion_actual = "positive"
                resto = linea_limpia.replace("POSITIVE:", "").strip()
                if resto:
                    prompt_positivo = resto
            
            # Detectar inicio de la sección NEGATIVE
            elif linea_limpia.startswith("NEGATIVE:"):
                seccion_actual = "negative"
                resto = linea_limpia.replace("NEGATIVE:", "").strip()
                if resto:
                    prompt_negativo = resto
            
            # Agregar líneas adicionales al prompt positivo
            elif seccion_actual == "positive" and linea_limpia:
                prompt_positivo += " " + linea_limpia if prompt_positivo else linea_limpia
            
            # Agregar líneas adicionales al prompt negativo
            elif seccion_actual == "negative" and linea_limpia:
                prompt_negativo += " " + linea_limpia if prompt_negativo else linea_limpia
        
        # Retornar los prompts parseados
        # Si no hay prompt negativo, usar uno por defecto
        return {
            "positivo": prompt_positivo.strip(),
            "negativo": prompt_negativo.strip() if prompt_negativo else "baja calidad, borroso, distorsionado, anatomía incorrecta"
        }


class BrainCourseGUI:
    """
    Interfaz gráfica moderna con CustomTkinter
    
    Esta clase maneja toda la interfaz de usuario de la aplicación,
    incluyendo la entrada de texto, selección de estilo, generación
    de prompts y funcionalidad de copiar al portapapeles.
    """
    
    # Paleta de colores sobria y profesional
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
    
    def __init__(self, root, api_key):
        self.root = root
        self.root.title("Images Generator - Gemini AI")
        self.root.geometry("900x850")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        try:
            self.generator = GeminiPromptGenerator(api_key)
        except Exception as e:
            self.mostrar_error(f"Error al inicializar Gemini: {str(e)}")
            self.root.destroy()
            return
        
        self.crear_interfaz()
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Error")
        dialog.geometry("400x150")
        
        label = ctk.CTkLabel(dialog, text=mensaje, wraplength=350)
        label.pack(pady=20, padx=20)
        
        btn = ctk.CTkButton(dialog, text="Cerrar", command=dialog.destroy)
        btn.pack(pady=10)
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # Header (fijo, no scrollable)
        header_frame = ctk.CTkFrame(self.root, fg_color=self.COLORS["bg_secondary"], corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Images Generator",
            font=("Helvetica", 24, "bold"),
            text_color=self.COLORS["text_primary"]
        )
        title_label.pack(pady=(12, 3))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Generador Inteligente de Prompts • Powered by Gemini 2.5 Flash",
            font=("Helvetica", 10),
            text_color=self.COLORS["text_secondary"]
        )
        subtitle_label.pack(pady=(0, 12))
        
        # Scrollable main container
        scrollable_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color="transparent",
            scrollbar_button_color=self.COLORS["bg_tertiary"],
            scrollbar_button_hover_color=self.COLORS["accent_primary"]
        )
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=(10, 15))
        
        # Category selector - más compacto
        category_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        category_frame.pack(fill="x", pady=(0, 10))
        
        category_label = ctk.CTkLabel(
            category_frame,
            text="📂 Categoría:",
            font=("Helvetica", 12, "bold"),
            text_color=self.COLORS["text_primary"]
        )
        category_label.pack(side="left", padx=(0, 10))
        
        self.category_var = ctk.StringVar(value="🖼️ Generación desde Cero")
        category_combo = ctk.CTkComboBox(
            category_frame,
            variable=self.category_var,
            values=list(self.generator.categorias.keys()),
            font=("Helvetica", 11),
            width=260,
            height=32,
            fg_color=self.COLORS["bg_secondary"],
            border_color=self.COLORS["border"],
            button_color=self.COLORS["bg_tertiary"],
            button_hover_color=self.COLORS["accent_primary"],
            dropdown_fg_color=self.COLORS["bg_secondary"],
            command=self.actualizar_campos_dinamicos
        )
        category_combo.pack(side="left")
        
        # Dynamic fields container (se empaquetará dinámicamente solo cuando tenga contenido)
        self.dynamic_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        
        # Input section - más compacto
        input_label = ctk.CTkLabel(
            scrollable_frame,
            text="✏️  Describe tu idea:",
            font=("Helvetica", 12, "bold"),
            text_color=self.COLORS["text_primary"],
            anchor="w"
        )
        input_label.pack(fill="x", pady=(0, 5))
        
        self.input_text = ctk.CTkTextbox(
            scrollable_frame,
            height=80,
            font=("Helvetica", 11),
            fg_color=self.COLORS["bg_secondary"],
            border_color=self.COLORS["border"],
            border_width=1,
            corner_radius=8
        )
        self.input_text.pack(fill="x", pady=(0, 10))
        
        # Style selector - más compacto
        style_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        style_frame.pack(fill="x", pady=(0, 10))
        
        style_label = ctk.CTkLabel(
            style_frame,
            text="🎨 Estilo:",
            font=("Helvetica", 12, "bold"),
            text_color=self.COLORS["text_primary"]
        )
        style_label.pack(side="left", padx=(0, 10))
        
        self.style_var = ctk.StringVar(value="✨ Auto-detectar")
        style_combo = ctk.CTkComboBox(
            style_frame,
            variable=self.style_var,
            values=list(self.generator.estilos.keys()),
            font=("Helvetica", 11),
            width=260,
            height=32,
            fg_color=self.COLORS["bg_secondary"],
            border_color=self.COLORS["border"],
            button_color=self.COLORS["bg_tertiary"],
            button_hover_color=self.COLORS["accent_primary"],
            dropdown_fg_color=self.COLORS["bg_secondary"]
        )
        style_combo.pack(side="left")
        
        # Initialize dynamic fields
        self.actualizar_campos_dinamicos()
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            scrollable_frame,
            text="✨ Generar Prompts",
            font=("Helvetica", 13, "bold"),
            fg_color=self.COLORS["accent_primary"],
            hover_color="#4a7449",
            height=40,
            corner_radius=8,
            command=self.generar_prompts
        )
        self.generate_btn.pack(pady=(0, 15))
        
        # Results section
        results_label = ctk.CTkLabel(
            scrollable_frame,
            text="📝 Resultados:",
            font=("Helvetica", 12, "bold"),
            text_color=self.COLORS["text_primary"],
            anchor="w"
        )
        results_label.pack(fill="x", pady=(0, 8))
        
        # Positive prompt
        positive_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.COLORS["bg_secondary"], corner_radius=10)
        positive_frame.pack(fill="x", pady=(0, 10))
        
        positive_header = ctk.CTkFrame(positive_frame, fg_color="transparent")
        positive_header.pack(fill="x", padx=12, pady=(10, 6))
        
        ctk.CTkLabel(
            positive_header,
            text="✅ PROMPT POSITIVO",
            font=("Helvetica", 10, "bold"),
            text_color=self.COLORS["accent_primary"]
        ).pack(side="left")
        
        copy_pos_btn = ctk.CTkButton(
            positive_header,
            text="📋 Copiar",
            font=("Helvetica", 9),
            fg_color=self.COLORS["accent_primary"],
            hover_color="#4a7449",
            width=80,
            height=26,
            corner_radius=6,
            command=lambda: self.copiar_texto(self.positive_text)
        )
        copy_pos_btn.pack(side="right")
        
        self.positive_text = ctk.CTkTextbox(
            positive_frame,
            height=120,
            font=("Helvetica", 10),
            fg_color=self.COLORS["bg_tertiary"],
            border_width=0,
            corner_radius=0,
            wrap="word"
        )
        self.positive_text.pack(fill="x", padx=12, pady=(0, 10))
        
        # Negative prompt
        negative_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.COLORS["bg_secondary"], corner_radius=10)
        negative_frame.pack(fill="x", pady=(0, 10))
        
        negative_header = ctk.CTkFrame(negative_frame, fg_color="transparent")
        negative_header.pack(fill="x", padx=12, pady=(10, 6))
        
        ctk.CTkLabel(
            negative_header,
            text="🚫 PROMPT NEGATIVO",
            font=("Helvetica", 10, "bold"),
            text_color=self.COLORS["accent_danger"]
        ).pack(side="left")
        
        copy_neg_btn = ctk.CTkButton(
            negative_header,
            text="📋 Copiar",
            font=("Helvetica", 9),
            fg_color=self.COLORS["accent_danger"],
            hover_color="#a84340",
            width=80,
            height=26,
            corner_radius=6,
            command=lambda: self.copiar_texto(self.negative_text)
        )
        copy_neg_btn.pack(side="right")
        
        self.negative_text = ctk.CTkTextbox(
            negative_frame,
            height=100,
            font=("Helvetica", 10),
            fg_color=self.COLORS["bg_tertiary"],
            border_width=0,
            corner_radius=0,
            wrap="word"
        )
        self.negative_text.pack(fill="x", padx=12, pady=(0, 10))
    
    def copiar_texto(self, text_widget):
        """
        Copia el texto del widget especificado al portapapeles del sistema
        
        Args:
            text_widget: Widget de texto de CustomTkinter del cual copiar
        """
        texto = text_widget.get("1.0", "end-1c").strip()
        if texto:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
            self.mostrar_notificacion("✅ Copiado", "Texto copiado al portapapeles")
        else:
            self.mostrar_notificacion("⚠️ Advertencia", "No hay texto para copiar")
    
    def actualizar_campos_dinamicos(self, *args):
        """
        Actualiza los campos dinámicos según la categoría seleccionada
        """
        # Limpiar campos dinámicos anteriores
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        
        categoria = self.generator.categorias[self.category_var.get()]
        
        if categoria == "face_transform":
            # Empaquetar el frame solo cuando tiene contenido
            self.dynamic_frame.pack(fill="x", pady=(0, 10), before=self.input_text.master.children[list(self.input_text.master.children.keys())[list(self.input_text.master.children.values()).index(self.input_text)-1]])
            
            # Campos para transformación de rostro
            # Tipo de transformación
            trans_label = ctk.CTkLabel(
                self.dynamic_frame,
                text="🎭 Tipo de transformación:",
                font=("Helvetica", 11, "bold"),
                text_color=self.COLORS["text_primary"]
            )
            trans_label.pack(anchor="w", pady=(0, 4))
            
            self.transformacion_var = ctk.StringVar(value="Disfraz/Vestuario")
            trans_combo = ctk.CTkComboBox(
                self.dynamic_frame,
                variable=self.transformacion_var,
                values=["Disfraz/Vestuario", "Cambio de Edad", "Cambio de Estilo", "Maquillaje/Efectos", "Otro"],
                font=("Helvetica", 10),
                width=260,
                height=32,
                fg_color=self.COLORS["bg_secondary"],
                border_color=self.COLORS["border"],
                button_color=self.COLORS["bg_tertiary"],
                button_hover_color=self.COLORS["accent_primary"],
                dropdown_fg_color=self.COLORS["bg_secondary"]
            )
            trans_combo.pack(anchor="w", pady=(0, 8))
            
            # Mantener identidad
            identity_label = ctk.CTkLabel(
                self.dynamic_frame,
                text="👤 ¿Mantener identidad facial?",
                font=("Helvetica", 11, "bold"),
                text_color=self.COLORS["text_primary"]
            )
            identity_label.pack(anchor="w", pady=(0, 4))
            
            self.identidad_var = ctk.StringVar(value="Sí")
            identity_combo = ctk.CTkComboBox(
                self.dynamic_frame,
                variable=self.identidad_var,
                values=["Sí", "No"],
                font=("Helvetica", 10),
                width=140,
                height=32,
                fg_color=self.COLORS["bg_secondary"],
                border_color=self.COLORS["border"],
                button_color=self.COLORS["bg_tertiary"],
                button_hover_color=self.COLORS["accent_primary"],
                dropdown_fg_color=self.COLORS["bg_secondary"]
            )
            identity_combo.pack(anchor="w", pady=(0, 5))
            
        elif categoria == "modify":
            # Empaquetar el frame solo cuando tiene contenido
            self.dynamic_frame.pack(fill="x", pady=(0, 10), before=self.input_text.master.children[list(self.input_text.master.children.keys())[list(self.input_text.master.children.values()).index(self.input_text)-1]])
            
            # Campos para modificación de imagen
            mod_label = ctk.CTkLabel(
                self.dynamic_frame,
                text="🎨 Tipo de modificación:",
                font=("Helvetica", 11, "bold"),
                text_color=self.COLORS["text_primary"]
            )
            mod_label.pack(anchor="w", pady=(0, 4))
            
            self.modificacion_var = ctk.StringVar(value="Cambio de Fondo")
            mod_combo = ctk.CTkComboBox(
                self.dynamic_frame,
                variable=self.modificacion_var,
                values=["Cambio de Fondo", "Agregar Elementos", "Eliminar Elementos", "Reemplazar Objetos", "Otro"],
                font=("Helvetica", 10),
                width=260,
                height=32,
                fg_color=self.COLORS["bg_secondary"],
                border_color=self.COLORS["border"],
                button_color=self.COLORS["bg_tertiary"],
                button_hover_color=self.COLORS["accent_primary"],
                dropdown_fg_color=self.COLORS["bg_secondary"]
            )
            mod_combo.pack(anchor="w", pady=(0, 5))
            
        elif categoria == "effects":
            # Empaquetar el frame solo cuando tiene contenido
            self.dynamic_frame.pack(fill="x", pady=(0, 10), before=self.input_text.master.children[list(self.input_text.master.children.keys())[list(self.input_text.master.children.values()).index(self.input_text)-1]])
            
            # Campos para efectos especiales
            effect_label = ctk.CTkLabel(
                self.dynamic_frame,
                text="✨ Tipo de efecto:",
                font=("Helvetica", 11, "bold"),
                text_color=self.COLORS["text_primary"]
            )
            effect_label.pack(anchor="w", pady=(0, 4))
            
            self.efecto_var = ctk.StringVar(value="Iluminación")
            effect_combo = ctk.CTkComboBox(
                self.dynamic_frame,
                variable=self.efecto_var,
                values=["Iluminación", "Clima/Atmósfera", "Hora del Día", "Color Grading", "Partículas/Humo", "Otro"],
                font=("Helvetica", 10),
                width=260,
                height=32,
                fg_color=self.COLORS["bg_secondary"],
                border_color=self.COLORS["border"],
                button_color=self.COLORS["bg_tertiary"],
                button_hover_color=self.COLORS["accent_primary"],
                dropdown_fg_color=self.COLORS["bg_secondary"]
            )
            effect_combo.pack(anchor="w", pady=(0, 5))
        else:
            # Para "generate" no hay campos adicionales - desempaquetar el frame
            self.dynamic_frame.pack_forget()
    
    def mostrar_notificacion(self, titulo, mensaje):
        """
        Muestra una ventana de notificación modal temporal
        
        Args:
            titulo (str): Título de la ventana de notificación
            mensaje (str): Mensaje a mostrar al usuario
        """
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(titulo)
        dialog.geometry("350x120")
        dialog.resizable(False, False)
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        label = ctk.CTkLabel(
            dialog,
            text=mensaje,
            font=("Helvetica", 12),
            wraplength=300
        )
        label.pack(pady=20, padx=20)
        
        btn = ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            command=dialog.destroy,
            fg_color=self.COLORS["accent_primary"],
            hover_color="#4a7449"
        )
        btn.pack(pady=(0, 15))
    
    def generar_prompts(self):
        """
        Genera los prompts usando Gemini 2.5 Flash de forma asíncrona
        
        Este método valida la entrada del usuario, deshabilita el botón de generación,
        y ejecuta la generación en un hilo separado para no bloquear la interfaz.
        """
        descripcion = self.input_text.get("1.0", "end-1c").strip()
        
        if not descripcion:
            self.mostrar_notificacion("⚠️ Advertencia", "Por favor, describe tu idea primero")
            return
        
        # Deshabilitar el botón mientras se genera
        self.generate_btn.configure(state="disabled", text="🤖 Generando...")
        
        # Limpiar los campos de resultados anteriores
        self.positive_text.delete("1.0", "end")
        self.negative_text.delete("1.0", "end")
        
        # Función interna para ejecutar en un hilo separado
        def generar():
            try:
                # Obtener la categoría y el estilo seleccionados
                categoria = self.generator.categorias[self.category_var.get()]
                estilo = self.generator.estilos[self.style_var.get()]
                
                # Recopilar detalles extra según la categoría
                detalles_extra = {}
                
                if categoria == "face_transform":
                    detalles_extra = {
                        "transformacion": self.transformacion_var.get(),
                        "mantener_identidad": self.identidad_var.get()
                    }
                elif categoria == "modify":
                    detalles_extra = {
                        "tipo_modificacion": self.modificacion_var.get()
                    }
                elif categoria == "effects":
                    detalles_extra = {
                        "tipo_efecto": self.efecto_var.get()
                    }
                
                # Generar los prompts usando Gemini 2.5 Flash con la nueva firma
                prompts = self.generator.generar_prompt_con_ia(categoria, descripcion, estilo, detalles_extra)
                
                # Actualizar la UI en el hilo principal
                self.root.after(0, lambda: self.mostrar_resultados(prompts))
            except Exception as e:
                # Mostrar error si algo falla
                self.root.after(0, lambda: self.mostrar_notificacion("❌ Error", f"Error al generar: {str(e)}"))
            finally:
                # Re-habilitar el botón de generación
                self.root.after(0, lambda: self.generate_btn.configure(state="normal", text="✨ Generar Prompts"))
        
        # Ejecutar la generación en un hilo daemon para no bloquear la UI
        threading.Thread(target=generar, daemon=True).start()
    
    def mostrar_resultados(self, prompts):
        """
        Muestra los prompts generados en los campos de texto correspondientes
        
        Args:
            prompts (Dict[str, str]): Diccionario con 'positivo' y 'negativo' prompts
        """
        self.positive_text.insert("1.0", prompts['positivo'])
        self.negative_text.insert("1.0", prompts['negativo'])


def cargar_api_key():
    """
    Carga la API key de Gemini desde el archivo api_key.txt
    
    Busca el archivo en el mismo directorio que el script.
    
    Returns:
        str or None: La API key si se encuentra, None en caso contrario
    """
    # Obtener el directorio donde está ubicado este script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta completa al archivo api_key.txt
    api_key_path = os.path.join(script_dir, "api_key.txt")
    
    try:
        with open(api_key_path, 'r') as f:
            api_key = f.read().strip()
            if api_key:
                return api_key
    except FileNotFoundError:
        pass
    
    return None


def main():
    """
    Función principal de la aplicación
    
    Carga la API key, valida su existencia y lanza la interfaz gráfica.
    Si no se encuentra la API key, muestra un diálogo de error.
    """
    # Intentar cargar la API key desde el archivo
    api_key = cargar_api_key()
    
    # Si no se encuentra la API key, mostrar error y salir
    if not api_key:
        root = ctk.CTk()
        root.withdraw()
        
        dialog = ctk.CTkToplevel(root)
        dialog.title("Error")
        dialog.geometry("450x180")
        
        label = ctk.CTkLabel(
            dialog,
            text="No se encontró la API key.\n\nCrea un archivo 'api_key.txt' en la misma carpeta\nque este script y pega tu API key de Gemini.",
            font=("Helvetica", 12),
            justify="center"
        )
        label.pack(pady=30, padx=20)
        
        btn = ctk.CTkButton(dialog, text="Cerrar", command=root.quit)
        btn.pack(pady=10)
        
        root.mainloop()
        return
    
    # Crear la ventana principal y la aplicación
    root = ctk.CTk()
    app = BrainCourseGUI(root, api_key)
    
    # Iniciar el loop principal de la interfaz
    root.mainloop()


if __name__ == "__main__":
    main()
