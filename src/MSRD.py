import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

#constantes
d1=1
d2=0.5
f=0.035
k=0.058

r1=0.396
r2=0.588

c1=2
c2=1

rows=200
columns=200

A = np.zeros((rows, columns))
B = np.zeros((rows, columns))
A_next = np.zeros((rows, columns))
B_next = np.zeros((rows, columns))

extraite=np.zeros((5,5))

grid = np.zeros((rows, columns, 3))

kernel=[[-0.25,-1,-1.5,-1,-0.25]
            [-1,2.5,7,2.5,-1]
          [-1.5,7,-23.5,7,-1.5]
            [-1,2.5,7,2.5,-1]
        [-0.25,-1,-1.5,-1,-0.25]]
#matrice du kernel pour RD avec voisinage de 5 par 5
#plus facile de changer les valeurs / plus lisible
#la complexité devrait rester la même



# on prend une matrice de 5*5 centrée autour du point (r,c)
def matriceExtraite5(A,r,c):
    for i in range(5):
        for j in range(5):
            extraite[i][j]=A[wrap(r-2+i,rows)][wrap(c-2+j,columns)]
    return extraite
    



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
            A_extraite=extraite(A,r,c)*d1   # le coef de diffusion
            A_extraite=np.multiply(A_extraite,kernel)
            A_next[r][c]+=A_extraite.sum()

            A_next[r][c] -= A[r][c] * B[r][c] * B[r][c]
            A_next[r][c] += f*(1-A[r][c])



    for r in range(rows):
        for c in range(columns):

            B_next[r][c] = B[r][c]
            B_extraite=extraite(B,r,c)*d1   # le coef de diffusion
            B_extraite=np.multiply(B_extraite,kernel)
            B_next[r][c]+=B_extraite.sum()


            B_next[r][c] += A[r][c] * B[r][c] * B[r][c]
            B_next[r][c] -= (f+k)*B[r][c]    



    for r in range(rows):
        for c in range(columns):
            A[r][c]=A_next[r][c]
            B[r][c]=B_next[r][c]





def wrap(a, limit):
    return((a+limit)%limit)



def main():
    print(0)


if __name__ == "__main__":
    main()