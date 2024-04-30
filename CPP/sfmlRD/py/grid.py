import numpy as np
import pandas as pd
from PIL import Image


def image_to_grayscale(image_path):
    img = Image.open(image_path).convert('L')  #nuance de grid
    img_array = np.array(img)
    normalized_img_array = img_array / 255.0  #normalisation pour 0 et 1
    return normalized_img_array


def generate_random_grid(rows, columns, white_chance=0.05):
    # grille random
    grid = np.random.choice([0, 1], size=(rows, columns), p=[1-white_chance, white_chance])
    return grid

def save_to_csv(grid, file_path):
    df = pd.DataFrame(grid)
    df.to_csv(file_path, header=False, index=False)

rows, columns = 200, 200  # doit etre comme le cpp

image_path = 'bin/media/image200.png'
csv_output_path = 'bin/data/grid.csv'



grayscale_data = image_to_grayscale(image_path)
save_to_csv(grayscale_data, csv_output_path)
