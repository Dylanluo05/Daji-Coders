from flask import Blueprint, render_template

app_y2022 = Blueprint('y2022', __name__,
                      url_prefix='/y2022',
                      template_folder='templates',
                      static_folder='static', static_url_path='/static/assets')