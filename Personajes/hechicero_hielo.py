from .hechicero import Hechicero, Hechizo

class HechiceroHielo(Hechicero):
    def __init__(self, nombre="Hechicero de Hielo"):
        super().__init__(nombre, salud=100, mana=150, ataque=16, defensa=12)
        self.aprender_hechizo(Hechizo("Lanza Helada", 20, 26))
        self.aprender_hechizo(Hechizo("Tormenta Glacial", 30, 34))
        self.aprender_hechizo(Hechizo("Hielo Sanador", 15, -22))
        self.aprender_hechizo(Hechizo("Muro de Hielo", 10, 0))
        self.escudo_activado = False

    def elegir_accion(self, objetivo):
        if self.salud < 60 and self.mana >= 15:
            return self.lanzar_hechizo(objetivo, "Hielo Sanador")
        if not self.escudo_activado and self.mana >= 10:
            return self.lanzar_hechizo(objetivo, "Muro de Hielo")
        if self.mana >= 30:
            return self.lanzar_hechizo(objetivo, "Tormenta Glacial")
        if self.mana >= 20:
            return self.lanzar_hechizo(objetivo, "Lanza Helada")

        # Ataque físico como último recurso
        daño = self.atacar(objetivo)
        return f"{self.nombre} ataca físicamente a {objetivo.nombre} e inflige {daño} de daño."

    def lanzar_hechizo(self, objetivo, hechizo_nombre):
        hechizo = next((h for h in self.hechizos if h.nombre == hechizo_nombre), None)
        if not hechizo:
            return f"{self.nombre} intenta lanzar un hechizo desconocido."

        if self.mana < hechizo.costo:
            return f"{self.nombre} no tiene suficiente maná para usar {hechizo.nombre}."

        self.mana -= hechizo.costo

        if hechizo.daño < 0:
            self.salud = min(self.salud + abs(hechizo.daño), 100)
            return f"{self.nombre} usa {hechizo.nombre} y se cura {abs(hechizo.daño)} puntos de salud."

        if hechizo.nombre == "Muro de Hielo" and not self.escudo_activado:
            self.defensa += 10
            self.escudo_activado = True
            return f"{self.nombre} activa {hechizo.nombre}. Defensa aumentada."

        # Daño ofensivo normal
        daño_real = max(0, hechizo.daño - objetivo.defensa)
        objetivo.recibir_daño(daño_real)
        return f"{self.nombre} lanza {hechizo.nombre} e inflige {daño_real} de daño a {objetivo.nombre}."
