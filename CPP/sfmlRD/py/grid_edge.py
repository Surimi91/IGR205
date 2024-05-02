import numpy as np
import pandas as pd
from PIL import Image
import cv2  # Import OpenCV

r1=0.396
r2=0.588

rows, columns = 512, 512  # doit etre comme le cpp

def image_to_grayscale(image_path):
    img = Image.open(image_path).convert('L')  # Nuance de gris
    img_array = np.array(img)
    normalized_img_array = img_array / 255.0  # Normalisation pour 0 et 1
    return normalized_img_array

def save_to_csv(grid, file_path):
    df = pd.DataFrame(grid)
    df.to_csv(file_path, header=False, index=False)

def remap_values(grayscale_array, r1, r2):
    return r1 + (r2 - r1) * grayscale_array

def apply_canny_edge_detection(grayscale_array, low_threshold, high_threshold):
    edges = cv2.Canny((grayscale_array * 255).astype('uint8'), low_threshold, high_threshold)
    return edges

image_path = 'bin/media/image512.png'
csv_output_path = 'bin/data/grid.csv'
edges_output_path = 'bin/data/grid.csv'

grayscale_data = image_to_grayscale(image_path)
remapped_data = remap_values(grayscale_data, r1, r2)
save_to_csv(remapped_data, csv_output_path)

edges = apply_canny_edge_detection(grayscale_data, 350, 500) 
save_to_csv(edges, edges_output_path)
