# ==========================================
# RafaTV Builder
# Punto de entrada de la aplicación
# ==========================================

from pathlib import Path

from builder.parser import leer_canales
from builder.normalizador import normalizar_nombre
from builder.puntuacion import calcular_puntuacion
from builder.duplicados import seleccionar_mejores, AUDITORIA_DUPLICADOS
from builder.motor_reglas import MotorReglas
from builder.configuracion import CONFIGURACION
from builder.exportador import exportar_m3u
from builder.dominio import detectar_dominio
from builder.auditoria import generar_auditoria
from builder.validador_config import validar_configuracion
from builder.estadisticas import contar_dominios, contar_puntuaciones
from builder.verificador import verificar_canales_paralelo


def main():
    print("=" * 50)
    print("        RafaTV Builder")
    print("=" * 50)
    print()

    # Validar configuración
    faltantes = validar_configuracion(CONFIGURACION)
    if faltantes:
        print("=" * 50)
        print("Error de configuración")
        print("=" * 50)
        print("\nFaltan las siguientes claves:\n")
        for clave in faltantes:
            print(f" - {clave}")
        print("\nRevise config/configuracion.json")
        return

    canales = leer_canales(CONFIGURACION["playlist_entrada"])
    total_canales = len(canales)

    motor = MotorReglas()

    # Normalización y asignación de puntuación
    for canal in canales:
        canal.nombre_normalizado = normalizar_nombre(canal.nombre)
        canal.dominio = detectar_dominio(canal.url)
        canal.puntuacion = calcular_puntuacion(canal, motor)

    # Filtrar duplicados
    canales = seleccionar_mejores(canales)

    # OPCIONAL: Verificación de streams activos (Activar según conveniencia)
    # CONFIGURACION.get("verificar_online", False)
    if CONFIGURACION.get("verificar_online", True):
        canales = verificar_canales_paralelo(canales, max_workers=25, timeout=3)
        # Opcional: Descartar caídos para la playlist final
        canales = [c for c in canales if c.online]

    print()
    print(f"Canales leídos                : {total_canales}")
    print(f"Canales después de procesar   : {len(canales)}")
    print(f"Canales eliminados/caídos     : {total_canales - len(canales)}")

    print()
    print("Primeros 10 canales seleccionados:\n")

    for canal in canales[:10]:
        print(f"- {canal.nombre}")
        print(f"  Normalizado : {canal.nombre_normalizado}")
        print(f"  Dominio     : {canal.dominio}")
        print(f"  Puntuación  : {canal.puntuacion}")
        if hasattr(canal, 'latencia') and canal.latencia > 0:
            print(f"  Latencia    : {canal.latencia}s")

        print("  Detalle de puntuación:")
        for motivo, valor in canal.detalle_puntuacion:
            print(f"    {valor:+4}  {motivo}")
        print()

    # Exportación de la playlist y reportes
    exportar_m3u(canales, CONFIGURACION["playlist_salida"])
    generar_auditoria(AUDITORIA_DUPLICADOS)

    print()
    print("=" * 50)
    print("Dominios con más canales")
    print("=" * 50)
    dominios = contar_dominios(canales)
    for dominio, cantidad in dominios.most_common(10):
        print(f"{cantidad:4}  {dominio}")

    print()
    print("=" * 50)
    print("Distribución de puntuaciones")
    print("=" * 50)
    puntuaciones = contar_puntuaciones(canales)
    for puntos, cantidad in sorted(puntuaciones.items()):
        print(f"{puntos:3} puntos : {cantidad}")

    print()
    print("Playlist exportada correctamente.")
    print(f'Archivo: {CONFIGURACION["playlist_salida"]}')

    print()
    print("Auditoría generada correctamente.")
    print("Archivo: output/auditoria_duplicados.txt")


if __name__ == "__main__":
    main()