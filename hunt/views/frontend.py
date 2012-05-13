
from flask import Blueprint, request, render_template, current_app,\
     send_from_directory

frontend = Blueprint('frontend', __name__)



@frontend.route('/')
def index():
    return render_template('layout.html')



@frontend.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.config['UPLOADS_DEFAULT_DEST'],
                               'images/favicon.ico', as_attachment=False)
