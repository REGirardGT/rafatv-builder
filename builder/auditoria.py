# ==========================================
# RafaTV Builder
# Auditoría de duplicados
# ==========================================

from pathlib import Path
from collections import Counter


def generar_auditoria(registros):

    salida = Path("output/auditoria_duplicados.txt")

    with open(salida, "w", encoding="utf-8") as f:

        f.write("=" * 50 + "\n")
        f.write("Auditoría de duplicados\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Total de decisiones: {len(registros)}\n\n")

        criterios = Counter()

        for registro in registros:
            criterios[registro["motivo"]] += 1

        f.write("Resumen de decisiones\n")
        f.write("-" * 50 + "\n")

        for motivo, cantidad in criterios.most_common():
            f.write(f"{motivo:<20} : {cantidad}\n")

        f.write("\n")
        f.write("=" * 50 + "\n\n")

        for registro in registros:

            ganador = registro["ganador"]
            perdedor = registro["perdedor"]

            f.write(f"Canal: {registro['canal']}\n")
            f.write(f"Motivo: {registro['motivo']}\n\n")

            f.write("Ganador\n")
            f.write(f"  Puntuación : {ganador['puntuacion']}\n")
            f.write(f"  Dominio    : {ganador['dominio']}\n")
            f.write(f"  URL        : {ganador['url']}\n")

            f.write("  Detalle:\n")

            for motivo, valor in ganador["detalle"]:
                f.write(f"     {valor:+4}  {motivo}\n")

            f.write("\n")


            f.write("Perdedor\n")
            f.write(f"  Puntuación : {perdedor['puntuacion']}\n")
            f.write(f"  Dominio    : {perdedor['dominio']}\n")
            f.write(f"  URL        : {perdedor['url']}\n")

            f.write("  Detalle:\n")

            for motivo, valor in perdedor["detalle"]:
                f.write(f"     {valor:+4}  {motivo}\n")

            f.write("\n")
            f.write("-" * 50)
            f.write("\n\n")