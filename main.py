# import "packages" from flask
from flask import Flask, render_template, request
import requests
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


@app.route('/AboutAlex/')
def AboutAlex():
    return render_template("AboutAlex.html")


@app.route('/AboutDylan/', methods=['GET', 'POST'])
def greet1():
    # submit button has been pushed
    if request.form:
        name = request.form.get("name")
        if len(name) != 0:  # input field has content
            return render_template("AboutDylan.html", name=name)
    # starting and empty input default
    return render_template("AboutDylan.html", name1="World")

@app.route('/AboutDylan/')
def greet():
    return render_template("AboutDylan.html")

@app.route('/AboutIsabelle/')
def AboutIsabelle():
    return render_template("AboutIsabelle.html")

@app.route('/AboutJean/')
def AboutJean():
    return render_template("AboutJean.html")

@app.route('/HotelSearch/')
def HotelSearch():
    return render_template("HotelSearch.html")

@app.route('/jean', methods=['GET', 'POST'])
def jean():
    return render_template("jean.html")

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
