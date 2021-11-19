# import "packages" from flask
from flask import Flask, render_template, request

# create a Flask instance
app = Flask(__name__)


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

@app.route('/stub/')
def stub():
    return render_template("stub.html")

@app.route('/jean', methods=['GET', 'POST'])
def jean():
    return render_template("jean.html")

# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
