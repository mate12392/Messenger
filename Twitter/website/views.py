from email import message_from_string
from flask import Blueprint, render_template, request
from flask import flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Friend, Message, User
from . import db
from .functions import getFriends, getMessages
from time import sleep
#import json
#import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    q = Message.query.filter_by(sender_id = current_user.id).all()
    if len(q) == 0:
        dest = "home.html"
    else:
        last = Message.query.filter_by(sender_id = current_user.id).first()
        return redirect(url_for('views.messenger', usr_id = last.__dict__['id'] ))
    
    

    return render_template(dest, user=current_user)

@views.route('/t/<usr_id>', methods=['GET', 'POST'])
def messenger(usr_id):
    """is_friend = getFriends(usr_id)
    if is_friend:"""

    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            new_message = Message(data = message, sender_id = current_user.id, reciever_id =  usr_id)
            db.session.add(new_message)
            db.session.commit()
            print()
    
    rec_name = db.session.query(User).filter_by(id=usr_id).first().__dict__['last_name'].capitalize() + " " + db.session.query(User).filter_by(id=usr_id).first().__dict__['first_name'].capitalize()

    #rec_Name = User.query.filter_by(id=usr_id).first().__dict__['last_name'].capitalize() + " " + User.query.filter_by(id=usr_id).first().__dict__['first_name'].capitalize()
    rec_name = User.query.filter_by(id=usr_id).first().__dict__['username']
    rec_user = db.session.query(Message).filter_by(sender_id=usr_id).all()

    messages = getMessages(rec_user)

    

    return render_template('messenger.html', user=current_user, sender=current_user.id, reciever=int(usr_id), rec_name=rec_name, rec_Names=rec_Name, messages=messages)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return render_template("profile.html", user=current_user)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template("profile.html", user=current_user)
        if file:
            filename = f"{current_user.username}.png"
            file.save(f"website/static/images/{filename}")

    return render_template("profile.html", user=current_user)