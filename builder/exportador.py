# ==========================================
# RafaTV Builder
# Exportador M3U Inteligente
# ==========================================

from pathlib import Path
from builder.filtros import limpiar_grupo

def reconstruir_extinf(canal):
    """
    Construye la línea #EXTINF con sintaxis estándar para Smart TVs y TiviMate.
    """
    atributos = []

    # TVG-ID (Clave para sincronizar la guía EPG)
    if hasattr(canal, "tvg_id") and canal.tvg_id:
        atributos.append(f'tvg-id="{canal.tvg_id}"')

    # Nombre alternativo/EPG
    atributos.append(f'tvg-name="{canal.nombre}"')

    # Logo del canal
    if hasattr(canal, "logo") and canal.logo:
        atributos.append(f'tvg-logo="{canal.logo}"')

    # País (opcional para reproductores avanzados)
    if hasattr(canal, "pais") and canal.pais:
        atributos.append(f'tvg-country="{canal.pais}"')

    # Idioma
    if hasattr(canal, "idioma") and canal.idioma:
        atributos.append(f'tvg-language="{canal.idioma}"')

    # Grupo / Categoría (Fundamental para la organización en pantalla)
    grupo_limpio = limpiar_grupo(canal.grupo)
    atributos.append(f'group-title="{grupo_limpio}"')

    cadena_atributos = " ".join(atributos)
    
    # Formato final estándar M3U Plus
    return f'#EXTINF:-1 {cadena_atributos},{canal.nombre}'


def exportar_m3u(canales, archivo_salida):
    salida = Path(archivo_salida)
    salida.parent.mkdir(parents=True, exist_ok=True)

    with open(salida, "w", encoding="utf-8") as f:
        # Cabecera principal con soporte EPG
        f.write('#EXTM3U x-tvg-url=""\n')

        for canal in canales:
            # Generar tag enriquecido
            linea_extinf = reconstruir_extinf(canal)
            f.write(linea_extinf + "\n")
            f.write(canal.url + "\n")