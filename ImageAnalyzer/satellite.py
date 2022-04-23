import numpy as np
import requests
import cv2 as cv
import io
from os import getenv

class CoordinateManager:
    """Class that is able to change coordinates from longitude, lattitude to x y and vice versa
    """
    def __init__(self, zoom=16):
        self.zoom = zoom

    def lat_lon_to_x_y(self, lat, lon):
        """Given longitute and lattitude returns x and y

        Args:
            lon (float): _description_
            lat (float): _description_

        Returns:
            tuple: x and y
        """
        num_of_tiles = 2 ** self.zoom

        lon_deg = lon  # This is in degrees already 
        lat_rad = lat * np.pi / 180

        x_tile = int(num_of_tiles * ((lon_deg + 180) / 360))
        y_tile = int(num_of_tiles * (1 - (np.log(np.tan(lat_rad) + 1/np.cos(lat_rad) ) / np.pi)) / 2)

        return x_tile, y_tile

    def x_y_to_lat_lon(self,x_tile,y_tile):
        """Function given x and y coordinates return longitute and lattitude of given place

        Args:
            x_tile (int): _description_
            y_tile (int): _description_

        Returns:
            tuple : tuple with longitude and lattitude
        """
        n = 2 ** self.zoom
        lon_deg = x_tile / n * 360.0 - 180.0
        lat_rad = np.arctan(np.sinh(np.pi * (1 - 2 * y_tile / n)))
        lat_deg = lat_rad * 180.0 / np.pi

        return lat_deg, lon_deg


class Satelite:
    def __init__(self, coordinate_manager: CoordinateManager, tilesetId='mapbox.satellite', zoom=16):
        """Initialize Satelite which can yielf you satelite images

        Args:
            accessToken (str): AccesToken to mapboxAPI
            tilesetId (string): dataset taken from the mapboxAPI. Default to mapbox.satellite
            zoom (int, optional): ZOMM ON SATELITE IMAGE. MUST BE BETWEEN 1 and 18. THE BIGGER VALUE THE CLOSER THE IMAGEIS. Defaults to 16.
        """
        self.accessToken = getenv('SATELITE_API_KEY')
        self.coordinate_manager = coordinate_manager
        self.tilesetId = tilesetId
        self.zoom = zoom

    def get_img(self, x_tile, y_tile, save=False, img_name="img.jpg"):
        """THis image does not take longitute and lattitude. Instead it take X and Y coordinates of the image
        These can be calculated using different function

        Args:
            x_tile (int): X cooridnate of the image
            y_tile (int): Y coordinate of the image
        """
        #This image is just a request object it must be converted to the image it is done below
        img = requests.get(f'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{self.zoom}/{x_tile}/{y_tile}?access_token={self.accessToken}')

        img_stream = io.BytesIO(img.content)
        img = cv.imdecode(np.frombuffer(img_stream.read(), np.uint8), 1)

        if save:
            cv.imwrite(img_name, img)

        return img

    def get_shape_of_heap_map(self,coordinates):
        lon_up, lat_up, lon_down, lat_down = coordinates
        x_up, y_up = self.coordinate_manager.lat_lon_to_x_y(lat_up, lon_up)
        x_down, y_down = self.coordinate_manager.lat_lon_to_x_y(lat_down, lon_down)

        return abs(y_up - y_down), abs(x_up - x_down)

    def iterate_over_box(self, coordinates, save=False):
        """Generator that iterates over boundaries of given terrain and returns images.
        Starting from bottom left corner (this is beneficial for the histogram creation)

        Args:
            coordinates [tuple]. tuple in format (west, north, east, south)
        Yields:
            _type_: _description_
        """
        lon_up, lat_up, lon_down, lat_down = coordinates
        self.x_up, self.y_up = self.coordinate_manager.lat_lon_to_x_y(lat_up, lon_up)
        x_down, y_down = self.coordinate_manager.lat_lon_to_x_y(lat_down, lon_down)
        #print(x_up,y_up,x_down,y_down)

        curr_x, curr_y = self.x_up, y_down
        while curr_y > self.y_up:
            while curr_x  < x_down:
                #print(curr_x, x_down)
                img = self.get_img(curr_x, curr_y)
                if save:
                    cv.imwrite(f"{curr_x}_{curr_y}.jpg", img)

                yield (abs(curr_x - self.x_up), abs(curr_y - self.y_up) -1 ), img

                curr_x += 1
            
            curr_x = self.x_up
            #print("New curr x:" + curr_x)
            curr_y -= 1
        

if __name__ == "__main__":
    coordinate = CoordinateManager(zoom=16)
    satelite = Satelite(coordinate_manager= coordinate, zoom=coordinate.zoom)
    

    lattitude, longitude = 52.422846950454876, 16.9350192582299

    x, y = coordinate.lat_lon_to_x_y(lattitude, longitude)

    #print(x,y)

    satelite.get_img(x,y, save=True)

    lattitude_, longitude_ = coordinate.x_y_to_lat_lon(x,y)

    #print(lattitude_, longitude_)
    
    lattitude_up, longitude_up = 52.46434148470483, 16.889537555799283
    lattitude_down, longitude_down = 52.444256476893926, 16.927560551057564

    for im in satelite.iterate_over_box(coordinates = (longitude_up, lattitude_up, longitude_down, lattitude_down), save=True):
        pass
        break # mozecie przeiterowac sie po wiekszej ilosci

