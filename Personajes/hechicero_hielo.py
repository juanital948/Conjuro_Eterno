
from .hechicero import Hechicero, Hechizo
import random

class HechiceroHielo(Hechicero):
    def __init__(self, nombre="Hechicero de Hielo"):
        super().__init__(nombre, salud=100, mana=150, ataque=16, defensa=12)
        self.aprender_hechizo(Hechizo("Lanza Helada", 20, 40))          # Ataque base
        self.aprender_hechizo(Hechizo("Tormenta Glacial", 30, 50))      # Ataque fuerte
        self.aprender_hechizo(Hechizo("Hielo Sanador", 15, -22))        # Curación
        self.aprender_hechizo(Hechizo("Muro de Hielo", 10, 0))          # Defensa
        self.escudo_activado = False

    def elegir_accion(self, objetivo):
        prioridades = [
            ("Hielo Sanador", self.salud < 60),
            ("Muro de Hielo", not self.escudo_activado and self.mana >= 10),
            ("Tormenta Glacial", self.mana >= 30),
            ("Lanza Helada", self.mana >= 20),
        ]
        for nombre, condicion in prioridades:
            if condicion:
                return self.lanzar_hechizo(objetivo, nombre)

        # Si no puede usar hechizos, ataca físicamente
        daño = self.atacar(objetivo)
        return f"{self.nombre} ataca físicamente a {objetivo.nombre} e inflige {daño} de daño."

    def lanzar_hechizo(self, objetivo, hechizo_nombre):
        hechizo = next((h for h in self.hechizos if h.nombre == hechizo_nombre), None)
        if not hechizo:
            return f"{self.nombre} intenta usar {hechizo_nombre}, pero no lo conoce."

        if self.mana < hechizo.costo:
            return f"{self.nombre} intentó usar {hechizo.nombre} pero no tiene suficiente maná."

        self.mana -= hechizo.costo

        if hechizo.nombre == "Hielo Sanador":
            curado = abs(hechizo.daño)
            self.salud = min(self.salud + curado, 100)
            return f"{self.nombre} usa {hechizo.nombre} y restaura {curado} puntos de salud."

        if hechizo.nombre == "Muro de Hielo" and not self.escudo_activado:
            self.defensa += 10
            self.escudo_activado = True
            return f"{self.nombre} activa {hechizo.nombre}. Su defensa aumenta."

        # Hechizos ofensivos
        daño_total = max(0, hechizo.daño - objetivo.defensa)
        objetivo.recibir_daño(daño_total)
        return f"{self.nombre} lanza {hechizo.nombre} e inflige {daño_total} de daño a {objetivo.nombre}."
