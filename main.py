import heapq

# Definición del mapa del juego
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

def main():
    inicio_pacman = (1, 1)
    objetivo_comida = (2, 2)
    camino = a_estrella(inicio_pacman, objetivo_comida, mapa)
    if camino:
        print("Camino encontrado:", camino)
    else:
        print("No hay camino disponible")

if __name__ == "__main__":
    main()