import cv2
import numpy as np
import csv
import os
from PIL import Image
import matplotlib.pyplot as plt

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

def find_bounding_quadrilateral(image):
    non_zero_points = cv2.findNonZero(image)
    rect = cv2.minAreaRect(non_zero_points)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    return box

def draw_contour(image, contour):
    contour_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contour_image, [contour], -1, (0, 255, 0), 3)
    return contour_image

def estimate_rotation_translation(box0, box1):
    transform_matrix, inliers = cv2.estimateAffinePartial2D(box0, box1, method=cv2.RANSAC)
    return transform_matrix

def apply_transformation_to_grid(grid, transform_matrix):
    height, width = grid.shape
    remapped_grid = np.zeros_like(grid)
    
    for y in range(height):
        for x in range(width):
            if grid[y, x] == 1:  # Only move black pixels
                new_pos = np.dot(transform_matrix[:, :2], np.array([x, y])) + transform_matrix[:, 2]
                new_x, new_y = int(new_pos[0]), int(new_pos[1])
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

def display_image_with_contour(image_path, contour):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contour_image = draw_contour(gray_image, contour)
    plt.figure(figsize=(8, 8))
    plt.imshow(cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB))
    plt.title('Detected Border')
    plt.show()

# main

def main(i):
    image_path0 = 'bin/media/carre/f0.png'
    image_path = f'bin/media/carre/f{i}.png'

    img0 = load_image_grayscale(image_path0)
    img1 = load_image_grayscale(image_path)

    grid = load_from_csv('bin/data/output.csv')

    box0 = find_bounding_quadrilateral(img0)
    box1 = find_bounding_quadrilateral(img1)

    if box0 is None or box1 is None:
        print("Error: Could not find a quadrilateral in one of the images.")
        return

    # Display contours for debugging
    #display_image_with_contour(image_path0, box0)
    #display_image_with_contour(image_path, box1)

    transform_matrix = estimate_rotation_translation(box0, box1)
    remapped_grid = apply_transformation_to_grid(grid, transform_matrix)
    remapped_grid = invert_colors(remapped_grid)

    save_to_png(remapped_grid, f'outputRemap/{i}.png')

    print(f'Remapped grid saved to outputRemap/{i}.png')

if __name__ == "__main__":
    for i in range(8):
        main(i)

    images_to_gif('outputRemap', 'outputRemap/animated.gif')
