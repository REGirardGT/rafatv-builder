# ==========================================
# RafaTV Builder
# Validador de configuración
# ==========================================

CLAVES_OBLIGATORIAS = [
    "bonificacion_favorito",
    "bonificacion_grupo",
    "bonificacion_pais",

    "peso_tvg_id",
    "peso_grupo",
    "peso_logo",

    "peso_https",
    "peso_http",

    "peso_1080",
    "peso_720",
    "peso_hd",
    "peso_sd",

    "playlist_entrada",
    "playlist_salida",

    "verificar_online"
]


def validar_configuracion(configuracion):

    faltantes = []

    for clave in CLAVES_OBLIGATORIAS:

        if clave not in configuracion:
            faltantes.append(clave)

    return faltantes