import numpy as np

def create_circular_object(grid_size, radius):
    grid = np.zeros((grid_size, grid_size))
    center = grid_size // 2
    
    for x in range(grid_size):
        for y in range(grid_size):
            if (x - center) ** 2 + (y - center) ** 2 <= radius ** 2:
                grid[x, y] = 1
    return grid

grid_size = 100
radius = 30  

binary_grid = create_circular_object(grid_size, radius)