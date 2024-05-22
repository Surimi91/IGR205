from PIL import Image
import os

def images_to_gif(input_folder, output_path, duration=0.20*8):
    images = []
    for file_name in sorted(os.listdir(input_folder)):
        if file_name.endswith('.png'):
            file_path = os.path.join(input_folder, file_name)
            img = Image.open(file_path)
            images.append(img)


    images[0].save(output_path, save_all=True, append_images=images[1:], duration=duration, loop=0)
    print(f"GIF saved to {output_path}")