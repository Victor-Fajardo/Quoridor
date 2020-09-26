import pygame
import networkx
import matplotlib.pyplot as plt

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

#Display Graph
networkx.draw(Board_Graph, with_labels = True, node_size = 50)
plt.show()

#=============#
#=============#
#=============#
#=============#
#=============#
#=============#

#Board visual representation using Pygame
pygame.init()

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
	ScapeY = int((height-100)/rows)
	for i in range(columns+1):
		x = 50 + SpaceX*i
		pygame.draw.line(screen, BLUE, (x,50), (x,height-50))
	for i in range(rows+1):
		y = 50 + ScapeY*i
		pygame.draw.line(screen, BLUE, (50,y), (width-50,y))

#Game Loop:
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
        	done = True
    screen.fill(BLACK)
    DrawBoard()
    pygame.display.flip()