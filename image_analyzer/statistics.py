import cv2 as cv
import numpy as np


def normalized_green_level(img: np.ndarray, normalization_factor=1):
    if len(img.shape) != 2:
        print("PROVIDE GRAYSCALE IMAGE")

    binarized_img = img > 40
    cv.imwrite("binarized.jpg", binarized_img * 255)
    area = binarized_img.shape[0] * binarized_img.shape[1]

    return np.sum(binarized_img) / (area * normalization_factor)


if __name__ == "__main__":
    img_to_inference = cv.imread("0.jpg")
    print(type(img_to_inference))
    print(normalized_green_level(img_to_inference))
