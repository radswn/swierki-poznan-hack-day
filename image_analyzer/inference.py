import sys

sys.path.append(".")

import cv2 as cv
import numpy as np
from image_analyzer.satellite import Satellite, CoordinateManager
from here.here_api import HereApi
from image_analyzer.statistics import normalized_green_level


def baseline_inference(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower_green = np.array([36, 25, 25])
    upper_green = np.array([70, 255, 100])

    mask = cv.inRange(hsv, lower_green, upper_green)

    res = cv.bitwise_and(img, img, mask=mask)

    res = res[:, :, 1]
    kernel = np.ones((8, 8), np.uint8)
    res = cv.morphologyEx(res, cv.MORPH_OPEN, kernel)

    return res


class Inference:
    def __init__(self, satellite: Satellite, inference_function=baseline_inference,
                 statistic_function=normalized_green_level):
        self.satellite = satellite
        self.inference_function = inference_function
        self.statistic_function = statistic_function

    def infer_bounding_box(self, coordinates):
        heatmap = np.zeros(self.satellite.get_shape_of_heap_map(coordinates))

        for coords, img in self.satellite.iterate_over_box(coordinates, save=False):
            inferred_image = self.inference_function(img)
            statistic = self.statistic_function(inferred_image)

            curr_x, curr_y = coords

            heatmap[curr_y, curr_x] = statistic

        return heatmap


if __name__ == '__main__':
    coordinate = CoordinateManager(zoom=16)
    satellite = Satellite(coordinate_manager=coordinate, zoom=coordinate.zoom)
    inference = Inference(satellite, inference_function=baseline_inference)

    here = HereApi()
    coordinates = here.get_data("Poznan malta")[1]

    inference.infer_bounding_box(coordinates)
