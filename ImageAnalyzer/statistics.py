import numpy as np
import cv2 as cv

def normalized_green_level(img: np.ndarray, normalization_factor=1):
    """Function calculating level of vegetation level in range of [0,1]
    with the equation 

    veg_level = np.sum(img) / area*normalization_factor 

    Args:
        img (np.ndarray): array with grayscale image to inference
        normalization factor (float, optional): . Defaults to 0.5.
    """

    if len(img.shape) != 2:
        print("PROVIDE GRAYSCALE IMAGE")

    binarized_img = img > 40
    cv.imwrite("binarized.jpg", binarized_img * 255)
    area = binarized_img.shape[0] * binarized_img.shape[1]

    #print(np.sum(binarized_img))
    #print(area)
    return np.sum(binarized_img) / (area*normalization_factor)


if __name__ == "__main__":
    img_to_inference = cv.imread("0.jpg")
    print(type(img_to_inference))
    print(normalized_green_level(img_to_inference))