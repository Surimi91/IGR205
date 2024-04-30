import numpy as np
import pandas as pd

def generate_grid(rows, columns, white_chance=0.05):
    # grille random
    grid = np.random.choice([0, 1], size=(rows, columns), p=[1-white_chance, white_chance])
    return grid

def save_to_csv(grid, file_path):
    df = pd.DataFrame(grid)
    df.to_csv(file_path, header=False, index=False)

rows, columns = 200, 200  # doit etre comme le cpp
grid = generate_grid(rows, columns)
save_to_csv(grid, 'bin/data/grid.csv')
