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
def RemoveEdge(x0, y0, x1, y1):
	Board_Graph.remove_edge((x0, y0), (x1, y1))
	return 0

'''
RemoveEdge(0,0,0,1)
RemoveEdge(0,2,1,2)
RemoveEdge(7,5,8,5)
RemoveEdge(4,3,4,4)
RemoveEdge(0,6,1,6)
RemoveEdge(2,0,3,0)
'''
#ToDo:
#Algorithm to place walls 
#def PlaceWall():
	#If degree return more than 1 then a wall can be placed
#	Board_Graph.degree[(0,0)]

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

	p = reconstructionPath()
	#print(len(p))
	time_end = pygame.time.get_ticks()
	time = time_end - time_start
	return p, time

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

	p = reconstructionPath()
	#print(len(p))
	time_end = pygame.time.get_ticks()
	time = time_end - time_start
	return p, time

def BruteForce(ini, fin):
	time_start = pygame.time.get_ticks()
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
		elif nodoIniAux[0] > fin[0]:
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
	time_end = pygame.time.get_ticks()
	time = time_end - time_start
	return queue, time

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

#Screen size defined:
global width
global height
width  = 800
height = 800
size = (width,height)

start_pos = (0, 0)
algorithm = 1
algorithm_name = "BFS"
path_lenght = 0
time = 0
path = None

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
		pygame.draw.line(screen, BLUE, (x,80), (x,SpaceX*columns+80))
	for i in range(rows+1):
		y = 80 + SpaceY*i
		pygame.draw.line(screen, BLUE, (50,y), (SpaceY*rows+50,y))

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

	pygame.draw.line(screen, WHITE, (x0, y0), (x, y), 5)

def RefreshScreen():
	screen.blit(instructions1, (0, 0))
	screen.blit(instructions2, (0, 16))
	screen.blit(instructions3, (0, 32))
	screen.blit(alg_name, (width-200, 0))
	screen.blit(alg_time, (0, height-21))
	screen.blit(path_len, (width-200, height-21))
	FillSquare(RED, start_pos)
	DrawBoard()
	'''
	DrawWall((0,0), (0,1))
	DrawWall((0,2), (1,2))
	DrawWall((7,5), (8,5))
	DrawWall((4,3), (4,4))
	DrawWall((0,6), (1,6))
	DrawWall((2,0), (3,0))
	'''
	pygame.display.flip()

#Game Loop:
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			done = True
		#Clicking a tile will create a path to it from (0, 0)
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				pos = ConvertMousePos(pygame.mouse.get_pos())
				start_pos = pos
				screen.fill(BLACK)
				path = ()

			if event.button == 3:
				pos = ConvertMousePos(pygame.mouse.get_pos())

				if algorithm == 1:
					alg_result = BFS(start_pos, pos)
				elif algorithm == 2:
					alg_result = DFS(start_pos, pos)
				elif algorithm == 3:
					alg_result = BruteForce(start_pos, pos)

				path = alg_result[0]
				path_lenght = len(path)
				time = alg_result[1]
				screen.fill(BLACK)
				for i in range(len(path)):
					FillSquare(GREEN, path[i])
					#Delay added
					pygame.time.delay(50)
					RefreshScreen()


		#Algorithm selection
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				algorithm = 1
				algorithm_name = "BFS"
				screen.fill(BLACK)
			if event.key == pygame.K_2:
				algorithm = 2
				algorithm_name = "DFS"
				screen.fill(BLACK)
			if event.key == pygame.K_3:
				algorithm = 3
				algorithm_name = "Fuerza Bruta"
				screen.fill(BLACK)

	if path != None:
		if len(path) > 0:
			start_pos = path[0]
			path.popleft()

	screen.fill(BLACK)
	instructions1 = font.render("Click izquierdo -> Seleccionar punto de inicio", True, WHITE)
	instructions2 = font.render("Click derecho -> Generar camino", True, WHITE)
	instructions3 = font.render("1, 2 y 3-> Cambiar de algoritmo", True, WHITE)
	alg_name = font.render("Algoritmo: " + str(algorithm_name), True, WHITE)
	alg_time = font.render("Tiempo de ejecucion: "+ str(time) + "ms", True, WHITE)
	path_len = font.render("Nodos recorridos: " + str(path_lenght), True, WHITE)
	pygame.time.delay(50)
	DrawPath(path)
	RefreshScreen()