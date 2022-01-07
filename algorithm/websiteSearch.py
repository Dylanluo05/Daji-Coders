from flask import Flask, render_template, request
from __init__ import app

@app.route('/')
def searchWeb():
    return render_template("searchWebsite.html")