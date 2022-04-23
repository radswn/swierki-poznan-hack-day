from typing import Tuple
import requests
from os import getenv


class HereApi:
    def __init__(self) -> None:
        self.apiKey = getenv("HERE_API_KEY")
        self.URL = 'https://geocode.search.hereapi.com/v1/geocode'
        self.directions = ['west', 'north', 'east', 'south']
    
    def getData(self, location) -> Tuple:
        PARAMS = {'q': location, 'apiKey': self.apiKey}
        r = requests.get(url=self.URL, params=PARAMS)
        data = r.json()
    
        center_latitude = data['items'][0]['position']['lat']
        center_longitude = data['items'][0]['position']['lng']
        corners = tuple([data['items'][0]['mapView'][x] for x in self.directions])
        
        location_name = data['items'][0]['title']
        if 'mapView' in data['items'][0].keys():
            corners = tuple([data['items'][0]['mapView'][x] for x in self.directions])
        else:
            corners = tuple([center_longitude-0.01, center_latitude+0.01,
                            center_longitude+0.01, center_latitude-0.01])

        return location_name, corners


if __name__ == '__main__':
    here = hereApi()
    print(here.getData("Poznan, Piatkowo"))

