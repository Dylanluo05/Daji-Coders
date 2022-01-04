from flask import Flask, render_template, request
from __init__ import app
import requests

@app.route('/')
def register():
    return render_template("user_registration.html")