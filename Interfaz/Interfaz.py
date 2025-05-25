

import tkinter as tk
from tkinter import messagebox, ttk
from Personajes.personaje_principal import PersonajePrincipal
from Personajes.hechicero_fuego import HechiceroFuego
from Personajes.hechicero_hielo import HechiceroHielo

class JuegoInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Conjuro Eterno - Batalla Mágica")
        self.root.geometry("900x600")
        self.root.configure(bg="#1a1a1a")

        self.jugador = PersonajePrincipal()
        self.enemigos = [HechiceroFuego(), HechiceroHielo()]
        self.nivel = 0
        self.enemigo = self.enemigos[self.nivel]

        self.crear_layout()
        self.actualizar_estado()

    def crear_layout(self):
        self.frame_enemigo = tk.Frame(self.root, bg="#2a2a2a", height=200)
        self.frame_enemigo.pack(fill=tk.X, side=tk.TOP)

        self.frame_iconos = tk.Frame(self.frame_enemigo, bg="#2a2a2a")
        self.frame_iconos.place(relx=1.0, rely=0.0, anchor='ne')
        self.label_enemigo = tk.Label(self.frame_enemigo, text="", fg="white", bg="#2a2a2a", font=("Arial", 16))
        self.label_enemigo.pack(pady=5)
        self.label_enemigo_salud = tk.Label(self.frame_enemigo, text="", fg="white", bg="#2a2a2a")
        self.label_enemigo_salud.pack()
        self.bar_enemigo_salud = ttk.Progressbar(self.frame_enemigo, length=300)
        self.bar_enemigo_salud.pack(pady=2)
        self.label_enemigo_mana = tk.Label(self.frame_enemigo, text="", fg="white", bg="#2a2a2a")
        self.label_enemigo_mana.pack()
        self.bar_enemigo_mana = ttk.Progressbar(self.frame_enemigo, length=300)
        self.bar_enemigo_mana.pack(pady=2)

        self.avatar_enemigo = tk.Label(self.frame_enemigo, text="🤖", font=("Arial", 30), bg="#2a2a2a")
        self.avatar_enemigo.pack(pady=5)

        self.frame_centro = tk.Frame(self.root, bg="#333", height=200)
        self.frame_centro.pack(fill=tk.X)

        self.frame_jugador = tk.Frame(self.root, bg="#2a2a2a", height=200)
        self.frame_jugador.pack(fill=tk.BOTH, expand=True)
        self.label_jugador = tk.Label(self.frame_jugador, text="", fg="white", bg="#2a2a2a", font=("Arial", 16))
        self.label_jugador.pack(pady=5)
        self.label_jugador_salud = tk.Label(self.frame_jugador, text="", fg="white", bg="#2a2a2a")
        self.label_jugador_salud.pack()
        self.bar_jugador_salud = ttk.Progressbar(self.frame_jugador, length=300)
        self.bar_jugador_salud.pack(pady=2)
        self.label_jugador_mana = tk.Label(self.frame_jugador, text="", fg="white", bg="#2a2a2a")
        self.label_jugador_mana.pack()
        self.bar_jugador_mana = ttk.Progressbar(self.frame_jugador, length=300)
        self.bar_jugador_mana.pack(pady=2)

        self.avatar_jugador = tk.Label(self.frame_jugador, text="🧙", font=("Arial", 30), bg="#2a2a2a")
        self.avatar_jugador.pack(pady=5)

        self.frame_cartas = tk.Frame(self.frame_jugador, bg="#2a2a2a")
        self.frame_cartas.pack(pady=10)

        self.botones = []
        for hechizo in self.jugador.hechizos:
            boton = tk.Button(
                self.frame_cartas,
                text=hechizo.nombre,
                width=15,
                height=4,
                font=("Arial", 12),
                command=lambda h=hechizo: self.usar_hechizo(h.nombre)
            )
            boton.pack(side=tk.LEFT, padx=10)
            self.botones.append(boton)

        self.text_log = tk.Text(self.root, height=6, bg="#111", fg="lime", font=("Consolas", 10))
        self.text_log.pack(fill=tk.X)

        self.boton_reiniciar = tk.Button(self.root, text="Reiniciar Partida", font=("Arial", 12), bg="#444", fg="white", command=self.reiniciar_partida)
        self.boton_reiniciar.pack(pady=5)
        self.log("Bienvenido a Conjuro Eterno. ¡Prepárate para luchar!\n")

        self.iconos_poderes = []
        for hechizo in self.jugador.hechizos:
            icono = tk.Label(self.frame_iconos, text=hechizo.nombre[:2], bg="#444", fg="white", font=("Arial", 10), width=4, height=2, relief="raised")
            icono.pack(padx=2, pady=2)
            self.iconos_poderes.append(icono)

    def parpadear(self, widget, color_original, tipo, veces=4):
        colores = {
            "daño": "#ff5555",
            "cura": "#55ff55",
            "defensa": "#5599ff",
            "default": color_original
        }
        color_destello = colores.get(tipo, color_original)

        def toggle(i=0):
            if i >= veces:
                widget.config(bg=color_original)
                return
            color = color_destello if i % 2 == 0 else color_original
            widget.config(bg=color)
            self.root.after(100, lambda: toggle(i + 1))
        toggle()

    def usar_hechizo(self, nombre):
        if not self.jugador.esta_vivo():
            self.log("Has sido derrotado.\n")
            return

        resultado = self.jugador.usar_hechizo_especial(nombre, self.enemigo)
        self.log(resultado)
        self.parpadear(self.frame_enemigo, "#2a2a2a", tipo=("cura" if "restaura" in resultado else ("defensa" if "Escudo" in resultado else "daño")))

        if self.enemigo.esta_vivo():
            respuesta = self.enemigo.elegir_accion(self.jugador)
            tipo_respuesta = "cura" if "restaura" in respuesta else ("defensa" if "Escudo" in respuesta or "Muralla" in respuesta or "Muro" in respuesta else "daño")
            self.log(respuesta)
            self.parpadear(self.frame_jugador, "#2a2a2a", tipo=tipo_respuesta)
        else:
            self.log(f"¡Has vencido a {self.enemigo.nombre}!")
            self.nivel += 1
            if self.nivel < len(self.enemigos):
                self.enemigo = self.enemigos[self.nivel]
                self.jugador.restaurar_estado()
                self.jugador.salud = min(self.jugador.salud + 40, 130)
                self.jugador.mana += 30
                self.log(f"\n--- Nivel {self.nivel + 1}: {self.enemigo.nombre} ---")
            else:
                self.log("\n¡Has ganado todos los combates!")

        self.actualizar_estado()

    def actualizar_estado(self):
        self.label_enemigo.config(text=f"{self.enemigo.nombre}")
        self.label_jugador.config(text=f"{self.jugador.nombre}")

        self.label_enemigo_salud.config(text=f"Salud: {self.enemigo.salud}/120")
        self.bar_enemigo_salud["maximum"] = 120
        self.bar_enemigo_salud["value"] = self.enemigo.salud
        self.label_enemigo_mana.config(text=f"Maná: {self.enemigo.mana}/150")
        self.bar_enemigo_mana["maximum"] = 150
        self.bar_enemigo_mana["value"] = self.enemigo.mana

        self.label_jugador_salud.config(text=f"Salud: {self.jugador.salud}/130")
        self.bar_jugador_salud["maximum"] = 130
        self.bar_jugador_salud["value"] = self.jugador.salud
        self.label_jugador_mana.config(text=f"Maná: {self.jugador.mana}/100")
        self.bar_jugador_mana["maximum"] = 100
        self.bar_jugador_mana["value"] = self.jugador.mana

    def reiniciar_partida(self):
        self.jugador = PersonajePrincipal()
        self.enemigos = [HechiceroFuego(), HechiceroHielo()]
        self.nivel = 0
        self.enemigo = self.enemigos[self.nivel]
        self.text_log.delete('1.0', tk.END)
        self.log("La partida ha sido reiniciada. ¡Buena suerte!")
        self.actualizar_estado()

    def log(self, texto):
        self.text_log.insert(tk.END, texto + "\n")
        self.text_log.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoInterfaz(root)
    root.mainloop()
