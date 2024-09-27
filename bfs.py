import tkinter as tk
import time
from collections import deque

mapa = [
    [3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 2, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 2, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre

    def __eq__(self, other):
        return self.posicion == other.posicion

    def __hash__(self):
        return hash(self.posicion)

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

def bfs(inicio, objetivo, mapa):
    queue = deque([Nodo(inicio)])
    visitados = set()
    iteraciones = 0

    while queue:
        iteraciones += 1
        nodo_actual = queue.popleft()

        if nodo_actual.posicion == objetivo:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual.posicion)
                nodo_actual = nodo_actual.padre
            return camino[::-1], iteraciones

        if nodo_actual.posicion not in visitados:
            visitados.add(nodo_actual.posicion)
            vecinos = get_vecinos(nodo_actual, mapa)
            queue.extend(vecinos) 

    return None, iteraciones

class PacmanGame(tk.Tk):
    def __init__(self, mapa):
        super().__init__()
        self.title("Pac-Man Automático (BFS)")
        self.mapa = mapa
        self.pacman_pos = [0, 0]
        self.comida = self.generar_comida()
        self.cell_size = 20
        self.canvas = tk.Canvas(self, width=len(mapa[0]) * self.cell_size, height=len(mapa) * self.cell_size)
        self.canvas.pack()
        self.update_canvas()
        self.after(500, self.mover_pacman)
        self.total_iteraciones = 0
        self.tiempo_inicio_total = time.time()

    def generar_comida(self):
        comida = []
        for x in range(len(self.mapa)):
            for y in range(len(self.mapa[0])):
                if self.mapa[x][y] == 0: 
                    comida.append([x, y])
        return comida

    def update_canvas(self):
        self.canvas.delete("all")
        
        for fila in range(len(self.mapa)):
            for col in range(len(self.mapa[fila])):
                if self.mapa[fila][col] == 1:
                    self.canvas.create_rectangle(
                        col * self.cell_size, fila * self.cell_size,
                        (col + 1) * self.cell_size, (fila + 1) * self.cell_size,
                        fill="blue"
                    )
                elif self.mapa[fila][col] == 2:
                    self.canvas.create_rectangle(
                        col * self.cell_size, fila * self.cell_size,
                        (col + 1) * self.cell_size, (fila + 1) * self.cell_size,
                        fill="red"
                    )

        for (x, y) in self.comida:
            self.canvas.create_oval(
                y * self.cell_size + 5, x * self.cell_size + 5,
                (y + 1) * self.cell_size - 5, (x + 1) * self.cell_size - 5,
                fill="yellow"
            )
        
        pacman_x, pacman_y = self.pacman_pos
        self.canvas.create_oval(
            pacman_y * self.cell_size, pacman_x * self.cell_size,
            (pacman_y + 1) * self.cell_size, (pacman_x + 1) * self.cell_size,
            fill="green"
        )

    def mover_pacman(self):
        if self.comida:
            comida_mas_cercana = min(self.comida, key=lambda c: (c[0] - self.pacman_pos[0])**2 + (c[1] - self.pacman_pos[1])**2)
            camino, iteraciones = bfs(tuple(self.pacman_pos), tuple(comida_mas_cercana), self.mapa)
            self.total_iteraciones += iteraciones

            if camino and len(camino) > 1:
                self.pacman_pos = list(camino[1])

                if self.pacman_pos in self.comida:
                    self.comida.remove(self.pacman_pos)

                self.update_canvas()
                self.after(500, self.mover_pacman)
            else:
                print("No se encontró un camino.")
        else:
            # Fin del juego
            tiempo_fin_total = time.time()
            print(f"Pac-Man ha comido toda la comida.")
            print(f"Iteraciones totales: {self.total_iteraciones}")
            print(f"Tiempo total de ejecución: {tiempo_fin_total - self.tiempo_inicio_total:.4f} segundos")

if __name__ == "__main__":
    game = PacmanGame(mapa)
    game.mainloop()