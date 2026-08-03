from pathlib import Path
import json


class MotorReglas:
    def __init__(self, carpeta_config="config"):
        self.carpeta = Path(carpeta_config)

        self.favoritos = set()
        self.grupos = set()
        self.paises = set()
        self.dominios = set()
        self.reglas = {}

        self.cargar()

    def cargar_lista(self, nombre_archivo):
        archivo = self.carpeta / nombre_archivo

        if not archivo.exists():
            return set()

        with open(archivo, "r", encoding="utf-8") as f:
            return {
                linea.strip()
                for linea in f
                if linea.strip() and not linea.startswith("#")
            }

    def cargar_json(self, nombre_archivo):
        archivo = self.carpeta / nombre_archivo

        if not archivo.exists():
            return {}

        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)

    def cargar(self):
        self.favoritos = self.cargar_lista("canales_favoritos.txt")
        self.grupos = self.cargar_lista("grupos_preferidos.txt")
        self.paises = self.cargar_lista("paises_preferidos.txt")
        self.dominios = self.cargar_lista("dominios_preferidos.txt")
        self.reglas = self.cargar_json("configuracion.json")

    def pertenece(self, valor, lista):
        """
        Comprueba si un valor pertenece a una lista de reglas.
        """

        if valor is None:
            return False

        return valor.lower().strip() in lista

    def es_favorito(self, canal):
        """
        Devuelve True si el canal está en favoritos.
        """

        return self.pertenece(
            canal.nombre,
            self.favoritos
        )

    def es_grupo_preferido(self, canal):
        """
        Devuelve True si el grupo está en grupos_preferidos.txt
        """

        return self.pertenece(
            canal.grupo,
            self.grupos
        )

    def es_pais_preferido(self, canal):
        """
        Devuelve True si el país está en paises_preferidos.txt
        """

        return self.pertenece(
            canal.pais,
            self.paises
        )

    def es_dominio_preferido(self, canal):
        """
        Devuelve True si el dominio está en dominios_preferidos.txt
        """

        return self.pertenece(
            canal.dominio,
            self.dominios
        )

    def evaluar(self, canal):

        return {
            "favorito": self.es_favorito(canal),
            "grupo_preferido": self.es_grupo_preferido(canal),
            "pais_preferido": self.es_pais_preferido(canal),
            "dominio_preferido": self.es_dominio_preferido(canal)
        }

    def calcular_bonificaciones(self, canal):
        """
        Calcula las bonificaciones que recibe un canal
        según las reglas configuradas.
        """

        evaluacion = self.evaluar(canal)

        bonificaciones = {
            "favorito": 0,
            "grupo": 0,
            "pais": 0,
            "dominio": 0
        }

        if evaluacion["favorito"]:
            bonificaciones["favorito"] = self.reglas.get(
                "bonificacion_favorito", 0
            )

        if evaluacion["grupo_preferido"]:
            bonificaciones["grupo"] = self.reglas.get(
                "bonificacion_grupo", 0
            )

        if evaluacion["pais_preferido"]:
            bonificaciones["pais"] = self.reglas.get(
                "bonificacion_pais", 0
            )

        if evaluacion["dominio_preferido"]:
            bonificaciones["dominio"] = self.reglas.get(
            "bonificacion_dominio",
            0
        )

        return bonificaciones