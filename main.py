import heapq
import tkinter as tk
import time

mapa = [
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.posicion == other.posicion

    def __hash__(self):
        return hash(self.posicion)

    def __lt__(self, other):
        return self.f < other.f

def get_vecinos(nodo_actual, mapa):
    x, y = nodo_actual.posicion
    vecinos = []
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for movimiento in movimientos:
        nuevo_x = x + movimiento[0]
        nuevo_y = y + movimiento[1]
        if 0 <= nuevo_x < len(mapa) and 0 <= nuevo_y < len(mapa[0]):
            if mapa[nuevo_x][nuevo_y] == 0:
                vecinos.append(Nodo((nuevo_x, nuevo_y), nodo_actual))
    return vecinos

def distancia_euclidiana(nodo_actual, nodo_objetivo):
    x1, y1 = nodo_actual.posicion
    x2, y2 = nodo_objetivo.posicion
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def a_estrella(inicio, objetivo, mapa):
    lista_abierta = []
    lista_cerrada = set()
    nodo_inicio = Nodo(inicio)
    nodo_objetivo = Nodo(objetivo)
    heapq.heappush(lista_abierta, nodo_inicio)

    while lista_abierta:
        nodo_actual = heapq.heappop(lista_abierta)

        if nodo_actual.posicion == nodo_objetivo.posicion:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual.posicion)
                nodo_actual = nodo_actual.padre
            return camino[::-1]

        lista_cerrada.add(nodo_actual)

        vecinos = get_vecinos(nodo_actual, mapa)
        for vecino in vecinos:
            if vecino in lista_cerrada:
                continue

            vecino.g = nodo_actual.g + 1
            vecino.h = distancia_euclidiana(vecino, nodo_objetivo)
            vecino.f = vecino.g + vecino.h

            if vecino in lista_abierta:
                index = lista_abierta.index(vecino)
                if vecino.g < lista_abierta[index].g:
                    lista_abierta[index] = lista_abierta[-1]
                    lista_abierta.pop()
                    heapq.heapify(lista_abierta)
                    heapq.heappush(lista_abierta, vecino)
            else:
                heapq.heappush(lista_abierta, vecino)

    return None

