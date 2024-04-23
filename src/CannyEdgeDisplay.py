import cv2
import numpy as np
import fill_outside

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

    binary_grid=fill_outside.fill(binary_grid)

    cv2.imshow('Binary Grid', binary_grid * 255)  # par 255 pour affichage
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return binary_grid


image_path = 'media/image.png'
binary_grid = canny_edge_to_binary_grid(image_path)

print(binary_grid)