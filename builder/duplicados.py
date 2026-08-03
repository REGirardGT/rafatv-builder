# ==========================================
# RafaTV Builder
# Detector de duplicados
# ==========================================

"""
Selecciona el mejor canal entre aquellos que representan
el mismo contenido.

El comparador utiliza varios criterios de desempate
en el siguiente orden:

1. Mayor puntuación
2. HTTPS
3. Mayor resolución
4. Tiene logo
5. Tiene TVG-ID
6. Primer canal

Cada decisión queda registrada para auditoría.
"""

from collections import defaultdict

AUDITORIA_DUPLICADOS = []


# ==========================================
# Auditoría
# ==========================================

def registrar_decision(ganador, perdedor, motivo):

    AUDITORIA_DUPLICADOS.append({

        "canal": ganador.nombre,
        "motivo": motivo,

        "ganador": {
            "nombre": ganador.nombre,
            "puntuacion": ganador.puntuacion,
            "dominio": ganador.dominio,
            "url": ganador.url,
            "detalle": list(ganador.detalle_puntuacion)
        },

        "perdedor": {
            "nombre": perdedor.nombre,
            "puntuacion": perdedor.puntuacion,
            "dominio": perdedor.dominio,
            "url": perdedor.url,
            "detalle": list(perdedor.detalle_puntuacion)
        }

    })


def elegir(ganador, perdedor, motivo):

    registrar_decision(
        ganador,
        perdedor,
        motivo
    )

    return ganador


# ==========================================
# Resolución
# ==========================================

def valor_resolucion(nombre):

    nombre = nombre.lower()

    if "uhd" in nombre:
        return 70

    if "4k" in nombre:
        return 60

    if "1080p" in nombre:
        return 50

    if "1080" in nombre:
        return 45

    if "fhd" in nombre:
        return 40

    if "720p" in nombre:
        return 30

    if "720" in nombre:
        return 25

    if "hd" in nombre:
        return 20

    if "sd" in nombre:
        return 10

    return 0


# ==========================================
# Agrupar
# ==========================================

def agrupar_por_nombre(canales):

    grupos = defaultdict(list)

    for canal in canales:
        grupos[canal.nombre_normalizado].append(canal)

    return grupos


# ==========================================
# Comparador
# ==========================================

def comparar_canales(canal_a, canal_b):

    # 1. Mayor puntuación

    if canal_a.puntuacion != canal_b.puntuacion:

        if canal_a.puntuacion > canal_b.puntuacion:
            return elegir(
                canal_a,
                canal_b,
                "Mayor puntuación"
            )

        return elegir(
            canal_b,
            canal_a,
            "Mayor puntuación"
        )

    # 2. HTTPS

    a_https = canal_a.url.startswith("https://")
    b_https = canal_b.url.startswith("https://")

    if a_https != b_https:

        if a_https:
            return elegir(
                canal_a,
                canal_b,
                "HTTPS"
            )

        return elegir(
            canal_b,
            canal_a,
            "HTTPS"
        )

    # 3. Resolución

    valor_a = valor_resolucion(canal_a.nombre)
    valor_b = valor_resolucion(canal_b.nombre)

    if valor_a != valor_b:

        if valor_a > valor_b:
            return elegir(
                canal_a,
                canal_b,
                "Mayor resolución"
            )

        return elegir(
            canal_b,
            canal_a,
            "Mayor resolución"
        )

    # 4. Logo

    a_logo = canal_a.logo.strip() != ""
    b_logo = canal_b.logo.strip() != ""

    if a_logo != b_logo:

        if a_logo:
            return elegir(
                canal_a,
                canal_b,
                "Tiene logo"
            )

        return elegir(
            canal_b,
            canal_a,
            "Tiene logo"
        )

    # 5. TVG-ID

    a_tvg = canal_a.tvg_id.strip() != ""
    b_tvg = canal_b.tvg_id.strip() != ""

    if a_tvg != b_tvg:

        if a_tvg:
            return elegir(
                canal_a,
                canal_b,
                "Tiene TVG-ID"
            )

        return elegir(
            canal_b,
            canal_a,
            "Tiene TVG-ID"
        )

    # 6. Primer canal

    return elegir(
        canal_a,
        canal_b,
        "Primer canal"
    )


# ==========================================
# Selección final
# ==========================================

def seleccionar_mejores(canales):

    grupos = agrupar_por_nombre(canales)

    mejores = []

    for lista in grupos.values():

        mejor = lista[0]

        for candidato in lista[1:]:

            mejor = comparar_canales(
                mejor,
                candidato
            )

        mejores.append(mejor)

    return mejores