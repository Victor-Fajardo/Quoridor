# Clase que contiene los algoritmos de busqueda de caminos en quoridor.
from collections import deque


def invalid(x, y, visited, rows, columns):
    return (x < 0) or (x >= rows) or (y < 0) or (y >= columns) \
           or (visited[x][y])


def reconstructionPath(ini, fin, dad):
    path = deque()
    ix = fin
    while ix is not dad[ini]:
        path.appendleft(ix)
        ix = dad[ix]
    return path


def BFS(ini, fin, rows, columns, Board_Graph):
    visit = [[False for col in range(columns)] for row in range(rows)]
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    dad = {}
    queue = deque()
    dad[ini] = (-1, -1)
    queue.appendleft(ini)
    # visited[ini[0]][ini[1]] = True
    while len(queue):
        cur = queue.popleft()
        visit[cur[0]][cur[1]] = True
        for op in range(4):
            nx, ny = cur[0] + dx[op], cur[1] + dy[op]
            if (not invalid(nx, ny, visit, rows, columns)) and (Board_Graph.has_edge(cur, (nx, ny))):
                queue.append((nx, ny))
                # visited[nx][ny] = True
                dad[(nx, ny)] = cur

    p = reconstructionPath(ini, fin, dad)
    return p


def DFS(ini, fin, rows, columns, Board_Graph):
    visit = [[False for col in range(columns)] for row in range(rows)]
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    dad = {}
    queue = deque()
    dad[ini] = (-1, -1)
    queue.appendleft(ini)
    # visit[ini[0]][ini[1]] = True
    while len(queue):
        cur = queue.pop()
        visit[cur[0]][cur[1]] = True
        for op in range(4):
            nx, ny = cur[0] + dx[op], cur[1] + dy[op]
            if (not invalid(nx, ny, visit, rows, columns)) and (Board_Graph.has_edge(cur, (nx, ny))):
                queue.append((nx, ny))
                # visit[nx][ny] = True
                dad[(nx, ny)] = cur

    p = reconstructionPath(ini, fin, dad)
    return p


def BruteForce(ini, fin, rows, columns, Board_Graph):
    queue = deque()
    queue.append(ini)

    def fuerza_bruta(ini, fin):
        if ini == fin:
            return

        visit = [[False for col in range(columns)] for row in range(rows)]
        nodoIniAux = ini
        pasoX = 0
        pasoY = 0
        visit[nodoIniAux[0]][nodoIniAux[1]] = True
        dx = [0, 0, 1, -1]
        dy = [1, -1, 0, 0]
        isValid = False
        if nodoIniAux[0] < fin[0]:
            # derecha
            pasoX += 1
        elif nodoIniAux[0] > fin[0]:
            # izquierda
            pasoX -= 1
        elif nodoIniAux[0] == fin[0]:
            if (nodoIniAux[1] < fin[1]):
                # abajo
                pasoY += 1
            elif (nodoIniAux[1] > fin[1]):
                # arriba
                pasoY -= 1

        nx, ny = nodoIniAux[0] + pasoX, nodoIniAux[1] + pasoY
        print("VALORES", nodoIniAux, ny)
        if (not invalid(nx, ny, visit, rows, columns)) and (Board_Graph.has_edge(nodoIniAux, (nx, ny))):
            ##se agrega el nodo valido
            isValid = True
            queue.append((nx, ny))
            fuerza_bruta((nx, ny), fin)
        if not isValid:
            for posi in range(4):
                nx, ny = nodoIniAux[0] + dx[posi], nodoIniAux[1] + dy[posi]
                if (not invalid(nx, ny, visit, rows, columns)) and (Board_Graph.has_edge(nodoIniAux, (nx, ny))):
                    ##se agrega el nodo valido
                    queue.append((nx, ny))
                    fuerza_bruta((nx, ny), fin)

    fuerza_bruta(ini, fin)
    return queue
