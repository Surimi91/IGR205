import cv2
import numpy as np
import csv

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

# Main
i = 1  # number for image
image_path0 = 'bin/media/chat/frame0bright.png'
image_path1 = f'bin/media/chat/frame{i}bright.png'

flow = calculate_optical_flow(image_path0, image_path1)



test_x, test_y = 300, 250  # test for coordinates in the first image
corresponding_point = find_corresponding_point(test_x, test_y, flow)

if corresponding_point:
    print(f"Point ({test_x}, {test_y}) in image 0 corresponds to {corresponding_point} in image {i}")
else:
    print(f"No corresponding point")