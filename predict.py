import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import cv2
from glob import glob
from tqdm import tqdm
import tensorflow as tf
from train import create_dir
from tensorflow.keras.utils import get_custom_objects
from tensorflow.keras.optimizers import Adam

""" Global parameters """
image_h = 512
image_w = 512

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory {path} created.")
    else:
        print(f"Directory {path} already exists.")

if __name__ == "__main__":
    """ Seeding """
    np.random.seed(42)
    tf.random.set_seed(42)

    """ Directory for storing files """
    create_dir("test/masks")

    """ Loading model """
    try:
        model = tf.keras.models.load_model("files/model.h5")
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        exit(1)

    """ Load the dataset """
    data_x = glob(os.path.join("test", "images", "*"))
    if not data_x:
        print("No images found in test/images/")
        exit(1)

    for path in tqdm(data_x, total=len(data_x)):
        """ Extracting name """
        name = os.path.splitext(os.path.basename(path))[0]

        """ Reading the image """
        image = cv2.imread(path, cv2.IMREAD_COLOR)
        if image is None:
            print(f"Failed to load image {path}")
            continue
        h, w, _ = image.shape
        x = cv2.resize(image, (image_w, image_h))
        x = x / 255.0
        x = x.astype(np.float32)  ## (h, w, 3)
        x = np.expand_dims(x, axis=0)  ## (1, h, w, 3)

        """ Prediction """
        y = model.predict(x, verbose=0)[0][:, :, -1]
        y = cv2.resize(y, (w, h))
        y = np.expand_dims(y, axis=-1)

        """ Save the image """
        masked_image = image * y
        line = np.ones((h, 10, 3)) * 128
        cat_images = np.concatenate([image, line, masked_image], axis=1)

        save_path = os.path.join("test", "masks", f"{name}.png")

        # Debugging information
        print(f"Saving image at {save_path}")
        print(f"cat_images shape: {cat_images.shape}, dtype: {cat_images.dtype}")

        if cv2.imwrite(save_path, cat_images):
            print(f"Image saved successfully at {save_path}")
        else:
            print(f"Failed to save image at {save_path}")

        # Additional check
        if not os.path.exists(save_path):
            print(f"File does not exist after cv2.imwrite: {save_path}")
