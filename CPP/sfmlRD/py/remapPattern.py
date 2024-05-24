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

def calculate_optical_flow_mean(image_path0, image_path1, patch_size=15):
    img0 = load_image_grayscale(image_path0)
    img1 = load_image_grayscale(image_path1)

    # flux optique dense entre les deux images
    flow = cv2.calcOpticalFlowFarneback(img0, img1, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    height, width = flow.shape[:2]
    mean_flow_height = (height + patch_size - 1) // patch_size
    mean_flow_width = (width + patch_size - 1) // patch_size
    mean_flow = np.zeros((mean_flow_height, mean_flow_width, 2), np.float32)

    for y in range(0, height, patch_size):
        for x in range(0, width, patch_size):
            patch_flow = flow[y:y+patch_size, x:x+patch_size]
            mean_dx = np.mean(patch_flow[..., 0])
            mean_dy = np.mean(patch_flow[..., 1])
            mean_flow[y // patch_size, x // patch_size] = (mean_dx, mean_dy)

    return mean_flow, patch_size

def remap_grid(grid, mean_flow, patch_size):
    height, width = grid.shape
    remapped_grid = np.zeros_like(grid)
    for y in range(height):
        for x in range(width):
            if grid[y, x] == 1:  # Only move black pixels
                zone_y = min(y // patch_size, mean_flow.shape[0] - 1)
                zone_x = min(x // patch_size, mean_flow.shape[1] - 1)
                flow_x, flow_y = mean_flow[zone_y, zone_x]
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

    mean_flow, patch_size = calculate_optical_flow_mean(image_path0, image_path)
    remapped_grid = remap_grid(grid, mean_flow, patch_size)
    remapped_grid = invert_colors(remapped_grid)

    save_to_png(remapped_grid, f'outputRemap/{i}.png')

    print(f'Remapped grid saved to outputRemap/{i}.png')

if __name__ == "__main__":
    for i in range(8):
        main(i)

    images_to_gif('outputRemap', 'outputRemap/animated.gif')
