import networkx
import matplotlib.pyplot as plt
from collections import deque

rows = 9
columns = 9

Board_Graph = networkx.Graph()
Board_Graph.add_nodes_from((i, j) for i in range(rows) for j in range(columns))
Board_Graph.add_edges_from((((i, j), (i - 1, j)) for i in range(rows) for j in range(columns) if i > 0))
Board_Graph.add_edges_from((((i, j), (i, j - 1)) for i in range(rows) for j in range(columns) if j > 0))


def fb(ini, fin):
    queue = deque()
    queue.append(ini)

    def fuerza_bruta(ini, fin):
        if ini == fin:
            return

        def invalid(x, y):
            return (x < 0) or (x >= rows) or (y < 0) or (y >= columns) \
                   or (visit[x][y])

        visit = [[False for col in range(columns)] for row in range(rows)]
        nodoIniAux = ini
        pasoX = 0
        pasoY = 0
        visit[nodoIniAux[0]][nodoIniAux[1]] = True

        if nodoIniAux[0] < fin[0]:
            pasoX += 1
        elif nodoIniAux[0] < fin[0]:
            pasoX -= 1
        elif nodoIniAux[0] == fin[0]:
            if (nodoIniAux[1] < fin[1]):
                pasoY += 1
            elif (nodoIniAux[1] > fin[1]):
                pasoY -= 1

        nx, ny = nodoIniAux[0] + pasoX, nodoIniAux[1] + pasoY
        if (not invalid(nx, ny)) and (Board_Graph.has_edge(nodoIniAux, (nx, ny))):
            ##se agrega el nodo valido
            queue.append((nx, ny))
            fuerza_bruta((nx, ny), fin)

    fuerza_bruta(ini, fin)
    return queue


networkx.draw(Board_Graph, with_labels=True, node_size=50)
plt.show()
var = fb((1, 1), (8, 7))
print(var)
print(len(var))
