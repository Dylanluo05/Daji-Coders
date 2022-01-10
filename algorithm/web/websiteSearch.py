from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_restful import Api, Resource
import requests

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_websearch = Blueprint('websearch', __name__,
                     url_prefix='/algorithm/web',
                     template_folder='templates/web/',
                     static_folder='static',
                     static_url_path='assets')