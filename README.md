# SIA-EARTH

## Run with Python

* create virtual environment `python -m venv env`
* activate it `env/Scripts/activate.ps1`
* install dependencies `pip install -r requirements.txt`
* run the app `python app.py`

## Run with Docker

* ensure that you have docker installed
* go into the root directory
* build the image with `docker build -t sia-earth:latest .`
* create the container with `docker run -d -p 5000:5000 --name=sia-earth sia-earth`
* start/stop the running container `docker (start/stop) sia-earth`