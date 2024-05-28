import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Segmentation des objets par couleur
def segment_color(image, lower_hsv, upper_hsv):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    return mask

# tri des imaegs
def sort_files(files):
    return sorted(files, key=lambda x: int(x.split('f')[1].split('.')[0]))

image_folder = "rond"
images = []
filenames = sort_files([f for f in os.listdir(image_folder) if f.endswith(".png")])
for filename in filenames:
    img = cv2.imread(os.path.join(image_folder, filename), cv2.IMREAD_UNCHANGED)
    if img is not None:
        images.append(img)

# seuils HSV pour les couleurs eventuellemnt à ajuster via CNN
color_ranges = {
    'rouge': ((0, 50, 50), (10, 255, 255)),
    'cyan': ((80, 50, 50), (100, 255, 255)),
}

# Détection des objets et extraction des positions
object_positions = {color: [] for color in color_ranges.keys()}


contour_colors = {
    'rouge': (0, 0, 255),
    'cyan': (255, 255, 0),
}



for i, img in enumerate(images):
    output_img = img.copy()
    bgr_img = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGRA2BGR)
    alpha_channel = img[:, :, 3]
    alpha_mask = alpha_channel > 0 #masque pour filtrer le png

    for color, (lower_hsv, upper_hsv) in color_ranges.items():
        mask = segment_color(bgr_img, lower_hsv, upper_hsv)
        mask = cv2.bitwise_and(mask, mask, mask=alpha_channel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        positions = []
        for cnt in contours:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                positions.append((cx, cy))
                cv2.circle(output_img, (cx, cy), 5, contour_colors[color], -1)
            cv2.drawContours(output_img, [cnt], -1, contour_colors[color], 2)
        object_positions[color].append(positions)
    

'''
    if i < 5:  # test premirers images
        plt.figure(figsize=(8, 8))
        plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGRA2RGBA))
        plt.title(f'Image {i} avec objets détectés')
        plt.show()    '''



# utilisation des coordonnées
colors = ['rouge', 'cyan']
for color in colors:
    all_positions = list(zip(*object_positions[color]))
    for idx, positions in enumerate(all_positions):
        x = [pos[0] for pos in positions]
        y = [pos[1] for pos in positions]
        #chaque point, pour un objet, puis chaque point pour l'autre etc...



        #plt.plot(x, y, marker='o', label=f'{color} Objet {idx}')



'''
plt.xlabel('Position X')
plt.ylabel('Position Y')
plt.title('Évolution de la position des objets')
plt.legend()
plt.show()
'''