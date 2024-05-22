import cv2
import numpy as np
import csv
import gif

def load_image_grayscale(image_path):
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

def save_to_csv(matrix, output_csv_path):
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(matrix)

def load_from_csv(input_csv_path):
    with open(input_csv_path, mode='r') as file:
        reader = csv.reader(file)
        matrix = [list(map(int, row)) for row in reader]
    return np.array(matrix)

def calculate_optical_flow(image_path0, image_path1):
    img0 = load_image_grayscale(image_path0)
    img1 = load_image_grayscale(image_path1)

    flow = cv2.calcOpticalFlowFarneback(img0, img1, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    return flow

def find_corresponding_point(x, y, flow):
    flow_x, flow_y = flow[y, x]
    corresponding_point = (int(x + flow_x), int(y + flow_y))
    return corresponding_point

def remap_grid(grid, flow):
    height, width = grid.shape
    remapped_grid = np.zeros_like(grid)
    for y in range(height):
        for x in range(width):
            new_x, new_y = find_corresponding_point(x, y, flow)
            if 0 <= new_x < width and 0 <= new_y < height:
                remapped_grid[new_y, new_x] = grid[y, x]
    return remapped_grid

def display_grids(remapped_grid):
    # convert to uint8
    if remapped_grid.dtype != np.uint8:
        remapped_grid = cv2.normalize(remapped_grid, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    cv2.imshow('Remapped Grid', remapped_grid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_to_png(image, output_png_path):
    if image.dtype != np.uint8:
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite(output_png_path, image)


# main

def main(i):
    image_path0 = 'bin/media/chat/frame0bright.png'
    image_path = f'bin/media/chat/frame{i}bright.png'

    grid = load_from_csv('bin/data/output.csv')


    flow = calculate_optical_flow(image_path0, image_path)
    remapped_grid = remap_grid(grid, flow)

    save_to_png(remapped_grid, f'outputRemap/{i}.png')

    print(f"Remapped grid saved to outputRemap/{i}.png")




if __name__ == "__main__":
    for i in range(8):
        main(i)

    gif.images_to_gif('outputRemap', 'outputRemap/animated.gif')