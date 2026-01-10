"""
PROMPTS IA - Generador Inteligente de Prompts
Aplicación principal - Punto de entrada

Genera prompts optimizados para herramientas de generación de imágenes y videos con IA
Powered by Google Gemini 2.5 Flash
"""
import customtkinter as ctk
from src.gui import BrainCourseGUI, set_gui_principal
from src.utils import cargar_api_key


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
        dialog.geometry("500x200")
        
        label = ctk.CTkLabel(
            dialog,
            text="❌ No se encontró la API key.\n\nCrea un archivo 'api_key.txt' en la carpeta del proyecto\ny pega tu API key de Google Gemini.\n\nPuedes obtener una en: https://makersuite.google.com/app/apikey",
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
    
    # Establecer referencia global para la ventana de historial
    set_gui_principal(app)
    
    # Iniciar el loop principal de la interfaz
    root.mainloop()


if __name__ == "__main__":
    main()
