import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv

def canny_edge_detection(image_path, low_threshold, high_threshold):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred_image = cv2.GaussianBlur(image, (5, 5), 1.4)
    
    edges = cv2.Canny(blurred_image, low_threshold, high_threshold, apertureSize=3, L2gradient=True)
    
    # contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = np.zeros_like(image)
    cv2.drawContours(contour_image, contours, -1, (255), 1) 
    edge_matrix = contour_image.tolist()
    
    return edge_matrix

def save_to_csv(edge_matrix, output_csv_path):
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(edge_matrix)

def load_from_csv(input_csv_path):
    with open(input_csv_path, mode='r') as file:
        reader = csv.reader(file)
        edge_matrix = [list(map(int, row)) for row in reader]
    return np.array(edge_matrix)


# main
image_path0 = 'bin/media/chat/frame0bright.png'
image_path1 = 'bin/media/chat/frame1bright.png'
low_threshold = 50
high_threshold = 150

edge_matrix1 = canny_edge_detection(image_path0, low_threshold, high_threshold)
edge_matrix2 = canny_edge_detection(image_path1, low_threshold, high_threshold)

save_to_csv(edge_matrix1, 'edges_frame0.csv')
save_to_csv(edge_matrix2, 'edges_frame1.csv')

edge1 = load_from_csv('edges_frame0.csv')
edge2 = load_from_csv('edges_frame1.csv')



def select_key_points(edge_matrix):
    points = [] #on garde la bordure
    for i in range(len(edge_matrix)):
        for j in range(len(edge_matrix[0])):
            if edge_matrix[i][j] == 255:
                points.append((j, i))
    return points

def match_points(points1, points2):
    # placeholder function. May need to find a more complex algorithm
    return list(zip(points1, points2))  # assume the points are in order and directly matchable

def compute_homography(matches):
    # Convert pairs to the format expected by cv2.findHomography
    src_pts = np.float32([m[0] for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([m[1] for m in matches]).reshape(-1, 1, 2)
    
    # Calcul de l'homographie
    homography_matrix, status = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    return homography_matrix



# main
key_points1 = select_key_points(edge_matrix1)
key_points2 = select_key_points(edge_matrix2)

matches = match_points(key_points1, key_points2)
homography_matrix = compute_homography(matches)

print(homography_matrix)