import tkinter as tk
from tkinter import messagebox, ttk
from Personajes.personaje_principal import PersonajePrincipal
from Personajes.hechicero_fuego import HechiceroFuego
from Personajes.hechicero_hielo import HechiceroHielo

class PantallaInicio:
    def __init__(self, root, iniciar_callback):
        self.root = root
        self.iniciar_callback = iniciar_callback
        self.frame = tk.Frame(root, bg="#f0f8ff")
        self.frame.pack(fill=tk.BOTH, expand=True)

        titulo = tk.Label(self.frame, text="✨ Conjuro Eterno ✨", font=("Helvetica", 28, "bold"), fg="#002244", bg="#f0f8ff")
        titulo.pack(pady=20)

        label = tk.Label(self.frame, text="Nombre del Invocador:", fg="#003366", bg="#f0f8ff", font=("Helvetica", 14))
        label.pack(pady=10)

        self.entry_nombre = tk.Entry(self.frame, font=("Helvetica", 14), bg="white", fg="black")
        self.entry_nombre.pack(pady=10)

        boton = tk.Button(self.frame, text="Comenzar Partida", font=("Helvetica", 14), bg="#99ccff", fg="#002244", command=self.continuar)
        boton.pack(pady=20)

    def continuar(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Campo vacío", "Por favor, escribe tu nombre.")
            return
        self.frame.destroy()
        self.iniciar_callback(nombre)


class JuegoInterfaz:
    def __init__(self, root, jugador):
        self.root = root
        self.root.title("Conjuro Eterno - Batalla Mágica")
        self.root.geometry("900x600")
        self.root.configure(bg="#e6f2ff")

        self.jugador = jugador
        self.enemigos = [HechiceroFuego(), HechiceroHielo()]
        self.nivel = 0
        self.enemigo = self.enemigos[self.nivel]

        self.crear_layout()
        self.actualizar_estado()

    def crear_layout(self):
        self.frame_enemigo = tk.Frame(self.root, bg="#d1ecf1", height=200)
        self.frame_enemigo.pack(fill=tk.X, side=tk.TOP)

        self.label_enemigo = tk.Label(self.frame_enemigo, text="", fg="#003366", bg="#d1ecf1", font=("Helvetica", 16))
        self.label_enemigo.pack(pady=5)
        self.label_enemigo_salud = tk.Label(self.frame_enemigo, text="", fg="#003366", bg="#d1ecf1")
        self.label_enemigo_salud.pack()
        self.bar_enemigo_salud = ttk.Progressbar(self.frame_enemigo, length=300)
        self.bar_enemigo_salud.pack(pady=2)
        self.label_enemigo_mana = tk.Label(self.frame_enemigo, text="", fg="#003366", bg="#d1ecf1")
        self.label_enemigo_mana.pack()
        self.bar_enemigo_mana = ttk.Progressbar(self.frame_enemigo, length=300)
        self.bar_enemigo_mana.pack(pady=2)
        self.avatar_enemigo = tk.Label(self.frame_enemigo, text="🧟", font=("Arial", 30), bg="#d1ecf1")
        self.avatar_enemigo.pack(pady=5)

        self.frame_jugador = tk.Frame(self.root, bg="#d1e7dd", height=200)
        self.frame_jugador.pack(fill=tk.BOTH, expand=True)
        self.label_jugador = tk.Label(self.frame_jugador, text="", fg="#004422", bg="#d1e7dd", font=("Helvetica", 16))
        self.label_jugador.pack(pady=5)
        self.label_jugador_salud = tk.Label(self.frame_jugador, text="", fg="#004422", bg="#d1e7dd")
        self.label_jugador_salud.pack()
        self.bar_jugador_salud = ttk.Progressbar(self.frame_jugador, length=300)
        self.bar_jugador_salud.pack(pady=2)
        self.label_jugador_mana = tk.Label(self.frame_jugador, text="", fg="#004422", bg="#d1e7dd")
        self.label_jugador_mana.pack()
        self.bar_jugador_mana = ttk.Progressbar(self.frame_jugador, length=300)
        self.bar_jugador_mana.pack(pady=2)
        self.avatar_jugador = tk.Label(self.frame_jugador, text="🧙‍♂️", font=("Arial", 30), bg="#d1e7dd")
        self.avatar_jugador.pack(pady=5)

        self.frame_cartas = tk.Frame(self.root, bg="#e6f2ff")
        self.frame_cartas.pack(pady=10)

        self.botones = []
        for hechizo in self.jugador.hechizos:
            boton = tk.Button(
                self.frame_cartas,
                text=hechizo.nombre,
                width=15,
                height=2,
                font=("Helvetica", 12),
                bg="#cce5ff",
                fg="#003366",
                command=lambda h=hechizo: self.usar_hechizo(h.nombre)
            )
            boton.pack(side=tk.LEFT, padx=10)
            self.botones.append(boton)

        self.text_log = tk.Text(self.root, height=6, bg="#fdfdfe", fg="#333", font=("Consolas", 10))
        self.text_log.pack(fill=tk.X, padx=5)

        self.boton_reiniciar = tk.Button(self.root, text="🔄 Reiniciar Partida", font=("Helvetica", 12), bg="#ffcccc", fg="#660000", command=self.reiniciar_partida)
        self.boton_reiniciar.pack(pady=5)
        self.log("🎮 ¡Bienvenido a Conjuro Eterno! Prepara tus hechizos...\n")

    def usar_hechizo(self, nombre):
        if not self.jugador.esta_vivo():
            self.log("Has sido derrotado.\n")
            return

        resultado = self.jugador.usar_hechizo_especial(nombre, self.enemigo)
        self.log(resultado)

        if self.enemigo.esta_vivo():
            respuesta = self.enemigo.elegir_accion(self.jugador)
            self.log(respuesta)
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
                self.log("\n🎉 ¡Has ganado todos los combates!")

        self.actualizar_estado()

    def actualizar_estado(self):
        self.label_enemigo.config(text=f"{self.enemigo.nombre}")
        self.label_jugador.config(text=f"{self.jugador.nombre}")
        self.label_enemigo_salud.config(text=f"Salud: {self.enemigo.salud}/120")
        self.bar_enemigo_salud["value"] = self.enemigo.salud
        self.label_enemigo_mana.config(text=f"Maná: {self.enemigo.mana}/150")
        self.bar_enemigo_mana["value"] = self.enemigo.mana
        self.label_jugador_salud.config(text=f"Salud: {self.jugador.salud}/130")
        self.bar_jugador_salud["value"] = self.jugador.salud
        self.label_jugador_mana.config(text=f"Maná: {self.jugador.mana}/100")
        self.bar_jugador_mana["value"] = self.jugador.mana

    def reiniciar_partida(self):
        # Guarda el nombre actual del jugador
        nombre = self.jugador.nombre

        # Crea un nuevo jugador y reinicia enemigos
        self.jugador = PersonajePrincipal(nombre)
        self.enemigos = [HechiceroFuego(), HechiceroHielo()]
        self.nivel = 0
        self.enemigo = self.enemigos[self.nivel]

        # Limpia el log
        self.text_log.delete('1.0', tk.END)
        self.log("🔁 ¡Partida reiniciada!")

        # Elimina botones anteriores
        for boton in self.botones:
            boton.destroy()

        # Crea botones de hechizos nuevamente
        self.botones = []
        for hechizo in self.jugador.hechizos:
            boton = tk.Button(
                self.frame_cartas,
                text=hechizo.nombre,
                width=15,
                height=2,
                font=("Arial", 12),
                command=lambda h=hechizo: self.usar_hechizo(h.nombre)
            )
            boton.pack(side=tk.LEFT, padx=10)
            self.botones.append(boton)

        # Actualiza las barras de salud/mana
        self.actualizar_estado()


    def log(self, texto):
        self.text_log.insert(tk.END, texto + "\n")
        self.text_log.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    def iniciar(nombre):
        jugador = PersonajePrincipal(nombre)
        JuegoInterfaz(root, jugador)
    PantallaInicio(root, iniciar)
    root.mainloop()
