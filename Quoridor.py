import pygame
import networkx
import matplotlib.pyplot as plt
from collections import deque
import random as rd


#Board Size Defined:
global rows
global columns
rows = 9
columns = 9

#9x9 Board Graph creation
#(Rows, Columns) = (Y, X)
Board_Graph = networkx.Graph()
Board_Graph.add_nodes_from((i, j) for i in range(rows) for j in range(columns))
Board_Graph.add_edges_from((((i, j), (i - 1, j)) for i in range(rows) for j in range(columns) if i > 0))
Board_Graph.add_edges_from((((i, j), (i, j - 1)) for i in range(rows) for j in range(columns) if j > 0))

def BFS(ini, fin):
    time_start = pygame.time.get_ticks()
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
        cur = queue.popleft()
        visit[cur[0]][cur[1]] = True
        for op in range(4):
            nx, ny = cur[0] + dx[op], cur[1] + dy[op]
            if (not invalid(cur, nx, ny)) and (Board_Graph.has_edge(cur, (nx, ny))):
                queue.append((nx, ny))
                #visit[nx][ny] = True
                dad[(nx, ny)] = cur
    try:
        p = reconstructionPath()
    except Exception as e:
        return [], 0, False, visit
    else:
        time_end = pygame.time.get_ticks()
        time = time_end - time_start
        return p, time, True, visit
    #print(len(p))

def DFS(ini, fin):
    time_start = pygame.time.get_ticks()
    def invalid(x, y):
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
            if (not invalid(nx, ny)) and (Board_Graph.has_edge(cur, (nx, ny))):
                queue.append((nx, ny))
                #visit[nx][ny] = True
                dad[(nx, ny)] = cur

    try:
        p = reconstructionPath()
    except Exception as e:
        return [], 0, False, visit
    else:
        time_end = pygame.time.get_ticks()
        time = time_end - time_start
        return p, time, True, visit


def bellman_ford(start, end):
    time_start = pygame.time.get_ticks()
    p = networkx.bellman_ford_path(Board_Graph, start, end)
    time_end = pygame.time.get_ticks()
    time = time_end - time_start
    return p, time, True, []
    distancias = dict()
    anterior = dict()
    for V in list(Board_Graph):
        distancias[V] = float('Inf')
        anterior[V] = None
    distancias[start] = 0
    for V in list(Board_Graph):
        for u, v in Board_Graph.edges():
            distancia = distancias[u] + 1
            if distancia < distancias[v]:
                distancias[v] = distancia
                anterior[v] = u
    antes = anterior[end]
    path = [end]
    while antes != start and antes is not None:
        path.insert(0, antes)
        antes = anterior[antes]
    if antes == start:
        path.insert(0, start)
        return path
    return []

#====================================================#
#====================================================#
#====================================================#
#====================================================#
#====================================================#
#====================================================#



def performMovement(player_pos, bot_pos):
    cur_movement = chooseMovement()

    if (cur_movement == 0) and (putUpWalls(player_pos)):
        updateLastsMovements(cur_movement)
        return bot_pos

    updateLastsMovements(1)
    return moveOnTheBoard(bot_pos, player_pos)

    # Metodo que actualiza el historial de los movimientos del bot.
def updateLastsMovements(newmovement):
    last_movements[0] = last_movements[1]
    last_movements[1] = newmovement
    return 0

    # Metodo que elige el movimiento a realizar el bot.
    # 1: moveOnTheBoard, 0: putUpWalls
def chooseMovement():
    if (last_movements[1] is not None) and (last_movements[0] == last_movements[1]):
        curmove = (1 if (last_movements[1] == 0) else 0)
    else:
        curmove = rd.randint(0, 1)

    return curmove

    # Metodo que devuelve si se pudo poner muro en el board.
def putUpWalls(player_pos):
    player_path = BFS(player_pos, (8, player_pos[1]))

    if PlaceWall(player_path[0][0], player_path[0][1]):
        return True
    return False

    # Metodo que devuelve la posicion nueva del bot.
