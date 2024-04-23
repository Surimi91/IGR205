import RD_grid
import CannyEdge as edge
import fill_outside
import matplotlib.pyplot as plt


image_path = 'media/image200.png'
binary_grid = edge.canny_edge_to_binary_grid(image_path)
binary_grid=fill_outside.fill(binary_grid)


grid=(RD_grid.getPattern())    #grid ok

lenght=len(binary_grid)
for i in range(lenght):
    for j in range(lenght):
        if (binary_grid[i][j]==0):
            grid[i][j]=[0,0,0]


plt.imshow(grid, interpolation='nearest')
plt.show()