"""
Utilidades para PROMPTS IA
Funciones auxiliares para manejo de archivos y configuración
"""
import os
import json
from datetime import datetime
from typing import Optional, List, Dict


def cargar_api_key() -> Optional[str]:
    """
    Carga la API key de Gemini desde el archivo api_key.txt
    
    Busca el archivo en el mismo directorio que el script.
    
    Returns:
        str or None: La API key si se encuentra, None en caso contrario
    """
    # Obtener el directorio raíz del proyecto
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
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


def guardar_historial(entrada: Dict) -> None:
    """
    Guarda un prompt generado en el historial
    
    Args:
        entrada: Diccionario con los datos del prompt generado
    """
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    historial_path = os.path.join(script_dir, "history.json")
    
    # Cargar historial existente
    historial = cargar_historial()
    
    # Agregar nueva entrada con timestamp
    entrada['timestamp'] = datetime.now().isoformat()
    historial.append(entrada)
    
    # Guardar historial actualizado
    try:
        with open(historial_path, 'w', encoding='utf-8') as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error al guardar historial: {e}")


def cargar_historial() -> List[Dict]:
    """
    Carga el historial de prompts generados
    
    Returns:
        Lista de diccionarios con el historial
    """
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    historial_path = os.path.join(script_dir, "history.json")
    
    try:
        with open(historial_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def exportar_prompts(prompt_positivo: str, prompt_negativo: str, metadata: Dict) -> str:
    """
    Exporta prompts a un archivo de texto
    
    Args:
        prompt_positivo: Prompt positivo generado
        prompt_negativo: Prompt negativo generado
        metadata: Información adicional (categoría, tipo de medio, etc.)
        
    Returns:
        Ruta del archivo generado
    """
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exports_dir = os.path.join(script_dir, "exports")
    
    # Crear directorio de exportaciones si no existe
    os.makedirs(exports_dir, exist_ok=True)
    
    # Generar nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prompt_{timestamp}.txt"
    filepath = os.path.join(exports_dir, filename)
    
    # Crear contenido del archivo
    contenido = f"""╔══════════════════════════════════════════════════════════════╗
║              PROMPTS IA - Prompt Exportado                   ║
╚══════════════════════════════════════════════════════════════╝

📅 Fecha: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
🎬 Tipo de Medio: {metadata.get('tipo_medio', 'N/A')}
📂 Categoría: {metadata.get('categoria', 'N/A')}
🎨 Estilo: {metadata.get('estilo', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 DESCRIPCIÓN:
{metadata.get('descripcion', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PROMPT POSITIVO:
{prompt_positivo}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚫 PROMPT NEGATIVO:
{prompt_negativo}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generado con PROMPTS IA - Powered by Gemini 2.5 Flash
"""
    
    # Guardar archivo
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return filepath
    except Exception as e:
        raise Exception(f"Error al exportar: {e}")
