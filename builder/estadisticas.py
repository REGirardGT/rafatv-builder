# ==========================================
# RafaTV Builder
# Estadísticas
# ==========================================

from collections import Counter


def contar_dominios(canales):

    contador = Counter()

    for canal in canales:

        if canal.dominio:
            contador[canal.dominio] += 1

    return contador

from collections import Counter


def contar_puntuaciones(canales):
    """
    Cuenta cuántos canales obtuvieron cada puntuación.
    """

    puntuaciones = Counter()

    for canal in canales:
        puntuaciones[canal.puntuacion] += 1

    return puntuaciones