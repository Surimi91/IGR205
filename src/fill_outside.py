import numpy as np

def fill(grid):  #on suppose ici que la grille est carrée
    n=len(grid)

    for i in range(n): # pour chaque ligne

        j=0
        while(grid[i][j]==1):
            grid[i][j]=0
            j+=1


        j=0
        while(grid[i][n-j-1]==1):
            grid[i][n-j-1]=0
            j+=1

    return grid