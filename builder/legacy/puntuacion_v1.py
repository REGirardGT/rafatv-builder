# ==========================================
# RafaTV Builder
# Motor de puntuación
# ==========================================

from configuracion import (
    CANALES_FAVORITOS,
    GRUPOS_PRIORITARIOS,
    PAISES_PRIORITARIOS,
    CONFIGURACION
)

def calcular_puntuacion(canal):

    puntos = 0

    # ----------------------------------
    # Información disponible
    # ----------------------------------

    if canal.tvg_id.strip():
        puntos += 20

    if canal.grupo.strip():
        puntos += 10

    if canal.logo.strip():
        puntos += 10

    # ----------------------------------
    # País prioritario
    # ----------------------------------

    if canal.pais in PAISES_PRIORITARIOS:
        puntos += CONFIGURACION["bonificacion_pais"]

    # ----------------------------------
    # Calidad del nombre
    # ----------------------------------

    nombre = canal.nombre_normalizado

    if "1080" in nombre:
        puntos += 30

    elif "720" in nombre:
        puntos += 20

    elif "hd" in nombre:
        puntos += 15

    elif "sd" in nombre:
        puntos += 5

    # ----------------------------------
    # Preferencias del usuario
    # ----------------------------------

    nombre = canal.nombre_normalizado.lower()

    if nombre in CANALES_FAVORITOS:
        puntos += CONFIGURACION["bonificacion_favorito"]

    grupo = canal.grupo.lower()

    if grupo in GRUPOS_PRIORITARIOS:
        puntos += CONFIGURACION["bonificacion_grupo"]

    pais = canal.pais.lower()

    if pais in PAISES_PRIORITARIOS:
        puntos += CONFIGURACION["bonificacion_pais"]

    # ----------------------------------
    # Preferencias del usuario
    # ----------------------------------

    if canal.nombre_normalizado in CANALES_FAVORITOS:
        puntos += CONFIGURACION["bonificacion_favorito"]

    if canal.grupo.lower() in GRUPOS_PRIORITARIOS:
        puntos += CONFIGURACION["bonificacion_grupo"]

    if canal.pais.lower() in PAISES_PRIORITARIOS:
        puntos += CONFIGURACION["bonificacion_pais"]

    # ----------------------------------
    # Penalizaciones
    # ----------------------------------

    if "backup" in nombre:
        puntos -= 15

    if "geo-blocked" in nombre:
        puntos -= 10

    # ----------------------------------
    # URL
    # ----------------------------------

    if canal.url.startswith("https://"):
        puntos += 10

    elif canal.url.startswith("http://"):
        puntos += 5

    return puntos