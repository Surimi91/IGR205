import cv2
import numpy as np
import csv
import os
from PIL import Image

def load_image_grayscale(image_path):
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

def save_to_csv(matrix, output_csv_path):
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(matrix)

def invert_colors(image):
    return 255 - image

def load_from_csv(input_csv_path):
    with open(input_csv_path, mode='r') as file:
        reader = csv.reader(file)
        matrix = [list(map(int, row)) for row in reader]
    return np.array(matrix)

def calculate_optical_flow_lucas_kanade(image_path0, image_path1):
    img0 = load_image_grayscale(image_path0)
    img1 = load_image_grayscale(image_path1)
    
    height, width = img0.shape
    flow = np.zeros((height, width, 2), np.float32)

    # Paramètres pour le flux optique de Lucas-Kanade
    lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Détecter les points de caractéristiques dans l'image initiale
    p0 = cv2.goodFeaturesToTrack(img0, mask=None, maxCorners=10000, qualityLevel=0.01, minDistance=1, blockSize=7)

    # Calculer le flux optique
    p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)

    # Sélectionner les bons points
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    # Mettre à jour le flux avec les déplacements calculés
    for (new, old) in zip(good_new, good_old):
        a, b = new.ravel()
        c, d = old.ravel()
        flow[int(d), int(c)] = (a - c, b - d)

    return flow

def remap_grid(grid, flow):
    height, width = grid.shape
    remapped_grid = np.zeros_like(grid)
    for y in range(height):
        for x in range(width):
            if grid[y, x] == 1:  # Only move black pixels
                flow_x, flow_y = flow[y, x]
                new_x, new_y = int(x + flow_x), int(y + flow_y)
                if 0 <= new_x < width and 0 <= new_y < height:
                    remapped_grid[new_y, new_x] = grid[y, x]
    return remapped_grid

def save_to_png(image, output_png_path):
    if image.dtype != np.uint8:
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite(output_png_path, image)

def images_to_gif(input_folder, output_path, duration=300):
    images = []
    for file_name in sorted(os.listdir(input_folder)):
        if file_name.endswith('.png'):
            file_path = os.path.join(input_folder, file_name)
            img = Image.open(file_path)
            images.append(img)
    
    if images:
        images[0].save(output_path, save_all=True, append_images=images[1:], duration=duration, loop=0)
        print(f"GIF saved to {output_path}")
    else:
        print("No images found in the input folder.")

# main

def main(i):
    image_path0 = 'bin/media/carre/f0.png'
    image_path = f'bin/media/carre/f{i}.png'

    grid = load_from_csv('bin/data/output.csv')

    flow = calculate_optical_flow_lucas_kanade(image_path0, image_path)
    remapped_grid = remap_grid(grid, flow)
    remapped_grid = invert_colors(remapped_grid)

    save_to_png(remapped_grid, f'outputRemap/{i}.png')

    print(f'Remapped grid saved to outputRemap/{i}.png')

if __name__ == "__main__":
    for i in range(8):
        main(i)

    images_to_gif('outputRemap', 'outputRemap/animated.gif')
