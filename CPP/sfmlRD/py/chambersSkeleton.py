import matplotlib.pyplot as plt
import pandas as pd
from skimage.filters import threshold_otsu, gaussian
from skimage.morphology import skeletonize, binary_dilation, binary_erosion
from skimage.measure import label, regionprops
from skimage.color import label2rgb

def CSVtoGrid(path):
    grid = pd.read_csv(path, header=None)
    return grid.values

def smooth_image(image, sigma=1):
    return gaussian(image, sigma=sigma)

def binarize_and_skeletonize(image):
    image = smooth_image(image, sigma=1)
    
    # threshold to remove noise
    thresh = threshold_otsu(image)
    binary_image = image > thresh
    
    # create the skeleton
    skeletonized_image = skeletonize(binary_image)
    skeletonized_image = refine_skeleton(skeletonized_image)
    
    return binary_image, skeletonized_image



#build skeleton
def refine_skeleton(skeleton):
    skeleton = binary_dilation(skeleton)
    skeleton = binary_erosion(skeleton)
    return skeleton


#chamber detection
def detect_and_colorize_chambers(binary_image):
    labeled_image = label(binary_image)
    regions = regionprops(labeled_image)
    chamber_info = []
    
    for region in regions:
        chamber_info.append({
            'label': region.label,
            'area': region.area,
            'bbox': region.bbox
        })
    
    colorized_image = label2rgb(labeled_image, bg_label=0)
    return colorized_image, chamber_info

# main
path = 'bin/data/output.csv'
image = CSVtoGrid(path)
binary_image, skeletonized_image = binarize_and_skeletonize(image)

# Detect and colorize chambers
colorized_image, chamber_info = detect_and_colorize_chambers(binary_image)


fig, axs = plt.subplots(1, 2, figsize=(12, 6))

axs[0].imshow(skeletonized_image, cmap='gray')
axs[0].set_title('Skeletonized Image')
axs[0].axis('off')

axs[1].imshow(colorized_image)
axs[1].set_title('Chambers in Labyrinth')
axs[1].axis('off')

plt.tight_layout()
plt.show()


for chamber in chamber_info:
    print(f"Chamber {chamber['label']}: Area={chamber['area']}, Bounding Box={chamber['bbox']}")
