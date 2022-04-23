from os import getenv

import folium
from flask import Flask, request, render_template

from ImageAnalyzer.inference import baseline_inference, Inference
from ImageAnalyzer.satellite import Satelite, CoordinateManager
from here.hereApi import HereApi

app = Flask(__name__)

heatmap = []
user_search = ""
location = ""
coordinate = CoordinateManager(zoom=16)
satelite = Satelite(coordinate_manager=coordinate, zoom=coordinate.zoom)


@app.route("/", methods=["POST", "GET"])
def home():
    cities = ["Poznań", "Kraków", "Warszawa", "Toruń", "Gdańsk", "Gdynia",
              "Sopot", "Szczecin", "Wrocław", "Zakopane"]

    return render_template("index.html", cities=cities)


@app.route('/search/<x>/<y>', methods=['GET'])
def search_map(x, y):
    x, y = int(x) + satelite.x_up, int(y) + satelite.y_up
    print(x, y)
    lat, lon = coordinate.x_y_to_lat_lon(x, y)
    print(lat, lon)
    m = folium.Map(
        location=[lat, lon],
        zoom_start=30,
        tiles='https://api.tiles.mapbox.com/v4/' + satelite.tilesetId +
              '/{z}/{x}/{y}.png?access_token=' + satelite.accessToken,
        attr='mapbox.com')

    print("generating a map!")

    m.save('map.html')

    return render_template('plots.html', search=user_search, location=location, z=heatmap)


@app.route('/search', methods=['POST'])
def search():
    global heatmap
    global location
    global user_search
    user_search = request.form['sbar']

    here = HereApi()
    location, coords = here.getData(location=user_search)

    inference = Inference(satelite=satelite, inference_function=baseline_inference)

    heatmap = inference.infer_bounding_box(coordinates=coords)
    heatmap = [list(x) for x in heatmap]
    print(type(heatmap))
    return render_template('plots.html', search=user_search, location=location, z=heatmap)


@app.route('/contact', methods=['GET'])
def go_contact():
    key = getenv('HERE_API_KEY')
    return render_template('contact.html', klucz=key)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=getenv('PORT'))
