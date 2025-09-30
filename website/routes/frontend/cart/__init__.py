from website.app import db
from flask import Blueprint, jsonify, render_template, session, request


cartpages = Blueprint('cartpages', __name__, template_folder="templates", url_prefix="/cart")