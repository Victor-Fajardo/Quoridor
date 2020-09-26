import pygame
import networkx
import matplotlib.pyplot as plt


#9x9 Board Graph creation
Board_Graph = networkx.Graph()
rows = range(9)
columns = range(9)
Board_Graph.add_nodes_from((i, j) for i in rows for j in columns)
Board_Graph.add_edges_from((((i, j), (i - 1, j)) for i in rows for j in columns if i > 0), weight=1)
Board_Graph.add_edges_from((((i, j), (i, j - 1)) for i in rows for j in columns if j > 0), weight=1)


networkx.draw(Board_Graph)
plt.show()


'''pygame.init()

size = (500,500)
black = (0, 0, 0)

screen = pygame.display.set_mode(size)
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
        	done = True
    screen.fill(black)
    pygame.display.flip()
'''