"""
Interfaz Gráfica para PROMPTS IA
GUI moderna con CustomTkinter - Soporte para Imágenes y Videos
"""
import threading
from typing import Dict, Optional
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

from .generator import GeminiPromptGenerator
from .utils import guardar_historial, cargar_historial, exportar_prompts


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
        "accent_secondary": "#6b7c9a",
        "accent_danger": "#c75450",
        "text_primary": "#e8e8e8",
        "text_secondary": "#a0a0a0",
        "border": "#3a3f4b"
    }
    
    def __init__(self, root, api_key):
        self.root = root
        self.root.title("PROMPTS IA - Generador de Prompts para Imágenes y Videos")
        self.root.geometry("950x900")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        try:
            self.generator = GeminiPromptGenerator(api_key)
        except Exception as e:
            self.mostrar_error(f"Error al inicializar Gemini: {str(e)}")
            self.root.destroy()
            return
        
        # Variables de estado
        self.tipo_medio_actual = "imagen"  # "imagen" o "video"
        self.ultimo_prompt_generado = None  # Para exportar
        
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
            text="PROMPTS IA",
            font=("Helvetica", 26, "bold"),
            text_color=self.COLORS["text_primary"]
        )
        title_label.pack(pady=(15, 3))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Generador Inteligente de Prompts • Imágenes & Videos • Powered by Gemini 2.5 Flash",
            font=("Helvetica", 10),
            text_color=self.COLORS["text_secondary"]
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Botones de acción en el header
        action_buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        action_buttons_frame.pack(pady=(0, 12))
        
        historial_btn = ctk.CTkButton(
            action_buttons_frame,
            text="📜 Historial",
            font=("Helvetica", 11),
            fg_color=self.COLORS["accent_secondary"],
            hover_color="#5a6b8a",
            width=120,
            height=32,
            corner_radius=6,
            command=self.abrir_historial
        )
        historial_btn.pack(side="left", padx=5)
        
        exportar_btn = ctk.CTkButton(
            action_buttons_frame,
            text="💾 Exportar",
            font=("Helvetica", 11),
            fg_color=self.COLORS["accent_secondary"],
            hover_color="#5a6b8a",
            width=120,
            height=32,
            corner_radius=6,
            command=self.exportar_prompt_actual
        )
        exportar_btn.pack(side="left", padx=5)
        
        # Scrollable main container
        scrollable_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color="transparent",
            scrollbar_button_color=self.COLORS["bg_tertiary"],
            scrollbar_button_hover_color=self.COLORS["accent_primary"]
        )
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=(10, 15))
        
        # ========== SELECTOR DE TIPO DE MEDIO ==========
        media_type_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.COLORS["bg_secondary"], corner_radius=10)
        media_type_frame.pack(fill="x", pady=(0, 15))
        
        media_label = ctk.CTkLabel(
            media_type_frame,
            text="🎯 Tipo de Medio:",
            font=("Helvetica", 13, "bold"),
            text_color=self.COLORS["text_primary"]
        )
        media_label.pack(side="left", padx=15, pady=12)
        
        self.media_type_var = ctk.StringVar(value="🖼️ Imagen")
        media_segmented = ctk.CTkSegmentedButton(
            media_type_frame,
            variable=self.media_type_var,
            values=["🖼️ Imagen", "🎬 Video"],
            font=("Helvetica", 12, "bold"),
            fg_color=self.COLORS["bg_tertiary"],
            selected_color=self.COLORS["accent_primary"],
            selected_hover_color="#4a7449",
            unselected_color=self.COLORS["bg_tertiary"],
            unselected_hover_color=self.COLORS["border"],
            command=self.cambiar_tipo_medio
        )
        media_segmented.pack(side="left", padx=10, pady=12)
        
        # Category selector
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
        self.category_combo = ctk.CTkComboBox(
            category_frame,
            variable=self.category_var,
            values=list(self.generator.categorias_imagen.keys()),
            font=("Helvetica", 11),
            width=280,
            height=32,
            fg_color=self.COLORS["bg_secondary"],
            border_color=self.COLORS["border"],
            button_color=self.COLORS["bg_tertiary"],
            button_hover_color=self.COLORS["accent_primary"],
            dropdown_fg_color=self.COLORS["bg_secondary"],
            command=self.actualizar_campos_dinamicos
        )
        self.category_combo.pack(side="left")
        
        # Dynamic fields container
        self.dynamic_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        
        # Input section
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
            height=90,
            font=("Helvetica", 11),
            fg_color=self.COLORS["bg_secondary"],
            border_color=self.COLORS["border"],
            border_width=1,
            corner_radius=8
        )
        self.input_text.pack(fill="x", pady=(0, 10))
        
        # Habilitar pegado con Cmd+V (Mac) y Ctrl+V (Windows/Linux)
        self.input_text.bind("<Command-v>", lambda e: self._pegar_texto())
        self.input_text.bind("<Control-v>", lambda e: self._pegar_texto())

        
        # Style selector
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
            width=280,
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
            font=("Helvetica", 14, "bold"),
            fg_color=self.COLORS["accent_primary"],
            hover_color="#4a7449",
            height=45,
            corner_radius=8,
            command=self.generar_prompts
        )
        self.generate_btn.pack(pady=(0, 20))
        
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
            height=130,
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
            height=110,
            font=("Helvetica", 10),
            fg_color=self.COLORS["bg_tertiary"],
            border_width=0,
            corner_radius=0,
            wrap="word"
        )
        self.negative_text.pack(fill="x", padx=12, pady=(0, 10))
    
    def cambiar_tipo_medio(self, valor):
        """Cambia entre modo Imagen y Video"""
        if "Imagen" in valor:
            self.tipo_medio_actual = "imagen"
            self.category_var.set("🖼️ Generación desde Cero")
            self.category_combo.configure(values=list(self.generator.categorias_imagen.keys()))
        else:
            self.tipo_medio_actual = "video"
            self.category_var.set("🎬 Generación desde Cero")
            self.category_combo.configure(values=list(self.generator.categorias_video.keys()))
        
        self.actualizar_campos_dinamicos()
    
    def actualizar_campos_dinamicos(self, *args):
        """Actualiza los campos dinámicos según la categoría y tipo de medio seleccionados"""
        # Limpiar campos dinámicos anteriores
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        
        if self.tipo_medio_actual == "imagen":
            self._crear_campos_imagen()
        else:
            self._crear_campos_video()
    
    def _crear_campos_imagen(self):
        """Crea campos específicos para generación de imágenes"""
        categoria = self.generator.categorias_imagen.get(self.category_var.get(), "generate")
        
        if categoria == "face_transform":
            self.dynamic_frame.pack(fill="x", pady=(0, 10), before=self.input_text)
            
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
            self.dynamic_frame.pack(fill="x", pady=(0, 10), before=self.input_text)
            
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
            self.dynamic_frame.pack(fill="x", pady=(0, 10), before=self.input_text)
            
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
            # Para "generate" no hay campos adicionales
            self.dynamic_frame.pack_forget()
    
    def _crear_campos_video(self):
        """Crea campos específicos para generación de videos"""
        self.dynamic_frame.pack(fill="x", pady=(0, 10), before=self.input_text)
        
        categoria = self.generator.categorias_video.get(self.category_var.get(), "video_generate")
        
        # Duración
        duracion_label = ctk.CTkLabel(
            self.dynamic_frame,
            text="⏱️ Duración:",
            font=("Helvetica", 11, "bold"),
            text_color=self.COLORS["text_primary"]
        )
        duracion_label.pack(anchor="w", pady=(0, 4))
        
        duracion_frame = ctk.CTkFrame(self.dynamic_frame, fg_color="transparent")
        duracion_frame.pack(anchor="w", pady=(0, 8))
        
        self.duracion_var = ctk.StringVar(value="5s")
        duracion_presets = ["3s", "5s", "10s", "30s", "1min", "Personalizado"]
        duracion_combo = ctk.CTkComboBox(
            duracion_frame,
            variable=self.duracion_var,
            values=duracion_presets,
            font=("Helvetica", 10),
            width=150,
            height=32,
            fg_color=self.COLORS["bg_secondary"],
            border_color=self.COLORS["border"],
            button_color=self.COLORS["bg_tertiary"],
            button_hover_color=self.COLORS["accent_primary"],
            dropdown_fg_color=self.COLORS["bg_secondary"],
            command=self._toggle_duracion_personalizada
        )
        duracion_combo.pack(side="left", padx=(0, 10))
        
        self.duracion_entry = ctk.CTkEntry(
            duracion_frame,
            placeholder_text="ej: 2min, 45s",
            font=("Helvetica", 10),
            width=120,
            height=32,
            fg_color=self.COLORS["bg_secondary"],
            border_color=self.COLORS["border"]
        )
        # Inicialmente oculto
        
        # Relación de aspecto
        aspecto_label = ctk.CTkLabel(
            self.dynamic_frame,
            text="📐 Relación de aspecto:",
            font=("Helvetica", 11, "bold"),
            text_color=self.COLORS["text_primary"]
        )
        aspecto_label.pack(anchor="w", pady=(0, 4))
        
        self.aspecto_var = ctk.StringVar(value="16:9")
        aspecto_combo = ctk.CTkComboBox(
            self.dynamic_frame,
            variable=self.aspecto_var,
            values=["16:9 (Horizontal)", "9:16 (Vertical)", "1:1 (Cuadrado)", "4:3 (Clásico)"],
            font=("Helvetica", 10),
            width=200,
            height=32,
            fg_color=self.COLORS["bg_secondary"],
            border_color=self.COLORS["border"],
            button_color=self.COLORS["bg_tertiary"],
            button_hover_color=self.COLORS["accent_primary"],
            dropdown_fg_color=self.COLORS["bg_secondary"]
        )
        aspecto_combo.pack(anchor="w", pady=(0, 8))
        
        # Movimiento de cámara
        camara_label = ctk.CTkLabel(
            self.dynamic_frame,
            text="🎥 Movimiento de cámara:",
            font=("Helvetica", 11, "bold"),
            text_color=self.COLORS["text_primary"]
        )
        camara_label.pack(anchor="w", pady=(0, 4))
        
        self.movimiento_camara_var = ctk.StringVar(value="Estático")
        movimientos = ["Estático", "Paneo (Izq/Der)", "Zoom (Acercar/Alejar)", "Dolly", "Tracking"]
        camara_combo = ctk.CTkComboBox(
            self.dynamic_frame,
            variable=self.movimiento_camara_var,
            values=movimientos,
            font=("Helvetica", 10),
            width=220,
            height=32,
            fg_color=self.COLORS["bg_secondary"],
            border_color=self.COLORS["border"],
            button_color=self.COLORS["bg_tertiary"],
            button_hover_color=self.COLORS["accent_primary"],
            dropdown_fg_color=self.COLORS["bg_secondary"]
        )
        camara_combo.pack(anchor="w", pady=(0, 8))
        
        # Intensidad de movimiento
        intensidad_label = ctk.CTkLabel(
            self.dynamic_frame,
            text="💫 Intensidad de movimiento:",
            font=("Helvetica", 11, "bold"),
            text_color=self.COLORS["text_primary"]
        )
        intensidad_label.pack(anchor="w", pady=(0, 4))
        
        self.intensidad_var = ctk.StringVar(value="Media")
        intensidad_combo = ctk.CTkComboBox(
            self.dynamic_frame,
            variable=self.intensidad_var,
            values=["Baja", "Media", "Alta"],
            font=("Helvetica", 10),
            width=150,
            height=32,
            fg_color=self.COLORS["bg_secondary"],
            border_color=self.COLORS["border"],
            button_color=self.COLORS["bg_tertiary"],
            button_hover_color=self.COLORS["accent_primary"],
            dropdown_fg_color=self.COLORS["bg_secondary"]
        )
        intensidad_combo.pack(anchor="w", pady=(0, 5))
        
        # Campos específicos por categoría de video
        if categoria == "video_effects":
            tipo_efecto_label = ctk.CTkLabel(
                self.dynamic_frame,
                text="✨ Tipo de efecto:",
                font=("Helvetica", 11, "bold"),
                text_color=self.COLORS["text_primary"]
            )
            tipo_efecto_label.pack(anchor="w", pady=(8, 4))
            
            self.tipo_efecto_video_var = ctk.StringVar(value="Iluminación")
            tipo_efecto_combo = ctk.CTkComboBox(
                self.dynamic_frame,
                variable=self.tipo_efecto_video_var,
                values=["Iluminación", "Clima", "Transición", "Color Grading", "Partículas"],
                font=("Helvetica", 10),
                width=200,
                height=32,
                fg_color=self.COLORS["bg_secondary"],
                border_color=self.COLORS["border"],
                button_color=self.COLORS["bg_tertiary"],
                button_hover_color=self.COLORS["accent_primary"],
                dropdown_fg_color=self.COLORS["bg_secondary"]
            )
            tipo_efecto_combo.pack(anchor="w", pady=(0, 5))
    
    def _toggle_duracion_personalizada(self, valor):
        """Muestra/oculta el campo de duración personalizada"""
        if valor == "Personalizado":
            self.duracion_entry.pack(side="left")
        else:
            self.duracion_entry.pack_forget()
    
    def copiar_texto(self, text_widget):
        """Copia el texto del widget especificado al portapapeles"""
        texto = text_widget.get("1.0", "end-1c").strip()
        if texto:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
            self.mostrar_notificacion("✅ Copiado", "Texto copiado al portapapeles")
        else:
            self.mostrar_notificacion("⚠️ Advertencia", "No hay texto para copiar")
    
    def _pegar_texto(self):
        """Pega texto del portapapeles en el campo de entrada"""
        try:
            texto = self.root.clipboard_get()
            if texto:
                # Insertar en la posición del cursor
                self.input_text.insert("insert", texto)
                return "break"  # Prevenir el comportamiento por defecto
        except:
            pass
        return "break"
    
    def mostrar_notificacion(self, titulo, mensaje):
        """Muestra una ventana de notificación modal temporal"""
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
        """Genera los prompts usando Gemini 2.5 Flash de forma asíncrona"""
        descripcion = self.input_text.get("1.0", "end-1c").strip()
        
        if not descripcion:
            self.mostrar_notificacion("⚠️ Advertencia", "Por favor, describe tu idea primero")
            return
        
        # Deshabilitar el botón mientras se genera
        self.generate_btn.configure(state="disabled", text="🤖 Generando...")
        
        # Limpiar los campos de resultados anteriores
        self.positive_text.delete("1.0", "end")
        self.negative_text.delete("1.0", "end")
        
        def generar():
            try:
                # Obtener categoría y estilo
                if self.tipo_medio_actual == "imagen":
                    categoria = self.generator.categorias_imagen[self.category_var.get()]
                else:
                    categoria = self.generator.categorias_video[self.category_var.get()]
                
                estilo = self.generator.estilos[self.style_var.get()]
                
                # Recopilar detalles extra
                detalles_extra = self._recopilar_detalles_extra(categoria)
                
                # Generar los prompts
                prompts = self.generator.generar_prompt_con_ia(
                    self.tipo_medio_actual,
                    categoria,
                    descripcion,
                    estilo,
                    detalles_extra
                )
                
                # Guardar en historial
                entrada_historial = {
                    "tipo_medio": self.tipo_medio_actual,
                    "categoria": self.category_var.get(),
                    "descripcion": descripcion,
                    "estilo": self.style_var.get(),
                    "prompt_positivo": prompts['positivo'],
                    "prompt_negativo": prompts['negativo'],
                    "detalles": detalles_extra
                }
                guardar_historial(entrada_historial)
                
                # Guardar para exportar
                self.ultimo_prompt_generado = entrada_historial
                
                # Actualizar la UI
                self.root.after(0, lambda: self.mostrar_resultados(prompts))
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.mostrar_notificacion("❌ Error", f"Error al generar: {error_msg}"))
            finally:
                self.root.after(0, lambda: self.generate_btn.configure(state="normal", text="✨ Generar Prompts"))
        
        # Ejecutar en hilo separado
        threading.Thread(target=generar, daemon=True).start()
    
    def _recopilar_detalles_extra(self, categoria):
        """Recopila detalles extra según la categoría"""
        detalles = {}
        
        if self.tipo_medio_actual == "imagen":
            if categoria == "face_transform":
                detalles = {
                    "transformacion": self.transformacion_var.get(),
                    "mantener_identidad": self.identidad_var.get()
                }
            elif categoria == "modify":
                detalles = {
                    "tipo_modificacion": self.modificacion_var.get()
                }
            elif categoria == "effects":
                detalles = {
                    "tipo_efecto": self.efecto_var.get()
                }
        else:  # video
            # Obtener duración
            if self.duracion_var.get() == "Personalizado":
                duracion = self.duracion_entry.get().strip() or "5s"
            else:
                duracion = self.duracion_var.get()
            
            # Extraer solo el ratio del aspecto
            aspecto = self.aspecto_var.get().split(" ")[0]
            
            detalles = {
                "duracion": duracion,
                "aspecto": aspecto,
                "movimiento_camara": self.movimiento_camara_var.get(),
                "intensidad_movimiento": self.intensidad_var.get()
            }
            
            # Agregar tipo de efecto si aplica
            if categoria == "video_effects" and hasattr(self, 'tipo_efecto_video_var'):
                detalles["tipo_efecto"] = self.tipo_efecto_video_var.get()
        
        return detalles
    
    def mostrar_resultados(self, prompts):
        """Muestra los prompts generados en los campos de texto"""
        self.positive_text.insert("1.0", prompts['positivo'])
        self.negative_text.insert("1.0", prompts['negativo'])
    
    def exportar_prompt_actual(self):
        """Exporta el prompt actual a un archivo de texto"""
        if not self.ultimo_prompt_generado:
            self.mostrar_notificacion("⚠️ Advertencia", "No hay prompts para exportar. Genera uno primero.")
            return
        
        try:
            metadata = {
                "tipo_medio": self.ultimo_prompt_generado["tipo_medio"].capitalize(),
                "categoria": self.ultimo_prompt_generado["categoria"],
                "estilo": self.ultimo_prompt_generado["estilo"],
                "descripcion": self.ultimo_prompt_generado["descripcion"]
            }
            
            filepath = exportar_prompts(
                self.ultimo_prompt_generado["prompt_positivo"],
                self.ultimo_prompt_generado["prompt_negativo"],
                metadata
            )
            
            self.mostrar_notificacion("✅ Exportado", f"Prompt exportado exitosamente a:\n{filepath}")
        except Exception as e:
            self.mostrar_notificacion("❌ Error", f"Error al exportar: {str(e)}")
    
    def abrir_historial(self):
        """Abre la ventana de historial"""
        HistorialWindow(self.root, self)


