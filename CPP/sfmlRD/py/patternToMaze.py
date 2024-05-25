import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label, gaussian_filter
from skimage.morphology import skeletonize
import networkx as nx
from scipy.spatial import cKDTree
from skimage.draw import line
from heapq import heappop, heappush


fichier_chemin = 'bin/data/output.csv'
data = pd.read_csv(fichier_chemin, header=None)
data_array = data.to_numpy()

seuil = 0.5
grille_binaire = (data_array > seuil).astype(int)

# smoothing
grille_lissée = gaussian_filter(grille_binaire.astype(float), sigma=1.0)
grille_lissée_binaire = (grille_lissée > seuil).astype(int)

# skeleton
squelette = skeletonize(grille_lissée_binaire)


grille_combinee = grille_lissée_binaire | squelette
grille_inversee = 1 - grille_combinee

grille_etiquetée, nombre_de_composants = label(grille_inversee)

print(nombre_de_composants)


plt.imshow(grille_etiquetée, cmap='nipy_spectral')
plt.title('chambers')
plt.colorbar()
plt.show()


centroides = []
for region in range(1, nombre_de_composants + 1):
    coords = np.column_stack(np.where(grille_etiquetée == region))
    centroid = coords.mean(axis=0)
    centroides.append(centroid)

centroides = np.array(centroides)

# k-D arbre pour recherche efficace des voisins
arbre = cKDTree(centroides)

# Trouver les voisins dans un certain seuil de distance
seuil_distance = 10 
arêtes = arbre.query_pairs(seuil_distance)


G = nx.Graph()
for i, centroid in enumerate(centroides):
    G.add_node(i, pos=tuple(centroid))

for arête in arêtes:
    G.add_edge(*arête)


pos = nx.get_node_attributes(G, 'pos')
plt.figure(figsize=(10, 10))
nx.draw(G, pos, node_size=10, with_labels=False)
plt.title('Graphe des Chambres')
plt.show()

# arbre couvrant minimal à partir du graphe
mst = nx.minimum_spanning_tree(G)

plt.figure(figsize=(10, 10))
nx.draw(mst, pos, node_size=10, with_labels=False)
plt.title('Arbre Couvrant Minimal (Chemin du Labyrinthe)')
plt.show()

# Convertir le MST en grille pour visualiser le maze
grille_labyrinthe = np.zeros_like(grille_binaire)

for arête in mst.edges:
    start, end = arête
    start_pos = np.array(pos[start]).astype(int)
    end_pos = np.array(pos[end]).astype(int)
    rr, cc = line(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
    grille_labyrinthe[rr, cc] = 1

# Combiner la grille binaire originale et le chemin du labyrinthe
labyrinthe_final = np.where(grille_binaire == 1, 1, grille_labyrinthe)

# points D/A
point_depart = (1, 1)
point_arrivee = (grille_binaire.shape[0] // 2, grille_binaire.shape[1] // 2)


#algo A* 
def astar(maze, start, end):
    def heuristic(a, b):
        return np.linalg.norm(np.array(a) - np.array(b))
    
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, end)}
    oheap = []
    
    heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heappop(oheap)[1]
        
        if current == end:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            return data[::-1]
        
        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1
            if 0 <= neighbor[0] < maze.shape[0]:
                if 0 <= neighbor[1] < maze.shape[1]:
                    if maze[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return False


chemin = astar(labyrinthe_final, point_depart, point_arrivee)

if chemin:
    for point in chemin:
        labyrinthe_final[point[0], point[1]] = 0.5


    labyrinthe_final[point_depart] = 0.8
    labyrinthe_final[point_arrivee] = 0.8


    plt.imshow(labyrinthe_final, cmap='gray')
    plt.title('Labyrinthe Final avec Chemin')
    plt.show()
else:
    print("Chemin pas trouvé")
