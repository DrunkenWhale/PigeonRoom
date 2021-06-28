from flask import Blueprint, send_from_directory, redirect
import os

static_html_bp = Blueprint('static_html', __name__)


# websocket

@static_html_bp.route('/html/<path:path>')
def static_html(path):
    return send_from_directory(os.getcwd() + '/html', path)


@static_html_bp.route('/index')
@static_html_bp.route('/')
def index():
    return redirect('/html/index.html')