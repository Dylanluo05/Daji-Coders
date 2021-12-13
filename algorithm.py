from flask import Blueprint, render_template, request

app_algorithm = Blueprint('algorithm', __name__,
                          url_prefix='/algorithm',
                          template_folder='templates/algorithm',
                          static_folder='static',
                          static_url_path='assets')