import random as rd
from findingPaths import *


class Bot:
    def __init__(self, name, nrowalls, iq, initialpos, meta):
        self.name = name
        self.nroWalls = nrowalls
        self.lastMoves = [None, None]  # save last 2 moves
        self.IQ = iq
        self.pos = initialpos
        self.meta = meta

    def chooseMovement(self):
        curmove = None  # 1: moveOnTheBoard, 0: putUpWalls

        if (self.lastMoves[1] is None) and (self.lastMoves[0] == self.lastMoves[1]):
            curmove = 1 if (self.lastMoves[1] == 0) else 1
        else:
            curmove = rd.randint(0, 1)

        self.lastMoves[0] = self.lastMoves[1]
        self.lastMoves[1] = curmove
        return curmove

    def putUpWalls(self, pos_opponent, meta_opponent, rows, columns, board_graph):
        path_opponent = BFS(pos_opponent, meta_opponent, rows, columns, board_graph)

        # for (cada par de nodo) en el path_opponent:
        #   new_board_graph = board_graph.removearista(par de nodo)
        #   if validotablero(new_board_graph):
        #       return par de nodos, True
        # Condicion -> Si sale del for: return None, None, False
        return

    def moveOnTheBoard(self, rows, columns, board_graph):
        # ToDo
        path = None
        if self.IQ == 3:
            path = BFS(self.pos, self.meta, rows, columns, board_graph)
        elif self.IQ == 2:
            path = BruteForce(self.pos, self.meta, rows, columns, board_graph)
        elif self.IQ == 1:
            path = DFS(self.pos, self.meta, rows, columns, board_graph)

        self.pos = path[1] # actualizamos la posicion del bot como atributo.
        return path[1]
