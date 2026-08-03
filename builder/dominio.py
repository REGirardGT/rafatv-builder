# ==========================================
# RafaTV Builder
# Detector de dominio
# ==========================================

from urllib.parse import urlparse


def detectar_dominio(url):

    if not url:
        return ""

    try:
        return urlparse(url).netloc.lower()

    except Exception:
        return ""