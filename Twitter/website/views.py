from flask import Blueprint, render_template, request
from flask import flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Tweet
from . import db
import json
import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template(dest, user=current_user)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = f"{current_user.username}.png"
            file.save(f"website/templates/upload/{filename}"""
    dest = "home.html"
    
    return render_template(dest, user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template(dest, user=current_user)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = f"{current_user.username}.png"
            file.save(f"website/static/images/{filename}")

    return render_template("profile.html", user=current_user)