def moveOnTheBoard(bot_pos, player_pos):
    path = None
    if IQ == 3:
        path = BFS(bot_pos, (0,bot_pos[1]))
    elif IQ == 2:
        path = bellman_ford(bot_pos, (0,bot_pos[1]))
    elif IQ == 1:
        path = DFS(bot_pos, (0,bot_pos[1]))

    if (path[0][1] == player_pos) and (len(path[0]) > 2):
        bot_pos = path[0][2]
    else:
        bot_pos = path[0][1]
    return bot_pos


#====================================================#
#====================================================#
#====================================================#
#====================================================#
#====================================================#
#====================================================#
#Board visual representation using Pygame
pygame.init()

#Font created
pygame.font.init()
font = pygame.font.SysFont("verdana", 16)
font2 = pygame.font.SysFont("verdana", 69)

#Screen size defined:
global width
global height
width  = 800
height = 800
size = (width,height)

#Colors defined:
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
YELLOW	 = ( 255, 255,   0)

start_pos = (0, 0)
algorithm = 1
algorithm_name = "BFS"
path_lenght = 0
time = 0
path = None
mode = 0

#Game variables
global game_status
game_status = True
game_time = 0

#Player variables
player_pos = (0,4)
player_color = BLUE
player_turn = True
player_walls = 0

#Bot variables
bot_pos = (8,4)
bot_color = GREEN
bot_walls = 0
global last_movements
last_movements = [None, None]
global IQ
IQ = 3

#Screen created:
screen = pygame.display.set_mode(size)
done = False

#Walls declared:
walls = []

#Function to draw the board
def DrawBoard():
    SpaceX = int((width-100)/columns)
    SpaceY = int((height-100)/rows)
    for i in range(columns+1):
        x = 50 + SpaceX*i
        pygame.draw.line(screen, WHITE, (x,80), (x,SpaceX*columns+80))
    for i in range(rows+1):
        y = 80 + SpaceY*i
        pygame.draw.line(screen, WHITE, (50,y), (SpaceY*rows+50,y))

def ConvertMousePos(MousePos):
    SpaceX = int((width-100)/columns)
    SpaceY = int((height-100)/rows)
    x = int((MousePos[0]-50)/SpaceX)
    y = int((MousePos[1]-80)/SpaceY)

    return x, y

def FillSquare(color, pos):
    SpaceX = int((width-100)/columns)
    SpaceY = int((height-100)/rows)

    x0 = 50 + SpaceX*pos[0]
    y0 = 80 + SpaceY*pos[1]

    pygame.draw.rect(screen, color, [x0, y0, SpaceX, SpaceY], 0)

def DrawPath(path):
    if path != None:
        for i in range(len(path)):
            FillSquare(GREEN, path[i])

def DrawWall(node1, node2):
    SpaceX = int((width-100)/columns)
    SpaceY = int((height-100)/rows)

    if node1[0] == node2[0]:
        x0 = 50 + SpaceX*node1[0]
        y0 = 80 + SpaceY*node2[1]
        x  = 50 + SpaceX*(node2[0]+1)
        y  = y0
    elif node1[1] == node2[1]:
        x0 = 50 + SpaceX*node2[0]
        y0 = 80 + SpaceY*node1[1]
        x  = x0
        y  = 80 + SpaceY*(node2[1]+1)

    pygame.draw.line(screen, RED, (x0, y0), (x, y), 5)

#Creating a wall will delete the edge
def RemoveEdge(start, end):
    Board_Graph.remove_edge((start[0], start[1]), (end[0], end[1]))
    return 0
'''
def VerifyWall(start, end):
    if len(walls) < 20:
        if BFS(start, (0,0))[2]:
            if BFS(start, (0,8))[2]:
                if BFS(start, (8,0))[2]:
                    if BFS(start, (8,8))[2]:
                        if BFS(start, (5,5))[2]:
                            if BFS((0,0), end)[2]:
                                if BFS((0,8), end)[2]:
                                    if BFS((8,0), end)[2]:
                                        if BFS((8,8), end)[2]:
                                            if BFS((4,4), end)[2]:
                                                return True
    return False
'''

