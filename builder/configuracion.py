# ==========================================
# RafaTV Builder
# Configuración
# ==========================================

from pathlib import Path
import json


def cargar_lista(nombre_archivo):

    archivo = Path("config") / nombre_archivo

    elementos = []

    if not archivo.exists():
        print(f"No existe {archivo}")
        return elementos

    with open(archivo, encoding="utf-8") as f:

        for linea in f:

            linea = linea.strip()

            if linea == "":
                continue

            if linea.startswith("#"):
                continue

            elementos.append(linea.lower())

    # Elimina duplicados y ordena la lista
    elementos = sorted(set(elementos))

    return elementos

# ==========================================
# Listas de configuración
# ==========================================

CANALES_FAVORITOS = cargar_lista(
    "canales_favoritos.txt"
)

GRUPOS_PRIORITARIOS = cargar_lista(
    "grupos_preferidos.txt"
)

PAISES_PRIORITARIOS = cargar_lista(
    "paises_preferidos.txt"
)

# ==========================================
# Configuración JSON
# ==========================================

from pathlib import Path
import json

def cargar_configuracion():

    archivo = Path("config/configuracion.json")

    print()

    with open(archivo, encoding="utf-8") as f:
        return json.load(f)

    archivo = Path("config/configuracion.json")

    if not archivo.exists():

        print("No se encontró config/configuracion.json")
        print("Usando configuración por defecto.\n")

        return {
            "bonificacion_favorito": 100,
            "bonificacion_grupo": 20,
            "bonificacion_pais": 15
        }

    with open(archivo, encoding="utf-8") as f:

        return json.load(f)


CONFIGURACION = cargar_configuracion()

CONFIGURACION.setdefault("version", "2.0")
CONFIGURACION.setdefault("autor", "RafaTV Builder")
CONFIGURACION.setdefault("fecha", "")

def obtener_configuracion(clave, valor_por_defecto):
    """
    Devuelve un valor de configuración.
    Si la clave no existe, utiliza el valor por defecto.
    """

    return CONFIGURACION.get(
        clave,
        valor_por_defecto
    )