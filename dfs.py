#import pygame
import networkx
import matplotlib.pyplot as plt
from collections import deque

rows = 9
columns = 9

Board_Graph = networkx.Graph()
Board_Graph.add_nodes_from((i, j) for i in range(rows) for j in range(columns))
Board_Graph.add_edges_from((((i, j), (i - 1, j)) for i in range(rows) for j in range(columns) if i > 0))
Board_Graph.add_edges_from((((i, j), (i, j - 1)) for i in range(rows) for j in range(columns) if j > 0))

print(Board_Graph.has_edge((0, 0), (0, 1)))


def dfs(ini, fin):
    def invalid(auxcur, x, y):
        return (x < 0) or (x >= rows) or (y < 0) or (y >= columns) \
               or (visit[x][y])

    def reconstructionPath():
        path = deque()
        ix = fin
        while ix is not dad[ini]:
            path.appendleft(ix)
            ix = dad[ix]

        return path

    visit = [[False for col in range(columns)] for row in range(rows)]
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    dad = {}
    queue = deque()
    dad[ini] = (-1, -1)
    queue.appendleft(ini)
    #visit[ini[0]][ini[1]] = True
    while len(queue):
        cur = queue.pop()
        visit[cur[0]][cur[1]] = True
        for op in range(4):
            nx, ny = cur[0] + dx[op], cur[1] + dy[op]
            if (not invalid(cur, nx, ny)) and (Board_Graph.has_edge(cur, (nx, ny))):
                queue.append((nx, ny))
                #visit[nx][ny] = True
                dad[(nx, ny)] = cur

    p = reconstructionPath()
    print(len(p))
    return p


#Display Graph
#networkx.draw(Board_Graph, with_labels = True, node_size = 50)
#plt.show()
print(dfs( (0, 0), (8, 8) ))
