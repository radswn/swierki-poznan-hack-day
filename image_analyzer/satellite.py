import io
from os import getenv

import cv2 as cv
import numpy as np
import requests


class CoordinateManager:
    def __init__(self, zoom=16):
        self.zoom = zoom

    def lat_lon_to_x_y(self, lat, lon):
        num_of_tiles = 2 ** self.zoom

        lon_deg = lon
        lat_rad = lat * np.pi / 180

        x_tile = int(num_of_tiles * ((lon_deg + 180) / 360))
        y_tile = int(num_of_tiles * (1 - (np.log(np.tan(lat_rad) + 1 / np.cos(lat_rad)) / np.pi)) / 2)

        return x_tile, y_tile

    def x_y_to_lat_lon(self, x_tile, y_tile):
        n = 2 ** self.zoom
        lon_deg = x_tile / n * 360.0 - 180.0
        lat_rad = np.arctan(np.sinh(np.pi * (1 - 2 * y_tile / n)))
        lat_deg = lat_rad * 180.0 / np.pi

        return lat_deg, lon_deg


class Satellite:
    def __init__(self, coordinate_manager: CoordinateManager, tile_set_id='mapbox.satellite', zoom=16):
        self.x_up = None
        self.y_up = None
        self.accessToken = getenv('SATELLITE_API_KEY')
        self.coordinate_manager = coordinate_manager
        self.tile_set_id = tile_set_id
        self.zoom = zoom

    def get_img(self, x_tile, y_tile, save=False, img_name="img.jpg"):
        img = requests.get(
            f'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{self.zoom}/{x_tile}/{y_tile}?access_token={self.accessToken}')

        img_stream = io.BytesIO(img.content)
        img = cv.imdecode(np.frombuffer(img_stream.read(), np.uint8), 1)

        if save:
            cv.imwrite(img_name, img)

        return img

    def get_shape_of_heap_map(self, coordinates):
        lon_up, lat_up, lon_down, lat_down = coordinates
        x_up, y_up = self.coordinate_manager.lat_lon_to_x_y(lat_up, lon_up)
        x_down, y_down = self.coordinate_manager.lat_lon_to_x_y(lat_down, lon_down)

        return abs(y_up - y_down), abs(x_up - x_down)

    def iterate_over_box(self, coordinates, save=False):
        lon_up, lat_up, lon_down, lat_down = coordinates
        self.x_up, self.y_up = self.coordinate_manager.lat_lon_to_x_y(lat_up, lon_up)
        x_down, y_down = self.coordinate_manager.lat_lon_to_x_y(lat_down, lon_down)

        curr_x, curr_y = self.x_up, y_down
        while curr_y > self.y_up:
            while curr_x < x_down:
                img = self.get_img(curr_x, curr_y)
                if save:
                    cv.imwrite(f"{curr_x}_{curr_y}.jpg", img)

                yield (abs(curr_x - self.x_up), abs(curr_y - self.y_up) - 1), img

                curr_x += 1

            curr_x = self.x_up
            curr_y -= 1


if __name__ == "__main__":
    coordinate = CoordinateManager(zoom=16)
    satellite = Satellite(coordinate_manager=coordinate, zoom=coordinate.zoom)

    latitude, longitude = 52.422846950454876, 16.9350192582299

    x, y = coordinate.lat_lon_to_x_y(latitude, longitude)

    satellite.get_img(x, y, save=True)

    latitude_, longitude_ = coordinate.x_y_to_lat_lon(x, y)

    latitude_up, longitude_up = 52.46434148470483, 16.889537555799283
    latitude_down, longitude_down = 52.444256476893926, 16.927560551057564

    for im in satellite.iterate_over_box(coordinates=(longitude_up, latitude_up, longitude_down, latitude_down),
                                         save=True):
        pass
        break
