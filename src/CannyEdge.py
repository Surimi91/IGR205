import cv2
import numpy as np

def canny_edge_to_binary_grid(image_path):

    image = cv2.imread(image_path)
    if image is None:
        print("L'image n'a pas pu être chargée")
        return
    
    # niveaux de gris
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # edge detection
    canny_edges = cv2.Canny(gray_image, 350, 500)

    binary_grid = (canny_edges == 0).astype(np.uint8)


    return binary_grid