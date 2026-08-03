from collections import Counter
from datetime import datetime

def generar_reporte(canales):

    grupos = Counter()
    motivos = Counter()

    sin_grupo = 0
    sin_tvg = 0

    for canal in canales:

        grupo = canal.grupo.strip()

        if grupo == "":
            sin_grupo += 1
        else:
            grupos[grupo] += 1

        if canal.tvg_id.strip() == "":
            sin_tvg += 1

        if canal.motivo != "":
            motivos[canal.motivo] +=1

    with open("output/reporte_v0.5.txt","w",encoding="utf-8") as f:

        f.write("=====================================\n")
        f.write(" RafaTV Builder - Reporte v1.0\n")
        f.write("=====================================\n\n")

        f.write(f"Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")

        f.write(f"Canales procesados : {len(canales)}\n")
        f.write(f"Sin grupo     : {sin_grupo}\n")
        f.write(f"Sin tvg-id    : {sin_tvg}\n\n")

        f.write("GRUPOS\n")
        f.write("-----------------------------\n")

        for grupo, cantidad in grupos.most_common():

            f.write(f"{grupo} : {cantidad}\n")

        f.write("\n")
        f.write("MOTIVOS REGISTRADOS\n")
        f.write("-----------------------------\n")

        if len(motivos) == 0:
            f.write("Sin motivos registrados\n")
        else:
            for motivo, cantidad in motivos.most_common():
                f.write(f"{motivo} : {cantidad}\n")
