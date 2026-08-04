# ==========================================
# RafaTV Builder
# Exportador M3U Inteligente
# ==========================================

from pathlib import Path
from builder.filtros import limpiar_grupo

# User-Agent estándar para evitar bloqueos HTTP 403 en reproductores IPTV
USER_AGENT_DEFAULT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

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

    # Grupo / Categoría (Prioriza el group_title normalizado en main.py)
    grupo_base = getattr(canal, "group_title", getattr(canal, "grupo", "General"))
    grupo_limpio = limpiar_grupo(grupo_base)
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
            
            # Directiva para que TiviMate / VLC envíen el User-Agent (Previene error 403)
            user_agent = getattr(canal, "user_agent", USER_AGENT_DEFAULT)
            f.write(f'#EXTVLCOPT:http-user-agent={user_agent}\n')
            
            # URL del canal
            f.write(canal.url + "\n")