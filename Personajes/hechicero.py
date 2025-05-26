class Hechizo:
    def __init__(self, nombre: str, costo_mana: int, danio: int):
        self.nombre = nombre
        self.costo_mana = costo_mana
        self.danio = danio

    def usar(self, objetivo):
        return self.danio


class Hechicero:
    def __init__(self, nombre: str, salud: int, mana: int, ataque: int, defensa: int):
        self.nombre = nombre
        self.salud = salud
        self.mana = mana
        self.ataque = ataque
        self.defensa = defensa
        self.hechizos = []

    def aprender_hechizo(self, hechizo: Hechizo):
        self.hechizos.append(hechizo)

    def atacar(self, objetivo):
        danio = max(0, self.ataque - objetivo.defensa)
        objetivo.recibir_danio(danio)
        return danio

    def lanzar_hechizo(self, objetivo, hechizo_nombre):
        hechizo = next((h for h in self.hechizos if h.nombre == hechizo_nombre), None)
        if not hechizo:
            return f"{self.nombre} no conoce el hechizo '{hechizo_nombre}'."
        if self.mana < hechizo.costo_mana:
            return f"{self.nombre} no tiene suficiente maná para lanzar '{hechizo_nombre}'."

        self.mana -= hechizo.costo_mana
        danio = hechizo.usar(objetivo)
        objetivo.recibir_danio(danio)
        return f"{self.nombre} lanza '{hechizo.nombre}' e inflige {danio} de daño."

    def recibir_danio(self, cantidad):
        self.salud = max(0, self.salud - cantidad)

    def esta_vivo(self):
        return self.salud > 0
