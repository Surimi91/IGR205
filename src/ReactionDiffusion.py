import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import grid
import random

#constantes
d1=1
d2=0.5
f=0.035
k=0.058

rows=200
columns=200

A = np.zeros((rows, columns))
B = np.zeros((rows, columns))
A_next = np.zeros((rows, columns))
B_next = np.zeros((rows, columns))

grid = np.zeros((rows, columns, 3))


def setup():
    for r in range(rows):
        for c in range(columns):
            A[r][c] = 1
            B[r][c] = 0  #il faut du B mais on initialise comme ça
            A_next[r][c] = 0
            B_next[r][c] = 0
            if (random.randint(0,100)<5):
                A[r][c] = 0
                B[r][c] = 1



def draw():
    for r in range(rows):
        for c in range(columns):
            grid[r][c]=[A[r][c], B[r][c], 0]   # pas besoin *255

    update()  #update les valeurs des produits A et B




def update():
    for r in range(rows):
        for c in range(columns):

            A_next[r][c] = A[r][c]
            A_next[r][c] += A[wrap(r-1,rows)][wrap(c-1,columns)]*d1*0.05  #coins
            A_next[r][c] += A[wrap(r-1,rows)][wrap(c+1,columns)]*d1*0.05
            A_next[r][c] += A[wrap(r+1,rows)][wrap(c-1,columns)]*d1*0.05
            A_next[r][c] += A[wrap(r+1,rows)][wrap(c+1,columns)]*d1*0.05

            A_next[r][c] += A[wrap(r-1,rows)][wrap(c,columns)]*d1*0.2   #juste à côté
            A_next[r][c] += A[wrap(r+1,rows)][wrap(c,columns)]*d1*0.2
            A_next[r][c] += A[wrap(r,rows)][wrap(c-1,columns)]*d1*0.2
            A_next[r][c] += A[wrap(r,rows)][wrap(c+1,columns)]*d1*0.2

            A_next[r][c] -= A[r][c]*d1     #retrancher la cellule du centre

            A_next[r][c] -= A[r][c] * B[r][c] * B[r][c]
            A_next[r][c] += f*(1-A[r][c])



    for r in range(rows):
        for c in range(columns):

            B_next[r][c] = B[r][c]
            B_next[r][c] += B_next[wrap(r-1,rows)][wrap(c-1,columns)]*d2*0.05  #coins
            B_next[r][c] += B[wrap(r-1,rows)][wrap(c+1,columns)]*d2*0.05
            B_next[r][c] += B[wrap(r+1,rows)][wrap(c-1,columns)]*d2*0.05
            B_next[r][c] += B[wrap(r+1,rows)][wrap(c+1,columns)]*d2*0.05

            B_next[r][c] += B[wrap(r-1,rows)][wrap(c,columns)]*d2*0.2   #juste à côté
            B_next[r][c] += B[wrap(r+1,rows)][wrap(c,columns)]*d2*0.2
            B_next[r][c] += B[wrap(r,rows)][wrap(c-1,columns)]*d2*0.2
            B_next[r][c] += B[wrap(r,rows)][wrap(c+1,columns)]*d2*0.2

            B_next[r][c] -= B[r][c]*d2     #retrancher la cellule du centre

            B_next[r][c] += A[r][c] * B[r][c] * B[r][c]
            B_next[r][c] -= (f+k)*B[r][c]    



    for r in range(rows):
        for c in range(columns):
            A[r][c]=A_next[r][c]
            B[r][c]=B_next[r][c]





def wrap(a, limit):
    return((a+limit)%limit)



def animate(i):
    for k in range(30):   # x steps
        draw()
    plt.imshow(grid, interpolation='nearest')
    plt.title(f"Etape {i*30}")


def main():
    setup()
    fig = plt.figure()
    ani = FuncAnimation(fig, animate, frames=100, interval=500)  # 100 frames, 1000ms between frames
    plt.show()


if __name__ == "__main__":
    main()