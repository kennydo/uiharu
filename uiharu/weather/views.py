import logging

from flask import Blueprint, render_template


weather = Blueprint('weather', __name__,
                    template_folder='templates', static_folder='static')
log = logging.getLogger(__name__)


@weather.route('/')
def root():
    return render_template('index.html')
