from tensorflow.keras.preprocessing import image as Image
import numpy as np

def preprocess_img(img_path, img_size):
    img = Image.load_img(img_path, target_size=img_size)
    img_tensor = Image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    return img_tensor