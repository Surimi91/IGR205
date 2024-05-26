import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import label2rgb
from scipy.spatial import distance
import networkx as nx
import random
from skimage.draw import disk


def load_grid(csv_path):
    return pd.read_csv(csv_path, header=None).values

# Fonction flood fill itératif
def flood_fill_iteratif(grille, x, y, marqueur, marqueurs):
    pile = [(x, y)]
    points = []
    while pile:
        cx, cy = pile.pop()
        if cx < 0 or cx >= grille.shape[0] or cy < 0 or cy >= grille.shape[1]:
            continue
        if grille[cx, cy] != 0 or marqueurs[cx, cy] != 0:
            continue
        marqueurs[cx, cy] = marqueur
        points.append((cx, cy))
        pile.append((cx + 1, cy))
        pile.append((cx - 1, cy))
        pile.append((cx, cy + 1))
        pile.append((cx, cy - 1))
    return points


csv_path = 'test.csv'
grille = 1-load_grid(csv_path)


marqueurs = np.zeros_like(grille, dtype=int)
marqueur_actuel = 1
chambres = []



# Appliquer le flood fill itératif pour chaque pixel blanc non marqué
for i in range(grille.shape[0]):
    for j in range(grille.shape[1]):
        if grille[i, j] == 0 and marqueurs[i, j] == 0:
            points = flood_fill_iteratif(grille, i, j, marqueur_actuel, marqueurs)
            centre = np.mean(points, axis=0)
            chambres.append((marqueur_actuel, centre, points))
            marqueur_actuel += 1



# Visu
chambres_colorées = np.copy(grille)
for chambre_id, _, points in chambres:
    for (x, y) in points:
        chambres_colorées[x, y] = chambre_id



plt.figure(figsize=(10, 10))
plt.imshow(chambres_colorées, cmap='tab20')
plt.show()

# graphe
G = nx.Graph()

# noeuds + positions
positions = {}
for chambre_id, centre, _ in chambres:
    positions[chambre_id] = (centre[1], centre[0])
    G.add_node(chambre_id, pos=(centre[1], centre[0]))

# arêtes + proximité directe des chambres
for i in range(len(chambres)):
    id1, centre1, points1 = chambres[i]
    distances = []
    for j in range(len(chambres)):
        if i != j:
            id2, centre2, points2 = chambres[j]
            dist = distance.euclidean(centre1, centre2)
            distances.append((dist, id2))

    distances.sort()
    for _, neighbor_id in distances[:4]:  
        G.add_edge(id1, neighbor_id, weight=_)


# D/A
start_node = random.choice(list(G.nodes))
end_node = random.choice(list(G.nodes))
while end_node == start_node:
    end_node = random.choice(list(G.nodes))


shortest_path = nx.dijkstra_path(G, source=start_node, target=end_node)



plt.figure(figsize=(10, 10))
nx.draw(G, pos=positions, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray')
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos=positions, edgelist=path_edges, edge_color='red', width=2)



plt.scatter(*positions[start_node], color='green', s=100, zorder=5)
plt.scatter(*positions[end_node], color='blue', s=100, zorder=5)
plt.show()




for i in range(len(shortest_path) - 1):
    start = positions[shortest_path[i]]
    end = positions[shortest_path[i + 1]]

    x1, y1 = int(start[1]), int(start[0])
    x2, y2 = int(end[1]), int(end[0])

    rr, cc = np.linspace(x1, x2, num=1000, dtype=int), np.linspace(y1, y2, num=1000, dtype=int)
    for (x, y) in zip(rr, cc):
        rr_disk, cc_disk = disk((x, y), 2) 
        for (r, c) in zip(rr_disk, cc_disk):
            if 0 <= r < grille.shape[0] and 0 <= c < grille.shape[1]:
                grille[r, c] = 0




start_pos = positions[start_node]
end_pos = positions[end_node]
rr_start, cc_start = disk((int(start_pos[1]), int(start_pos[0])), 2)
rr_end, cc_end = disk((int(end_pos[1]), int(end_pos[0])), 2)

for r, c in zip(rr_start, cc_start):
    if 0 <= r < grille.shape[0] and 0 <= c < grille.shape[1]:
        grille[r, c] = 3 
for r, c in zip(rr_end, cc_end):
    if 0 <= r < grille.shape[0] and 0 <= c < grille.shape[1]:
        grille[r, c] = 4 



from matplotlib.colors import ListedColormap
cmap = ListedColormap(['black', 'white', 'red', 'green', 'blue', 'cyan'])


plt.figure(figsize=(10, 10))
plt.imshow(grille, cmap=cmap)
plt.show()
