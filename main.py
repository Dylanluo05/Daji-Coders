# import "packages" from flask
from flask import Flask, render_template, request
import requests
import json
from api.jeanapi import api_bp

# create a Flask instance
app = Flask(__name__)
app.register_blueprint(api_bp)

# connects default URL to render index.html
@app.route('/')
def index():
    return render_template("index.html")


# connects /kangaroos path to render kangaroos.html
@app.route('/kangaroos/')
def kangaroos():
    return render_template("kangaroos.html")

@app.route('/hawkers/')
def hawkers():
    return render_template("hawkers.html")

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

# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
