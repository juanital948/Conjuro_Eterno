

from .hechicero import Hechicero, Hechizo
import random

class HechiceroFuego(Hechicero):
    def __init__(self, nombre="Hechicero de Fuego"):
        super().__init__(nombre, salud=100, mana=150, ataque=20, defensa=10)
        self.aprender_hechizo(Hechizo("Llama Roja", 20, 28))        # daño medio
        self.aprender_hechizo(Hechizo("Columna Ígnea", 30, 36))     # daño fuerte
        self.aprender_hechizo(Hechizo("Regeneración Ígnea", 15, -20))  # curación
        self.aprender_hechizo(Hechizo("Muralla de Fuego", 10, 0))   # defensa
        self.escudo_activado = False

    def elegir_accion(self, objetivo):
        # IA prioriza curarse, luego atacar, luego defender
        if self.salud < 40 and self.mana >= 15:
            self.mana -= 15
            self.salud = min(100, self.salud + 20)
            return f"{self.nombre} usa Regeneración Ígnea y recupera 20 de salud."

        elif self.mana >= 30:
            return self.lanzar_hechizo(objetivo, "Columna Ígnea")

        elif self.mana >= 20:
            return self.lanzar_hechizo(objetivo, "Llama Roja")

        elif self.mana >= 10 and not self.escudo_activado:
            self.mana -= 10
            self.defensa += 10
            self.escudo_activado = True
            return f"{self.nombre} levanta una Muralla de Fuego y aumenta su defensa."

        else:
            danio = self.atacar(objetivo)
            return f"{self.nombre} ataca físicamente a {objetivo.nombre}, causando {danio} de daño."

    def lanzar_hechizo(self, objetivo, hechizo_nombre):
        hechizo = next((h for h in self.hechizos if h.nombre == hechizo_nombre), None)
        if not hechizo:
            return f"{self.nombre} no conoce el hechizo {hechizo_nombre}."
        if self.mana < hechizo.costo_mana:
            return f"{self.nombre} no tiene suficiente maná para usar {hechizo_nombre}."

        self.mana -= hechizo.costo_mana
        danio = hechizo.usar(objetivo)
        objetivo.recibir_danio(danio)
        return f"{self.nombre} lanza {hechizo.nombre} y causa {danio} de daño a {objetivo.nombre}."

    def recibir_danio(self, cantidad):
        self.salud = max(0, self.salud - cantidad)

    def esta_vivo(self):
        return self.salud > 0