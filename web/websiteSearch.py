"""control dependencies to support CRUD app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_restful import Api, Resource
import requests

from web.webModel import webPages

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
websiteSearch = Blueprint('web', __name__,
                     url_prefix='/algorithm/web',
                     template_folder='templates/web/',
                     static_folder='static',
                     static_url_path='assets')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
webApi = Api(websiteSearch)




# User/Users extraction from SQL
def pages_all():
    """converts Users table into JSON list """
    return [page.read() for page in webPages.query.all()]


def pages_ilike(term):
    """filter Users table by term into JSON list """
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = webPages.query.filter((webPages.pageName.ilike(term)) | (webPages.pageURL.ilike(term)))
    return [page.read() for page in table]


# User extraction from SQL
def page_by_id(pageID):
    """finds User in table matching userid """
    return webPages.query.filter_by(pageID=pageID).first()


# User extraction from SQL
def page_by_URL(pageURL):
    """finds User in table matching email """
    return webPages.query.filter_by(pageURL=pageURL).first()


""" app route section """


# Default URL
@websiteSearch.route('/', methods=['GET', 'POST'])
def searchWebsite():
    """obtains all Users from table and loads Admin Form"""
    if request.form:
        term = request.form.get("term")
        if len(term) != 0:
            return render_template("web/searchWebsite.html", term=term)
    return render_template("web/searchWebsite.html", term="")


# CRUD create/add
@websiteSearch.route('/create/', methods=['GET', 'POST'])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = webPages(
            request.form.get("pageName"),
            request.form.get("pageURL"),
            request.form.get("pageDesc"),
        )
        po.create()
    return redirect(url_for('web.enterWeb'))


# CRUD read
@websiteSearch.route('/read/', methods=["POST"])
def read():
    """gets userid from form and obtains corresponding data from Users table"""
    table = []
    if request.form:
        pageID = request.form.get("pageID")
        po = page_by_id(pageID)
        if po is not None:
            table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("web/enterWeb.html", table=table)


# CRUD update
@websiteSearch.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""
    if request.form:
        pageID = request.form.get("pageID")
        pageName = request.form.get("pageName")
        po = page_by_id(pageID)
        if po is not None:
            po.update(pageName)
    return redirect(url_for('web.enterWeb'))


# CRUD delete
@websiteSearch.route('/delete/', methods=["POST"])
def delete():
    """gets userid from form delete corresponding record from Users table"""
    if request.form:
        pageID = request.form.get("pageID")
        po = page_by_id(pageID)
        if po is not None:
            po.delete()
    return redirect(url_for('web.enterWeb'))


# Search Form
# @websiteSearch.route('/search/')
# def search():
#    """loads form to search Users data"""
#    return render_template("web/searchWebsite.html", term=search)

        # Search request and response
@websiteSearch.route('/search/term/', methods=["POST"])
def search_term():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    response = make_response(jsonify(pages_ilike(term)), 200)
    return response


""" API routes section """


class PagesAPI:
    # class for create/post
    class _Create(Resource):
        def post(self, pageName, pageURL, pageDesc):
            po = webPages(pageName, pageURL, pageDesc)
            person = po.create()
            if person:
                return person.read()
            return {'message': f'Processed {pageName}, either a format error or {pageURL} is duplicate'}, 210

    # class for read/get
    class _Read(Resource):
        def get(self):
            return pages_all()

    # class for read/get
    class _ReadILike(Resource):
        def get(self, term):
            return pages_ilike(term)

    # class for update/put
    class _Update(Resource):
        def put(self, pageURL, pageName):
            po = page_by_URL(pageURL)
            if po is None:
                return {'message': f"{pageURL} is not found"}, 210
            po.update(pageName)
            return po.read()

    class _UpdateAll(Resource):
        def put(self, pageURL, pageName, pageDesc):
            po = page_by_URL(pageURL)
            if po is None:
                return {'message': f"{pageURL} is not found"}, 210
            po.update(pageName, pageDesc)
            return po.read()

    # class for delete
    class _Delete(Resource):
        def delete(self, pageID):
            po = page_by_id(pageID)
            if po is None:
                return {'message': f"{pageID} is not found"}, 210
            data = po.read()
            po.delete()
            return data

    # building RESTapi resource
    webApi.add_resource(_Create, '/create/<string:pageName>/<string:pageURL>/<string:pageDesc>')
    webApi.add_resource(_Read, '/read/')
    webApi.add_resource(_ReadILike, '/read/ilike/<string:term>')
    webApi.add_resource(_Update, '/update/<string:pageURL>/<string:pageName>')
    webApi.add_resource(_UpdateAll, '/update/<string:pageURL>/<string:pageName>/<string:pageDesc>')
    webApi.add_resource(_Delete, '/delete/<int:pageID>')


""" API testing section """


def webApi_tester():
    # local host URL for model
    url = 'http://localhost:5222/searchWebsite'

    # test conditions
    API = 0
    METHOD = 1
    tests = [
#        ['/create/Boat Search/wilma@bedrock.org/123wifli/0001112222', "post"],
#        ['/create/Fred Flintstone/fred@bedrock.org/123wifli/0001112222', "post"],
#        ['/read/', "get"],
#        ['/read/ilike/John', "get"],
#        ['/read/ilike/com', "get"],
#        ['/update/wilma@bedrock.org/Wilma S Flintstone/123wsfli/0001112229', "put"],
#        ['/update/wilma@bedrock.org/Wilma Slaghoople Flintstone', "put"],
#        ['/delete/4', "delete"],
#        ['/delete/5', "delete"],
    ]

    # loop through each test condition and provide feedback
    for test in tests:
        print()
        print(f"({test[METHOD]}, {url + test[API]})")
        if test[METHOD] == 'get':
            response = requests.get(url + test[API])
        elif test[METHOD] == 'post':
            response = requests.post(url + test[API])
        elif test[METHOD] == 'put':
            response = requests.put(url + test[API])
        elif test[METHOD] == 'delete':
            response = requests.delete(url + test[API])
        else:
            print("unknown RESTapi method")
            continue

        print(response)
        try:
            print(response.json())
        except:
            print("unknown error")


def webApi_printer():
    print()
    print("pages table")
    for page in pages_all():
        print(page)


# """validating api's requires server to be running"""
if __name__ == "__main__":
    webApi_tester()
    webApi_printer()