from os import getenv

from flask import Flask, request, render_template, redirect

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        cities = ["Poznań", "Kraków", "Warszawa", "Toruń", "Gdańsk", "Gdynia", 
                    "Sopot", "Szczecin", "Wrocław", "Zakopane"]
          
        return render_template("index.html", cities=cities)


@app.route('/search', methods=['POST'])
def search():
    user_search = request.form['sbar']  
       
    return render_template('plots.html', search=user_search)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=getenv('PORT'))
