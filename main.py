# import "packages" from flask
from flask import Flask, render_template

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

@app.route('/AboutDylan/')
def AboutDylan():
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

@app.route('/isabelle', methods=['GET', 'POST'])
def isabelle():
    return render_template("isabelle.html")

@app.route('/jean', methods=['GET', 'POST'])
def jean():
    return render_template("jean.html")

# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
