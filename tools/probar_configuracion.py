# ==========================================
# RafaTV Builder
# Prueba del módulo de configuración
# ==========================================

from builder.configuracion import (
    CANALES_FAVORITOS,
    GRUPOS_PRIORITARIOS,
    PAISES_PRIORITARIOS,
    CONFIGURACION
)

print()
print("========== CONFIGURACIÓN ==========")

print()
print("Canales favoritos")
print("------------------")

for canal in CANALES_FAVORITOS:
    print("-", canal)

print()
print("Grupos prioritarios")
print("-------------------")

for grupo in GRUPOS_PRIORITARIOS:
    print("-", grupo)

print()
print("Países prioritarios")
print("-------------------")

for pais in PAISES_PRIORITARIOS:
    print("-", pais)

print()
print("Configuración JSON")
print("------------------")

for clave, valor in CONFIGURACION.items():

    print(f"{clave} = {valor}")