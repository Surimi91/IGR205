import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from skimage.color import label2rgb
from scipy.spatial import distance
import networkx as nx
import random
from skimage.draw import disk


def load_grid(csv_path):
    return pd.read_csv(csv_path, header=None).values

# Fonction flood fill itérative
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
grille = load_grid(csv_path)

grille_lissée = gaussian_filter(grille.astype(float), sigma=1)
grille=grille_lissée
grille_binaire = (grille_lissée > 0.5).astype(int)

# Initialiser les marqueurs
marqueurs = np.zeros_like(grille_binaire, dtype=int)
marqueur_actuel = 1
chambres = []

# flood fill itératif pour chaque pixel blanc non marqué
for i in range(grille_binaire.shape[0]):
    for j in range(grille_binaire.shape[1]):
        if grille_binaire[i, j] == 0 and marqueurs[i, j] == 0:
            points = flood_fill_iteratif(grille_binaire, i, j, marqueur_actuel, marqueurs)
            centre = np.mean(points, axis=0)
            chambres.append((marqueur_actuel, centre, points))
            marqueur_actuel += 1





chambres_colorees = np.copy(grille_binaire)
for chambre_id, _, points in chambres:
    for (x, y) in points:
        chambres_colorees[x, y] = chambre_id


'''
plt.figure(figsize=(10, 10))
plt.imshow(chambres_colorées, cmap='tab20')
plt.title('Grille avec les chambres détectées')
plt.show()
'''



G = nx.Graph()

#noeuds du graph
positions = {}
for chambre_id, centre, _ in chambres:
    positions[chambre_id] = (centre[1], centre[0])
    G.add_node(chambre_id, pos=(centre[1], centre[0]))

# Ajouter les arêtes + proximité directe des chambres
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




#D/A
max_dist = 0
start_node, end_node = None, None
for i in range(len(chambres)):
    for j in range(i + 1, len(chambres)):
        dist = distance.euclidean(chambres[i][1], chambres[j][1])
        if dist > max_dist:
            max_dist = dist
            start_node = chambres[i][0]
            end_node = chambres[j][0]



shortest_path = nx.dijkstra_path(G, source=start_node, target=end_node)




'''
plt.figure(figsize=(6, 6))
nx.draw(G, pos=positions, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray')
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos=positions, edgelist=path_edges, edge_color='red', width=2)


plt.scatter(*positions[start_node], color='green', s=100, zorder=5)
plt.scatter(*positions[end_node], color='blue', s=100, zorder=5)

plt.show() '''



# Superposer le path
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




# Marquer D/A
start_pos = positions[start_node]
end_pos = positions[end_node]
rr_start, cc_start = disk((int(start_pos[1]), int(start_pos[0])), 2)
rr_end, cc_end = disk((int(end_pos[1]), int(end_pos[0])), 2)



# final maze display
plt.figure(figsize=(6, 6))
grille=1-(grille > 0.5).astype(int) #inversion pour les couleurs
plt.imshow(grille, cmap='gray')
plt.show()
