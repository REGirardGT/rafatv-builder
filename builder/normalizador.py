# ==========================================
# RafaTV Builder
# Normalizador de nombres
# ==========================================

import re


def normalizar_nombre(nombre):

    nombre = nombre.lower()

    # Eliminar contenido entre ()
    nombre = re.sub(r"\(.*?\)", "", nombre)

    # Eliminar contenido entre []
    nombre = re.sub(r"\[.*?\]", "", nombre)

    # Palabras que no aportan al nombre
    eliminar = [
        "uhd",
        "4k",
        "fhd",
        "hd",
        "sd",
        "1080p",
        "1080",
        "720p",
        "720",
        "backup",
        "multiaudio"
    ]

    for palabra in eliminar:
        nombre = nombre.replace(palabra, "")

    # Eliminar espacios repetidos
    nombre = " ".join(nombre.split())

    return nombre.strip()

if __name__ == "__main__":

    pruebas = [
        "ESPN HD",
        "ESPN FHD",
        "ESPN (720p)",
        "ESPN [Geo-blocked]",
        "TVE Internacional HD",
        "Discovery Channel 1080p",
    ]

    for nombre in pruebas:

        print(nombre)
        print(" ->", normalizar_nombre(nombre))
        print()