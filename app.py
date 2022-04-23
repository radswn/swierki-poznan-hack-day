from os import getenv

from flask import Flask, request, render_template, redirect
import folium

app = Flask(__name__)

<<<<<<< HEAD
heatmap = []
user_search = ""
location = ""
coordinate = CoordinateManager(zoom=16)
satelite = Satelite(coordinate_manager=coordinate, zoom=coordinate.zoom)
=======
>>>>>>> parent of e32759c (resolve conflicts)

@app.route("/", methods=["POST", "GET"])
def home():
    cities = ["Poznań", "Kraków", "Warszawa", "Toruń", "Gdańsk", "Gdynia", 
                "Sopot", "Szczecin", "Wrocław", "Zakopane"]
        
    return render_template("index.html", cities=cities)


<<<<<<< HEAD
@app.route('/search/<x>/<y>', methods=['GET'])
def search_map(x, y):
    x,y = int(x) + satelite.x_up, int(y) + satelite.y_up
    print(x,y)
    lat, lon = coordinate.x_y_to_lat_lon(x,y)
    print(lat,lon)
    m = folium.Map(
        location=[lat, lon],
        zoom_start=30,
        tiles='https://api.tiles.mapbox.com/v4/' + satelite.tilesetId +
        '/{z}/{x}/{y}.png?access_token=' + satelite.accessToken,
        attr='mapbox.com')
        
    print("generating a map!")

    m.save('map.html')

    return render_template('plots.html', search=user_search, location=location, z=heatmap)


=======
>>>>>>> parent of e32759c (resolve conflicts)
@app.route('/search', methods=['POST'])
def search():
    user_search = request.form['sbar']  
    
    here = HereApi()
    location, coords = here.getData(location=user_search)

    
    inference = Inference(satelite=satelite, inference_function=baseline_inference)
    
    heatmap = inference.infer_bounding_box(coordinates=coords)
    heatmap = [list(x) for x in heatmap]
    print(type(heatmap))
    return render_template('plots.html', search=user_search, location = location, z=heatmap)


@app.route('/contact', methods=['GET'])
def go_contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=getenv('PORT'))
