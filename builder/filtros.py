# ==========================================
# RafaTV Builder
# Módulo de filtros y listas de control
# ==========================================

from pathlib import Path

def _cargar_lineas_config(nombre_archivo):
    archivo = Path(f"config/{nombre_archivo}")
    elementos = []

    if not archivo.exists():
        return elementos

    with open(archivo, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            elementos.append(linea.lower())

    return elementos


PALABRAS_PROHIBIDAS = _cargar_lineas_config("palabras_prohibidas.txt")
CANALES_EXCLUIDOS = _cargar_lineas_config("canales_excluidos.txt")
GRUPOS_PREFERIDOS = _cargar_lineas_config("grupos_preferidos.txt")


def canal_permitido(canal):
    texto = " ".join([
        canal.nombre,
        canal.grupo,
        canal.tvg_id,
        canal.url
    ]).lower()

    nombre = canal.nombre.lower().strip()

    if nombre in CANALES_EXCLUIDOS:
        return False, "Canal excluido de la lista"

    for palabra in PALABRAS_PROHIBIDAS:
        if palabra in texto:
            return False, f"Palabra prohibida: {palabra}"

    return True, ""


def limpiar_grupo(grupo_original):
    """
    Formatea el nombre del grupo para que luzca limpio en TiviMate / Samsung.
    """
    if not grupo_original:
        return "General"
    
    # Capitalizar la primera letra y quitar etiquetas raras
    grupo = grupo_original.strip().title()
    return grupo