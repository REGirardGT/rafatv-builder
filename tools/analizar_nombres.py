# ==========================================
# RafaTV Builder
# Analizador de nombres normalizados
# ==========================================

from pathlib import Path
from collections import Counter

from builder.parser import leer_canales
from builder.normalizador import normalizar_nombre


archivo = Path("source/spa.m3u")

lineas = archivo.read_text(
    encoding="utf-8",
    errors="ignore"
).splitlines()

canales = leer_canales(lineas)

contador = Counter()

for canal in canales:

    nombre = normalizar_nombre(canal.nombre)

    contador[nombre] += 1


print("=" * 50)
print("TOP 50 NOMBRES MÁS REPETIDOS")
print("=" * 50)

for nombre, cantidad in contador.most_common(50):

    if cantidad > 1:

        print(f"{cantidad:3}   {nombre}")