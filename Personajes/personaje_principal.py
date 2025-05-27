
from .hechicero import Hechicero, Hechizo

class PersonajePrincipal(Hechicero):
    def __init__(self, nombre="Invocador"):
        super().__init__(nombre, salud=130, mana=100, ataque=25, defensa=12)

        self.aprender_hechizo(Hechizo("Rayo Arcano", 20, 30))         # Daño básico
        self.aprender_hechizo(Hechizo("Golpe de Luz", 25, 35))        # Daño más fuerte
        self.aprender_hechizo(Hechizo("Curación Rápida", 15, -25))    # Curación (daño negativo)
        self.aprender_hechizo(Hechizo("Escudo Arcano", 10, 0))        # Defensa

        self.escudo_activado = False

    def usar_hechizo_especial(self, nombre_hechizo, objetivo):
        if nombre_hechizo == "Curación Rápida":
            if self.mana >= 15:
                self.mana -= 15
                self.salud = min(130, self.salud + 25)
                return f"{self.nombre} usa Curación Rápida y restaura 25 puntos de salud."
            return f"{self.nombre} no tiene suficiente maná para curarse."

        if nombre_hechizo == "Escudo Arcano":
            if self.mana >= 10:
                self.mana -= 10
                if not self.escudo_activado:
                    self.defensa += 10
                    self.escudo_activado = True
                    return f"{self.nombre} activa Escudo Arcano. Defensa aumentada."
                return f"{self.nombre} ya tiene Escudo Arcano activo."
            return f"{self.nombre} no tiene suficiente maná para Escudo Arcano."

        # Poder ofensivo estándar
        return self.lanzar_hechizo(objetivo, nombre_hechizo)

    def restaurar_estado(self):
        if self.escudo_activado:
            self.defensa -= 10
            self.escudo_activado = False
