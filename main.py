# import "packages" from flask
from flask import render_template, request
import requests
import json

from starter import app_starter
from algorithm import app_algorithm
from webapi import app_api
from dc_crud.app_crud import app_crud
from y2022 import app_y2022
from web.websiteSearch import websiteSearch
# from create_task.foodiefinder import foodiefinder
# from api.jeanapi import api_bp
from __init__ import app

# create a Flask instance
# app = Flask(__name__)
# app.register_blueprint(api_bp)

app.register_blueprint(app_starter)
app.register_blueprint(app_algorithm)
app.register_blueprint(app_api)
app.register_blueprint(app_crud)
app.register_blueprint(app_y2022)
app.register_blueprint(websiteSearch)
# app.register_blueprint(foodiefinder)
forumList = []
# connects default URL to render index.html


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/AboutAlex/', methods=['GET', 'POST'])
def AboutAlex():
    import requests
    # Get the keyword value from POST
    keyword = request.form.get("keyword");
    url = "https://nba-player-individual-stats.p.rapidapi.com/players/firstname"
    querystring = {"firstname":keyword}
    headers = {
        'x-rapidapi-host': "nba-player-individual-stats.p.rapidapi.com",
        'x-rapidapi-key': "39c4bf8c2emsh30b02ab6dc01dd9p13f427jsn690a650cf2ec"
    }
    athleteApiResponse = requests.request("GET", url, headers=headers, params=querystring)

    return render_template("AboutAlex.html", results = athleteApiResponse.json())

@app.route('/AboutDylan/', methods=['GET', 'POST'])
def AboutDylan():
    url = "https://sportscore1.p.rapidapi.com/sports/1/teams"
    headers = {
        'x-rapidapi-host': "sportscore1.p.rapidapi.com",
        'x-rapidapi-key': "39c4bf8c2emsh30b02ab6dc01dd9p13f427jsn690a650cf2ec"
    }
    # return render_template("AboutDylan.html")

    response = requests.request("GET", url, headers=headers)
    return render_template("AboutDylan.html", stats=response.json())
def AboutDylan1():
    # submit button has been pushed
    if request.form:
        name = request.form.get("name")
        if len(name) != 0:  # input field has content
            return render_template("AboutDylan.html", nickname=name)
    # starting and empty input default
    return render_template("AboutDylan.html", nickname="World")


@app.route('/AboutIsabelle/', methods=['GET', 'POST'])
def AboutIsabelle():
    url = "https://iata-and-icao-codes.p.rapidapi.com/airlines"

    headers = {
        'x-rapidapi-host': "iata-and-icao-codes.p.rapidapi.com",
        'x-rapidapi-key': "1d7d18e024msh1c32fb3c6271277p1b2d7djsnd1cb3334d831"
    }
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    print(response.text)
    return render_template("AboutIsabelle.html", output=response.json())


@app.route('/AboutJean/', methods=['GET', 'POST'])
def AboutJean():
    url = "https://world-time2.p.rapidapi.com/timezone/Europe/London"
    headers = {
            'x-rapidapi-host': "world-time2.p.rapidapi.com",
            'x-rapidapi-key': "0a00932a78msh5f89ea8b8f5d589p124611jsn64789e16513c"
            }
    response = requests.request("GET", url, headers=headers)
    # return(response.json())
    data = json.loads(response.text)
    return render_template("AboutJean.html", output=response.json())


@app.route('/HotelSearch/')
def HotelSearch():
    return render_template("HotelSearch.html")


@app.route('/FunTimes/')
def FunTimes():
    return render_template("FunTimes.html")


@app.route('/currency_exchange/', methods=['GET', 'POST'])
def currency_exchange():
    return render_template("currency_exchange.html")


@app.route('/fact', methods=['GET', 'POST'])
def fact():
    url = "http://localhost:5000/api/fact"
    response = requests.request("GET", url)
    return render_template("fact.html", fact=response.json())


@app.route('/facts/', methods=['GET', 'POST'])
def facts():
    url = "http://localhost:5000/api/facts"
    response = requests.request("GET", url)
    return render_template("facts.html", facts=response.json())


@app.route('/forum/', methods=['GET', 'POST'])
def forum():
    # submit button has been pushed
    if request.form:
        name = request.form.get("name")
        forumList.append(name)
        if len(name) != 0:  # input field has content
            return render_template("forum.html", greetforum=forumList)
    # starting and empty input default
    return render_template("forum.html", greetforum="Hello World")


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if len(forumList) > 0:
        forumList.pop(len(forumList) - 1)
    return render_template("forum.html", nickname=forumList)


@app.route('/RestaurantSearch/')
def RestaurantSearch():
    return render_template("RestaurantSearch.html")


@app.route('/CarSearch/')
def CarSearch():
    return render_template("CarSearch.html")


@app.route('/Calculator/')
def Calculator():
    return render_template("Calculator.html")


@app.route('/FlightInformation/')
def FlightInformation():
    return render_template("FlightInformation.html")

@app.route('/travelcard/')
def travelcard():
    return render_template("travelcard.html")

@app.route('/vacationtodo/')
def vacationtodo():
    return render_template("vacationtodo.html")


@app.route('/pixel_art/')
def pixel_art():
    return render_template("pixel_art.html")

@app.route('/contactus/')
def contactus():
    return render_template("contactus.html")

@app.route('/map/')
def map():
    return render_template("map.html")

@app.route('/AmusementParksBookTickets/')
def AmusementParksBookTickets():
    return render_template("AmusementParksBookTickets.html")

@app.route('/ContactOthers/')
def contactothers():
    return render_template("contactothers.html")

@app.route('/travelquiz/')
def travelquiz():
    return render_template("travelquiz.html")

@app.route('/foodquiz/')
def foodquiz():
    return render_template("foodquiz.html")

@app.route('/budget/')
def budget():
    return render_template("budget.html")

@app.route('/packinglist/')
def packinglist():
    return render_template("packinglist.html")


@app.route('/GoogleSearch/')
def GoogleSearch():
    return render_template("GoogleSearch.html")

@app.route('/TravelRecommendation/')
def TravelRecommendation():
    return render_template("TravelRecommendation.html")


# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True, port=8002)
