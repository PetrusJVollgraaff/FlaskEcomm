
from flask import render_template
from . import modules

@modules.route('/')
def index():
    return  render_template("dashboard.html")