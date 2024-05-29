import numpy as np
import pandas as pd
from PIL import Image
import cv2

r1=0.396
r2=0.588

rows, columns = 512, 512  # doit etre comme le cpp

def image_to_grayscale(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_array = np.array(img)
    normalized_img_array = (img_array / 127.5) - 1  # Normalize to range [-1, 1]
    return normalized_img_array



def save_to_csv(grid, file_path):
    df = pd.DataFrame(grid)
    df.to_csv(file_path, header=False, index=False)

def remap_values(grayscale_array, r1, r2):
    return r1 + (r2 - r1) * grayscale_array 

image_path = 'bin/media/NomDuDossier/f0.png'
csv_output_path = 'bin/data/grid.csv'



grayscale_data = image_to_grayscale(image_path)
remapped_data = 2*remap_values(grayscale_data, r1, r2)-1   #fonction 2x - 1
save_to_csv(remapped_data, csv_output_path)
#j'ai changé pour remapped