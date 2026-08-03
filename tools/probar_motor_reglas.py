from builder.motor_reglas import MotorReglas

print("=" * 40)
print("Prueba del Motor de Reglas")
print("=" * 40)

motor = MotorReglas()

print("Favoritos cargados :", len(motor.favoritos))
print("Grupos cargados    :", len(motor.grupos))
print("Países cargados    :", len(motor.paises))
print("Dominios cargados  :", len(motor.dominios))

print()
print("Prueba finalizada correctamente.")

print()
print("Prueba de métodos")

class CanalPrueba:
    def __init__(self):
        self.nombre = "Canal Demo"
        self.grupo = "TV General"
        self.pais = "guatemala"

canal = CanalPrueba()

print("¿Es favorito?        :", motor.es_favorito(canal))
print("¿Grupo preferido?    :", motor.es_grupo_preferido(canal))

print()
print("Evaluación completa")

resultado = motor.evaluar(canal)

for regla, valor in resultado.items():
    print(f"{regla:20}: {valor}")

print()
print("Bonificaciones")

bonos = motor.calcular_bonificaciones(canal)

for regla, puntos in bonos.items():
    print(f"{regla:20}: {puntos}")