# ==========================================
# RafaTV Builder
# Detector de país
# ==========================================

import re


def detectar_pais(tvg_id):

    if not tvg_id:
        return ""

    tvg_id = tvg_id.lower()

    coincidencia = re.search(r"\.([a-z]{2})@", tvg_id)

    if coincidencia:
        return coincidencia.group(1)

    return ""