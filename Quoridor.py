import pygame
import networkx
import matplotlib.pyplot as plt
from collections import deque

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

#Creating a wall will delete the edge
def RemoveEdge(G, x0, y0, x1, y1):
	G.remove_edge((y0, x0), (y1, x1))
	return G

#ToDo:
#Algorithm to place walls 
def PlaceWall():
	#If degree return more than 1 then a wall can be placed
	Board_Graph.degree[(0,0)]

def BFS(ini, fin):
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

    p = reconstructionPath()
    print(len(p))
    return p

#Display Graph
#networkx.draw(Board_Graph, with_labels = True, node_size = 50)
#plt.show()

#=============#
#=============#
#=============#
#=============#
#=============#
#=============#

#Board visual representation using Pygame
pygame.init()

#Font created
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)

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

#Screen created:
screen = pygame.display.set_mode(size)
done = False

#Function to draw the board
def DrawBoard():
	SpaceX = int((width-100)/columns)
	SpaceY = int((height-100)/rows)
	for i in range(columns+1):
		x = 50 + SpaceX*i
		pygame.draw.line(screen, BLUE, (x,50), (x,height-50))
	for i in range(rows+1):
		y = 50 + SpaceY*i
		pygame.draw.line(screen, BLUE, (50,y), (width-50,y))

def ConvertMousePos(MousePos):
	SpaceX = int((width-100)/columns)
	SpaceY = int((height-100)/rows)
	x = int((MousePos[0]-50)/SpaceX)
	y = int((MousePos[1]-50)/SpaceY)

	return x, y

def FillSquare(color, pos):
	SpaceX = int((width-100)/columns)
	SpaceY = int((height-100)/rows)

	x0 = 50 + SpaceX*pos[0]
	y0 = 50 + SpaceY*pos[1]

	pygame.draw.rect(screen, color, [x0, y0, SpaceX, SpaceY], 0)


#Game Loop:
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
        	done = True
        #Clicking a tile will create a path to it from (0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
        	pos = ConvertMousePos(pygame.mouse.get_pos())
        	path =  BFS((0,0), pos)
        	for i in range(len(path)):
        		FillSquare(GREEN, path[i])
        #Pressing 4 will clear the board
        if event.type == pygame.KEYDOWN:
        	if event.key == pygame.K_4:
        		screen.fill(BLACK)

    instructions1 = font.render("Hacer click en un recuadro para generar un camino", True, WHITE)
    instructions2 = font.render("Presionar 4 para limpiar el tablero", True, WHITE)
    screen.blit(instructions1, (0, 0))
    screen.blit(instructions2, (0, 20))
    DrawBoard()
    pygame.display.flip()