def VerifyWall(start, end):
    if len(walls) < 20:
        results = BFS(start, end)
        if results[2]:
            for arr in results[3]:
                for elem in arr:
                    if not elem:
                        return False
                return True
    return False

def PlaceWall(start, end):
    if Board_Graph.has_edge(start, end):
        RemoveEdge(start, end)
        if VerifyWall(start, end):
            walls.append((start, end))
            return True
        Board_Graph.add_edge(start, end)
        print("No se puede encerrar un area")
        return False
    return False

def VerticalPlacement(MousePos):
    SpaceY = int((height-100)/rows)
    y = int((MousePos[1]-80)/SpaceY)

    SpaceX = int((width-100)/columns)
    x = round((MousePos[0]-50)/SpaceX)
    aux = int((MousePos[0]-50)/SpaceX)

    if x > aux:
        x2 = x
        x = aux
    elif x == aux:
        x2 = x
        x = aux-1

    start = (x, y)
    end = (x2, y)

    return PlaceWall(start, end)

def HorizontalPlacement(MousePos):
    SpaceX = int((width-100)/columns)
    x = int((MousePos[0]-50)/SpaceX)

    SpaceY = int((height-100)/rows)
    y = round((MousePos[1]-80)/SpaceY)
    aux = int((MousePos[1]-80)/SpaceY)

    if y > aux:
        y2 = y
        y = aux
    elif y == aux:
        y2 = y
        y = aux-1

    start = (x, y)
    end = (x, y2)

    return PlaceWall(start, end)

#Player functions:
def Move(actual, target):
    if abs(actual[0]-target[0]+actual[1]-target[1]) == 1:
        if Board_Graph.has_edge(actual, target) and bot_pos != target:
            return True
    return False

#Update screen
def RefreshScreen():
    screen.blit(instructions1, (0, 0))
    screen.blit(instructions2, (0, 16))
    screen.blit(instructions3, (0, 32))
    FillSquare(player_color, player_pos)
    FillSquare(bot_color, bot_pos)
    DrawBoard()

    for i in walls:
        DrawWall(i[0], i[1])

    if not game_status:
        screen.blit(game_over, (200, height-500))
        screen.blit(winner, (200, height-450))
    pygame.display.flip()

#Game Loop:
while not done:

    #Win condition
    if player_pos[0] == 8 or bot_pos[0] == 0:
        game_status = False

    if not player_turn:
            if game_status:
                pygame.time.delay(500)
                bot_pos = performMovement(player_pos, bot_pos)
                player_turn = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if player_turn:
            #Clicking a tile will create a path to it from (0, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mode == 0:
                        mouse_pos = ConvertMousePos(pygame.mouse.get_pos())
                        if Move(player_pos, mouse_pos):
                            player_pos = mouse_pos
                            screen.fill(BLACK)
                            player_turn = False
                    if mode == 1:
                        if VerticalPlacement(pygame.mouse.get_pos()):
                            player_turn = False
                    if mode == 2:
                        if HorizontalPlacement(pygame.mouse.get_pos()):
                            player_turn = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    mode = 0
                if event.key == pygame.K_w:
                    mode = 1
                if event.key == pygame.K_e:
                    mode = 2

    if path != None:
        if len(path) > 0:
            start_pos = path[0]
            path.popleft()

    screen.fill(BLACK)
    instructions1 = font.render("Click izquierdo -> Seleccionar punto de inicio", True, WHITE)
    instructions2 = font.render("Click derecho -> Generar camino", True, WHITE)
    instructions3 = font.render("1, 2 y 3-> Cambiar de algoritmo", True, WHITE)
    game_over = font2.render("Game Over", True, RED)
    winner = font2.render("Ha Ganado", True, RED)
    pygame.time.delay(30)
    DrawPath(path)
    RefreshScreen()