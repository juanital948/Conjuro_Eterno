from .hechicero import Hechicero, Hechizo
import random

class HechiceroHielo(Hechicero):
    def __init__(self, nombre="Hechicero de Hielo"):
        super().__init__(nombre, salud=100, mana=150, ataque=16, defensa=12)
        self.aprender_hechizo(Hechizo("Lanza Helada", 20, 26))
        self.aprender_hechizo(Hechizo("Tormenta Glacial", 30, 34))
        self.aprender_hechizo(Hechizo("Hielo Sanador", 15, -22))
        self.aprender_hechizo(Hechizo("Muro de Hielo", 10, 0))
        self.escudo_activado = False

    def elegir_accion(self, objetivo):
        prioridades = [
            ("Hielo Sanador", self.salud < 60),
            ("Muro de Hielo", not self.escudo_activado and self.mana >= 10),
            ("Tormenta Glacial", self.mana >= 30),
            ("Lanza Helada", self.mana >= 20),
        ]
        for nombre, cond in prioridades:
            if cond:
                return self.lanzar_hechizo(objetivo, nombre)

        return f"{self.nombre} ataca físicamente a {objetivo.nombre} e inflige {self.atacar(objetivo)} de daño."

    def lanzar_hechizo(self, objetivo, hechizo_nombre):
        hechizo = next((h for h in self.hechizos if h.nombre == hechizo_nombre), None)
        if not hechizo or self.mana < hechizo.costo:
            return f"{self.nombre} intentó usar {hechizo_nombre} pero no tiene suficiente maná."

        self.mana -= hechizo.costo

        if hechizo.nombre == "Hielo Sanador":
            self.salud = min(self.salud + abs(hechizo.daño), 100)
            return f"{self.nombre} usa {hechizo.nombre} y restaura {abs(hechizo.daño)} puntos de salud."

        if hechizo.nombre == "Muro de Hielo" and not self.escudo_activado:
            self.defensa += 10
            self.escudo_activado = True
            return f"{self.nombre} activa {hechizo.nombre}. Su defensa aumenta."

        daño_real = max(0, hechizo.daño - objetivo.defensa)
        objetivo.recibir_daño(daño_real)
        return f"{self.nombre} lanza {hechizo.nombre} e inflige {daño_real} de daño a {objetivo.nombre}."
