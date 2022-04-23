from os import getenv
from here.hereApi import HereApi
from ImageAnalyzer.satellite import Satelite, CoordinateManager
from ImageAnalyzer.inference import baseline_inference, Inference
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

heatmap = []
user_search = ""
location = ""

@app.route("/", methods=["POST", "GET"])
def home():
    cities = ["Poznań", "Kraków", "Warszawa", "Toruń", "Gdańsk", "Gdynia", 
                "Sopot", "Szczecin", "Wrocław", "Zakopane"]
        
    return render_template("index.html", cities=cities)


@app.route('/search/<x>/<y>', methods=['GET'])
def search_map(x, y):
    print("asdasd")
    print(heatmap)
    return render_template('plots.html', search=user_search, location=location, z=heatmap)


@app.route('/search', methods=['POST'])
def search():
    global heatmap
    global location
    global user_search
    user_search = request.form['sbar']  
    
    here = HereApi()
    location, coords = here.getData(location=user_search)

    coordinate = CoordinateManager(zoom=16)
    satelite = Satelite(coordinate_manager=coordinate, zoom=coordinate.zoom)
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
