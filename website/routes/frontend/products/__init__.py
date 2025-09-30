from website.app import db
from sqlalchemy import text
import os

from flask import Blueprint, redirect, render_template, url_for

productpages = Blueprint('productpages', __name__, template_folder="templates", static_folder='static', url_prefix='/products')