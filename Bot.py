import random as rd
from findingPaths import *


class Bot:
    def __init__(self, name, nrowalls, iq, initialpos, meta):
        self.name = name
        self.nroWalls = nrowalls
        self.lastMovements = [None, None]  # save last 2 moves
        self.IQ = iq
        self.pos = initialpos
        self.meta = meta

    # Metodo que realiza el movimiento del bot en el tablero.
    def performMovement(self, pos_opponent, meta_opponent, rows, columns, board_graph):
        cur_movement = self.chooseMovement()

        if (cur_movement == 0) and (self.putUpWalls(pos_opponent, meta_opponent, rows, columns, board_graph)):
            self.updateLastsMovements(cur_movement)
            return

        self.updateLastsMovements(1)
        self.moveOnTheBoard(rows, columns, board_graph)

    # Metodo que actualiza el historial de los movimientos del bot.
    def updateLastsMovements(self, newmovement):
        self.lastMovements[0] = self.lastMovements[1]
        self.lastMovements[1] = newmovement
        return

    # Metodo que elige el movimiento a realizar el bot.
    # 1: moveOnTheBoard, 0: putUpWalls
    def chooseMovement(self):

        if (self.lastMovements[1] is None) and (self.lastMovements[0] == self.lastMovements[1]):
            curmove = 1 if (self.lastMovements[1] == 0) else 1
        else:
            curmove = rd.randint(0, 1)

        return curmove

    # Metodo que devuelve si se pudo poner muro en el board.
    def putUpWalls(self, pos_opponent, meta_opponent, rows, columns, board_graph):
        path_opponent = BFS(pos_opponent, meta_opponent, rows, columns, board_graph)
        '''
        # for (cada par de nodo) en el path_opponent:
        #   new_board_graph = board_graph.removearista(par de nodo)
        #   if validotablero(new_board_graph):
        #       return par de nodos, True
        # Condicion -> Si sale del for: return None, None, False
        '''

        if not place_wall(path_opponent[0], path_opponent[1]):  # Todo: importar en este archivo la funcion ´place_wall´
            return False
        return True

    # Metodo que devuelve la posicion nueva del bot.
    def moveOnTheBoard(self, rows, columns, board_graph):
        path = None
        if self.IQ == 3:
            path = BFS(self.pos, self.meta, rows, columns, board_graph)
        elif self.IQ == 2:
            path = BruteForce(self.pos, self.meta, rows, columns, board_graph)
        elif self.IQ == 1:
            path = DFS(self.pos, self.meta, rows, columns, board_graph)

        self.pos = path[1]  # actualizamos la posicion del bot como atributo.
        return self.pos
