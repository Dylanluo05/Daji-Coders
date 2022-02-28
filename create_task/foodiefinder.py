"""control dependencies to support CRUD app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_restful import Api, Resource
import requests

from create_task.foodModel import foods

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
foodiefinder = Blueprint('create_task', __name__,
                         url_prefix='/create_task',
                         template_folder='templates/create_task/',
                         static_folder='static',
                         static_url_path='assets')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
foodApi = Api(foodiefinder)




# User/Users extraction from SQL
def foods_all():
    """converts Users table into JSON list """
    return [food.read() for food in foods.query.all()]


def foods_ilike(term):
    """filter Users table by term into JSON list """
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = foods.query.filter((foods.restaurantName.ilike(term)) | (foods.foodName.ilike(term)))
    return [food.read() for food in table]


# User extraction from SQL
def restaurant_by_id(restaurantID):
    """finds User in table matching userid """
    return foods.query.filter_by(restaurantID=restaurantID).first()


# User extraction from SQL
def food_by_name(foodName):
    """finds User in table matching email """
    return foods.query.filter_by(foodName=foodName).first()


""" app route section """


# Default URL
@foodiefinder.route('/', methods=['GET', 'POST'])
def foodiefinder():
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
    return render_template("create_task/foodieFinder.html", table=table)


# CRUD update
@foodiefinder.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""
    if request.form:
        restaurantID = request.form.get("restaurantID")
        restaurantName = request.form.get("restaurantName")
        po = restaurant_by_id(restaurantID)
        if po is not None:
            po.update(restaurantName)
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
    return render_template("create_task/foodieFinder.html", term=search)

# Search request and response
@foodiefinder.route('/search/term/', methods=["POST"])
def search_term():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    response = make_response(jsonify(foods_ilike(term)), 200)
    return response


""" API routes section """


class foodAPI:
    # class for create/post
    class _Create(Resource):
        def post(self, restaurantName, foodName):
            po = foods(restaurantName, foodName)
            person = po.create()
            if person:
                return person.read()
            return {'message': f'Processed {restaurantName}, either a format error or {foodName} is duplicate'}, 210

    # class for read/get
    class _Read(Resource):
        def get(self):
            return foods_all()

    # class for read/get
    class _ReadILike(Resource):
        def get(self, term):
            return foods_ilike(term)

    # class for update/put
    class _Update(Resource):
        def put(self, foodName, restaurantName):
            po = food_by_name(foodName)
            if po is None:
                return {'message': f"{foodName} is not found"}, 210
            po.update(restaurantName)
            return po.read()

    class _UpdateAll(Resource):
        def put(self, foodName, restaurantName):
            po = food_by_name(foodName)
            if po is None:
                return {'message': f"{foodName} is not found"}, 210
            po.update(restaurantName)
            return po.read()

    # class for delete
    class _Delete(Resource):
        def delete(self, restaurantID):
            po = restaurant_by_id(restaurantID)
            if po is None:
                return {'message': f"{restaurantID} is not found"}, 210
            data = po.read()
            po.delete()
            return data

    # building RESTapi resource
#     foodApi.add_resource(_Create, '/create/<string:pageName>/<string:pageURL>/<string:pageDesc>')
#     foodApi.add_resource(_Read, '/read/')
#     foodApi.add_resource(_ReadILike, '/read/ilike/<string:term>')
#     foodApi.add_resource(_Update, '/update/<string:pageURL>/<string:pageName>')
#     foodApi.add_resource(_UpdateAll, '/update/<string:pageURL>/<string:pageName>/<string:pageDesc>')
#     foodApi.add_resource(_Delete, '/delete/<int:pageID>')
#
#
# """ API testing section """
#
#
# def webApi_tester():
#     # local host URL for model
#     url = 'http://localhost:5222/searchWebsite'
#
#     # test conditions
#     API = 0
#     METHOD = 1
#     tests = [
#         #        ['/create/Boat Search/wilma@bedrock.org/123wifli/0001112222', "post"],
#         #        ['/create/Fred Flintstone/fred@bedrock.org/123wifli/0001112222', "post"],
#         #        ['/read/', "get"],
#         #        ['/read/ilike/John', "get"],
#         #        ['/read/ilike/com', "get"],
#         #        ['/update/wilma@bedrock.org/Wilma S Flintstone/123wsfli/0001112229', "put"],
#         #        ['/update/wilma@bedrock.org/Wilma Slaghoople Flintstone', "put"],
#         #        ['/delete/4', "delete"],
#         #        ['/delete/5', "delete"],
#     ]
#
#     # loop through each test condition and provide feedback
#     for test in tests:
#         print()
#         print(f"({test[METHOD]}, {url + test[API]})")
#         if test[METHOD] == 'get':
#             response = requests.get(url + test[API])
#         elif test[METHOD] == 'post':
#             response = requests.post(url + test[API])
#         elif test[METHOD] == 'put':
#             response = requests.put(url + test[API])
#         elif test[METHOD] == 'delete':
#             response = requests.delete(url + test[API])
#         else:
#             print("unknown RESTapi method")
#             continue
#
#         print(response)
#         try:
#             print(response.json())
#         except:
#             print("unknown error")
#
#
# def webApi_printer():
#     print()
#     print("pages table")
#     for page in pages_all():
#         print(page)
#
#
# # """validating api's requires server to be running"""
# if __name__ == "__main__":
#     webApi_tester()
#     webApi_printer()