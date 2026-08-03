# ==========================================
# RafaTV Builder
# Clase Canal
# ==========================================

class Canal:

    def __init__(
        self,
        nombre="",
        grupo="",
        tvg_id="",
        url="",
        extinf=""
    ):
        # ----------------------------------
        # Información original
        # ----------------------------------
        self.nombre = nombre
        self.grupo = grupo
        self.tvg_id = tvg_id
        self.url = url
        self.extinf = extinf

        # ----------------------------------
        # Información detectada
        # ----------------------------------
        self.pais = ""
        self.idioma = ""
        self.logo = ""
        self.resolucion = ""
        self.dominio = ""
        self.proveedor = ""
        self.extension = ""

        # ----------------------------------
        # Información calculada
        # ----------------------------------
        self.nombre_normalizado = ""
        self.clasificacion = ""

        # ----------------------------------
        # Estado y Verificación del canal
        # ----------------------------------
        self.activo = True
        self.online = True
        self.latencia = 0.0
        self.motivo = ""

        # ----------------------------------
        # Calidad / Puntuación
        # ----------------------------------
        self.puntuacion = 0
        self.detalle_puntuacion = []

        # ----------------------------------
        # Historial del procesamiento
        # ----------------------------------
        self.historial = []

    def __repr__(self):
        return f"<Canal {self.nombre} ({'ONLINE' if self.online else 'OFFLINE'}) - Puntos: {self.puntuacion}>"