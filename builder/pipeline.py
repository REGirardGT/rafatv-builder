# =======================================
# RafaTV Builder v1
# Leer la informacion de cada canal
# =======================================

from pathlib import Path

from parser import leer_canales
from filtros import canal_permitido
from reporte import generar_reporte
from exportador import exportar_m3u
from normalizador import normalizar_nombre
from puntuacion import calcular_puntuacion
from duplicados import seleccionar_mejores
from pais import detectar_pais

print("=" * 40)
print("     RafaTV Builder v1")
print("=" * 40)

# Ruta del archivo
archivo = Path("source/spa.m3u")

# Verificar si existe
if not archivo.exists():
    print("\nError")
    print("No se encontro el archivo")
    exit()

print(f"\nArchivo: {archivo.name}")

# Leer archivo
lineas = archivo.read_text(
    encoding="utf-8",
    errors="ignore"
).splitlines()

canales = leer_canales(lineas)

print()
print(f"Canales encontrados: {len(canales):,}")

print ("\nPrimeros 10 canales:\n")

canales_filtrados = []

for canal in canales:

    canal.nombre_normalizado = normalizar_nombre(canal.nombre)

    canal.pais = detectar_pais(canal.tvg_id)

    canal.puntuacion = calcular_puntuacion(canal)

    permitido, motivo = canal_permitido(canal)

    canal.motivo = motivo

    if permitido:
        canal.activo = True
        canales_filtrados.append(canal)
    else:
        canal.activo = False

canales_filtrados = seleccionar_mejores(canales_filtrados)

canales_filtrados.sort(
    key=lambda canal: canal.puntuacion,
    reverse=True
)

print()
print(f"Canales originales : {len(canales)}")
print(f"Canales filtrados  : {len(canales_filtrados)}")
print(f"Eliminados         : {len(canales)-len(canales_filtrados)}")

for canal in canales_filtrados[:10]:
    print(f" {canal.nombre}")
    print(f" Puntuacion: {canal.puntuacion}")
    print(f" Normalizado: {canal.nombre_normalizado}")
    print(f" Grupo: {canal.grupo}")
    print(f" Paìs: {canal.pais}")
    print(f" tvg-id: {canal.tvg_id}")
    print()

generar_reporte(canales_filtrados)

print()
print("Reporte generado correctamente")
print("Archivo: output/reporte_V1.txt")

exportar_m3u(
    canales_filtrados,
    "output/RafaTV_filtrado.m3u"
)

print()
print("Playlist exportada correctamente")
print("Archivo: output/RafaTV_filtrado.m3u")