class HistorialWindow:
    """Ventana para mostrar el historial de prompts generados"""
    
    def __init__(self, parent, gui_principal):
        self.parent = parent
        self.gui_principal = gui_principal
        
        self.window = ctk.CTkToplevel(parent)
        self.window.title("📜 Historial de Prompts")
        self.window.geometry("900x600")
        
        self.crear_interfaz()
        self.cargar_historial()
    
    def crear_interfaz(self):
        """Crea la interfaz de la ventana de historial"""
        # Header
        header = ctk.CTkFrame(self.window, fg_color=gui_principal.COLORS["bg_secondary"], corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        
        title = ctk.CTkLabel(
            header,
            text="📜 Historial de Prompts Generados",
            font=("Helvetica", 18, "bold"),
            text_color=gui_principal.COLORS["text_primary"]
        )
        title.pack(pady=15)
        
        # Scrollable frame para el historial
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.window,
            fg_color="transparent"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def cargar_historial(self):
        """Carga y muestra el historial"""
        historial = cargar_historial()
        
        if not historial:
            label = ctk.CTkLabel(
                self.scroll_frame,
                text="No hay prompts en el historial aún.",
                font=("Helvetica", 12),
                text_color=gui_principal.COLORS["text_secondary"]
            )
            label.pack(pady=50)
            return
        
        # Mostrar en orden inverso (más reciente primero)
        for i, entrada in enumerate(reversed(historial)):
            self._crear_entrada_historial(entrada, len(historial) - i)
    
    def _crear_entrada_historial(self, entrada, numero):
        """Crea una entrada visual en el historial"""
        frame = ctk.CTkFrame(self.scroll_frame, fg_color=gui_principal.COLORS["bg_secondary"], corner_radius=10)
        frame.pack(fill="x", pady=(0, 10))
        
        # Header de la entrada
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10, 5))
        
        # Número y timestamp
        timestamp = entrada.get("timestamp", "")
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                fecha_str = dt.strftime("%d/%m/%Y %H:%M")
            except:
                fecha_str = timestamp
        else:
            fecha_str = "Fecha desconocida"
        
        info_label = ctk.CTkLabel(
            header,
            text=f"#{numero} • {fecha_str} • {entrada.get('tipo_medio', 'N/A').capitalize()} • {entrada.get('categoria', 'N/A')}",
            font=("Helvetica", 10, "bold"),
            text_color=gui_principal.COLORS["text_primary"]
        )
        info_label.pack(side="left")
        
        # Descripción
        desc_label = ctk.CTkLabel(
            frame,
            text=f"📝 {entrada.get('descripcion', 'Sin descripción')[:100]}...",
            font=("Helvetica", 9),
            text_color=gui_principal.COLORS["text_secondary"],
            anchor="w"
        )
        desc_label.pack(fill="x", padx=15, pady=(0, 10))


# Variable global para acceder a los colores desde HistorialWindow
gui_principal = None

def set_gui_principal(gui):
    global gui_principal
    gui_principal = gui
