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

# ==========================================
# DICCIONARIO DE MAPPING DE PAÍSES
# ==========================================
PAISES_HISPANOS_Y_USA = {
    "GT": "Guatemala",
    "MX": "México",
    "AR": "Argentina",
    "CO": "Colombia",
    "CL": "Chile",
    "PE": "Perú",
    "CR": "Costa Rica",
    "SV": "El Salvador",
    "HN": "Honduras",
    "NI": "Nicaragua",
    "PA": "Panamá",
    "DO": "República Dominicana",
    "PR": "Puerto Rico",
    "EC": "Ecuador",
    "VE": "Venezuela",
    "UY": "Uruguay",
    "PY": "Paraguay",
    "BO": "Bolivia",
    "ES": "España",
    "US": "Estados Unidos",
}

def obtener_grupo_normalizado(canal) -> str | None:
    """
    Analiza el objeto canal y retorna un grupo normalizado por país.
    Si no pertenece a Hispanoamérica/USA, retorna None para descartar.
    """
    pais_code = getattr(canal, "pais", "").upper() if hasattr(canal, "pais") else ""
    grupo_orig = getattr(canal, "grupo", "").upper() if hasattr(canal, "grupo") else ""
    nombre = canal.nombre.upper()

    # 1. Por código ISO de país si existe en el objeto canal
    if pais_code in PAISES_HISPANOS_Y_USA:
        return PAISES_HISPANOS_Y_USA[pais_code]

    # 2. Por coincidencia en el grupo original o nombre
    if any(k in grupo_orig or k in nombre for k in ["GUATEMALA", "GUATE"]):
        return "Guatemala"
    elif any(k in grupo_orig or k in nombre for k in ["MEXICO", "MÉXICO", "MEX"]):
        return "México"
    elif any(k in grupo_orig or k in nombre for k in ["ESPAÑA", "SPAIN", "ESP"]):
        return "España"
    elif any(k in grupo_orig or k in nombre for k in ["USA", "UNITED STATES", "EEUU"]):
        return "Estados Unidos"
    
    # 3. Mapeo genérico por otros países hispanos
    for code, nombre_pais in PAISES_HISPANOS_Y_USA.items():
        if nombre_pais.upper() in grupo_orig or nombre_pais.upper() in nombre:
            return nombre_pais

    # 4. Si la fuente etiqueta la categoría por idioma
    if "SPANISH" in grupo_orig or "ESPAÑOL" in grupo_orig or "LATINO" in grupo_orig:
        return "Latinoamérica / General"

    return None


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

    # --------------------------------------------------------------------------
    # FILTRADO Y CLASIFICACIÓN POR PAÍS (Hispanoamérica y USA)
    # --------------------------------------------------------------------------
    canales_filtrados_pais = []
    for canal in canales:
        grupo_limpio = obtener_grupo_normalizado(canal)
        if grupo_limpio:
            canal.grupo = grupo_limpio  # Asignamos la nueva categoría limpia
            canales_filtrados_pais.append(canal)
    
    canales = canales_filtrados_pais

    # --------------------------------------------------------------------------
    # VERIFICACIÓN DE STREAMS ACTIVOS (Health Check)
    # --------------------------------------------------------------------------
    if CONFIGURACION.get("verificar_online", True):
        canales = verificar_canales_paralelo(canales, max_workers=25, timeout=3)
        # Descartar caídos / error 403 / sin señal para la playlist final
        canales = [c for c in canales if c.online]

    print()
    print(f"Canales leídos                 : {total_canales}")
    print(f"Canales después de procesar    : {len(canales)}")
    print(f"Canales eliminados/caídos      : {total_canales - len(canales)}")

    print()
    print("Primeros 10 canales seleccionados:\n")

    for canal in canales[:10]:
        print(f"- {canal.nombre}")
        print(f"  Grupo (País) : {getattr(canal, 'grupo', 'Sin Grupo')}")
        print(f"  Normalizado  : {canal.nombre_normalizado}")
        print(f"  Dominio      : {canal.dominio}")
        print(f"  Puntuación   : {canal.puntuacion}")
        if hasattr(canal, 'latencia') and canal.latencia > 0:
            print(f"  Latencia     : {canal.latencia}s")

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