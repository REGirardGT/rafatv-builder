# ==========================================
# RafaTV Builder
# Motor de puntuación
# ==========================================

from builder.configuracion import CONFIGURACION

def calcular_puntuacion(canal, motor):

    puntos = 0

    canal.detalle_puntuacion.clear()

    bonos = motor.calcular_bonificaciones(canal)

    # ----------------------------------
    # Información disponible
    # ----------------------------------

    if canal.tvg_id.strip():
        valor = CONFIGURACION["peso_tvg_id"]

        puntos += valor

        canal.detalle_puntuacion.append(
        ("TVG-ID válido", valor)
        )

    if canal.grupo.strip():
        valor = CONFIGURACION["peso_grupo"]

        puntos += valor

        canal.detalle_puntuacion.append(
            ("Grupo identificado", valor)
        )

    if canal.logo.strip():
        valor = CONFIGURACION["peso_logo"]

        puntos += valor

        canal.detalle_puntuacion.append(
            ("Logo", valor)
        )

    # ----------------------------------
    # Calidad del nombre
    # ----------------------------------

    nombre = canal.nombre.lower()

    if "1080" in nombre:
        valor = CONFIGURACION["peso_1080"]
        puntos += valor
        canal.detalle_puntuacion.append(("Calidad 1080p", valor))

    elif "720" in nombre:
        valor = CONFIGURACION["peso_720"]
        puntos += valor
        canal.detalle_puntuacion.append(("Calidad 720p", valor))

    elif "hd" in nombre:
        valor = CONFIGURACION["peso_hd"]
        puntos += valor
        canal.detalle_puntuacion.append(("Calidad HD", valor))

    elif "sd" in nombre:
        valor = CONFIGURACION["peso_sd"]
        puntos += valor
        canal.detalle_puntuacion.append(("Calidad SD", valor))


    # ----------------------------------
    # Bonificaciones
    # ----------------------------------

    puntos += bonos["favorito"]
    puntos += bonos["grupo"]
    puntos += bonos["pais"]
    puntos += bonos["dominio"]


    if bonos["favorito"] > 0:
        canal.detalle_puntuacion.append(
            ("Canal favorito", bonos["favorito"])
        )

    if bonos["grupo"] > 0:
        canal.detalle_puntuacion.append(
            ("Grupo preferido", bonos["grupo"])
        )

    if bonos["pais"] > 0:
        canal.detalle_puntuacion.append(
            ("País preferido", bonos["pais"])
        )

    if bonos["dominio"] > 0:
        canal.detalle_puntuacion.append(
            ("Dominio preferido", bonos["dominio"])
        )

    # ----------------------------------
    # Penalizaciones
    # ----------------------------------

    if "backup" in nombre:

        valor = CONFIGURACION["penalizacion_backup"]

        puntos += valor

        canal.detalle_puntuacion.append(
            ("Canal Backup", valor)
        )

    if "geo-blocked" in nombre:

        valor = CONFIGURACION.get(
            "penalizacion_geo_blocked",
            -10
        )

        puntos += valor

        canal.detalle_puntuacion.append(
            ("Canal geo-blocked", valor)
        )

    # ----------------------------------
    # URL
    # ----------------------------------

    if canal.url.startswith("https://"):
        valor = CONFIGURACION["peso_https"]
        puntos += valor
        canal.detalle_puntuacion.append(
            ("HTTPS", valor)
        )

    elif canal.url.startswith("http://"):
        valor = CONFIGURACION["peso_http"]
        puntos += valor
        canal.detalle_puntuacion.append(
            ("HTTP", valor)
        )

    return puntos