from builder.canal import Canal
from builder.duplicados import comparar_canales

a = Canal(
    nombre="ESPN HD",
    url="https://canal1",
)

b = Canal(
    nombre="ESPN FHD",
    url="https://canal2",
)

a.puntuacion = 100
b.puntuacion = 100

ganador = comparar_canales(a, b)

print("Ganador:")
print("URL:", ganador.url)