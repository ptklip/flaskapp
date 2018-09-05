from flask import (
  Flask, render_template, request, flash, redirect, url_for, session
)
import os

flaskapp = Flask(__name__.split('.')[0])

from app import routes

# Required for CSRF
flaskapp.config.update(dict(
    SECRET_KEY=os.environ['SECRET_KEY']
))

