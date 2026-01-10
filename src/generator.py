"""
Generador de Prompts con IA (Gemini 2.5 Flash)
Soporte para generación de prompts de imágenes y videos
"""
from typing import Dict, Optional
import google.generativeai as genai


class GeminiPromptGenerator:
    """
    Generador de prompts usando Google Gemini 2.5 Flash API
    
    Esta clase se encarga de comunicarse con la API de Gemini para generar
    prompts optimizados para herramientas de generación de imágenes y videos con IA.
    """
    
    def __init__(self, api_key: str):
        """
        Inicializa el generador con la API key de Gemini
        
        Args:
            api_key (str): API key de Google Gemini
        """
        # Configurar la API de Gemini con la clave proporcionada
        genai.configure(api_key=api_key)
        
        # Inicializar el modelo Gemini 2.5 Flash
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Categorías de generación para IMÁGENES
        self.categorias_imagen = {
            "🎭 Transformación de Rostro": "face_transform",
            "🖼️ Generación desde Cero": "generate",
            "🎨 Modificación de Imagen": "modify",
            "✨ Efectos Especiales": "effects"
        }
        
        # Categorías de generación para VIDEOS
        self.categorias_video = {
            "🎬 Generación desde Cero": "video_generate",
            "🖼️➡️🎬 Imagen a Video": "image_to_video",
            "✨ Efectos y Transiciones": "video_effects",
            "🎥 Movimientos de Cámara": "camera_movement"
        }
        
        # Estilos artísticos disponibles
        self.estilos = {
            "📸 Realista/Fotográfico": "realista/fotográfico",
            "🎨 Artístico/Digital Art": "artístico/digital art",
            "🌸 Anime/Manga": "anime/manga",
            "🎮 3D/Render": "3D/render",
            "🖼️ Pintura Clásica": "pintura clásica",
            "🎬 Cinematográfico": "cinematográfico",
            "✨ Auto-detectar": "auto-detectar el mejor estilo"
        }
    
    def generar_prompt_con_ia(self, tipo_medio: str, categoria: str, descripcion: str, 
                             estilo: str, detalles_extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Usa Gemini 2.5 Flash para generar un prompt optimizado según el tipo de medio y categoría
        
        Args:
            tipo_medio (str): "imagen" o "video"
            categoria (str): Categoría de generación seleccionada
            descripcion (str): Descripción del usuario sobre el contenido deseado
            estilo (str): Estilo artístico seleccionado
            detalles_extra (Dict[str, str]): Detalles adicionales específicos de la categoría
            
        Returns:
            Dict[str, str]: Diccionario con 'positivo' y 'negativo' prompts
        """
        
        # Seleccionar el prompt del sistema según el tipo de medio y categoría
        if tipo_medio == "imagen":
            sistema_prompt = self._generar_prompt_imagen(categoria, descripcion, estilo, detalles_extra)
        else:  # video
            sistema_prompt = self._generar_prompt_video(categoria, descripcion, estilo, detalles_extra)
        
        # Enviar el prompt al modelo Gemini 2.5 Flash
        response = self.model.generate_content(sistema_prompt)
        texto = response.text
        
        # Parsear la respuesta para extraer los prompts positivo y negativo
        return self._parsear_respuesta(texto)
    
    def _generar_prompt_imagen(self, categoria: str, descripcion: str, estilo: str, 
                               detalles: Optional[Dict[str, str]]) -> str:
        """Genera el prompt del sistema para imágenes según la categoría"""
        if categoria == "face_transform":
            return self._prompt_transformacion_rostro(descripcion, estilo, detalles)
        elif categoria == "modify":
            return self._prompt_modificacion_imagen(descripcion, estilo, detalles)
        elif categoria == "effects":
            return self._prompt_efectos_especiales(descripcion, estilo, detalles)
        else:  # generate
            return self._prompt_generacion_desde_cero(descripcion, estilo)
    
    def _generar_prompt_video(self, categoria: str, descripcion: str, estilo: str,
                             detalles: Optional[Dict[str, str]]) -> str:
        """Genera el prompt del sistema para videos según la categoría"""
        if categoria == "video_generate":
            return self._prompt_video_desde_cero(descripcion, estilo, detalles)
        elif categoria == "image_to_video":
            return self._prompt_video_desde_imagen(descripcion, estilo, detalles)
        elif categoria == "video_effects":
            return self._prompt_video_efectos(descripcion, estilo, detalles)
        else:  # camera_movement
            return self._prompt_video_camara(descripcion, estilo, detalles)
    
    # ==================== PROMPTS PARA IMÁGENES ====================
    
    def _prompt_transformacion_rostro(self, descripcion: str, estilo: str, detalles: Optional[Dict[str, str]]) -> str:
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

    def _prompt_modificacion_imagen(self, descripcion: str, estilo: str, detalles: Optional[Dict[str, str]]) -> str:
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

    def _prompt_efectos_especiales(self, descripcion: str, estilo: str, detalles: Optional[Dict[str, str]]) -> str:
        """Genera el prompt del sistema para efectos especiales en imágenes"""
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
        """Genera el prompt del sistema para generación de imágenes desde cero"""
        
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
    
    # ==================== PROMPTS PARA VIDEOS ====================
    
    def _prompt_video_desde_cero(self, descripcion: str, estilo: str, detalles: Optional[Dict[str, str]]) -> str:
        """Genera el prompt del sistema para generación de videos desde cero"""
        duracion = detalles.get("duracion", "5s") if detalles else "5s"
        aspecto = detalles.get("aspecto", "16:9") if detalles else "16:9"
        movimiento_camara = detalles.get("movimiento_camara", "Estático") if detalles else "Estático"
        intensidad = detalles.get("intensidad_movimiento", "Media") if detalles else "Media"
        
        return f"""Eres un experto en crear prompts para GENERACIÓN DE VIDEOS con IA (como Runway, Pika, Sora).

Tu tarea es convertir una descripción del usuario en un prompt técnico para generación de video.

DESCRIPCIÓN: "{descripcion}"
ESTILO: {estilo}
DURACIÓN: {duracion}
RELACIÓN DE ASPECTO: {aspecto}
MOVIMIENTO DE CÁMARA: {movimiento_camara}
INTENSIDAD DE MOVIMIENTO: {intensidad}

INSTRUCCIONES IMPORTANTES:

1. PROMPT POSITIVO:
   - Describe la ESCENA y la ACCIÓN de forma TÉCNICA y CINEMATOGRÁFICA
   - Especifica el movimiento de cámara: {movimiento_camara}
   - Menciona la duración aproximada: {duracion}
   - Describe el movimiento de elementos en la escena (intensidad: {intensidad})
   - Incluye: composición, iluminación, transiciones suaves
   - Enfatiza: "movimiento fluido", "transición natural", "continuidad temporal"
   - Menciona el aspecto ratio: {aspecto}
   - Tono TÉCNICO y CINEMATOGRÁFICO

   EJEMPLO: "Video de un gato caminando por una playa al atardecer, cámara con paneo lateral suave siguiendo al animal, olas en movimiento constante en segundo plano, arena con textura detallada, iluminación dorada del atardecer, movimiento fluido y natural, duración 5 segundos, aspecto 16:9, estilo cinematográfico realista"

2. PROMPT NEGATIVO:
   - "movimiento brusco, saltos de frames, parpadeo, glitches, movimiento antinatural, cámara inestable, cortes abruptos"
   - Agregar: "baja calidad, artefactos de compresión, distorsión temporal, objetos que aparecen/desaparecen"

IMPORTANTE:
- Todo en ESPAÑOL
- Enfoque en MOVIMIENTO FLUIDO y CONTINUIDAD
- Especifica claramente el tipo de movimiento de cámara
- Tono técnico y cinematográfico

FORMATO DE RESPUESTA:
POSITIVE:
[descripción técnica del video con movimientos y duración]

NEGATIVE:
[elementos a evitar en el video]"""

    def _prompt_video_desde_imagen(self, descripcion: str, estilo: str, detalles: Optional[Dict[str, str]]) -> str:
        """Genera el prompt del sistema para animar imágenes (imagen a video)"""
        duracion = detalles.get("duracion", "3s") if detalles else "3s"
        aspecto = detalles.get("aspecto", "16:9") if detalles else "16:9"
        movimiento_camara = detalles.get("movimiento_camara", "Zoom") if detalles else "Zoom"
        intensidad = detalles.get("intensidad_movimiento", "Baja") if detalles else "Baja"
        
        return f"""Eres un experto en crear prompts para ANIMAR IMÁGENES ESTÁTICAS (imagen a video) con IA.

Tu tarea es describir cómo animar una imagen estática en un video dinámico.

DESCRIPCIÓN: "{descripcion}"
ESTILO: {estilo}
DURACIÓN: {duracion}
RELACIÓN DE ASPECTO: {aspecto}
MOVIMIENTO DE CÁMARA: {movimiento_camara}
INTENSIDAD DE MOVIMIENTO: {intensidad}

INSTRUCCIONES IMPORTANTES:

1. PROMPT POSITIVO:
   - Describe cómo ANIMAR la imagen estática
   - Especifica el movimiento de cámara: {movimiento_camara}
   - Menciona qué elementos deben moverse y cómo (intensidad: {intensidad})
   - Describe movimientos sutiles: cabello, ropa, elementos ambientales
   - Enfatiza: "animación sutil", "movimiento natural", "transición suave desde imagen estática"
   - Menciona duración: {duracion}
   - Tono TÉCNICO enfocado en ANIMACIÓN

   EJEMPLO: "Animar imagen de retrato, zoom in suave hacia el rostro, movimiento sutil del cabello como si hubiera brisa ligera, parpadeo natural de ojos, ligero movimiento de ropa, fondo con desenfoque bokeh que se mueve sutilmente, transición fluida, duración 3 segundos, intensidad baja, aspecto 9:16"

2. PROMPT NEGATIVO:
   - "movimiento excesivo, distorsión de rostro, animación artificial, elementos que se deforman, movimiento no natural"
   - Agregar: "glitches, parpadeo, saltos bruscos, pérdida de calidad de imagen original"

IMPORTANTE:
- Todo en ESPAÑOL
- Enfoque en ANIMACIÓN SUTIL y NATURAL
- Preservar la calidad de la imagen original
- Movimientos coherentes con la escena

FORMATO DE RESPUESTA:
POSITIVE:
[descripción técnica de cómo animar la imagen]

NEGATIVE:
[elementos a evitar en la animación]"""

    def _prompt_video_efectos(self, descripcion: str, estilo: str, detalles: Optional[Dict[str, str]]) -> str:
        """Genera el prompt del sistema para efectos y transiciones en video"""
        duracion = detalles.get("duracion", "5s") if detalles else "5s"
        tipo_efecto = detalles.get("tipo_efecto", "Iluminación") if detalles else "Iluminación"
        
        return f"""Eres un experto en crear prompts para EFECTOS Y TRANSICIONES EN VIDEO con IA.

Tu tarea es describir efectos visuales para aplicar a un video.

DESCRIPCIÓN: "{descripcion}"
TIPO DE EFECTO: {tipo_efecto}
ESTILO: {estilo}
DURACIÓN: {duracion}

INSTRUCCIONES IMPORTANTES:

1. PROMPT POSITIVO:
   - Describe el EFECTO VISUAL de forma TÉCNICA
   - Si es iluminación: especifica cambios de luz, color grading, rayos volumétricos
   - Si es clima: describe lluvia, nieve, niebla con movimiento natural
   - Si es transición: describe el tipo (fade, dissolve, wipe) y duración
   - Enfatiza: "transición suave", "efecto progresivo", "integración natural"
   - Menciona cómo evoluciona el efecto durante la duración
   - Tono TÉCNICO y CINEMATOGRÁFICO

   EJEMPLO: "Video con transición de día a noche, cambio gradual de iluminación de tonos cálidos a azules fríos, aparición progresiva de estrellas en el cielo, sombras que se alargan y oscurecen, color grading que evoluciona suavemente, duración 5 segundos, transición cinematográfica fluida"

2. PROMPT NEGATIVO:
   - "transición brusca, cambios abruptos, efectos artificiales, inconsistencia temporal, parpadeo"
   - Agregar: "artefactos visuales, glitches, efectos mal aplicados"

IMPORTANTE:
- Todo en ESPAÑOL
- Enfoque en TRANSICIONES SUAVES y EFECTOS NATURALES
- Describir la evolución temporal del efecto

FORMATO DE RESPUESTA:
POSITIVE:
[descripción técnica del efecto o transición]

NEGATIVE:
[elementos a evitar]"""

    def _prompt_video_camara(self, descripcion: str, estilo: str, detalles: Optional[Dict[str, str]]) -> str:
        """Genera el prompt del sistema para movimientos de cámara cinematográficos"""
        duracion = detalles.get("duracion", "5s") if detalles else "5s"
        aspecto = detalles.get("aspecto", "16:9") if detalles else "16:9"
        movimiento_camara = detalles.get("movimiento_camara", "Dolly") if detalles else "Dolly"
        intensidad = detalles.get("intensidad_movimiento", "Media") if detalles else "Media"
        
        return f"""Eres un experto en crear prompts para MOVIMIENTOS DE CÁMARA CINEMATOGRÁFICOS en video con IA.

Tu tarea es describir movimientos de cámara profesionales para un video.

DESCRIPCIÓN: "{descripcion}"
MOVIMIENTO DE CÁMARA: {movimiento_camara}
ESTILO: {estilo}
DURACIÓN: {duracion}
RELACIÓN DE ASPECTO: {aspecto}
INTENSIDAD: {intensidad}

INSTRUCCIONES IMPORTANTES:

1. PROMPT POSITIVO:
   - Describe el MOVIMIENTO DE CÁMARA de forma TÉCNICA y PRECISA
   - Especifica el tipo: {movimiento_camara}
   - Describe la trayectoria y velocidad (intensidad: {intensidad})
   - Menciona: punto de inicio, punto final, velocidad de movimiento
   - Si es paneo: dirección (izquierda/derecha, arriba/abajo)
   - Si es zoom: in/out, velocidad
   - Si es dolly: avance/retroceso, altura de cámara
   - Si es tracking: seguimiento del sujeto, estabilidad
   - Enfatiza: "movimiento suave", "estabilizado", "cinematográfico"
   - Tono TÉCNICO de CINEMATOGRAFÍA

   EJEMPLO: "Video con dolly in cinematográfico, cámara avanza suavemente hacia el sujeto desde 3 metros hasta primer plano, movimiento estabilizado y fluido, velocidad media constante, altura de cámara a nivel de ojos, enfoque rack progresivo, duración 5 segundos, aspecto 16:9, estilo cinematográfico profesional"

2. PROMPT NEGATIVO:
   - "cámara inestable, movimiento brusco, sacudidas, desenfoque de movimiento, trayectoria errática"
   - Agregar: "movimiento robótico, aceleración/desaceleración abrupta, pérdida de estabilización"

IMPORTANTE:
- Todo en ESPAÑOL
- Enfoque en MOVIMIENTOS PROFESIONALES y SUAVES
- Especificar claramente la trayectoria de cámara
- Tono de cinematografía profesional

FORMATO DE RESPUESTA:
POSITIVE:
[descripción técnica del movimiento de cámara]

NEGATIVE:
[elementos a evitar en el movimiento]"""
    
    # ==================== UTILIDADES ====================
    
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
        seccion_actual = None
        
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
        return {
            "positivo": prompt_positivo.strip(),
            "negativo": prompt_negativo.strip() if prompt_negativo else "baja calidad, borroso, distorsionado, anatomía incorrecta"
        }
