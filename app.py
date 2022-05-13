from os import getenv

import folium
from flask import Flask, request, render_template

from image_analyzer.inference import baseline_inference, Inference
from image_analyzer.satellite import Satellite, CoordinateManager
from here.here_api import HereApi
import webbrowser

app = Flask(__name__)

heatmap = []
user_search = ""
location = ""
coordinate = CoordinateManager(zoom=16)
satellite = Satellite(coordinate_manager=coordinate, zoom=coordinate.zoom)


@app.route("/", methods=["POST", "GET"])
def home():
    cities = ["Poznań", "Kraków", "Warszawa", "Toruń", "Gdańsk", "Gdynia",
              "Sopot", "Szczecin", "Wrocław", "Zakopane"]

    return render_template("index.html", cities=cities)


@app.route('/search/<x>/<y>', methods=['GET'])
def search_map(x, y):
    x, y = int(x) + satellite.x_up, int(y) + satellite.y_up
    print(x, y)
    lat, lon = coordinate.x_y_to_lat_lon(x+1, y+1)
    print(lat, lon)
    m = folium.Map(
        location=[lat, lon],
        zoom_start=30,
        tiles='https://api.tiles.mapbox.com/v4/' + satellite.tile_set_id +
              '/{z}/{x}/{y}.png?access_token=' + satellite.accessToken,
        attr='mapbox.com')

    print("generating a map!")

    m.save('map.html')
    webbrowser.open("map.html")

    return render_template('plots.html', search=user_search, location=location, z=heatmap)


@app.route('/search', methods=['POST'])
def search():
    global heatmap
    global location
    global user_search
    user_search = request.form['sbar']

    here = HereApi()
    location, coords = here.get_data(location=user_search)

    inference = Inference(satellite=satellite, inference_function=baseline_inference)

    heatmap = inference.infer_bounding_box(coordinates=coords)
    heatmap = [list(x) for x in heatmap]
    print(type(heatmap))
    return render_template('plots.html', search=user_search, location=location, z=heatmap)


@app.route('/contact', methods=['GET'])
def go_contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=getenv('PORT'))
