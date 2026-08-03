# ==========================================
# RafaTV Builder
# Parser de Playlists IPTV (Local y Remoto)
# ==========================================

import re
import urllib.request
from pathlib import Path
from builder.canal import Canal

def extraer_atributo(linea, atributo):
    """
    Extrae el valor de un atributo de una línea #EXTINF.
    Ejemplo: tvg-id="espn.us", group-title="Deportes"
    """
    patron = rf'{atributo}="([^"]*)"'
    resultado = re.search(patron, linea)
    if resultado:
        return resultado.group(1)
    return ""


def obtener_contenido_fuente(origen):
    """
    Lee las líneas desde una URL remota (http/https) o un archivo local.
    """
    lineas = []
    
    if origen.startswith("http://") or origen.startswith("https://"):
        print(f"Descargando playlist remota desde: {origen}")
        try:
            req = urllib.request.Request(
                origen, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=15) as respuesta:
                contenido = respuesta.read().decode('utf-8', errors='ignore')
                lineas = contenido.splitlines()
            print(f" Descarga exitosa. ({len(lineas)} líneas obtenidas)")
        except Exception as e:
            print(f" Error al descargar la playlist remota: {e}")
            return []
    else:
        archivo = Path(origen)
        if not archivo.exists():
            print(f" No se encontró el archivo local: {origen}")
            return []
        
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            lineas = f.readlines()

    return lineas


def leer_canales(fuente):
    """
    Procesa un archivo local, una URL remota o una lista de fuentes.
    """
    # Si la fuente es una lista de URLs/archivos, las procesa recursivamente
    if isinstance(fuente, list):
        todos_los_canales = []
        for f in fuente:
            todos_los_canales.extend(leer_canales(f))
        return todos_los_canales

    # Si es un string (ruta local o URL)
    lineas = obtener_contenido_fuente(fuente) if isinstance(fuente, str) else fuente
    canales = []

    for i, linea in enumerate(lineas):
        linea_str = linea.strip() if isinstance(linea, str) else linea

        if not linea_str.startswith("#EXTINF"):
            continue

        # Extraer el nombre visible del canal
        nombre = linea_str.split(",")[-1].strip()

        # Extraer metadatos
        grupo = extraer_atributo(linea_str, "group-title")
        tvg_id = extraer_atributo(linea_str, "tvg-id")
        logo = extraer_atributo(linea_str, "tvg-logo")
        pais = extraer_atributo(linea_str, "tvg-country")
        idioma = extraer_atributo(linea_str, "tvg-language")

        url = ""

        # Buscar la primera línea que no sea un comentario para la URL de streaming
        if i + 1 < len(lineas):
            j = i + 1
            while j < len(lineas):
                siguiente = lineas[j].strip()
                if siguiente and not siguiente.startswith("#"):
                    url = siguiente
                    break
                j += 1

        if not url:
            continue

        canal = Canal(
            nombre=nombre,
            grupo=grupo,
            tvg_id=tvg_id,
            url=url,
            extinf=linea_str
        )

        canal.logo = logo
        canal.pais = pais
        canal.idioma = idioma

        canales.append(canal)

    return canales