"""control dependencies to support CRUD app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from foodsql import *

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
foodiefinder = Blueprint('food', __name__,
                     url_prefix='/create_task',
                     template_folder='templates/create_task/',
                     static_folder='static',
                     static_url_path='static')

""" Application control for CRUD is main focus of this File, key features:
    1.) User table queries
    2.) app routes for CRUD (Blueprint)
"""


# Default URL
@foodiefinder.route('/')
def crud():
    """obtains all Users from table and loads Admin Form"""
    return render_template("foodieFinder.html", table=foods_all())


# CRUD create/add
@foodiefinder.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = foods(
            request.form.get("restaurantName"),
            request.form.get("foodName"),
        )
        po.create()
    return redirect(url_for('create_task.foodieFinder'))


# CRUD read
@foodiefinder.route('/read/', methods=["POST"])
def read():
    """gets userid from form and obtains corresponding data from Users table"""
    table = []
    if request.form:
        restaurantID = request.form.get("restaurantID")
        po = restaurant_by_id(restaurantID)
        if po is not None:
            table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("foodieFinder.html", table=table)


# CRUD update
@foodiefinder.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""
    if request.form:
        restaurantID = request.form.get("restaurantID")
        name = request.form.get("name")
        po = restaurant_by_id(restaurantID)
        if po is not None:
            po.update(name)
    return redirect(url_for('create_task.foodieFinder'))


# CRUD delete
@foodiefinder.route('/delete/', methods=["POST"])
def delete():
    """gets userid from form delete corresponding record from Users table"""
    if request.form:
        restaurantID = request.form.get("restaurantID")
        po = restaurant_by_id(restaurantID)
        if po is not None:
            po.delete()
    return redirect(url_for('create_task.foodieFinder'))


# Search Form
@foodiefinder.route('/search/')
def search():
    """loads form to search Users data"""
    return render_template("foodieFinder.html")


# Search request and response
@foodiefinder.route('/search/term/', methods=["POST"])
def search_term():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    response = make_response(jsonify(foods_ilike(term)), 200)
    return response
