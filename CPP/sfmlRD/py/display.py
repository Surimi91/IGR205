import matplotlib.pyplot as plt
import pandas as pd
from skimage.filters import threshold_otsu, gaussian
from skimage.morphology import skeletonize, binary_dilation, binary_erosion


def CSVtoGrid(path):
    grid = pd.read_csv(path, header=None)
    return grid.values

def smooth_image(image, sigma=1):
    return gaussian(image, sigma=sigma)

def binarize_and_skeletonize(image):
    # smoothing pour avoir de belles lignes
    image = smooth_image(image, sigma=1)
    
    # treshold pour éliminer le bruit
    thresh = threshold_otsu(image)
    binary_image = image > thresh
    
    # creation du skeleton
    skeletonized_image = skeletonize(binary_image)
    skeletonized_image = refine_skeleton(skeletonized_image)
    
    return binary_image, skeletonized_image

def refine_skeleton(skeleton):
    skeleton = binary_dilation(skeleton)
    skeleton = binary_erosion(skeleton)
    return skeleton


# main
path = 'bin/data/output.csv'
image = CSVtoGrid(path)
binary_image, skeletonized_image = binarize_and_skeletonize(image)



# affichage
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(image, cmap='gray')
axes[0].set_title('RD')
axes[0].axis('off')

axes[1].imshow(binary_image, cmap='gray')
axes[1].set_title('Binary')
axes[1].axis('off')

axes[2].imshow(skeletonized_image, cmap='gray')
axes[2].set_title('Skeletonized')
axes[2].axis('off')

plt.tight_layout()
plt.show()