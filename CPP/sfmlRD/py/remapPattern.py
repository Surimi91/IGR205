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


loaded_edge_matrix1 = load_from_csv('edges_frame0.csv')
loaded_edge_matrix2 = load_from_csv('edges_frame1.csv')

# display
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

axes[0].imshow(loaded_edge_matrix1, cmap='gray')
axes[0].set_title('Contours Frame 0')
axes[0].axis('off')

axes[1].imshow(loaded_edge_matrix2, cmap='gray')
axes[1].set_title('Contours Frame 1')
axes[1].axis('off')

plt.show()
