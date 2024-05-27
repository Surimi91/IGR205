import cv2

image1 = cv2.imread('f0.png', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('f1.png', cv2.IMREAD_GRAYSCALE)


features_to_track = cv2.goodFeaturesToTrack(image1, maxCorners=100, qualityLevel=0.01, minDistance=10)


points2, st, err = cv2.calcOpticalFlowPyrLK(image1, image2, features_to_track, None)


movement_vectors = points2 - features_to_track


for i, (new, old) in enumerate(zip(points2, features_to_track)):
    a, b = new.ravel()
    c, d = old.ravel()
    print(f"Point {i}: Old position: ({c}, {d}), New position: ({a}, {b})")