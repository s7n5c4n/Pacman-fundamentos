import heapq
import tkinter as tk
import time

# El mapa con los fantasmas estáticos como obstáculos (se representan con 2)
mapa = [
    [3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 2, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1],  # Fantasmas estáticos (2)
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
            if mapa[nuevo_x][nuevo_y] == 0:  # Considerar solo casillas vacías y no fantasmas (2)
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
        self.title("Pac-Man Automático")
        self.mapa = mapa
        self.pacman_pos = [0, 0]  # Posición inicial de Pac-Man
        self.comida = self.generar_comida()
        self.cell_size = 20
        self.canvas = tk.Canvas(self, width=len(mapa[0]) * self.cell_size, height=len(mapa) * self.cell_size)
        self.canvas.pack()
        self.update_canvas()
        self.after(500, self.mover_pacman)

    def generar_comida(self):
        comida = []
        for x in range(len(self.mapa)):
            for y in range(len(self.mapa[0])):
                if self.mapa[x][y] == 0:  # Agregar comida en las casillas vacías
                    comida.append([x, y])
        return comida

    def update_canvas(self):
        # Limpiar el canvas
        self.canvas.delete("all")
        
        # Dibujar el mapa
        for fila in range(len(self.mapa)):
            for col in range(len(self.mapa[fila])):
                if self.mapa[fila][col] == 1:
                    # Dibujar paredes
                    self.canvas.create_rectangle(
                        col * self.cell_size, fila * self.cell_size,
                        (col + 1) * self.cell_size, (fila + 1) * self.cell_size,
                        fill="blue"
                    )
                elif self.mapa[fila][col] == 2:
                    # Dibujar fantasmas estáticos
                    self.canvas.create_rectangle(
                        col * self.cell_size, fila * self.cell_size,
                        (col + 1) * self.cell_size, (fila + 1) * self.cell_size,
                        fill="red"
                    )
        
        # Dibujar comida
        for (x, y) in self.comida:
            self.canvas.create_oval(
                y * self.cell_size + 5, x * self.cell_size + 5,
                (y + 1) * self.cell_size - 5, (x + 1) * self.cell_size - 5,
                fill="yellow"
            )
        
        # Dibujar Pac-Man
        pacman_x, pacman_y = self.pacman_pos
        self.canvas.create_oval(
            pacman_y * self.cell_size, pacman_x * self.cell_size,
            (pacman_y + 1) * self.cell_size, (pacman_x + 1) * self.cell_size,
            fill="green"
        )

    def mover_pacman(self):
        if self.comida:
            comida_mas_cercana = min(self.comida, key=lambda c: distancia_euclidiana(Nodo(self.pacman_pos), Nodo(c)))
            camino = a_estrella(tuple(self.pacman_pos), tuple(comida_mas_cercana), self.mapa)
            if camino and len(camino) > 1:
                self.pacman_pos = list(camino[1])

                if self.pacman_pos in self.comida:
                    self.comida.remove(self.pacman_pos)

                self.update_canvas()
                self.after(500, self.mover_pacman)
            else:
                print("No se encontró un camino.")
        else:
            print("¡Pac-Man ha comido toda la comida!")

if __name__ == "__main__":
    game = PacmanGame(mapa)
    game.mainloop()