class PacmanGame(tk.Tk):
    def __init__(self, mapa):
        super().__init__()
        self.title("Pac-Man")
        self.mapa = mapa
        self.pacman_pos = [1, 1]
        self.fantasmas = [
            {"pos": [7, 7], "color": "red", "tipo": "blinky"},  # Blinky (persigue directamente)
            {"pos": [7, 8], "color": "pink", "tipo": "pinky"},  # Pinky (adelanta a Pac-Man)
            {"pos": [7, 9], "color": "blue", "tipo": "inky"}    # Inky (intersecta)
        ]

        self.cell_size = 20
        self.canvas = tk.Canvas(self, width=len(mapa[0]) * self.cell_size, height=len(mapa) * self.cell_size)
        self.canvas.pack()
        self.bind("<KeyPress>", self.on_key_press)
        self.update_canvas()
        self.after(500, self.mover_fantasmas)

    def update_canvas(self):
        self.canvas.delete("all")
        for x in range(len(self.mapa)):
            for y in range(len(self.mapa[0])):
                color = "white"
                if (x, y) == tuple(self.pacman_pos):
                    color = "yellow"
                elif self.mapa[x][y] == 1:
                    color = "black"

                self.canvas.create_rectangle(
                    y * self.cell_size, x * self.cell_size,
                    (y + 1) * self.cell_size, (x + 1) * self.cell_size,
                    fill=color
                )
        for fantasma in self.fantasmas:
            x, y = fantasma["pos"]
            self.canvas.create_rectangle(
                y * self.cell_size, x * self.cell_size,
                (y + 1) * self.cell_size, (x + 1) * self.cell_size,
                fill=fantasma["color"]
            )
        self.update()

    def on_key_press(self, event):
        movimiento = event.keysym.upper()
        if movimiento == 'W' and self.pacman_pos[0] > 0 and self.mapa[self.pacman_pos[0] - 1][self.pacman_pos[1]] == 0:
            self.pacman_pos[0] -= 1
        elif movimiento == 'S' and self.pacman_pos[0] < len(self.mapa) - 1 and self.mapa[self.pacman_pos[0] + 1][self.pacman_pos[1]] == 0:
            self.pacman_pos[0] += 1
        elif movimiento == 'A' and self.pacman_pos[1] > 0 and self.mapa[self.pacman_pos[0]][self.pacman_pos[1] - 1] == 0:
            self.pacman_pos[1] -= 1
        elif movimiento == 'D' and self.pacman_pos[1] < len(self.mapa[0]) - 1 and self.mapa[self.pacman_pos[0]][self.pacman_pos[1] + 1] == 0:
            self.pacman_pos[1] += 1
        self.update_canvas()

    def mover_fantasmas(self):
        for fantasma in self.fantasmas:
            if fantasma["tipo"] == "blinky":
               
                # Blinky: Sigue el camino directo hacia Pac-Man osea el camino mas corto hacia el
                camino = a_estrella(tuple(fantasma["pos"]), tuple(self.pacman_pos), self.mapa)
                if camino and len(camino) > 1:
                    fantasma["pos"] = list(camino[1])

            elif fantasma["tipo"] == "pinky":
                # Pinky: Trata de adelantarse 4 casillas en la dirección de Pac-Man tratando de acorralarlo(no lo veo bien ya que se queda quieto pero en si si cumple su funcion) 
                target_pos = self.predecir_posicion_pacman(4)  # 4 casillas adelante
                camino = a_estrella(tuple(fantasma["pos"]), tuple(target_pos), self.mapa)
                if camino and len(camino) > 1:
                    fantasma["pos"] = list(camino[1])

            elif fantasma["tipo"] == "inky":
                # Inky: Ataca desde un ángulo basado en la posición de Blinky y Pac-Man, segun el rojo y pacman va a un 3er punto en el mapa
                # para acorralarlo pero este se queda quieto segun si esta muy lejos igual puede que sea por la forma del mapa o nose
                blinky_pos = next(f["pos"] for f in self.fantasmas if f["tipo"] == "blinky")
                target_pos = self.calcular_posicion_inky(blinky_pos)
                camino = a_estrella(tuple(fantasma["pos"]), tuple(target_pos), self.mapa)
                if camino and len(camino) > 1:
                    fantasma["pos"] = list(camino[1])

            # Verificar si el fantasma colisionaron
            if fantasma["pos"] == self.pacman_pos:
                self.game_over() 
                return 
        self.update_canvas()
        self.after(500, self.mover_fantasmas)

    def predecir_posicion_pacman(self, distancia):
        # Predecir la posición futura de Pac-Man según su dirección actual
        x, y = self.pacman_pos
        # Aquí puedes agregar lógica para predecir la posición según el movimiento
        return [x + distancia, y]  # Este es solo un ejemplo básico

    def calcular_posicion_inky(self, blinky_pos):
        # Inky se mueve en función de la posición de Pac-Man y Blinky
        pacman_x, pacman_y = self.pacman_pos
        blinky_x, blinky_y = blinky_pos
        # Calcular un punto "intermedio" entre Blinky y Pac-Man
        target_x = pacman_x + (pacman_x - blinky_x)
        target_y = pacman_y + (pacman_y - blinky_y)
        return [target_x, target_y]

    def game_over(self):
        self.canvas.create_text(
            len(self.mapa[0]) * self.cell_size // 2,
            len(self.mapa) * self.cell_size // 2,
            text="Game Over",
            font=("Arial", 24),
            fill="red"
        )
        self.update() 

if __name__ == "__main__":
    game = PacmanGame(mapa)
    game.mainloop()
