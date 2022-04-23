from flask import Flask, request, render_template
from os import getenv

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        cities = ["Poznań", "Kraków", "Warszawa", "Toruń", "Gdańsk", "Gdynia", 
                    "Sopot", "Szczecin", "Wrocław", "Zakopane"]
          
        return render_template("index.html", cities=cities)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=getenv('PORT'))
